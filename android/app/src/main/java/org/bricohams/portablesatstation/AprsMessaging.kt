package org.bricohams.portablesatstation

import java.io.ByteArrayOutputStream
import kotlin.math.PI
import kotlin.math.roundToInt
import kotlin.math.sin

internal enum class AprsMessageKind { MESSAGE, ACK, REJ }

internal data class AprsMessage(
    val addressee: String,
    val kind: AprsMessageKind,
    val text: String,
    val messageId: String?
)

internal object AprsAddressing {
    private val callBase = Regex("(?i)[A-Z0-9]{1,6}")

    fun normalizeStation(value: String): String? {
        val normalized = value.trim().uppercase()
        val parts = normalized.split('-')
        if (parts.size !in 1..2 || !callBase.matches(parts[0])) return null
        if (parts[0] != "APRS" && !isCallsign(parts[0])) return null
        val ssid = parts.getOrNull(1)?.toIntOrNull() ?: 0
        if (ssid !in 0..15) return null
        return normalized.substringBefore('-') + if (ssid == 0) "" else "-$ssid"
    }

    fun normalizeCallsign(value: String): String? {
        val normalized = normalizeStation(value) ?: return null
        if (normalized.substringBefore('-') == "APRS") return null
        return normalized
    }

    private fun isCallsign(value: String): Boolean =
        value.any { it.isLetter() } && value.any { it.isDigit() }

    fun parsePath(value: String): List<String>? {
        if (value.isBlank()) return emptyList()
        val entries = value.split(',')
        if (entries.size > 8) return null
        val normalized = entries.map { normalizeCallsign(it) ?: return null }
        if (normalized.distinct().size != normalized.size) return null
        return normalized
    }
}

internal object AprsMessageCodec {
    private val messageIdPattern = Regex("[A-Za-z0-9]{1,5}")

    fun parse(information: ByteArray): AprsMessage? {
        val text = printablePayload(information) ?: return null
        if (text.length < 11 || text[0] != ':' || text[10] != ':') return null
        val addressee = text.substring(1, 10).trim().uppercase()
        if (AprsAddressing.normalizeCallsign(addressee) != addressee) return null
        val payload = text.substring(11).trimEnd()
        if (payload.startsWith("ack") || payload.startsWith("rej")) {
            val kind = if (payload.startsWith("ack")) AprsMessageKind.ACK else AprsMessageKind.REJ
            val id = payload.substring(3)
            if (!messageIdPattern.matches(id)) return null
            return AprsMessage(addressee, kind, "", id)
        }
        val marker = payload.lastIndexOf('{')
        val id = if (marker >= 0) payload.substring(marker + 1) else null
        if (id != null && !messageIdPattern.matches(id)) return null
        val body = if (marker >= 0) payload.substring(0, marker) else payload
        if (body.isEmpty() || body.length > 67) return null
        return AprsMessage(addressee, AprsMessageKind.MESSAGE, body, id)
    }

    fun format(message: AprsMessage, sender: String): String = when (message.kind) {
        AprsMessageKind.MESSAGE -> buildString {
            append(sender)
            append(" → ")
            append(message.addressee)
            append(": ")
            append(message.text)
            message.messageId?.let { append(" {"); append(it); append('}') }
        }
        AprsMessageKind.ACK ->
            "Received APRS ACK ${message.messageId} from $sender; not correlated to a local transmission"
        AprsMessageKind.REJ ->
            "Received APRS rej ${message.messageId} from $sender; not correlated to a local transmission"
    }

    fun encodeUiFrame(
        source: String,
        destination: String,
        digipeaters: List<String>,
        information: ByteArray
    ): ByteArray {
        val sourceAddress = AprsAddressing.normalizeCallsign(source)
            ?: throw ProtocolFailure("aprs_source_invalid")
        val destinationAddress = AprsAddressing.normalizeStation(destination)
            ?: throw ProtocolFailure("aprs_destination_invalid")
        if (destinationAddress.length > 9 || information.isEmpty() || information.size > 256)
            throw ProtocolFailure("aprs_frame_invalid")
        if (digipeaters.size > 8 || digipeaters.any { AprsAddressing.normalizeCallsign(it) != it })
            throw ProtocolFailure("aprs_path_invalid")

        val frame = ByteArrayOutputStream()
        fun address(value: String, last: Boolean, repeated: Boolean = false) {
            val call = value.substringBefore('-').uppercase()
            val ssid = value.substringAfter('-', "0").toInt()
            call.padEnd(6, ' ').forEach { frame.write((it.code shl 1) and 0xff) }
            frame.write(0x60 or (ssid shl 1) or (if (repeated) 0x80 else 0) or if (last) 1 else 0)
        }
        address(destinationAddress, false)
        address(sourceAddress, digipeaters.isEmpty())
        digipeaters.forEachIndexed { index, pathCall ->
            address(pathCall, index == digipeaters.lastIndex)
        }
        frame.write(0x03)
        frame.write(0xf0)
        frame.write(information)
        val withoutFcs = frame.toByteArray()
        val crc = Ax25Crc.crc16X25(withoutFcs)
        return withoutFcs + byteArrayOf(crc.toByte(), (crc ushr 8).toByte())
    }

