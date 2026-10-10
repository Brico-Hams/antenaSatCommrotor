package org.bricohams.portablesatstation

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import kotlin.math.PI
import kotlin.math.ceil
import kotlin.math.roundToInt
import kotlin.math.sin
import kotlin.random.Random

class DigitalDecodeTest {
    @Test fun hilbertDemodulatorTracksKnownAudioFrequencies() {
        val samples = ToneVector(2.0).apply {
            tone(1200.0, 500.0)
            tone(1900.0, 500.0)
            tone(2300.0, 500.0)
            tone(1500.0, 500.0)
        }.finish()
        val demodulated = AudioDemodulator.demodulate(samples, AudioPcm.TARGET_SAMPLE_RATE)
        for ((time, expected) in listOf(0.25 to 1200.0, 0.75 to 1900.0, 1.25 to 2300.0, 1.75 to 1500.0)) {
            assertEquals(expected, demodulated.frequencyAt(time).toDouble(), 35.0)
            assertTrue(demodulated.amplitudeAt(time) > 0.4f)
        }
    }

    @Test fun pd120PcmDecodesVisLinePairChromaAndEverySync() {
        val audio = SstvVector(SstvMode.PD120).finish()
        val image = SstvDecoder.decode(audio, AudioPcm.TARGET_SAMPLE_RATE, SstvModeChoice.PD120)
        assertEquals(SstvMode.PD120, image.mode)
        assertEquals(248, image.verifiedLines)
        val rowZero = image.pixels[200 * 640 + 320]
        val rowOne = image.pixels[201 * 640 + 320]
        assertTrue("R-Y chroma is present", red(rowZero) > green(rowZero) + 80)
        assertTrue("the second paired luminance line is brighter", green(rowOne) > green(rowZero) + 80)
    }

    @Test fun pd180PcmDecodesItsDistinctTimingAndVis() {
        val audio = SstvVector(SstvMode.PD180).finish()
        val image = SstvDecoder.decode(audio, AudioPcm.TARGET_SAMPLE_RATE, SstvModeChoice.PD180)
        assertEquals(SstvMode.PD180, image.mode)
        assertEquals(248, image.verifiedLines)
        assertEquals(640 * 496, image.pixels.size)
    }

    @Test fun pd120ReceiveAt8000HzPcmRatePreservesSstvToneRange() {
        val audio = SstvVector(SstvMode.PD120, sampleRate = 8000).finish()
        val image = SstvDecoder.decode(audio, 8000, SstvModeChoice.PD120)
        assertEquals(SstvMode.PD120, image.mode)
        assertEquals(248, image.verifiedLines)
        assertEquals(640 * 496, image.pixels.size)
    }

    @Test fun pd180ReceiveAt8000HzPcmRatePreservesSstvToneRange() {
        val audio = SstvVector(SstvMode.PD180, sampleRate = 8000).finish()
        val image = SstvDecoder.decode(audio, 8000, SstvModeChoice.PD180)
        assertEquals(SstvMode.PD180, image.mode)
        assertEquals(248, image.verifiedLines)
        assertEquals(640 * 496, image.pixels.size)
    }

    @Test fun sstvRejectsNoiseCorruptVisAndWrongSelectedMode() {
        val noise = ShortArray(AudioPcm.TARGET_SAMPLE_RATE) {
            Random(it.toLong()).nextInt(-1200, 1200).toShort()
        }
        rejects("sstv_header_not_found") {
            SstvDecoder.decode(noise, AudioPcm.TARGET_SAMPLE_RATE, SstvModeChoice.PD120)
        }
        val corrupt = SstvVector(SstvMode.PD120, corruptParity = true).finish()
        rejects("sstv_vis_parity") {
            SstvDecoder.decode(corrupt, AudioPcm.TARGET_SAMPLE_RATE, SstvModeChoice.PD120)
        }
        val valid = SstvVector(SstvMode.PD120).finish()
        rejects("sstv_mode_mismatch") {
            SstvDecoder.decode(valid, AudioPcm.TARGET_SAMPLE_RATE, SstvModeChoice.PD180)
        }
    }

