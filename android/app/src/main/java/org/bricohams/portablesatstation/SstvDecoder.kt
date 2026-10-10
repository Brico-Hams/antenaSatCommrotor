package org.bricohams.portablesatstation

import kotlin.math.abs
import kotlin.math.floor
import kotlin.math.max
import kotlin.math.min
import kotlin.math.roundToInt

internal enum class SstvModeChoice { PD120, PD180 }

internal enum class SstvMode(
    val vis: Int,
    val componentMillis: Double
) {
    PD120(0x5f, 121.6),
    PD180(0x60, 183.04);

    val width = 640
    val height = 496
    val transmittedLines = height / 2
    val syncMillis = 20.0
    val porchMillis = 2.08
    val lineMillis = syncMillis + porchMillis + 4.0 * componentMillis
}

internal data class SstvImage(
    val mode: SstvMode,
    val pixels: IntArray,
    val headerStartSeconds: Double,
    val verifiedLines: Int
)

internal object SstvDecoder {
    private const val COARSE_STEP_SECONDS = 0.005
    private const val FREQ_SYNC = 1200.0
    private const val FREQ_VIS_LEADER = 1900.0
    private const val FREQ_BLACK = 1500.0
    private const val FREQ_WHITE = 2300.0
    private const val MIN_AMPLITUDE = 0.004
    private const val CHANNEL_EDGE_GUARD_SECONDS = 0.0018

    fun decode(
        input: ShortArray,
        sampleRate: Int,
        requestedMode: SstvModeChoice,
        cancelled: () -> Boolean = { false }
    ): SstvImage {
        val audio = AudioPcm.resample(input, sampleRate, cancelled)
        val demodulated = AudioDemodulator.demodulate(audio.samples, audio.sampleRate, cancelled)
        val coarse = coarseToneMap(demodulated)
        val headerIndex = findHeader(coarse.first, coarse.second)
        val visCode = readVis(coarse.first, coarse.second, headerIndex)
        val mode = when (visCode) {
            SstvMode.PD120.vis -> SstvMode.PD120
            SstvMode.PD180.vis -> SstvMode.PD180
            else -> throw ProtocolFailure("sstv_vis_unknown")
        }
        if (requestedMode.name != mode.name)
            throw ProtocolFailure("sstv_mode_mismatch")

        val imageStart = headerIndex * COARSE_STEP_SECONDS + 0.91
        val requiredDuration = imageStart + mode.transmittedLines * mode.lineMillis / 1000.0
        if (demodulated.durationSeconds + 0.002 < requiredDuration - 0.025)
            throw ProtocolFailure("sstv_image_truncated")

        val pixels = IntArray(mode.width * mode.height)
        val linePeriod = mode.lineMillis / 1000.0
        val componentDuration = mode.componentMillis / 1000.0
        for (line in 0 until mode.transmittedLines) {
            if (cancelled() || Thread.currentThread().isInterrupted)
                throw java.util.concurrent.CancellationException()
            val expectedSync = imageStart + line * linePeriod
            val syncTime = findSync(demodulated, expectedSync)
                ?: throw ProtocolFailure("sstv_sync_missing_$line")
            val porchTime = syncTime + mode.syncMillis / 1000.0 + mode.porchMillis / 2000.0
            if (!isTone(demodulated, porchTime, 1500.0, 220.0))
                throw ProtocolFailure("sstv_porch_invalid")

            var channelStart = syncTime + (mode.syncMillis + mode.porchMillis) / 1000.0
            val y0 = samplePlane(demodulated, channelStart, componentDuration, mode.width)
            channelStart += componentDuration
            val cr = samplePlane(demodulated, channelStart, componentDuration, mode.width)
            channelStart += componentDuration
            val cb = samplePlane(demodulated, channelStart, componentDuration, mode.width)
            channelStart += componentDuration
            val y1 = samplePlane(demodulated, channelStart, componentDuration, mode.width)
            writeRgbRow(pixels, 2 * line, y0, cb, cr)
            writeRgbRow(pixels, 2 * line + 1, y1, cb, cr)
        }
        return SstvImage(mode, pixels, headerIndex * COARSE_STEP_SECONDS, mode.transmittedLines)
    }

