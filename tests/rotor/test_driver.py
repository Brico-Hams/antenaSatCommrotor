import json
from pathlib import Path
import re
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from rotor.driver import (
    CM5_SPI1_AXIS_CHIP_SELECT,
    CM5_SPI1_CHIP_SELECT_BCM_GPIO,
    REGISTER_VELOCITY_MAX,
    LinuxSpidevTransport,
    TMC5160_REG_IOIN,
    TMC5160_REG_VMAX,
    Tmc5160Axis,
    Tmc5160Fault,
    Tmc5160Spi,
)


class SimulatedSpiTransport:
    """Strict test-only five-byte SPI fixture; never used by production code."""

    def __init__(self, responses=None):
        self.frames = []
        self.responses = list(responses or [])

    def transfer(self, frame):
        if len(frame) != 5:
            raise AssertionError("test fixture received a non-five-byte SPI datagram")
        self.frames.append(frame)
        if self.responses:
            return self.responses.pop(0)
        return bytes(5)


def response(register_value):
    return b"\x00" + register_value.to_bytes(4, "big")


class DriverTests(unittest.TestCase):
    def test_cm5_axis_selects_match_frozen_interface_contract(self):
        contract_path = Path(__file__).resolve().parents[2] / "hardware" / "cm5" / "interface.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        axes = contract["softwareContract"]["rotor"]["axes"]

        self.assertEqual(CM5_SPI1_AXIS_CHIP_SELECT, {"az": 0, "el": 1, "pol": 2})
        fault_pins = {"az": 24, "el": 25, "pol": 26}
        for axis, expected in (("az", "AZ"), ("el", "EL"), ("pol", "POL")):
            chip_select = re.search(r"\bCS(\d+)\b", axes[expected]["spiChipSelect"])
            bcm_gpio = re.search(r"\bBCM(\d+)\b", axes[expected]["spiChipSelect"])
            self.assertIsNotNone(chip_select)
            self.assertIsNotNone(bcm_gpio)
            self.assertEqual(CM5_SPI1_AXIS_CHIP_SELECT[axis], int(chip_select.group(1)))
            self.assertEqual(
                CM5_SPI1_CHIP_SELECT_BCM_GPIO[CM5_SPI1_AXIS_CHIP_SELECT[axis]],
                int(bcm_gpio.group(1)),
            )
            self.assertEqual(axes[expected]["driverFaultBcm"], fault_pins[axis])
        gpio = {item["bcm"]: item for item in contract["gpio"]}
        for axis, bcm in fault_pins.items():
            self.assertEqual(gpio[bcm]["signal"], f"FAULT_{axis.upper()}_N")
            self.assertEqual(gpio[bcm]["activeLevel"], "LOW")
        for bcm in (4, 5, 6, 7, 8, 9, 10):
            self.assertEqual(gpio[bcm]["healthy"], "LOW")
        self.assertEqual(
            contract["safety"]["limitInputs"]["healthyLevel"], "LOW"
        )
        self.assertEqual(
            contract["safety"]["limitInputs"]["openWireLevel"], "HIGH"
        )
        self.assertEqual(contract["board"]["hardwareStatus"], "not yet designed or fabricated")
        self.assertTrue(contract["softwareContract"]["unverifiedHardwareMustRemainDisabled"])

    def test_cm5_axis_transport_opens_the_frozen_spidev_select(self):
        opened = []

        class FakeSpiDev:
            def open(self, bus, chip_select):
                opened.append((bus, chip_select))

            def close(self):
                pass

        fake_spidev = SimpleNamespace(SpiDev=FakeSpiDev)
        with patch.dict(sys.modules, {"spidev": fake_spidev}):
            for axis, chip_select in (("az", 0), ("el", 1), ("pol", 2)):
                transport = LinuxSpidevTransport.for_cm5_axis(
                    axis, spi_hz=1_000_000, spi_mode=3
                )
                transport.close()
        self.assertEqual(opened, [(1, 0), (1, 1), (1, 2)])

    def test_cm5_axis_transport_rejects_unknown_axis(self):
        with self.assertRaises(ValueError):
            LinuxSpidevTransport.for_cm5_axis(
                "rotor", spi_hz=1_000_000, spi_mode=3
            )

    def test_read_uses_two_five_byte_pipeline_transactions(self):
        transport = SimulatedSpiTransport(
            [response(0x12345678), response(0xAABBCCDD)]
        )
        spi = Tmc5160Spi(transport)
        status, value = spi.read_register(0x21)
        self.assertEqual(status, 0)
        self.assertEqual(value, 0xAABBCCDD)
        self.assertEqual(transport.frames, [b"\x21\0\0\0\0"] * 2)

    def test_axis_requires_chip_id_and_calculates_datasheet_ramp_units(self):
        transport = SimulatedSpiTransport(
            [response(0), response(0x30000000)]
        )
        spi = Tmc5160Spi(transport)
        axis = Tmc5160Axis(
            spi,
            clock_hz=12_000_000,
            microsteps_per_output_revolution=80_000,
            max_velocity_deg_s=2.25,
            acceleration_deg_s2=1.0,
            deceleration_deg_s2=1.0,
        )
        with self.assertRaises(Tmc5160Fault):
            axis.position_steps()
        axis.verify_identity()
        expected_vmax = round((2.25 * 80_000 / 360) * (1 << 24) / 12_000_000)
        self.assertEqual(axis.velocity_register(2.25), expected_vmax)
        self.assertLessEqual(expected_vmax, REGISTER_VELOCITY_MAX)
        self.assertGreater(axis.acceleration_register(1.0), 0)
        with self.assertRaises(ValueError):
            axis.velocity_register(2.2501)

    def test_move_uses_driver_internal_ramp_registers_not_gpio_steps(self):
        transport = SimulatedSpiTransport(
            [response(0), response(0x30000000)]
        )
        axis = Tmc5160Axis(
            Tmc5160Spi(transport),
            clock_hz=12_000_000,
            microsteps_per_output_revolution=80_000,
            max_velocity_deg_s=2.25,
            acceleration_deg_s2=1.0,
            deceleration_deg_s2=1.0,
        )
        axis.verify_identity()
        target = axis.move_to_degrees(90.0)
        writes = transport.frames[2:]
        self.assertEqual(target, 20_000)
        self.assertEqual(writes[0][0], 0x80 | 0x26)
        self.assertEqual(writes[1][0], 0x80 | 0x28)
        self.assertEqual(writes[2][0], 0x80 | TMC5160_REG_VMAX)
        self.assertEqual(writes[3][0], 0x80 | 0x20)
        self.assertEqual(writes[4][0], 0x80 | 0x2D)
        self.assertEqual(int.from_bytes(writes[4][1:], "big"), target)
        self.assertEqual(TMC5160_REG_IOIN, 0x04)

    def test_invalid_frames_registers_and_unrepresentable_values_fail(self):
        malformed = SimulatedSpiTransport([b"\0\0"])
        with self.assertRaises(Tmc5160Fault):
            Tmc5160Spi(malformed).read_register(0x21)
        spi = Tmc5160Spi(SimulatedSpiTransport())
        with self.assertRaises(ValueError):
            spi.read_register(0x80)
        with self.assertRaises(ValueError):
            spi.write_register(0x21, -1)
        axis = Tmc5160Axis(
            spi,
            clock_hz=1,
            microsteps_per_output_revolution=80_000,
            max_velocity_deg_s=2.25,
            acceleration_deg_s2=1.0,
            deceleration_deg_s2=1.0,
        )
        with self.assertRaises(ValueError):
            axis.velocity_register(2.25)


if __name__ == "__main__":
    unittest.main()
