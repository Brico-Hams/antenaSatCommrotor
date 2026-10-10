import unittest

from radio.safety import Safety
from radio.tracking import TrackingInput


class TrackingInputTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.safety = Safety(lambda: None, lambda: self.now, lambda: 1000)
        self.input = TrackingInput(self.safety)

    def test_local_source_without_esp32_or_ble(self):
        self.input.provision("local-pi-sgp4")
        self.input.update("local-pi-sgp4", 1000, 1000, [42, 2, 20])
        self.assertTrue(self.safety.tracking_fresh())
        self.assertIsNone(self.safety.session)
        self.assertEqual(self.safety.frequencies(), (145899513, 435101451))
        self.now += 1.001
        self.assertFalse(self.safety.tracking_fresh())

    def test_trust_not_inferred_from_remote_token_and_revoke(self):
        with self.assertRaises(PermissionError):
            self.input.update("authenticated-phone", 0, 1000, [42, 2, 20])
        self.input.provision("authenticated-upstream")
        self.input.update("authenticated-upstream", 0, 1000, [42, 2, 20])
        self.input.revoke("authenticated-upstream")
        self.assertFalse(self.safety.tracking_fresh())
        self.assertEqual(self.safety.fault, "tracking-source-revoked")

    def test_invalid_source_or_sample_revokes_previous_state(self):
        for source in ("", None, "x" * 129):
            with self.assertRaises(ValueError):
                self.input.provision(source)
        self.input.provision("local")
        self.input.update("local", 0, 1000, [42, 2, 20])
        with self.assertRaises(ValueError):
            self.input.update("local", float("nan"), 1000, [42, 2, 20])
        self.assertFalse(self.safety.tracking_fresh())
        self.assertFalse(self.safety.check())
