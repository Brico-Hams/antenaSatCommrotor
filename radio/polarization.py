"""RF handedness switch, NOT mechanical POL axial roll.

Integration must verify antenna/switch capabilities and supply actual feedback
GPIO lines. Output register readback alone is not a switch acknowledgement.
"""

import time
from enum import Enum


class RFPolarization(str, Enum):
    LINEAR = "LINEAR"
    RHCP = "RHCP"
    LHCP = "LHCP"


class PolarizationSwitch:
    def __init__(self, safety, hardware=None, clock=time.monotonic):
        self.safety, self.hardware, self.clock = safety, hardware, clock
        self.requested = None
        self.configured = None
        self.settle_until = 0.0
        safety.polarization = self

    def select(self, value: str):
        self.configured = None
        self.requested = None
        self.safety.inhibit("RF-polarization-switch")
        mode = RFPolarization(value)
        if (self.hardware is None or self.hardware.capability_verified is not True
                or mode not in self.hardware.capabilities):
            raise PermissionError("verified RF antenna/switch capability unavailable")
        if self.safety.transmitting or self.hardware.tx_off_acknowledged() is not True:
            raise PermissionError("RF switch requires actual TX-off acknowledgement")
        # stop_tx above must successfully deactivate the SDR/drop the gate.
        self.hardware.write(mode)
        self.requested = mode
        self.settle_until = self.clock() + self.hardware.settle_seconds

    def ready(self):
        if (self.hardware is None or self.requested is None
                or self.hardware.capability_verified is not True
                or self.requested not in self.hardware.capabilities):
            self.configured = None
            return False
        if self.clock() < self.settle_until:
            return False
        try:
            actual = self.hardware.acknowledge()
        except Exception:
            actual = None
        if actual != self.requested:
            self.configured = None
            return False
        self.configured = actual
        return True

    def status(self):
        ready = self.ready()
        return {"requested": self.requested.value if self.requested else None,
                "configured": self.configured.value if ready else None,
                "ready": ready,
                "capabilities": [x.value for x in self.hardware.capabilities]
                if self.hardware and self.hardware.capability_verified else []}


class GPIOAcknowledgedSwitch:
    """Real gpiod v2 switch outputs plus independent contact/sense inputs.

No board pinout is assumed. A local hardware integrator supplies verified
truth tables and settle time. LINEAR is supported only if actually advertised
by the verified antenna/network combination, never inferred from roll angle.
"""

    def __init__(self, chip: str, outputs: tuple[int, ...], feedback: tuple[int, ...],
                 truth_table: dict, settle_seconds: float, capability_verified: bool,
                 tx_off_acknowledged):
        import gpiod
        from gpiod.line import Direction, Value, Bias
        if capability_verified is not True:
            raise PermissionError("antenna, switch and feedback verification required")
        if (not outputs or not feedback or len(set(outputs + feedback)) != len(outputs + feedback)
                or not 0.001 <= settle_seconds <= 1):
            raise ValueError("independent switch/feedback lines and verified settle time required")
        table = {RFPolarization(mode): tuple(bits) for mode, bits in truth_table.items()}
        if (not table or any(len(bits) != len(outputs) or any(type(b) is not bool for b in bits)
                             for bits in table.values())
                or len(feedback) != len(outputs) or len(set(table.values())) != len(table)):
            raise ValueError("invalid verified RF switch truth table")
        self.capability_verified = True
        self.capabilities = tuple(table)
        self.settle_seconds = settle_seconds
        if not callable(tx_off_acknowledged):
            raise ValueError("actual TX-off feedback callback required")
        self.tx_off_acknowledged = tx_off_acknowledged
        self.outputs, self.feedback, self.table, self.Value = outputs, feedback, table, Value
        self.lines = gpiod.request_lines(chip, consumer="radio-rf-polarization", config={
            outputs: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
            feedback: gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_DOWN),
        })

    def write(self, mode):
        self.lines.set_values({line: self.Value.ACTIVE if bit else self.Value.INACTIVE
                               for line, bit in zip(self.outputs, self.table[mode])})

    def acknowledge(self):
        bits = tuple(self.lines.get_value(line) == self.Value.ACTIVE for line in self.feedback)
        return next((mode for mode, pattern in self.table.items() if pattern == bits), None)

    def close(self):
        self.lines.release()
