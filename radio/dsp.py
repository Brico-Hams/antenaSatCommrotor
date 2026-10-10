"""Streaming 96 ksample/s complex RF <-> 8 ksample/s mono audio DSP.

No oscillators substitute for received audio. FIR states persist across blocks.
"""

import math
from collections import deque

import numpy as np

AUDIO_RATE = 8000
IQ_RATE = 96000
RATIO = IQ_RATE // AUDIO_RATE
C = 299_792_458
MODES = {"USB", "FM", "AM"}
USB_TAPS = 513


def doppler(rx_hz: int, tx_hz: int, range_rate_mps: float) -> tuple[int, int]:
    """Positive range rate is receding; integer Hz, first-order one-way shift."""
    if type(rx_hz) is not int or type(tx_hz) is not int:
        raise ValueError("nominal frequency must be integer Hz")
    if not math.isfinite(range_rate_mps) or abs(range_rate_mps) > 12000:
        raise ValueError("invalid satellite range rate")
    return rx_hz - round(rx_hz * range_rate_mps / C), tx_hz + round(
        tx_hz * range_rate_mps / C
    )


def lowpass(cutoff: float, rate: int, taps: int = 129) -> list[float]:
    if taps % 2 != 1 or not 0 < cutoff < rate / 2:
        raise ValueError("invalid FIR")
    mid = taps // 2
    result = []
    for n in range(taps):
        x = n - mid
        sinc = 2 * cutoff / rate if x == 0 else math.sin(
            2 * math.pi * cutoff / rate * x
        ) / (math.pi * x)
        result.append(sinc * (0.54 - 0.46 * math.cos(2 * math.pi * n / (taps - 1))))
    total = sum(result)
    return [h / total for h in result]


def hilbert(taps=USB_TAPS):
    mid = taps // 2
    return [(2 / (math.pi * (n - mid)) if (n - mid) % 2 else 0.0)
            * (0.54 - 0.46 * math.cos(2 * math.pi * n / (taps - 1)))
            for n in range(taps)]


class FIR:
    def __init__(self, coefficients: list[float]):
        self.h = coefficients
        self.history = deque([0j] * len(coefficients), maxlen=len(coefficients))
        self.block_history = np.zeros(len(coefficients) - 1, dtype=complex)

    def sample(self, value: complex) -> complex:
        self.history.appendleft(value)
        return sum(h * x for h, x in zip(self.h, self.history))

    def process(self, values):
        values = np.asarray(values, dtype=complex)
        if not len(values):
            return values
        combined = np.concatenate((self.block_history, values))
        output = np.convolve(combined, self.h, mode="valid")
        self.block_history = combined[-len(self.block_history):].copy()
        return output


class Modulator:
    def __init__(self, mode: str):
        if mode not in MODES:
            raise ValueError("unsupported mode")
        self.mode = mode
        self.phase = 0.0
        self.interpolate = FIR([x * RATIO for x in lowpass(3000, IQ_RATE)])
        taps = USB_TAPS
        mid = taps // 2
        self.hilbert = FIR(hilbert(taps))
        self.delay = deque([0.0] * (mid + 1), maxlen=mid + 1)

    def process(self, pcm: list[float]) -> list[complex]:
        values = np.asarray(pcm, dtype=float)
        if not np.all(np.isfinite(values)) or np.any(np.abs(values) > 1):
            raise ValueError("PCM must be finite normalized [-1,1]")
        if not len(values):
            return []
        upsampled = np.zeros(len(values) * RATIO)
        upsampled[::RATIO] = values
        audio = np.clip(self.interpolate.process(upsampled).real, -1, 1)
        if self.mode == "FM":
            phases = self.phase + np.cumsum(2 * math.pi * 2500 * audio / IQ_RATE)
            self.phase = float(phases[-1] % (2 * math.pi))
            output = np.exp(1j * phases)
        elif self.mode == "AM":
            output = 0.5 * (1 + 0.8 * audio) + 0j
        else:
            mid = len(self.hilbert.h) // 2
            delayed = np.concatenate((np.asarray(list(self.delay)[:-1]), audio))
            # Store exactly the preceding mid samples (plus unused final slot).
            previous = delayed[-mid:].tolist()
            self.delay = deque(previous + [0.0], maxlen=mid + 1)
            output = delayed[:len(audio)] + 1j * self.hilbert.process(audio).real
        return output.tolist()


class Demodulator:
    def __init__(self, mode: str):
        if mode not in MODES:
            raise ValueError("unsupported mode")
        self.mode = mode
        self.previous = 1 + 0j
        self.filter = FIR(lowpass(3000, IQ_RATE))
        self.usb_hilbert = FIR(hilbert())
        self.usb_history = np.zeros(USB_TAPS // 2, dtype=complex)
        self.index = 0
        self.carrier = 0.5
        self.last_x = 0.0
        self.last_y = 0.0

    def process(self, iq: list[complex]) -> list[float]:
        values = np.asarray(iq, dtype=complex)
        if not np.all(np.isfinite(values)):
            raise ValueError("nonfinite IQ")
        if not len(values):
            return []
        if self.mode == "FM":
            preceding = np.concatenate(([self.previous], values[:-1]))
            audio = np.angle(values * np.conjugate(preceding)) * IQ_RATE / (
                2 * math.pi * 2500
            )
            self.previous = complex(values[-1])
        elif self.mode == "AM":
            # Track the carrier at 1.53 Hz; preserves speech above 30 Hz.
            audio = []
            for value in np.abs(values):
                self.carrier += 0.0001 * (float(value) - self.carrier)
                audio.append((float(value) - self.carrier) / max(1e-8, self.carrier * 0.8))
        else:
            delayed = np.concatenate((self.usb_history, values))
            self.usb_history = delayed[-(USB_TAPS // 2):].copy()
            # Positive-frequency selector; do not demodulate the unwanted LSB.
            analytic = 0.5 * (delayed[:len(values)] + 1j * self.usb_hilbert.process(values))
            audio = analytic.real
        filtered = self.filter.process(audio).real
        first = (RATIO - self.index % RATIO) - 1
        selected = filtered[first::RATIO]
        self.index += len(values)
        output = []
        for value in selected:
            y = value - self.last_x + 0.9767 * self.last_y
            self.last_x, self.last_y = float(value), float(y)
            output.append(float(y))
        return output
