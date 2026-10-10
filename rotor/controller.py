"""Fail-closed three-axis controller and transport-neutral JSON operations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import math
import threading
import time
from typing import Callable, Mapping, Protocol

from .catalog import TleCatalog
from .driver import Tmc5160Axis, Tmc5160Fault
from .gnss import GnssFix, StaleFixError
from .orbit import (
    PropagationError,
    SatellitePass,
    Site,
    Tle,
    TleError,
    predict_passes,
    propagate,
)
from .sensors import (
    CompassCalibration,
    EncoderReading,
    SensorFault,
    SensorInputs,
    SensorSnapshot,
    tilt_compensated_true_heading,
)


AXES = ("az", "el", "pol")
SERVICE_PERIOD_S = 0.050
TRACKING_UPDATE_PERIOD_S = 0.500
HOME_TIMEOUT_S = 120.0
HOME_POLL_S = 0.020
GNSS_MAX_AGE_S = 10.0
ACQUISITION_ELEVATION_DEG = 15.0
ZENITH_GUARD_DEG = 89.0
DRIVER_GLOBAL_FAULT_MASK = 0x06
DRIVER_STATUS_FAULT_MASK = (1 << 26) | (1 << 25) | (1 << 15) | (1 << 14) | (1 << 7) | (1 << 6)


class MotorPowerGate(Protocol):
    """Carrier-specific normally-off motor power enable; not a step generator."""

    def enable(self) -> None: ...

    def disable(self) -> None: ...


@dataclass(frozen=True)
class AxisSettings:
    minimum_deg: float
    maximum_deg: float
    microsteps_per_output_revolution: int
    maximum_velocity_deg_s: float
    home_direction: int
    home_switch_index: int
    home_speed_deg_s: float
    maximum_following_error_deg: float = 2.0

    def __post_init__(self) -> None:
        values = (
            self.minimum_deg,
            self.maximum_deg,
            self.maximum_velocity_deg_s,
            self.home_speed_deg_s,
            self.maximum_following_error_deg,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("axis limits and speeds must be finite")
        if not self.minimum_deg < self.maximum_deg:
            raise ValueError("axis minimum must be below its maximum")
        if self.maximum_deg - self.minimum_deg > 360:
            raise ValueError("single-turn encoder travel cannot exceed 360 degrees")
        if (
            isinstance(self.microsteps_per_output_revolution, bool)
            or not isinstance(self.microsteps_per_output_revolution, int)
            or self.microsteps_per_output_revolution <= 0
        ):
            raise ValueError("mechanical microstep ratio must be a positive verified integer")
        if self.maximum_velocity_deg_s <= 0:
            raise ValueError("axis slew limit must be positive")
        if self.home_direction not in (-1, 1):
            raise ValueError("home direction must be -1 or 1")
        if self.home_switch_index not in (0, 1):
            raise ValueError("home switch index must be 0 (minimum) or 1 (maximum)")
        if not 0 < self.home_speed_deg_s <= 1:
            raise ValueError("homing speed must be in (0, 1] degree/second")
        if not 0 < self.maximum_following_error_deg <= 15:
            raise ValueError("following error threshold must be in (0, 15] degrees")


@dataclass(frozen=True)
class RotorSettings:
    axes: Mapping[str, AxisSettings]
    mechanics_verified: bool = False

    def __post_init__(self) -> None:
        if set(self.axes) != set(AXES):
            raise ValueError("rotor settings require exactly AZ, EL, and POL axes")
        for axis, settings in self.axes.items():
            if not isinstance(settings, AxisSettings):
                raise ValueError(f"{axis.upper()} settings are invalid")
            rate_limit = 1.0 if axis == "pol" else 2.25
            if settings.maximum_velocity_deg_s > rate_limit:
                raise ValueError(f"{axis.upper()} speed exceeds its allowed/provisional limit")


@dataclass(frozen=True)
class CommissioningRecord:
    encoder_zero_deg: Mapping[str, float]
    az_base_true_deg: float
    base_level_roll_deg: float
    base_level_pitch_deg: float
    pol_offset_deg: float
    pol_model: str
    pol_model_source: str
    compass: CompassCalibration | None
    manual_true_heading_deg: float | None
    manual_heading_source: str | None
    manual_heading_date: str | None
    manual_heading_utc: datetime | None
    declination_deg: float
    declination_source: str
    declination_date: str
    calibrated_utc: datetime


class RotorController:
    """Controller dependency-injected with real drivers and timestamped sensors."""

    def __init__(
        self,
        *,
        motors: Mapping[str, Tmc5160Axis],
        sensors: SensorInputs,
        power_gate: MotorPowerGate,
        catalog: TleCatalog,
        settings: RotorSettings,
        monotonic: Callable[[], float] = time.monotonic,
        utc_now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        if set(motors) != set(AXES):
            raise ValueError("three real motor drivers (AZ, EL, POL) are required")
        if not callable(monotonic) or not callable(utc_now):
            raise ValueError("clock providers must be callable")
        for axis, motor in motors.items():
            axis_settings = settings.axes[axis]
            if motor.microsteps_per_output_revolution != axis_settings.microsteps_per_output_revolution:
                raise ValueError(f"{axis.upper()} driver microstep ratio differs from verified mechanics")
            if motor.max_velocity_deg_s > axis_settings.maximum_velocity_deg_s:
                raise ValueError(f"{axis.upper()} driver speed exceeds its configured safety limit")
        self._motors = dict(motors)
        self._sensors = sensors
        self._power_gate = power_gate
        self._catalog = catalog
        self._settings = settings
        self._monotonic = monotonic
        self._utc_now = utc_now
        self._lock = threading.RLock()
        self._state = "DISARMED"
        self._fault: str | None = None
        self._commissioned = False
        self._calibration: CommissioningRecord | None = None
        self._homed = {axis: False for axis in AXES}
        self._targets: dict[str, float | None] = {axis: None for axis in AXES}
        self._tracking: dict[str, object] | None = None
        self._thread: threading.Thread | None = None
        self._home_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._home_cancel_event = threading.Event()
        self._last_track_update = -math.inf
        self._last_positions: dict[str, float] = {}
        self._last_satellite_state: dict[str, object] | None = None
        self._move_started = 0.0
        self._closed = False
        self._power_gate.disable()

    def start_service(self) -> None:
        with self._lock:
            if self._closed:
                raise RuntimeError("rotor controller is closed")
            if self._thread is not None and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._service_worker,
                name="cm5-rotor-service",
                daemon=True,
            )
            self._thread.start()

    def close(self) -> None:
        self._stop_event.set()
        with self._lock:
            self._closed = True
            self._tracking = None
            self._state = "DISARMED" if self._fault is None else "FAULT"
        gate_error: OSError | None = None
        try:
            self._power_gate.disable()
        except OSError as exc:
            gate_error = exc
        failures = self._stop_motors()
        if gate_error is not None:
            failures.append(f"power-gate:{gate_error}")
        if failures:
            self._latch_fault("close-stop-failed:" + ";".join(failures))
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=1.0)
        home_thread = self._home_thread
        if home_thread is not None and home_thread is not threading.current_thread():
            home_thread.join(timeout=1.0)

    def handle_control(
        self,
        operation: str,
        data: Mapping[str, object],
        *,
        local_console: bool = False,
    ) -> Mapping[str, object]:
        if not isinstance(operation, str) or not isinstance(data, Mapping):
            return self._error("operation and data object are required")
        if type(local_console) is not bool:
            return self._error("local_console must be a trusted boolean")
        if self._closed:
            return self._error("rotor controller is closed")
        try:
            if operation == "status":
                return self._success(self._status())
            if operation == "sensorsstatus":
                return self._success(self._sensor_status(self._read_snapshot()))
            if operation == "catalog":
                return self._success(
                    {
                        "items": [
                            {
                                "noradId": item.norad_id,
                                "name": item.name,
                                "epochUtc": item.epoch_utc,
                            }
                            for item in self._catalog.entries()
                        ]
                    }
                )
            if operation == "passes":
                return self._success(self._passes(data))
            if operation == "calibrate":
                return self._success(self._calibrate(data, local_console))
            if operation == "home":
                return self._success(self._home(data, local_console))
            if operation == "goto":
                return self._success(self._goto(data))
            if operation == "track":
                return self._success(self._track(data))
            if operation == "stop":
                return self._success(self._stop())
            return self._error(f"unsupported rotor operation: {operation}")
        except (PermissionError, ValueError, KeyError, StaleFixError, TleError, PropagationError,
                SensorFault, Tmc5160Fault, OSError, TimeoutError) as exc:
            if operation == "calibrate" and isinstance(exc, (Tmc5160Fault, OSError)):
                self._latch_fault(f"calibration-hardware:{exc}")
            return self._error(str(exc))

    def integration_snapshot(self) -> Mapping[str, object]:
        """Return the local-only radio safety/tracking handoff with source times."""
        reply = self.handle_control("status", {})
        if reply.get("ok") is not True or not isinstance(reply.get("data"), dict):
            raise SensorFault(str(reply.get("error") or "rotor status unavailable"))
        status = reply["data"]
        sensors = status["sensors"]
        gnss = sensors["gnss"]
        satellite = status["satellite"]
        now = self._monotonic()
        gnss_valid = isinstance(gnss, dict) and gnss.get("valid") is True
        satellite_valid = (
            isinstance(satellite, dict)
            and isinstance(satellite.get("sampledMonotonic"), (int, float))
            and 0 <= now - satellite["sampledMonotonic"] <= 1.0
            and isinstance(satellite.get("rangeRateMps"), (int, float))
        )
        site = None
        gnss_sampled = None
        if gnss_valid:
            site = (
                gnss["latitudeDeg"],
                gnss["longitudeDeg"],
                gnss["altitudeM"],
            )
            gnss_sampled = now - gnss["ageMs"] / 1000.0
        satellite_utc = None
        if satellite_valid:
            satellite_utc = datetime.fromisoformat(
                satellite["utc"].replace("Z", "+00:00")
            ).timestamp()
        hardware_commissioned = status["verifiedHealthy"] is True
        fault = status["fault"]
        if fault is None and not hardware_commissioned:
            fault = "rotor-not-verified"
        if fault is None and not (gnss_valid and satellite_valid):
            fault = "tracking-source-unavailable"
        return {
            "sampledMonotonic": now,
            "hardwareCommissioned": hardware_commissioned,
            "gnssValid": gnss_valid,
            "gnssSampledMonotonic": gnss_sampled,
            "sgp4Valid": satellite_valid,
            "trackingSampledMonotonic": (
                satellite.get("sampledMonotonic")
                if isinstance(satellite, dict)
                else None
            ),
            "fault": fault,
            "utc": satellite_utc,
            "site": site,
            "rangeRateMps": (
                satellite.get("rangeRateMps")
                if satellite_valid and isinstance(satellite, dict)
                else None
            ),
            "status": status,
        }

    def dispatch_host_path(
        self,
        path: str,
        operation: str,
        data: Mapping[str, object],
    ) -> Mapping[str, object]:
        """Translate authenticated host paths to controller JSON operations."""
        routes = {
            ("/rotor/status", "get"): "status",
            ("/rotor/sensorsstatus", "get"): "sensorsstatus",
            ("/rotor/home", "set"): "home",
            ("/rotor/calibrate", "set"): "calibrate",
            ("/rotor/target", "set"): "goto",
            ("/rotor/track", "set"): "track",
            ("/rotor/stop", "set"): "stop",
            ("/satellites/catalog", "get"): "catalog",
            ("/satellites/passes", "get"): "passes",
        }
        controller_operation = routes.get((path, operation))
        if controller_operation is None:
            return {
                "schema": "cm5-rotor/v1",
                "ok": False,
                "data": None,
                "error": f"unsupported rotor host path/operation: {path} {operation}",
            }
        reply = self.handle_control(controller_operation, data)
        return {
            "schema": "cm5-rotor/v1",
            **reply,
        }

    def service_once(self) -> None:
        with self._lock:
            state = self._state
            if state in ("DISARMED", "FAULT", "HOMING"):
                return
        snapshot = self._read_snapshot()
        self._require_motion_feedback(snapshot, self._monotonic())
        self._check_driver_health()
        with self._lock:
            if self._state == "TRACKING":
                now = self._monotonic()
                if now - self._last_track_update >= TRACKING_UPDATE_PERIOD_S:
                    targets = self._tracking_targets(snapshot, now)
                    self._issue_targets(targets, snapshot)
                    self._last_track_update = now
            if self._state in ("MOVING", "TRACKING"):
                self._check_following_error(snapshot, self._monotonic())

    def _status(self) -> dict[str, object]:
        now = self._monotonic()
        snapshot: SensorSnapshot | None
        try:
            snapshot = self._read_snapshot()
        except (OSError, TimeoutError, SensorFault) as exc:
            snapshot = None
            self._latch_fault(f"sensor-read:{exc}")
        sensor_data = self._sensor_status(snapshot) if snapshot is not None else {
            "valid": False,
            "fault": self._fault or "sensor-read-failed",
            "gnss": None,
            "encoders": {},
            "limits": None,
            "compass": None,
            "imu": None,
            "estopHealthy": None,
            "watchdogHealthy": None,
            "motorPermitHealthy": None,
            "driverFaultsClear": None,
            "interlockAgeMs": None,
            "interlocksValid": False,
        }
        driver_healthy = False
        if snapshot is not None:
            try:
                self._check_driver_health()
                driver_healthy = True
            except (OSError, Tmc5160Fault) as exc:
                self._latch_fault(f"driver-status:{exc}")
        axes: dict[str, object] = {}
        for axis in AXES:
            reading = snapshot.encoders.get(axis) if snapshot is not None else None
            valid = reading is not None and reading.valid(now)
            position = (
                self._position_from_encoder(axis, reading)
                if valid and reading is not None and self._calibration is not None
                else None
            )
            axes[axis] = {
                "positionDeg": position,
                "targetDeg": self._targets[axis],
                "homed": self._homed[axis],
                "encoderValid": valid,
                "encoderAgeMs": (
                    round(reading.age_s(now) * 1000) if reading is not None else None
                ),
                "minimumLimitClosed": (
                    snapshot.limits.closed[axis][0]
                    if snapshot is not None and snapshot.limits is not None
                    else None
                ),
                "maximumLimitClosed": (
                    snapshot.limits.closed[axis][1]
                    if snapshot is not None and snapshot.limits is not None
                    else None
                ),
            }
        healthy = (
            snapshot is not None
            and self._fault is None
            and self._commissioned
            and self._calibration is not None
            and all(self._homed.values())
            and driver_healthy
            and self._snapshot_healthy(snapshot, now, require_gnss=True)
        )
        return {
            "state": self._state,
            "fault": self._fault,
            "verifiedHealthy": bool(healthy),
            "commissioned": self._commissioned,
            "calibrated": self._calibration is not None,
            "updatedMonotonic": now,
            "axes": axes,
            "sensors": sensor_data,
            "satellite": self._last_satellite_state,
        }

    def _sensor_status(self, snapshot: SensorSnapshot) -> dict[str, object]:
        now = self._monotonic()
        gnss: GnssFix | None = snapshot.gnss
        heading_true: float | None = None
        declination: float | None = None
        declination_source: str | None = None
        declination_date: str | None = None
        heading_mode: str | None = None
        if (
            self._calibration is not None
            and self._calibration.compass is not None
            and snapshot.magnetometer is not None
            and snapshot.imu is not None
            and snapshot.magnetometer.valid(now)
            and snapshot.imu.valid(now)
        ):
            heading = tilt_compensated_true_heading(
                snapshot.magnetometer,
                snapshot.imu,
                self._calibration.compass,
                now,
            )
            heading_true = heading.true_deg
            declination = heading.declination_deg
            declination_source = heading.declination_source
            declination_date = heading.declination_date
            heading_mode = "compass"
        elif self._calibration is not None:
            heading_true = self._calibration.manual_true_heading_deg
            declination_source = self._calibration.manual_heading_source
            heading_mode = "manual"
            declination = self._calibration.declination_deg
            declination_source = self._calibration.declination_source
            declination_date = self._calibration.declination_date
        encoder_data = {
            axis: (
                {
                    "channel": reading.channel,
                    "rawAngle": reading.raw_angle,
                    "angleDeg": reading.angle_deg,
                    "magnetDetected": reading.magnet_detected,
                    "magnetTooStrong": reading.magnet_too_strong,
                    "magnetTooWeak": reading.magnet_too_weak,
                    "ageMs": round(reading.age_s(now) * 1000),
                    "valid": reading.valid(now),
                }
                if reading is not None
                else None
            )
            for axis in AXES
            for reading in (snapshot.encoders.get(axis),)
        }
        limits_data = None
        if snapshot.limits is not None:
            limits_data = {
                "minimumClosed": {
                    axis: (
                        snapshot.limits.closed[axis][0]
                        if axis in snapshot.limits.closed
                        and len(snapshot.limits.closed[axis]) == 2
                        else None
                    )
                    for axis in AXES
                },
                "maximumClosed": {
                    axis: (
                        snapshot.limits.closed[axis][1]
                        if axis in snapshot.limits.closed
                        and len(snapshot.limits.closed[axis]) == 2
                        else None
                    )
                    for axis in AXES
                },
                "ageMs": round((now - snapshot.limits.monotonic_received) * 1000),
                "valid": snapshot.limits.healthy(now),
            }
        return {
            "valid": self._snapshot_healthy(snapshot, now, require_gnss=False),
            "gnss": (
                {
                    "valid": gnss is not None and gnss.fresh(now, GNSS_MAX_AGE_S),
                    "utc": gnss.utc.isoformat() if gnss is not None else None,
                    "latitudeDeg": gnss.latitude_deg if gnss is not None else None,
                    "longitudeDeg": gnss.longitude_deg if gnss is not None else None,
                    "altitudeM": gnss.altitude_m if gnss is not None else None,
                    "ageMs": (
                        round(gnss.age_s(now) * 1000) if gnss is not None else None
                    ),
                    "fixQuality": gnss.fix_quality if gnss is not None else None,
                    "satellites": gnss.satellites if gnss is not None else None,
                }
            ),
            "encoders": encoder_data,
            "limits": limits_data,
            "compass": {
                "valid": heading_true is not None,
                "mode": heading_mode,
                "headingTrueDeg": heading_true,
                "declinationDeg": declination,
                "declinationSource": declination_source,
                "declinationDate": declination_date,
                "manualReferenceSource": (
                    self._calibration.manual_heading_source
                    if self._calibration is not None
                    else None
                ),
                "manualReferenceDate": (
                    self._calibration.manual_heading_date
                    if self._calibration is not None
                    else None
                ),
                "manualReferenceUtc": (
                    self._calibration.manual_heading_utc.isoformat()
                    if self._calibration is not None
                    and self._calibration.manual_heading_utc is not None
                    else None
                ),
            },
            "imu": (
                {
                    "valid": snapshot.imu.valid(now),
                    "rollDeg": snapshot.imu.roll_deg,
                    "pitchDeg": snapshot.imu.pitch_deg,
                    "accelerationMps2": list(snapshot.imu.acceleration_mps2),
                    "ageMs": round((now - snapshot.imu.monotonic_received) * 1000),
                }
                if snapshot.imu is not None
                else None
            ),
            "estopHealthy": snapshot.estop_healthy,
            "watchdogHealthy": snapshot.watchdog_healthy,
            "motorPermitHealthy": snapshot.motor_permit_healthy,
            "driverFaultsClear": (
                dict(snapshot.driver_faults_clear)
                if snapshot.driver_faults_clear is not None
                else None
            ),
            "interlockAgeMs": (
                round((now - snapshot.interlock_monotonic_received) * 1000)
                if snapshot.interlock_monotonic_received is not None
                and math.isfinite(snapshot.interlock_monotonic_received)
                and now >= snapshot.interlock_monotonic_received
                else None
            ),
            "interlocksValid": snapshot.interlocks_healthy(now),
        }

    def _read_snapshot(self) -> SensorSnapshot:
        snapshot = self._sensors.read_snapshot(self._monotonic())
        if not isinstance(snapshot, SensorSnapshot):
            raise SensorFault("sensor provider returned an invalid snapshot")
        return snapshot

    def _snapshot_healthy(
        self,
        snapshot: SensorSnapshot,
        now: float,
        *,
        require_gnss: bool,
        require_compass: bool | None = None,
    ) -> bool:
        if set(snapshot.encoders) != set(AXES):
            return False
        if not all(snapshot.encoders[axis].valid(now) for axis in AXES):
            return False
        if snapshot.limits is None or not snapshot.limits.healthy(now):
            return False
        if not snapshot.interlocks_healthy(now):
            return False
        if snapshot.imu is None or not snapshot.imu.valid(now):
            return False
        if require_compass is None:
            require_compass = self._calibration is None or self._calibration.compass is not None
        if require_compass and (
            snapshot.magnetometer is None or not snapshot.magnetometer.valid(now)
        ):
            return False
        if self._calibration is not None and (
            abs(snapshot.imu.roll_deg - self._calibration.base_level_roll_deg) > 2
            or abs(snapshot.imu.pitch_deg - self._calibration.base_level_pitch_deg) > 2
        ):
            return False
        if require_gnss and (
            snapshot.gnss is None or not snapshot.gnss.fresh(now, GNSS_MAX_AGE_S)
        ):
            return False
        return True

    def _require_motion_feedback(self, snapshot: SensorSnapshot, now: float) -> None:
        if not self._commissioned:
            raise SensorFault("carrier is not locally commissioned and verified")
        if self._calibration is None:
            raise SensorFault("rotor calibration is not present in this boot session")
        if self._fault is not None:
            raise SensorFault(f"latched rotor fault: {self._fault}")
        if not self._snapshot_healthy(
            snapshot,
            now,
            require_gnss=False,
            require_compass=self._calibration.compass is not None,
        ):
            raise SensorFault(
                "required encoder, NC limit, E-stop/watchdog, motor-permit "
                "return, driver-fault, compass, or IMU feedback is invalid"
            )
        if not all(self._homed.values()):
            raise SensorFault("all three axes must be homed in this boot session")
        self._check_driver_health()

    def _check_driver_health(self) -> None:
        for axis, motor in self._motors.items():
            state = motor.driver_status()
            if state["globalStatus"] & DRIVER_GLOBAL_FAULT_MASK:
                raise Tmc5160Fault(f"{axis.upper()} TMC5160 global fault")
            if state["driverStatus"] & DRIVER_STATUS_FAULT_MASK:
                raise Tmc5160Fault(f"{axis.upper()} TMC5160 driver fault")

    def _calibrate(
        self, data: Mapping[str, object], local_console: bool
    ) -> dict[str, object]:
        if not local_console:
            raise PermissionError("calibration is available only from the trusted local console")
        with self._lock:
            if self._state not in ("DISARMED", "FAULT"):
                raise SensorFault(f"calibration is not permitted while state is {self._state}")
        required = {
            "confirm",
            "carrierVerified",
            "faultInspected",
            "encoderZeroDeg",
            "azBaseTrueDeg",
            "polModel",
            "polOffsetDeg",
            "headingMode",
            "declinationDeg",
            "declinationSource",
            "declinationDate",
            "baseLevelRollDeg",
            "baseLevelPitchDeg",
            "polModelSource",
        }
        if not required <= set(data):
            raise ValueError("calibration is missing required surveyed values")
        if data["confirm"] != "CALIBRATE AND ARM CM5 ROTOR":
            raise PermissionError("explicit local calibration/arm confirmation is required")
        if data["carrierVerified"] is not True:
            raise PermissionError("carrier verification must be explicitly confirmed locally")
        if data["faultInspected"] is not True:
            raise PermissionError("local fault inspection/reset must be explicitly confirmed")
        if not self._settings.mechanics_verified:
            raise PermissionError("mechanical ratios, travel, and hard stops are not frozen")
        if data["polModel"] not in ("apparent-track", "cross-track"):
            raise ValueError("POL tracking model must be explicitly selected")
        encoder_zero = self._axis_values(data["encoderZeroDeg"], "encoderZeroDeg")
        if any(not 0 <= value < 360 for value in encoder_zero.values()):
            raise ValueError("encoderZeroDeg values must be in [0, 360)")
        az_base = self._finite_number(data["azBaseTrueDeg"], "azBaseTrueDeg")
        if not 0 <= az_base < 360:
            raise ValueError("azBaseTrueDeg must be in [0, 360)")
        pol_offset = self._finite_number(data["polOffsetDeg"], "polOffsetDeg")
        if not -180 <= pol_offset <= 180:
            raise ValueError("polOffsetDeg must be in [-180, 180]")
        declination = self._finite_number(data["declinationDeg"], "declinationDeg")
        if not -180 <= declination <= 180:
            raise ValueError("declinationDeg must be in [-180, 180]")
        declination_source = self._string(data["declinationSource"], "declinationSource", 128)
        declination_date = self._string(data["declinationDate"], "declinationDate", 32)
        pol_model_source = self._string(data["polModelSource"], "polModelSource", 128)
        heading_mode = data["headingMode"]
        if heading_mode == "manual":
            raise PermissionError(
                "manual heading calibration is disabled until the selected compass/IMU BSP is verified"
            )
        if heading_mode != "compass":
            raise ValueError("headingMode must be compass")
        base_level_roll = self._finite_number(data["baseLevelRollDeg"], "baseLevelRollDeg")
        base_level_pitch = self._finite_number(data["baseLevelPitchDeg"], "baseLevelPitchDeg")
        if abs(base_level_roll) > 2 or abs(base_level_pitch) > 2:
            raise ValueError("base must be level within 2 degrees before commissioning")
        snapshot = self._read_snapshot()
        now = self._monotonic()
        if not self._snapshot_healthy(
            snapshot,
            now,
            require_gnss=True,
            require_compass=True,
        ):
            raise SensorFault(
                "calibration requires fresh GNSS, encoders/limits, validated "
                "E-stop/watchdog/motor-permit/driver-fault returns, IMU, and "
                "selected heading source"
            )
        if snapshot.imu is None:
            raise SensorFault("calibration requires a fresh base IMU")
        if (
            abs(snapshot.imu.roll_deg - base_level_roll) > 2
            or abs(snapshot.imu.pitch_deg - base_level_pitch) > 2
        ):
            raise SensorFault("measured base level does not match the local calibration values")
        for motor in self._motors.values():
            motor.verify_identity()
        self._check_driver_health()
        synchronized_positions: dict[str, float] = {}
        for axis in AXES:
            reading = snapshot.encoders[axis]
            relative = (reading.angle_deg - encoder_zero[axis]) % 360
            position = self._nearest_equivalent(
                relative, None, self._settings.axes[axis]
            )
            if not self._settings.axes[axis].minimum_deg <= position <= self._settings.axes[axis].maximum_deg:
                raise SensorFault(f"{axis.upper()} encoder position is outside frozen travel")
            synchronized_positions[axis] = position
        compass: CompassCalibration | None = None
        compass = self._compass_calibration(
            data, declination, declination_source, declination_date
        )
        measured_heading = tilt_compensated_true_heading(
            snapshot.magnetometer, snapshot.imu, compass, now
        )
        if abs((measured_heading.true_deg - az_base + 180) % 360 - 180) > 5:
            raise SensorFault("compass heading differs from the independently surveyed AZ base by more than 5 degrees")
        manual_heading: float | None = None
        manual_source: str | None = None
        manual_date: str | None = None
        manual_heading_utc: datetime | None = None
        candidate = CommissioningRecord(
            encoder_zero,
            az_base,
            base_level_roll,
            base_level_pitch,
            pol_offset,
            str(data["polModel"]),
            pol_model_source,
            compass,
            manual_heading,
            manual_source,
            manual_date,
            manual_heading_utc,
            declination,
            declination_source,
            declination_date,
            self._utc_now().astimezone(timezone.utc),
        )
        self._power_gate.disable()
        try:
            for axis in AXES:
                self._motors[axis].stop_ramped()
            for axis in AXES:
                self._motors[axis].set_position_degrees(
                    synchronized_positions[axis] + encoder_zero[axis]
                )
        except (OSError, Tmc5160Fault, ValueError) as exc:
            self._latch_fault(f"calibration-position-sync:{exc}")
            raise
        self._last_positions.update(synchronized_positions)
        with self._lock:
            self._calibration = candidate
            self._commissioned = True
            self._homed = {axis: False for axis in AXES}
            self._fault = None
            self._state = "DISARMED"
        return {
            "commissioned": True,
            "calibratedUtc": self._calibration.calibrated_utc.isoformat(),
            "headingMode": heading_mode,
            "polModel": self._calibration.pol_model,
            "polModelSource": self._calibration.pol_model_source,
            "motionReady": False,
            "note": "home all axes before motion; calibration is RAM-only and must be repeated after reboot",
        }

    def _compass_calibration(
        self,
        data: Mapping[str, object],
        declination: float,
        declination_source: str,
        declination_date: str,
    ) -> CompassCalibration:
        hard = self._vector(data.get("hardIronUT"), "hardIronUT")
        soft = self._matrix(data.get("softIronMatrix"), "softIronMatrix")
        orientation = self._matrix(data.get("sensorToBase"), "sensorToBase")
        return CompassCalibration(
            hard_iron_uT=hard,
            soft_iron_matrix=soft,
            sensor_to_base=orientation,
            declination_deg=declination,
            declination_source=declination_source,
            declination_date=declination_date,
            calibrated_utc=self._utc_now().astimezone(timezone.utc),
        )

    def _home(
        self, data: Mapping[str, object], local_console: bool
    ) -> dict[str, object]:
        if not local_console:
            raise PermissionError("homing is available only from the trusted local console")
        if data.get("confirm") != "HOME CM5 ROTOR":
            raise PermissionError("explicit local homing confirmation is required")
        with self._lock:
            if self._state != "DISARMED" or self._fault is not None:
                raise SensorFault(
                    f"homing requires a fault-free DISARMED state, not {self._state}"
                )
            if not self._commissioned or self._calibration is None:
                raise SensorFault("local commissioning and calibration are required before homing")
            if self._home_thread is not None and self._home_thread.is_alive():
                raise RuntimeError("homing is already in progress")
            snapshot = self._read_snapshot()
            self._require_commissioning_sensors(snapshot)
            for axis, settings in self._settings.axes.items():
                if not all(snapshot.limits.closed[axis]):
                    raise SensorFault(f"{axis.upper()} NC limits are not both closed at homing start")
                if not snapshot.limits.closed[axis][settings.home_switch_index]:
                    raise SensorFault(f"{axis.upper()} home limit is not closed at homing start")
            for motor in self._motors.values():
                motor.verify_identity()
            self._check_driver_health()
            self._homed = {axis: False for axis in AXES}
            self._home_cancel_event.clear()
            self._enable_power_gate()
            self._state = "HOMING"
            self._home_thread = threading.Thread(
                target=self._home_worker,
                name="cm5-rotor-home",
                daemon=True,
            )
            try:
                self._home_thread.start()
            except RuntimeError as exc:
                self._latch_fault(f"home-worker-start:{exc}")
                raise SensorFault("homing worker could not be started") from exc
        return {"accepted": True, "state": "HOMING", "timeoutPerAxisSeconds": HOME_TIMEOUT_S}

    def _home_worker(self) -> None:
        try:
            for axis in AXES:
                settings = self._settings.axes[axis]
                motor = self._motors[axis]
                with self._lock:
                    if self._stop_event.is_set() or self._home_cancel_event.is_set():
                        break
                    self._check_driver_health()
                    motor.move_velocity_degrees_s(
                        settings.home_direction * settings.home_speed_deg_s
                    )
                deadline = self._monotonic() + HOME_TIMEOUT_S
                while self._monotonic() < deadline:
                    if self._stop_event.is_set() or self._home_cancel_event.is_set():
                        break
                    snapshot = self._read_snapshot()
                    self._require_commissioning_sensors(snapshot)
                    self._check_driver_health()
                    pair = snapshot.limits.closed[axis]
                    if not pair[1 - settings.home_switch_index]:
                        raise SensorFault(f"{axis.upper()} opposite limit opened during homing")
                    if not pair[settings.home_switch_index]:
                        motor.stop_ramped()
                        with self._lock:
                            self._homed[axis] = True
                        break
                    time.sleep(HOME_POLL_S)
                else:
                    raise TimeoutError(f"{axis.upper()} homing exceeded {HOME_TIMEOUT_S:.0f} seconds")
                if self._home_cancel_event.is_set() or self._stop_event.is_set():
                    break
            with self._lock:
                if self._home_cancel_event.is_set() or self._stop_event.is_set():
                    self._state = "DISARMED"
                else:
                    self._state = "READY"
        except (OSError, TimeoutError, SensorFault, Tmc5160Fault, ValueError) as exc:
            with self._lock:
                self._fault = f"homing:{exc}"
                self._state = "FAULT"
                self._tracking = None
                self._homed = {axis: False for axis in AXES}
            try:
                self._power_gate.disable()
            except OSError as disable_exc:
                with self._lock:
                    self._fault = f"{self._fault};power-gate-disable:{disable_exc}"
        finally:
            failures = self._stop_motors()
            if failures:
                with self._lock:
                    self._fault = (
                        (self._fault or "homing-complete")
                        + ";stop-errors:"
                        + ";".join(failures)
                    )
                    self._state = "FAULT"
            if self._state == "HOMING":
                with self._lock:
                    self._fault = "homing-worker-exited-unexpectedly"
                    self._state = "FAULT"
                try:
                    self._power_gate.disable()
                except OSError as exc:
                    with self._lock:
                        self._fault = f"{self._fault};power-gate-disable:{exc}"
            elif self._fault is not None:
                try:
                    self._power_gate.disable()
                except OSError as exc:
                    with self._lock:
                        self._fault = f"{self._fault};power-gate-disable:{exc}"

    def _goto(self, data: Mapping[str, object]) -> dict[str, object]:
        targets = self._axis_values(
            {
                "az": data.get("azDeg"),
                "el": data.get("elDeg"),
                "pol": data.get("polDeg"),
            },
            "goto",
        )
        with self._lock:
            if self._state not in ("READY",):
                raise SensorFault(f"goto is not permitted while state is {self._state}")
            if self._thread is None or not self._thread.is_alive():
                raise SensorFault("rotor monitor/service loop is not running")
            snapshot = self._read_snapshot()
            self._require_motion_feedback(snapshot, self._monotonic())
            self._validate_targets(targets, snapshot)
            self._enable_power_gate()
            self._issue_targets(targets, snapshot)
            self._tracking = None
            self._state = "MOVING"
            self._move_started = self._monotonic()
        return {"accepted": True, "targetsDeg": targets}

    def _track(self, data: Mapping[str, object]) -> dict[str, object]:
        if set(data) != {"noradId"}:
            raise ValueError("track request must contain only a NORAD ID")
        norad_id = data["noradId"]
        if isinstance(norad_id, bool) or not isinstance(norad_id, int):
            raise ValueError("noradId must be an integer")
        with self._lock:
            if self._state not in ("READY", "TRACKING"):
                raise SensorFault(f"track is not permitted while state is {self._state}")
            if self._thread is None or not self._thread.is_alive():
                raise SensorFault("rotor monitor/service loop is not running")
            snapshot = self._read_snapshot()
            self._require_motion_feedback(snapshot, self._monotonic())
            if snapshot.gnss is None or not snapshot.gnss.fresh(
                self._monotonic(), GNSS_MAX_AGE_S
            ):
                raise StaleFixError("tracking requires a fresh GNSS fix")
            tle = self._catalog.get(norad_id)
            self._tracking = {
                "tle": tle,
                "azimuth": self._settings.axes["az"],
                "elevation": self._settings.axes["el"],
            }
            first = self._tracking_targets(snapshot, self._monotonic())
            self._validate_targets(first, snapshot)
            self._enable_power_gate()
            self._issue_targets(first, snapshot)
            self._targets.update(first)
            self._state = "TRACKING"
            self._last_track_update = self._monotonic()
        return {
            "accepted": True,
            "state": "TRACKING",
            "targetsDeg": first,
            "satellite": self._last_satellite_state,
        }

    def _tracking_targets(
        self, snapshot: SensorSnapshot, now_monotonic: float
    ) -> dict[str, float]:
        if self._tracking is None or self._calibration is None or snapshot.gnss is None:
            raise SensorFault("tracking state lacks TLE, calibration, or GNSS")
        if not snapshot.gnss.fresh(now_monotonic, GNSS_MAX_AGE_S):
            raise StaleFixError("GNSS site or UTC is stale")
        tle = self._tracking["tle"]
        if not isinstance(tle, Tle):
            raise SensorFault("tracking TLE state is invalid")
        site = Site(
            snapshot.gnss.latitude_deg,
            snapshot.gnss.longitude_deg,
            snapshot.gnss.altitude_m,
        )
        state = propagate(tle, snapshot.gnss.utc, site)
        self._last_satellite_state = {
            "noradId": state.norad_id,
            "name": state.name,
            "utc": state.utc.isoformat(),
            "latitudeDeg": state.latitude_deg,
            "longitudeDeg": state.longitude_deg,
            "altitudeKm": state.altitude_km,
            "azimuthDeg": state.azimuth_deg,
            "elevationDeg": state.elevation_deg,
            "rangeM": state.range_m,
            "rangeRateMps": state.range_rate_mps,
            "apparentTrackAngleDeg": state.apparent_track_angle_deg,
            "siteUtc": snapshot.gnss.utc.isoformat(),
            "gnssAgeMs": round(snapshot.gnss.age_s(now_monotonic) * 1000),
        }
        self._last_satellite_state["sampledMonotonic"] = now_monotonic
        if state.elevation_deg < ACQUISITION_ELEVATION_DEG:
            raise SensorFault(
                f"satellite is below the {ACQUISITION_ELEVATION_DEG:.0f}-degree acquisition limit"
            )
        if state.elevation_deg > ZENITH_GUARD_DEG:
            raise SensorFault("satellite is inside the 89-degree zenith guard")
        if state.apparent_track_angle_deg is None:
            raise SensorFault("SGP4 apparent track angle is undefined")
        az = self._mechanical_azimuth(state.azimuth_deg)
        el = state.elevation_deg
        pol = self._calibration.pol_offset_deg + state.apparent_track_angle_deg
        if self._calibration.pol_model == "cross-track":
            pol += 90
        pol = (pol + 180) % 360 - 180
        current_pol = self._position_from_encoder(
            "pol", snapshot.encoders["pol"]
        )
        pol = self._nearest_equivalent(pol, current_pol, self._settings.axes["pol"])
        return {"az": az, "el": el, "pol": pol}

    def _passes(self, data: Mapping[str, object]) -> dict[str, object]:
        if set(data) - {"noradId", "limit"} or "noradId" not in data:
            raise ValueError("passes requires noradId and optional limit")
        norad_id = data["noradId"]
        limit = data.get("limit", 10)
        if isinstance(norad_id, bool) or not isinstance(norad_id, int):
            raise ValueError("noradId must be an integer")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 20:
            raise ValueError("limit must be an integer in [1, 20]")
        with self._lock:
            if self._state not in ("DISARMED", "READY"):
                raise SensorFault("pass prediction runs only when rotor is idle")
        snapshot = self._read_snapshot()
        now = self._monotonic()
        if snapshot.gnss is None or not snapshot.gnss.fresh(now, GNSS_MAX_AGE_S):
            raise StaleFixError("pass prediction requires a fresh GNSS fix")
        tle = self._catalog.get(norad_id)
        site = Site(
            snapshot.gnss.latitude_deg,
            snapshot.gnss.longitude_deg,
            snapshot.gnss.altitude_m,
        )
        passes = predict_passes(
            tle,
            site,
            snapshot.gnss.utc,
            duration=timedelta(hours=24),
            limit=limit,
        )
        return {"noradId": norad_id, "passes": [self._pass_data(item) for item in passes]}

    def _mechanical_azimuth(self, true_azimuth_deg: float) -> float:
        if self._calibration is None:
            raise SensorFault("AZ base true heading is not calibrated")
        relative = (true_azimuth_deg - self._calibration.az_base_true_deg) % 360
        return self._nearest_equivalent(
            relative, self._last_positions.get("az"), self._settings.axes["az"]
        )

    @staticmethod
    def _nearest_equivalent(
        angle_deg: float,
        current_deg: float | None,
        settings: AxisSettings,
    ) -> float:
        candidates = [
            angle_deg + 360 * multiple
            for multiple in range(-2, 3)
            if settings.minimum_deg
            <= angle_deg + 360 * multiple
            <= settings.maximum_deg
        ]
        if not candidates:
            raise SensorFault("target has no cable-safe representation inside axis travel")
        reference = current_deg if current_deg is not None else (settings.minimum_deg + settings.maximum_deg) / 2
        return min(candidates, key=lambda value: abs(value - reference))

    def _validate_targets(
        self, targets: Mapping[str, float], snapshot: SensorSnapshot
    ) -> None:
        if set(targets) != set(AXES):
            raise ValueError("goto/track requires AZ, EL, and POL targets")
        for axis, target in targets.items():
            settings = self._settings.axes[axis]
            if not math.isfinite(target) or not settings.minimum_deg <= target <= settings.maximum_deg:
                raise ValueError(f"{axis.upper()} target is outside commissioned travel")
            position = self._position_from_encoder(axis, snapshot.encoders[axis])
            low_closed, high_closed = snapshot.limits.closed[axis]
            if target < position and not low_closed:
                raise SensorFault(f"{axis.upper()} minimum NC limit is active")
            if target > position and not high_closed:
                raise SensorFault(f"{axis.upper()} maximum NC limit is active")

    def _issue_targets(
        self, targets: Mapping[str, float], snapshot: SensorSnapshot
    ) -> None:
        try:
            for axis in AXES:
                zero = self._calibration.encoder_zero_deg[axis]
                relative_target = targets[axis] + zero
                self._motors[axis].move_to_degrees(relative_target)
                self._targets[axis] = targets[axis]
            self._move_started = self._monotonic()
        except (OSError, Tmc5160Fault, ValueError) as exc:
            self._latch_fault(f"command:{exc}")
            raise

    def _check_following_error(self, snapshot: SensorSnapshot, now: float) -> None:
        reached = True
        positions: dict[str, float] = {}
        for axis in AXES:
            current = self._position_from_encoder(axis, snapshot.encoders[axis])
            positions[axis] = current
            low_closed, high_closed = snapshot.limits.closed[axis]
            target = self._targets[axis]
            if not low_closed and (target is None or target <= current):
                raise SensorFault(f"{axis.upper()} minimum NC limit is active toward the commanded position")
            if not high_closed and (target is None or target >= current):
                raise SensorFault(f"{axis.upper()} maximum NC limit is active toward the commanded position")
            self._last_positions[axis] = current
            calibration = self._calibration
            if calibration is None:
                raise SensorFault("following-error check lost the calibration record")
            steps_per_revolution = self._settings.axes[
                axis
            ].microsteps_per_output_revolution
            encoder_position_steps = round(
                (current + calibration.encoder_zero_deg[axis])
                * steps_per_revolution
                / 360.0
            )
            motor_position_steps = self._motors[axis].position_steps()
            position_error_deg = (
                abs(encoder_position_steps - motor_position_steps)
                * 360.0
                / steps_per_revolution
            )
            if position_error_deg > self._settings.axes[axis].maximum_following_error_deg:
                raise SensorFault(f"{axis.upper()} encoder/driver position disagreement exceeded its limit")
        if now - self._move_started < 1.0:
            return
        for axis in AXES:
            target = self._targets[axis]
            if target is None:
                continue
            error = abs(target - positions[axis])
            status = self._motors[axis].driver_status()
            reached = reached and bool(status["rampStatus"] & (1 << 9))
            if error > self._settings.axes[axis].maximum_following_error_deg:
                if status["rampStatus"] & (1 << 9):
                    raise SensorFault(f"{axis.upper()} following error exceeded its limit")
                reached = False
        if reached:
            with self._lock:
                if self._state == "MOVING":
                    self._state = "READY"

    def _position_from_encoder(
        self, axis: str, reading: EncoderReading
    ) -> float:
        if self._calibration is None:
            raise SensorFault("encoder position requires local zero calibration")
        relative = (reading.angle_deg - self._calibration.encoder_zero_deg[axis]) % 360
        with self._lock:
            position = self._nearest_equivalent(
                relative,
                self._last_positions.get(axis),
                self._settings.axes[axis],
            )
            self._last_positions[axis] = position
        return position

    def _stop(self) -> dict[str, object]:
        with self._lock:
            homing = self._state == "HOMING"
            if homing:
                self._home_cancel_event.set()
                self._homed = {axis: False for axis in AXES}
                self._state = "DISARMED"
            self._tracking = None
            self._last_satellite_state = None
        failures = self._stop_motors()
        gate_error: OSError | None = None
        try:
            self._power_gate.disable()
        except OSError as exc:
            gate_error = exc
        if failures:
            self._latch_fault("stop-failed:" + ";".join(failures))
            raise Tmc5160Fault(self._fault or "driver stop failed")
        if gate_error is not None:
            self._latch_fault(f"stop-power-gate-failed:{gate_error}")
            raise OSError(self._fault or "power gate disable failed")
        with self._lock:
            if self._fault is None:
                self._state = (
                    "READY"
                    if not homing and all(self._homed.values())
                    else "DISARMED"
                )
            self._targets = {axis: None for axis in AXES}
        return {"stopped": True, "state": self._state}

    def _stop_motors(self) -> list[str]:
        errors: list[str] = []
        for axis, motor in self._motors.items():
            try:
                motor.stop_ramped()
            except (OSError, Tmc5160Fault) as exc:
                errors.append(f"{axis}:{exc}")
        return errors

    def _enable_power_gate(self) -> None:
        try:
            self._power_gate.enable()
        except OSError as exc:
            self._latch_fault(f"power-gate-enable:{exc}")
            raise

    def _latch_fault(self, reason: str) -> None:
        with self._lock:
            self._fault = reason
            self._state = "FAULT"
            self._tracking = None
            self._homed = {axis: False for axis in AXES}
        gate_error: str | None = None
        try:
            self._power_gate.disable()
        except OSError as exc:
            gate_error = f";power-gate-disable:{exc}"
        errors = self._stop_motors()
        if errors or gate_error:
            with self._lock:
                suffix = ";".join(errors)
                if gate_error:
                    suffix = suffix + gate_error
                self._fault = reason + ";shutdown-errors:" + suffix

    def _service_worker(self) -> None:
        try:
            while not self._stop_event.is_set():
                started = self._monotonic()
                self.service_once()
                elapsed = self._monotonic() - started
                self._stop_event.wait(max(0.0, SERVICE_PERIOD_S - elapsed))
        except (OSError, TimeoutError, SensorFault, Tmc5160Fault, TleError,
                PropagationError, StaleFixError, ValueError) as exc:
            self._latch_fault(f"service:{exc}")
        finally:
            if not self._stop_event.is_set() and self._fault is None:
                self._latch_fault("service-worker-exited-unexpectedly")
            elif self._fault is not None:
                try:
                    self._power_gate.disable()
                except OSError as exc:
                    with self._lock:
                        self._fault = f"{self._fault};power-gate-disable:{exc}"

    def _require_commissioning_sensors(self, snapshot: SensorSnapshot) -> None:
        now = self._monotonic()
        if not self._snapshot_healthy(
            snapshot,
            now,
            require_gnss=True,
            require_compass=(
                self._calibration is not None
                and self._calibration.compass is not None
            ),
        ):
            raise SensorFault("fresh GNSS, encoders, limits, E-stop, watchdog, IMU, and calibrated heading required")

    @staticmethod
    def _axis_values(value: object, name: str) -> dict[str, float]:
        if not isinstance(value, Mapping) or set(value) != set(AXES):
            raise ValueError(f"{name} must contain exactly az, el, and pol values")
        return {
            axis: RotorController._finite_number(value[axis], f"{name}.{axis}")
            for axis in AXES
        }

    @staticmethod
    def _finite_number(value: object, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite number")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"{name} must be finite")
        return number

    @staticmethod
    def _string(value: object, name: str, maximum: int) -> str:
        if not isinstance(value, str) or not value.strip() or len(value) > maximum:
            raise ValueError(f"{name} must contain 1..{maximum} characters")
        return value.strip()

    @classmethod
    def _vector(cls, value: object, name: str) -> tuple[float, float, float]:
        if not isinstance(value, (list, tuple)) or len(value) != 3:
            raise ValueError(f"{name} must contain exactly three values")
        return tuple(cls._finite_number(item, name) for item in value)

    @classmethod
    def _matrix(
        cls, value: object, name: str
    ) -> tuple[tuple[float, float, float], ...]:
        if not isinstance(value, (list, tuple)) or len(value) != 3:
            raise ValueError(f"{name} must be a 3 by 3 matrix")
        rows = tuple(cls._vector(row, name) for row in value)
        return rows

    @staticmethod
    def _pass_data(item: SatellitePass) -> dict[str, object]:
        return {
            "noradId": item.norad_id,
            "name": item.name,
            "aosUtc": item.aos_utc.isoformat(),
            "tcaUtc": item.tca_utc.isoformat(),
            "losUtc": item.los_utc.isoformat(),
            "maxElevationDeg": item.max_elevation_deg,
        }

    @staticmethod
    def _success(data: dict[str, object]) -> dict[str, object]:
        return {"ok": True, "data": data, "error": None}

    @staticmethod
    def _error(message: str) -> dict[str, object]:
        return {"ok": False, "data": None, "error": message}
