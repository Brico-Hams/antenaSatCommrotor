package org.bricohams.portablesatstation

import org.json.JSONException
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.util.UUID

class ProtocolFailure(val code: String) : IllegalArgumentException(code)

object Protocol {
    val SERVICE: UUID = UUID.fromString("c8200001-4e53-4253-9000-000000000001")
    val RX: UUID = UUID.fromString("c8200002-4e53-4253-9000-000000000001")
    val TX: UUID = UUID.fromString("c8200003-4e53-4253-9000-000000000001")
    val CCCD: UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
    const val VERSION = 1
    const val API_VERSION = 1
    const val FIRMWARE_VERSION = "0.2.0-prototype"
    const val REQUEST_LIMIT = 2048
    const val RESPONSE_LIMIT = 8192
    const val ALT_MIN = -500.0
    const val ALT_MAX = 9000.0
    private val getOperations = setOf("status", "tle", "passes")
    private val postOperations = setOf("stop", "clear", "home", "move", "calibrate", "site", "select", "track", "catalog",
        "tle/begin", "tle/chunk", "tle/commit", "tle/abort")

    fun request(id: Long, token: String, operation: String, body: JSONObject): ByteArray {
        if (id !in 1..0xffffffffL || token.isEmpty()) throw ProtocolFailure("invalid_request")
        if (operation !in getOperations && operation !in postOperations) throw ProtocolFailure("invalid_operation")
        validateCommand(operation, body)
        val bytes = JSONObject().put("v", VERSION).put("id", id).put("path", "/api/$operation")
            .put("method", if (operation in getOperations) "GET" else "POST")
            .put("token", token).put("body", body).toString().toByteArray(Charsets.UTF_8)
        if (bytes.size > REQUEST_LIMIT) throw ProtocolFailure("request_too_large")
        return bytes
    }
    private fun numeric(body: JSONObject, key: String, low: Double, high: Double, inclusive: Boolean = true): Double {
        val value = body.opt(key)
        if (value !is Number) throw ProtocolFailure("invalid_number")
        val number = value.toDouble()
        if (!number.isFinite() || number < low || (if (inclusive) number > high else number >= high))
            throw ProtocolFailure("invalid_number")
        return number
    }
    fun validateCommand(operation: String, body: JSONObject) {
        fun integer(key: String, minimum: Long, maximum: Long) {
            val value = body.opt(key)
            if (value !is Int && value !is Long) throw ProtocolFailure("invalid_number")
            val number = (value as Number).toLong()
            if (number !in minimum..maximum) throw ProtocolFailure("invalid_number")
        }
        when (operation) {
            "move" -> { numeric(body, "az", -180.0, 180.0); numeric(body, "el", 0.0, 90.0) }
            "calibrate" -> {
                numeric(body, "trueAz", 0.0, 360.0, false)
                if (body.opt("levelConfirmed") != true) throw ProtocolFailure("level_required")
            }
            "site" -> {
                numeric(body, "lat", -90.0, 90.0); numeric(body, "lon", -180.0, 180.0)
                numeric(body, "alt", ALT_MIN, ALT_MAX)
                if (body.opt("manual") !is Boolean) throw ProtocolFailure("invalid_site")
            }
            "select" -> integer("id", 0, 99)
            "catalog" -> {
                integer("offset", 0, 99)
                integer("limit", 1, 10)
            }
            "tle/begin" -> {
                integer("length", 1, TleCatalogue.MAX_BYTES.toLong())
                if (!(body.opt("sha256") as? String ?: "").matches(Regex("[0-9a-f]{64}")))
                    throw ProtocolFailure("tle_hash")
            }
            "tle/chunk" -> {
                integer("uploadId", 1, 0xffffffffL)
                integer("offset", 0, TleCatalogue.MAX_BYTES.toLong() - 1)
                val text = body.opt("text") as? String ?: throw ProtocolFailure("tle_chunk")
                if (text.length !in 1..512 || text.any { it.code > 127 || it == '\u0000' })
                    throw ProtocolFailure("tle_chunk")
            }
            "tle/commit", "tle/abort" -> integer("uploadId", 1, 0xffffffffL)
        }
    }
    /** Firmware v1 fixes the frame to 20 bytes even with a larger negotiated MTU. */
    fun frames(bytes: ByteArray, mtu: Int): List<ByteArray> {
        if (mtu < 23 || bytes.isEmpty() || bytes.size > REQUEST_LIMIT || bytes.any { it == 0.toByte() })
            throw ProtocolFailure("invalid_frame")
        return bytes.toList().chunked(16).mapIndexed { sequence, payload ->
            byteArrayOf(0x53, ((if (sequence == 0) 1 else 0) or
                (if ((sequence + 1) * 16 >= bytes.size) 2 else 0)).toByte(),
                sequence.toByte(), (sequence ushr 8).toByte()) + payload.toByteArray()
        }
    }
    fun response(bytes: ByteArray, expectedId: Long): Response {
        if (bytes.isEmpty() || bytes.size > RESPONSE_LIMIT) throw ProtocolFailure("response_too_large")
        try {
            val decoder = Charsets.UTF_8.newDecoder().onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT)
            val objectValue = JSONObject(decoder.decode(ByteBuffer.wrap(bytes)).toString())
            if (strictInteger(objectValue, "v") != VERSION.toLong()) throw ProtocolFailure("protocol_mismatch")
            val id = strictInteger(objectValue, "id")
            if (id != expectedId || id !in 1..0xffffffffL) throw ProtocolFailure("request_id_mismatch")
            val wireCode = strictInteger(objectValue, "code")
            if (wireCode !in 100..599) throw ProtocolFailure("invalid_response")
            val code = wireCode.toInt()
            val data = objectValue.opt("data") as? JSONObject ?: throw ProtocolFailure("invalid_response")
            return Response(id, code, data)
        } catch (_: JSONException) { throw ProtocolFailure("invalid_json") }
        catch (_: java.nio.charset.CharacterCodingException) { throw ProtocolFailure("invalid_utf8") }
    }
    fun strictInteger(value: JSONObject, key: String): Long {
        val number = value.opt(key)
        if (number !is Number || !number.toDouble().isFinite() || number.toDouble() % 1 != 0.0)
            throw ProtocolFailure("invalid_response")
        return number.toLong()
    }
    data class Response(val id: Long, val code: Int, val data: JSONObject) {
        fun requireSuccess() {
            if (code !in 200..299) throw ProtocolFailure(when (code) {
                401, 403 -> "authentication_failed"
                409 -> "rotor_state_or_control_owner_conflict"
                413 -> "response_too_large_use_http"
                429 -> "firmware_busy"
                else -> "firmware_rejected_$code"
            })
            if (data.has("error")) throw ProtocolFailure("invalid_success_shape")
        }
    }
}

