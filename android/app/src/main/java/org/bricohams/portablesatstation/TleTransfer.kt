package org.bricohams.portablesatstation

import org.json.JSONObject

/** Mirrors the controller's atomic staging API. Each next command depends on the previous ACK. */
class TleTransfer(private val catalogue: TleCatalogue) {
    data class Command(val operation: String, val body: JSONObject)
    private enum class Stage { NEW, BEGIN, CHUNK, COMMIT, ABORT, DONE }
    private var stage = Stage.NEW
    private var uploadId = 0L
    private var sentThrough = 0
    var received = 0; private set
    var committed = false; private set
    var cancelled = false; private set
    val size: Int get() = catalogue.bytes.size
    val done: Boolean get() = stage == Stage.DONE
    val commitPending: Boolean get() = stage == Stage.COMMIT

    fun begin(status: RotorStatus): Command {
        if (catalogue.entries.size !in 1..100 || catalogue.bytes.size !in 1..TleCatalogue.MAX_BYTES)
            throw ProtocolFailure("tle_catalog_limit")
        if (stage != Stage.NEW || !status.utcValid || status.mode !in setOf("READY", "DISARMED") ||
            catalogue.entries.any { !it.fresh(status.utc) }) throw ProtocolFailure("tle_rotor_not_ready_or_fresh")
        stage = Stage.BEGIN
        return Command("tle/begin", JSONObject().put("length", size).put("sha256", catalogue.sha256))
    }
    fun cancel() { cancelled = true }
    fun acknowledge(operation: String, body: JSONObject): Command? {
        val expected = when (stage) {
            Stage.BEGIN -> "tle/begin"
            Stage.CHUNK -> "tle/chunk"
            Stage.COMMIT -> "tle/commit"
            Stage.ABORT -> "tle/abort"
            else -> throw ProtocolFailure("tle_transfer_sequence")
        }
        if (operation != expected || body.has("error")) throw ProtocolFailure("tle_transfer_sequence")
        when (stage) {
            Stage.BEGIN -> {
                uploadId = Protocol.strictInteger(body, "uploadId")
                if (uploadId !in 1..0xffffffffL) throw ProtocolFailure("tle_upload_id")
            }
            Stage.CHUNK -> {
                if (Protocol.strictInteger(body, "received") != sentThrough.toLong())
                    throw ProtocolFailure("tle_offset_mismatch")
                received = sentThrough
            }
            Stage.COMMIT -> {
                if (body.opt("message") !is String) throw ProtocolFailure("tle_commit_shape")
                committed = true; stage = Stage.DONE; return null
            }
            Stage.ABORT -> {
                if (body.opt("message") !is String) throw ProtocolFailure("tle_commit_shape")
                stage = Stage.DONE; return null
            }
            else -> throw ProtocolFailure("tle_transfer_sequence")
        }
        if (cancelled) {
            stage = Stage.ABORT
            return Command("tle/abort", JSONObject().put("uploadId", uploadId))
        }
        if (received < size) {
            val chunk = catalogue.text.substring(received, minOf(received + 512, size))
            sentThrough = received + chunk.length
            stage = Stage.CHUNK
            return Command("tle/chunk", JSONObject().put("uploadId", uploadId).put("offset", received).put("text", chunk))
        }
        stage = Stage.COMMIT
        return Command("tle/commit", JSONObject().put("uploadId", uploadId))
    }
}
