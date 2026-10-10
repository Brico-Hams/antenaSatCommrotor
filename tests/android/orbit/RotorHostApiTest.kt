package org.bricohams.portablesatstation.orbit

import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class RotorHostApiTest {
    @Test fun permitsOnlyVerifiedRemoteRotorAndSatelliteRoutes() {
        val reads = listOf(
            "/rotor/status" to "get",
            "/rotor/sensorsstatus" to "get",
            "/satellites/catalog" to "get"
        )
        reads.forEach { (path, operation) ->
            assertNull(RotorHostApi.requestError(path, operation, JSONObject()))
        }
        assertNull(RotorHostApi.requestError("/satellites/passes", "get",
            JSONObject().put("noradId", 25544).put("limit", 10)))
        assertNull(RotorHostApi.requestError("/rotor/track", "set",
            JSONObject().put("noradId", 25544)))
        assertNull(RotorHostApi.requestError("/rotor/target", "set",
            JSONObject().put("azDeg", 12.5).put("elDeg", 45.0).put("polDeg", -10.0)))
        assertNull(RotorHostApi.requestError("/rotor/stop", "set", JSONObject()))

        assertEquals("rotor_route_unsupported",
            RotorHostApi.requestError("/rotor/home", "set", JSONObject()))
        assertEquals("rotor_route_unsupported",
            RotorHostApi.requestError("/rotor/calibrate", "set", JSONObject()))
        assertEquals("rotor_route_unsupported",
            RotorHostApi.requestError("/rotor/status", "set", JSONObject()))
    }

    @Test fun validatesExactMotionPayloadsAndHostReplySemantics() {
        assertEquals("rotor_target_fields", RotorHostApi.requestError(
            "/rotor/target", "set", JSONObject().put("azDeg", 1).put("elDeg", 2)))
        assertEquals("rotor_target_values", RotorHostApi.requestError(
            "/rotor/target", "set", JSONObject().put("azDeg", "NaN")
                .put("elDeg", 2).put("polDeg", 3)))
        assertEquals("rotor_track_norad_id", RotorHostApi.requestError(
            "/rotor/track", "set", JSONObject().put("noradId", 0)))
        assertEquals("rotor_passes_limit", RotorHostApi.requestError(
            "/satellites/passes", "get", JSONObject().put("noradId", 25544).put("limit", 21)))

        val data = JSONObject().put("state", "READY")
        val (parsed, error) = RotorHostApi.response("/rotor/status", "get",
            JSONObject().put("v", 1).put("id", "r1").put("path", "/rotor/status")
                .put("schema", "cm5-rotor/v1").put("ok", true).put("data", data)
                .put("error", JSONObject.NULL))
        assertEquals(data.toString(), parsed.toString())
        assertNull(error)

        val (failedData, failedError) = RotorHostApi.response("/rotor/target", "set",
            JSONObject().put("v", 1).put("id", "r2").put("path", "/rotor/target")
                .put("schema", "cm5-rotor/v1").put("ok", false).put("data", JSONObject.NULL)
                .put("error", "rotor not commissioned"))
        assertNull(failedData)
        assertEquals("rotor not commissioned", failedError)
    }
}
