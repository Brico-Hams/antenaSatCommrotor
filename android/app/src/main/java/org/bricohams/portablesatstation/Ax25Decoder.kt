package org.bricohams.portablesatstation

import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.util.ArrayDeque
import kotlin.math.floor
import kotlin.math.roundToInt

internal data class Ax25Address(val call: String, val ssid: Int, val repeated: Boolean = false) {
    override fun toString(): String = call + if (ssid == 0) "" else "-$ssid"
}

internal data class AprsInterpretation(
    val text: String,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val message: AprsMessage? = null
)

internal data class Ax25Packet(
    val destination: Ax25Address,
    val source: Ax25Address,
    val digipeaters: List<Ax25Address>,
    val control: Int,
    val pid: Int?,
    val information: ByteArray,
    val aprs: AprsInterpretation?
) {
    val path: String
        get() = buildString {
            append(source)
            append('>')
            append(destination)
            digipeaters.forEach {
                append(',')
                append(it)
                if (it.repeated) append('*')
            }
        }

    fun logEntry(): String {
        val raw = printablePayload(information)
        return buildString {
            append(path)
            append(" [FCS OK]")
            if (control == 0x03 || control == 0x13) {
                append(" UI")
                if (pid == 0xf0) append(" APRS")
            } else {
                append(" control=0x")
                append("%02X".format(control))
                pid?.let {
                    append(" PID=0x")
                    append("%02X".format(it))
                }
            }
            append('\n')
            append(aprs?.text ?: raw ?: "[non-printable information payload not rendered]")
        }
    }
}

private fun printablePayload(bytes: ByteArray): String? {
    if (bytes.any {
            val value = it.toInt() and 0xff
            value !in 32..126 && value != 10 && value != 13
        })
        return null
    return bytes.toString(Charsets.US_ASCII).trimEnd()
}

internal object Ax25Crc {
    fun crc16X25(bytes: ByteArray, offset: Int = 0, length: Int = bytes.size - offset): Int {
        if (offset < 0 || length < 0 || offset + length > bytes.size)
            throw IllegalArgumentException("Invalid CRC range")
        var crc = 0xffff
        for (index in offset until offset + length) {
            crc = crc xor (bytes[index].toInt() and 0xff)
            repeat(8) {
                crc = if (crc and 1 != 0) (crc ushr 1) xor 0x8408 else crc ushr 1
            }
        }
        return crc xor 0xffff
    }

    fun hasValidFcs(frame: ByteArray): Boolean {
        if (frame.size < 4) return false
        val received = (frame[frame.lastIndex - 1].toInt() and 0xff) or
            ((frame[frame.lastIndex].toInt() and 0xff) shl 8)
        return crc16X25(frame, 0, frame.size - 2) == received
    }
}

internal object AprsTextInterpreter {
    fun interpret(information: ByteArray): AprsInterpretation? {
        val text = try {
            Charsets.US_ASCII.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
                .decode(ByteBuffer.wrap(information)).toString()
        } catch (_: java.nio.charset.CharacterCodingException) {
            return null
        }
        if (text.any { it != '\r' && it != '\n' && it.code !in 32..126 }) return null
        return when (text.firstOrNull()) {
            '!', '=' -> position(text, 1)
            '/', '@' -> position(text, 8)
            ':' -> message(text)
            '>' -> AprsInterpretation("Status: ${text.drop(1).trimEnd()}")
            '?' -> AprsInterpretation("Query: ${text.drop(1).trimEnd()}")
            else -> AprsInterpretation("APRS text: ${text.trimEnd()}")
        }
    }

    private fun message(text: String): AprsInterpretation {
        val parsed = AprsMessageCodec.parse(text.toByteArray(Charsets.US_ASCII))
        if (parsed == null)
            return AprsInterpretation("APRS message: ${text.trimEnd()}")
        val display = when (parsed.kind) {
            AprsMessageKind.MESSAGE -> "Message to ${parsed.addressee}: ${parsed.text}" +
                (parsed.messageId?.let { " {$it}" } ?: "")
            AprsMessageKind.ACK ->
                "Received APRS ACK ${parsed.messageId} addressed to ${parsed.addressee}; not correlated to a local transmission"
            AprsMessageKind.REJ ->
                "Received APRS rej ${parsed.messageId} addressed to ${parsed.addressee}; not correlated to a local transmission"
        }
        return AprsInterpretation(display, message = parsed)
    }

