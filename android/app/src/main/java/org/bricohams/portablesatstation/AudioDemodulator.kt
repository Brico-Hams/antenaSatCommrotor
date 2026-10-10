package org.bricohams.portablesatstation

import kotlin.math.PI
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.sqrt

internal data class DemodulatedAudio(
    val sampleRate: Int,
    val hopSamples: Int,
    val firstFrameTime: Double,
    val frequencies: FloatArray,
    val amplitudes: FloatArray
) {
    val durationSeconds: Double
        get() = (frequencies.size - 1).coerceAtLeast(0) * hopSamples.toDouble() / sampleRate

    fun framePosition(timeSeconds: Double): Double =
        (timeSeconds - firstFrameTime) * sampleRate / hopSamples

    fun frequencyAt(timeSeconds: Double): Float = interpolate(frequencies, timeSeconds)
    fun amplitudeAt(timeSeconds: Double): Float = interpolate(amplitudes, timeSeconds)

    private fun interpolate(values: FloatArray, timeSeconds: Double): Float {
        val position = framePosition(timeSeconds)
        if (!position.isFinite() || position < 0.0 || position > values.lastIndex) return Float.NaN
        val lower = position.toInt()
        val upper = minOf(lower + 1, values.lastIndex)
        val fraction = position - lower
        return (values[lower] * (1.0 - fraction) + values[upper] * fraction).toFloat()
    }
}

internal object AudioDemodulator {
    private const val HILBERT_TAPS = 31
    private const val HOP_SAMPLES = 2
    private val hilbertCoefficients = DoubleArray(HILBERT_TAPS) { index ->
        val distance = index - HILBERT_TAPS / 2
        if (distance == 0 || distance % 2 == 0) 0.0
        else {
            val window = 0.54 - 0.46 * cos(2.0 * PI * index / (HILBERT_TAPS - 1))
            2.0 / (PI * distance) * window
        }
    }

    fun demodulate(samples: ShortArray, sampleRate: Int, cancelled: () -> Boolean = { false }): DemodulatedAudio {
        if (sampleRate != AudioPcm.TARGET_SAMPLE_RATE)
            throw ProtocolFailure("audio_not_resampled")
        if (samples.size < HILBERT_TAPS * 4) throw ProtocolFailure("audio_too_short")

        val delay = HILBERT_TAPS / 2
        val firstOutputSample = HILBERT_TAPS + HILBERT_TAPS % 2
        val lastOutputSample = samples.lastIndex - samples.lastIndex % HOP_SAMPLES
        val frameCount = (lastOutputSample - firstOutputSample) / HOP_SAMPLES + 1
        val frequencies = FloatArray(frameCount)
        val amplitudes = FloatArray(frameCount)
        var previousImaginary = hilbert(samples, firstOutputSample - 1, delay)
        var previousReal = samples[firstOutputSample - 1 - delay].toDouble() / 32768.0
        var outputIndex = 0

        for (index in firstOutputSample..lastOutputSample) {
            if (index % (HOP_SAMPLES * 8192) == 0 &&
                (cancelled() || Thread.currentThread().isInterrupted))
                throw java.util.concurrent.CancellationException()
            val imaginary = hilbert(samples, index, delay)
            val real = samples[index - delay].toDouble() / 32768.0
            val cross = imaginary * previousReal - real * previousImaginary
            val dot = real * previousReal + imaginary * previousImaginary
            if (index % HOP_SAMPLES == 0 && outputIndex < frameCount) {
                val frequency = atan2(cross, dot) * sampleRate / (2.0 * PI)
                val magnitude = sqrt(real * real + imaginary * imaginary)
                frequencies[outputIndex] =
                    if (frequency in 300.0..(sampleRate / 2.0)) frequency.toFloat() else 0.0f
                amplitudes[outputIndex] = magnitude.toFloat()
                outputIndex++
            }
            previousImaginary = imaginary
            previousReal = real
        }
        if (outputIndex == 0) throw ProtocolFailure("audio_too_short")
        return DemodulatedAudio(
            sampleRate,
            HOP_SAMPLES,
            (firstOutputSample - delay - 0.5) / sampleRate,
            frequencies.copyOf(outputIndex),
            amplitudes.copyOf(outputIndex)
        )
    }

    private fun hilbert(samples: ShortArray, end: Int, delay: Int): Double {
        var result = 0.0
        for (tap in hilbertCoefficients.indices) {
            val sampleIndex = end - tap
            if (sampleIndex >= 0)
                result += hilbertCoefficients[tap] * samples[sampleIndex].toDouble() / 32768.0
        }
        return result
    }
}