class FrameAssembler(private val limit: Int = Protocol.RESPONSE_LIMIT) {
    private val buffer = ByteArrayOutputStream()
    private var active = false
    private var expected = 0
    fun reset() { buffer.reset(); active = false; expected = 0 }
    fun feed(frame: ByteArray): ByteArray? {
        fun fail(): Nothing { reset(); throw ProtocolFailure("invalid_fragment") }
        if (frame.size !in 5..20 || frame[0] != 0x53.toByte()) fail()
        val flags = frame[1].toInt() and 255
        val sequence = (frame[2].toInt() and 255) or ((frame[3].toInt() and 255) shl 8)
        if (flags and 0xfc != 0) fail()
        if (flags and 1 != 0) {
            if (active || sequence != 0) fail()
            reset(); active = true
        }
        if (!active || sequence != expected || buffer.size() + frame.size - 4 > limit ||
            frame.drop(4).any { it == 0.toByte() }) fail()
        buffer.write(frame, 4, frame.size - 4); expected++
        if (flags and 2 == 0) return null
        val result = buffer.toByteArray(); reset(); return result
    }
}

data class RotorStatus(
    val mode: String, val fault: String, val az: Double, val el: Double,
    val homed: Boolean, val calibrated: Boolean, val utcValid: Boolean, val utc: Long,
    val siteValid: Boolean, val latitude: Double, val longitude: Double, val altitude: Double
) {
    companion object {
        fun parse(data: JSONObject): RotorStatus {
            fun version(key: String, expected: Int, failure: String) {
                val value = data.opt(key) as? Number ?: throw ProtocolFailure(failure)
                if (value.toDouble() != expected.toDouble()) throw ProtocolFailure(failure)
            }
            version("apiVersion", Protocol.API_VERSION, "api_version_mismatch")
            version("protocolVersion", Protocol.VERSION, "protocol_mismatch")
            if (data.opt("firmwareVersion") != Protocol.FIRMWARE_VERSION)
                throw ProtocolFailure("firmware_version_mismatch")
            fun bool(key: String): Boolean = data.opt(key) as? Boolean ?: throw ProtocolFailure("invalid_status")
            fun number(key: String): Double = (data.opt(key) as? Number)?.toDouble()?.takeIf { it.isFinite() }
                ?: throw ProtocolFailure("invalid_status")
            fun text(key: String): String = data.opt(key) as? String ?: throw ProtocolFailure("invalid_status")
            val mode = text("mode")
            if (mode !in setOf("DISARMED", "READY", "HOMING", "MOVING", "TRACKING", "FAULT"))
                throw ProtocolFailure("invalid_status")
            if (!bool("bleSecure") || !bool("bleConnected")) throw ProtocolFailure("insecure_firmware_session")
            val utc = Protocol.strictInteger(data, "utc")
            if (utc !in 0..4102444800L) throw ProtocolFailure("invalid_status")
            return RotorStatus(mode, text("fault"), number("azMechanical"), number("el"),
                bool("homed"), bool("calibrated"), bool("utcValid"), utc,
                bool("siteValid"), number("lat"), number("lon"), number("alt"))
        }
    }
}
