package org.bricohams.portablesatstation

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class ProtocolTest {
    private fun rejects(expected: String, action: () -> Unit) {
        try { action(); fail("Expected $expected") }
        catch (error: ProtocolFailure) { assertEquals(expected, error.code) }
    }
    @Test fun requestMatchesActualFirmwareEnvelopeAndUnits() {
        val request = JSONObject(Protocol.request(7, "locally-entered-test-token", "move",
            JSONObject().put("az", -180.0).put("el", 90)).toString(Charsets.UTF_8))
        assertEquals(1, request.getInt("v"))
        assertEquals(7, request.getInt("id"))
        assertEquals("/api/move", request.getString("path"))
        assertEquals("POST", request.getString("method"))
        assertEquals(-180.0, request.getJSONObject("body").getDouble("az"), 0.0)
        val status = JSONObject(Protocol.request(1, "test-only", "status", JSONObject()).toString(Charsets.UTF_8))
        assertEquals("GET", status.getString("method"))
        assertEquals("/api/status", status.getString("path"))
        assertEquals(0, status.getJSONObject("body").length())
    }
    @Test fun exactMtu23AndNegotiatedMtuFraming() {
        val bytes = "0123456789ABCDEFx".toByteArray()
        val frames = Protocol.frames(bytes, 23)
        assertArrayEquals(byteArrayOf(0x53, 1, 0, 0) + "0123456789ABCDEF".toByteArray(), frames[0])
        assertArrayEquals(byteArrayOf(0x53, 2, 1, 0, 'x'.code.toByte()), frames[1])
        assertEquals(frames.map { it.toList() }, Protocol.frames(bytes, 185).map { it.toList() })
        val assembler = FrameAssembler()
        assertNull(assembler.feed(frames[0]))
        assertArrayEquals(bytes, assembler.feed(frames[1]))
        assertArrayEquals(byteArrayOf(0x53, 3, 0, 0, 65), Protocol.frames(byteArrayOf(65), 23).single())
    }
    @Test fun framingBoundsOrderingAndMissingStart() {
        rejects("invalid_frame") { Protocol.frames(ByteArray(2049) { 65 }, 23) }
        rejects("invalid_frame") { Protocol.frames(byteArrayOf(65), 22) }
        rejects("invalid_fragment") { FrameAssembler().feed(byteArrayOf(0x53, 2, 0, 0, 65)) }
        rejects("invalid_fragment") { FrameAssembler().feed(byteArrayOf(0x53, 7, 0, 0, 65)) }
        val frames = Protocol.frames(ByteArray(32) { 65 }, 23)
        val ordered = FrameAssembler()
        ordered.feed(frames[0])
        rejects("invalid_fragment") { ordered.feed(frames[0]) }
        val sequence = FrameAssembler()
        sequence.feed(frames[0])
        rejects("invalid_fragment") { sequence.feed(frames[1].clone().apply { this[2] = 3 }) }
        val bounded = FrameAssembler(16)
        bounded.feed(frames[0])
        rejects("invalid_fragment") { bounded.feed(frames[1]) }
        rejects("invalid_fragment") { FrameAssembler().feed(byteArrayOf(0x53, 3, 0, 0, 0)) }
    }
    @Test fun utf8SurvivesFragmentBoundary() {
        val bytes = ("A".repeat(15) + "ñ🌍").toByteArray()
        val assembler = FrameAssembler()
        var complete: ByteArray? = null
        Protocol.frames(bytes, 23).forEach { complete = assembler.feed(it) }
        assertArrayEquals(bytes, complete)
    }
    @Test fun responseRejectsAuthFailureEvenWithSuccessLookingData() {
        val response = Protocol.response("""{"v":1,"id":1,"code":401,"data":{"homed":true,"message":"ok"}}""".toByteArray(), 1)
        rejects("authentication_failed") { response.requireSuccess() }
        val malformedSuccess = Protocol.response("""{"v":1,"id":1,"code":200,"data":{"error":"bad"}}""".toByteArray(), 1)
        rejects("invalid_success_shape") { malformedSuccess.requireSuccess() }
        rejects("protocol_mismatch") { Protocol.response("""{"v":2,"id":1,"code":200,"data":{}}""".toByteArray(), 1) }
        rejects("request_id_mismatch") { Protocol.response("""{"v":1,"id":2,"code":200,"data":{}}""".toByteArray(), 1) }
        rejects("invalid_response") { Protocol.response("""{"v":"1","id":1,"code":200,"data":{}}""".toByteArray(), 1) }
        rejects("invalid_response") { Protocol.response("""{"v":1,"id":1,"code":200,"data":[]}""".toByteArray(), 1) }
        rejects("invalid_response") { Protocol.response("""{"v":1,"id":1,"code":4294967496,"data":{}}""".toByteArray(), 1) }
        rejects("invalid_utf8") { Protocol.response(byteArrayOf(0xc3.toByte(), 0x28), 1) }
    }
    @Test fun commandsRejectStringsBooleansNonfiniteAndOutOfRange() {
        for (value in listOf("1", true, 181, -181)) {
            rejects("invalid_number") { Protocol.validateCommand("move", JSONObject().put("az", value).put("el", 0)) }
        }
        for (el in listOf(-0.1, 90.1)) {
            rejects("invalid_number") { Protocol.validateCommand("move", JSONObject().put("az", 0).put("el", el)) }
        }
        rejects("level_required") { Protocol.validateCommand("calibrate", JSONObject().put("trueAz", 0).put("levelConfirmed", "true")) }
        rejects("invalid_number") { Protocol.validateCommand("calibrate", JSONObject().put("trueAz", 360).put("levelConfirmed", true)) }
        rejects("invalid_number") { Protocol.validateCommand("site", JSONObject().put("manual", true).put("lat", 0).put("lon", 0).put("alt", 9001)) }
        rejects("invalid_operation") { Protocol.request(1, "test", "enable", JSONObject()) }
    }
    fun status(): JSONObject = JSONObject("""{
        "apiVersion":1,"protocolVersion":1,"firmwareVersion":"0.2.0-prototype",
        "mode":"READY","fault":"","azMechanical":-180.0,"el":0,"homed":true,
        "calibrated":false,"utcValid":true,"utc":1791626400,"siteValid":true,
        "lat":40.0,"lon":-3.0,"alt":600.0,"bleSecure":true,"bleConnected":true
    }""")
    @Test fun statusShapeIsStrictAndSecure() {
        assertFalse(RotorStatus.parse(status()).calibrated)
        assertEquals(-180.0, RotorStatus.parse(status()).az, 0.0)
        rejects("invalid_status") { RotorStatus.parse(status().put("homed", "true")) }
        rejects("invalid_status") { RotorStatus.parse(status().put("mode", "unknown")) }
        rejects("invalid_status") { RotorStatus.parse(status().put("el", "0")) }
        rejects("insecure_firmware_session") { RotorStatus.parse(status().put("bleSecure", false)) }
        rejects("invalid_status") { RotorStatus.parse(status().apply { remove("utcValid") }) }
    }
    @Test fun handshakeRequiresExactFrozenApiProtocolAndFirmwareVersions() {
        rejects("api_version_mismatch") { RotorStatus.parse(status().put("apiVersion", 2)) }
        rejects("api_version_mismatch") { RotorStatus.parse(status().put("apiVersion", "1")) }
        rejects("api_version_mismatch") { RotorStatus.parse(status().apply { remove("apiVersion") }) }
        rejects("protocol_mismatch") { RotorStatus.parse(status().put("protocolVersion", 2)) }
        rejects("firmware_version_mismatch") { RotorStatus.parse(status().put("firmwareVersion", "unknown")) }
        rejects("firmware_version_mismatch") { RotorStatus.parse(status().apply { remove("firmwareVersion") }) }
    }
}
