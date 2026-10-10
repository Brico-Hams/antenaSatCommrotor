"""Vallado SGP4 propagation and TEME-to-local look-angle calculations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import math
from sgp4.api import Satrec, WGS72, jday


MAX_TLE_AGE = timedelta(days=14)
MAX_TLE_FUTURE = timedelta(days=1)
EARTH_ROTATION_RAD_S = 7.29211514670698e-5
WGS84_A_M = 6_378_137.0
WGS84_F = 1 / 298.257223563


class TleError(ValueError):
    """A TLE is malformed, inconsistent, or fails SGP4 initialization."""


class PropagationError(RuntimeError):
    """SGP4 could not propagate a requested satellite state."""


def _checksum(line: str) -> bool:
    if len(line) != 69 or not line[68].isdigit():
        return False
    total = sum(int(char) for char in line[:68] if char.isdigit())
    total += line[:68].count("-")
    return total % 10 == int(line[68])


def _julian_to_datetime(jd: float, fraction: float) -> datetime:
    return datetime(2000, 1, 1, 12, tzinfo=timezone.utc) + timedelta(
        days=(jd - 2_451_545.0) + fraction
    )


@dataclass(frozen=True)
class Tle:
    norad_id: int
    name: str
    line1: str
    line2: str
    epoch_utc: datetime
    satrec: Satrec

    def require_current(self, utc: datetime) -> None:
        if utc.tzinfo is None or utc.utcoffset() is None:
            raise ValueError("propagation time must be timezone-aware UTC")
        age = utc.astimezone(timezone.utc) - self.epoch_utc
        if age > MAX_TLE_AGE or age < -MAX_TLE_FUTURE:
            raise TleError("TLE epoch is stale or implausibly in the future")


@dataclass(frozen=True)
class Site:
    latitude_deg: float
    longitude_deg: float
    altitude_m: float

    def __post_init__(self) -> None:
        values = (self.latitude_deg, self.longitude_deg, self.altitude_m)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("site coordinates must be finite")
        if not -90 <= self.latitude_deg <= 90:
            raise ValueError("site latitude is outside [-90, 90]")
        if not -180 <= self.longitude_deg <= 180:
            raise ValueError("site longitude is outside [-180, 180]")
        if not -1000 <= self.altitude_m <= 100_000:
            raise ValueError("site altitude is outside the supported range")


@dataclass(frozen=True)
class SatelliteState:
    norad_id: int
    name: str
    utc: datetime
    latitude_deg: float
    longitude_deg: float
    altitude_km: float
    azimuth_deg: float
    elevation_deg: float
    range_m: float
    range_rate_mps: float
    apparent_track_angle_deg: float | None


def parse_tle(name: str, line1: str, line2: str) -> Tle:
    normalized_name = name.strip()
    line1 = line1.rstrip("\r\n")
    line2 = line2.rstrip("\r\n")
    if not normalized_name or len(normalized_name) > 64:
        raise TleError("satellite name must contain 1..64 characters")
    if not line1.startswith("1 ") or not line2.startswith("2 "):
        raise TleError("TLE lines must start with line numbers 1 and 2")
    if not _checksum(line1) or not _checksum(line2):
        raise TleError("TLE checksum mismatch or line length is not 69")
    norad1, norad2 = line1[2:7], line2[2:7]
    if not norad1.isdigit() or norad1 != norad2:
        raise TleError("only matching numeric NORAD IDs are supported")
    norad_id = int(norad1)
    try:
        satrec = Satrec.twoline2rv(line1, line2, WGS72)
    except (ValueError, TypeError) as exc:
        raise TleError("SGP4 rejected the TLE fields") from exc
    if satrec.error:
        raise TleError(f"SGP4 initialization error {satrec.error}")
    epoch = _julian_to_datetime(satrec.jdsatepoch, satrec.jdsatepochF)
    return Tle(norad_id, normalized_name, line1, line2, epoch, satrec)


def tle_checksum_line(body: str) -> str:
    """Return a 69-character TLE line from a 68-character body."""
    if len(body) != 68:
        raise ValueError("TLE body must be exactly 68 characters")
    total = sum(int(char) for char in body if char.isdigit()) + body.count("-")
    return f"{body}{total % 10}"


def gmst82(utc: datetime) -> float:
    """Greenwich mean sidereal angle in radians, using Vallado's GMST82."""
    if utc.tzinfo is None or utc.utcoffset() is None:
        raise ValueError("GMST input must be timezone-aware UTC")
    instant = utc.astimezone(timezone.utc)
    jd, fraction = jday(
        instant.year,
        instant.month,
        instant.day,
        instant.hour,
        instant.minute,
        instant.second + instant.microsecond / 1_000_000,
    )
    centuries = ((jd - 2_451_545.0) + fraction) / 36_525.0
    seconds = (
        67_310.54841
        + (876_600 * 3_600 + 8_640_184.812866) * centuries
        + 0.093104 * centuries**2
        - 6.2e-6 * centuries**3
    )
    return (seconds * (math.tau / 86_400)) % math.tau


