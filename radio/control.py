"""Authenticated versioned radio paths and original localhost Kenwood subset."""

import asyncio
import hmac
import json
import os
import secrets
import stat
from pathlib import Path

from . import VERSION
from .tracking import TrackingInput
from .polarization import PolarizationSwitch


def private_token(path: Path) -> str:
    """Provision a radio-private token, never a rotor NVS or repository secret."""
    path = path.expanduser()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not path.exists():
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w") as file:
            file.write(secrets.token_hex(32))
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
        raise PermissionError("token must be regular private 0600 file")
    if hasattr(os, "getuid") and info.st_uid != os.getuid():
        raise PermissionError("token owned by another user")
    value = path.read_text().strip()
    if len(value) != 64:
        raise ValueError("invalid private radio token")
    return value


class Dispatcher:
    def __init__(self, safety, audio, token: str, tracking_input=None):
        self.safety, self.audio, self.token = safety, audio, token
        self.authenticated = set()
        self.tracking_input = tracking_input if tracking_input is not None else TrackingInput(safety)
        self.polarization = safety.polarization if safety.polarization is not None else PolarizationSwitch(safety)
        self.rotor = None

    def disconnect(self, peer: str):
        self.authenticated.discard(peer)
        if peer in self.tracking_input.trusted_sources:
            self.tracking_input.revoke(peer)
        self.safety.disconnect(peer)
        self.audio.stop()
        if self.rotor:
            self.rotor.disconnect(peer)

    def dispatch(self, message: dict, peer: str, bonded: bool, encrypted: bool,
                 mtu: int = 0) -> dict:
        reply = {"v": 1, "id": message.get("id"), "path": message.get("path"),
                 "ok": False, "data": {}, "error": None}
        try:
            if (message.get("v") != 1 or not isinstance(message.get("id"), str)
                    or len(message["id"]) > 64 or message.get("op") not in {"get", "set"}
                    or not isinstance(message.get("data", {}), dict)):
                raise ValueError("invalid radio v1 envelope")
            path, op, data = message["path"], message["op"], message.get("data", {})
            if not bonded or not encrypted:
                raise PermissionError("bonded encrypted peer required")
            if path == "/auth" and op == "set":
                if not hmac.compare_digest(str(data.get("token", "")), self.token):
                    raise PermissionError("authentication denied")
                if self.safety.session not in (None, peer):
                    raise PermissionError("another audio control session owns radio")
                self.authenticated.add(peer)
                self.safety.connect(peer)
                reply["data"] = {"fw": VERSION}
            else:
                if peer not in self.authenticated:
                    raise PermissionError("authenticate first")
                if isinstance(path, str) and path.startswith(("/rotor/", "/satellites/")):
                    if self.rotor is None:
                        raise PermissionError("RotorController integration unavailable")
                    result = self.rotor.dispatch(path, op, data, peer)
                    reply.update(ok=result["ok"], data=result["data"], error=result["error"])
                    reply["schema"] = result["schema"]
                    return reply
                elif path == "/status" and op == "get":
                    reply["data"] = {
                        "fw": VERSION, "rxHz": self.safety.rx_hz, "txHz": self.safety.tx_hz,
                        "mode": self.safety.mode, "actualHz": self.safety.frequencies(),
                        "sdrReady": self.safety.sdr_ready, "tx": self.safety.transmitting,
                        "physicalArm": self.safety.physical_arm,
                        "physicalPtt": self.safety.physical_ptt,
                        "trackingFresh": self.safety.tracking_fresh(),
                        "rfPolarization": self.polarization.status(),
                        "rotorFault": self.safety.rotor_fault,
                        "rotorReady": self.safety.rotor_ready(),
                        "profiles": self.safety.profile_status(),
                        "rxChannel": self.safety.rx_channel,
                        "txChannel": self.safety.tx_channel,
                        "txPolicy": "ONE_TX_ONLY",
                        "driveAmplitudeLimit": 0.1,
                        "operationProfile": self.safety.operation_profile,
                        "availableChannels": list(self.safety.available_channels),
                        "fault": self.safety.fault, "rxDropped": self.audio.rx_dropped,
                        "txFaults": self.audio.tx_faults, "txCredits": self.audio.credits,
                    }
                elif path == "/radio" and op == "set":
                    self.safety.tune(data.get("rxHz"), data.get("txHz"), data.get("mode"))
                    self.audio.stop()
                elif path == "/profile" and op == "set":
                    self.safety.select_profile(data.get("profile"), peer, data.get("confirm"))
                    self.audio.stop()
                    reply["data"] = {"operationProfile": self.safety.operation_profile}
                elif path == "/audio/start" and op == "set":
                    if data.get("mtu") != mtu:
                        raise ValueError("claimed MTU differs from BlueZ negotiated MTU")
                    rx_channel, tx_channel = data.get("rxChannel"), data.get("txChannel")
                    if (rx_channel not in self.safety.available_channels
                            or tx_channel not in self.safety.available_channels
                            or (rx_channel == tx_channel and len(self.safety.available_channels) != 1)):
                        raise ValueError("explicit crossband rxChannel/txChannel required")
                    self.safety.inhibit("audio-channel-change")
                    nominal = {self.safety.rx_channel: self.safety.rx_hz,
                               self.safety.tx_channel: self.safety.tx_hz}
                    self.safety.rx_channel, self.safety.tx_channel = rx_channel, tx_channel
                    if len(self.safety.available_channels) != 1:
                        self.safety.tune(rx=nominal[rx_channel], tx=nominal[tx_channel])
                    reply["data"] = self.audio.start(data.get("rate"), mtu)
                    reply["data"].update({"rxChannel": rx_channel, "txChannel": tx_channel,
                                          "txPolicy": "ONE_TX_ONLY"})
                elif path == "/audio/stop" and op == "set":
                    self.audio.stop()
                elif path == "/rf/polarization" and op == "get":
                    reply["data"] = self.polarization.status()
                elif path == "/rf/polarization" and op == "set":
                    self.polarization.select(data["mode"])
                    reply["data"] = self.polarization.status()
                elif path == "/ptt" and op == "set":
                    if type(data.get("enabled")) is not bool:
                        raise ValueError("enabled must be boolean")
                    if data["enabled"]:
                        if not self.audio.active:
                            raise PermissionError("audio stream required")
                        if not self.safety.check():
                            self.audio.tx.clear()
                        self.safety.lease(peer, data.get("leaseMs"))
                    else:
                        self.safety.inhibit("remote-release")
                elif path == "/tracking" and op == "set":
                    # BLE authentication alone never provisions an orbit source.
                    self.tracking_input.update(peer, data["rangeRateMps"], data["utc"],
                                               data["site"])
                else:
                    raise ValueError("unknown path/op")
            reply["ok"] = True
        except (ValueError, PermissionError, KeyError, TypeError) as error:
            reply["error"] = str(error)
            if message.get("path") in {"/ptt", "/tracking", "/radio", "/audio/start", "/rf/polarization", "/profile"}:
                self.safety.inhibit("control-rejected")
        return reply


