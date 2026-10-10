"""Timestamped sensor contracts and AS5600 encoders behind a TCA9548A mux."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import math
import threading
from typing import Protocol

from .gnss import GnssFix

ENCODER_MAX_AGE_S = 0.100
LIMIT_MAX_AGE_S = 0.050
ATTITUDE_MAX_AGE_S = 0.500
AS5600_ADDRESS = 0x36
AS5600_STATUS_REGISTER = 0x0B
AS5600_RAW_ANGLE_REGISTER = 0x0C
TCA9548A_ADDRESS = 0x70


class SensorFault(RuntimeError):
    """A required sensor is absent, invalid, or stale."""


class I2cBus(Protocol):
    def write_byte(self, address: int, value: int) -> None: ...

    def read_i2c_block_data(self, address: int, register: int, length: int) -> list[int]: ...


class LinuxSmbus:
    """Real Linux I2C adapter; bus number must come from the verified carrier."""

    def __init__(self, bus_number: int) -> None:
        if isinstance(bus_number, bool) or not isinstance(bus_number, int) or bus_number < 0:
            raise ValueError("Linux I2C bus number must be explicit and nonnegative")
        try:
            from smbus2 import SMBus
        except ImportError as exc:
            raise RuntimeError("smbus2 is required for physical rotor I2C access") from exc
        self._bus = SMBus(bus_number)

    def write_byte(self, address: int, value: int) -> None:
        self._bus.write_byte(address, value)

    def read_i2c_block_data(self, address: int, register: int, length: int) -> list[int]:
        return self._bus.read_i2c_block_data(address, register, length)

    def close(self) -> None:
        self._bus.close()


@dataclass(frozen=True)
class EncoderReading:
    axis: str
    channel: int
    raw_angle: int
    angle_deg: float
    magnet_detected: bool
    magnet_too_strong: bool
    magnet_too_weak: bool
    monotonic_received: float

    def age_s(self, now_monotonic: float) -> float:
        age = now_monotonic - self.monotonic_received
        return age if math.isfinite(age) and age >= 0 else math.inf

    def valid(self, now_monotonic: float, max_age_s: float = ENCODER_MAX_AGE_S) -> bool:
        return (
            0 <= self.raw_angle <= 4095
            and 0 <= self.angle_deg < 360
            and self.magnet_detected
            and not self.magnet_too_strong
            and not self.magnet_too_weak
            and self.age_s(now_monotonic) <= max_age_s
        )


@dataclass(frozen=True)
class LimitSnapshot:
    closed: dict[str, tuple[bool, bool]]
    monotonic_received: float

    def healthy(self, now_monotonic: float) -> bool:
        age = now_monotonic - self.monotonic_received
        return (
            math.isfinite(age)
            and 0 <= age <= LIMIT_MAX_AGE_S
            and set(self.closed) == {"az", "el", "pol"}
            and all(len(pair) == 2 and any(pair) for pair in self.closed.values())
        )


@dataclass(frozen=True)
class ImuReading:
    roll_deg: float
    pitch_deg: float
    acceleration_mps2: tuple[float, float, float]
    monotonic_received: float

    def valid(self, now_monotonic: float) -> bool:
        age = now_monotonic - self.monotonic_received
        values = (self.roll_deg, self.pitch_deg, *self.acceleration_mps2)
        acceleration = math.sqrt(sum(value * value for value in self.acceleration_mps2))
        return (
            math.isfinite(age)
            and 0 <= age <= ATTITUDE_MAX_AGE_S
            and all(math.isfinite(value) for value in values)
            and 7.0 <= acceleration <= 12.5
            and -90 <= self.roll_deg <= 90
            and -90 <= self.pitch_deg <= 90
        )


@dataclass(frozen=True)
class MagnetometerReading:
    magnetic_uT: tuple[float, float, float]
    monotonic_received: float

    def valid(self, now_monotonic: float) -> bool:
        age = now_monotonic - self.monotonic_received
        magnitude = math.sqrt(sum(value * value for value in self.magnetic_uT))
        return (
            math.isfinite(age)
            and 0 <= age <= ATTITUDE_MAX_AGE_S
            and all(math.isfinite(value) for value in self.magnetic_uT)
            and math.isfinite(magnitude)
            and 5 <= magnitude <= 200
        )


@dataclass(frozen=True)
class CompassCalibration:
    hard_iron_uT: tuple[float, float, float]
    soft_iron_matrix: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]
    sensor_to_base: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]
    declination_deg: float
    declination_source: str
    declination_date: str
    calibrated_utc: datetime

    def __post_init__(self) -> None:
        if len(self.hard_iron_uT) != 3 or not all(
            math.isfinite(value) and abs(value) <= 1000 for value in self.hard_iron_uT
        ):
            raise ValueError("hard-iron offset must contain three finite microtesla values")
        if not math.isfinite(self.declination_deg) or not -180 <= self.declination_deg <= 180:
            raise ValueError("declination must be explicitly supplied in [-180, 180]")
        if not self.declination_source or len(self.declination_source) > 128:
            raise ValueError("declination source is required")
        if not self.declination_date or len(self.declination_date) > 32:
            raise ValueError("declination source date is required")
        if (
            self.calibrated_utc.tzinfo is None
            or self.calibrated_utc.utcoffset() is None
        ):
            raise ValueError("compass calibration time must be timezone-aware")
        for matrix in (self.soft_iron_matrix, self.sensor_to_base):
            if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
                raise ValueError("compass matrices must be 3 by 3")
            if not all(math.isfinite(value) for row in matrix for value in row):
                raise ValueError("compass matrix values must be finite")
        if any(abs(value) > 10 for row in self.soft_iron_matrix for value in row):
            raise ValueError("soft-iron matrix coefficient is out of range")
        determinant = _determinant(self.soft_iron_matrix)
        if determinant <= 1e-4:
            raise ValueError("soft-iron calibration matrix must be nonsingular and positive")
        for i in range(3):
            for j in range(3):
                dot = sum(self.sensor_to_base[i][k] * self.sensor_to_base[j][k] for k in range(3))
                if abs(dot - (1.0 if i == j else 0.0)) > 1e-3:
                    raise ValueError("sensor-to-base matrix must be orthonormal")
        if abs(_determinant(self.sensor_to_base) - 1.0) > 1e-3:
            raise ValueError("sensor-to-base matrix must preserve handedness")


@dataclass(frozen=True)
class HeadingReading:
    magnetic_deg: float
    true_deg: float
    declination_deg: float
    declination_source: str
    declination_date: str
    monotonic_received: float


def tilt_compensated_true_heading(
    magnetometer: MagnetometerReading,
    imu: ImuReading,
    calibration: CompassCalibration,
    now_monotonic: float,
) -> HeadingReading:
    if not magnetometer.valid(now_monotonic):
        raise SensorFault("magnetometer reading is stale or invalid")
    if not imu.valid(now_monotonic):
        raise SensorFault("accelerometer/IMU reading is stale or invalid")
    corrected = tuple(
        magnetometer.magnetic_uT[index] - calibration.hard_iron_uT[index]
        for index in range(3)
    )
    calibrated = tuple(
        sum(calibration.soft_iron_matrix[row][col] * corrected[col] for col in range(3))
        for row in range(3)
    )
    body = tuple(
        sum(calibration.sensor_to_base[row][col] * calibrated[col] for col in range(3))
        for row in range(3)
    )
    ax, ay, az = imu.acceleration_mps2
    roll = math.atan2(ay, az)
    pitch = math.atan2(-ax, math.hypot(ay, az))
    sin_roll, cos_roll = math.sin(roll), math.cos(roll)
    sin_pitch, cos_pitch = math.sin(pitch), math.cos(pitch)
    horizontal_north = cos_pitch * body[0] + sin_pitch * (
        sin_roll * body[1] + cos_roll * body[2]
    )
    horizontal_east = cos_roll * body[1] - sin_roll * body[2]
    if math.hypot(horizontal_north, horizontal_east) < 1e-6:
        raise SensorFault("tilt-compensated horizontal magnetic field is invalid")
    magnetic = math.degrees(math.atan2(-horizontal_east, horizontal_north)) % 360
    true = (magnetic + calibration.declination_deg) % 360
    return HeadingReading(
        magnetic_deg=magnetic,
        true_deg=true,
        declination_deg=calibration.declination_deg,
        declination_source=calibration.declination_source,
        declination_date=calibration.declination_date,
        monotonic_received=min(
            magnetometer.monotonic_received, imu.monotonic_received
        ),
    )


def _determinant(matrix: tuple[tuple[float, float, float], ...]) -> float:
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


@dataclass(frozen=True)
class SensorSnapshot:
    encoders: dict[str, EncoderReading]
    limits: LimitSnapshot | None
    gnss: GnssFix | None
    imu: ImuReading | None
    magnetometer: MagnetometerReading | None
    estop_healthy: bool | None
    watchdog_healthy: bool | None
    motor_permit_healthy: bool | None = None
    driver_faults_clear: dict[str, bool] | None = None
    interlock_monotonic_received: float | None = None

    def interlocks_healthy(self, now_monotonic: float) -> bool:
        """Require fresh BSP-translated physical permit and active-low fault inputs."""
        sampled = self.interlock_monotonic_received
        faults = self.driver_faults_clear
        if (
            sampled is None
            or not math.isfinite(sampled)
            or not math.isfinite(now_monotonic)
            or now_monotonic < sampled
            or now_monotonic - sampled > LIMIT_MAX_AGE_S
        ):
            return False
        return (
            self.estop_healthy is True
            and self.watchdog_healthy is True
            and self.motor_permit_healthy is True
            and faults is not None
            and set(faults) == {"az", "el", "pol"}
            and all(faults[axis] is True for axis in ("az", "el", "pol"))
        )


class SensorInputs(Protocol):
    """Production sensor adapter; missing hardware must be represented as absent."""

    def read_snapshot(self, monotonic_now: float) -> SensorSnapshot: ...


class Tca9548a:
    """Single-channel-select TCA9548A driver for the three encoder branches."""

    def __init__(self, bus: I2cBus, address: int = TCA9548A_ADDRESS) -> None:
        if not 0x70 <= address <= 0x77:
            raise ValueError("TCA9548A address must be in [0x70, 0x77]")
        self._bus = bus
        self.address = address

    def select(self, channel: int) -> None:
        if channel not in (0, 1, 2):
            raise ValueError("rotor encoder channel must be 0, 1, or 2")
        self._bus.write_byte(self.address, 1 << channel)


class As5600EncoderBank:
    """Reads one AS5600 per selected TCA9548A branch; never invents an angle."""

    def __init__(
        self,
        bus: I2cBus,
        *,
        mux_address: int = TCA9548A_ADDRESS,
        axis_channels: dict[str, int] | None = None,
    ) -> None:
        channels = axis_channels or {"az": 0, "el": 1, "pol": 2}
        if set(channels) != {"az", "el", "pol"}:
            raise ValueError("exactly az, el, and pol encoder channels are required")
        if len(set(channels.values())) != 3 or any(
            channel not in (0, 1, 2) for channel in channels.values()
        ):
            raise ValueError("AZ, EL, and POL must use distinct mux channels 0, 1, and 2")
        self._bus = bus
        self._mux = Tca9548a(bus, mux_address)
        self._channels = dict(channels)
        self._lock = threading.Lock()

    def read_all(self, monotonic_now: float) -> dict[str, EncoderReading]:
        if not math.isfinite(monotonic_now):
            raise ValueError("monotonic_now must be finite")
        readings: dict[str, EncoderReading] = {}
        with self._lock:
            for axis in ("az", "el", "pol"):
                channel = self._channels[axis]
                self._mux.select(channel)
                raw = self._bus.read_i2c_block_data(
                    AS5600_ADDRESS, AS5600_STATUS_REGISTER, 3
                )
                if len(raw) != 3 or any(not 0 <= item <= 0xFF for item in raw):
                    raise SensorFault(f"{axis.upper()} encoder returned an invalid I2C frame")
                status, angle_high, angle_low = raw
                angle = ((angle_high & 0x0F) << 8) | angle_low
                readings[axis] = EncoderReading(
                    axis=axis,
                    channel=channel,
                    raw_angle=angle,
                    angle_deg=angle * (360.0 / 4096.0),
                    magnet_detected=bool(status & (1 << 5)),
                    magnet_too_strong=bool(status & (1 << 3)),
                    magnet_too_weak=bool(status & (1 << 4)),
                    monotonic_received=monotonic_now,
                )
        return readings