    @Test fun wavReaderAcceptsBoundedMonoPcmAndRejectsCompressedAudio() {
        val source = shortArrayOf(0, 12000, -12000, 32767)
        val wav = makeWav(source, AudioPcm.TARGET_SAMPLE_RATE, 1, 16, 1)
        val decoded = PcmWav.read(ByteArrayInputStream(wav))
        assertEquals(AudioPcm.TARGET_SAMPLE_RATE, decoded.sampleRate)
        assertTrue(decoded.samples.contentEquals(source))

        val compressed = makeWav(source, AudioPcm.TARGET_SAMPLE_RATE, 1, 16, 3)
        rejects("wav_pcm_format") { PcmWav.read(ByteArrayInputStream(compressed)) }
        rejects("wav_truncated") { PcmWav.read(ByteArrayInputStream(byteArrayOf(1, 2, 3))) }
    }

    @Test fun pcmSourceSinkPreserveS16LeSamplesAndRejectSampleCounterGaps() {
        val samples = ShortArray(9500) { ((it * 811) % Short.MAX_VALUE).toShort() }
        val source = PcmArraySource(samples, 8000, blockSize = 733)
        val collected = BoundedPcmBuffer(8000, samples.size)
        assertEquals(samples.size.toLong(), source.copyTo(collected, samples.size))
        assertTrue(samples.contentEquals(collected.toAudio().samples))

        val wav = PcmWav.encodeS16(samples, 8000)
        assertEquals(8000, littleEndianInt(wav, 24))
        val imported = PcmWav.read(ByteArrayInputStream(wav))
        assertEquals(AudioPcm.TARGET_SAMPLE_RATE, imported.sampleRate)
        assertEquals((samples.size.toDouble() * AudioPcm.TARGET_SAMPLE_RATE / 8000).toInt(), imported.samples.size)

        val broken = BoundedPcmBuffer(8000, 4)
        broken.write(PcmBlock(42, 900, shortArrayOf(1, 2)))
        rejects("pcm_discontinuity") {
            broken.write(PcmBlock(43, 903, shortArrayOf(3, 4)))
        }
        val wrongSequence = BoundedPcmBuffer(8000, 4)
        wrongSequence.write(PcmBlock(42, 0, shortArrayOf(1, 2)))
        rejects("pcm_discontinuity") {
            wrongSequence.write(PcmBlock(44, 2, shortArrayOf(3, 4)))
        }
    }

    @Test fun ax25CrcKnownCheckAndValidAprsPositionFixture() {
        assertEquals(0x906e, Ax25Crc.crc16X25("123456789".toByteArray(Charsets.US_ASCII)))
        val frame = ax25Frame("N0CALL", "APRS", "!4903.50N/07201.75W>ISS~digital")
        assertEquals(AX25_POSITION_FCS, Ax25Crc.crc16X25(frame))
        val withFcs = frame + byteArrayOf(
            (AX25_POSITION_FCS and 0xff).toByte(),
            (AX25_POSITION_FCS ushr 8).toByte()
        )
        assertTrue(Ax25Crc.hasValidFcs(withFcs))
        val damaged = withFcs.clone().apply { this[15] = (this[15].toInt() xor 0x01).toByte() }
        assertFalse(Ax25Crc.hasValidFcs(damaged))

        val audio = AfskVector(withFcs).finish()
        val packet = Ax25AfskDecoder.decode(audio, AudioPcm.TARGET_SAMPLE_RATE).single()
        assertEquals("N0CALL", packet.source.call)
        assertEquals("APRS", packet.destination.call)
        val aprs = assertNotNullAndReturn(packet.aprs)
        assertEquals(49.058333, aprs.latitude!!, 0.00001)
        assertEquals(-72.029167, aprs.longitude!!, 0.00001)
        assertTrue(aprs.text.contains("ISS~digital"))
        assertTrue(packet.logEntry().contains("[FCS OK]"))
        assertTrue(packet.logEntry().contains("N0CALL>APRS"))
    }

