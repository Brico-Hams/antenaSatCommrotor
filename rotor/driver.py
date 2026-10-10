"""TMC5160 SPI register access and autonomous position-ramp commands."""

from __future__ import annotations

import math
import threading
from typing import Protocol


SPI_FRAME_BYTES = 5
TMC5160_VERSION = 0x30
TMC5160_REG_IOIN = 0x04
TMC5160_REG_GSTAT = 0x01
TMC5160_REG_RAMPMODE = 0x20
TMC5160_REG_XACTUAL = 0x21
TMC5160_REG_VMAX = 0x27
TMC5160_REG_AMAX = 0x26
TMC5160_REG_DMAX = 0x28
TMC5160_REG_XTARGET = 0x2D
TMC5160_REG_RAMP_STAT = 0x35
TMC5160_REG_DRV_STATUS = 0x6F
RAMP_MODE_POSITION = 0
RAMP_MODE_VELOCITY_POSITIVE = 1
RAMP_MODE_VELOCITY_NEGATIVE = 2
RAMP_MODE_HOLD = 3
REGISTER_VELOCITY_MAX = 0x7FFFFF
CM5_SPI1_BUS = 1
CM5_SPI1_CHIP_SELECT_BCM_GPIO = {0: 18, 1: 17, 2: 16}
CM5_SPI1_AXIS_CHIP_SELECT = {"az": 0, "el": 1, "pol": 2}


class SpiTransport(Protocol):
    def transfer(self, frame: bytes) -> bytes: ...


class Tmc5160Fault(RuntimeError):
    """TMC5160 identity, SPI protocol, ramp, or register fault."""


class Tmc5160Spi:
    """A serialized TMC5160 bus; each transfer is exactly one 40-bit datagram."""

    def __init__(self, transport: SpiTransport) -> None:
        self._transport = transport
        self._lock = threading.Lock()

    def read_register(self, address: int) -> tuple[int, int]:
        address = self._address(address)
        frame = bytes((address, 0, 0, 0, 0))
        with self._lock:
            self._checked_transfer(frame)
            response = self._checked_transfer(frame)
        return response[0], int.from_bytes(response[1:], "big")

    def write_register(self, address: int, value: int) -> int:
        address = self._address(address)
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 0xFFFFFFFF:
            raise ValueError("register value must be an unsigned 32-bit integer")
        frame = bytes((address | 0x80,)) + value.to_bytes(4, "big")
        with self._lock:
            response = self._checked_transfer(frame)
        return response[0]

    @staticmethod
    def _address(address: int) -> int:
        if isinstance(address, bool) or not isinstance(address, int) or not 0 <= address <= 0x7F:
            raise ValueError("TMC5160 register address must be in [0, 0x7f]")
        return address

    def _checked_transfer(self, frame: bytes) -> bytes:
        response = self._transport.transfer(frame)
        if not isinstance(response, bytes) or len(response) != SPI_FRAME_BYTES:
            raise Tmc5160Fault("TMC5160 SPI transfer did not return exactly five bytes")
        return response