def geodetic_to_ecef(site: Site) -> tuple[float, float, float]:
    latitude = math.radians(site.latitude_deg)
    longitude = math.radians(site.longitude_deg)
    eccentricity_sq = WGS84_F * (2 - WGS84_F)
    sin_lat = math.sin(latitude)
    normal = WGS84_A_M / math.sqrt(1 - eccentricity_sq * sin_lat * sin_lat)
    return (
        (normal + site.altitude_m) * math.cos(latitude) * math.cos(longitude),
        (normal + site.altitude_m) * math.cos(latitude) * math.sin(longitude),
        (normal * (1 - eccentricity_sq) + site.altitude_m) * sin_lat,
    )


def ecef_to_geodetic(
    position: tuple[float, float, float],
) -> tuple[float, float, float]:
    x, y, z = position
    if not all(math.isfinite(component) for component in position):
        raise ValueError("ECEF position must be finite")
    longitude = math.atan2(y, x)
    radial = math.hypot(x, y)
    if radial < 1e-9:
        latitude = math.copysign(math.pi / 2, z)
        semi_minor = WGS84_A_M * (1 - WGS84_F)
        altitude = abs(z) - semi_minor
        return math.degrees(latitude), math.degrees(longitude), altitude
    eccentricity_sq = WGS84_F * (2 - WGS84_F)
    latitude = math.atan2(z, radial * (1 - eccentricity_sq))
    altitude = 0.0
    for _ in range(10):
        sin_lat = math.sin(latitude)
        normal = WGS84_A_M / math.sqrt(1 - eccentricity_sq * sin_lat * sin_lat)
        altitude = radial / math.cos(latitude) - normal
        next_latitude = math.atan2(
            z,
            radial * (1 - eccentricity_sq * normal / (normal + altitude)),
        )
        if abs(next_latitude - latitude) < 1e-13:
            latitude = next_latitude
            break
        latitude = next_latitude
    sin_lat = math.sin(latitude)
    normal = WGS84_A_M / math.sqrt(1 - eccentricity_sq * sin_lat * sin_lat)
    altitude = radial / math.cos(latitude) - normal
    return (
        math.degrees(latitude),
        math.degrees(longitude),
        altitude,
    )


def _rotate_z(vector: tuple[float, float, float], angle: float) -> tuple[float, float, float]:
    cosine, sine = math.cos(angle), math.sin(angle)
    x, y, z = vector
    return cosine * x - sine * y, sine * x + cosine * y, z


