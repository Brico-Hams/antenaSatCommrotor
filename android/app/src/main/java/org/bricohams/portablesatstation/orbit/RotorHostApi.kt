package org.bricohams.portablesatstation.orbit

import org.json.JSONObject

internal object RotorHostApi {
    const val SCHEMA = "cm5-rotor/v1"

    internal val remoteRouteOperations = setOf(
        "/rotor/status" to "get",
        "/rotor/sensorsstatus" to "get",
        "/rotor/target" to "set",
        "/rotor/track" to "set",
        "/rotor/stop" to "set",
        "/satellites/catalog" to "get",
        "/satellites/passes" to "get"
    )

    fun requestError(path: String, operation: String, data: JSONObject): String? {
        if ((path to operation) !in remoteRouteOperations) return "rotor_route_unsupported"
        val keys = data.keys().asSequence().toSet()
        return when (path) {
            "/rotor/target" -> {
                if (keys != setOf("azDeg", "elDeg", "polDeg")) return "rotor_target_fields"
                val values = listOf("azDeg", "elDeg", "polDeg").map { data.opt(it) }
                if (values.any { it !is Number || !it.toDouble().isFinite() })
                    "rotor_target_values"
                else null
            }
            "/rotor/track" -> {
                val id = data.opt("noradId")
                if (keys != setOf("noradId") || id !is Number ||
                    id.toDouble() % 1.0 != 0.0 || id.toLong() !in 1..999_999_999L)
                    "rotor_track_norad_id"
                else null
            }
            "/satellites/passes" -> {
                val id = data.opt("noradId")
                val limit = if (data.has("limit")) data.opt("limit") else 10
                if (keys != setOf("noradId", "limit") && keys != setOf("noradId"))
                    "rotor_passes_fields"
                else if (id !is Number || id.toDouble() % 1.0 != 0.0 ||
                    id.toLong() !in 1..999_999_999L)
                    "rotor_passes_norad_id"
                else if (limit !is Number || limit.toDouble() % 1.0 != 0.0 ||
                    limit.toInt() !in 1..20)
                    "rotor_passes_limit"
                else null
            }
            else -> if (keys.isNotEmpty()) "rotor_route_fields" else null
        }
    }

    fun response(path: String, operation: String, envelope: JSONObject): Pair<JSONObject?, String?> {
        if ((path to operation) !in remoteRouteOperations || envelope.optString("path") != path)
            throw IllegalArgumentException("unsupported rotor route")
        if (envelope.optInt("v", -1) != 1 || envelope.optString("schema") != SCHEMA)
            throw IllegalArgumentException("incompatible rotor response schema")
        val ok = envelope.opt("ok") as? Boolean
            ?: throw IllegalArgumentException("rotor response missing boolean ok")
        if (ok) {
            val data = envelope.optJSONObject("data")
                ?: throw IllegalArgumentException("successful rotor response missing object data")
            if (envelope.has("error") && !envelope.isNull("error"))
                throw IllegalArgumentException("successful rotor response contains error")
            return data to null
        }
        val error = envelope.opt("error") as? String
        if (error.isNullOrBlank()) throw IllegalArgumentException("failed rotor response missing error")
        if (!envelope.has("data"))
            throw IllegalArgumentException("failed rotor response missing data field")
        if (!envelope.isNull("data") && envelope.optJSONObject("data") == null)
            throw IllegalArgumentException("failed rotor response data must be object or null")
        return null to error
    }
}
