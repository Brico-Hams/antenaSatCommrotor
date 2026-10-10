"""In-host binding to the actual rotor.radio_adapter public hook.

Only the fixed local production module may be loaded, not a configurable
entry point or a mock. Config cannot attest hardware commissioning.
"""

import asyncio
import contextlib
from dataclasses import replace
import importlib
import json
import math
import time
from pathlib import Path


def open_rotor(config_path: str):
    path = Path(config_path).expanduser()
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("v") != 1:
        raise ValueError("rotor integration config requires v:1")
    if set(data) - {"v", "controllerConfig"} or not isinstance(data.get("controllerConfig"), str):
        raise ValueError("only explicit controllerConfig path accepted; no backend/mock flags")
    controller = Path(data["controllerConfig"])
    if not controller.is_absolute():
        controller = path.parent / controller
    controller = controller.resolve(strict=True)
    try:
        module = importlib.import_module("rotor.radio_adapter")
    except ImportError as error:
        raise RuntimeError("production RotorController radio_adapter not available; integration pending") from error
    factory = getattr(module, "open_adapter", None)
    if not callable(factory):
        raise RuntimeError("actual RotorController open_adapter hook not supplied")
    adapter = factory(controller)
    if not all(callable(getattr(adapter, method, None))
               for method in ("snapshot", "dispatch", "disconnect", "close")):
        with contextlib.suppress(Exception):
            adapter.close()
        raise RuntimeError("production rotor adapter contract incomplete")
    return adapter


class RotorIntegration:
    def __init__(self, adapter, safety, tracking, clock=time.monotonic):
        self.adapter, self.safety, self.tracking, self.clock = adapter, safety, tracking, clock
        self.last_sample = None
        self.tracking.provision("local-RotorController")

    def refresh(self):
        try:
            sample = self.adapter.snapshot()
            if not isinstance(sample, dict):
                raise ValueError("invalid rotor snapshot")
            sampled = sample["sampledMonotonic"]
            if not math.isfinite(sampled) or not 0 <= self.clock() - sampled <= 0.2:
                raise ValueError("stale rotor integration snapshot")
            if (sample.get("hardwareCommissioned") is not True
                    or sample.get("gnssValid") is not True
                    or sample.get("sgp4Valid") is not True):
                raise PermissionError("BSP/watchdog/GNSS/SGP4 not commissioned and valid")
            gnss_sampled = sample["gnssSampledMonotonic"]
            tracking_sampled = sample["trackingSampledMonotonic"]
            for source_time, max_age in ((gnss_sampled, 1.0), (tracking_sampled, 1.0)):
                if (type(source_time) not in (float, int) or not math.isfinite(source_time)
                        or not 0 <= self.clock() - source_time <= max_age):
                    raise ValueError("stale GNSS/SGP4 source timestamp")
            self.safety.rotor_update(sample["fault"], verified=True)
            # Preserve original source freshness; polling cannot refresh stale samples.
            self.safety.rotor_received = sampled
            if sample["fault"] is not None:
                raise PermissionError("rotor safety fault")
            if tracking_sampled != self.last_sample:
                self.tracking.provision("local-RotorController")
                self.tracking.update("local-RotorController", sample["rangeRateMps"],
                                     sample["utc"], sample["site"])
                self.safety.tracking = replace(
                    self.safety.tracking, received=min(gnss_sampled, tracking_sampled))
                self.last_sample = tracking_sampled
        except Exception:
            self.tracking.revoke("local-RotorController")
            self.safety.rotor_update("rotor-integration-invalid", verified=True)
            raise

    def dispatch(self, path, op, data, peer):
        self.safety.inhibit("rotor-operation")
        if path == "/rotor/target" and op == "set":
            if set(data) != {"azDeg", "elDeg", "polDeg"} or not all(
                type(data[key]) in (int, float) and math.isfinite(data[key])
                for key in ("azDeg", "elDeg", "polDeg")
            ):
                raise ValueError("explicit finite azDeg/elDeg/polDeg required")
        elif (path, op) not in {
            ("/rotor/status", "get"), ("/rotor/sensorsstatus", "get"),
            ("/rotor/home", "set"), ("/rotor/calibrate", "set"),
            ("/rotor/track", "set"), ("/rotor/stop", "set"),
            ("/satellites/catalog", "get"), ("/satellites/passes", "get")
        }:
            raise ValueError("rotor compatibility path not frozen/unsupported")
        # Status, stop, homing and calibration must remain reachable before
        # GNSS/tracking readiness. Controller itself enforces motion rules.
        result = self.adapter.dispatch(path, op, data, peer)
        if (not isinstance(result, dict) or result.get("schema") != "cm5-rotor/v1"
                or type(result.get("ok")) is not bool
                or "data" not in result or "error" not in result):
            raise ValueError("actual CM5 rotor reply schema required")
        return result

    def disconnect(self, peer):
        self.safety.inhibit("rotor-session-disconnect")
        self.adapter.disconnect(peer)

    async def pump(self):
        try:
            while True:
                try:
                    await asyncio.wait_for(asyncio.to_thread(self.refresh), timeout=0.2)
                except (ValueError, PermissionError, KeyError, TypeError):
                    # Invalid fix/unhomed hardware denies TX, not access to
                    # controller diagnostics/commissioning through authenticated BLE.
                    pass
                await asyncio.sleep(0.05)
        except BaseException:
            self.tracking.revoke("local-RotorController")
            self.safety.rotor_update("rotor-integration-disconnected", verified=True)
            raise

    def close(self):
        self.tracking.revoke("local-RotorController")
        self.adapter.close()
