package org.bricohams.portablesatstation

import org.junit.Assert.*
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.File
import java.net.URL
import java.security.cert.Certificate
import javax.net.ssl.HttpsURLConnection

class TleDownloadTest {
    private class FakeHttps(url: URL, private val data: ByteArray, private val code: Int = 200) : HttpsURLConnection(url) {
        var closed = false
        override fun disconnect() { closed = true }
        override fun usingProxy() = false
        override fun connect() {}
        override fun getCipherSuite() = "TLS_AES_128_GCM_SHA256"
        override fun getLocalCertificates(): Array<Certificate>? = null
        override fun getServerCertificates(): Array<Certificate> = emptyArray()
        override fun getResponseCode() = code
        override fun getContentLengthLong() = data.size.toLong()
        override fun getContentEncoding(): String? = null
        override fun getInputStream() = ByteArrayInputStream(data)
    }
    @Test fun exactHttpsAllowlistNoUploadsTokensOrRedirectFallback() {
        for (provider in TleProvider.entries) assertTrue(TleDownload.allowed(provider.url))
        for (url in listOf("http://www.amsat.org/tle/current/dailytle.txt",
            "https://www.amsat.org.evil.invalid/tle/current/dailytle.txt",
            "https://www.amsat.org/tle/current/dailytle.txt?token=secret",
            "https://user:pass@www.amsat.org/tle/current/dailytle.txt")) assertFalse(TleDownload.allowed(url))
        var connection: FakeHttps? = null
        val value = TleDownload.fetch(TleProvider.AMSAT, { false }, { _, _ -> }) { url ->
            FakeHttps(url, TleCatalogueTest.fixture().toByteArray()).also { connection = it }
        }
        assertEquals(1, value.entries.size)
        val actual = checkNotNull(connection)
        assertEquals("GET", actual.requestMethod)
        assertFalse(actual.doOutput)
        assertFalse(actual.instanceFollowRedirects)
        assertNull(actual.getRequestProperty("X-Control-Token"))
        assertNull(actual.getRequestProperty("Cookie"))
        assertTrue(actual.closed)
        try {
            TleDownload.fetch(TleProvider.AMSAT, { false }, { _, _ -> }) { url -> FakeHttps(url, byteArrayOf(), 302) }
            fail()
        } catch (failure: ProtocolFailure) { assertEquals("tle_http_302", failure.code) }
    }
    @Test fun boundedReadsCancellationAndTruncationAreNotSuccess() {
        try { TleDownload.readBounded(ByteArrayInputStream(ByteArray(48001)), -1); fail() }
        catch (failure: ProtocolFailure) { assertEquals("tle_size", failure.code) }
        try { TleDownload.readBounded(ByteArrayInputStream(byteArrayOf(1)), 2); fail() }
        catch (failure: ProtocolFailure) { assertEquals("tle_truncated", failure.code) }
        try { TleDownload.readBounded(ByteArrayInputStream(byteArrayOf(1)), 1, { true }); fail() }
        catch (_: java.io.InterruptedIOException) { }
    }
    @Test fun privateCacheOnlyChangesAfterValidatedAtomicReplacement() {
        val directory = File("build/android-cache-test").apply { mkdirs() }
        val cache = TleCache(directory)
        val good = TleCatalogueTest.parse()
        try {
            cache.save(good)
            assertEquals(good.sha256, cache.load()!!.sha256)
            try { cache.save(TleCatalogue("INVALID", good.entries)); fail() }
            catch (_: ProtocolFailure) { }
            assertEquals(good.sha256, cache.load()!!.sha256)
            val next = TleCatalogueTest.parse(TleCatalogueTest.fixture(6))
            cache.save(next)
            assertEquals(next.sha256, cache.load()!!.sha256)
            assertFalse(File(directory, "validated-tle.new").exists())
        } finally {
            File(directory, "validated-tle.txt").delete()
            File(directory, "validated-tle.new").delete()
            directory.delete()
        }
    }
}
