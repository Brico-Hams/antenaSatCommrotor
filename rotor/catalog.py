"""Bounded atomic cache of actual validated TLE records."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import tempfile
import threading

from .orbit import Tle, TleError, parse_tle


MAX_CACHE_BYTES = 48 * 1024
MAX_CATALOG_ITEMS = 100


class CatalogError(RuntimeError):
    """The on-disk satellite catalog is unsafe or invalid."""


@dataclass(frozen=True)
class CatalogEntry:
    norad_id: int
    name: str
    epoch_utc: str


class TleCatalog:
    def __init__(self, path: str | os.PathLike[str]) -> None:
        self._path = Path(path)
        self._lock = threading.RLock()
        self._items: dict[int, Tle] = {}
        self._load()

    def entries(self) -> tuple[CatalogEntry, ...]:
        with self._lock:
            return tuple(
                CatalogEntry(item.norad_id, item.name, item.epoch_utc.isoformat())
                for item in sorted(self._items.values(), key=lambda value: value.norad_id)
            )

    def get(self, norad_id: int) -> Tle:
        if isinstance(norad_id, bool) or not isinstance(norad_id, int):
            raise ValueError("NORAD ID must be an integer")
        with self._lock:
            try:
                return self._items[norad_id]
            except KeyError as exc:
                raise KeyError(f"NORAD ID {norad_id} is not in the local catalog") from exc

    def replace(self, records: list[tuple[str, str, str]]) -> tuple[CatalogEntry, ...]:
        if not isinstance(records, list) or len(records) > MAX_CATALOG_ITEMS:
            raise ValueError(f"catalog must contain at most {MAX_CATALOG_ITEMS} TLE records")
        parsed: dict[int, Tle] = {}
        for name, line1, line2 in records:
            item = parse_tle(name, line1, line2)
            if item.norad_id in parsed:
                raise ValueError(f"duplicate NORAD ID {item.norad_id}")
            parsed[item.norad_id] = item
        payload = {
            "version": 1,
            "items": [
                {"name": item.name, "line1": item.line1, "line2": item.line2}
                for item in sorted(parsed.values(), key=lambda value: value.norad_id)
            ],
        }
        encoded = json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode("ascii")
        if len(encoded) > MAX_CACHE_BYTES:
            raise ValueError(f"catalog exceeds the {MAX_CACHE_BYTES}-byte limit")
        with self._lock:
            self._write_atomic(encoded)
            self._items = parsed
            return self.entries()

    def _load(self) -> None:
        if self._path.is_symlink():
            raise CatalogError("catalog path must not be a symlink")
        if not self._path.exists():
            return
        if not self._path.is_file():
            raise CatalogError("catalog path is not a regular file")
        if self._path.stat().st_size > MAX_CACHE_BYTES:
            raise CatalogError("catalog exceeds the configured size limit")
        try:
            payload = json.loads(self._path.read_text(encoding="ascii"))
            if (
                not isinstance(payload, dict)
                or payload.get("version") != 1
                or not isinstance(payload.get("items"), list)
            ):
                raise CatalogError("catalog version or items field is invalid")
            items = payload["items"]
            if len(items) > MAX_CATALOG_ITEMS:
                raise CatalogError("catalog has too many records")
            parsed: dict[int, Tle] = {}
            for record in items:
                if not isinstance(record, dict):
                    raise CatalogError("catalog record is not an object")
                item = parse_tle(record["name"], record["line1"], record["line2"])
                if item.norad_id in parsed:
                    raise CatalogError(f"duplicate NORAD ID {item.norad_id}")
                parsed[item.norad_id] = item
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, TleError) as exc:
            raise CatalogError("catalog contents are invalid") from exc
        self._items = parsed

    def _write_atomic(self, encoded: bytes) -> None:
        parent = self._path.parent
        parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if parent.is_symlink():
            raise CatalogError("catalog directory must not be a symlink")
        fd, temporary = tempfile.mkstemp(prefix=".tle-", dir=parent)
        try:
            if os.name == "posix":
                os.fchmod(fd, 0o600)
            with os.fdopen(fd, "wb") as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self._path)
            if os.name == "posix":
                os.chmod(self._path, 0o600)
                directory_fd = os.open(parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
        except OSError:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
