"""Revision-A radio request/independent-feedback boundary; hardware on HOLD.

Only BCM22/23 are owned here. Shared MCP23017 is read-only: another BSP
owner must configure BANK=0 and GPA4..7 inputs without altering motor lines.
An output request or I2C register value never attests guard commissioning.
"""

import json
import os
import stat
import time
from pathlib import Path


def validate_contract(contract):
    mapping = {line["signal"]: line["bcm"] for line in contract["gpio"]}
    expander = contract["peripherals"]["i2c"]["gpioExpander"]
    expected = {"GPA4": "PTT_VHF_FEEDBACK_N", "GPA5": "PTT_UHF_FEEDBACK_N",
                "GPA6": "PA_VHF_FAULT_N", "GPA7": "PA_UHF_FAULT_N"}
    if (contract["board"]["revision"] != "A" or
            mapping.get("PTT_VHF_REQUEST") != 22 or mapping.get("PTT_UHF_REQUEST") != 23
            or expander["address"] != "0x20"
            or any(expander["pins"].get(pin) != value for pin, value in expected.items())):
        raise ValueError("frozen revision-A radio GPIO contract mismatch")


class RadioGPIOProduction:
    def __init__(self, request_lines, expander, guard, clock=time.monotonic):
        self.lines, self.expander, self.guard, self.clock = request_lines, expander, guard, clock
        self.requested = None
        self.fault = "not-commissioned"
        self.off()

    def off(self):
        self.requested = None
        # Always attempt both request deassertions, even if one fails.
        error = None
        for bcm in (22, 23):
            try:
                self.lines.write(bcm, False)
            except Exception as fault:
                error = error or fault
        if error:
            raise error

    def feedback(self):
        # BANK=0, GPA4..7 must remain inputs. Never write shared expander.
        if self.expander.read(0x0A) & 0x80 or self.expander.read(0x00) & 0xF0 != 0xF0:
            raise RuntimeError("shared MCP23017 bank/direction contract invalid")
        value = self.expander.read(0x12)
        # Revision A suffix _N: LOW asserted. Pull-up/open is NOT healthy.
        return {"VHF": not bool(value & 0x10), "UHF": not bool(value & 0x20),
                "vhfFault": not bool(value & 0x40), "uhfFault": not bool(value & 0x80)}

    def guard_ready(self):
        sample = self.guard.snapshot()
        return (isinstance(sample, dict) and sample.get("hardwareCommissioned") is True
                and sample.get("physicalArm") is True and sample.get("physicalPtt") is True
                and sample.get("ncEstopHealthy") is True
                and sample.get("watchdogHealthy") is True
                and sample.get("rfPathHealthy") is True
                and type(sample.get("sampledMonotonic")) in (int, float)
                and 0 <= self.clock() - sample["sampledMonotonic"] <= 0.05)

    def request(self, channel):
        self.off()
        try:
            if channel not in ("VHF", "UHF") or not self.guard_ready():
                raise PermissionError("commissioned physical RF guard required")
            feedback = self.feedback()
            if any(feedback.values()):
                raise PermissionError("stuck PTT feedback or PA fault before request")
            self.lines.write(22 if channel == "VHF" else 23, True)
            self.requested = channel
            self.fault = "awaiting-independent-feedback"
        except Exception:
            self.off()
            self.fault = "request-rejected"
            raise

    def permitted(self, channel):
        try:
            feedback = self.feedback()
            other = "UHF" if channel == "VHF" else "VHF"
            ready = (channel in ("VHF", "UHF") and self.requested == channel
                     and self.guard_ready() and feedback[channel] and not feedback[other]
                     and not feedback["vhfFault"] and not feedback["uhfFault"])
            if not ready:
                self.off()
                self.fault = "independent-feedback-or-guard-fault"
                return False
            self.fault = None
            return True
        except Exception:
            self.off()
            self.fault = "GPIO-I2C-guard-link-fault"
            return False

    def tx_off_acknowledged(self):
        try:
            feedback = self.feedback()
            return self.requested is None and not feedback["VHF"] and not feedback["UHF"]
        except Exception:
            return False

    def close(self):
        try:
            self.off()
        finally:
            self.lines.close()
            self.expander.close()


class GpiodRequests:
    def __init__(self, chip):
        import gpiod
        from gpiod.line import Direction, Value
        self.Value = Value
        self.lines = gpiod.request_lines(chip, consumer="radio-PTT-requests", config={
            (22, 23): gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)})

    def write(self, bcm, active):
        self.lines.set_value(bcm, self.Value.ACTIVE if active else self.Value.INACTIVE)

    def close(self):
        self.lines.release()


class MCPReadOnly:
    def __init__(self, bus):
        from smbus2 import SMBus
        self.bus = SMBus(bus)

    def read(self, register):
        return self.bus.read_byte_data(0x20, register)

    def close(self):
        self.bus.close()


def open_production(config_path, contract_path, guard):
    """Local root config cannot substitute for actual external guard attestation."""
    path = Path(config_path)
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_mode & 0o022
            or not hasattr(os, "getuid") or info.st_uid != 0):
        raise PermissionError("root-owned non-writable local radio GPIO config required")
    config = json.loads(path.read_text())
    if config.get("v") != 1:
        raise ValueError("radio GPIO config v:1 required")
    if config.get("hardwareCommissioned") is not True:
        raise PermissionError("hardwareCommissioned=false: external circuit on HOLD")
    validate_contract(json.loads(Path(contract_path).read_text()))
    if guard is None:
        raise PermissionError("actual verified external guard provider unavailable")
    lines = GpiodRequests(config["gpioChip"])
    try:
        expander = MCPReadOnly(config["i2cBus"])
        result = RadioGPIOProduction(lines, expander, guard)
        if not result.guard_ready():
            expander.close()
            raise PermissionError("external guard not physically commissioned/live")
        return result
    except Exception:
        lines.close()
        raise
