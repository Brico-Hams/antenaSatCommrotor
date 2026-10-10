"""TEST ONLY Soapy API fixture; never selectable from the hardware runtime."""

from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from radio.soapy import MAX_DRIVE, SoapyRadio, discover, supports


class Range:
    def __init__(self, minimum, maximum=None, step=0):
        self.low = minimum
        self.high = minimum if maximum is None else maximum
        self.increment = step

    def minimum(self):
        return self.low

    def maximum(self):
        return self.high

    def step(self):
        return self.increment


class TestOnlyDevice:
    frequency_ranges = [Range(144e6, 146e6), Range(430e6, 440e6)]
    sample_ranges = [Range(96000)]
    advertised = [{"driver": "unit-test-fixture", "serial": "TEST-ONLY"}]
    duplex = True
    last = None
    read_result = 960
    write_result = None
    activation_result = 0
    stop_result = 0

    @staticmethod
    def enumerate():
        return TestOnlyDevice.advertised

    def __init__(self, selector):
        self.rates = {}
        self.frequencies = {}
        self.activations = []
        self.stops = []
        self.closes = []
        self.tx = None
        TestOnlyDevice.last = self

    def getHardwareInfo(self):
        return {"TEST_ONLY": "not RF hardware"}

    def getFullDuplex(self, direction, channel):
        return self.duplex

    def getNumChannels(self, direction):
        return 1

    def getFrequencyRange(self, direction, channel):
        return self.frequency_ranges

    def getSampleRateRange(self, direction, channel):
        return self.sample_ranges

    def setSampleRate(self, direction, channel, value):
        self.rates[direction] = value

    def getSampleRate(self, direction, channel):
        return self.rates[direction]

    def setFrequency(self, direction, channel, value):
        self.frequencies[direction] = value

    def getFrequency(self, direction, channel):
        return self.frequencies[direction]

    def setGainMode(self, direction, channel, mode):
        self.assert_gain_mode = mode

    def getGainRange(self, direction, channel):
        return Range(-20, 30)

    def setGain(self, direction, channel, gain):
        self.gain = gain

    def setupStream(self, direction, format, channels):
        return f"stream-{direction}"

    def activateStream(self, stream):
        self.activations.append(stream)
        return self.activation_result if stream == "stream-1" else 0

    def deactivateStream(self, stream):
        self.stops.append(stream)
        return self.stop_result

    def closeStream(self, stream):
        self.closes.append(stream)

    def readStream(self, stream, buffers, size, timeoutUs):
        buffers[0][:] = 1 + 0j
        return SimpleNamespace(ret=self.read_result)

    def writeStream(self, stream, buffers, size, timeoutUs):
        self.tx = buffers[0].copy()
        return SimpleNamespace(ret=size if self.write_result is None else self.write_result)


API = SimpleNamespace(Device=TestOnlyDevice, SOAPY_SDR_RX=0, SOAPY_SDR_TX=1,
                      SOAPY_SDR_CF32="CF32", SOAPY_SDR_TIMEOUT=-1)


