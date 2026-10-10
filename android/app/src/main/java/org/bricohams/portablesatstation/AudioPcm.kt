package org.bricohams.portablesatstation

import java.io.EOFException
import java.io.IOException
import java.io.InputStream
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin
import kotlin.math.sqrt

internal data class PcmAudio(val samples: ShortArray, val sampleRate: Int)

internal data class PcmBlock(
    val sequence: Long,
    val firstSampleCounter: Long,
    val samples: ShortArray
)

internal interface PcmSource {
    val sampleRate: Int
    fun readBlock(maxSamples: Int): PcmBlock?
}

internal interface PcmSink {
    val sampleRate: Int
    fun write(block: PcmBlock)
}

internal class PcmArraySource(
    private val samples: ShortArray,
    override val sampleRate: Int,
    private val blockSize: Int = 2048
) : PcmSource {
    private var offset = 0
    private var sequence = 0L

    init {
        require(sampleRate in 8000..48000)
        require(blockSize > 0)
    }

    override fun readBlock(maxSamples: Int): PcmBlock? {
        require(maxSamples > 0)
        if (offset >= samples.size) return null
        val start = offset
        val end = minOf(samples.size, start + minOf(maxSamples, blockSize))
        offset = end
        return PcmBlock(sequence++, start.toLong(), samples.copyOfRange(start, end))
    }
}

internal class BoundedPcmBuffer(
    override val sampleRate: Int,
    maxSamples: Int
) : PcmSink {
    private val storage = ShortArray(maxSamples.also {
        require(sampleRate in 8000..48000 && it in 1..sampleRate * AudioPcm.MAX_CAPTURE_SECONDS)
    })
    private var size = 0
    private var nextSequence: Long? = null
    private var expectedSampleCounter: Long? = null

    override fun write(block: PcmBlock) {
        if ((nextSequence != null && block.sequence != nextSequence) ||
            (expectedSampleCounter != null && block.firstSampleCounter != expectedSampleCounter))
            throw ProtocolFailure("pcm_discontinuity")
        if (block.samples.isEmpty() || block.samples.size > storage.size - size)
            throw ProtocolFailure("audio_duration_limit")
        if (block.sequence == Long.MAX_VALUE || block.firstSampleCounter > Long.MAX_VALUE - block.samples.size)
            throw ProtocolFailure("pcm_counter_overflow")
        block.samples.copyInto(storage, size)
        size += block.samples.size
        nextSequence = block.sequence + 1
        expectedSampleCounter = block.firstSampleCounter + block.samples.size
    }

    fun toAudio(): PcmAudio {
        if (size == 0) throw ProtocolFailure("audio_too_short")
        return PcmAudio(storage.copyOf(size), sampleRate)
    }
}

internal fun PcmSource.copyTo(sink: PcmSink, maxSamples: Int, cancelled: () -> Boolean = { false }): Long {
    require(maxSamples > 0)
    if (sampleRate !in 8000..48000 || sampleRate != sink.sampleRate)
        throw ProtocolFailure("pcm_sample_rate")
    var copied = 0L
    while (copied < maxSamples) {
        if (cancelled() || Thread.currentThread().isInterrupted)
            throw java.util.concurrent.CancellationException()
        val block = readBlock(minOf(4096, (maxSamples - copied).toInt())) ?: break
        if (block.samples.size > minOf(4096L, maxSamples.toLong() - copied).toInt())
            throw ProtocolFailure("pcm_block_size")
        sink.write(block)
        copied += block.samples.size
    }
    return copied
}

internal object AudioPcm {
    const val TARGET_SAMPLE_RATE = 11025
    const val MAX_CAPTURE_SECONDS = 240
    const val MAX_WAV_BYTES = 50 * 1024 * 1024
    private const val MIN_SAMPLE_RATE = 8000
    private const val MAX_SAMPLE_RATE = 48000

