import unittest
from datetime import datetime, timezone

from rotor.sensors import (
    As5600EncoderBank,
    CompassCalibration,
    EncoderReading,
    ImuReading,
    LimitSnapshot,
    MagnetometerReading,
    SensorFault,
    Tca9548a,
    tilt_compensated_true_heading,
)


class SimulatedI2cBus:
    """Strict test-only I2C fixture for TCA9548A and AS5600 behavior."""

    def __init__(self):
        self.selected = []
        self.reads = []
        self.frames = {
            0: [0x20, 0x01, 0x23],
            1: [0x28, 0x08, 0x00],
            2: [0x30, 0x0F, 0xFF],
        }

    def write_byte(self, address, value):
        self.selected.append((address, value))

    def read_i2c_block_data(self, address, register, length):
        channel = self.selected[-1][1].bit_length() - 1
        self.reads.append((address, register, length, channel))
        return self.frames[channel]


class SensorTests(unittest.TestCase):
    def test_as5600_multiplexer_reads_all_three_real_address_channels(self):
        bus = SimulatedI2cBus()
        bank = As5600EncoderBank(bus)
        readings = bank.read_all(10.0)
        self.assertEqual([item[1] for item in bus.selected], [1, 2, 4])
        self.assertEqual([item[3] for item in bus.reads], [0, 1, 2])
        self.assertEqual(readings["az"].raw_angle, 0x123)
        self.assertAlmostEqual(readings["az"].angle_deg, 0x123 * 360 / 4096)
        self.assertTrue(readings["az"].valid(10.05))
        self.assertFalse(readings["az"].valid(10.101))
        self.assertFalse(readings["el"].valid(10.0))
        self.assertFalse(readings["pol"].valid(10.0))

    def test_mux_rejects_invalid_or_aliased_rotor_channels(self):
        bus = SimulatedI2cBus()
        mux = Tca9548a(bus)
        with self.assertRaises(ValueError):
            mux.select(3)
        with self.assertRaisesRegex(ValueError, "distinct"):
            As5600EncoderBank(bus, axis_channels={"az": 0, "el": 0, "pol": 2})

    def test_limits_accept_single_active_nc_switch_but_not_both_open(self):
        normal = LimitSnapshot(
            {"az": (True, True), "el": (True, True), "pol": (True, True)}, 5.0
        )
        active_min = LimitSnapshot(
            {"az": (False, True), "el": (True, True), "pol": (True, True)}, 5.0
        )
        broken_pair = LimitSnapshot(
            {"az": (False, False), "el": (True, True), "pol": (True, True)}, 5.0
        )
        self.assertTrue(normal.healthy(5.01))
        self.assertTrue(active_min.healthy(5.01))
        self.assertFalse(broken_pair.healthy(5.01))
        self.assertFalse(normal.healthy(5.051))

    def test_tilt_compensated_heading_requires_calibration_and_fresh_sensors(self):
        identity = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        calibration = CompassCalibration(
            hard_iron_uT=(0.0, 0.0, 0.0),
            soft_iron_matrix=identity,
            sensor_to_base=identity,
            declination_deg=5.0,
            declination_source="manual survey",
            declination_date="2026-10-10",
            calibrated_utc=datetime.now(timezone.utc),
        )
        magnetic = MagnetometerReading((50.0, 0.0, 0.0), 20.0)
        imu = ImuReading(0.0, 0.0, (0.0, 0.0, 9.81), 20.0)
        heading = tilt_compensated_true_heading(magnetic, imu, calibration, 20.1)
        self.assertAlmostEqual(heading.magnetic_deg, 0.0)
        self.assertAlmostEqual(heading.true_deg, 5.0)
        with self.assertRaises(SensorFault):
            tilt_compensated_true_heading(magnetic, imu, calibration, 20.501)

    def test_encoder_missing_magnet_and_stale_timestamps_never_become_valid(self):
        missing = EncoderReading("az", 0, 0, 0.0, False, False, False, 1.0)
        too_strong = EncoderReading("el", 1, 10, 0.8, True, True, False, 1.0)
        stale = EncoderReading("pol", 2, 10, 0.8, True, False, False, 1.0)
        self.assertFalse(missing.valid(1.0))
        self.assertFalse(too_strong.valid(1.0))
        self.assertFalse(stale.valid(1.101))


if __name__ == "__main__":
    unittest.main()
