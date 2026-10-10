package org.bricohams.portablesatstation.orbit

import org.junit.Assert.*
import org.junit.Test

class OrbitModelsTest {
    private fun snapshot(points: List<TimedGeoPoint> = emptyList(), connected: Boolean = true) = OrbitSnapshot(
        1000, 2000, connected, listOf(OrbitSatellite(25544, "ISS")), 25544, null, null,
        points, emptyList(), emptyList(), null, null, null, emptyList()
    )
    private fun rejects(block: () -> Unit) {
        try { block(); fail("Expected invalid supplied data to fail closed") }
        catch (_: IllegalArgumentException) {}
    }
    @Test fun immutableSnapshotCopiesHostLists() {
        val points = mutableListOf(TimedGeoPoint(1200, GeoPoint(10.0, 20.0)))
        val value = snapshot(points)
        points.clear()
        assertEquals(1, value.groundTrack.size)
        try { (value.groundTrack as MutableList).clear(); fail("Must not be mutable") }
        catch (_: UnsupportedOperationException) {}
    }
    @Test fun geographicProjectionIsActualCoordinatesNotOrbitPropagation() {
        assertEquals(Pair(0.0, 0.0), OrbitGeometry.project(GeoPoint(90.0, -180.0)))
        assertEquals(Pair(1.0, 1.0), OrbitGeometry.project(GeoPoint(-90.0, 180.0)))
        assertEquals(Pair(0.5, 0.5), OrbitGeometry.project(GeoPoint(0.0, 0.0)))
        rejects { GeoPoint(Double.NaN, 0.0) }
        rejects { GeoPoint(0.0, 181.0) }
    }
    @Test fun radarHasNorthUpEastRightAndHorizonBounds() {
        val north = OrbitGeometry.radar(RadarPoint(1000, 0.0, 0.0))!!
        assertEquals(0.0, north.first, 0.000001); assertEquals(-1.0, north.second, 0.000001)
        val east = OrbitGeometry.radar(RadarPoint(1000, 90.0, 0.0))!!
        assertEquals(1.0, east.first, 0.000001); assertEquals(0.0, east.second, 0.000001)
        assertEquals(Pair(0.0, -0.0), OrbitGeometry.radar(RadarPoint(1000, 0.0, 90.0)))
        assertNull(OrbitGeometry.radar(RadarPoint(1000, 0.0, -1.0)))
        rejects { RadarPoint(1000, 361.0, 10.0) }
    }
    @Test fun freshnessNeverClaimsDisconnectedFutureOrExpiredDataLive() {
        assertTrue(snapshot().isFresh(1500))
        assertFalse(snapshot(connected = false).isFresh(1500))
        assertFalse(snapshot().isFresh(999)); assertFalse(snapshot().isFresh(2001))
    }
    @Test fun aosIsUtcAndPastPartialAndInvalidPassesAreRejected() {
        val pass = OrbitPass(1791626400, 1791626700, 1791627000, 45.0, false)
        assertTrue(OrbitGeometry.alertEligible(pass, 1791626399))
        assertFalse(OrbitGeometry.alertEligible(pass, 1791626400))
        assertFalse(OrbitGeometry.alertEligible(pass.copy(partial = true), 1791626399))
        rejects { pass.copy(losUtc = pass.aosUtc) }
        rejects { pass.copy(peakUtc = pass.losUtc + 1) }
        rejects { pass.copy(aosUtc = 1791626400000) }
    }
    @Test fun boundedTracksMonotonicTimestampsAndNoradFavorites() {
        rejects { snapshot(List(721) { TimedGeoPoint(1000 + it.toLong(), GeoPoint(0.0, 0.0)) }) }
        rejects { snapshot(listOf(TimedGeoPoint(1500, GeoPoint(0.0, 0.0)), TimedGeoPoint(1400, GeoPoint(0.0, 0.0)))) }
        val sats = listOf(OrbitSatellite(25544, "ISS"), OrbitSatellite(43017, "AO-91"))
        assertEquals(listOf(sats[0]), OrbitGeometry.filtered(sats, "iss", true, setOf(25544)))
        assertEquals(listOf(sats[1]), OrbitGeometry.filtered(sats, "43017", false, emptySet()))
        assertTrue(OrbitGeometry.filtered(sats, "", true, setOf(0)).isEmpty())
        rejects { OrbitSatellite(0, "Rotor slot is not a NORAD ID") }
    }
    @Test fun unknownRadioValuesStayUnknownAndPolIsIndependent() {
        val profile = RadioProfile("User profile", "unknown", false, null, null, null, null, null, null)
        assertNull(profile.downlinkHz); assertFalse(profile.supported)
        rejects { profile.copy(downlinkHz = 0) }
        assertEquals(-90.0, ThreeAxisState(180.0, 30.0, -90.0).polDegrees, 0.0)
        rejects { ThreeAxisState(0.0, 0.0, Double.POSITIVE_INFINITY) }
    }
}
