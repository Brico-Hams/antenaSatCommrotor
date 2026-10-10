package org.bricohams.portablesatstation.orbit

import org.json.JSONObject

/** Proposed adapter schema, not a claim that the rotor exposes this response or any endpoint. */
object OrbitSnapshotJson {
    private fun JSONObject.number(key: String): Double {
        val n = opt(key) as? Number ?: error("Missing numeric $key")
        return n.toDouble().also { require(it.isFinite()) }
    }
    private fun JSONObject.integer(key: String): Long {
        val n = opt(key)
        require(n is Int || n is Long) { "Missing integer $key" }
        return (n as Number).toLong()
    }
    private fun JSONObject.id(key: String): Int = integer(key).also { require(it in 1..999999999L) }.toInt()
    private fun JSONObject.text(key: String): String = (opt(key) as? String ?: error("Missing $key")).also { label(it) }
    private fun JSONObject.bool(key: String): Boolean = opt(key) as? Boolean ?: error("Missing boolean $key")
    private fun JSONObject.geo() = GeoPoint(number("latitude"), number("longitude"))
    private fun JSONObject.sky() = RadarPoint(integer("utc"), number("azimuth"), number("elevation"))
    private fun JSONObject.axes() = ThreeAxisState(number("azimuth"), number("elevation"), number("pol"))
    private fun <T> JSONObject.optional(key: String, transform: (JSONObject) -> T): T? {
        require(has(key)) { "Missing $key (explicit null required for unavailable data)" }
        if (isNull(key)) return null
        return transform(optJSONObject(key) ?: error("Invalid $key"))
    }
    private fun JSONObject.hz(key: String): Long? {
        require(has(key))
        return if (isNull(key)) null else integer(key)
    }
    private fun <T> JSONObject.list(key: String, limit: Int, transform: (JSONObject) -> T): List<T> {
        val array = optJSONArray(key) ?: error("Missing array $key")
        require(array.length() <= limit)
        return (0 until array.length()).map { transform(array.optJSONObject(it) ?: error("Invalid $key item")) }
    }
    fun parse(data: JSONObject): OrbitSnapshot {
        require(data.integer("schemaVersion") == 1L)
        require(data.has("selectedNoradId"))
        return OrbitSnapshot(
            data.integer("generatedUtc"), data.integer("validUntilUtc"), data.bool("sourceConnected"),
            data.list("catalogue", 100) { OrbitSatellite(it.id("noradId"), it.text("name")) },
            if (data.isNull("selectedNoradId")) null else data.id("selectedNoradId"),
            data.optional("observer") { ObserverSite(it.text("name"), it.geo(), it.number("altitudeMeters")) },
            data.optional("subpoint") { TimedGeoPoint(it.integer("utc"), it.geo()) },
            data.list("groundTrack", 720) { TimedGeoPoint(it.integer("utc"), it.geo()) },
            data.list("passes", 100) { OrbitPass(it.integer("aosUtc"), it.integer("peakUtc"),
                it.integer("losUtc"), it.number("maxElevation"), it.bool("partial")) },
            data.list("radarTrack", 360) { it.sky() }, data.optional("tracking") { it.sky() },
            data.optional("measuredAxes") { it.axes() }, data.optional("requestedAxes") { it.axes() },
            data.list("radioProfiles", 32) { RadioProfile(it.text("name"), it.text("mode"), it.bool("supported"),
                it.hz("uplinkHz"), it.hz("downlinkHz"), it.hz("requestedUplinkHz"), it.hz("requestedDownlinkHz"),
                it.hz("acknowledgedUplinkHz"), it.hz("acknowledgedDownlinkHz")) }
        )
    }
}