    @Test fun ax25MessageIsInterpretedAndBadAudioNeverProducesFakePacket() {
        val message = AprsTextInterpreter.interpret(":W1AW     :Hello APRS{42".toByteArray(Charsets.US_ASCII))
        assertTrue(message!!.text.contains("Message to W1AW: Hello APRS"))
        assertEquals(AprsMessageKind.MESSAGE, message.message!!.kind)
        assertEquals("42", message.message.messageId)
        val ack = AprsTextInterpreter.interpret(":N0CALL   :ack42".toByteArray(Charsets.US_ASCII))!!
        assertEquals(AprsMessageKind.ACK, ack.message!!.kind)
        assertEquals("42", ack.message.messageId)
        val rej = AprsTextInterpreter.interpret(":N0CALL   :rej42".toByteArray(Charsets.US_ASCII))!!
        assertEquals(AprsMessageKind.REJ, rej.message!!.kind)
        val damaged = ax25Frame("N0CALL", "APRS", ">bad CRC")
        val withWrongCrc = damaged + byteArrayOf(0, 0)
        rejects("afsk_no_valid_ax25") {
            Ax25AfskDecoder.decode(AfskVector(withWrongCrc).finish(), AudioPcm.TARGET_SAMPLE_RATE)
        }
        val noise = ShortArray(AudioPcm.TARGET_SAMPLE_RATE) {
            Random(it.toLong() + 23).nextInt(-1800, 1800).toShort()
        }
        rejects("afsk_no_valid_ax25") {
            Ax25AfskDecoder.decode(noise, AudioPcm.TARGET_SAMPLE_RATE)
        }
    }

    @Test fun aprsMessageEncodesAx25HdlcNrziBell202AndRoundTripsFromPcmWav() {
        val information = AprsMessageCodec.encodeMessageInformation("W1AW", "Hello ISS", "7")
        assertEquals(":W1AW     :Hello ISS{7", information.toString(Charsets.US_ASCII))
        val path = AprsAddressing.parsePath("WIDE1-1,WIDE2-1")!!
        val frame = AprsMessageCodec.encodeUiFrame("EA5KAO-7", "APRS", path, information)
        assertTrue("Encoder must append the valid AX.25 FCS", Ax25Crc.hasValidFcs(frame))

        val audio = Bell202Encoder.encode(frame)
        assertEquals(8000, audio.sampleRate)
        val wav = audio.toWav()
        assertEquals("RIFF", wav.copyOfRange(0, 4).toString(Charsets.US_ASCII))
        assertEquals("WAVE", wav.copyOfRange(8, 12).toString(Charsets.US_ASCII))
        assertEquals(1, littleEndianShort(wav, 22))
        assertEquals(8000, littleEndianInt(wav, 24))
        assertEquals(16, littleEndianShort(wav, 34))
        val imported = PcmWav.read(ByteArrayInputStream(wav))
        val decoded = Ax25AfskDecoder.decode(imported.samples, imported.sampleRate).single()
        assertEquals("EA5KAO", decoded.source.call)
        assertEquals(7, decoded.source.ssid)
        assertEquals(listOf("WIDE1-1", "WIDE2-1"), decoded.digipeaters.map { it.toString() })
        assertTrue(decoded.information.contentEquals(information))
        assertEquals(AprsMessageKind.MESSAGE, decoded.aprs!!.message!!.kind)
        assertEquals("W1AW", decoded.aprs.message.addressee)
        assertEquals("Hello ISS", decoded.aprs.message.text)
        assertEquals("7", decoded.aprs.message.messageId)

        val corruptedFrame = frame.clone().apply { this[20] = (this[20].toInt() xor 0x40).toByte() }
        assertFalse(Ax25Crc.hasValidFcs(corruptedFrame))
    }

    @Test fun aprsCallsignPathAndMessageLengthsAreValidated() {
        assertEquals(null, AprsAddressing.normalizeStation("CALL"))
        assertEquals(null, AprsAddressing.normalizeStation("N0CALL-16"))
        assertEquals(null, AprsAddressing.parsePath("WIDE1-1,WIDE1-1"))
        assertEquals(null, AprsAddressing.parsePath((1..9).joinToString(",") { "WIDE$it-1" }))
        rejects("aprs_message_invalid") {
            AprsMessageCodec.encodeMessageInformation("W1AW", "x".repeat(68), null)
        }
        rejects("aprs_message_id_invalid") {
            AprsMessageCodec.encodeMessageInformation("W1AW", "Test", "bad-id")
        }
    }

