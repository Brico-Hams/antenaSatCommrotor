import unittest

from rotor.gnss import (
    GnssFixAssembler,
    NmeaError,
    StaleFixError,
    parse_gga,
    parse_rmc,
)


def nmea(body: str) -> str:
    checksum = 0
    for char in body:
        checksum ^= ord(char)
    return f"${body}*{checksum:02X}"


class NmeaTests(unittest.TestCase):
    def test_valid_rmc_and_gga_form_actual_utc_fix(self):
        rmc = nmea("GPRMC,123519.00,A,4807.038,N,01131.000,E,0.0,0.0,230394,,,A")
        gga = nmea("GPGGA,123519.00,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,")
        parsed_rmc = parse_rmc(rmc)
        parsed_gga = parse_gga(gga)
        self.assertTrue(parsed_rmc.valid)
        self.assertEqual((parsed_rmc.fix_date.year, parsed_rmc.fix_date.month, parsed_rmc.fix_date.day),
                         (1994, 3, 23))
        self.assertEqual(parsed_gga.fix_quality, 1)

        assembler = GnssFixAssembler()
        self.assertIsNone(assembler.feed(rmc, 50.0))
        fix = assembler.feed(gga, 50.05)
        self.assertIsNotNone(fix)
        assert fix is not None
        self.assertEqual(fix.utc.isoformat(), "1994-03-23T12:35:19+00:00")
        self.assertAlmostEqual(fix.latitude_deg, 48.1173)
        self.assertAlmostEqual(fix.longitude_deg, 11.5166666667)
        self.assertEqual(fix.altitude_m, 545.4)
        self.assertTrue(fix.fresh(60.05))
        self.assertFalse(fix.fresh(60.051))

    def test_checksums_and_void_fixes_are_rejected_as_position(self):
        bad = "$GPRMC,123519.00,A,4807.038,N,01131.000,E,0.0,0.0,230394,,,A*00"
        with self.assertRaisesRegex(NmeaError, "checksum"):
            parse_rmc(bad)

        assembler = GnssFixAssembler()
        valid_rmc = nmea("GPRMC,123519.00,A,4807.038,N,01131.000,E,0.0,0.0,230394,,,A")
        valid_gga = nmea("GPGGA,123519.00,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,")
        assembler.feed(valid_rmc, 1.0)
        self.assertIsNotNone(assembler.feed(valid_gga, 1.1))
        void_rmc = nmea("GPRMC,123520.00,V,4807.038,N,01131.000,E,0.0,0.0,230394,,,N")
        self.assertIsNone(assembler.feed(void_rmc, 2.0))
        with self.assertRaises(StaleFixError):
            assembler.current(2.0)

    def test_mismatched_fix_times_and_invalid_coordinates_do_not_form_fix(self):
        assembler = GnssFixAssembler()
        rmc = nmea("GPRMC,123519.00,A,4807.038,N,01131.000,E,0.0,0.0,230394,,,A")
        gga = nmea("GPGGA,123521.00,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,")
        assembler.feed(rmc, 10.0)
        self.assertIsNone(assembler.feed(gga, 10.1))
        invalid = nmea("GPGGA,123519.00,9960.000,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,")
        with self.assertRaisesRegex(NmeaError, "out of range"):
            parse_gga(invalid)


if __name__ == "__main__":
    unittest.main()