    private fun position(text: String, offset: Int): AprsInterpretation {
        if (text.length < offset + 19)
            return AprsInterpretation("Position packet (malformed): ${text.trimEnd()}")
        val latitudeText = text.substring(offset, offset + 8)
        val table = text[offset + 8]
        val longitudeText = text.substring(offset + 9, offset + 18)
        val symbol = text[offset + 18]
        val latitude = coordinate(latitudeText, 2, 'N', 'S', 90)
        val longitude = coordinate(longitudeText, 3, 'E', 'W', 180)
        if (latitude == null || longitude == null)
            return AprsInterpretation("Position packet (coordinates invalid): ${text.trimEnd()}")
        val comment = text.substring(offset + 19).trimEnd()
        val suffix = if (comment.isEmpty()) "" else " · $comment"
        return AprsInterpretation(
            "Position: %.4f°, %.4f° · symbol %c%c%s".format(latitude, longitude, table, symbol, suffix),
            latitude,
            longitude
        )
    }

    private fun coordinate(
        value: String,
        degreeDigits: Int,
        positive: Char,
        negative: Char,
        maximumDegrees: Int
    ): Double? {
        if (value.length != degreeDigits + 6) return null
        val degrees = value.substring(0, degreeDigits).toIntOrNull() ?: return null
        val minutes = value.substring(degreeDigits, degreeDigits + 5).toDoubleOrNull() ?: return null
        val hemisphere = value.last()
        if (degrees > maximumDegrees || minutes !in 0.0..<60.0 ||
            (degrees == maximumDegrees && minutes != 0.0) ||
            hemisphere != positive && hemisphere != negative)
            return null
        val coordinate = degrees + minutes / 60.0
        return if (hemisphere == negative) -coordinate else coordinate
    }
}

internal object Ax25AfskDecoder {
    private const val SYMBOL_RATE = 1200.0
    private const val TONE_THRESHOLD = 1700.0
    private const val MIN_AMPLITUDE = 0.004
    private const val MAX_FRAME_BYTES = 512

    fun decode(input: ShortArray, sampleRate: Int, cancelled: () -> Boolean = { false }): List<Ax25Packet> {
        val audio = AudioPcm.resample(input, sampleRate, cancelled)
        val demodulated = AudioDemodulator.demodulate(audio.samples, audio.sampleRate, cancelled)
        val framesPerSymbol = audio.sampleRate.toDouble() / SYMBOL_RATE / demodulated.hopSamples
        val result = linkedMapOf<String, Ax25Packet>()
        var phase = 0.0
        while (phase < framesPerSymbol) {
            if (cancelled() || Thread.currentThread().isInterrupted)
                throw java.util.concurrent.CancellationException()
            val framer = HdlcUnframer { frame ->
                val packet = parseFrame(frame) ?: return@HdlcUnframer
                result.putIfAbsent(frame.toHex(), packet)
            }
            val symbolCount = floor((demodulated.frequencies.size - phase) / framesPerSymbol).toInt()
            var previousMark = true
            for (symbol in 0 until symbolCount) {
                if (symbol % 8192 == 0 && (cancelled() || Thread.currentThread().isInterrupted))
                    throw java.util.concurrent.CancellationException()
                val center = phase + (symbol + 0.5) * framesPerSymbol
                val mark = readMark(demodulated, center)
                if (mark == null) {
                    framer.reset()
                    previousMark = true
                } else {
                    val nrziBit = if (mark == previousMark) 1 else 0
                    framer.accept(nrziBit)
                    previousMark = mark
                }
            }
            phase += 1.0
        }
        if (result.isEmpty()) throw ProtocolFailure("afsk_no_valid_ax25")
        return result.values.toList()
    }

    private fun readMark(audio: DemodulatedAudio, centerFrame: Double): Boolean? {
        var frequencySum = 0.0
        var valid = 0
        for (offset in -2..2) {
            val frame = (centerFrame + offset).roundToInt()
            if (frame !in audio.frequencies.indices ||
                audio.amplitudes[frame] < MIN_AMPLITUDE)
                continue
            val frequency = audio.frequencies[frame].toDouble()
            if (frequency in 850.0..1550.0 || frequency in 1850.0..2600.0) {
                frequencySum += frequency
                valid++
            }
        }
        if (valid < 3) return null
        val average = frequencySum / valid
        return when {
            average < TONE_THRESHOLD -> true
            average > TONE_THRESHOLD -> false
            else -> null
        }
    }

