"""Test-only integration fixture, not a selectable production backend."""

from types import SimpleNamespace
import unittest

from radio.rotor_integration import RotorIntegration
from radio.safety import Safety
from radio.tracking import TrackingInput


class RotorIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.safety = Safety(lambda: None, lambda: self.now, lambda: 1000)
        self.tracking = TrackingInput(self.safety)
        self.sample = {"sampledMonotonic": 100, "hardwareCommissioned": True,
                       "gnssSampledMonotonic": 100, "trackingSampledMonotonic": 100,
                       "gnssValid": True, "sgp4Valid": True, "fault": None,
                       "rangeRateMps": 1000, "utc": 1000, "site": [42, 2, 20]}
        self.calls = []
        adapter = SimpleNamespace(
            snapshot=lambda: self.sample,
            dispatch=lambda *args: self.calls.append(args) or {
                "schema": "cm5-rotor/v1", "ok": True, "data": {}, "error": None},
            disconnect=lambda peer: self.calls.append(("disconnect", peer)),
            close=lambda: self.calls.append(("close",)))
        self.integration = RotorIntegration(adapter, self.safety, self.tracking,
                                             clock=lambda: self.now)

    def test_fresh_state_routes_exact_authenticated_session_three_axes(self):
        result = self.integration.dispatch("/rotor/target", "set",
                                           {"azDeg": 1, "elDeg": 2, "polDeg": 3}, "radio-peer")
        self.assertEqual(result["schema"], "cm5-rotor/v1")
        self.assertEqual(self.calls[0][-1], "radio-peer")
        self.integration.refresh()
        self.assertTrue(self.safety.tracking_fresh())
        self.assertTrue(self.safety.rotor_ready())
        self.integration.disconnect("radio-peer")
        self.assertEqual(self.calls[-1], ("disconnect", "radio-peer"))

    def test_invalid_commission_or_stale_state_revokes_tracking(self):
        self.integration.refresh()
        self.sample["hardwareCommissioned"] = False
        with self.assertRaises(PermissionError):
            self.integration.refresh()
        self.assertFalse(self.safety.tracking_fresh())
        self.sample["hardwareCommissioned"] = True
        self.now += 0.201
        with self.assertRaises(ValueError):
            self.integration.refresh()
        self.assertFalse(self.safety.rotor_ready())

    def test_no_two_axis_defaults_or_unknown_legacy_path(self):
        with self.assertRaises(ValueError):
            self.integration.dispatch("/rotor/target", "set", {"azDeg": 1, "elDeg": 2}, "peer")
        with self.assertRaises(ValueError):
            self.integration.dispatch("/rotor/assumed-old-api", "set", {}, "peer")
        self.assertFalse(self.calls)

    def test_source_timestamp_not_refreshed_by_new_snapshot_timestamp(self):
        self.integration.refresh()
        self.now = 101.01
        self.sample["sampledMonotonic"] = self.now
        with self.assertRaises(ValueError):
            self.integration.refresh()
        self.assertFalse(self.safety.tracking_fresh())

    def test_all_actual_routes_available_before_gnss_commissioning(self):
        self.sample["hardwareCommissioned"] = False
        for path, op in (
            ("/rotor/status", "get"), ("/rotor/sensorsstatus", "get"),
            ("/rotor/home", "set"), ("/rotor/calibrate", "set"),
            ("/rotor/track", "set"), ("/rotor/stop", "set"),
            ("/satellites/catalog", "get"), ("/satellites/passes", "get")
        ):
            result = self.integration.dispatch(path, op, {}, "verified-phone")
            self.assertTrue(result["ok"])
            self.assertEqual(self.calls[-1][-1], "verified-phone")
        self.assertFalse(self.safety.check())

    def test_actual_public_adapter_with_test_only_controller_and_reply_propagation(self):
        from rotor.radio_adapter import RotorRadioAdapter
        from radio.control import Dispatcher
        from radio.protocol import Audio
        calls = []
        # Actual rotor adapter, explicitly test-only controller composition.
        controller = SimpleNamespace(
            start_service=lambda: calls.append("start"),
            integration_snapshot=lambda: self.sample,
            dispatch_host_path=lambda path, operation, data: {
                "schema": "cm5-rotor/v1", "ok": False, "data": None,
                "error": "controller-safety-denied"},
            close=lambda: calls.append("close"))
        adapter = RotorRadioAdapter(controller)
        integration = RotorIntegration(adapter, self.safety, self.tracking,
                                       clock=lambda: self.now)
        dispatcher = Dispatcher(self.safety, Audio(self.safety.inhibit), "a" * 64)
        dispatcher.authenticated.add("phone")
        dispatcher.rotor = integration
        reply = dispatcher.dispatch({
            "v": 1, "id": "track-1", "path": "/rotor/track", "op": "set",
            "data": {"noradId": 25544}}, "phone", True, True)
        self.assertFalse(reply["ok"])
        self.assertEqual(reply["schema"], "cm5-rotor/v1")
        self.assertEqual(reply["error"], "controller-safety-denied")
        self.assertEqual(reply["id"], "track-1")
        integration.close()
        self.assertEqual(calls, ["start", "close"])
