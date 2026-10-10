package org.bricohams.portablesatstation

import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.util.UUID

internal object RadioHostWire {
    private const val BASE = "-4e53-4253-9000-000000000001"
    val SERVICE: UUID = UUID.fromString("c8201001$BASE")
    val CONTROL_RX: UUID = UUID.fromString("c8201002$BASE")
    val CONTROL_TX: UUID = UUID.fromString("c8201003$BASE")
    val AUDIO_RX: UUID = UUID.fromString("c8201004$BASE")
    val AUDIO_TX: UUID = UUID.fromString("c8201005$BASE")
    val CCCD: UUID = Protocol.CCCD
    const val AUDIO_RATE = 8000
    const val AUDIO_HEADER_SIZE = 16
    const val MAX_AUDIO_PAYLOAD = 228
    const val MAX_CREDITS = 16
    const val MAX_CONTROL_BYTES = 4096
    const val MAX_MTU = 517
    const val CONTROL_MAGIC = 0x53
    const val FLAG_START = 1
    const val FLAG_END = 2

    fun validAudioChannels(rxChannel: String, txChannel: String, availableChannels: Set<String>): Boolean {
        if (rxChannel !in setOf("VHF", "UHF") || txChannel !in setOf("VHF", "UHF") ||
            rxChannel !in availableChannels || txChannel !in availableChannels)
            return false
        return if (availableChannels.size == 1) rxChannel == txChannel
        else availableChannels == setOf("VHF", "UHF") && rxChannel != txChannel
    }

    fun channelForFrequency(hz: Long): String? = when (hz) {
        in 144_000_000L..146_000_000L -> "VHF"
        in 430_000_000L..440_000_000L -> "UHF"
        else -> null
    }

    fun controlFrames(json: ByteArray, sequence: Int): List<ByteArray> {
        if (json.isEmpty() || json.size > MAX_CONTROL_BYTES || json.any { it == 0.toByte() })
            throw ProtocolFailure("radio_control_size")
        val count = (json.size + 15) / 16
        return List(count) { index ->
            val start = index * 16
            val length = minOf(16, json.size - start)
            ByteArray(20).also { frame ->
                frame[0] = CONTROL_MAGIC.toByte()
                frame[1] = ((if (index == 0) FLAG_START else 0) or
                    (if (index == count - 1) FLAG_END else 0)).toByte()
                frame[2] = sequence.toByte()
                frame[3] = (sequence ushr 8).toByte()
                json.copyInto(frame, 4, start, start + length)
            }
        }
    }

    fun request(id: String, path: String, op: String, data: JSONObject): ByteArray {
        require(id.isNotBlank() && id.length <= 64)
        require(path.startsWith("/") && path.length <= 128)
        require(op == "get" || op == "set")
        return JSONObject().put("v", 1).put("id", id).put("path", path)
            .put("op", op).put("data", data).toString().toByteArray(Charsets.UTF_8)
            .also { if (it.size > MAX_CONTROL_BYTES) throw ProtocolFailure("radio_control_size") }
    }
}

internal class RadioHostControlAssembler {
    private val buffer = ByteArrayOutputStream()
    private var sequence: Int? = null

    fun reset() {
        buffer.reset()
        sequence = null
    }

    fun feed(frame: ByteArray): ByteArray? {
        fun fail(): Nothing {
            reset()
            throw ProtocolFailure("radio_control_frame")
        }
        if (frame.size != 20 || (frame[0].toInt() and 0xff) != RadioHostWire.CONTROL_MAGIC)
            fail()
        val flags = frame[1].toInt() and 0xff
        if (flags and (RadioHostWire.FLAG_START or RadioHostWire.FLAG_END).inv() != 0) fail()
        val currentSequence = (frame[2].toInt() and 0xff) or ((frame[3].toInt() and 0xff) shl 8)
        if (flags and RadioHostWire.FLAG_START != 0) {
            if (sequence != null) fail()
            sequence = currentSequence
        }
        if (sequence != currentSequence) fail()
        buffer.write(frame, 4, 16)
        if (buffer.size() > RadioHostWire.MAX_CONTROL_BYTES + 15) fail()
        if (flags and RadioHostWire.FLAG_END == 0) return null
        val bytes = buffer.toByteArray()
        reset()
        return bytes.copyOf(bytes.indexOfLast { it != 0.toByte() } + 1)
            .takeIf { it.isNotEmpty() } ?: fail()
    }
}