    fun resample(input: ShortArray, sourceRate: Int, cancelled: () -> Boolean = { false }): PcmAudio {
        if (sourceRate !in MIN_SAMPLE_RATE..MAX_SAMPLE_RATE || input.isEmpty())
            throw ProtocolFailure("audio_sample_rate")
        if (input.size.toLong() > sourceRate.toLong() * MAX_CAPTURE_SECONDS)
            throw ProtocolFailure("audio_duration_limit")
        if (sourceRate == TARGET_SAMPLE_RATE) return PcmAudio(input, sourceRate)

        val outputLength = ((input.size.toLong() * TARGET_SAMPLE_RATE + sourceRate / 2) / sourceRate)
            .toInt()
        if (outputLength !in 1..(TARGET_SAMPLE_RATE * MAX_CAPTURE_SECONDS))
            throw ProtocolFailure("audio_duration_limit")

        val output = ShortArray(outputLength)
        val cutoff = 0.45 * minOf(1.0, TARGET_SAMPLE_RATE.toDouble() / sourceRate)
        val radius = 16
        for (outIndex in output.indices) {
            if (outIndex % 4096 == 0 && (cancelled() || Thread.currentThread().isInterrupted))
                throw java.util.concurrent.CancellationException()
            val position = outIndex.toDouble() * sourceRate / TARGET_SAMPLE_RATE
            val center = position.toInt()
            var weighted = 0.0
            var weightSum = 0.0
            for (offset in -radius + 1..radius) {
                val sourceIndex = center + offset
                if (sourceIndex !in input.indices) continue
                val distance = sourceIndex - position
                val sinc = if (distance == 0.0) 2.0 * cutoff
                    else sin(2.0 * PI * cutoff * distance) / (PI * distance)
                val windowPosition = (distance / radius).coerceIn(-1.0, 1.0)
                val window = 0.5 + 0.5 * cos(PI * windowPosition)
                val weight = sinc * window
                weighted += input[sourceIndex] * weight
                weightSum += weight
            }
            val value = if (weightSum == 0.0) 0.0 else weighted / weightSum
            output[outIndex] = value.roundToInt().coerceIn(Short.MIN_VALUE.toInt(), Short.MAX_VALUE.toInt()).toShort()
        }
        return PcmAudio(output, TARGET_SAMPLE_RATE)
    }
}

internal object PcmWav {
    fun encodeS16(samples: ShortArray, sampleRate: Int): ByteArray {
        if (sampleRate !in MIN_WAV_SAMPLE_RATE..MAX_WAV_SAMPLE_RATE || samples.isEmpty() ||
            samples.size.toLong() > sampleRate.toLong() * AudioPcm.MAX_CAPTURE_SECONDS)
            throw ProtocolFailure("wav_output_limit")
        val dataSize = samples.size * 2
        if (dataSize > AudioPcm.MAX_WAV_BYTES - 44)
            throw ProtocolFailure("wav_output_limit")
        val output = java.io.ByteArrayOutputStream(44 + dataSize)
        PcmWavSink(output, sampleRate, samples.size).use { sink ->
            PcmArraySource(samples, sampleRate).copyTo(sink, samples.size)
        }
        return output.toByteArray()
    }

