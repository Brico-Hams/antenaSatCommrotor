"""Two uniquely selected real Lime Mini chains; at most one active TX."""

import queue
import threading

from .dsp import IQ_RATE
from .resample import RationalResampler
from .soapy import SoapyRadio, load

CHANNELS = ("VHF", "UHF")


class DualLime:
    def __init__(self, vhf_serial: str, uhf_serial: str, hardware_rate=1000000,
                 single_channel=None):
        if single_channel not in (None, "VHF", "UHF"):
            raise ValueError("explicit single radio channel required")
        self.channels = CHANNELS if single_channel is None else (single_channel,)
        selections = {"VHF": vhf_serial, "UHF": uhf_serial}
        if (any(not selections[c] for c in self.channels)
                or (single_channel is None and vhf_serial == uhf_serial)):
            raise ValueError("two explicit unique Lime Mini serials required")
        if type(hardware_rate) is not int or not 192000 <= hardware_rate <= 4000000:
            raise ValueError("hardware rate must be explicit 192k..4M sample/s")
        api, _ = load()
        candidates = [dict(x) for x in api.Device.enumerate()]
        self.selectors = {}
        for channel in self.channels:
            serial = selections[channel]
            matches = [x for x in candidates if x.get("serial") == serial
                       and x.get("driver", "").lower() == "lime"
                       and "mini" in (x.get("label", "") + x.get("name", "")).lower()]
            if len(matches) != 1:
                raise ValueError("serial must identify exactly one advertised LimeSDR Mini")
            self.selectors[channel] = matches[0]
        self.rate = hardware_rate
        self.chains = {}
        self.queues = {c: queue.Queue(maxsize=8) for c in self.channels}
        self.errors = {}
        self.reads = {c: 0 for c in self.channels}
        self.running = False
        self.active_tx = None
        self.lock = threading.RLock()
        self.threads = []
        self.rf_guard = None
        self.down = {c: RationalResampler(hardware_rate, IQ_RATE) for c in self.channels}
        self.up = {c: RationalResampler(IQ_RATE, hardware_rate) for c in self.channels}
        try:
            for channel, hz in (("VHF", 145900000), ("UHF", 435100000)):
                if channel not in self.channels:
                    continue
                selector = self.selectors[channel]
                self.chains[channel] = SoapyRadio(selector, selector, hz, hz,
                                                  hardware_rate, crossband=False)
        except BaseException:
            self.close()
            raise

    def start_receivers(self):
        if self.running or self.threads:
            raise RuntimeError("RX workers already started")
        self.running = True
        for channel in self.channels:
            thread = threading.Thread(target=self._receive, args=(channel,), daemon=True)
            self.threads.append(thread)
            thread.start()

    def _receive(self, channel):
        try:
            while self.running:
                iq = self.chains[channel].receive()
                self.reads[channel] += 1
                converted = self.down[channel].process(iq)
                if converted:
                    self.queues[channel].put_nowait(converted)
        except BaseException as error:
            self.errors[channel] = f"{type(error).__name__}: {error}"
            self.running = False
            self.stop_tx()

    @property
    def ready(self):
        return (self.running and not self.errors and
                all(self.chains[c].ready for c in self.channels))

    def receive(self, channel):
        if self.errors:
            raise RuntimeError(f"dual RX fault: {self.errors}")
        try:
            return self.queues[channel].get(timeout=0.05)
        except queue.Empty:
            raise TimeoutError(f"{channel} RX resource queue timeout")

    def tune(self, vhf_hz, uhf_hz):
        from .safety import band
        if band(vhf_hz) != "VHF" or band(uhf_hz) != "UHF":
            raise ValueError("RF path/profile frequency mismatch")
        self.stop_tx()
        for channel, hz in (("VHF", vhf_hz), ("UHF", uhf_hz)):
            if channel in self.chains:
                self.chains[channel].tune(hz, hz)

    def tune_single(self, rx_hz, tx_hz):
        from .safety import band
        if len(self.channels) != 1 or band(rx_hz) != self.channels[0] or band(tx_hz) != self.channels[0]:
            raise ValueError("single profile frequency mismatch")
        self.stop_tx()
        self.chains[self.channels[0]].tune(rx_hz, tx_hz)

    def transmit(self, channel, iq, permitted):
        with self.lock:
            if channel not in self.channels or not self.ready:
                raise PermissionError("dual Lime not ready")
            if self.active_tx not in (None, channel):
                raise PermissionError("simultaneous dual TX forbidden")
            self.active_tx = channel
            try:
                if self.rf_guard:
                    if self.rf_guard.requested != channel:
                        self.rf_guard.request(channel)
                        import time
                        time.sleep(0.01)
                    if not self.rf_guard.permitted(channel):
                        raise PermissionError("independent hardware RF guard rejected TX")
                converted = self.up[channel].process(iq)
                if converted:
                    def guarded():
                        return permitted() and (self.rf_guard is None or self.rf_guard.permitted(channel))
                    self.chains[channel].transmit(converted, guarded)
            except BaseException:
                self.stop_tx()
                raise

    def stop_tx(self):
        with self.lock:
            first_error = None
            try:
                if self.rf_guard:
                    try:
                        self.rf_guard.off()
                    except Exception as error:
                        first_error = error
                for chain in self.chains.values():
                    try:
                        chain.stop_tx()
                    except Exception as error:
                        first_error = first_error or error
            finally:
                self.active_tx = None
                self.up = {c: RationalResampler(IQ_RATE, self.rate) for c in self.channels}
            if first_error:
                raise first_error

    def status(self):
        return {c: {"serial": self.selectors[c]["serial"], "rxReady": self.chains[c].ready,
                    "rxHzReadback": self.chains[c].rx.getFrequency(self.chains[c].api.SOAPY_SDR_RX, 0),
                    "txHzReadback": self.chains[c].tx.getFrequency(self.chains[c].api.SOAPY_SDR_TX, 0),
                    "rxRateReadback": self.chains[c].rx.getSampleRate(self.chains[c].api.SOAPY_SDR_RX, 0),
                    "txRateReadback": self.chains[c].tx.getSampleRate(self.chains[c].api.SOAPY_SDR_TX, 0),
                    "rxReads": self.reads[c], "queueDepth": self.queues[c].qsize(),
                    "fault": self.errors.get(c), "txActive": self.active_tx == c}
                for c in self.channels}

    def close(self):
        self.running = False
        error = None
        try:
            self.stop_tx()
        except Exception as fault:
            error = fault
        for thread in self.threads:
            thread.join(timeout=0.2)
        for chain in self.chains.values():
            try:
                chain.close()
            except Exception as fault:
                error = error or fault
        if error:
            raise error
