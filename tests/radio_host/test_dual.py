"""Explicit dual-device test fixtures; never a runtime RF backend."""

import queue
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from radio.dual import DualLime
from radio.resample import RationalResampler
from radio.dsp import Modulator, Demodulator


class DualTests(unittest.TestCase):
    def setUp(self):
        self.devices = [
            {"driver": "lime", "serial": "TEST-VHF", "label": "LimeSDR Mini test-only"},
            {"driver": "lime", "serial": "TEST-UHF", "label": "LimeSDR Mini test-only"}]
        self.api = SimpleNamespace(Device=SimpleNamespace(enumerate=lambda: self.devices))
        self.records = []
        records = self.records

        class TestOnlyChain:
            def __init__(self, rx_selector, tx_selector, rx_hz, tx_hz, rate, crossband):
                self.rx_hz, self.tx_hz = rx_hz, tx_hz
                self.ready = True
                self.tx_active = False
                self.writes = []
                self.reads = 0
                self.rate = rate
                self.api = SimpleNamespace(SOAPY_SDR_RX=0, SOAPY_SDR_TX=1)
                self.rx = self.tx = SimpleNamespace(
                    getFrequency=lambda direction, channel: self.rx_hz if direction == 0 else self.tx_hz,
                    getSampleRate=lambda direction, channel: self.rate)
                records.append((rx_selector["serial"], rate, crossband, self))

            def receive(self):
                self.reads += 1
                return [1j] * 10000

            def transmit(self, iq, permitted):
                if not permitted():
                    raise PermissionError("lease")
                self.tx_active = True
                self.writes.append(iq)

            def stop_tx(self):
                self.tx_active = False

            def tune(self, rx, tx):
                self.rx_hz, self.tx_hz = rx, tx

            def close(self):
                self.ready = False

        self.load = patch("radio.dual.load", return_value=(self.api, np))
        self.chain = patch("radio.dual.SoapyRadio", TestOnlyChain)
        self.load.start()
        self.chain.start()
        self.addCleanup(self.load.stop)
        self.addCleanup(self.chain.stop)

    def create(self):
        result = DualLime("TEST-VHF", "TEST-UHF")
        self.addCleanup(result.close)
        return result

    def test_unique_explicit_serials_no_first_device_auto(self):
        for args in (("", "TEST-UHF"), ("TEST-VHF", "TEST-VHF"), ("missing", "TEST-UHF")):
            with self.assertRaises(ValueError):
                DualLime(*args)
        self.devices.append(dict(self.devices[0]))
        with self.assertRaises(ValueError):
            self.create()
        self.devices.pop()
        self.devices[0]["label"] = "Other Lime device"
        with self.assertRaises(ValueError):
            self.create()

    def test_explicit_single_radio_not_missing_dual_fallback(self):
        single = DualLime("TEST-VHF", None, single_channel="VHF")
        self.addCleanup(single.close)
        self.assertEqual(tuple(single.chains), ("VHF",))
        single.running = True
        single.tune_single(145800000, 145900000)
        single.transmit("VHF", [0.1j] * 960, lambda: True)
        with self.assertRaises(PermissionError):
            single.transmit("UHF", [0.1j] * 960, lambda: True)
        with self.assertRaises(ValueError):
            DualLime("TEST-VHF", None)

    def test_both_chains_tx_capable_only_one_tx_owner(self):
        dual = self.create()
        dual.running = True
        self.assertEqual([(x[0], x[1], x[2]) for x in self.records],
                         [("TEST-VHF", 1000000, False), ("TEST-UHF", 1000000, False)])
        dual.transmit("VHF", [0.1j] * 960, lambda: True)
        with self.assertRaises(PermissionError):
            dual.transmit("UHF", [0.1j] * 960, lambda: True)
        self.assertTrue(dual.chains["VHF"].tx_active)
        self.assertFalse(dual.chains["UHF"].tx_active)
        dual.stop_tx()
        dual.transmit("UHF", [0.1j] * 960, lambda: True)
        self.assertTrue(dual.chains["UHF"].tx_active)
        self.assertFalse(dual.chains["VHF"].tx_active)
        status = dual.status()
        self.assertEqual(set(status), {"VHF", "UHF"})
        self.assertEqual(status["UHF"]["rxRateReadback"], 1000000)
        dual.tune(145800000, 435200000)
        self.assertIsNone(dual.active_tx)

    def test_hardware_guard_denial_no_sdr_tx_and_requests_off(self):
        dual = self.create()
        dual.running = True
        requests = []
        guard = SimpleNamespace(
            requested=None, request=lambda channel: requests.append(channel),
            permitted=lambda channel: False, off=lambda: requests.append("OFF"))
        dual.rf_guard = guard
        with self.assertRaises(PermissionError):
            dual.transmit("VHF", [0.1j] * 960, lambda: True)
        self.assertFalse(dual.chains["VHF"].tx_active)
        self.assertFalse(dual.chains["UHF"].tx_active)
        self.assertEqual(requests[:2], ["VHF", "OFF"])

    def test_rx_workers_bounded_fault_without_silence(self):
        dual = self.create()
        dual.start_receivers()
        for thread in dual.threads:
            thread.join(timeout=2)
        self.assertTrue(dual.errors)
        self.assertLessEqual(max(q.qsize() for q in dual.queues.values()), 8)
        with self.assertRaises(RuntimeError):
            dual.receive("VHF")
        self.assertFalse(dual.ready)

    def test_two_rx_workers_really_enter_receive_concurrently(self):
        dual = self.create()
        barrier = threading.Barrier(2, timeout=1)
        entered = []
        for channel in ("VHF", "UHF"):
            chain = dual.chains[channel]
            original = chain.receive
            def receive(channel=channel, original=original):
                if channel not in entered:
                    entered.append(channel)
                    barrier.wait()
                return original()
            chain.receive = receive
        dual.start_receivers()
        for thread in dual.threads:
            thread.join(timeout=2)
        self.assertEqual(set(entered), {"VHF", "UHF"})
        self.assertTrue(all(dual.reads[channel] > 0 for channel in ("VHF", "UHF")))


