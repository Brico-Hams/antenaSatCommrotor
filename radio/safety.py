"""Single-owner safety state; hardware callbacks never accept remote arm flags."""

import math
import time
from dataclasses import dataclass

from .dsp import doppler


def band(hz: int) -> str:
    if type(hz) is not int:
        raise ValueError("frequency must be integer Hz")
    if 144_000_000 <= hz <= 146_000_000:
        return "VHF"
    if 430_000_000 <= hz <= 440_000_000:
        return "UHF"
    raise ValueError("outside initial authorized radio band")


@dataclass(frozen=True)
class Tracking:
    rate_mps: float
    utc: float
    site: tuple[float, float, float]
    received: float


class Safety:
    def __init__(self, stop_tx, clock=time.monotonic, utc_clock=time.time):
        self.stop_tx = stop_tx
        self.clock, self.utc_clock = clock, utc_clock
        self.rx_hz, self.tx_hz = 145_900_000, 435_100_000
        self.mode = "FM"
        self.physical_arm = False
        self.physical_ptt = False
        self.sdr_ready = False
        self.session = None
        self.lease_until = 0.0
        self.tracking = None
        self.transmitting = False
        self.fault = None
        self.tuning = False
        self.polarization = None
        self.rotor_fault = "rotor-status-unavailable"
        self.rotor_received = None
        self.profile_status = lambda: {}
        self.rx_channel = "VHF"
        self.tx_channel = "UHF"
        self.operation_profile = "INTEGRATED_TRACKING"
        self.allowed_profile = "INTEGRATED_TRACKING"
        self.profile_session = None
        self.available_channels = ("VHF", "UHF")

    def select_profile(self, profile: str, session: str, confirmed: bool):
        self.inhibit("explicit-operation-profile-selection")
        if (profile not in {"STANDALONE_MANUAL", "INTEGRATED_TRACKING"}
                or profile != self.allowed_profile or confirmed is not True
                or session != self.session or not session):
            raise PermissionError("locally configured profile and authenticated confirmation required")
        self.operation_profile = profile
        self.profile_session = session

    def rotor_update(self, fault: str | None, verified: bool):
        if verified is not True or (fault is not None and not isinstance(fault, str)):
            self.rotor_fault = "rotor-status-untrusted"
            self.rotor_received = None
            self.inhibit("rotor-status-untrusted")
            raise PermissionError("verified local motion safety source required")
        self.rotor_fault = fault
        self.rotor_received = self.clock()
        if fault is not None:
            self.inhibit("rotor-fault")

    def rotor_ready(self):
        return (self.rotor_fault is None and self.rotor_received is not None
                and 0 <= self.clock() - self.rotor_received <= 0.5)

    def inhibit(self, reason: str):
        self.transmitting = False
        self.lease_until = 0
        self.fault = reason
        self.stop_tx()

    def physical(self, arm: bool, ptt: bool):
        self.physical_arm, self.physical_ptt = bool(arm), bool(ptt)
        if not arm or not ptt:
            self.inhibit("physical-release")

    def connect(self, session: str):
        self.inhibit("session-change")
        self.session = session
        self.profile_session = None

    def disconnect(self, session: str):
        if self.session == session:
            self.session = None
            self.profile_session = None
            self.inhibit("disconnect")

    def tracking_update(self, rate: float, utc: float, site, verified: bool):
        if not verified:
            raise ValueError("verified tracking source required")
        if not math.isfinite(utc) or abs(self.utc_clock() - utc) > 2:
            raise ValueError("UTC state stale")
        if len(site) != 3 or not all(math.isfinite(x) for x in site):
            raise ValueError("invalid site")
        if not (-90 <= site[0] <= 90 and -180 <= site[1] <= 180 and -500 <= site[2] <= 10000):
            raise ValueError("invalid site")
        doppler(self.rx_hz, self.tx_hz, rate)
        self.tracking = Tracking(rate, utc, tuple(site), self.clock())

    def tracking_fresh(self) -> bool:
        return bool(self.tracking and self.clock() - self.tracking.received <= 1
                    and abs(self.utc_clock() - self.tracking.utc) <= 2)

    def frequencies(self) -> tuple[int, int]:
        if self.operation_profile == "INTEGRATED_TRACKING" and self.tracking_fresh():
            return doppler(self.rx_hz, self.tx_hz, self.tracking.rate_mps)
        return self.rx_hz, self.tx_hz

    def tune(self, rx=None, tx=None, mode=None):
        # Never retune over the air; a fresh lease is required after tuning.
        self.inhibit("tuning")
        new_rx = self.rx_hz if rx is None else rx
        new_tx = self.tx_hz if tx is None else tx
        if band(new_rx) == band(new_tx) and len(self.available_channels) != 1:
            raise ValueError("initial configuration requires crossband RX/TX")
        if band(new_rx) != self.rx_channel or band(new_tx) != self.tx_channel:
            raise ValueError("frequency must match explicitly selected VHF/UHF profiles")
        if mode is not None and mode not in {"USB", "FM", "AM"}:
            raise ValueError("unsupported mode")
        self.rx_hz, self.tx_hz = new_rx, new_tx
        if mode:
            self.mode = mode

    def permitted(self, session: str) -> bool:
        rx, tx = self.frequencies()
        try:
            crossband = (band(rx) != band(tx) or
                         (len(self.available_channels) == 1 and band(rx) == band(tx)))
        except ValueError:
            crossband = False
        tracking_ok = (self.operation_profile == "STANDALONE_MANUAL" or
                       (self.tracking_fresh() and self.rotor_ready()))
        profile_ok = (self.operation_profile == "INTEGRATED_TRACKING" or
                      self.profile_session == session)
        return bool(session == self.session and self.session and self.physical_arm
                    and self.physical_ptt and self.sdr_ready and not self.tuning
                    and tracking_ok and profile_ok and crossband
                    and self.polarization is not None and self.polarization.ready())

    def lease(self, session: str, milliseconds: int):
        if type(milliseconds) is not int or not 1 <= milliseconds <= 500:
            raise ValueError("lease must be 1..500 ms")
        if not self.permitted(session):
            self.inhibit("TX-interlock")
            raise PermissionError("TX interlock not satisfied")
        self.lease_until = self.clock() + milliseconds / 1000
        self.fault = None

    def check(self) -> bool:
        if not self.permitted(self.session) or self.clock() >= self.lease_until:
            if self.transmitting or self.lease_until:
                self.inhibit("lease-or-tracking-expired")
            return False
        return True
