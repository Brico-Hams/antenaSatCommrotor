package org.bricohams.portablesatstation

import org.junit.Assert.*
import org.junit.Test
import java.time.Instant

class TleCatalogueTest {
    companion object {
        private const val ONE = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
        private const val TWO = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
        fun checksum(line: String): String {
            val base = line.take(68)
            return base + (base.sumOf { if (it in '0'..'9') it - '0' else if (it == '-') 1 else 0 } % 10)
        }
        fun fixture(id: Int = 5, epoch: String = "26283.50000000"): String {
            val norad = "%05d".format(id)
            val first = ONE.substring(0, 2) + norad + ONE.substring(7, 18) + epoch + ONE.substring(32)
            val second = TWO.substring(0, 2) + norad + TWO.substring(7)
            return "TEST-$id\n${checksum(first)}\n${checksum(second)}\n"
        }
        fun parse(text: String = fixture()): TleCatalogue = TleCatalogue.parse(text.toByteArray(Charsets.US_ASCII))
    }
    private fun reject(code: String, text: String) {
        try { parse(text); fail(code) } catch (failure: ProtocolFailure) { assertEquals(code, failure.code) }
    }
    @Test fun mirrorsValladoEpochAndChecksumsWithoutPhonePropagation() {
        val published = parse("VALLADO-TEST\n$ONE\n$TWO\n")
        assertEquals(962131819L, published.entries.single().epoch)
        val current = parse()
        assertEquals(Instant.parse("2026-10-10T12:00:00Z").epochSecond, current.entries.single().epoch)
        assertEquals(current.text, parse(current.text.replace("\n", "\r\n")).text)
        assertEquals(64, current.sha256.length)
        assertEquals(current.bytes.size, current.text.length)
    }
    @Test fun rejectsChecksumOrderIdsNumericFieldsEpochAndNonAscii() {
        val valid = fixture()
        reject("tle_checksum", valid.replace(".00000023", ".00000024"))
        reject("tle_order", valid.lines()[2] + "\n")
        reject("tle_duplicate", valid + valid)
        reject("tle_epoch", fixture(epoch = "26366.00000000"))
        reject("tle_epoch", fixture(epoch = "69001.00000000"))
        val nonNumeric = valid.lines().toMutableList()
        nonNumeric[2] = checksum(nonNumeric[2].replaceRange(8, 16, "     NaN"))
        reject("tle_numeric", nonNumeric.joinToString("\n"))
        val mismatch = valid.lines().toMutableList()
        mismatch[2] = checksum(mismatch[2].replaceRange(2, 7, "00006"))
        reject("tle_catalog_id", mismatch.joinToString("\n"))
        try { TleCatalogue.parse("ñ\n".toByteArray()); fail() }
        catch (failure: ProtocolFailure) { assertEquals("tle_ascii", failure.code) }
    }
    @Test fun catalogAndByteBoundsAreEnforced() {
        assertEquals(100, parse((1..100).joinToString("") { fixture(it) }).entries.size)
        reject("tle_catalog_limit", (1..101).joinToString("") { fixture(it) })
        try { TleCatalogue.parse(ByteArray(48001) { 65 }); fail() }
        catch (failure: ProtocolFailure) { assertEquals("tle_size", failure.code) }
        reject("tle_name", "A".repeat(65) + "\n" + fixture().substringAfter('\n'))
        reject("tle_order", fixture() + "UNPAIRED NAME\n")
    }
    @Test fun freshnessUsesRotorUtcNotPhoneClockAndNeverInventsFrequencies() {
        val entry = parse().entries.single()
        assertTrue(entry.fresh(entry.epoch + 14 * 86400))
        assertFalse(entry.fresh(entry.epoch + 14 * 86400 + 1))
        assertTrue(entry.fresh(entry.epoch - 86400))
        assertFalse(entry.fresh(entry.epoch - 86401))
        assertFalse(entry.fresh(0))
    }
    @Test fun realAmsatBlankZeroExponentIsAcceptedWithoutRewritingChecksum() {
        val lines = fixture().lines().toMutableList()
        lines[1] = checksum(lines[1].replaceRange(44, 52, " 00000 0"))
        val catalogue = parse(lines.joinToString("\n"))
        assertEquals(" 00000 0", catalogue.entries.single().one.substring(44, 52))
        lines[1] = checksum(lines[1].replaceRange(44, 52, " 12345 0"))
        assertEquals(" 12345 0", parse(lines.joinToString("\n")).entries.single().one.substring(44, 52))
        lines[1] = checksum(lines[1].replaceRange(44, 52, " 12345?0"))
        reject("tle_numeric", lines.joinToString("\n"))
    }
    @Test fun largerProviderRequiresExplicitBoundedSubsetNeverSilentTruncation() {
        val source = (1..110).joinToString("") { fixture(it) }.toByteArray(Charsets.US_ASCII)
        val candidate = TleCatalogue.parse(source, 300)
        assertEquals(110, candidate.entries.size)
        val subset = TleCatalogue.subset(candidate, setOf(0, 109))
        assertEquals(listOf(1, 110), subset.entries.map { it.id })
        assertEquals(2, TleCatalogue.parse(subset.bytes).entries.size)
        for (selection in listOf(emptySet(), (-1..2).toSet(), (0..100).toSet())) {
            try { TleCatalogue.subset(candidate, selection); fail() }
            catch (error: ProtocolFailure) { assertEquals("tle_subset_limit", error.code) }
        }
    }
}
