package org.bricohams.portablesatstation

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class ControlSessionTest {
    private fun response(id: Long, data: JSONObject, code: Int = 200): ByteArray =
        JSONObject().put("v", 1).put("id", id).put("code", code).put("data", data).toString().toByteArray()
    private fun failure(code: String, action: () -> Unit) {
        try { action(); fail(code) } catch (error: ProtocolFailure) { assertEquals(code, error.code) }
    }
    @Test fun actualCallSequenceNeverEnablesMotorsAtConnection() {
        val session = ControlSession()
        session.start("test-local-token")
        assertFalse(session.authenticated)
        failure("not_authenticated") { session.create("home", JSONObject()) }
        val handshake = session.create("status", JSONObject())
        assertEquals(1, handshake.id)
        assertEquals("/api/status", JSONObject(handshake.bytes.toString(Charsets.UTF_8)).getString("path"))
        failure("request_busy") { session.create("status", JSONObject()) }
        session.accept(response(1, ProtocolTest().status()))
        assertTrue(session.authenticated)
        assertNull(session.pending)
        val move = session.create("move", JSONObject().put("az", 0).put("el", 0))
        assertEquals(2, move.id)
        failure("request_busy") { session.create("home", JSONObject()) }
        session.accept(response(2, JSONObject().put("message", "Movimiento iniciado"), 202))
        assertNull(session.pending)
        assertEquals(3, session.create("stop", JSONObject()).id)
        session.reset()
        assertFalse(session.authenticated)
        failure("not_authenticated") { session.create("move", JSONObject().put("az", 0).put("el", 0)) }
    }
    @Test fun authenticationFailureCannotUnlockOrReturnSuccess() {
        val session = ControlSession()
        session.start("invalid-test-token")
        session.create("status", JSONObject())
        failure("authentication_failed") { session.accept(response(1, ProtocolTest().status(), 401)) }
        assertFalse(session.authenticated)
        assertNull(session.pending)
        failure("not_authenticated") { session.create("home", JSONObject()) }
    }
    @Test fun malformedStatusAndWrongRequestIdFailClosed() {
        val session = ControlSession()
        session.start("test")
        session.create("status", JSONObject())
        failure("api_version_mismatch") { session.accept(response(1, JSONObject())) }
        assertFalse(session.authenticated)
        session.start("test")
        session.create("status", JSONObject())
        failure("request_id_mismatch") { session.accept(response(2, ProtocolTest().status())) }
        assertFalse(session.authenticated)
    }
}
