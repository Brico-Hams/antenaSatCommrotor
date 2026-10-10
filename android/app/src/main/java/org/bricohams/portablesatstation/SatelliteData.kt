package org.bricohams.portablesatstation

import org.json.JSONObject

data class SatelliteData(val id: Int, val name: String) {
    companion object {
        fun parse(data: JSONObject): List<SatelliteData> {
            val list = data.optJSONArray("satellites") ?: throw ProtocolFailure("invalid_satellites")
            if (list.length() > 100) throw ProtocolFailure("invalid_satellites")
            return (0 until list.length()).map { index ->
                val item = list.optJSONObject(index) ?: throw ProtocolFailure("invalid_satellites")
                val id = Protocol.strictInteger(item, "id")
                val name = item.opt("name") as? String ?: throw ProtocolFailure("invalid_satellites")
                if (id !in 0..99 || name.length > 128) throw ProtocolFailure("invalid_satellites")
                SatelliteData(id.toInt(), name)
            }.also { values ->
                if (values.map { it.id }.distinct().size != values.size) throw ProtocolFailure("invalid_satellites")
            }
        }
    }
}
data class CatalogPage(val total: Int, val nextOffset: Int, val satellites: List<SatelliteData>) {
    companion object {
        fun parse(data: JSONObject, offset: Int): CatalogPage {
            val total = Protocol.strictInteger(data, "total")
            val next = Protocol.strictInteger(data, "nextOffset")
            val satellites = SatelliteData.parse(data)
            if (total !in 0..100 || satellites.size > 10 || offset !in 0..99 ||
                satellites.map { it.id } != (offset until offset + satellites.size).toList() ||
                offset + satellites.size > total ||
                next != (if (offset + satellites.size < total) offset + satellites.size.toLong() else -1L) ||
                (satellites.isEmpty() && next != -1L)) throw ProtocolFailure("invalid_catalog")
            return CatalogPage(total.toInt(), next.toInt(), satellites)
        }
    }
}

data class PassData(val calculating: Boolean, val passes: List<Pass>) {
    data class Pass(val aos: Long, val los: Long, val maxEl: Double, val peak: Long, val partial: Boolean)
    companion object {
        fun parse(data: JSONObject): PassData {
            val calculating = data.opt("calculating") as? Boolean ?: throw ProtocolFailure("invalid_passes")
            val list = data.optJSONArray("passes") ?: throw ProtocolFailure("invalid_passes")
            if (list.length() > 100) throw ProtocolFailure("invalid_passes")
            return PassData(calculating, (0 until list.length()).map { index ->
                val item = list.optJSONObject(index) ?: throw ProtocolFailure("invalid_passes")
                val aos = Protocol.strictInteger(item, "aos")
                val los = Protocol.strictInteger(item, "los")
                val maxEl = (item.opt("maxEl") as? Number)?.toDouble() ?: throw ProtocolFailure("invalid_passes")
                val peak = Protocol.strictInteger(item, "peak")
                val partial = item.opt("partial") as? Boolean ?: throw ProtocolFailure("invalid_passes")
                if (aos !in 0..4102444800L || los !in aos..4102444800L || !maxEl.isFinite() || maxEl !in 0.0..90.0)
                    throw ProtocolFailure("invalid_passes")
                if (peak !in aos..los) throw ProtocolFailure("invalid_passes")
                Pass(aos, los, maxEl, peak, partial)
            })
        }
    }
}