class ResamplingTests(unittest.TestCase):
    def test_rational_streaming_block_invariance_and_tone(self):
        values = np.exp(2j * np.pi * 1000 * np.arange(96000) / 96000)
        whole = RationalResampler(96000, 1000000).process(values)
        converter = RationalResampler(96000, 1000000)
        split = []
        for offset in range(0, len(values), 731):
            split.extend(converter.process(values[offset:offset + 731]))
        np.testing.assert_allclose(split, whole, atol=1e-12)
        recovered = np.asarray(RationalResampler(1000000, 96000).process(whole))[2000:]
        rms = float(np.sqrt(np.mean(abs(recovered) ** 2)))
        frequency = float(np.mean(np.angle(recovered[1:] * recovered[:-1].conjugate()))
                          * 96000 / (2 * np.pi))
        print(f"96k<->1M rational tone: {frequency:.6f}Hz amplitude={rms:.6f}")
        self.assertAlmostEqual(frequency, 1000, delta=0.1)
        self.assertAlmostEqual(rms, 1, delta=0.02)
        self.assertLess(abs(len(whole) - 1000000), 12)

    def test_hardware_iq_pcm_fm_am_usb_roundtrip(self):
        pcm = 0.4 * np.sin(2 * np.pi * 700 * np.arange(8000) / 8000)
        for mode in ("FM", "AM", "USB"):
            iq = Modulator(mode).process(pcm.tolist())
            hardware = RationalResampler(96000, 1000000).process(iq)
            baseband = RationalResampler(1000000, 96000).process(hardware)
            recovered = np.asarray(Demodulator(mode).process(baseband))[1000:]
            frequency = float(np.argmax(abs(np.fft.rfft(recovered))) * 8000 / len(recovered))
            gain = float(np.sqrt(np.mean(recovered ** 2)) / (0.4 / np.sqrt(2)))
            print(f"{mode} hardware1M roundtrip: frequency={frequency:.3f}Hz gain={gain:.6f}")
            self.assertAlmostEqual(frequency, 700, delta=2)
            self.assertTrue(0.94 < gain < 1.06)

    def test_alias_rejection_and_invalid_rates(self):
        t = np.arange(100000) / 1000000
        high = np.exp(2j * np.pi * 100000 * t)
        down = np.asarray(RationalResampler(1000000, 96000).process(high))[1000:]
        rejection = -20 * np.log10(np.sqrt(np.mean(abs(down) ** 2)))
        print(f"1M->96k 100kHz alias suppression: {rejection:.2f}dB")
        self.assertGreater(rejection, 40)
        for rates in ((0, 96000), (96000, 1000000.0)):
            with self.assertRaises(ValueError):
                RationalResampler(*rates)
