"""Explicit test-only local I/O; no physical RF or GPIO is exercised."""

import asyncio
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from radio.main import Physical, radio_loop, dual_radio_loop
from radio.protocol import Audio, HEADER
from radio.safety import Safety


class RuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_dual_runtime_consumes_both_rx_and_labels_selected_audio(self):
        safety = Safety(lambda: None, lambda: 100, lambda: 1000)
        safety.connect("test")
        safety.physical(True, True)
        safety.sdr_ready = True
        safety.tracking_update(0, 1000, [42, 2, 20], True)
        safety.rotor_update(None, True)
        safety.polarization = SimpleNamespace(ready=lambda: True)
        safety.rx_channel, safety.tx_channel = "UHF", "VHF"
        safety.rx_hz, safety.tx_hz = 435100000, 145900000
        audio = Audio(safety.inhibit)
        audio.start(8000, 247)
        audio.accept(HEADER.pack(1, 0, 0, audio.tx_id, 0, 0) + b"\0\0" * 80)
        safety.lease("test", 500)
        received, transmitted = [], []
        def receive(channel):
            received.append(channel)
            if len(received) > 2:
                raise RuntimeError("TEST ONLY end")
            return [complex(0.1 if channel == "VHF" else 0.2)] * 80
        def transmit(channel, iq, permitted):
            self.assertTrue(permitted())
            transmitted.append(channel)
        backend = SimpleNamespace(
            ready=True, receive=receive, transmit=transmit,
            chains={"VHF": SimpleNamespace(rx_hz=145900000),
                    "UHF": SimpleNamespace(rx_hz=435100000)})
        with patch("radio.main.Demodulator", side_effect=lambda mode: SimpleNamespace(
                process=lambda iq: [value.real for value in iq])):
            with self.assertRaisesRegex(RuntimeError, "TEST ONLY"):
                await dual_radio_loop(backend, safety, audio,
                                      SimpleNamespace(credit=lambda: None))
        self.assertEqual(received[:2], ["VHF", "UHF"])
        self.assertEqual(transmitted, ["VHF"])
        self.assertTrue(audio.rx)
        self.assertEqual(HEADER.unpack(audio.rx[0][:16])[3], audio.rx_id)
        import struct
        first_sample = struct.unpack("<h", audio.rx[0][16:18])[0]
        self.assertEqual(first_sample, round(0.2 * 32767))
        self.assertFalse(safety.transmitting)

    async def test_pcm_starvation_pauses_tx_without_silent_fill(self):
        clock = [100.0]
        writes, stops = [], []
        safety = Safety(lambda: stops.append("stop"), lambda: clock[0], lambda: 1000)
        safety.connect("test-session")
        safety.physical(True, True)
        safety.sdr_ready = True
        safety.tracking_update(0, 1000, [42, 2, 20], True)
        safety.rotor_update(None, True)
        safety.polarization = SimpleNamespace(ready=lambda: True)
        audio = Audio(safety.inhibit)
        audio.start(8000, 247)
        audio.accept(HEADER.pack(1, 0, 0, audio.tx_id, 0, 0) + b"\0\0" * 80)
        safety.lease("test-session", 500)

        class TestOnlySDR:
            ready = True
            rx_hz, tx_hz = 145900000, 435100000
            count = 0

            def receive(self):
                self.count += 1
                clock[0] += 0.025
                if self.count > 6:
                    raise RuntimeError("TEST ONLY stop condition")
                return [1 + 0j] * 960

            def transmit(self, iq, permitted):
                if not permitted():
                    raise AssertionError("transmission without lease")
                writes.append(len(iq))

        credits = []
        ble = SimpleNamespace(credit=lambda: credits.append(audio.credits))
        with self.assertLogs("radio", level="ERROR"):
            with self.assertRaisesRegex(RuntimeError, "TEST ONLY"):
                await radio_loop(TestOnlySDR(), safety, audio, ble, clock=lambda: clock[0])
        self.assertEqual(writes, [960])
        self.assertFalse(audio.active)
        self.assertFalse(safety.transmitting)
        self.assertFalse(safety.sdr_ready)
        self.assertTrue(stops)
        self.assertIn(0, credits)

    def test_physical_release_drops_gate_before_driver_stop(self):
        order = []
        safety = Safety(lambda: order.append("driver-stop"))
        physical = Physical.__new__(Physical)
        physical.arm, physical.ptt, physical.gate = 1, 2, 3
        physical.safety = safety
        physical.Value = SimpleNamespace(ACTIVE=1, INACTIVE=0)
        physical.lines = SimpleNamespace(
            get_value=lambda line: 0,
            set_value=lambda line, value: order.append(("gate", value))
        )
        physical.running = True
        def tick(_):
            physical.running = False
        with patch("radio.main.time.sleep", side_effect=tick):
            physical.monitor()
        self.assertEqual(order[0], ("gate", 0))
        self.assertIn("driver-stop", order)
        self.assertFalse(safety.physical_arm)
        self.assertFalse(safety.physical_ptt)
        self.assertTrue(all(x[1] == 0 for x in order if isinstance(x, tuple)))


if __name__ == "__main__":
    unittest.main()
