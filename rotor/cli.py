"""Standalone local JSON-lines interface for the rotor package."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from typing import Protocol, TextIO

from .radio_adapter import open_adapter


class LocalRotorAdapter(Protocol):
    def control(
        self,
        operation: str,
        data: Mapping[str, object],
        *,
        local_console: bool = False,
    ) -> Mapping[str, object]: ...

    def close(self) -> None: ...


def serve_json_lines(
    adapter: LocalRotorAdapter,
    source: TextIO,
    sink: TextIO,
    *,
    local_console: bool = False,
) -> None:
    """Serve one local JSON request per line; privilege is process configuration."""
    for line in source:
        try:
            request = json.loads(line)
            if not isinstance(request, dict) or set(request) != {"operation", "data"}:
                raise ValueError("request must contain exactly operation and data")
            operation = request["operation"]
            data = request["data"]
            if not isinstance(operation, str) or not isinstance(data, dict):
                raise ValueError("operation must be a string and data must be an object")
            result = adapter.control(
                operation, data, local_console=local_console
            )
            response = dict(result)
        except (json.JSONDecodeError, ValueError) as exc:
            response = {"ok": False, "data": None, "error": str(exc)}
        sink.write(json.dumps(response, allow_nan=False, separators=(",", ":")))
        sink.write("\n")
        sink.flush()


def _arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="portable-sat-rotor",
        description="Standalone CM5 rotor control; no radio/SDR/audio services are started.",
    )
    parser.add_argument(
        "--config",
        required=True,
        help="locally provisioned rotor hardware configuration",
    )
    parser.add_argument(
        "--local-console",
        action="store_true",
        help="grant this local stdin session the local commissioning principal",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _arguments(argv)
    try:
        adapter = open_adapter(args.config)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        print(f"portable-sat-rotor: {exc}", file=sys.stderr)
        return 2
    try:
        serve_json_lines(
            adapter,
            sys.stdin,
            sys.stdout,
            local_console=args.local_console,
        )
    finally:
        adapter.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
