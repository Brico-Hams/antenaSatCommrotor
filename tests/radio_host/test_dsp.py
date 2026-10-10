import math
import unittest

import numpy as np

from radio.dsp import AUDIO_RATE, IQ_RATE, Demodulator, Modulator, doppler


class DSPTests(unittest.TestCase):
    def test_integer_doppler_directions(self):
        base = (145_900_000, 435_100_000)
        self.assertEqual(doppler(*base, 0), base)
        self.assertEqual(doppler(*base, 1000), (145_899_513, 435_101_451))
        self.assertEqual(doppler(*base, -1000), (145_900_487, 435_098_549))
        for invalid in (float("nan"), float("inf"), 12001):
            with self.assertRaises(ValueError):
                doppler(*base, invalid)

    def test_known_pcm_iq_roundtrip_measured(self):
        frequency = 700
        pcm = (0.45 * np.sin(2 * np.pi * frequency * np.arange(8000) / AUDIO_RATE)).tolist()
        for mode in ("FM", "AM", "USB"):
            with self.subTest(mode=mode):
                iq = Modulator(mode).process(pcm)
                self.assertEqual(len(iq), len(pcm) * 12)
                self.assertLessEqual(max(abs(x) for x in iq), 1.001)
                recovered = np.asarray(Demodulator(mode).process(iq))[1000:]
                spectrum = abs(np.fft.rfft(recovered))
                measured = np.argmax(spectrum) * AUDIO_RATE / len(recovered)
                self.assertLess(abs(measured - frequency), 2)
                # Compare against best delayed reference; deterministic FIR group delay.
                best = 0
                gain = 0
                error = 1
                for lag in range(100):
                    reference = np.asarray(pcm)[1000 - lag:8000 - lag]
                    correlation = float(np.corrcoef(reference, recovered)[0, 1])
                    if correlation > best:
                        best = correlation
                        gain = float(np.dot(recovered, reference) / np.dot(reference, reference))
                        error = float(np.sqrt(np.mean((recovered - gain * reference) ** 2)))
                print(f"DSP {mode}: frequency={measured:.3f}Hz correlation={best:.6f} "
                      f"gain={gain:.6f} residualRMS={error:.6f}")
                self.assertGreater(best, 0.995)
                self.assertGreater(gain, 0.94)
                self.assertLess(gain, 1.06)
                self.assertLess(error, 0.025)

    def test_usb_upper_sideband_rejection(self):
        pcm = (0.4 * np.sin(2 * np.pi * 1000 * np.arange(8000) / AUDIO_RATE)).tolist()
        iq = np.asarray(Modulator("USB").process(pcm))[12000:]
        spectrum = abs(np.fft.fft(iq))
        bins = np.fft.fftfreq(len(iq), 1 / IQ_RATE)
        upper = float(np.max(spectrum[(bins > 800) & (bins < 1200)]))
        lower = float(np.max(spectrum[(bins < -800) & (bins > -1200)]))
        rejection = 20 * math.log10(upper / lower)
        print(f"DSP USB unwanted-sideband rejection={rejection:.2f}dB (>=25dB)")
        self.assertGreater(rejection, 25)

    def test_usb_receiver_rejects_lower_sideband(self):
        t = np.arange(96000) / IQ_RATE
        upper = Demodulator("USB").process((0.4 * np.exp(2j * np.pi * 1000 * t)).tolist())
        lower = Demodulator("USB").process((0.4 * np.exp(-2j * np.pi * 1000 * t)).tolist())
        upper_rms = float(np.sqrt(np.mean(np.asarray(upper)[1000:] ** 2)))
        lower_rms = float(np.sqrt(np.mean(np.asarray(lower)[1000:] ** 2)))
        rejection = 20 * math.log10(upper_rms / lower_rms)
        print(f"DSP USB RX unwanted-sideband rejection={rejection:.2f}dB (>=25dB)")
        self.assertGreater(rejection, 25)

    def test_streaming_block_invariance_and_real_fm_phase(self):
        pcm = (0.4 * np.sin(2 * np.pi * 433 * np.arange(997) / AUDIO_RATE)).tolist()
        for mode in ("FM", "AM", "USB"):
            whole = Modulator(mode).process(pcm)
            mod = Modulator(mode)
            fragmented = []
            for offset in range(0, len(pcm), 31):
                fragmented.extend(mod.process(pcm[offset:offset + 31]))
            np.testing.assert_allclose(fragmented, whole, atol=1e-12)
            expected = Demodulator(mode).process(whole)
            demod = Demodulator(mode)
            actual = []
            for offset in range(0, len(whole), 127):
                actual.extend(demod.process(whole[offset:offset + 127]))
            np.testing.assert_allclose(actual, expected, atol=1e-11)
        iq = np.asarray(Modulator("FM").process(pcm))
        np.testing.assert_allclose(np.abs(iq), 1, atol=1e-12)
        self.assertGreater(len(np.unique(np.round(iq.real, 5))), 1000)

    def test_reject_invalid_modes_and_samples(self):
        for cls in (Modulator, Demodulator):
            with self.assertRaises(ValueError):
                cls("LSB")
        for value in (float("nan"), 1.1):
            with self.assertRaises(ValueError):
                Modulator("FM").process([value])
        with self.assertRaises(ValueError):
            Demodulator("FM").process([complex(float("nan"))])


if __name__ == "__main__":
    unittest.main()