internal data class RadioAudioFrame(
    val streamId: Long,
    val sequence: Long,
    val sampleIndex: Long,
    val samples: ShortArray
)

internal object RadioHostAudioWire {
    fun parse(
        bytes: ByteArray,
        mtu: Int,
        expectedStreamId: Long,
        expectedSequence: Long,
        expectedSampleIndex: Long
    ): RadioAudioFrame {
        val maxBytes = minOf(mtu - 3, 244)
        if (mtu !in 247..RadioHostWire.MAX_MTU || bytes.size !in 18..maxBytes)
            throw ProtocolFailure("radio_audio_length")
        val input = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN)
        val version = input.get().toInt() and 0xff
        val flags = input.get().toInt() and 0xff
        val reserved = input.short.toInt() and 0xffff
        val stream = input.int.toLong() and 0xffffffffL
        val sequence = input.int.toLong() and 0xffffffffL
        val sampleIndex = input.int.toLong() and 0xffffffffL
        val payloadLength = input.remaining()
        if (version != 1 || flags != 0 || reserved != 0 || payloadLength == 0 || payloadLength % 2 != 0)
            throw ProtocolFailure("radio_audio_header")
        if (stream != expectedStreamId || sequence != expectedSequence || sampleIndex != expectedSampleIndex)
            throw ProtocolFailure("radio_audio_discontinuity")
        val samples = ShortArray(payloadLength / 2) { input.short }
        return RadioAudioFrame(stream, sequence, sampleIndex, samples)
    }

    fun encode(
        samples: ShortArray,
        offset: Int,
        length: Int,
        mtu: Int,
        streamId: Long,
        sequence: Long,
        sampleIndex: Long
    ): ByteArray {
        val maxPayload = minOf(mtu - 3 - RadioHostWire.AUDIO_HEADER_SIZE, RadioHostWire.MAX_AUDIO_PAYLOAD)
        if (mtu !in 247..RadioHostWire.MAX_MTU || length !in 1..(maxPayload / 2) ||
            offset < 0 || offset > samples.size - length ||
            listOf(streamId, sequence, sampleIndex).any { it !in 0..0xffffffffL })
            throw ProtocolFailure("radio_audio_tx_frame")
        return ByteBuffer.allocate(RadioHostWire.AUDIO_HEADER_SIZE + length * 2)
            .order(ByteOrder.LITTLE_ENDIAN)
            .put(1).put(0).putShort(0).putInt(streamId.toInt()).putInt(sequence.toInt())
            .putInt(sampleIndex.toInt()).apply {
                for (index in offset until offset + length) putShort(samples[index])
            }.array()
    }
}

internal data class RadioHostStatus(
    val firmware: String,
    val operationProfile: String,
    val availableChannels: Set<String>,
    val rxChannel: String,
    val txChannel: String,
    val mode: String,
    val rxHz: Long,
    val txHz: Long,
    val sdrReady: Boolean,
    val transmitting: Boolean,
    val physicalArm: Boolean,
    val physicalPtt: Boolean,
    val trackingFresh: Boolean,
    val rotorReady: Boolean,
    val rotorFault: String?,
    val fault: String?,
    val txCredits: Int,
    val profiles: Map<String, RadioProfileStatus>,
    val polarizationReady: Boolean,
    val polarizationCapabilities: Set<String>,
    val requestedPolarization: String?,
    val configuredPolarization: String?
) {
    fun canRequestPtt(channel: String): Boolean {
        if (channel != txChannel || !physicalArm || !physicalPtt || !sdrReady ||
            transmitting || profiles.values.any { it.txActive } ||
            fault != null || !polarizationReady ||
            mode !in setOf("FM", "AM", "USB"))
            return false
        val profile = profiles[channel] ?: return false
        if (!profile.rxReady || profile.txActive || profile.fault != null) return false
        return operationProfile == "STANDALONE_MANUAL" ||
            (operationProfile == "INTEGRATED_TRACKING" && trackingFresh && rotorReady && rotorFault == null)
    }

    fun canMaintainPtt(channel: String): Boolean {
        if (channel != txChannel || !physicalArm || !physicalPtt || !sdrReady ||
            fault != null || !polarizationReady ||
            mode !in setOf("FM", "AM", "USB"))
            return false
        val profile = profiles[channel] ?: return false
        if (!profile.rxReady || profile.fault != null ||
            profiles.any { (name, state) -> name != channel && state.txActive })
            return false
        return operationProfile == "STANDALONE_MANUAL" ||
            (operationProfile == "INTEGRATED_TRACKING" && trackingFresh && rotorReady && rotorFault == null)
    }
}

