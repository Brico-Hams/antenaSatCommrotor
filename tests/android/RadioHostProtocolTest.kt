package org.bricohams.portablesatstation

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class RadioHostProtocolTest {
    @Test fun frozenRadioHostUuidsAndControlFragmentRoundTrip() {
        assertEquals("c8201001-4e53-4253-9000-000000000001", RadioHostWire.SERVICE.toString())
        assertEquals("c8201002-4e53-4253-9000-000000000001", RadioHostWire.CONTROL_RX.toString())
        assertEquals("c8201003-4e53-4253-9000-000000000001", RadioHostWire.CONTROL_TX.toString())
        assertEquals("c8201004-4e53-4253-9000-000000000001", RadioHostWire.AUDIO_RX.toString())
        assertEquals("c8201005-4e53-4253-9000-000000000001", RadioHostWire.AUDIO_TX.toString())
        val payload = RadioHostWire.request("r1", "/status", "get", JSONObject())
        val frames = RadioHostWire.controlFrames(payload, 0x1234)
        assertTrue(frames.all { it.size == 20 && (it[0].toInt() and 0xff) == 0x53 })
        val assembler = RadioHostControlAssembler()
        var assembled: ByteArray? = null
        frames.forEach { assembled = assembler.feed(it) ?: assembled }
        assertEquals(JSONObject(payload.toString(Charsets.UTF_8)).toString(),
            JSONObject(assembled!!.toString(Charsets.UTF_8)).toString())
    }

    @Test fun audioHeaderValidatesStreamSequenceSampleIndexAndS16lePayload() {
        val expected = shortArrayOf(0, 1234, -32768, 32767)
        val encoded = RadioHostAudioWire.encode(expected, 0, expected.size, 247, 0xdeadbeefL, 7, 900)
        assertEquals(24, encoded.size)
        val parsed = RadioHostAudioWire.parse(encoded, 247, 0xdeadbeefL, 7, 900)
        assertEquals(0xdeadbeefL, parsed.streamId)
        assertEquals(7L, parsed.sequence)
        assertEquals(900L, parsed.sampleIndex)
        assertTrue(expected.contentEquals(parsed.samples))
        rejects("radio_audio_discontinuity") {
            RadioHostAudioWire.parse(encoded, 247, 0xdeadbeefL, 8, 900)
        }
        rejects("radio_audio_discontinuity") {
            RadioHostAudioWire.parse(encoded, 247, 0xdeadbeefL, 7, 901)
        }
        rejects("radio_audio_header") {
            RadioHostAudioWire.parse(encoded.clone().apply { this[1] = 1 }, 247, 0xdeadbeefL, 7, 900)
        }
        rejects("radio_audio_header") {
            RadioHostAudioWire.parse(encoded.copyOf(23), 247, 0xdeadbeefL, 7, 900)
        }
    }

    @Test fun hostStatusRequiresVersionDualProfilesAndFailsClosedForTx() {
        val status = RadioHostStatusParser.parse(statusJson())
        assertEquals(setOf("VHF", "UHF"), status.availableChannels)
        assertEquals("VHF", status.rxChannel)
        assertEquals("UHF", status.txChannel)
        assertEquals(1000000L, status.profiles.getValue("VHF").rxRateReadback)
        assertEquals(1000000L, status.profiles.getValue("UHF").txRateReadback)
        assertTrue(RadioHostWire.validAudioChannels("VHF", "UHF", status.availableChannels))
        assertTrue(RadioHostWire.validAudioChannels("UHF", "VHF", status.availableChannels))
        assertFalse(RadioHostWire.validAudioChannels("VHF", "VHF", status.availableChannels))
        assertFalse(RadioHostWire.validAudioChannels("VHF", "UHF", setOf("VHF")))
        assertTrue(RadioHostWire.validAudioChannels("VHF", "VHF", setOf("VHF")))
        assertFalse(RadioHostWire.validAudioChannels("UHF", "UHF", setOf("VHF")))
        assertFalse(RadioHostWire.validAudioChannels("VHF", "UHF", setOf("VHF", "UHF", "OTHER")))
        assertEquals("VHF", RadioHostWire.channelForFrequency(145_900_000))
        assertEquals("UHF", RadioHostWire.channelForFrequency(435_100_000))
        assertEquals(null, RadioHostWire.channelForFrequency(220_000_000))
        val singleRadio = RadioHostStatusParser.parse(statusJson()
            .put("availableChannels", JSONArray().put("VHF"))
            .put("rxChannel", "VHF").put("txChannel", "VHF")
            .put("rxHz", 145900000).put("txHz", 145900000)
            .put("actualHz", JSONArray().put(145900000).put(145900000))
            .put("profiles", JSONObject().put("VHF", statusProfile("VHF-SERIAL"))))
        assertEquals(setOf("VHF"), singleRadio.availableChannels)
        assertFalse(singleRadio.canRequestPtt("VHF"))
        val singleRadioManualArmed = RadioHostStatusParser.parse(statusJson()
            .put("availableChannels", JSONArray().put("VHF"))
            .put("rxChannel", "VHF").put("txChannel", "VHF")
            .put("rxHz", 145900000).put("txHz", 145900000)
            .put("actualHz", JSONArray().put(145900000).put(145900000))
            .put("profiles", JSONObject().put("VHF", statusProfile("VHF-SERIAL")))
            .put("physicalArm", true).put("physicalPtt", true).put("sdrReady", true)
            .put("rfPolarization", JSONObject().put("ready", true).put("requested", "LINEAR")
                .put("configured", "LINEAR").put("capabilities", JSONArray().put("LINEAR"))))
        assertTrue(singleRadioManualArmed.canRequestPtt("VHF"))
        assertFalse(status.canRequestPtt("VHF"))
        assertFalse(status.canRequestPtt("UHF"))
        val armed = RadioHostStatusParser.parse(statusJson().put("physicalArm", true)
            .put("physicalPtt", true).put("sdrReady", true)
            .put("rfPolarization", JSONObject().put("ready", true).put("requested", "LINEAR")
                .put("configured", "LINEAR").put("capabilities", JSONArray().put("LINEAR"))))
        assertTrue(armed.canRequestPtt("UHF"))
        assertFalse(armed.canRequestPtt("VHF"))
        val transmitting = RadioHostStatusParser.parse(statusJson().put("tx", true)
            .put("physicalArm", true).put("physicalPtt", true).put("sdrReady", true)
            .put("rfPolarization", JSONObject().put("ready", true).put("requested", "LINEAR")
                .put("configured", "LINEAR").put("capabilities", JSONArray().put("LINEAR")))
            .put("profiles", JSONObject()
                .put("VHF", JSONObject().put("serial", "VHF-SERIAL").put("rxReady", true)
                    .put("rxHzReadback", 145900000).put("txHzReadback", 145900000)
                    .put("rxRateReadback", 1000000).put("txRateReadback", 1000000)
                    .put("rxReads", 1).put("queueDepth", 0).put("fault", JSONObject.NULL)
                    .put("txActive", false))
                .put("UHF", JSONObject().put("serial", "UHF-SERIAL").put("rxReady", true)
                    .put("rxHzReadback", 435100000).put("txHzReadback", 435100000)
                    .put("rxRateReadback", 1000000).put("txRateReadback", 1000000)
                    .put("rxReads", 1).put("queueDepth", 0).put("fault", JSONObject.NULL)
                    .put("txActive", true))))
        assertTrue(transmitting.canMaintainPtt("UHF"))
        assertFalse(transmitting.canMaintainPtt("VHF"))
        assertFalse(transmitting.canMaintainPtt("OTHER"))
        assertFalse(RadioHostStatusParser.parse(statusJson().put("tx", true)
            .put("physicalArm", true).put("physicalPtt", true).put("sdrReady", true)
            .put("rfPolarization", JSONObject().put("ready", true).put("requested", "LINEAR")
                .put("configured", "LINEAR").put("capabilities", JSONArray().put("LINEAR")))
        ).canRequestPtt("UHF"))
        rejects("radio_host_version_unsupported") {
            RadioHostStatusParser.parse(statusJson().put("fw", "unknown"))
        }
        rejects("radio_status_txPolicy") {
            RadioHostStatusParser.parse(statusJson().put("txPolicy", "MULTI_TX"))
        }
        val noHardware = statusJson().put("availableChannels", JSONArray())
            .put("profiles", JSONObject()).put("sdrReady", false)
        assertTrue(RadioHostStatusParser.parse(noHardware).availableChannels.isEmpty())
        rejects("radio_status_profile_readback") {
            RadioHostStatusParser.parse(statusJson().put("profiles", JSONObject()
                .put("VHF", JSONObject().put("serial", "VHF-SERIAL").put("rxReady", true)
                    .put("rxHzReadback", 0).put("txHzReadback", 145900000)
                    .put("rxRateReadback", 1000000).put("txRateReadback", 1000000)
                    .put("rxReads", 1).put("queueDepth", 0).put("fault", JSONObject.NULL)
                    .put("txActive", false))
                .put("UHF", JSONObject().put("serial", "UHF-SERIAL").put("rxReady", true)
                    .put("rxHzReadback", 435100000).put("txHzReadback", 435100000)
                    .put("rxRateReadback", 1000000).put("txRateReadback", 1000000)
                    .put("rxReads", 1).put("queueDepth", 0).put("fault", JSONObject.NULL)
                    .put("txActive", false))))
        }
        rejects("radio_status_profile_frequency") {
            RadioHostStatusParser.parse(statusJson().put("profiles", JSONObject()
                .put("VHF", JSONObject().put("serial", "VHF-SERIAL").put("rxReady", true)
                    .put("rxHzReadback", 435100000).put("txHzReadback", 145900000)
                    .put("rxRateReadback", 1000000).put("txRateReadback", 1000000)
                    .put("rxReads", 1).put("queueDepth", 0).put("fault", JSONObject.NULL)
                    .put("txActive", false))
                .put("UHF", statusProfile("UHF-SERIAL"))))
        }
    }

    private fun statusJson(): JSONObject {
        return JSONObject()
            .put("fw", "radio-host/1.0.0")
            .put("operationProfile", "STANDALONE_MANUAL")
            .put("availableChannels", JSONArray().put("VHF").put("UHF"))
            .put("rxChannel", "VHF").put("txChannel", "UHF")
            .put("mode", "FM").put("rxHz", 145900000).put("txHz", 435100000)
            .put("actualHz", JSONArray().put(145900000).put(435100000))
            .put("sdrReady", false).put("tx", false).put("physicalArm", false)
            .put("physicalPtt", false).put("trackingFresh", false).put("rotorReady", false)
            .put("rotorFault", JSONObject.NULL).put("fault", JSONObject.NULL)
            .put("profiles", JSONObject().put("VHF", statusProfile("VHF-SERIAL"))
                .put("UHF", statusProfile("UHF-SERIAL")))
            .put("rxDropped", 0).put("txFaults", 0).put("txCredits", 16)
            .put("rfPolarization", JSONObject().put("requested", "LINEAR")
                .put("configured", JSONObject.NULL).put("ready", false)
                .put("capabilities", JSONArray().put("LINEAR")))
            .put("rxChannel", "VHF").put("txChannel", "UHF")
            .put("txPolicy", "ONE_TX_ONLY").put("driveAmplitudeLimit", 0.1)
    }

    private fun statusProfile(serial: String) = JSONObject()
        .put("serial", serial).put("rxReady", true)
        .put("rxHzReadback", if (serial.startsWith("VHF")) 145900000 else 435100000)
        .put("txHzReadback", if (serial.startsWith("VHF")) 145900000 else 435100000)
        .put("rxRateReadback", 1000000)
        .put("txRateReadback", 1000000).put("rxReads", 1).put("queueDepth", 0)
        .put("fault", JSONObject.NULL).put("txActive", false)

    private fun rejects(code: String, action: () -> Unit) {
        try {
            action()
            throw AssertionError("Expected ProtocolFailure($code)")
        } catch (error: ProtocolFailure) {
            assertEquals(code, error.code)
        }
    }
}