class LinuxSpidevTransport:
    """Linux spidev transport; electrical routing remains a carrier configuration."""

    def __init__(
        self,
        bus_number: int,
        chip_select: int,
        *,
        spi_hz: int,
        spi_mode: int,
    ) -> None:
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0
            for value in (bus_number, chip_select)
        ):
            raise ValueError("SPI bus and chip-select numbers must be nonnegative integers")
        if not isinstance(spi_hz, int) or isinstance(spi_hz, bool) or not 1_000 <= spi_hz <= 10_000_000:
            raise ValueError("SPI clock must be explicitly set in [1 kHz, 10 MHz]")
        if spi_mode not in (0, 3):
            raise ValueError("TMC5160 supports only the documented SPI mode 0 or 3")
        try:
            import spidev
        except ImportError as exc:
            raise RuntimeError("spidev is required for physical Linux rotor access") from exc
        device = spidev.SpiDev()
        device.open(bus_number, chip_select)
        device.mode = spi_mode
        device.max_speed_hz = spi_hz
        self._device = device
        self._lock = threading.Lock()

    @classmethod
    def for_cm5_spi1(
        cls,
        chip_select: int,
        *,
        spi_hz: int,
        spi_mode: int,
    ) -> LinuxSpidevTransport:
        """Open one CM5 SPI1 CS; axis-to-CS assignment is supplied by the carrier."""
        if (
            isinstance(chip_select, bool)
            or not isinstance(chip_select, int)
            or chip_select not in CM5_SPI1_CHIP_SELECT_BCM_GPIO
        ):
            raise ValueError("CM5 SPI1 chip-select must be 0, 1, or 2")
        return cls(
            CM5_SPI1_BUS,
            chip_select,
            spi_hz=spi_hz,
            spi_mode=spi_mode,
        )

    @classmethod
    def for_cm5_axis(
        cls,
        axis: str,
        *,
        spi_hz: int,
        spi_mode: int,
    ) -> LinuxSpidevTransport:
        """Open the revision-A SPI1 chip-select assigned to an axis."""
        if not isinstance(axis, str) or axis.lower() not in CM5_SPI1_AXIS_CHIP_SELECT:
            raise ValueError("CM5 SPI1 axis must be az, el, or pol")
        return cls.for_cm5_spi1(
            CM5_SPI1_AXIS_CHIP_SELECT[axis.lower()],
            spi_hz=spi_hz,
            spi_mode=spi_mode,
        )

    def transfer(self, frame: bytes) -> bytes:
        if len(frame) != SPI_FRAME_BYTES:
            raise ValueError("TMC5160 SPI frame must be exactly five bytes")
        with self._lock:
            return bytes(self._device.xfer2(list(frame)))

    def close(self) -> None:
        with self._lock:
            self._device.close()