class Cat:
    MODES = {2: "USB", 4: "FM", 5: "AM"}

    def __init__(self, safety):
        self.safety = safety

    def command(self, command: str) -> str:
        try:
            if command in {"FA", "FB"}:
                return command + f"{self.safety.rx_hz if command == 'FA' else self.safety.tx_hz:011d};"
            if command.startswith(("FA", "FB")):
                if len(command) != 13 or not command[2:].isascii() or not command[2:].isdigit():
                    return "?;"
                self.safety.tune(**{"rx" if command[:2] == "FA" else "tx": int(command[2:])})
                return ""
            if command == "MD":
                code = next(code for code, mode in self.MODES.items() if mode == self.safety.mode)
                return f"MD{code};"
            if command.startswith("MD") and len(command) == 3:
                self.safety.tune(mode=self.MODES[int(command[2])])
                return ""
            if command == "RX":
                self.safety.inhibit("CAT-RX")
                return ""
            if command == "TX":
                # CAT has no authenticated radio session/lease; never creates one.
                self.safety.inhibit("CAT-TX-denied")
                return "?;"
        except (ValueError, KeyError):
            return "?;"
        return "?;"

    async def handle(self, reader, writer):
        buffer = ""
        try:
            while True:
                data = await asyncio.wait_for(reader.read(64), timeout=2)
                if not data:
                    break
                buffer += data.decode("ascii", errors="strict")
                if len(buffer) > 256:
                    writer.write(b"?;")
                    break
                while ";" in buffer:
                    command, buffer = buffer.split(";", 1)
                    writer.write(self.command(command).encode("ascii"))
                await writer.drain()
        except (TimeoutError, UnicodeError, ConnectionError):
            pass
        finally:
            self.safety.inhibit("CAT-disconnect-or-timeout")
            writer.close()
            await writer.wait_closed()

    async def listen(self, port: int = 4532):
        return await asyncio.start_server(self.handle, "127.0.0.1", port,
                                         limit=256, backlog=4)
