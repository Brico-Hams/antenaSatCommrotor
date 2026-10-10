package org.bricohams.portablesatstation.orbit

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class OrbitSnapshotJsonTest {
    private fun payload() = JSONObject("""{
        "schemaVersion":1,"generatedUtc":1791626400,"validUntilUtc":1791626460,"sourceConnected":true,
        "catalogue":[{"noradId":25544,"name":"ISS"}],"selectedNoradId":25544,
        "observer":{"name":"Manual site","latitude":48.0,"longitude":2.0,"altitudeMeters":120},
        "subpoint":{"utc":1791626400,"latitude":5.0,"longitude":-175.0},
        "groundTrack":[{"utc":1791626400,"latitude":5.0,"longitude":-175.0}],
        "passes":[{"aosUtc":1791626500,"peakUtc":1791626700,"losUtc":1791626900,"maxElevation":60,"partial":false}],
        "radarTrack":[{"utc":1791626500,"azimuth":150,"elevation":0}],
        "tracking":{"utc":1791626400,"azimuth":100,"elevation":-10},
        "measuredAxes":{"azimuth":100,"elevation":0,"pol":30},"requestedAxes":null,
        "radioProfiles":[{"name":"Operator supplied","mode":"FM","supported":false,
        "uplinkHz":null,"downlinkHz":145800000,"requestedUplinkHz":null,"requestedDownlinkHz":145801234,
        "acknowledgedUplinkHz":null,"acknowledgedDownlinkHz":null}]
    }""")
    private fun rejects(json: JSONObject) {
        try { OrbitSnapshotJson.parse(json); fail("Malformed host data must fail") }
        catch (_: IllegalArgumentException) {}
        catch (_: IllegalStateException) {}
    }
    @Test fun parsesExplicitActualFieldsWithoutInventedDefaults() {
        val s = OrbitSnapshotJson.parse(payload())
        assertEquals(25544, s.selectedNoradId)
        assertEquals(-175.0, s.subpoint!!.point.longitude, 0.0)
        assertNull(s.radioProfiles.single().acknowledgedDownlinkHz)
        assertEquals(1791626500L, s.passes.single().aosUtc)
    }
    @Test fun requiresFieldsIntegerSecondsAndActualNoradIdentity() {
        rejects(payload().apply { remove("groundTrack") })
        rejects(payload().put("schemaVersion", 2))
        rejects(payload().put("generatedUtc", "1791626400"))
        rejects(payload().put("generatedUtc", 1791626400.0))
        rejects(payload().put("selectedNoradId", 0))
        rejects(payload().put("sourceConnected", "true"))
        rejects(payload().apply { getJSONArray("radioProfiles").getJSONObject(0).remove("acknowledgedDownlinkHz") })
    }
    @Test fun rejectsRotorHostEnvelopeUntilAnExplicitAdapterExists() {
        rejects(JSONObject().put("schema", "cm5-rotor/v1").put("ok", true)
            .put("data", JSONObject()))
    }
    @Test fun rejectsCrossSatelliteAndObserverlessPassData() {
        rejects(payload().put("selectedNoradId", 12345))
        rejects(payload().put("observer", JSONObject.NULL))
        rejects(payload().put("selectedNoradId", JSONObject.NULL))
        rejects(payload().apply { getJSONArray("catalogue").put(getJSONArray("catalogue").getJSONObject(0)) })
    }
}
