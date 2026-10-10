"""TEST ONLY switch/contact simulation, not RF or GPIO verification."""

from types import SimpleNamespace
import unittest

from radio.polarization import PolarizationSwitch, RFPolarization
from radio.safety import Safety


class PolarizationTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.events = []
        self.safety = Safety(lambda: self.events.append("TX-off"),
                             lambda: self.now, lambda: 1000)
        self.ack = None
        self.tx_off = True
        self.hardware = SimpleNamespace(
            capability_verified=True, capabilities=tuple(RFPolarization),
            settle_seconds=0.05, acknowledge=lambda: self.ack,
            tx_off_acknowledged=lambda: self.tx_off,
            write=lambda mode: self.events.append(mode))
        self.switch = PolarizationSwitch(self.safety, self.hardware, lambda: self.now)

    def test_no_hardware_never_claims_configured(self):
        switch = PolarizationSwitch(self.safety)
        for mode in RFPolarization:
            with self.assertRaises(PermissionError):
                switch.select(mode)
            self.assertIsNone(switch.status()["configured"])
        self.hardware.capability_verified = False
        with self.assertRaises(PermissionError):
            self.switch.select("RHCP")

    def test_tx_off_settle_ack_and_feedback_loss(self):
        self.safety.transmitting = True
        self.switch.select("RHCP")
        self.assertEqual(self.events, ["TX-off", RFPolarization.RHCP])
        self.ack = RFPolarization.RHCP
        self.assertFalse(self.switch.ready())
        self.now += 0.051
        self.assertTrue(self.switch.ready())
        self.assertEqual(self.switch.status()["configured"], "RHCP")
        self.ack = RFPolarization.LHCP
        self.assertFalse(self.switch.ready())
        self.assertIsNone(self.switch.status()["configured"])
        self.tx_off = False
        with self.assertRaises(PermissionError):
            self.switch.select("LHCP")
        self.assertEqual(self.events.count(RFPolarization.LHCP), 0)

    def test_rotor_fault_or_stale_or_switch_prevents_lease(self):
        self.safety.connect("test")
        self.safety.physical(True, True)
        self.safety.sdr_ready = True
        self.safety.tracking_update(0, 1000, [42, 2, 20], True)
        self.safety.rotor_update(None, True)
        with self.assertRaises(PermissionError):
            self.safety.lease("test", 500)
        self.switch.select("LINEAR")
        self.ack = RFPolarization.LINEAR
        self.now += 0.051
        self.safety.lease("test", 500)
        self.assertTrue(self.safety.check())
        self.safety.rotor_update("NC-estop-open", True)
        self.assertFalse(self.safety.check())
        self.safety.rotor_update(None, True)
        self.safety.lease("test", 500)
        self.now += 0.4
        self.safety.lease("test", 500)
        self.now += 0.101
        self.assertFalse(self.safety.check())
        self.assertFalse(self.safety.rotor_ready())

    def test_stop_failure_no_switch_write_and_untrusted_rotor(self):
        self.safety.stop_tx = lambda: (_ for _ in ()).throw(RuntimeError("stop failure"))
        with self.assertRaises(RuntimeError):
            self.switch.select("LHCP")
        self.assertFalse(self.events)
        self.safety.stop_tx = lambda: None
        with self.assertRaises(PermissionError):
            self.safety.rotor_update(None, False)
        self.assertFalse(self.safety.rotor_ready())