    internal class PcmWavSink(
        private val output: java.io.OutputStream,
        override val sampleRate: Int,
        private val expectedSamples: Int
    ) : PcmSink, java.io.Closeable {
        private var writtenSamples = 0
        private var nextSequence: Long? = null
        private var expectedSampleCounter: Long? = null
        private var closed = false

        init {
            if (sampleRate !in 8000..48000 || expectedSamples !in 1..sampleRate * AudioPcm.MAX_CAPTURE_SECONDS ||
                expectedSamples.toLong() * 2 > AudioPcm.MAX_WAV_BYTES - 44)
                throw ProtocolFailure("wav_output_limit")
            fun word(value: Int) { output.write(value and 0xff); output.write((value ushr 8) and 0xff) }
            fun dword(value: Int) { word(value); word(value ushr 16) }
            fun text(value: String) { output.write(value.toByteArray(Charsets.US_ASCII)) }
            val dataSize = expectedSamples * 2
            text("RIFF"); dword(36 + dataSize); text("WAVEfmt "); dword(16)
            word(1); word(1); dword(sampleRate); dword(sampleRate * 2); word(2); word(16)
            text("data"); dword(dataSize)
        }

        override fun write(block: PcmBlock) {
            check(!closed) { "PCM WAV sink is closed" }
            if ((nextSequence != null && block.sequence != nextSequence) ||
                (expectedSampleCounter != null && block.firstSampleCounter != expectedSampleCounter))
                throw ProtocolFailure("pcm_discontinuity")
            if (block.samples.isEmpty() || block.samples.size > expectedSamples - writtenSamples)
                throw ProtocolFailure("wav_output_length")
            if (block.sequence == Long.MAX_VALUE || block.firstSampleCounter > Long.MAX_VALUE - block.samples.size)
                throw ProtocolFailure("pcm_counter_overflow")
            for (sample in block.samples) {
                val value = sample.toInt() and 0xffff
                output.write(value and 0xff)
                output.write((value ushr 8) and 0xff)
            }
            writtenSamples += block.samples.size
            nextSequence = block.sequence + 1
            expectedSampleCounter = block.firstSampleCounter + block.samples.size
        }

        override fun close() {
            if (closed) return
            closed = true
            try {
                if (writtenSamples != expectedSamples) throw ProtocolFailure("wav_output_length")
            } finally {
                output.close()
            }
        }
    }

    private const val MIN_WAV_SAMPLE_RATE = 8000
    private const val MAX_WAV_SAMPLE_RATE = 48000

    fun read(input: InputStream, cancelled: () -> Boolean = { false }): PcmAudio = try {
        readChecked(input, cancelled)
    } catch (_: EOFException) {
        throw ProtocolFailure("wav_truncated")
    }