class Tmc5160Axis:
    """One TMC5160 internal-ramp axis with explicit clock/mechanics parameters."""

    def __init__(
        self,
        spi: Tmc5160Spi,
        *,
        clock_hz: int,
        microsteps_per_output_revolution: int,
        max_velocity_deg_s: float,
        acceleration_deg_s2: float,
        deceleration_deg_s2: float,
        expected_version: int = TMC5160_VERSION,
    ) -> None:
        if isinstance(clock_hz, bool) or not isinstance(clock_hz, int) or clock_hz <= 0:
            raise ValueError("TMC5160 clock_hz must be an explicit positive integer")
        if (
            isinstance(microsteps_per_output_revolution, bool)
            or not isinstance(microsteps_per_output_revolution, int)
            or microsteps_per_output_revolution <= 0
        ):
            raise ValueError("output microstep resolution must be a positive integer")
        for name, value in (
            ("max_velocity_deg_s", max_velocity_deg_s),
            ("acceleration_deg_s2", acceleration_deg_s2),
            ("deceleration_deg_s2", deceleration_deg_s2),
        ):
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")
        if expected_version != TMC5160_VERSION:
            raise ValueError("unexpected expected chip version")
        self._spi = spi
        self.clock_hz = clock_hz
        self.microsteps_per_output_revolution = microsteps_per_output_revolution
        self.max_velocity_deg_s = max_velocity_deg_s
        self.acceleration_deg_s2 = acceleration_deg_s2
        self.deceleration_deg_s2 = deceleration_deg_s2
        self._verified = False
        self._lock = threading.RLock()

    def verify_identity(self) -> None:
        _, ioin = self._spi.read_register(TMC5160_REG_IOIN)
        version = (ioin >> 24) & 0xFF
        if version != TMC5160_VERSION:
            self._verified = False
            raise Tmc5160Fault(
                f"TMC5160 IOIN version mismatch: expected 0x{TMC5160_VERSION:02x}, got 0x{version:02x}"
            )
        self._verified = True

    def position_steps(self) -> int:
        self._require_verified()
        _, raw = self._spi.read_register(TMC5160_REG_XACTUAL)
        return raw - (1 << 32) if raw & 0x80000000 else raw

    def set_position_degrees(self, position_deg: float) -> int:
        self._require_verified()
        if not math.isfinite(position_deg):
            raise ValueError("axis position must be finite")
        steps = round(
            position_deg * self.microsteps_per_output_revolution / 360.0
        )
        if not -(1 << 31) <= steps < (1 << 31):
            raise ValueError("axis position exceeds TMC5160 signed position range")
        self._spi.write_register(TMC5160_REG_XACTUAL, steps & 0xFFFFFFFF)
        if self.position_steps() != steps:
            raise Tmc5160Fault("TMC5160 XACTUAL readback did not match calibration")
        return steps

    def driver_status(self) -> dict[str, int]:
        self._require_verified()
        status, ramp = self._spi.read_register(TMC5160_REG_RAMP_STAT)
        driver_status, driver = self._spi.read_register(TMC5160_REG_DRV_STATUS)
        global_status, global_faults = self._spi.read_register(TMC5160_REG_GSTAT)
        return {
            "spiStatus": status,
            "rampStatus": ramp,
            "driverSpiStatus": driver_status,
            "driverStatus": driver,
            "globalSpiStatus": global_status,
            "globalStatus": global_faults,
        }

    def move_to_degrees(self, target_deg: float) -> int:
        self._require_verified()
        if not math.isfinite(target_deg):
            raise ValueError("axis target must be finite")
        target_steps = round(
            target_deg * self.microsteps_per_output_revolution / 360.0
        )
        if not -(1 << 31) <= target_steps < (1 << 31):
            raise ValueError("axis target exceeds TMC5160 signed position range")
        vmax = self.velocity_register(self.max_velocity_deg_s)
        amax = self.acceleration_register(self.acceleration_deg_s2)
        dmax = self.acceleration_register(self.deceleration_deg_s2)
        with self._lock:
            self._spi.write_register(TMC5160_REG_AMAX, amax)
            self._spi.write_register(TMC5160_REG_DMAX, dmax)
            self._spi.write_register(TMC5160_REG_VMAX, vmax)
            self._spi.write_register(TMC5160_REG_RAMPMODE, RAMP_MODE_POSITION)
            self._spi.write_register(TMC5160_REG_XTARGET, target_steps & 0xFFFFFFFF)
        return target_steps

    def stop_ramped(self) -> None:
        self._require_verified()
        with self._lock:
            self._spi.write_register(TMC5160_REG_RAMPMODE, RAMP_MODE_HOLD)

    def move_velocity_degrees_s(self, speed_deg_s: float) -> int:
        self._require_verified()
        if not math.isfinite(speed_deg_s) or speed_deg_s == 0:
            raise ValueError("velocity must be finite and nonzero")
        magnitude = abs(speed_deg_s)
        vmax = self.velocity_register(magnitude)
        amax = self.acceleration_register(self.acceleration_deg_s2)
        dmax = self.acceleration_register(self.deceleration_deg_s2)
        mode = (
            RAMP_MODE_VELOCITY_POSITIVE
            if speed_deg_s > 0
            else RAMP_MODE_VELOCITY_NEGATIVE
        )
        with self._lock:
            self._spi.write_register(TMC5160_REG_AMAX, amax)
            self._spi.write_register(TMC5160_REG_DMAX, dmax)
            self._spi.write_register(TMC5160_REG_VMAX, vmax)
            self._spi.write_register(TMC5160_REG_RAMPMODE, mode)
        return mode

    def hold(self) -> None:
        self._require_verified()
        with self._lock:
            self._spi.write_register(TMC5160_REG_RAMPMODE, RAMP_MODE_HOLD)

    def velocity_register(self, speed_deg_s: float) -> int:
        if not math.isfinite(speed_deg_s) or not 0 < speed_deg_s <= self.max_velocity_deg_s:
            raise ValueError("requested axis speed is outside its configured safe range")
        microsteps_per_second = (
            speed_deg_s * self.microsteps_per_output_revolution / 360.0
        )
        # TMC5160 datasheet velocity unit: V[steps/s] = VMAX * fCLK / 2^24.
        register = round(microsteps_per_second * (1 << 24) / self.clock_hz)
        if not 0 < register <= REGISTER_VELOCITY_MAX:
            raise ValueError("requested speed cannot be represented by TMC5160 VMAX")
        return register

    def acceleration_register(self, acceleration_deg_s2: float) -> int:
        if not math.isfinite(acceleration_deg_s2) or acceleration_deg_s2 <= 0:
            raise ValueError("axis acceleration must be finite and positive")
        microsteps_per_second_sq = (
            acceleration_deg_s2 * self.microsteps_per_output_revolution / 360.0
        )
        register = round(microsteps_per_second_sq * (1 << 41) / self.clock_hz**2)
        if not 0 < register <= 0xFFFF:
            raise ValueError("requested acceleration cannot be represented by TMC5160 AMAX")
        return register

    def _require_verified(self) -> None:
        if not self._verified:
            raise Tmc5160Fault("TMC5160 identity has not been verified")