class SoapyTests(unittest.TestCase):
    def setUp(self):
        TestOnlyDevice.frequency_ranges = [Range(144e6, 146e6), Range(430e6, 440e6)]
        TestOnlyDevice.sample_ranges = [Range(96000)]
        TestOnlyDevice.advertised = [{"driver": "unit-test-fixture", "serial": "TEST-ONLY"}]
        TestOnlyDevice.duplex = True
        TestOnlyDevice.read_result = 960
        TestOnlyDevice.write_result = None
        TestOnlyDevice.activation_result = 0
        TestOnlyDevice.stop_result = 0
        self.patch = patch("radio.soapy.load", return_value=(API, np))
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def create(self):
        selector = dict(TestOnlyDevice.advertised[0])
        return SoapyRadio(selector, selector, 145900000, 435100000)

    def test_real_adapter_api_discovery_no_tx_activation(self):
        entries = discover()
        self.assertEqual(entries[0]["channels"]["TX"][0]["sampleRates"][0]["minimum"], 96000)
        self.assertFalse(TestOnlyDevice.last.activations)
        radio = self.create()
        self.assertEqual(TestOnlyDevice.last.activations, ["stream-0"])
        self.assertFalse(radio.ready)
        with self.assertRaises(PermissionError):
            radio.transmit([1 + 0j], lambda: True)
        radio.receive()
        self.assertTrue(radio.ready)
        radio.transmit([2 + 2j, 0.5 + 0j], lambda: True)
        self.assertLessEqual(float(np.max(abs(TestOnlyDevice.last.tx))), MAX_DRIVE + 1e-8)
        self.assertEqual(TestOnlyDevice.last.gain, -20)
        radio.stop_tx()
        self.assertFalse(radio.tx_active)
        radio.close()
        self.assertFalse(radio.ready)

    def test_no_discovery_or_unsupported_ranges_failclosed(self):
        TestOnlyDevice.advertised = []
        self.assertEqual(discover(), [])
        with self.assertRaises(ValueError):
            SoapyRadio({"driver": "not-present"}, {"driver": "not-present"}, 145900000, 435100000)
        TestOnlyDevice.advertised = [{"driver": "unit-test-fixture"}]
        for ranges, field in (([Range(2e9, 2.1e9)], "frequency_ranges"),
                              ([Range(48000)], "sample_ranges")):
            old = getattr(TestOnlyDevice, field)
            setattr(TestOnlyDevice, field, ranges)
            with self.assertRaises(ValueError):
                self.create()
            setattr(TestOnlyDevice, field, old)
        TestOnlyDevice.duplex = False
        with self.assertRaises(ValueError):
            self.create()
        for fake in ("null", "dummy", "test"):
            with self.assertRaises(ValueError):
                SoapyRadio({"driver": fake}, {"driver": fake}, 145900000, 435100000)
        self.assertFalse(supports([Range(90000, 100000, 5000)], 96000))

    def test_start_stop_timeout_and_partial_write_faults(self):
        radio = self.create()
        TestOnlyDevice.read_result = -1
        with self.assertRaises(TimeoutError):
            radio.receive()
        self.assertFalse(radio.ready)
        TestOnlyDevice.read_result = 960
        radio.receive()
        TestOnlyDevice.activation_result = -2
        with self.assertRaises(RuntimeError):
            radio.transmit([1j], lambda: True)
        self.assertFalse(radio.tx_active)
        self.assertIn("stream-1", TestOnlyDevice.last.stops)
        TestOnlyDevice.activation_result = 0
        TestOnlyDevice.write_result = 0
        with self.assertRaises(RuntimeError):
            radio.transmit([1j], lambda: True)
        self.assertFalse(radio.tx_active)
        TestOnlyDevice.write_result = None
        radio.transmit([1j], lambda: True)
        with self.assertRaises(PermissionError):
            radio.tune(145900100, 435100100)
        self.assertFalse(radio.tx_active)
        radio.transmit([1j], lambda: True)
        TestOnlyDevice.stop_result = -2
        with self.assertRaises(RuntimeError):
            radio.stop_tx()
        self.assertFalse(radio.ready)
        self.assertIsNone(radio.tx_stream)

    def test_missing_bindings_are_errors_not_test_fallback(self):
        self.patch.stop()
        with patch.dict("sys.modules", {"SoapySDR": None}):
            with self.assertRaises(ModuleNotFoundError):
                discover()

    def test_lease_revoked_during_activation_and_after_write(self):
        radio = self.create()
        radio.receive()
        answers = iter((True, False))
        with self.assertRaises(PermissionError):
            radio.transmit([1j], lambda: next(answers))
        self.assertFalse(radio.tx_active)
        self.assertIsNone(TestOnlyDevice.last.tx)
        answers = iter((True, True, False))
        with self.assertRaises(RuntimeError):
            radio.transmit([1j], lambda: next(answers))
        self.assertFalse(radio.tx_active)

    def test_hardware_one_megasample_exact_readback_and_range(self):
        TestOnlyDevice.sample_ranges = [Range(1000000)]
        selection = dict(TestOnlyDevice.advertised[0])
        radio = SoapyRadio(selection, selection, 145900000, 145900000,
                           hardware_rate=1000000, crossband=False)
        self.assertEqual(TestOnlyDevice.last.rates, {0: 1000000, 1: 1000000})
        radio.close()
        TestOnlyDevice.sample_ranges = [Range(2000000)]
        with self.assertRaises(ValueError):
            SoapyRadio(selection, selection, 145900000, 145900000,
                       hardware_rate=1000000, crossband=False)


if __name__ == "__main__":
    unittest.main()
