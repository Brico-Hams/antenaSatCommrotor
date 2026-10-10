"""Bounded streaming rational clock conversion, with anti-alias FIR.

Output clock positions are integer ratios, not floating accumulated phases.
One input sample of interpolation lookahead is retained across blocks.
"""

import numpy as np
from scipy.signal import firwin, lfilter


class RationalResampler:
    def __init__(self, input_rate: int, output_rate: int):
        if any(type(rate) is not int or not 8000 <= rate <= 4000000
               for rate in (input_rate, output_rate)):
            raise ValueError("invalid verified resampling rates")
        self.input_rate, self.output_rate = input_rate, output_rate
        # RF baseband occupies <=12kHz. Suppress aliases before downsampling.
        self.h = firwin(257, min(18000, min(input_rate, output_rate) * 0.4),
                        fs=input_rate)
        self.state = np.zeros(len(self.h) - 1, dtype=complex)
        self.received = self.produced = 0
        self.previous = None

    def process(self, values):
        values = np.asarray(values, dtype=complex)
        if not np.all(np.isfinite(values)):
            raise ValueError("nonfinite resampling input")
        if not len(values):
            return []
        filtered, self.state = lfilter(self.h, [1.0], values, zi=self.state)
        start = self.received
        self.received += len(values)
        if self.previous is not None:
            filtered = np.concatenate(([self.previous], filtered))
            start -= 1
        self.previous = complex(filtered[-1])
        # Only produce clock ticks with available interpolation lookahead.
        last = self.received - 1
        end = (last * self.output_rate + self.input_rate - 1) // self.input_rate
        indexes = np.arange(self.produced, end, dtype=np.int64)
        numerator = indexes * self.input_rate
        left = numerator // self.output_rate - start
        fraction = (numerator % self.output_rate) / self.output_rate
        if len(indexes):
            output = filtered[left] * (1 - fraction) + filtered[left + 1] * fraction
        else:
            output = np.empty(0, dtype=complex)
        self.produced = end
        return output.tolist()
