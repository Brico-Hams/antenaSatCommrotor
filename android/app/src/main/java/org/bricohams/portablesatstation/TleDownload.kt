package org.bricohams.portablesatstation

import java.io.ByteArrayOutputStream
import java.io.InputStream
import java.net.URL
import javax.net.ssl.HttpsURLConnection

enum class TleProvider(val url: String, val label: String) {
    CELESTRAK("https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle", "CelesTrak"),
    AMSAT("https://www.amsat.org/tle/current/dailytle.txt", "AMSAT"),
    PE0SAT("https://tle.pe0sat.nl/kepler/mykepler.txt", "PE0SAT")
}

object TleDownload {
    fun allowed(url: String): Boolean = TleProvider.entries.any { it.url == url }
    fun readBounded(input: InputStream, length: Long, cancelled: () -> Boolean = { false },
                    progress: (Int, Int) -> Unit = { _, _ -> }): ByteArray {
        if (length > TleCatalogue.MAX_BYTES) throw ProtocolFailure("tle_size")
        val result = ByteArrayOutputStream()
        val buffer = ByteArray(2048)
        val deadline = System.nanoTime() + 45_000_000_000L
        while (true) {
            if (cancelled() || Thread.currentThread().isInterrupted) throw java.io.InterruptedIOException("cancelled")
            if (System.nanoTime() > deadline) throw ProtocolFailure("tle_download_timeout")
            val count = input.read(buffer)
            if (count < 0) break
            if (result.size() + count > TleCatalogue.MAX_BYTES) throw ProtocolFailure("tle_size")
            result.write(buffer, 0, count)
            progress(result.size(), if (length > 0) length.toInt() else 0)
        }
        if (length >= 0 && result.size().toLong() != length) throw ProtocolFailure("tle_truncated")
        return result.toByteArray()
    }
    fun fetch(provider: TleProvider, cancelled: () -> Boolean, progress: (Int, Int) -> Unit,
              open: (URL) -> HttpsURLConnection = { it.openConnection() as HttpsURLConnection }): TleCatalogue {
        check(allowed(provider.url))
        // Platform CA trust and hostname verification are unchanged. No token, cookie or location headers.
        val connection = open(URL(provider.url))
        try {
            connection.requestMethod = "GET"
            connection.instanceFollowRedirects = false
            connection.connectTimeout = 15000
            connection.readTimeout = 15000
            connection.useCaches = false
            connection.setRequestProperty("Accept", "text/plain")
            connection.setRequestProperty("Accept-Encoding", "identity")
            connection.setRequestProperty("User-Agent", "PortableSatStation-TLE/0.2")
            if (connection.responseCode != 200) throw ProtocolFailure("tle_http_${connection.responseCode}")
            if (connection.contentEncoding?.let { it != "identity" } == true) throw ProtocolFailure("tle_encoding")
            return connection.inputStream.use {
                TleCatalogue.parse(readBounded(it, connection.contentLengthLong, cancelled, progress), 300)
            }
        } finally { connection.disconnect() }
    }
}