def propagate(tle: Tle, utc: datetime, site: Site) -> SatelliteState:
    if utc.tzinfo is None or utc.utcoffset() is None:
        raise ValueError("propagation time must be timezone-aware UTC")
    instant = utc.astimezone(timezone.utc)
    tle.require_current(instant)
    jd, fraction = jday(
        instant.year,
        instant.month,
        instant.day,
        instant.hour,
        instant.minute,
        instant.second + instant.microsecond / 1_000_000,
    )
    error, position_km, velocity_km_s = tle.satrec.sgp4(jd, fraction)
    if error:
        raise PropagationError(f"SGP4 propagation error {error}")
    position_teme = tuple(component * 1000 for component in position_km)
    velocity_teme = tuple(component * 1000 for component in velocity_km_s)
    theta = gmst82(instant)
    position_ecef = _rotate_z(position_teme, -theta)
    site_ecef = geodetic_to_ecef(site)
    relative_ecef = tuple(a - b for a, b in zip(position_ecef, site_ecef))
    latitude = math.radians(site.latitude_deg)
    longitude = math.radians(site.longitude_deg)
    sin_lat, cos_lat = math.sin(latitude), math.cos(latitude)
    sin_lon, cos_lon = math.sin(longitude), math.cos(longitude)
    dx, dy, dz = relative_ecef
    east = -sin_lon * dx + cos_lon * dy
    north = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz
    up = cos_lat * cos_lon * dx + cos_lat * sin_lon * dy + sin_lat * dz
    horizontal = math.hypot(east, north)
    distance = math.sqrt(east * east + north * north + up * up)
    if not math.isfinite(distance) or distance <= 0:
        raise PropagationError("SGP4 produced an invalid topocentric range")
    azimuth = math.degrees(math.atan2(east, north)) % 360
    elevation = math.degrees(math.atan2(up, horizontal))

    # Range rate is inertial relative velocity projected on the TEME line of sight.
    site_teme = _rotate_z(site_ecef, theta)
    site_velocity_teme = (
        -EARTH_ROTATION_RAD_S * site_teme[1],
        EARTH_ROTATION_RAD_S * site_teme[0],
        0.0,
    )
    relative_teme = tuple(position_teme[i] - site_teme[i] for i in range(3))
    relative_velocity_teme = tuple(
        velocity_teme[i] - site_velocity_teme[i] for i in range(3)
    )
    range_rate = sum(
        relative_teme[i] * relative_velocity_teme[i] for i in range(3)
    ) / distance
    satellite_velocity_ecef = _rotate_z(velocity_teme, -theta)
    earth_rotation_velocity_ecef = (
        -EARTH_ROTATION_RAD_S * position_ecef[1],
        EARTH_ROTATION_RAD_S * position_ecef[0],
        0.0,
    )
    relative_velocity_ecef = tuple(
        satellite_velocity_ecef[i] - earth_rotation_velocity_ecef[i]
        for i in range(3)
    )
    vx, vy, vz = relative_velocity_ecef
    velocity_east = -sin_lon * vx + cos_lon * vy
    velocity_north = -sin_lat * cos_lon * vx - sin_lat * sin_lon * vy + cos_lat * vz
    velocity_up = cos_lat * cos_lon * vx + cos_lat * sin_lon * vy + sin_lat * vz
    line_east, line_north, line_up = east / distance, north / distance, up / distance
    tangent_east = velocity_east - range_rate * line_east
    tangent_north = velocity_north - range_rate * line_north
    tangent_up = velocity_up - range_rate * line_up
    azimuth_rad = math.radians(azimuth)
    elevation_rad = math.radians(elevation)
    azimuth_basis = (
        math.cos(azimuth_rad),
        -math.sin(azimuth_rad),
        0.0,
    )
    elevation_basis = (
        -math.sin(azimuth_rad) * math.sin(elevation_rad),
        -math.cos(azimuth_rad) * math.sin(elevation_rad),
        math.cos(elevation_rad),
    )
    tangent_norm = math.sqrt(
        tangent_east**2 + tangent_north**2 + tangent_up**2
    )
    apparent_track_angle = None
    if tangent_norm >= 1e-6:
        along_azimuth = (
            tangent_east * azimuth_basis[0]
            + tangent_north * azimuth_basis[1]
            + tangent_up * azimuth_basis[2]
        )
        along_elevation = (
            tangent_east * elevation_basis[0]
            + tangent_north * elevation_basis[1]
            + tangent_up * elevation_basis[2]
        )
        apparent_track_angle = math.degrees(
            math.atan2(along_azimuth, along_elevation)
        ) % 360

    latitude_sat, longitude_sat, altitude_sat_m = ecef_to_geodetic(position_ecef)
    return SatelliteState(
        norad_id=tle.norad_id,
        name=tle.name,
        utc=instant,
        latitude_deg=latitude_sat,
        longitude_deg=(longitude_sat + 180) % 360 - 180,
        altitude_km=altitude_sat_m / 1000,
        azimuth_deg=azimuth,
        elevation_deg=elevation,
        range_m=distance,
        range_rate_mps=range_rate,
        apparent_track_angle_deg=apparent_track_angle,
    )


