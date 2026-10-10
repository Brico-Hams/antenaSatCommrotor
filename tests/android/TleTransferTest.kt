package org.bricohams.portablesatstation

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class TleTransferTest {
    private fun status(catalogue: TleCatalogue): RotorStatus =
        RotorStatus.parse(ProtocolTest().status().put("utc", catalogue.entries.first().epoch))
    @Test fun beginSequentialByteChunksAndShaCommitMatchActualController() {
        val catalogue = TleCatalogueTest.parse((1..9).joinToString("") { TleCatalogueTest.fixture(it) })
        val upload = TleTransfer(catalogue)
        var command: TleTransfer.Command? = upload.begin(status(catalogue))
        assertEquals("tle/begin", command!!.operation)
        assertEquals(catalogue.bytes.size, command.body.getInt("length"))
        assertEquals(catalogue.sha256, command.body.getString("sha256"))
        Protocol.request(1, "test-local-token", command.operation, command.body)
        command = upload.acknowledge("tle/begin", JSONObject().put("uploadId", 81))
        val transferred = StringBuilder()
        var requestId = 2L
        while (command?.operation == "tle/chunk") {
            val chunk = command.body.getString("text")
            assertEquals(transferred.length, command.body.getInt("offset"))
            assertTrue(chunk.length in 1..512)
            val envelope = Protocol.request(requestId++, "test-local-token", command.operation, command.body)
            assertTrue(envelope.size <= 2048)
            assertTrue(Protocol.frames(envelope, 23).all { it.size <= 20 })
            assertEquals(81, command.body.getInt("uploadId"))
            transferred.append(chunk)
            command = upload.acknowledge(command.operation, JSONObject().put("received", transferred.length))
        }
        assertEquals(catalogue.text, transferred.toString())
        assertEquals("tle/commit", command!!.operation)
        assertTrue(upload.commitPending)
        assertFalse(upload.committed)
        assertNull(upload.acknowledge("tle/commit", JSONObject().put("message", "TLE validado y guardado")))
        assertTrue(upload.done)
        assertTrue(upload.committed)
    }
    @Test fun abortPreservesOldCacheAndNeverPretendsCommitSucceeded() {
        val catalogue = TleCatalogueTest.parse()
        val upload = TleTransfer(catalogue)
        upload.begin(status(catalogue)); upload.cancel()
        val abort = upload.acknowledge("tle/begin", JSONObject().put("uploadId", 2))
        assertEquals("tle/abort", abort!!.operation)
        assertEquals(2, abort.body.getInt("uploadId"))
        assertNull(upload.acknowledge("tle/abort", JSONObject().put("message", "Cache conservada")))
        assertTrue(upload.done); assertFalse(upload.committed)
    }
    @Test fun malformedAckNonsequentialOffsetAndUnsafeRotorFailClosed() {
        val catalogue = TleCatalogueTest.parse()
        for (rotor in listOf(status(catalogue).copy(mode = "MOVING"), status(catalogue).copy(utcValid = false),
            status(catalogue).copy(utc = catalogue.entries.first().epoch + 15 * 86400))) {
            try { TleTransfer(catalogue).begin(rotor); fail() }
            catch (error: ProtocolFailure) { assertEquals("tle_rotor_not_ready_or_fresh", error.code) }
        }
        val upload = TleTransfer(catalogue)
        upload.begin(status(catalogue))
        upload.acknowledge("tle/begin", JSONObject().put("uploadId", 5))
        try { upload.acknowledge("tle/chunk", JSONObject().put("received", 0)); fail() }
        catch (error: ProtocolFailure) { assertEquals("tle_offset_mismatch", error.code) }
        assertFalse(upload.committed)
        try { Protocol.validateCommand("tle/begin", JSONObject().put("length", 48001).put("sha256", "a".repeat(64))); fail() }
        catch (_: ProtocolFailure) { }
        try { Protocol.validateCommand("tle/chunk", JSONObject().put("uploadId", 1).put("offset", 0).put("text", "a".repeat(513))); fail() }
        catch (_: ProtocolFailure) { }
    }
}
