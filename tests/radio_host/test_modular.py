from types import SimpleNamespace
import unittest

from radio.safety import Safety


class ModularPolicyTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.safety = Safety(lambda: None, lambda: self.now, lambda: 1000)
        self.safety.connect("authenticated")
        self.safety.physical(True, True)
        self.safety.sdr_ready = True
        self.safety.polarization = SimpleNamespace(ready=lambda: True)

    def test_standalone_explicit_confirmation_no_gnss_or_rotor(self):
        self.safety.allowed_profile = "STANDALONE_MANUAL"
        self.safety.operation_profile = "STANDALONE_MANUAL"
        with self.assertRaises(PermissionError):
            self.safety.lease("authenticated", 500)
        self.safety.select_profile("STANDALONE_MANUAL", "authenticated", True)
        self.safety.lease("authenticated", 500)
        self.assertTrue(self.safety.check())
        self.assertIsNone(self.safety.tracking)
        self.assertFalse(self.safety.rotor_ready())
        self.safety.tracking_update(1000, 1000, [42, 2, 20], True)
        self.assertEqual(self.safety.frequencies(), (145900000, 435100000))
        self.now += 0.501
        self.assertFalse(self.safety.check())

    def test_no_automatic_fallback_or_remote_policy_override(self):
        with self.assertRaises(PermissionError):
            self.safety.select_profile("STANDALONE_MANUAL", "authenticated", True)
        self.assertEqual(self.safety.operation_profile, "INTEGRATED_TRACKING")
        self.assertFalse(self.safety.check())
        self.assertEqual(self.safety.operation_profile, "INTEGRATED_TRACKING")
        self.safety.allowed_profile = "STANDALONE_MANUAL"
        with self.assertRaises(PermissionError):
            self.safety.select_profile("STANDALONE_MANUAL", "wrong-peer", True)
        with self.assertRaises(PermissionError):
            self.safety.select_profile("STANDALONE_MANUAL", "authenticated", False)

    def test_single_manual_channel_retains_physical_interlocks(self):
        self.safety.available_channels = ("VHF",)
        self.safety.rx_channel = self.safety.tx_channel = "VHF"
        self.safety.allowed_profile = "STANDALONE_MANUAL"
        self.safety.select_profile("STANDALONE_MANUAL", "authenticated", True)
        self.safety.tune(rx=145800000, tx=145900000)
        self.safety.lease("authenticated", 500)
        self.assertTrue(self.safety.check())
        self.safety.physical(True, False)
        self.assertFalse(self.safety.check())
        self.safety.disconnect("authenticated")
        self.assertIsNone(self.safety.profile_session)