@dataclass(frozen=True)
class SatellitePass:
    norad_id: int
    name: str
    aos_utc: datetime
    tca_utc: datetime
    los_utc: datetime
    max_elevation_deg: float


def predict_passes(
    tle: Tle,
    site: Site,
    start_utc: datetime,
    *,
    duration: timedelta = timedelta(hours=24),
    step: timedelta = timedelta(seconds=60),
    minimum_elevation_deg: float = 0.0,
    limit: int = 10,
) -> list[SatellitePass]:
    if start_utc.tzinfo is None or start_utc.utcoffset() is None:
        raise ValueError("pass prediction start must be timezone-aware UTC")
    if not timedelta(0) < duration <= timedelta(hours=24):
        raise ValueError("pass prediction duration must be in (0, 24 hours]")
    if not timedelta(seconds=10) <= step <= timedelta(seconds=120):
        raise ValueError("pass prediction step must be in [10, 120] seconds")
    if not math.isfinite(minimum_elevation_deg) or not 0 <= minimum_elevation_deg < 90:
        raise ValueError("minimum elevation must be in [0, 90)")
    if not 1 <= limit <= 20:
        raise ValueError("pass result limit must be in [1, 20]")
    start = start_utc.astimezone(timezone.utc)
    end = start + duration
    tle.require_current(start)
    points: list[tuple[datetime, SatelliteState]] = []
    cursor = start
    while cursor <= end:
        points.append((cursor, propagate(tle, cursor, site)))
        cursor += step
    if points[-1][0] < end:
        points.append((end, propagate(tle, end, site)))

    passes: list[SatellitePass] = []
    aos: datetime | None = start if points[0][1].elevation_deg >= minimum_elevation_deg else None
    visible: list[tuple[datetime, SatelliteState]] = []
    if aos is not None:
        visible.append(points[0])
    for (left_time, left), (right_time, right) in zip(points, points[1:]):
        left_visible = left.elevation_deg >= minimum_elevation_deg
        right_visible = right.elevation_deg >= minimum_elevation_deg
        if left_visible != right_visible:
            crossing = _refine_horizon(
                tle, site, left_time, right_time, minimum_elevation_deg, right_visible
            )
            if right_visible:
                aos = crossing
                visible = [(crossing, propagate(tle, crossing, site))]
            elif aos is not None:
                visible.append((crossing, propagate(tle, crossing, site)))
                peak_time, peak = max(visible, key=lambda item: item[1].elevation_deg)
                passes.append(
                    SatellitePass(
                        tle.norad_id,
                        tle.name,
                        aos,
                        peak_time,
                        crossing,
                        peak.elevation_deg,
                    )
                )
                if len(passes) >= limit:
                    return passes
                aos = None
                visible = []
        elif right_visible and aos is not None:
            visible.append((right_time, right))
    if aos is not None and visible:
        peak_time, peak = max(visible, key=lambda item: item[1].elevation_deg)
        passes.append(
            SatellitePass(
                tle.norad_id,
                tle.name,
                aos,
                peak_time,
                end,
                peak.elevation_deg,
            )
        )
    return passes[:limit]


def _refine_horizon(
    tle: Tle,
    site: Site,
    low_time: datetime,
    high_time: datetime,
    minimum_elevation_deg: float,
    high_visible: bool,
) -> datetime:
    low, high = low_time, high_time
    while (high - low).total_seconds() > 1:
        middle = low + (high - low) / 2
        is_visible = (
            propagate(tle, middle, site).elevation_deg >= minimum_elevation_deg
        )
        if is_visible == high_visible:
            high = middle
        else:
            low = middle
    return high