    private fun coarseToneMap(audio: DemodulatedAudio): Pair<FloatArray, FloatArray> {
        val count = floor(audio.durationSeconds / COARSE_STEP_SECONDS).toInt()
        val frequencies = FloatArray(count)
        val amplitudes = FloatArray(count)
        for (bin in 0 until count) {
            val start = audio.framePosition(bin * COARSE_STEP_SECONDS)
            val end = audio.framePosition((bin + 1) * COARSE_STEP_SECONDS)
            val first = max(0, start.toInt())
            val last = min(audio.frequencies.size, end.toInt() + 1)
            var frequencySum = 0.0
            var amplitudeSum = 0.0
            var valid = 0
            for (frame in first until last) {
                val frequency = audio.frequencies[frame]
                if (frequency > 0) {
                    frequencySum += frequency
                    amplitudeSum += audio.amplitudes[frame]
                    valid++
                }
            }
            if (valid > 0) {
                frequencies[bin] = (frequencySum / valid).toFloat()
                amplitudes[bin] = (amplitudeSum / valid).toFloat()
            }
        }
        return frequencies to amplitudes
    }

    private fun findHeader(frequencies: FloatArray, amplitudes: FloatArray): Int {
        val leaderBins = 60
        val breakBins = 2
        val totalBins = leaderBins * 2 + breakBins
        for (start in 0..frequencies.size - totalBins) {
            if (!stableTone(frequencies, amplitudes, start, leaderBins, FREQ_VIS_LEADER, 130.0, 0.78))
                continue
            if (!stableTone(frequencies, amplitudes, start + leaderBins, breakBins, FREQ_SYNC, 170.0, 0.5))
                continue
            if (stableTone(
                    frequencies, amplitudes, start + leaderBins + breakBins,
                    leaderBins, FREQ_VIS_LEADER, 130.0, 0.78
                ))
                return start
        }
        throw ProtocolFailure("sstv_header_not_found")
    }

    private fun stableTone(
        frequencies: FloatArray,
        amplitudes: FloatArray,
        start: Int,
        count: Int,
        expected: Double,
        tolerance: Double,
        requiredRatio: Double
    ): Boolean {
        var matching = 0
        for (index in start until start + count) {
            if (amplitudes[index] >= MIN_AMPLITUDE &&
                abs(frequencies[index] - expected) <= tolerance)
                matching++
        }
        return matching >= (count * requiredRatio).roundToInt()
    }

    private fun readVis(frequencies: FloatArray, amplitudes: FloatArray, headerIndex: Int): Int {
        val firstBit = headerIndex + 122
        fun frequencyOf(bit: Int): Double {
            val center = firstBit + bit * 6 + 3
            val values = (center - 1..center + 1).map { frequencies.getOrElse(it) { 0.0f }.toDouble() }
            if (values.any { it == 0.0 } ||
                (center - 1..center + 1).any { amplitudes.getOrElse(it) { 0.0f } < MIN_AMPLITUDE })
                throw ProtocolFailure("sstv_vis_invalid")
            return values.average()
        }

        if (abs(frequencyOf(0) - FREQ_SYNC) > 160.0 ||
            abs(frequencyOf(9) - FREQ_SYNC) > 160.0)
            throw ProtocolFailure("sstv_vis_invalid")
        var code = 0
        var parity = 0
        for (bit in 0 until 7) {
            val frequency = frequencyOf(bit + 1)
            val value = when {
                abs(frequency - 1100.0) <= 100.0 -> 1
                abs(frequency - 1300.0) <= 100.0 -> 0
                else -> throw ProtocolFailure("sstv_vis_invalid")
            }
            code = code or (value shl bit)
            parity = parity xor value
        }
        val parityFrequency = frequencyOf(8)
        val parityBit = when {
            abs(parityFrequency - 1100.0) <= 100.0 -> 1
            abs(parityFrequency - 1300.0) <= 100.0 -> 0
            else -> throw ProtocolFailure("sstv_vis_invalid")
        }
        if (parityBit != parity) throw ProtocolFailure("sstv_vis_parity")
        return code
    }

