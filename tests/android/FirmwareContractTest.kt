package org.bricohams.portablesatstation

import org.junit.Assert.*
import org.junit.Test
import java.io.File

/** Detects drift against the actual checked-in controller, not a second invented API fixture. */
class FirmwareContractTest {
    @Test fun frozenGattAndVersionConstantsMatchControllerSource() {
        val working = File(checkNotNull(System.getProperty("user.dir"))).canonicalFile
        val root = generateSequence(working) { it.parentFile }.take(3).firstOrNull {
            it.resolve("firmware").resolve("include").resolve("ble_protocol.h").isFile
        } ?: error("Controller source required to verify the frozen BLE contract")
        val header = root.resolve("firmware").resolve("include").resolve("ble_protocol.h").readText()
        val source = root.resolve("firmware").resolve("src").resolve("main.cpp").readText()
        fun constant(name: String): Long =
            Regex("""(?:constexpr\s+(?:uint32_t|size_t)\s+|,\s*)$name\s*=\s*(\d+)""")
                .find(header)?.groupValues?.get(1)?.toLong() ?: error("Missing controller constant $name")
        assertEquals(Protocol.VERSION.toLong(), constant("protocolVersion"))
        assertEquals(Protocol.API_VERSION.toLong(), constant("apiVersion"))
        assertEquals(Protocol.REQUEST_LIMIT.toLong(), constant("maxRequest"))
        assertEquals(20L, constant("frameBytes"))
        assertEquals(4L, constant("headerBytes"))
        assertEquals(16L, constant("payloadBytes"))
        assertTrue(header.contains("\"${Protocol.FIRMWARE_VERSION}\""))
        for (uuid in listOf(Protocol.SERVICE, Protocol.RX, Protocol.TX))
            assertTrue("GATT UUID drift: $uuid", source.contains("\"$uuid\""))
        for (key in listOf("apiVersion", "protocolVersion", "firmwareVersion"))
            assertTrue("Missing real status version field: $key", source.contains("\"$key\""))
        assertTrue(source.contains("\"/api/catalog\""))
        for (route in listOf("begin", "chunk", "commit", "abort"))
            assertTrue(source.contains("\"/api/tle/$route\""))
        val control = root.resolve("firmware").resolve("include").resolve("control_logic.h").readText()
        assertTrue("Public AMSAT blank positive exponent support must remain available",
            control.contains("one[start + 6] != ' '"))
    }
}