    private fun readChecked(input: InputStream, cancelled: () -> Boolean): PcmAudio {
        val reader = BoundedReader(input)
        if (reader.text(4) != "RIFF") throw ProtocolFailure("wav_riff")
        val riffSize = reader.unsignedInt()
        if (riffSize !in 4..(AudioPcm.MAX_WAV_BYTES - 8).toLong())
            throw ProtocolFailure("wav_size")
        if (reader.text(4) != "WAVE") throw ProtocolFailure("wav_wave")

        var format: WavFormat? = null
        var result: ShortArray? = null
        val riffEnd = riffSize + 8
        while (reader.bytesRead + 8 <= riffEnd) {
            if (cancelled() || Thread.currentThread().isInterrupted)
                throw java.util.concurrent.CancellationException()
            val chunkId = reader.text(4)
            val chunkSize = reader.unsignedInt()
            if (chunkSize > AudioPcm.MAX_WAV_BYTES.toLong() || reader.bytesRead + chunkSize > riffEnd)
                throw ProtocolFailure("wav_chunk_size")
            when (chunkId) {
                "fmt " -> {
                    if (format != null || chunkSize < 16) throw ProtocolFailure("wav_format")
                    val encoding = reader.unsignedShort()
                    val channels = reader.unsignedShort()
                    val sampleRate = reader.unsignedInt()
                    val byteRate = reader.unsignedInt()
                    val blockAlign = reader.unsignedShort()
                    val bits = reader.unsignedShort()
                    val bytesPerSample = bits / 8
                    if (encoding != 1 || channels !in 1..2 ||
                        sampleRate !in 8000L..48000L || bits !in setOf(8, 16, 24, 32) ||
                        blockAlign != channels * bytesPerSample ||
                        byteRate != sampleRate * blockAlign)
                        throw ProtocolFailure("wav_pcm_format")
                    format = WavFormat(channels, sampleRate.toInt(), bits, blockAlign)
                    reader.skip(chunkSize - 16)
                }
                "data" -> {
                    val pcmFormat = format ?: throw ProtocolFailure("wav_format_missing")
                    if (result != null || chunkSize % pcmFormat.blockAlign != 0L)
                        throw ProtocolFailure("wav_data")
                    val frames = chunkSize / pcmFormat.blockAlign
                    if (frames !in 1..(pcmFormat.sampleRate.toLong() * AudioPcm.MAX_CAPTURE_SECONDS))
                        throw ProtocolFailure("audio_duration_limit")
                    val mono = ShortArray(frames.toInt())
                    val bytesPerSample = pcmFormat.bits / 8
                    for (frame in mono.indices) {
                        if (frame % 8192 == 0 && (cancelled() || Thread.currentThread().isInterrupted))
                            throw java.util.concurrent.CancellationException()
                        var sum = 0L
                        repeat(pcmFormat.channels) {
                            val sample = when (pcmFormat.bits) {
                                8 -> ((reader.unsignedByte() - 128) shl 8)
                                16 -> reader.signedShort()
                                24 -> reader.signed24() shr 8
                                32 -> reader.signedInt() shr 16
                                else -> throw ProtocolFailure("wav_pcm_format")
                            }
                            sum += sample
                        }
                        mono[frame] = (sum / pcmFormat.channels)
                            .coerceIn(Short.MIN_VALUE.toLong(), Short.MAX_VALUE.toLong()).toShort()
                    }
                    result = mono
                }
                else -> reader.skip(chunkSize)
            }
            if (chunkSize and 1L != 0L) reader.skip(1)
        }
        val mono = result ?: throw ProtocolFailure("wav_data_missing")
        val pcmFormat = format ?: throw ProtocolFailure("wav_format_missing")
        return AudioPcm.resample(mono, pcmFormat.sampleRate, cancelled)
    }

    private data class WavFormat(val channels: Int, val sampleRate: Int, val bits: Int, val blockAlign: Int)

    private class BoundedReader(private val input: InputStream) {
        var bytesRead = 0L
            private set

        fun text(count: Int): String = readBytes(count).toString(Charsets.US_ASCII)
        fun unsignedByte(): Int = readByte()
        fun unsignedShort(): Int = readByte() or (readByte() shl 8)
        fun signedShort(): Int = unsignedShort().toShort().toInt()
        fun signed24(): Int {
            val value = readByte() or (readByte() shl 8) or (readByte() shl 16)
            return if (value and 0x800000 != 0) value or -0x1000000 else value
        }
        fun signedInt(): Int = readByte() or (readByte() shl 8) or (readByte() shl 16) or (readByte() shl 24)
        fun unsignedInt(): Long = signedInt().toLong() and 0xffffffffL

        fun skip(count: Long) {
            if (count < 0) throw ProtocolFailure("wav_chunk_size")
            var remaining = count
            val buffer = ByteArray(4096)
            while (remaining > 0) {
                val read = input.read(buffer, 0, minOf(buffer.size.toLong(), remaining).toInt())
                if (read < 0) throw EOFException("Truncated WAV")
                if (read == 0) continue
                bytesRead += read
                if (bytesRead > AudioPcm.MAX_WAV_BYTES) throw ProtocolFailure("wav_size")
                remaining -= read
            }
        }

        private fun readByte(): Int {
            val value = input.read()
            if (value < 0) throw EOFException("Truncated WAV")
            bytesRead++
            if (bytesRead > AudioPcm.MAX_WAV_BYTES) throw ProtocolFailure("wav_size")
            return value
        }

        private fun readBytes(count: Int): ByteArray {
            if (count < 0) throw IOException("Invalid WAV field")
            val result = ByteArray(count)
            for (index in result.indices) result[index] = readByte().toByte()
            return result
        }
    }
}
