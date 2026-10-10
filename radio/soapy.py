"""Real SoapySDR API adapter. Import/discovery/stream failures never become IQ."""

import json
import math

from .dsp import IQ_RATE
from .safety import band

MAX_DRIVE = 0.1


def load():
    import SoapySDR
    import numpy
    return SoapySDR, numpy


def ranges(values):
    return [{"minimum": x.minimum(), "maximum": x.maximum(), "step": x.step()}
            for x in values]


def supports(values, value):
    for item in values:
        minimum, maximum, step = item.minimum(), item.maximum(), item.step()
        if minimum <= value <= maximum:
            if step <= 0 or math.isclose((value - minimum) / step,
                                        round((value - minimum) / step), abs_tol=1e-6):
                return True
    return False


def discover():
    api, _ = load()
    result = []
    for selector in api.Device.enumerate():
        device = api.Device(selector)
        entry = {"selector": dict(selector), "hardware": dict(device.getHardwareInfo()),
                 "channels": {}}
        for name, direction in (("RX", api.SOAPY_SDR_RX), ("TX", api.SOAPY_SDR_TX)):
            entry["channels"][name] = [{
                "channel": channel,
                "fullDuplexAdvertised": bool(device.getFullDuplex(direction, channel)),
                "frequencies": ranges(device.getFrequencyRange(direction, channel)),
                "sampleRates": ranges(device.getSampleRateRange(direction, channel)),
            } for channel in range(device.getNumChannels(direction))]
        result.append(entry)
    return result