    fun encodeMessageInformation(addressee: String, body: String, messageId: String?): ByteArray {
        val recipient = AprsAddressing.normalizeCallsign(addressee)
            ?: throw ProtocolFailure("aprs_destination_invalid")
        if (recipient.length > 9) throw ProtocolFailure("aprs_destination_invalid")
        if (body.isEmpty() || body.length > 67 || body.any { it.code !in 32..126 || it == '{' })
            throw ProtocolFailure("aprs_message_invalid")
        if (messageId != null && !messageIdPattern.matches(messageId))
            throw ProtocolFailure("aprs_message_id_invalid")
        val info = ":${recipient.padEnd(9)}:$body${messageId?.let { "{$it" } ?: ""}"
        return info.toByteArray(Charsets.US_ASCII)
    }

    private fun printablePayload(bytes: ByteArray): String? =
        if (bytes.any { (it.toInt() and 0xff) !in 32..126 }) null
        else bytes.toString(Charsets.US_ASCII)
}

internal object AprsInbox {
    fun addressedTo(packets: List<Ax25Packet>, ownCallsign: String): List<String> {
        val local = AprsAddressing.normalizeCallsign(ownCallsign) ?: return emptyList()
        return packets.mapNotNull { packet ->
            val message = packet.aprs?.message ?: return@mapNotNull null
            if (AprsAddressing.normalizeCallsign(message.addressee) != local) return@mapNotNull null
            AprsMessageCodec.format(message, packet.source.toString())
        }
    }
}

internal data class TxAudio(val samples: ShortArray, val sampleRate: Int = SAMPLE_RATE) {
    fun toWav(): ByteArray = PcmWav.encodeS16(samples, sampleRate)

    companion object { const val SAMPLE_RATE = 8000 }
}

internal object Bell202Encoder {
    private const val SAMPLE_RATE = TxAudio.SAMPLE_RATE
    private const val BAUD = 1200.0
    private const val MAX_AUDIO_SECONDS = 8

    fun encode(frame: ByteArray): TxAudio {
        require(Ax25Crc.hasValidFcs(frame)) { "AX.25 frame must include a valid FCS" }
        val samples = ArrayList<Short>()
        repeat(SAMPLE_RATE / 10) { samples += 0 }
        var symbols = 0L
        var phase = 0.0
        var previousMark = true
        var consecutiveOnes = 0

        fun appendBit(bit: Int) {
            if (bit == 0) previousMark = !previousMark
            val frequency = if (previousMark) 1200.0 else 2200.0
            symbols++
            val end = (symbols * SAMPLE_RATE / BAUD).roundToInt()
            val amplitude = 0.48 * Short.MAX_VALUE
            while (samples.size < SAMPLE_RATE / 10 + end) {
                samples += (sin(phase) * amplitude).roundToInt().toShort()
                phase += 2.0 * PI * frequency / SAMPLE_RATE
                if (phase >= 2.0 * PI) phase -= 2.0 * PI
            }
            if (samples.size > SAMPLE_RATE * MAX_AUDIO_SECONDS)
                throw ProtocolFailure("aprs_audio_limit")
        }

        fun appendFlag() { repeat(8) { appendBit((0x7e ushr it) and 1) } }
        repeat(36) { appendFlag() }
        for (byte in frame) {
            val value = byte.toInt() and 0xff
            repeat(8) { bitIndex ->
                val bit = (value ushr bitIndex) and 1
                appendBit(bit)
                consecutiveOnes = if (bit == 1) consecutiveOnes + 1 else 0
                if (consecutiveOnes == 5) {
                    appendBit(0)
                    consecutiveOnes = 0
                }
            }
        }
        repeat(4) { appendFlag() }
        repeat(SAMPLE_RATE / 10) { samples += 0 }
        return TxAudio(ShortArray(samples.size) { samples[it] })
    }
}
