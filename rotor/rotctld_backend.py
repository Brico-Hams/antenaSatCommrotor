"""Hamlib rotctld backend for BricoHams LibreSat rotators (LSR-1 / LSR-2).

Fail-closed: unknown models, malformed replies, RPRT errors and out-of-range
targets raise instead of being guessed. Standard library only.
"""

from __future__ import annotations

import math
import socket
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Protocol


DEFAULT_PORT = 4533
DEFAULT_TIMEOUT_S = 5.0
CLAMP_TOLERANCE_DEG = 0.5
MAX_LINE_BYTES = 512


class RotctldError(RuntimeError):
    """rotctld transport, protocol, range or RPRT error."""


@dataclass(frozen=True)
class RotatorModel:
    name: str
    az_min: float
    az_max: float
    el_min: float
    el_max: float


LSR1 = RotatorModel("LSR-1", 0.0, 450.0, 0.0, 180.0)
LSR2 = RotatorModel("LSR-2", -360.0, 360.0, -30.0, 150.0)
MODELS = {"lsr-1": LSR1, "lsr-2": LSR2}


class SocketLike(Protocol):
    def sendall(self, data: bytes) -> None: ...

    def recv(self, size: int) -> bytes: ...

    def close(self) -> None: ...

    def settimeout(self, timeout: float | None) -> None: ...


def _tcp_connector(host: str, port: int, timeout: float) -> Callable[[], SocketLike]:
    def connect() -> SocketLike:
        return socket.create_connection((host, port), timeout=timeout)

    return connect


def detect_model(info: str) -> RotatorModel:
    upper = info.upper()
    found = [model for model in (LSR1, LSR2) if model.name in upper]
    if len(found) != 1:
        raise RotctldError(f"unrecognised LibreSat model: {info!r}")
    return found[0]


