package org.bricohams.portablesatstation

import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Test

class SatelliteDataTest {
    @Test fun usesOnlyRotorCatalogueAndActualPassShape() {
        val list = SatelliteData.parse(JSONObject("""{"satellites":[{"id":0,"name":"TEST-SAT","fresh":true}]}"""))
        assertEquals(0, list.single().id)
        val passes = PassData.parse(JSONObject("""{"calculating":false,"stepSeconds":10,"passes":[
            {"aos":1791626400,"los":1791627000,"peak":1791626700,"maxEl":45.5,"partial":false}]}"""))
        assertEquals(45.5, passes.passes.single().maxEl, 0.0)
    }
    @Test fun invalidRemoteCatalogueAndPassesFailClosed() {
        for (json in listOf("""{"satellites":[{"id":"0","name":"bad"}]}""",
            """{"satellites":[{"id":0,"name":"one"},{"id":0,"name":"duplicate"}]}""")) {
            try { SatelliteData.parse(JSONObject(json)); fail() }
            catch (_: ProtocolFailure) { }
        }
        for (json in listOf("""{"calculating":"false","passes":[]}""",
            """{"calculating":false,"passes":[{"aos":200,"los":100,"maxEl":20}]}""")) {
            try { PassData.parse(JSONObject(json)); fail() }
            catch (_: ProtocolFailure) { }
        }
    }
    @Test fun actualCatalogPagesAreBoundedAndMonotonic() {
        val first = JSONObject("""{"total":11,"nextOffset":10,"satellites":[]}""")
        for (index in 0..9) first.getJSONArray("satellites").put(JSONObject().put("id", index).put("name", "SAT-$index"))
        assertEquals(10, CatalogPage.parse(first, 0).nextOffset)
        val last = JSONObject("""{"total":11,"nextOffset":-1,"satellites":[{"id":10,"name":"LAST"}]}""")
        assertEquals(-1, CatalogPage.parse(last, 10).nextOffset)
        assertEquals(0, CatalogPage.parse(JSONObject("""{"total":0,"nextOffset":-1,"satellites":[]}"""), 0).total)
        try { CatalogPage.parse(first.put("nextOffset", 0), 0); fail() }
        catch (_: ProtocolFailure) { }
        try { Protocol.validateCommand("catalog", JSONObject().put("offset", 0).put("limit", 11)); fail() }
        catch (_: ProtocolFailure) { }
        try { Protocol.validateCommand("select", JSONObject().put("id", 0.0)); fail() }
        catch (_: ProtocolFailure) { }
    }
}
