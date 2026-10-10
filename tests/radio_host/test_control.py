import asyncio
import json
import struct
import unittest
from types import SimpleNamespace

from radio.control import Cat, Dispatcher
from radio.protocol import Audio, ControlAssembler, HEADER, fragments
from radio.safety import Safety, band


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def fixture():
    clock = Clock()
    stops = []
    safety = Safety(lambda: stops.append("stop"), clock, lambda: 1000 + clock.now - 100)
    audio = Audio(safety.inhibit)
    dispatcher = Dispatcher(safety, audio, "a" * 64)
    return clock, stops, safety, audio, dispatcher


class SafetyTests(unittest.TestCase):
    def ready(self):
        clock, stops, safety, audio, dispatcher = fixture()
        safety.connect("peer")
        safety.physical(True, True)
        safety.sdr_ready = True
        safety.tracking_update(1000, 1000, [42, 2, 20], True)
        safety.rotor_update(None, True)
        safety.polarization = SimpleNamespace(ready=lambda: True)
        return clock, stops, safety

    def test_all_interlocks_and_start_failclosed(self):
        _, _, safety, _, _ = fixture()
        self.assertFalse(safety.check())
        for session in (None, "peer"):
            with self.assertRaises(PermissionError):
                safety.lease(session, 500)
        clock, stops, safety = self.ready()
        safety.lease("peer", 500)
        self.assertTrue(safety.check())
        safety.transmitting = True
        clock.now += 0.501
        self.assertFalse(safety.check())
        self.assertFalse(safety.transmitting)
        self.assertTrue(stops)

    def test_release_disconnect_fault_tune_inhibit(self):
        for action in ("arm", "ptt", "disconnect", "fault", "tune", "sdr"):
            clock, stops, safety = self.ready()
            safety.lease("peer", 500)
            safety.transmitting = True
            if action == "arm":
                safety.physical(False, True)
            elif action == "ptt":
                safety.physical(True, False)
            elif action == "disconnect":
                safety.disconnect("peer")
            elif action == "fault":
                safety.inhibit("injected-fault")
            elif action == "tune":
                safety.tune(rx=145_950_000)
            else:
                safety.sdr_ready = False
            self.assertFalse(safety.check(), action)
            self.assertFalse(safety.transmitting, action)

    def test_tracking_freshness_provenance_and_range(self):
        clock, _, safety = self.ready()
        safety.lease("peer", 500)
        clock.now += 1.001
        self.assertFalse(safety.check())
        self.assertFalse(safety.tracking_fresh())
        with self.assertRaises(ValueError):
            safety.tracking_update(0, 1001, [0, 0, 0], False)
        for args in ((0, 950, [0, 0, 0]), (0, 1001, [91, 0, 0]),
                     (float("nan"), 1001, [0, 0, 0])):
            with self.assertRaises(ValueError):
                safety.tracking_update(*args, True)
        for milliseconds in (0, 501, 3.5, True):
            with self.assertRaises(ValueError):
                safety.lease("peer", milliseconds)
        with self.assertRaises(ValueError):
            safety.tune(tx=145_900_000)
        for frequency in (143_999_999, 146_000_001, 429_999_999, 440_000_001, 145000000.0):
            with self.assertRaises(ValueError):
                band(frequency)


