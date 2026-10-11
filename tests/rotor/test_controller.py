from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from rotor.catalog import TleCatalog
from rotor.controller import AxisSettings, RotorController, RotorSettings
from rotor.driver import Tmc5160Axis, Tmc5160Spi
from rotor.gnss import GnssFix
from rotor.radio_adapter import open_adapter
from rotor.sensors import (
    EncoderReading,
    ImuReading,
    LimitSnapshot,
    MagnetometerReading,
    SensorFault,
    SensorSnapshot,
)


class SimulatedSpiTransport:
    """Strict test-only SPI fixture; production code never substitutes it."""

    def __init__(self):
        self.registers = {0x04: 0x30000000}
        self.pending_address = None

    def transfer(self, frame):
        if len(frame) != 5:
            raise AssertionError("expected a five-byte TMC5160 datagram")
        address = frame[0] & 0x7F
        if frame[0] & 0x80:
            self.registers[address] = int.from_bytes(frame[1:], "big")
            if address == 0x2D:
                self.registers[0x21] = self.registers[address]
                self.registers[0x35] = 1 << 9
            return bytes(5)
        value = (
            self.registers.get(self.pending_address, 0)
            if self.pending_address is not None
            else 0
        )
        self.pending_address = address
        return b"\0" + value.to_bytes(4, "big")


class TestOnlySensors:
    def __init__(self):
        self.now = 100.0
        self.limit_states = {
            "az": (True, True),
            "el": (True, True),
            "pol": (True, True),
        }

    def read_snapshot(self, monotonic_now):
        now = self.now
        return SensorSnapshot(
            encoders={
                axis: EncoderReading(
                    axis, channel, 0x100, 22.5, True, False, False, now
                )
                for axis, channel in (("az", 0), ("el", 1), ("pol", 2))
            },
            limits=LimitSnapshot(
                dict(self.limit_states), now
            ),
            gnss=GnssFix(
                datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc),
                40.0,
                -3.0,
                650.0,
                1,
                8,
                now,
            ),
            imu=ImuReading(0.0, 0.0, (0.0, 0.0, 9.81), now),
            magnetometer=MagnetometerReading((40.0, 0.0, 0.0), now),
            estop_healthy=True,
            watchdog_healthy=True,
            motor_permit_healthy=True,
            driver_faults_clear={"az": True, "el": True, "pol": True},
            interlock_monotonic_received=now,
        )


class TestOnlyPowerGate:
    def __init__(self):
        self.enabled = None
        self.fail_enable = False

    def enable(self):
        if self.fail_enable:
            raise OSError("test-only power gate failure")
        self.enabled = True

    def disable(self):
        self.enabled = False


