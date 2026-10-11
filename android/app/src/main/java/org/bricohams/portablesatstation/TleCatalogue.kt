package org.bricohams.portablesatstation

import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction
import java.time.LocalDate
import java.time.ZoneOffset
import java.security.MessageDigest

data class TleEntry(val id: Int, val name: String, val one: String, val two: String, val epoch: Long) {
    fun text(): String = "$name\n$one\n$two\n"
    fun fresh(utc: Long): Boolean = utc > 0 && utc >= epoch - 86400 && utc - epoch <= 14 * 86400
}
data class TleCatalogue(val text: String, val entries: List<TleEntry>) {
    val bytes: ByteArray get() = text.toByteArray(Charsets.US_ASCII)
    val sha256: String get() = sha256(bytes)
    companion object {
        const val MAX_BYTES = 48000
        fun sha256(bytes: ByteArray): String = MessageDigest.getInstance("SHA-256").digest(bytes)
            .joinToString("") { "%02x".format(it.toInt() and 255) }
        fun parse(bytes: ByteArray, maximumEntries: Int = 100): TleCatalogue {
            require(maximumEntries in 1..300)
            if (bytes.size !in 1..MAX_BYTES) throw ProtocolFailure("tle_size")
            val decoded = try {
                Charsets.US_ASCII.newDecoder().onMalformedInput(CodingErrorAction.REPORT)
                    .onUnmappableCharacter(CodingErrorAction.REPORT).decode(ByteBuffer.wrap(bytes)).toString()
            } catch (_: java.nio.charset.CharacterCodingException) { throw ProtocolFailure("tle_ascii") }
            val entries = mutableListOf<TleEntry>()
            val ids = mutableSetOf<Int>()
            var name = ""
            var one: String? = null
            for (rawLine in decoded.replace("\r\n", "\n").split('\n')) {
                // Public feeds sometimes pad lines with trailing blanks or a stray CR; they carry no data.
                val line = rawLine.trimEnd(' ', '\r', '\t')
                if (line.isEmpty()) continue
                if (line.any { it.code !in 32..126 }) throw ProtocolFailure("tle_ascii")
                when {
                    line.startsWith("1 ") -> {
                        if (one != null) throw ProtocolFailure("tle_order")
                        one = line
                    }
                    line.startsWith("2 ") -> {
                        val first = one ?: throw ProtocolFailure("tle_order")
                        val entry = entry(name, first, line)
                        if (!ids.add(entry.id)) throw ProtocolFailure("tle_duplicate")
                        entries += entry
                        if (entries.size > maximumEntries) throw ProtocolFailure("tle_catalog_limit")
                        name = ""; one = null
                    }
                    else -> {
                        if (one != null || line.length > 64 || name.isNotEmpty()) throw ProtocolFailure("tle_name")
                        name = line.removePrefix("0 ")
                    }
                }
            }
            if (one != null || name.isNotEmpty() || entries.isEmpty()) throw ProtocolFailure("tle_order")
            val normalized = entries.joinToString("") { it.text() }
            if (normalized.toByteArray(Charsets.US_ASCII).size > MAX_BYTES) throw ProtocolFailure("tle_size")
            return TleCatalogue(normalized, entries)
        }
        fun subset(candidate: TleCatalogue, selectedIndices: Set<Int>): TleCatalogue {
            if (selectedIndices.size !in 1..100 || selectedIndices.any { it !in candidate.entries.indices })
                throw ProtocolFailure("tle_subset_limit")
            val text = candidate.entries.filterIndexed { index, _ -> index in selectedIndices }.joinToString("") { it.text() }
            return parse(text.toByteArray(Charsets.US_ASCII))
        }
        private fun checksum(line: String, type: Char) {
            if (line.length != 69 || line[0] != type || line[1] != ' ' || !line[68].isDigit())
                throw ProtocolFailure("tle_shape")
            val sum = line.take(68).sumOf { if (it in '0'..'9') it - '0' else if (it == '-') 1 else 0 }
            if (sum % 10 != line[68] - '0') throw ProtocolFailure("tle_checksum")
        }
        private fun number(line: String, start: Int, length: Int): Double =
            line.substring(start, start + length).trim().toDoubleOrNull()?.takeIf { it.isFinite() }
                ?: throw ProtocolFailure("tle_numeric")
        private fun entry(name: String, one: String, two: String): TleEntry {
            checksum(one, '1'); checksum(two, '2')
            val id = one.substring(2, 7)
            if (!id.all { it in '0'..'9' } || id != two.substring(2, 7)) throw ProtocolFailure("tle_catalog_id")
            if (!one.substring(18, 20).all { it in '0'..'9' }) throw ProtocolFailure("tle_epoch")
            val yearTwo = one.substring(18, 20).toInt()
            val year = yearTwo + if (yearTwo < 57) 2000 else 1900
            val day = number(one, 20, 12)
            val january = LocalDate.of(year, 1, 1)
            if (year < 1970 || day < 1 || day >= january.lengthOfYear() + 1) throw ProtocolFailure("tle_epoch")
            val epoch = january.atStartOfDay().toEpochSecond(ZoneOffset.UTC) + ((day - 1) * 86400).toLong()
            number(one, 33, 10)
            for (start in listOf(44, 53)) {
                // A blank positive exponent sign is accepted by the controller and public AMSAT feed.
                if (one[start] !in " +-" || !one.substring(start + 1, start + 6).all { it in '0'..'9' } ||
                    one[start + 6] !in " +-" || one[start + 7] !in '0'..'9')
                    throw ProtocolFailure("tle_numeric")
            }
            val inclination = number(two, 8, 8)
            val node = number(two, 17, 8)
            val argument = number(two, 34, 8)
            val anomaly = number(two, 43, 8)
            val motion = number(two, 52, 11)
            if (!two.substring(26, 33).all { it in '0'..'9' } || inclination !in 0.0..180.0 ||
                node < 0 || node >= 360 || argument < 0 || argument >= 360 || anomaly < 0 || anomaly >= 360 ||
                motion <= 0 || motion > 18) throw ProtocolFailure("tle_numeric")
            return TleEntry(id.toInt(), name.ifEmpty { id }, one, two, epoch)
        }
    }
}
