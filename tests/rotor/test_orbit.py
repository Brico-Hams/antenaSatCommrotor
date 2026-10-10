from datetime import datetime, timedelta, timezone
import math
import unittest

from sgp4.api import Satrec, WGS72

from rotor.orbit import (
    Site,
    TleError,
    ecef_to_geodetic,
    geodetic_to_ecef,
    gmst82,
    parse_tle,
    propagate,
)


LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=timezone.utc)


def tle_line(body):
    checksum = sum(int(char) for char in body if char.isdigit()) + body.count("-")
    return f"{body}{checksum % 10}"


class OrbitTests(unittest.TestCase):
    def test_pinned_sgp4_matches_vallado_epoch_state(self):
        tle = parse_tle("VANGUARD 1", LINE1, LINE2)
        error, position, velocity = tle.satrec.sgp4(
            tle.satrec.jdsatepoch, tle.satrec.jdsatepochF
        )
        self.assertEqual(error, 0)
        expected_position = (7022.46529266, -1400.08296755, 0.03995155)
        expected_velocity = (1.893841015, 6.405893759, 4.534807250)
        for actual, expected in zip(position, expected_position):
            self.assertAlmostEqual(actual, expected, delta=0.001)
        for actual, expected in zip(velocity, expected_velocity):
            self.assertAlmostEqual(actual, expected, delta=0.000001)
        self.assertEqual(tle.norad_id, 5)

    def test_tle_checksum_id_epoch_and_staleness_are_enforced(self):
        with self.assertRaisesRegex(TleError, "checksum"):
            parse_tle("bad", LINE1[:-1] + "4", LINE2)
        wrong_satellite = tle_line(LINE2[:2] + "00006" + LINE2[7:68])
        with self.assertRaisesRegex(TleError, "matching"):
            parse_tle("bad", LINE1, wrong_satellite)
        tle = parse_tle("VANGUARD 1", LINE1, LINE2)
        tle.require_current(EPOCH)
        with self.assertRaisesRegex(TleError, "stale"):
            tle.require_current(EPOCH + timedelta(days=15))

    def test_topocentric_state_is_finite_and_range_rate_uses_velocity(self):
        tle = parse_tle("VANGUARD 1", LINE1, LINE2)
        site = Site(0.0, 0.0, 0.0)
        state = propagate(tle, EPOCH, site)
        values = (
            state.latitude_deg,
            state.longitude_deg,
            state.altitude_km,
            state.azimuth_deg,
            state.elevation_deg,
            state.range_m,
            state.range_rate_mps,
        )
        self.assertTrue(all(math.isfinite(value) for value in values))
        self.assertTrue(0 <= state.azimuth_deg < 360)
        self.assertGreater(state.range_m, 0)
        self.assertLess(abs(state.range_rate_mps), 20_000)

        before = propagate(tle, EPOCH - timedelta(seconds=1), site)
        after = propagate(tle, EPOCH + timedelta(seconds=1), site)
        numerical_rate = (after.range_m - before.range_m) / 2
        self.assertAlmostEqual(state.range_rate_mps, numerical_rate, delta=0.1)

    def test_wgs84_geodetic_round_trip_and_utc_guard(self):
        site = Site(40.0, -3.0, 650.0)
        ecef = geodetic_to_ecef(site)
        latitude, longitude, altitude = ecef_to_geodetic(ecef)
        self.assertAlmostEqual(latitude, site.latitude_deg, places=8)
        self.assertAlmostEqual(longitude, site.longitude_deg, places=8)
        self.assertAlmostEqual(altitude, site.altitude_m, places=5)
        self.assertAlmostEqual(
            gmst82(EPOCH), gmst82(EPOCH.astimezone(timezone.utc)), places=14
        )
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            propagate(parse_tle("VANGUARD 1", LINE1, LINE2), datetime(2000, 6, 27), site)


if __name__ == "__main__":
    unittest.main()