    @Test fun aprsInboxOnlyShowsMessagesAndAcknowledgementsAddressedToOwnCallsign() {
        val addressedMessage = messagePacket("W1AW", ":N0CALL-7 :Meet at the lab{A")
        val addressedAck = messagePacket("W1AW", ":N0CALL-7 :ackA")
        val otherStation = messagePacket("W1AW", ":K1OTHER  :Not for K1OTHER")
        assertEquals(
            listOf(
                "W1AW → N0CALL-7: Meet at the lab {A}",
                "Received APRS ACK A from W1AW; not correlated to a local transmission"
            ),
            AprsInbox.addressedTo(listOf(addressedMessage, addressedAck, otherStation), "N0CALL-7")
        )
        assertTrue(AprsInbox.addressedTo(listOf(addressedMessage), "N0CALL").isEmpty())
        assertTrue(AprsInbox.addressedTo(listOf(addressedMessage), "not-a-call").isEmpty())
    }

    private fun messagePacket(sourceCall: String, info: String): Ax25Packet {
        val aprs = AprsTextInterpreter.interpret(info.toByteArray(Charsets.US_ASCII))
        return Ax25Packet(
            Ax25Address("APRS", 0),
            Ax25Address(sourceCall.substringBefore('-'), sourceCall.substringAfter('-', "0").toInt()),
            emptyList(),
            0x03,
            0xf0,
            info.toByteArray(Charsets.US_ASCII),
            aprs
        )
    }

    private fun rejects(code: String, action: () -> Unit) {
        try {
            action()
            throw AssertionError("Expected ProtocolFailure($code)")
        } catch (error: ProtocolFailure) {
            assertEquals(code, error.code)
        }
    }

    private fun assertNotNullAndReturn(value: AprsInterpretation?): AprsInterpretation {
        assertNotNull(value)
        return value!!
    }

    private fun red(pixel: Int): Int = (pixel ushr 16) and 0xff
    private fun green(pixel: Int): Int = (pixel ushr 8) and 0xff
    private fun littleEndianShort(bytes: ByteArray, offset: Int): Int =
        (bytes[offset].toInt() and 0xff) or ((bytes[offset + 1].toInt() and 0xff) shl 8)
    private fun littleEndianInt(bytes: ByteArray, offset: Int): Int =
        littleEndianShort(bytes, offset) or (littleEndianShort(bytes, offset + 2) shl 16)

    private fun makeWav(samples: ShortArray, sampleRate: Int, channels: Int, bits: Int, encoding: Int): ByteArray {
        val dataSize = samples.size * channels * bits / 8
        val bytes = ByteArrayOutputStream()
        fun short(value: Int) {
            bytes.write(value and 0xff)
            bytes.write((value ushr 8) and 0xff)
        }
        fun int(value: Int) {
            short(value and 0xffff)
            short(value ushr 16)
        }
        fun text(value: String) { bytes.write(value.toByteArray(Charsets.US_ASCII)) }
        text("RIFF")
        int(36 + dataSize)
        text("WAVEfmt ")
        int(16)
        short(encoding)
        short(channels)
        int(sampleRate)
        int(sampleRate * channels * bits / 8)
        short(channels * bits / 8)
        short(bits)
        text("data")
        int(dataSize)
        for (sample in samples) short(sample.toInt())
        return bytes.toByteArray()
    }

    private fun ax25Frame(source: String, destination: String, information: String): ByteArray {
        fun address(call: String, last: Boolean): ByteArray {
            require(call.length <= 6)
            val callBytes = call.padEnd(6, ' ').map { (it.code shl 1).toByte() }
            return (callBytes + (0x60 or if (last) 1 else 0).toByte()).toByteArray()
        }
        return address(destination, false) + address(source, true) +
            byteArrayOf(0x03, 0xf0.toByte()) + information.toByteArray(Charsets.US_ASCII)
    }