class RotctldAxisPair:
    """AZ/EL pair driven through rotctld; the socket factory is injectable."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = DEFAULT_PORT,
        *,
        model: str | None = None,
        timeout: float = DEFAULT_TIMEOUT_S,
        connector: Callable[[], SocketLike] | None = None,
    ) -> None:
        if model is not None and model.lower() not in MODELS:
            raise ValueError("model must be lsr-1 or lsr-2")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be a positive finite number")
        self._override = MODELS[model.lower()] if model is not None else None
        self._connector = connector or _tcp_connector(host, port, timeout)
        self._timeout = timeout
        self._sock: SocketLike | None = None
        self._buffer = b""
        self._lock = threading.Lock()
        self.model: RotatorModel | None = None

    def connect(self) -> RotatorModel:
        with self._lock:
            self._open()
            try:
                info = self._exchange("_", 1)[0]
            except (OSError, EOFError) as exc:
                self._close()
                raise RotctldError(f"rotctld model query failed: {exc}") from exc
            except RotctldError:
                self._close()
                raise
            detected = detect_model(info)
            if self._override is not None and self._override != detected:
                self._close()
                raise RotctldError(
                    f"model override {self._override.name} does not match {detected.name}"
                )
            self.model = self._override or detected
            return self.model

    def close(self) -> None:
        with self._lock:
            self._close()

    def position(self) -> tuple[float, float]:
        with self._lock:
            lines = self._command("p", 2)
        try:
            az, el = float(lines[0]), float(lines[1])
        except ValueError as exc:
            raise RotctldError(f"malformed position reply: {lines!r}") from exc
        if not (math.isfinite(az) and math.isfinite(el)):
            raise RotctldError("non-finite position reply")
        return az, el

    def move_to(self, az: float, el: float) -> tuple[float, float]:
        model = self._require_model()
        az = self._limit(az, model.az_min, model.az_max, "azimuth")
        el = self._limit(el, model.el_min, model.el_max, "elevation")
        with self._lock:
            self._command(f"P {az:.3f} {el:.3f}", 0)
        return az, el

    def stop(self) -> None:
        with self._lock:
            self._command("S", 0)

    def park(self) -> None:
        with self._lock:
            self._command("K", 0)

    def _require_model(self) -> RotatorModel:
        if self.model is None:
            raise RotctldError("not connected: model unknown")
        return self.model

    @staticmethod
    def _limit(value: float, low: float, high: float, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")
        value = float(value)
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        if value < low - CLAMP_TOLERANCE_DEG or value > high + CLAMP_TOLERANCE_DEG:
            raise ValueError(f"{name} {value} outside {low}..{high}")
        return min(max(value, low), high)

    def _open(self) -> None:
        self._close()
        try:
            sock = self._connector()
            sock.settimeout(self._timeout)
        except OSError as exc:
            raise RotctldError(f"rotctld connection failed: {exc}") from exc
        self._sock = sock

    def _close(self) -> None:
        sock, self._sock, self._buffer = self._sock, None, b""
        if sock is not None:
            try:
                sock.close()
            except OSError:
                pass

    def _command(self, text: str, lines: int) -> list[str]:
        """Run one command, reconnecting and retrying exactly once on I/O failure."""
        try:
            if self._sock is None:
                raise OSError("not connected")
            return self._exchange(text, lines)
        except (OSError, EOFError):
            self._open()
            try:
                return self._exchange(text, lines)
            except (OSError, EOFError) as exc:
                self._close()
                raise RotctldError(f"rotctld I/O failure: {exc}") from exc

    def _exchange(self, text: str, lines: int) -> list[str]:
        assert self._sock is not None
        self._buffer = b""
        try:
            self._sock.sendall(text.encode("ascii") + b"\n")
        except socket.timeout as exc:
            raise OSError(f"timeout: {exc}") from exc
        first = self._read_line()
        if first.startswith("RPRT"):
            code = self._rprt(first)
            if code != 0:
                raise RotctldError(f"rotctld error {first} for {text.split()[0]!r}")
            if lines:
                raise RotctldError(f"unexpected empty reply to {text.split()[0]!r}")
            return []
        if lines == 0:
            raise RotctldError(f"unexpected reply {first!r}")
        out = [first]
        while len(out) < lines:
            out.append(self._read_line())
        return out

    @staticmethod
    def _rprt(line: str) -> int:
        try:
            return int(line.split()[1])
        except (IndexError, ValueError) as exc:
            raise RotctldError(f"malformed RPRT reply: {line!r}") from exc

    def _read_line(self) -> str:
        assert self._sock is not None
        while b"\n" not in self._buffer:
            if len(self._buffer) > MAX_LINE_BYTES:
                raise RotctldError("rotctld reply line too long")
            try:
                chunk = self._sock.recv(256)
            except socket.timeout as exc:
                raise OSError("timeout waiting for rotctld") from exc
            if not chunk:
                raise EOFError("rotctld closed the connection")
            self._buffer += chunk
        line, _, self._buffer = self._buffer.partition(b"\n")
        return line.decode("ascii", "replace").strip()


class RotctldAdapter:
    """Thin JSON-lines control adapter (status/goto/stop/park) over a RotctldAxisPair."""

    def __init__(self, axes: RotctldAxisPair) -> None:
        self._axes = axes

    def control(
        self,
        operation: str,
        data: Mapping[str, object],
        *,
        local_console: bool = False,
    ) -> Mapping[str, object]:
        try:
            if operation == "status":
                az, el = self._axes.position()
                model = self._axes.model
                return {
                    "ok": True,
                    "data": {
                        "backend": "rotctld",
                        "model": model.name if model else None,
                        "az": az,
                        "el": el,
                    },
                    "error": None,
                }
            if operation == "goto":
                az, el = self._axes.move_to(data["az"], data["el"])  # type: ignore[arg-type]
                return {"ok": True, "data": {"az": az, "el": el}, "error": None}
            if operation == "stop":
                self._axes.stop()
                return {"ok": True, "data": {}, "error": None}
            if operation == "park":
                self._axes.park()
                return {"ok": True, "data": {}, "error": None}
            return self._error(f"unsupported rotctld operation: {operation}")
        except (RotctldError, ValueError, KeyError, OSError) as exc:
            return self._error(str(exc))

    def close(self) -> None:
        self._axes.close()

    @staticmethod
    def _error(message: str) -> dict[str, object]:
        return {"ok": False, "data": None, "error": message}


def open_rotctld_adapter(
    host: str, port: int, model: str | None = None, timeout: float = DEFAULT_TIMEOUT_S
) -> RotctldAdapter:
    axes = RotctldAxisPair(host, port, model=model, timeout=timeout)
    axes.connect()
    return RotctldAdapter(axes)