    private fun parseFrame(frame: ByteArray): Ax25Packet? {
        if (!Ax25Crc.hasValidFcs(frame)) return null
        val payloadLength = frame.size - 2
        val addresses = mutableListOf<Ax25Address>()
        var offset = 0
        var extension = false
        while (!extension && addresses.size < 10) {
            if (offset + 7 > payloadLength) return null
            val callBytes = frame.copyOfRange(offset, offset + 6)
            if (callBytes.any { it.toInt() and 1 != 0 }) return null
            val call = callBytes.map { ((it.toInt() and 0xff) ushr 1).toChar() }
                .joinToString("").trimEnd()
            if (call.isEmpty() || call.any { it !in 'A'..'Z' && it !in '0'..'9' }) return null
            val ssidByte = frame[offset + 6].toInt() and 0xff
            extension = ssidByte and 1 != 0
            addresses += Ax25Address(call, (ssidByte ushr 1) and 0x0f, ssidByte and 0x80 != 0)
            offset += 7
        }
        if (!extension || addresses.size < 2 || offset >= payloadLength) return null
        val control = frame[offset].toInt() and 0xff
        val hasPid = control == 0x03 || control == 0x13 || control and 1 == 0
        if (hasPid && offset + 2 > payloadLength) return null
        val pid = if (hasPid) frame[offset + 1].toInt() and 0xff else null
        val informationOffset = offset + if (hasPid) 2 else 1
        val information = frame.copyOfRange(informationOffset, payloadLength)
        val destination = addresses[0]
        val source = addresses[1]
        return Ax25Packet(
            destination,
            source,
            addresses.drop(2),
            control,
            pid,
            information,
            if ((control == 0x03 || control == 0x13) && pid == 0xf0)
                AprsTextInterpreter.interpret(information) else null
        )
    }

    private fun ByteArray.toHex(): String =
        joinToString("") { "%02x".format(it.toInt() and 0xff) }

    private class HdlcUnframer(private val onFrame: (ByteArray) -> Unit) {
        private val pending = IntArray(8)
        private val frame = ByteArray(MAX_FRAME_BYTES)
        private var pendingStart = 0
        private var pendingSize = 0
        private var window = 0
        private var windowBits = 0
        private var collecting = false
        private var byteValue = 0
        private var bitsInByte = 0
        private var consecutiveOnes = 0
        private var frameSize = 0
        private var overflow = false

        fun accept(bit: Int) {
            if (pendingSize == pending.size) {
                commit(pending[pendingStart])
                pendingStart = (pendingStart + 1) % pending.size
                pendingSize--
            }
            pending[(pendingStart + pendingSize) % pending.size] = bit
            pendingSize++
            window = ((window shl 1) or bit) and 0xff
            windowBits = minOf(windowBits + 1, 8)
            if (windowBits == 8 && window == 0x7e) {
                if (collecting) finishFrame()
                collecting = true
                clearFrame()
                pendingStart = 0
                pendingSize = 0
                window = 0
                windowBits = 0
            }
        }

        fun reset() {
            pendingStart = 0
            pendingSize = 0
            window = 0
            windowBits = 0
            collecting = false
            clearFrame()
        }

        private fun commit(bit: Int) {
            if (!collecting || overflow) return
            if (bit == 1) {
                consecutiveOnes++
                if (consecutiveOnes > 6) overflow = true
            } else {
                if (consecutiveOnes == 5) {
                    consecutiveOnes = 0
                    return
                }
                consecutiveOnes = 0
            }
            byteValue = byteValue or (bit shl bitsInByte)
            bitsInByte++
            if (bitsInByte == 8) {
                if (frameSize == frame.size) overflow = true
                else frame[frameSize++] = byteValue.toByte()
                byteValue = 0
                bitsInByte = 0
            }
        }

        private fun finishFrame() {
            if (!overflow && bitsInByte == 0 && frameSize >= 17)
                onFrame(frame.copyOf(frameSize))
        }

        private fun clearFrame() {
            byteValue = 0
            bitsInByte = 0
            consecutiveOnes = 0
            frameSize = 0
            overflow = false
        }
    }
}