    private class ToneVector(
        seconds: Double,
        private val sampleRate: Int = AudioPcm.TARGET_SAMPLE_RATE
    ) {
        private val samples = ShortArray(ceil(seconds * sampleRate).toInt() + 4)
        private var cursor = 0
        private var totalMillis = 0.0
        private var phase = 0.0

        fun tone(frequency: Double, durationMillis: Double, amplitude: Double = 0.58) {
            totalMillis += durationMillis
            val end = (totalMillis * sampleRate / 1000.0).roundToInt()
            while (cursor < end) {
                samples[cursor++] = (sin(phase) * amplitude * Short.MAX_VALUE)
                    .roundToInt().toShort()
                phase += 2.0 * PI * frequency / sampleRate
                if (phase >= 2.0 * PI) phase -= 2.0 * PI
            }
        }

        fun silence(durationMillis: Double) {
            totalMillis += durationMillis
            val end = (totalMillis * sampleRate / 1000.0).roundToInt()
            while (cursor < end) samples[cursor++] = 0
        }

        fun finish(): ShortArray = samples.copyOf(cursor)
    }

    private class SstvVector(
        private val mode: SstvMode,
        private val corruptParity: Boolean = false,
        sampleRate: Int = AudioPcm.TARGET_SAMPLE_RATE
    ) {
        private val vector = ToneVector(190.0, sampleRate)

        fun finish(): ShortArray {
            vector.tone(1900.0, 300.0)
            vector.tone(1200.0, 10.0)
            vector.tone(1900.0, 300.0)
            vector.tone(1200.0, 30.0)
            var parity = 0
            for (bit in 0 until 7) {
                val value = (mode.vis ushr bit) and 1
                parity = parity xor value
                vector.tone(if (value == 1) 1100.0 else 1300.0, 30.0)
            }
            vector.tone(
                if ((if (corruptParity) parity xor 1 else parity) == 1) 1100.0 else 1300.0,
                30.0
            )
            vector.tone(1200.0, 30.0)
            for (line in 0 until mode.transmittedLines) {
                vector.tone(1200.0, mode.syncMillis)
                vector.tone(1500.0, mode.porchMillis)
                vector.tone(1900.0, mode.componentMillis)
                vector.tone(2300.0, mode.componentMillis)
                vector.tone(1900.0, mode.componentMillis)
                vector.tone(2300.0, mode.componentMillis)
            }
            vector.silence(50.0)
            return vector.finish()
        }
    }

    private class AfskVector(private val frame: ByteArray) {
        private val symbolRate = 1200.0
        private val sampleRate = AudioPcm.TARGET_SAMPLE_RATE
        private val bytes = ByteArrayOutputStream()
        private var phase = 0.0
        private var totalSymbols = 0L
        private var toneMark = true

        fun finish(): ShortArray {
            repeat(30) { encodeFlag() }
            var consecutiveOnes = 0
            for (value in frame) {
                var byte = value.toInt() and 0xff
                repeat(8) {
                    val bit = byte and 1
                    encodeBit(bit)
                    consecutiveOnes = if (bit == 1) consecutiveOnes + 1 else 0
                    if (consecutiveOnes == 5) {
                        encodeBit(0)
                        consecutiveOnes = 0
                    }
                    byte = byte ushr 1
                }
            }
            repeat(5) { encodeFlag() }
            val raw = bytes.toByteArray()
            return ShortArray(raw.size / 2) { index ->
                ((raw[index * 2].toInt() and 0xff) or (raw[index * 2 + 1].toInt() shl 8)).toShort()
            }
        }

        private fun encodeFlag() {
            for (bit in 0 until 8) encodeBit((0x7e ushr bit) and 1)
        }

        private fun encodeBit(bit: Int) {
            if (bit == 0) toneMark = !toneMark
            totalSymbols++
            val end = (totalSymbols.toDouble() * sampleRate / symbolRate).roundToInt()
            val frequency = if (toneMark) 1200.0 else 2200.0
            while (bytes.size() / 2 < end) {
                val sample = (sin(phase) * 0.58 * Short.MAX_VALUE).roundToInt().toShort().toInt()
                bytes.write(sample and 0xff)
                bytes.write((sample ushr 8) and 0xff)
                phase += 2.0 * PI * frequency / sampleRate
                if (phase >= 2.0 * PI) phase -= 2.0 * PI
            }
        }
    }

    companion object {
        private const val AX25_POSITION_FCS = 0x8840
    }
}