internal data class RadioProfileStatus(
    val serial: String,
    val rxReady: Boolean,
    val rxHzReadback: Long,
    val txHzReadback: Long,
    val rxRateReadback: Long,
    val txRateReadback: Long,
    val rxReads: Long,
    val queueDepth: Long,
    val txActive: Boolean,
    val fault: String?
)

internal object RadioHostStatusParser {
    private fun JSONObject.requiredString(key: String): String =
        opt(key) as? String ?: throw ProtocolFailure("radio_status_$key")

    private fun JSONObject.requiredBool(key: String): Boolean =
        opt(key) as? Boolean ?: throw ProtocolFailure("radio_status_$key")

    private fun JSONObject.requiredLong(key: String): Long {
        val value = opt(key)
        if (value !is Number || value.toDouble() % 1 != 0.0 || !value.toDouble().isFinite())
            throw ProtocolFailure("radio_status_$key")
        return value.toLong()
    }

    private fun JSONObject.nullableString(key: String): String? {
        if (!has(key)) throw ProtocolFailure("radio_status_$key")
        return if (isNull(key)) null else opt(key) as? String ?: throw ProtocolFailure("radio_status_$key")
    }

    fun parse(data: JSONObject): RadioHostStatus {
        val firmware = data.requiredString("fw")
        if (firmware != "radio-host/1.0.0") throw ProtocolFailure("radio_host_version_unsupported")
        val operationProfile = data.requiredString("operationProfile")
        if (operationProfile !in setOf("INTEGRATED_TRACKING", "STANDALONE_MANUAL"))
            throw ProtocolFailure("radio_status_operationProfile")
        val rxChannel = data.requiredString("rxChannel")
        val txChannel = data.requiredString("txChannel")
        if (rxChannel !in setOf("VHF", "UHF") || txChannel !in setOf("VHF", "UHF"))
            throw ProtocolFailure("radio_status_channel")
        val channelsArray = data.optJSONArray("availableChannels")
            ?: throw ProtocolFailure("radio_status_availableChannels")
        val channels = (0 until channelsArray.length()).map {
            channelsArray.optString(it, "")
        }
        if (channels.any { it !in setOf("VHF", "UHF") } ||
            channels.distinct().size != channels.size ||
            (channels.isNotEmpty() && (rxChannel !in channels || txChannel !in channels)))
            throw ProtocolFailure("radio_status_availableChannels")
        val actualHz = data.optJSONArray("actualHz") ?: throw ProtocolFailure("radio_status_actualHz")
        if (actualHz.length() != 2 || actualHz.opt(0) !is Number || actualHz.opt(1) !is Number)
            throw ProtocolFailure("radio_status_actualHz")
        val profilesJson = data.optJSONObject("profiles") ?: throw ProtocolFailure("radio_status_profiles")
        val profiles = LinkedHashMap<String, RadioProfileStatus>()
        if (profilesJson.length() != 0 && profilesJson.length() != channels.size)
            throw ProtocolFailure("radio_status_profile_set")
        for (channel in channels) {
            if (profilesJson.length() == 0) break
            val value = profilesJson.optJSONObject(channel) ?: throw ProtocolFailure("radio_status_profile_$channel")
            val serial = value.opt("serial") as? String ?: throw ProtocolFailure("radio_status_profile_serial")
            if (serial.isBlank()) throw ProtocolFailure("radio_status_profile_serial")
            val rxReady = value.opt("rxReady") as? Boolean ?: throw ProtocolFailure("radio_status_profile_rxReady")
            val txActive = value.opt("txActive") as? Boolean ?: throw ProtocolFailure("radio_status_profile_txActive")
            val profileFault = if (!value.has("fault")) throw ProtocolFailure("radio_status_profile_fault")
                else if (value.isNull("fault")) null
                else value.opt("fault") as? String ?: throw ProtocolFailure("radio_status_profile_fault")
            fun profileLong(key: String): Long {
                val number = value.opt(key)
                if (number !is Number || !number.toDouble().isFinite() ||
                    number.toDouble() % 1 != 0.0 || number.toLong() < 0)
                    throw ProtocolFailure("radio_status_profile_$key")
                return number.toLong()
            }
            val rxHzReadback = profileLong("rxHzReadback")
            val txHzReadback = profileLong("txHzReadback")
            val rxRateReadback = profileLong("rxRateReadback")
            val txRateReadback = profileLong("txRateReadback")
            val rxReads = profileLong("rxReads")
            val queueDepth = profileLong("queueDepth")
            if (rxReady && (rxHzReadback == 0L || txHzReadback == 0L ||
                    rxRateReadback == 0L || txRateReadback == 0L))
                throw ProtocolFailure("radio_status_profile_readback")
            if ((rxHzReadback > 0 && RadioHostWire.channelForFrequency(rxHzReadback) != channel) ||
                (txHzReadback > 0 && RadioHostWire.channelForFrequency(txHzReadback) != channel))
                throw ProtocolFailure("radio_status_profile_frequency")
            profiles[channel] = RadioProfileStatus(
                serial, rxReady, rxHzReadback, txHzReadback, rxRateReadback,
                txRateReadback, rxReads, queueDepth, txActive, profileFault
            )
        }
        if (profilesJson.length() != profiles.size || (profiles.isEmpty() && data.opt("sdrReady") != false))
            throw ProtocolFailure("radio_status_profile_set")
        val polarization = data.optJSONObject("rfPolarization") ?: throw ProtocolFailure("radio_status_rfPolarization")
        val ready = polarization.opt("ready") as? Boolean ?: throw ProtocolFailure("radio_status_polarization_ready")
        val capabilitiesArray = polarization.optJSONArray("capabilities")
        if (!polarization.has("requested") || !polarization.has("configured") ||
            capabilitiesArray == null)
            throw ProtocolFailure("radio_status_rfPolarization")
        fun nullablePolarization(key: String): String? =
            if (polarization.isNull(key)) null
            else polarization.opt(key) as? String ?: throw ProtocolFailure("radio_status_rfPolarization_$key")
        val capabilities = (0 until capabilitiesArray.length()).map {
            capabilitiesArray.optString(it, "")
        }
        if (capabilities.any { it !in setOf("LINEAR", "RHCP", "LHCP") } ||
            capabilities.distinct().size != capabilities.size)
            throw ProtocolFailure("radio_status_rfPolarization_capabilities")
        val txPolicy = data.requiredString("txPolicy")
        if (txPolicy != "ONE_TX_ONLY") throw ProtocolFailure("radio_status_txPolicy")
        val credits = data.requiredLong("txCredits")
        if (credits !in 0..RadioHostWire.MAX_CREDITS.toLong()) throw ProtocolFailure("radio_status_txCredits")
        for (key in listOf("rxHz", "txHz", "rxDropped", "txFaults")) data.requiredLong(key)
        val actualRxHz = actualHz.opt(0) as Number
        val actualTxHz = actualHz.opt(1) as Number
        if (listOf(actualRxHz, actualTxHz).any { !it.toDouble().isFinite() || it.toDouble() <= 0 })
            throw ProtocolFailure("radio_status_actualHz")
        val driveLimit = data.opt("driveAmplitudeLimit") as? Number
            ?: throw ProtocolFailure("radio_status_driveAmplitudeLimit")
        if (!driveLimit.toDouble().isFinite() || driveLimit.toDouble() !in 0.0..1.0)
            throw ProtocolFailure("radio_status_driveAmplitudeLimit")
        val rotorFault = data.nullableString("rotorFault")
        val fault = data.nullableString("fault")
        return RadioHostStatus(
            firmware, operationProfile, channels.toSet(), rxChannel, txChannel,
            data.requiredString("mode"),
            data.requiredLong("rxHz"), data.requiredLong("txHz"),
            data.requiredBool("sdrReady"), data.requiredBool("tx"),
            data.requiredBool("physicalArm"), data.requiredBool("physicalPtt"),
            data.requiredBool("trackingFresh"), data.requiredBool("rotorReady"),
            rotorFault, fault, credits.toInt(), profiles, ready, capabilities.toSet(),
            nullablePolarization("requested"), nullablePolarization("configured")
        )
    }
}
