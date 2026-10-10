package org.bricohams.portablesatstation.orbit

import java.util.Collections
import kotlin.math.cos
import kotlin.math.sin

internal fun utc(value: Long) = require(value in 1..4102444800L) { "UTC must be positive Unix seconds through 2100" }
internal fun angle(value: Double, low: Double, high: Double) =
    require(value.isFinite() && value in low..high) { "Invalid angle" }
internal fun label(value: String) = require(value.isNotBlank() && value.length <= 128)
internal fun <T> bounded(values: List<T>, limit: Int): List<T> {
    require(values.size <= limit)
    return Collections.unmodifiableList(ArrayList(values))
}

data class OrbitSatellite(val noradId: Int, val name: String) {
    init { require(noradId in 1..999999999); label(name) }
}
data class GeoPoint(val latitude: Double, val longitude: Double) {
    init { angle(latitude, -90.0, 90.0); angle(longitude, -180.0, 180.0) }
}
data class TimedGeoPoint(val utcSeconds: Long, val point: GeoPoint) {
    init { utc(utcSeconds) }
}
data class ObserverSite(val name: String, val point: GeoPoint, val altitudeMeters: Double) {
    init { label(name); require(altitudeMeters.isFinite() && altitudeMeters in -500.0..10000.0) }
}
data class RadarPoint(val utcSeconds: Long, val azimuthDegrees: Double, val elevationDegrees: Double) {
    init { utc(utcSeconds); angle(azimuthDegrees, 0.0, 360.0); angle(elevationDegrees, -90.0, 90.0) }
}
data class OrbitPass(val aosUtc: Long, val peakUtc: Long, val losUtc: Long, val maxElevation: Double, val partial: Boolean) {
    init {
        utc(aosUtc); utc(peakUtc); utc(losUtc)
        require(aosUtc < losUtc && peakUtc in aosUtc..losUtc)
        angle(maxElevation, 0.0, 90.0)
    }
}
data class ThreeAxisState(val azimuthDegrees: Double, val elevationDegrees: Double, val polDegrees: Double) {
    init {
        angle(azimuthDegrees, 0.0, 360.0); angle(elevationDegrees, -90.0, 90.0)
        angle(polDegrees, -180.0, 180.0)
    }
}
data class RadioProfile(
    val name: String, val mode: String, val supported: Boolean,
    val uplinkHz: Long?, val downlinkHz: Long?,
    val requestedUplinkHz: Long?, val requestedDownlinkHz: Long?,
    val acknowledgedUplinkHz: Long?, val acknowledgedDownlinkHz: Long?
) {
    init {
        label(name); label(mode)
        listOf(uplinkHz, downlinkHz, requestedUplinkHz, requestedDownlinkHz,
            acknowledgedUplinkHz, acknowledgedDownlinkHz).forEach {
            require(it == null || it in 1..100000000000L)
        }
    }
}

/** Host-derived measurements/predictions only; this layer never propagates an orbit. */
class OrbitSnapshot(
    val generatedUtc: Long, val validUntilUtc: Long, val sourceConnected: Boolean,
    catalogue: List<OrbitSatellite>, val selectedNoradId: Int?,
    val observer: ObserverSite?, val subpoint: TimedGeoPoint?,
    groundTrack: List<TimedGeoPoint>, passes: List<OrbitPass>,
    radarTrack: List<RadarPoint>, val tracking: RadarPoint?,
    val measuredAxes: ThreeAxisState?, val requestedAxes: ThreeAxisState?,
    radioProfiles: List<RadioProfile>
) {
    val catalogue = bounded(catalogue, 100)
    val groundTrack = bounded(groundTrack, 720)
    val passes = bounded(passes, 100)
    val radarTrack = bounded(radarTrack, 360)
    val radioProfiles = bounded(radioProfiles, 32)
    init {
        utc(generatedUtc); utc(validUntilUtc); require(validUntilUtc >= generatedUtc)
        require(this.catalogue.map { it.noradId }.distinct().size == this.catalogue.size)
        require(selectedNoradId == null || this.catalogue.any { it.noradId == selectedNoradId })
        require(selectedNoradId != null || (subpoint == null && this.groundTrack.isEmpty() &&
            this.passes.isEmpty() && this.radarTrack.isEmpty() && tracking == null &&
            measuredAxes == null && requestedAxes == null && this.radioProfiles.isEmpty()))
        require(observer != null || (this.passes.isEmpty() && this.radarTrack.isEmpty() && tracking == null))
        require(this.groundTrack.zipWithNext().all { it.first.utcSeconds < it.second.utcSeconds })
        require(this.radarTrack.zipWithNext().all { it.first.utcSeconds < it.second.utcSeconds })
        require(this.passes.zipWithNext().all { it.first.aosUtc <= it.second.aosUtc })
    }
    fun isFresh(nowUtc: Long) = sourceConnected && nowUtc in generatedUtc..validUntilUtc
}

object OrbitGeometry {
    fun project(point: GeoPoint): Pair<Double, Double> =
        Pair((point.longitude + 180.0) / 360.0, (90.0 - point.latitude) / 180.0)
    /** North up, east right; below-horizon samples are not drawn on the visible sky. */
    fun radar(point: RadarPoint): Pair<Double, Double>? {
        if (point.elevationDegrees < 0) return null
        val radius = (90.0 - point.elevationDegrees) / 90.0
        val az = Math.toRadians(point.azimuthDegrees)
        return Pair(radius * sin(az), -radius * cos(az))
    }
    fun filtered(catalogue: List<OrbitSatellite>, query: String, favoritesOnly: Boolean, favorites: Set<Int>) =
        catalogue.filter { (!favoritesOnly || it.noradId in favorites) &&
            (it.name.contains(query.take(128), ignoreCase = true) || it.noradId.toString().contains(query.take(128))) }
    fun alertEligible(pass: OrbitPass, nowUtc: Long) = !pass.partial && pass.aosUtc > nowUtc
}