class SoapyRadio:
    def __init__(self, rx_selector: dict, tx_selector: dict, rx_hz: int, tx_hz: int,
                 hardware_rate: int = IQ_RATE, crossband: bool = True):
        self.api, self.np = load()
        self.rx_stream = self.tx_stream = None
        self.tx_active = False
        self.rx_ready = False
        self.closed = False
        self.hardware_rate = hardware_rate
        self.crossband = crossband
        self.rx = self.tx = None
        self.rx_hz = self.tx_hz = None
        available = [dict(x) for x in self.api.Device.enumerate()]
        for selector in (rx_selector, tx_selector):
            if not selector or selector.get("driver") in {"null", "dummy", "test"}:
                raise ValueError("explicit real discovered module selector required")
            if not any(all(candidate.get(k) == v for k, v in selector.items())
                       for candidate in available):
                raise ValueError("requested module not discovered")
        try:
            self.rx = self.api.Device(rx_selector)
            self.tx = self.rx if rx_selector == tx_selector else self.api.Device(tx_selector)
            if self.rx is self.tx and not all(
                self.rx.getFullDuplex(direction, 0)
                for direction in (self.api.SOAPY_SDR_RX, self.api.SOAPY_SDR_TX)
            ):
                raise ValueError("module does not advertise independent full duplex")
            self._configure(self.rx, self.api.SOAPY_SDR_RX, rx_hz)
            self._configure(self.tx, self.api.SOAPY_SDR_TX, tx_hz)
            if crossband and band(rx_hz) == band(tx_hz):
                raise ValueError("crossband required")
            self.rx_hz, self.tx_hz = rx_hz, tx_hz
            self.rx_stream = self.rx.setupStream(self.api.SOAPY_SDR_RX, self.api.SOAPY_SDR_CF32, [0])
            self.tx_stream = self.tx.setupStream(self.api.SOAPY_SDR_TX, self.api.SOAPY_SDR_CF32, [0])
            if self.rx_stream is None or self.tx_stream is None:
                raise RuntimeError("stream setup failed")
            if self.rx.activateStream(self.rx_stream) != 0:
                raise RuntimeError("RX activation failed")
        except Exception:
            self.close()
            raise

    def _configure(self, device, direction, hz):
        band(hz)
        if device.getNumChannels(direction) < 1:
            raise ValueError("required direction unavailable")
        if not supports(device.getFrequencyRange(direction, 0), hz):
            raise ValueError("module does not advertise requested frequency")
        if not supports(device.getSampleRateRange(direction, 0), self.hardware_rate):
            raise ValueError("module does not advertise requested hardware sample/s")
        device.setSampleRate(direction, 0, self.hardware_rate)
        if device.getSampleRate(direction, 0) != self.hardware_rate:
            raise RuntimeError("module did not apply sample rate")
        device.setFrequency(direction, 0, hz)
        if abs(device.getFrequency(direction, 0) - hz) > 1:
            raise RuntimeError("module did not apply integer-Hz tuning")
        if direction == self.api.SOAPY_SDR_TX:
            device.setGainMode(direction, 0, False)
            gain = device.getGainRange(direction, 0).minimum()
            device.setGain(direction, 0, gain)

    def tune(self, rx_hz, tx_hz):
        if self.tx_active:
            self.stop_tx()
            raise PermissionError("retune while TX forbidden")
        if self.crossband and band(rx_hz) == band(tx_hz):
            raise ValueError("crossband required")
        for device, direction, hz, old in (
            (self.rx, self.api.SOAPY_SDR_RX, rx_hz, self.rx_hz),
            (self.tx, self.api.SOAPY_SDR_TX, tx_hz, self.tx_hz)
        ):
            if hz != old:
                if not supports(device.getFrequencyRange(direction, 0), hz):
                    raise ValueError("Doppler tuning outside module advertised range")
                device.setFrequency(direction, 0, hz)
                if abs(device.getFrequency(direction, 0) - hz) > 1:
                    raise RuntimeError("tune readback failed")
        self.rx_hz, self.tx_hz = rx_hz, tx_hz

    @property
    def ready(self):
        return self.rx_ready and self.tx_stream is not None and not self.closed

    def receive(self):
        buffer = self.np.empty(self.hardware_rate // 100, dtype=self.np.complex64)
        result = self.rx.readStream(self.rx_stream, [buffer], len(buffer), timeoutUs=10000)
        if result.ret == self.api.SOAPY_SDR_TIMEOUT:
            self.rx_ready = False
            raise TimeoutError("SDR RX timeout")
        if result.ret <= 0:
            self.rx_ready = False
            raise RuntimeError(f"SDR RX fault {result.ret}")
        self.rx_ready = True
        return buffer[:result.ret].tolist()

    def transmit(self, iq, permitted):
        try:
            self._transmit(iq, permitted)
        except BaseException:
            self.stop_tx()
            raise

    def _transmit(self, iq, permitted):
        if not self.ready or not permitted():
            raise PermissionError("actual SDR not ready")
        buffer = self.np.asarray(iq, dtype=self.np.complex64)
        if not len(buffer) or not self.np.all(self.np.isfinite(buffer)):
            raise ValueError("invalid TX IQ")
        peak = float(self.np.max(self.np.abs(buffer)))
        buffer *= MAX_DRIVE / max(1.0, peak)
        if not self.tx_active:
            # Treat ambiguous activation failures as possibly active and deactivate.
            self.tx_active = True
            try:
                if self.tx.activateStream(self.tx_stream) != 0:
                    raise RuntimeError("TX activation failed")
            except BaseException:
                self.stop_tx()
                raise
        if not permitted():
            self.stop_tx()
            raise PermissionError("TX lease revoked before write")
        result = self.tx.writeStream(self.tx_stream, [buffer], len(buffer), timeoutUs=10000)
        if result.ret != len(buffer) or not permitted():
            self.stop_tx()
            raise RuntimeError(f"TX short write/timeout/fault: {result.ret}/{len(buffer)}")

    def stop_tx(self):
        if self.tx_active and self.tx_stream is not None:
            self.tx_active = False
            result = self.tx.deactivateStream(self.tx_stream)
            if result != 0:
                self.closed = True
                try:
                    self.tx.closeStream(self.tx_stream)
                finally:
                    self.tx_stream = None
                raise RuntimeError("TX deactivation failed; external RF gate REQUIRED")

    def close(self):
        self.closed = True
        try:
            self.stop_tx()
        finally:
            for device, stream in ((self.rx, self.rx_stream), (self.tx, self.tx_stream)):
                if device is not None and stream is not None:
                    try:
                        device.deactivateStream(stream)
                    finally:
                        device.closeStream(stream)
            self.rx_stream = self.tx_stream = None


def selector(text: str):
    value = json.loads(text)
    if not isinstance(value, dict) or not all(isinstance(k, str) and isinstance(v, str)
                                             for k, v in value.items()):
        raise ValueError("selector must be JSON string-to-string object")
    return value
