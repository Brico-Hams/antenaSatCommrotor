"""Radio BLE v1 wire framing; all losses are observable, never filled with zeros."""

import json
import secrets
import struct
from collections import deque

BASE = "-4e53-4253-9000-000000000001"
SERVICE = "c8201001" + BASE
CONTROL_RX = "c8201002" + BASE
CONTROL_TX = "c8201003" + BASE
AUDIO_RX = "c8201004" + BASE
AUDIO_TX = "c8201005" + BASE
HEADER = struct.Struct("<BBHIII")


def fragments(message: dict, sequence: int):
    data = json.dumps(message, separators=(",", ":"), allow_nan=False).encode()
    if len(data) > 4096:
        raise ValueError("control message too large")
    for offset in range(0, len(data), 16):
        flags = (1 if offset == 0 else 0) | (2 if offset + 16 >= len(data) else 0)
        yield struct.pack("<BBH", 0x53, flags, sequence & 0xFFFF) + data[offset:offset + 16].ljust(16, b"\0")


class ControlAssembler:
    def __init__(self):
        self.buffer = bytearray()
        self.sequence = None

    def reset(self):
        self.buffer.clear()
        self.sequence = None

    def feed(self, frame: bytes):
        if len(frame) != 20 or frame[0] != 0x53 or frame[1] & ~3:
            self.reset()
            raise ValueError("invalid control frame")
        _, flags, sequence = struct.unpack("<BBH", frame[:4])
        if flags & 1:
            if self.sequence is not None:
                self.reset()
                raise ValueError("unfinished control message")
            self.sequence = sequence
        if self.sequence != sequence:
            self.reset()
            raise ValueError("control sequence mismatch")
        self.buffer.extend(frame[4:])
        if len(self.buffer) > 4096:
            self.reset()
            raise ValueError("control message overflow")
        if flags & 2:
            raw = bytes(self.buffer).rstrip(b"\0")
            self.reset()
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise ValueError("control envelope must be object")
            return value
        return None


class Audio:
    CAPACITY = 16

    def __init__(self, fault):
        self.fault = fault
        self.active = False
        self.rx = deque()
        self.tx = deque()
        self.rx_sequence = self.tx_sequence = 0
        self.rx_sample = self.tx_sample = 0
        self.rx_dropped = self.tx_faults = 0
        self.rx_notifications = 0
        self.mtu = 0

    def stop(self, reason="audio-stopped"):
        self.active = False
        self.rx.clear()
        self.tx.clear()
        self.fault(reason)

    def start(self, rate: int, mtu: int) -> dict:
        self.stop()
        if rate != 8000 or mtu < 247 or mtu > 517:
            raise ValueError("PCM requires 8000 Hz and actual ATT MTU >=247")
        self.mtu = mtu
        self.rx_id = secrets.randbits(32) or 1
        self.tx_id = secrets.randbits(32) or 2
        while self.rx_id == self.tx_id:
            self.tx_id = secrets.randbits(32) or 2
        self.rx_sequence = self.tx_sequence = 0
        self.rx_sample = self.tx_sample = 0
        self.active = True
        return {"rate": 8000, "rxStreamId": self.rx_id, "txStreamId": self.tx_id,
                "txCredits": self.credits}

    @property
    def credits(self):
        return self.CAPACITY - len(self.tx) if self.active else 0

    def failure(self, reason: str):
        self.tx_faults += 1
        self.stop(reason)
        raise ValueError(reason)

    def accept(self, packet: bytes):
        if not self.active or len(packet) < 18 or len(packet) > min(self.mtu - 3, 244):
            self.failure("audio-length-or-inactive")
        version, flags, reserved, stream, sequence, sample = HEADER.unpack(packet[:16])
        pcm = packet[16:]
        if version != 1 or flags or reserved or len(pcm) % 2:
            self.failure("audio-header")
        if stream != self.tx_id or sequence != self.tx_sequence or sample != self.tx_sample:
            self.failure("audio-gap-or-reorder")
        if not self.credits:
            self.failure("audio-credit-overrun")
        self.tx.append(pcm)
        self.tx_sequence = (sequence + 1) & 0xFFFFFFFF
        self.tx_sample = (sample + len(pcm) // 2) & 0xFFFFFFFF

    def consume(self):
        return self.tx.popleft() if self.tx else None

    def enqueue_rx(self, pcm: bytes):
        if not self.active:
            return
        if len(pcm) % 2:
            self.failure("RX-odd-PCM")
        size = min(self.mtu - 3 - 16, 228)
        for offset in range(0, len(pcm), size):
            chunk = pcm[offset:offset + size]
            frame = HEADER.pack(1, 0, 0, self.rx_id, self.rx_sequence, self.rx_sample) + chunk
            self.rx_sequence = (self.rx_sequence + 1) & 0xFFFFFFFF
            self.rx_sample = (self.rx_sample + len(chunk) // 2) & 0xFFFFFFFF
            if len(self.rx) >= self.CAPACITY:
                self.rx_dropped += 1
                # Stop the stream so Android cannot unknowingly consume incomplete audio.
                self.stop("RX-notify-queue-overflow")
                return
            self.rx.append(frame)

    def notify(self, send):
        if not self.rx:
            return False
        frame = self.rx[0]
        try:
            send(frame)
        except Exception:
            self.stop("RX-notify-failed")
            raise
        self.rx.popleft()
        self.rx_notifications += 1
        return True
