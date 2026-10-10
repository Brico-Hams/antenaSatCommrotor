"""Local adapter boundary for the independent rotor controller.

This module has no radio, SDR, audio, PA, Bluetooth, or SoapySDR imports.
The hardware composition must be supplied by the CM5 platform bootstrap;
there is intentionally no simulated or guessed production composition here.
"""

from __future__ import annotations

from collections.abc import Mapping
from importlib.metadata import entry_points
from pathlib import Path
from typing import Protocol

from .controller import RotorController


HOST_SCHEMA = "cm5-rotor/v1"


class ControllerProtocol(Protocol):
    def start_service(self) -> None: ...

    def integration_snapshot(self) -> Mapping[str, object]: ...

    def handle_control(
        self,
        operation: str,
        data: Mapping[str, object],
        *,
        local_console: bool = False,
    ) -> Mapping[str, object]: ...

    def dispatch_host_path(
        self, path: str, operation: str, data: Mapping[str, object]
    ) -> Mapping[str, object]: ...

    def close(self) -> None: ...


class RotorRadioAdapter:
    """Adapt RotorController methods to the host's local rotor adapter contract."""

    def __init__(self, controller: ControllerProtocol) -> None:
        self._controller = controller
        self._closed = False
        try:
            self._controller.start_service()
        except RuntimeError:
            self._controller.close()
            raise

    def snapshot(self) -> dict[str, object]:
        self._require_open()
        result = self._controller.integration_snapshot()
        if not isinstance(result, Mapping):
            raise TypeError("rotor integration snapshot must be a mapping")
        return dict(result)

    def control(
        self,
        operation: str,
        data: Mapping[str, object],
        *,
        local_console: bool = False,
    ) -> dict[str, object]:
        self._require_open()
        if not isinstance(data, Mapping):
            raise ValueError("rotor request data must be an object")
        result = self._controller.handle_control(
            operation, data, local_console=local_console
        )
        if not isinstance(result, Mapping):
            raise TypeError("rotor controller control must return a mapping")
        reply = dict(result)
        if set(reply) != {"ok", "data", "error"}:
            raise ValueError("rotor controller returned an invalid control envelope")
        return reply

    def dispatch(
        self,
        path: str,
        operation: str,
        data: Mapping[str, object],
        peer: str,
    ) -> dict[str, object]:
        self._require_open()
        if not isinstance(peer, str) or not peer:
            raise PermissionError("authenticated host peer identity is required")
        if not isinstance(path, str) or not isinstance(operation, str):
            raise ValueError("rotor path and operation must be strings")
        if not isinstance(data, Mapping):
            raise ValueError("rotor request data must be an object")
        result = self._controller.dispatch_host_path(path, operation, data)
        if not isinstance(result, Mapping):
            raise TypeError("rotor controller host dispatch must return a mapping")
        reply = dict(result)
        if reply.get("schema") != HOST_SCHEMA:
            raise ValueError("rotor controller returned an incompatible host schema")
        return reply

    def disconnect(self, peer: str) -> None:
        self._require_open()
        if not isinstance(peer, str) or not peer:
            raise ValueError("authenticated host peer identity is required")
        # Tracking and motor control are autonomous and must not depend on a phone.

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._controller.close()

    def _require_open(self) -> None:
        if self._closed:
            raise RuntimeError("rotor adapter is closed")


def open_adapter(controller_config_path: str | Path) -> RotorRadioAdapter:
    """Open the installed CM5 hardware provider, never a guessed/test backend.

    A separately installed platform BSP registers exactly one
    ``portable_sat_rotor.hardware`` entry point named ``cm5``. It receives the
    explicit controller configuration path and must return a real
    :class:`RotorController` composition. The configuration and provider are
    not themselves evidence of commissioning; controller health remains
    fail-closed until live hardware readbacks and local calibration succeed.
    """
    if not isinstance(controller_config_path, (str, Path)):
        raise TypeError("controller configuration path must be a string or Path")
    config_path = Path(controller_config_path).expanduser().resolve(strict=True)
    if not config_path.is_file():
        raise ValueError("controller configuration must be a regular file")
    providers = [
        provider
        for provider in entry_points(group="portable_sat_rotor.hardware")
        if provider.name == "cm5"
    ]
    if len(providers) != 1:
        raise RuntimeError(
            "exactly one CM5 hardware BSP entry point named 'cm5' is required; "
            "no simulated or radio-coupled fallback is provided"
        )
    factory = providers[0].load()
    if not callable(factory):
        raise TypeError("CM5 hardware BSP entry point is not callable")
    controller = factory(config_path)
    if not isinstance(controller, RotorController):
        raise TypeError("CM5 hardware BSP must return a RotorController")
    return RotorRadioAdapter(controller)