class WireTests(unittest.TestCase):
    def test_original_control_fragmentation_and_invalid_sequences(self):
        message = {"v": 1, "id": "a", "path": "/status", "op": "get", "data": {}}
        assembler = ControlAssembler()
        frames = list(fragments(message, 65535))
        self.assertTrue(all(len(frame) == 20 for frame in frames))
        results = [assembler.feed(frame) for frame in frames]
        self.assertEqual(results[-1], message)
        self.assertTrue(all(x is None for x in results[:-1]))
        with self.assertRaises(ValueError):
            assembler.feed(bytes(20))
        assembler.feed(frames[0])
        bad = frames[1][:2] + b"\0\0" + frames[1][4:]
        with self.assertRaises(ValueError):
            assembler.feed(bad)
        with self.assertRaises(ValueError):
            list(fragments({"payload": "a" * 4096}, 1))

    def test_mtu_credit_sequences_wrap_and_no_fill(self):
        _, _, safety, audio, _ = fixture()
        for rate, mtu in ((8000, 23), (48000, 247), (8000, 246), (8000, 518)):
            with self.assertRaises(ValueError):
                audio.start(rate, mtu)
        start = audio.start(8000, 247)
        self.assertEqual(start["txCredits"], 16)
        packet = HEADER.pack(1, 0, 0, audio.tx_id, 0, 0) + b"\1\0" * 114
        audio.accept(packet)
        self.assertEqual(audio.credits, 15)
        self.assertEqual(audio.consume(), b"\1\0" * 114)
        self.assertEqual(audio.credits, 16)
        self.assertIsNone(audio.consume())
        with self.assertRaisesRegex(ValueError, "gap"):
            audio.accept(packet)
        self.assertFalse(audio.active)
        self.assertEqual(safety.fault, "audio-gap-or-reorder")
        audio.start(8000, 247)
        audio.tx_sequence = audio.tx_sample = 0xFFFFFFFF
        audio.accept(HEADER.pack(1, 0, 0, audio.tx_id, 0xFFFFFFFF, 0xFFFFFFFF) + b"\0\0")
        self.assertEqual((audio.tx_sequence, audio.tx_sample), (0, 0))

    def test_rx_bounded_notify_loss_and_failure(self):
        _, _, safety, audio, _ = fixture()
        audio.start(8000, 247)
        pcm = struct.pack("<" + "h" * 228, *range(228))
        audio.enqueue_rx(pcm)
        sent = []
        while audio.notify(sent.append):
            pass
        self.assertEqual(len(sent), 2)
        self.assertEqual([HEADER.unpack(x[:16])[4:] for x in sent], [(0, 0), (1, 114)])
        self.assertEqual(b"".join(x[16:] for x in sent), pcm)
        self.assertEqual(audio.rx_notifications, 2)
        audio.enqueue_rx(b"\0\0" * (114 * 17))
        self.assertFalse(audio.active)
        self.assertEqual(audio.rx_dropped, 1)
        self.assertFalse(audio.rx)
        audio.start(8000, 247)
        audio.enqueue_rx(b"\1\0")
        with self.assertRaises(RuntimeError):
            audio.notify(lambda _: (_ for _ in ()).throw(RuntimeError("notify")))
        self.assertFalse(audio.active)

    def test_bad_audio_headers_and_credit_overrun(self):
        for field in ("length", "version", "flags", "reserved", "stream", "gap", "sample", "odd"):
            _, _, _, audio, _ = fixture()
            audio.start(8000, 247)
            header = [1, 0, 0, audio.tx_id, 0, 0]
            indexes = {"version": 0, "flags": 1, "reserved": 2, "stream": 3,
                       "gap": 4, "sample": 5}
            if field in indexes:
                header[indexes[field]] += 1
            pcm = b"\0" if field == "odd" else b"\0\0" * (115 if field == "length" else 1)
            with self.assertRaises(ValueError, msg=field):
                audio.accept(HEADER.pack(*header) + pcm)
            self.assertFalse(audio.active)
        audio.start(8000, 247)
        for i in range(16):
            audio.accept(HEADER.pack(1, 0, 0, audio.tx_id, i, i) + b"\0\0")
        with self.assertRaisesRegex(ValueError, "credit"):
            audio.accept(HEADER.pack(1, 0, 0, audio.tx_id, 16, 16) + b"\0\0")


