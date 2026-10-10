"""Checksum-validated NMEA RMC/GGA parsing and coherent fresh-fix assembly."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
import math
import time as monotonic_time


MAX_FIX_AGE_S = 10.0
PAIR_TOLERANCE_S = 1.0


class NmeaError(ValueError):
    """An NMEA sentence is malformed, unsupported, or has a bad checksum."""


class StaleFixError(RuntimeError):
    """No fresh, coherent, valid GNSS fix is available."""


@dataclass(frozen=True)
class Rmc:
    utc_time: time
    fix_date: date
    valid: bool
    latitude_deg: float | None
    longitude_deg: float | None


@dataclass(frozen=True)
class Gga:
    utc_time: time
    fix_quality: int
    satellites: int
    latitude_deg: float | None
    longitude_deg: float | None
    altitude_m: float | None


@dataclass(frozen=True)
class GnssFix:
    utc: datetime
    latitude_deg: float
    longitude_deg: float
    altitude_m: float
    fix_quality: int
    satellites: int
    monotonic_received: float

    def age_s(self, now_monotonic: float) -> float:
        age = now_monotonic - self.monotonic_received
        if not math.isfinite(age) or age < 0:
            return math.inf
        return age

    def fresh(self, now_monotonic: float, max_age_s: float = MAX_FIX_AGE_S) -> bool:
        return 0 <= self.age_s(now_monotonic) <= max_age_s


def _utc_time(value: str) -> time:
    if len(value) < 6:
        raise NmeaError("NMEA UTC time is truncated")
    try:
        hour = int(value[0:2])
        minute = int(value[2:4])
        seconds = float(value[4:])
    except ValueError as exc:
        raise NmeaError("NMEA UTC time is not numeric") from exc
    if not math.isfinite(seconds) or not 0 <= seconds < 60:
        raise NmeaError("NMEA UTC seconds are out of range")
    whole = int(seconds)
    microsecond = int((seconds - whole) * 1_000_000)
    try:
        parsed = datetime(2000, 1, 1, hour, minute, whole, microsecond, tzinfo=timezone.utc)
    except ValueError as exc:
        raise NmeaError("NMEA UTC time is out of range") from exc
    return parsed.timetz().replace(tzinfo=None)


def _coordinate(value: str, hemisphere: str, degree_digits: int) -> float:
    if not value or len(value) <= degree_digits:
        raise NmeaError("NMEA coordinate is missing")
    try:
        degrees = int(value[:degree_digits])
        minutes = float(value[degree_digits:])
    except ValueError as exc:
        raise NmeaError("NMEA coordinate is not numeric") from exc
    if not math.isfinite(minutes) or not 0 <= minutes < 60:
        raise NmeaError("NMEA coordinate minutes are out of range")
    maximum = 90 if degree_digits == 2 else 180
    if degrees > maximum or (degrees == maximum and minutes != 0):
        raise NmeaError("NMEA coordinate is out of range")
    result = degrees + minutes / 60
    if hemisphere in ("S", "W"):
        result = -result
    elif hemisphere not in ("N", "E"):
        raise NmeaError("NMEA coordinate hemisphere is invalid")
    return result


def parse_rmc(line: str) -> Rmc:
    fields = parse_sentence(line)
    if not fields[0].endswith("RMC") or len(fields) < 10:
        raise NmeaError("Expected a complete RMC sentence")
    utc_time = _utc_time(fields[1])
    status = fields[2]
    if status not in ("A", "V"):
        raise NmeaError("RMC status is invalid")
    valid = status == "A"
    latitude = _coordinate(fields[3], fields[4], 2) if valid else None
    longitude = _coordinate(fields[5], fields[6], 3) if valid else None
    date_field = fields[9]
    if len(date_field) != 6 or not date_field.isdigit():
        raise NmeaError("RMC date is invalid")
    day, month, year2 = int(date_field[:2]), int(date_field[2:4]), int(date_field[4:])
    year = 2000 + year2 if year2 < 80 else 1900 + year2
    try:
        fix_date = date(year, month, day)
    except ValueError as exc:
        raise NmeaError("RMC date is out of range") from exc
    return Rmc(utc_time, fix_date, valid, latitude, longitude)


def parse_gga(line: str) -> Gga:
    fields = parse_sentence(line)
    if not fields[0].endswith("GGA") or len(fields) < 12:
        raise NmeaError("Expected a complete GGA sentence")
    utc_time = _utc_time(fields[1])
    try:
        quality = int(fields[6])
        satellites = int(fields[7])
    except ValueError as exc:
        raise NmeaError("GGA quality/satellite count is not numeric") from exc
    if quality < 0 or satellites < 0:
        raise NmeaError("GGA quality/satellite count is negative")
    if quality == 0:
        return Gga(utc_time, quality, satellites, None, None, None)
    latitude = _coordinate(fields[2], fields[3], 2)
    longitude = _coordinate(fields[4], fields[5], 3)
    if fields[10] != "M":
        raise NmeaError("GGA altitude must be expressed in metres")
    try:
        altitude = float(fields[9])
    except ValueError as exc:
        raise NmeaError("GGA altitude is not numeric") from exc
    if not math.isfinite(altitude) or not -1000 <= altitude <= 100_000:
        raise NmeaError("GGA altitude is out of range")
    return Gga(utc_time, quality, satellites, latitude, longitude, altitude)


def parse_sentence(line: str) -> list[str]:
    text = line.strip()
    if not text.startswith("$") or "*" not in text:
        raise NmeaError("NMEA sentence must start with '$' and include a checksum")
    payload, checksum_text = text[1:].rsplit("*", 1)
    if len(checksum_text) != 2:
        raise NmeaError("NMEA checksum must be two hexadecimal digits")
    try:
        supplied = int(checksum_text, 16)
    except ValueError as exc:
        raise NmeaError("NMEA checksum is not hexadecimal") from exc
    checksum = 0
    for char in payload:
        code = ord(char)
        if code > 0x7F:
            raise NmeaError("NMEA sentence must be ASCII")
        checksum ^= code
    if checksum != supplied:
        raise NmeaError("NMEA checksum mismatch")
    fields = payload.split(",")
    if not fields[0] or len(fields[0]) != 5:
        raise NmeaError("NMEA sentence identifier is invalid")
    return fields


class GnssFixAssembler:
    """Combines current valid RMC and GGA records; never fabricates a fix."""

    def __init__(
        self,
        *,
        max_age_s: float = MAX_FIX_AGE_S,
        pair_tolerance_s: float = PAIR_TOLERANCE_S,
    ) -> None:
        if not math.isfinite(max_age_s) or not 0 < max_age_s <= MAX_FIX_AGE_S:
            raise ValueError("max_age_s must be in (0, 10]")
        if not math.isfinite(pair_tolerance_s) or not 0 <= pair_tolerance_s <= 2:
            raise ValueError("pair_tolerance_s must be in [0, 2]")
        self._max_age_s = max_age_s
        self._pair_tolerance_s = pair_tolerance_s
        self._rmc: tuple[Rmc, float] | None = None
        self._gga: tuple[Gga, float] | None = None
        self._fix: GnssFix | None = None

    def feed(self, line: str, monotonic_received: float) -> GnssFix | None:
        if not math.isfinite(monotonic_received):
            raise ValueError("monotonic_received must be finite")
        fields = parse_sentence(line)
        sentence_type = fields[0][-3:]
        if sentence_type == "RMC":
            rmc = parse_rmc(line)
            self._rmc = (rmc, monotonic_received)
            if not rmc.valid:
                self._fix = None
                return None
        elif sentence_type == "GGA":
            gga = parse_gga(line)
            self._gga = (gga, monotonic_received)
            if gga.fix_quality == 0:
                self._fix = None
                return None
        else:
            return None
        self._fix = self._assemble()
        return self._fix

    def current(self, now_monotonic: float) -> GnssFix:
        if not math.isfinite(now_monotonic):
            raise ValueError("now_monotonic must be finite")
        if self._fix is None or not self._fix.fresh(now_monotonic, self._max_age_s):
            raise StaleFixError("no fresh coherent GNSS RMC/GGA fix")
        return self._fix

    def _assemble(self) -> GnssFix | None:
        if self._rmc is None or self._gga is None:
            return None
        rmc, rmc_received = self._rmc
        gga, gga_received = self._gga
        if not rmc.valid or gga.fix_quality == 0:
            return None
        if abs((rmc_received - gga_received)) > self._pair_tolerance_s:
            return None
        time_delta = abs(
            (
                datetime.combine(date.min, rmc.utc_time)
                - datetime.combine(date.min, gga.utc_time)
            ).total_seconds()
        )
        time_delta = min(time_delta, 86_400 - time_delta)
        if time_delta > self._pair_tolerance_s:
            return None
        if (
            rmc.latitude_deg is None
            or rmc.longitude_deg is None
            or gga.latitude_deg is None
            or gga.longitude_deg is None
            or gga.altitude_m is None
        ):
            return None
        if abs(rmc.latitude_deg - gga.latitude_deg) > 0.002:
            return None
        longitude_delta = abs(rmc.longitude_deg - gga.longitude_deg)
        longitude_delta = min(longitude_delta, 360 - longitude_delta)
        if longitude_delta > 0.002:
            return None
        utc = datetime.combine(rmc.fix_date, rmc.utc_time, tzinfo=timezone.utc)
        received = max(rmc_received, gga_received)
        return GnssFix(
            utc=utc,
            latitude_deg=gga.latitude_deg,
            longitude_deg=gga.longitude_deg,
            altitude_m=gga.altitude_m,
            fix_quality=gga.fix_quality,
            satellites=gga.satellites,
            monotonic_received=received,
        )


class LinuxNmeaReceiver:
    """Real serial NMEA input; port, rate, and timeout must be board-configured."""

    def __init__(
        self,
        port: str,
        *,
        baudrate: int,
        timeout_s: float = 0.1,
        assembler: GnssFixAssembler | None = None,
    ) -> None:
        if not port or not isinstance(port, str):
            raise ValueError("GNSS serial port must be explicitly configured")
        if isinstance(baudrate, bool) or not isinstance(baudrate, int) or baudrate <= 0:
            raise ValueError("GNSS baudrate must be explicitly configured")
        if not math.isfinite(timeout_s) or not 0 < timeout_s <= 1:
            raise ValueError("GNSS serial timeout must be in (0, 1] seconds")
        try:
            import serial
        except ImportError as exc:
            raise RuntimeError("pyserial is required for physical GNSS serial access") from exc
        self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout_s)
        self._assembler = assembler or GnssFixAssembler()

    def poll(self) -> GnssFix | None:
        raw = self._serial.readline()
        if not raw:
            return None
        try:
            line = raw.decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise NmeaError("GNSS serial frame is not ASCII") from exc
        return self._assembler.feed(line, monotonic_time.monotonic())

    def current(self) -> GnssFix:
        return self._assembler.current(monotonic_time.monotonic())

    def close(self) -> None:
        self._serial.close()