    private fun findSync(audio: DemodulatedAudio, expected: Double): Double? {
        var bestTime: Double? = null
        var bestScore = 0.0
        val step = 0.00036
        var candidate = expected - 0.020
        while (candidate <= expected + 0.025) {
            var matching = 0
            var valid = 0
            var errorSum = 0.0
            var time = candidate + 0.002
            val end = candidate + 0.018
            while (time <= end) {
                val frequency = audio.frequencyAt(time)
                val amplitude = audio.amplitudeAt(time)
                if (frequency.isFinite() && amplitude >= MIN_AMPLITUDE) {
                    valid++
                    if (frequency in 1080.0..1320.0) {
                        matching++
                        errorSum += abs(frequency - FREQ_SYNC)
                    }
                }
                time += 0.00072
            }
            val ratio = if (valid == 0) 0.0 else matching.toDouble() / valid
            val porchTime = candidate + SstvMode.PD120.syncMillis / 1000.0 +
                SstvMode.PD120.porchMillis / 2000.0
            if (ratio >= 0.82 && isTone(audio, porchTime, 1500.0, 220.0)) {
                val score = ratio - errorSum / max(1, matching) / 1000.0
                if (score > bestScore) {
                    bestScore = score
                    bestTime = candidate
                }
            }
            candidate += step
        }
        return bestTime
    }

    private fun isTone(audio: DemodulatedAudio, time: Double, expected: Double, tolerance: Double): Boolean {
        var matching = 0
        var valid = 0
        for (step in -2..2) {
            val sampleTime = time + step * 0.00018
            val frequency = audio.frequencyAt(sampleTime)
            if (frequency.isFinite() && audio.amplitudeAt(sampleTime) >= MIN_AMPLITUDE) {
                valid++
                if (abs(frequency - expected) <= tolerance) matching++
            }
        }
        return valid >= 4 && matching >= valid * 3 / 4
    }

    private fun samplePlane(audio: DemodulatedAudio, start: Double, duration: Double, width: Int): IntArray {
        val result = IntArray(width)
        val usableDuration = duration - 2.0 * CHANNEL_EDGE_GUARD_SECONDS
        for (pixel in 0 until width) {
            val time = start + CHANNEL_EDGE_GUARD_SECONDS + (pixel + 0.5) * usableDuration / width
            val frequency = audio.frequencyAt(time)
            val amplitude = audio.amplitudeAt(time)
            if (!frequency.isFinite() || amplitude < MIN_AMPLITUDE ||
                frequency !in 1250.0..2550.0)
                throw ProtocolFailure("sstv_scan_invalid")
            result[pixel] = (((frequency - FREQ_BLACK) * 255.0 / (FREQ_WHITE - FREQ_BLACK))
                .roundToInt()).coerceIn(0, 255)
        }
        return result
    }

    private fun writeRgbRow(pixels: IntArray, row: Int, y: IntArray, cb: IntArray, cr: IntArray) {
        val offset = row * y.size
        for (column in y.indices) {
            val luminance = y[column].toDouble()
            val blueDifference = cb[column] - 128.0
            val redDifference = cr[column] - 128.0
            val red = (luminance + 1.402 * redDifference).roundToInt().coerceIn(0, 255)
            val green = (luminance - 0.344136 * blueDifference - 0.714136 * redDifference)
                .roundToInt().coerceIn(0, 255)
            val blue = (luminance + 1.772 * blueDifference).roundToInt().coerceIn(0, 255)
            pixels[offset + column] = (0xff shl 24) or (red shl 16) or (green shl 8) or blue
        }
    }
}
