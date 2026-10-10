"""Explicit independent-contact fixtures; no real GPIO/I2C or RF."""

from types import SimpleNamespace
import unittest

from radio.gpio_production import RadioGPIOProduction


class RadioGPIOTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.outputs = {}
        self.value = 0xFF
        self.link = True
        self.commissioned = True
        def read(reg):
            if not self.link:
                raise OSError("I2C disconnected")
            return {0x0A: 0, 0x00: 0xFF, 0x12: self.value}[reg]
        self.guard = SimpleNamespace(snapshot=lambda: {
            "hardwareCommissioned": self.commissioned, "physicalArm": True,
            "physicalPtt": True, "ncEstopHealthy": True, "watchdogHealthy": True,
            "rfPathHealthy": True, "sampledMonotonic": self.now})
        self.adapter = RadioGPIOProduction(
            SimpleNamespace(write=lambda pin, active: self.outputs.update({pin: active}), close=lambda: None),
            SimpleNamespace(read=read, close=lambda: None), self.guard, clock=lambda: self.now)

    def test_request_not_permit_independent_feedback_required(self):
        self.adapter.request("VHF")
        self.assertTrue(self.outputs[22])
        self.assertFalse(self.outputs[23])
        # Output high alone is never permit.
        self.assertFalse(self.adapter.permitted("VHF"))
        self.assertFalse(any(self.outputs.values()))
        self.adapter.request("VHF")
        self.value = 0xEF  # Independent active-low VHF contact only.
        self.assertTrue(self.adapter.permitted("VHF"))
        self.assertFalse(self.adapter.tx_off_acknowledged())

    def test_stuck_feedback_double_assertion_pa_fault_and_link_failclosed(self):
        for value in (0xEF, 0xDF, 0xCF, 0xBF, 0x7F):
            self.value = value
            with self.assertRaises(PermissionError):
                self.adapter.request("UHF")
            self.assertFalse(any(self.outputs.values()))
        self.value = 0xFF
        self.adapter.request("UHF")
        self.value = 0xCF  # Both feedback contacts asserted.
        self.assertFalse(self.adapter.permitted("UHF"))
        self.value = 0xFF
        self.adapter.request("UHF")
        self.link = False
        self.assertFalse(self.adapter.permitted("UHF"))
        self.assertFalse(any(self.outputs.values()))

    def test_uncommissioned_or_guard_disconnect_never_permits(self):
        self.commissioned = False
        with self.assertRaises(PermissionError):
            self.adapter.request("VHF")
        self.commissioned = True
        self.adapter.request("VHF")
        self.value = 0xEF
        self.guard.snapshot = lambda: (_ for _ in ()).throw(OSError("guard link lost"))
        self.assertFalse(self.adapter.permitted("VHF"))
        self.assertFalse(any(self.outputs.values()))

    def test_guard_staleness_and_pa_fault_during_tx(self):
        self.adapter.request("VHF")
        self.value = 0xEF
        self.assertTrue(self.adapter.permitted("VHF"))
        self.value = 0xAF  # VHF contact and active-low VHF PA fault.
        self.assertFalse(self.adapter.permitted("VHF"))
        self.value = 0xFF
        self.adapter.request("VHF")
        self.value = 0xEF
        self.guard.snapshot = lambda: {
            "hardwareCommissioned": True, "physicalArm": True, "physicalPtt": True,
            "ncEstopHealthy": True, "watchdogHealthy": True, "rfPathHealthy": True,
            "sampledMonotonic": 99.9}
        self.assertFalse(self.adapter.permitted("VHF"))