class DispatcherTests(unittest.TestCase):
    def test_audio_requires_explicit_profiles_and_binds_stream_channels(self):
        _, _, safety, audio, dispatch = fixture()
        dispatch.authenticated.add("peer")
        safety.connect("peer")
        request = {"v": 1, "id": "start", "path": "/audio/start",
                   "op": "set", "data": {"rate": 8000, "mtu": 247}}
        self.assertFalse(dispatch.dispatch(request, "peer", True, True, 247)["ok"])
        request["data"].update(rxChannel="UHF", txChannel="VHF")
        reply = dispatch.dispatch(request, "peer", True, True, 247)
        self.assertTrue(reply["ok"])
        self.assertEqual(reply["data"]["rxChannel"], "UHF")
        self.assertEqual(reply["data"]["txChannel"], "VHF")
        self.assertEqual(reply["data"]["txPolicy"], "ONE_TX_ONLY")
        self.assertEqual((safety.rx_hz, safety.tx_hz), (435100000, 145900000))
        self.assertFalse(safety.check())

    def test_auth_mtu_tracking_and_ptt(self):
        clock, _, safety, audio, dispatch = fixture()
        def call(path, data, bonded=True, encrypted=True, op="set"):
            if path == "/audio/start":
                data = dict(data, rxChannel="VHF", txChannel="UHF")
            return dispatch.dispatch({"v": 1, "id": "req", "path": path,
                                      "op": op, "data": data}, "peer", bonded, encrypted, 247)
        self.assertFalse(call("/auth", {"token": "a" * 64}, encrypted=False)["ok"])
        self.assertFalse(call("/auth", {"token": "wrong"})["ok"])
        self.assertTrue(call("/auth", {"token": "a" * 64})["ok"])
        self.assertFalse(call("/audio/start", {"rate": 8000, "mtu": 23})["ok"])
        self.assertTrue(call("/audio/start", {"rate": 8000, "mtu": 247})["ok"])
        self.assertFalse(call("/ptt", {"enabled": True, "leaseMs": 500})["ok"])
        self.assertFalse(call("/tracking", {"rangeRateMps": 0, "utc": 1000,
                                            "site": [42, 2, 20]})["ok"])
        dispatch.tracking_input.provision("peer")  # TEST ONLY authenticated upstream injection.
        self.assertTrue(call("/tracking", {"rangeRateMps": 0, "utc": 1000,
                                           "site": [42, 2, 20]})["ok"])
        safety.physical(True, True)
        safety.sdr_ready = True
        safety.rotor_update(None, True)
        safety.polarization = SimpleNamespace(ready=lambda: True)
        self.assertTrue(call("/ptt", {"enabled": True, "leaseMs": 500})["ok"])
        self.assertTrue(safety.check())
        status = call("/status", {}, op="get")
        self.assertNotIn("token", json.dumps(status))
        self.assertTrue(call("/ptt", {"enabled": False})["ok"])
        self.assertFalse(safety.check())
        dispatch.disconnect("peer")
        self.assertFalse(audio.active)

    def test_cat_original_subset(self):
        _, _, safety, _, _ = fixture()
        cat = Cat(safety)
        self.assertEqual(cat.command("FA"), "FA00145900000;")
        self.assertEqual(cat.command("FB"), "FB00435100000;")
        self.assertEqual(cat.command("FA00145000000"), "")
        self.assertEqual(safety.rx_hz, 145_000_000)
        for code, mode in ((2, "USB"), (4, "FM"), (5, "AM")):
            self.assertEqual(cat.command(f"MD{code}"), "")
            self.assertEqual(cat.command("MD"), f"MD{code};")
            self.assertEqual(safety.mode, mode)
        for invalid in ("MD1", "TX", "FA144000000", "FA00143000000", "FB00145000000", "IF"):
            self.assertEqual(cat.command(invalid), "?;")


class CatSocketTests(unittest.IsolatedAsyncioTestCase):
    async def test_localhost_socket_and_disconnect_stop(self):
        _, stops, safety, _, _ = fixture()
        server = await Cat(safety).listen(0)
        try:
            self.assertEqual(server.sockets[0].getsockname()[0], "127.0.0.1")
            port = server.sockets[0].getsockname()[1]
            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            writer.write(b"FA;MD2;MD;TX;")
            await writer.drain()
            received = await asyncio.wait_for(reader.read(100), 1)
            self.assertEqual(received, b"FA00145900000;MD2;?;")
            writer.close()
            await writer.wait_closed()
            await asyncio.sleep(0.02)
            self.assertTrue(stops)
            self.assertFalse(safety.check())
        finally:
            server.close()
            await server.wait_closed()


if __name__ == "__main__":
    unittest.main()
