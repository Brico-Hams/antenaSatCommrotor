package org.bricohams.portablesatstation

import org.json.JSONObject

/** Tested command gate shared by the real GATT transport: first command is authenticated status only. */
class ControlSession {
    data class Pending(val id: Long, val operation: String, val bytes: ByteArray)
    private var token = ""
    private var nextId = 1L
    private var handshaking = false
    var authenticated = false; private set
    var pending: Pending? = null; private set
    fun start(credential: String) {
        reset()
        if (credential.isEmpty()) throw ProtocolFailure("token_required")
        token = credential; handshaking = true
    }
    fun reset() {
        token = ""; nextId = 1; handshaking = false; authenticated = false; pending = null
    }
    fun create(operation: String, body: JSONObject): Pending {
        if (pending != null) throw ProtocolFailure("request_busy")
        if (!authenticated && !(handshaking && operation == "status"))
            throw ProtocolFailure("not_authenticated")
        val value = Pending(nextId, operation, Protocol.request(nextId, token, operation, body))
        nextId++; pending = value
        return value
    }
    fun accept(bytes: ByteArray): Protocol.Response {
        val request = pending ?: throw ProtocolFailure("unsolicited_response")
        try {
            val response = Protocol.response(bytes, request.id)
            response.requireSuccess()
            if (request.operation == "status") {
                RotorStatus.parse(response.data)
                if (handshaking) { authenticated = true; handshaking = false }
            }
            pending = null
            return response
        } catch (error: ProtocolFailure) { reset(); throw error }
    }
}