def build_test_controller(settings, sensors, gate, catalog):
    motors = {
        axis: Tmc5160Axis(
            Tmc5160Spi(SimulatedSpiTransport()),
            clock_hz=12_000_000,
            microsteps_per_output_revolution=steps,
            max_velocity_deg_s=2.0 if axis != "pol" else 1.0,
            acceleration_deg_s2=1.0,
            deceleration_deg_s2=1.0,
        )
        for axis, steps in (("az", 80_000), ("el", 80_000), ("pol", 16_000))
    }
    return RotorController(
        motors=motors,
        sensors=sensors,
        power_gate=gate,
        catalog=catalog,
        settings=settings,
        monotonic=lambda: sensors.now,
        utc_now=lambda: datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc),
    )


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.catalog = TleCatalog(f"{self.temp.name}/tle.json")
        self.settings = RotorSettings(
            axes={
                "az": AxisSettings(0, 360, 80_000, 2.25, 1, 0, 0.5),
                "el": AxisSettings(0, 180, 80_000, 2.25, -1, 0, 0.5),
                "pol": AxisSettings(-90, 90, 16_000, 1.0, -1, 0, 0.25),
            },
            mechanics_verified=False,
        )
        self.sensors = TestOnlySensors()
        self.gate = TestOnlyPowerGate()
        self.controller = build_test_controller(
            self.settings, self.sensors, self.gate, self.catalog
        )

    def tearDown(self):
        self.controller.close()
        self.temp.cleanup()

    def test_startup_is_deenergized_uncommissioned_and_status_is_explicit(self):
        self.assertFalse(self.gate.enabled)
        result = self.controller.handle_control("status", {})
        self.assertTrue(result["ok"])
        data = result["data"]
        self.assertFalse(data["commissioned"])
        self.assertFalse(data["verifiedHealthy"])
        self.assertIsNotNone(data["fault"])
        self.assertEqual(data["axes"]["az"]["positionDeg"], None)

    def test_motion_interlocks_require_fresh_physical_return_and_clear_driver_faults(self):
        snapshot = self.sensors.read_snapshot(self.sensors.now)
        self.assertTrue(snapshot.interlocks_healthy(self.sensors.now))
        self.assertTrue(
            self.controller._snapshot_healthy(
                snapshot, self.sensors.now, require_gnss=True
            )
        )
        self.assertFalse(
            replace(snapshot, motor_permit_healthy=None).interlocks_healthy(
                self.sensors.now
            )
        )
        self.assertFalse(
            self.controller._snapshot_healthy(
                replace(snapshot, motor_permit_healthy=None),
                self.sensors.now,
                require_gnss=True,
            )
        )
        self.assertFalse(
            replace(
                snapshot,
                driver_faults_clear={"az": True, "el": False, "pol": True},
            ).interlocks_healthy(self.sensors.now)
        )
        self.assertFalse(
            replace(
                snapshot,
                interlock_monotonic_received=self.sensors.now - 0.051,
            ).interlocks_healthy(self.sensors.now)
        )

    def test_remote_cannot_home_or_calibrate_and_goto_fails_closed(self):
        for operation, data in (
            ("home", {"confirm": "HOME CM5 ROTOR"}),
            ("calibrate", {"carrierVerified": True}),
        ):
            reply = self.controller.handle_control(operation, data)
            self.assertFalse(reply["ok"])
            self.assertIn("local console", reply["error"])
        reply = self.controller.handle_control(
            "goto", {"azDeg": 20, "elDeg": 30, "polDeg": 0}
        )
        self.assertFalse(reply["ok"])
        self.assertIn("state", reply["error"])
        self.assertFalse(self.gate.enabled)

    def test_power_gate_enable_failure_latches_fault_and_keeps_motion_inhibited(self):
        self.gate.fail_enable = True
        with self.assertRaisesRegex(OSError, "test-only power gate failure"):
            self.controller._enable_power_gate()
        self.assertEqual(self.controller._state, "FAULT")
        self.assertIn("power-gate-enable", self.controller._fault)
        self.assertFalse(self.gate.enabled)

    def test_stop_cancels_homing_and_invalidates_all_home_references(self):
        for motor in self.controller._motors.values():
            motor.verify_identity()
        self.controller._state = "HOMING"
        self.controller._homed = {"az": True, "el": True, "pol": True}
        self.gate.enabled = True

        reply = self.controller.handle_control("stop", {})

        self.assertTrue(reply["ok"], reply["error"])
        self.assertEqual(reply["data"]["state"], "DISARMED")
        self.assertTrue(self.controller._home_cancel_event.is_set())
        self.assertEqual(
            self.controller._homed, {"az": False, "el": False, "pol": False}
        )
        self.assertFalse(self.gate.enabled)

    def test_local_calibration_still_requires_frozen_mechanics(self):
        request = {
            "confirm": "CALIBRATE AND ARM CM5 ROTOR",
            "carrierVerified": True,
            "faultInspected": True,
            "encoderZeroDeg": {"az": 0, "el": 0, "pol": 0},
            "azBaseTrueDeg": 0,
            "polModel": "apparent-track",
            "polModelSource": "explicit commissioned orbit-plane convention",
            "polOffsetDeg": 0,
            "headingMode": "manual",
            "manualTrueHeadingDeg": 0,
            "manualHeadingSource": "surveyed compass",
            "manualHeadingDate": "2026-10-10",
            "manualHeadingUtc": "2026-10-10T12:00:00Z",
            "declinationDeg": 0,
            "declinationSource": "survey",
            "declinationDate": "2026-10-10",
            "baseLevelRollDeg": 0,
            "baseLevelPitchDeg": 0,
        }
        reply = self.controller.handle_control(
            "calibrate", request, local_console=True
        )
        self.assertFalse(reply["ok"])
        self.assertIn("not frozen", reply["error"])
        self.assertFalse(self.gate.enabled)

    def test_local_manual_heading_calibration_is_rejected_without_verified_bsp(self):
        settings = RotorSettings(
            axes=self.settings.axes,
            mechanics_verified=True,
        )
        gate = TestOnlyPowerGate()
        controller = build_test_controller(settings, self.sensors, gate, self.catalog)
        request = {
            "confirm": "CALIBRATE AND ARM CM5 ROTOR",
            "carrierVerified": True,
            "faultInspected": True,
            "encoderZeroDeg": {"az": 0, "el": 0, "pol": 0},
            "azBaseTrueDeg": 0,
            "polModel": "apparent-track",
            "polModelSource": "explicit local commissioning",
            "polOffsetDeg": 0,
            "headingMode": "manual",
            "manualTrueHeadingDeg": 0,
            "manualHeadingSource": "independent survey",
            "manualHeadingDate": "2026-10-10",
            "manualHeadingUtc": "2026-10-10T12:00:00Z",
            "declinationDeg": 0,
            "declinationSource": "survey record",
            "declinationDate": "2026-10-10",
            "baseLevelRollDeg": 0,
            "baseLevelPitchDeg": 0,
        }
        try:
            reply = controller.handle_control(
                "calibrate", request, local_console=True
            )
            self.assertFalse(reply["ok"])
            self.assertIn("manual heading calibration is disabled", reply["error"])
            self.assertFalse(gate.enabled)
            status = controller.handle_control("status", {})
            self.assertTrue(status["ok"])
            self.assertFalse(status["data"]["calibrated"])
            self.assertFalse(status["data"]["commissioned"])
            self.assertFalse(status["data"]["verifiedHealthy"])
        finally:
            controller.close()

    def test_unknown_operations_and_client_supplied_origin_are_not_trusted(self):
        self.assertFalse(self.controller.handle_control("arm", {})["ok"])
        reply = self.controller.handle_control(
            "calibrate",
            {"local_console": True},
            local_console=False,
        )
        self.assertFalse(reply["ok"])
        self.assertIn("local console", reply["error"])

    def test_prepared_host_path_opens_adapter_with_path_and_public_methods(self):
        config_path = Path(self.temp.name) / "rotor-controller.json"
        config_path.write_text("{}", encoding="utf-8")
        received_paths = []

        def factory(path):
            received_paths.append(path)
            return self.controller

        provider = SimpleNamespace(name="cm5", load=lambda: factory)
        with patch("rotor.radio_adapter.entry_points", return_value=[provider]):
            adapter = open_adapter(config_path)
        try:
            self.assertEqual(received_paths, [config_path.resolve()])
            for method in ("snapshot", "dispatch", "disconnect", "close"):
                self.assertTrue(callable(getattr(adapter, method, None)))
            snapshot = adapter.snapshot()
            self.assertFalse(snapshot["hardwareCommissioned"])
            reply = adapter.dispatch(
                "/rotor/status", "get", {}, "authenticated-host-peer"
            )
            self.assertEqual(reply["schema"], "cm5-rotor/v1")
            self.assertTrue(reply["ok"])
            self.assertFalse(reply["data"]["verifiedHealthy"])
        finally:
            adapter.close()

    def test_host_adapter_refuses_to_fabricate_missing_cm5_bsp(self):
        config_path = Path(self.temp.name) / "rotor-controller.json"
        config_path.write_text("{}", encoding="utf-8")
        with patch("rotor.radio_adapter.entry_points", return_value=[]):
            with self.assertRaisesRegex(RuntimeError, "exactly one CM5 hardware BSP"):
                open_adapter(config_path)


if __name__ == "__main__":
    unittest.main()
