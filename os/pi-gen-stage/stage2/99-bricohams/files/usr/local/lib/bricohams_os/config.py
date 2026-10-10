"""Strict non-secret radio host configuration validation for the OS image."""

import grp
import json
import os
import re
import stat


CONFIG_PATH = "/etc/bricohams/radio-host.json"
RADIO_EXECUTABLE = "/opt/bricohams/venv/bin/portable-sat-radio"
TOKEN_PATH = "/var/lib/bricohams/radio/token"
MAX_CONFIG_BYTES = 4096
PEER_PATTERN = re.compile(
    r"/org/bluez/hci[0-9]+/dev_(?:[0-9A-Fa-f]{2}_){5}[0-9A-Fa-f]{2}\Z",
    re.ASCII,
)
SERIAL_PATTERN = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z", re.ASCII)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key in radio host configuration")
        result[key] = value
    return result


def validate_config(value):
    if not isinstance(value, dict) or set(value) != {
        "version", "peer", "vhfSerial", "uhfSerial", "hardwareRate"
    }:
        raise ValueError("radio host configuration must contain exactly version, peer, vhfSerial, uhfSerial, hardwareRate")
    if type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("radio host configuration version must be integer 1")
    if not isinstance(value["peer"], str) or not PEER_PATTERN.fullmatch(value["peer"]):
        raise ValueError("peer must be a provisioned BlueZ Device1 object path")
    for key in ("vhfSerial", "uhfSerial"):
        if not isinstance(value[key], str) or not SERIAL_PATTERN.fullmatch(value[key]):
            raise ValueError(f"{key} must be an exact discovered Lime device serial")
    if value["vhfSerial"] == value["uhfSerial"]:
        raise ValueError("VHF and UHF Lime Mini serials must differ")
    rate = value["hardwareRate"]
    if type(rate) is not int or not 192_000 <= rate <= 4_000_000:
        raise ValueError("hardwareRate must be an integer in [192000, 4000000]")
    return value


def read_config(path=CONFIG_PATH):
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, "rb") as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0
                or info.st_gid != grp.getgrnam("bricohams-radio").gr_gid
                or stat.S_IMODE(info.st_mode) != 0o640):
            raise PermissionError("radio host configuration must be root:bricohams-radio mode 0640")
        contents = stream.read(MAX_CONFIG_BYTES + 1)
    if len(contents) > MAX_CONFIG_BYTES:
        raise ValueError("radio host configuration exceeds 4096 bytes")
    try:
        value = json.loads(contents.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("radio host configuration must be valid UTF-8 JSON") from error
    return validate_config(value)


def write_config(value, path=CONFIG_PATH):
    if os.geteuid() != 0:
        raise PermissionError("radio host configuration must be written as root")
    value = validate_config(value)
    directory = os.path.dirname(path)
    service_gid = grp.getgrnam("bricohams-radio").gr_gid
    os.makedirs(directory, mode=0o750, exist_ok=True)
    directory_info = os.stat(directory, follow_symlinks=False)
    if not stat.S_ISDIR(directory_info.st_mode) or directory_info.st_uid != 0:
        raise PermissionError("radio configuration directory must be a root-owned directory")
    if directory_info.st_gid != service_gid:
        os.chown(directory, 0, service_gid)
    if stat.S_IMODE(directory_info.st_mode) != 0o750:
        os.chmod(directory, 0o750, follow_symlinks=False)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o640)
    try:
        os.fchown(descriptor, 0, service_gid)
        os.fchmod(descriptor, 0o640)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
    except OSError:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
        raise
    return path
