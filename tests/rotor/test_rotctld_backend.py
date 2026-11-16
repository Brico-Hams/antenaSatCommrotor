import socket
import threading
import unittest

from rotor.cli import _arguments
from rotor.rotctld_backend import (
    LSR1,
    LSR2,
    RotctldAdapter,
    RotctldAxisPair,
    RotctldError,
)


class FakeRotctld:
    """Minimal localhost rotctld; `drop_first` closes the first connection mid-command."""

    def __init__(self, info="LibreSat Rotator LSR-1 v1", drop_first=False, errors=()):
        self.info = info
        self.drop_first = drop_first
        self.errors = set(errors)
        self.commands = []
        self.az, self.el = 10.0, 20.0
        self.server = socket.socket()
        self.server.bind(("127.0.0.1", 0))
        self.server.listen(4)
        self.port = self.server.getsockname()[1]
        self.connections = 0
        self._thread = threading.Thread(target=self._accept, daemon=True)
        self._thread.start()

    def _accept(self):
        while True:
            try:
                conn, _ = self.server.accept()
            except OSError:
                return
            self.connections += 1
            threading.Thread(target=self._serve, args=(conn, self.connections), daemon=True).start()

    def _serve(self, conn, number):
        with conn:
            for line in conn.makefile("r"):
                line = line.strip()
                self.commands.append(line)
                verb = line.split()[0] if line else ""
                if self.drop_first and number == 1 and verb != "_":
                    return
                if verb in self.errors:
                    conn.sendall(b"RPRT -1\n")
                elif verb == "_":
                    conn.sendall(self.info.encode() + b"\n")
                elif verb == "p":
                    conn.sendall(f"{self.az}\n{self.el}\n".encode())
                elif verb == "P":
                    _, az, el = line.split()
                    self.az, self.el = float(az), float(el)
                    conn.sendall(b"RPRT 0\n")
                elif verb in ("S", "K"):
                    conn.sendall(b"RPRT 0\n")
                else:
                    conn.sendall(b"RPRT -4\n")

    def close(self):
        self.server.close()


class RotctldBackendTests(unittest.TestCase):
    def start(self, **kwargs):
        server = FakeRotctld(**kwargs.pop("server", {}))
        self.addCleanup(server.close)
        axes = RotctldAxisPair("127.0.0.1", server.port, timeout=2.0, **kwargs)
        self.addCleanup(axes.close)
        return server, axes

    def test_position_and_move(self):
        server, axes = self.start()
        self.assertEqual(axes.connect(), LSR1)
        self.assertEqual(axes.position(), (10.0, 20.0))
        self.assertEqual(axes.move_to(100, 45), (100.0, 45.0))
        self.assertEqual(axes.position(), (100.0, 45.0))

    def test_rprt_error_raises(self):
        server, axes = self.start(server={"errors": {"P"}})
        axes.connect()
        with self.assertRaises(RotctldError):
            axes.move_to(10, 10)

    def test_lsr1_limits(self):
        server, axes = self.start()
        axes.connect()
        self.assertEqual(axes.move_to(450, 180), (450.0, 180.0))
        self.assertEqual(axes.move_to(-0.3, 0), (0.0, 0.0))
        for az, el in ((-5, 10), (451, 10), (10, -5), (10, 181), (float("nan"), 0)):
            with self.assertRaises(ValueError):
                axes.move_to(az, el)
        self.assertNotIn("P -5.000 10.000", server.commands)

    def test_lsr2_detection_and_limits(self):
        server, axes = self.start(server={"info": "LibreSat Rotator LSR-2 v1"})
        self.assertEqual(axes.connect(), LSR2)
        self.assertEqual(axes.move_to(-360, -30), (-360.0, -30.0))
        self.assertEqual(axes.move_to(360, 150), (360.0, 150.0))
        with self.assertRaises(ValueError):
            axes.move_to(0, 160)

    def test_unknown_model_and_override_mismatch(self):
        _, axes = self.start(server={"info": "Dummy rotator"})
        with self.assertRaises(RotctldError):
            axes.connect()
        _, axes = self.start(model="lsr-2")
        with self.assertRaises(RotctldError):
            axes.connect()
        with self.assertRaises(ValueError):
            RotctldAxisPair(model="lsr-3")

    def test_reconnect_once_after_drop(self):
        server, axes = self.start(server={"drop_first": True})
        axes.connect()
        self.assertEqual(axes.position(), (10.0, 20.0))
        self.assertEqual(server.connections, 2)

    def test_timeout_fails_closed(self):
        silent = socket.socket()
        silent.bind(("127.0.0.1", 0))
        silent.listen(4)
        self.addCleanup(silent.close)
        axes = RotctldAxisPair("127.0.0.1", silent.getsockname()[1], timeout=0.2)
        self.addCleanup(axes.close)
        with self.assertRaises(RotctldError):
            axes.connect()

    def test_stop_park_and_adapter(self):
        server, axes = self.start()
        axes.connect()
        adapter = RotctldAdapter(axes)
        self.assertTrue(adapter.control("stop", {})["ok"])
        self.assertTrue(adapter.control("park", {})["ok"])
        self.assertIn("S", server.commands)
        self.assertIn("K", server.commands)
        self.assertEqual(adapter.control("status", {})["data"]["model"], "LSR-1")
        self.assertFalse(adapter.control("goto", {"az": 900, "el": 0})["ok"])
        self.assertFalse(adapter.control("goto", {})["ok"])

    def test_cli_options(self):
        args = _arguments(["--backend", "rotctld", "--host", "h", "--port", "4600", "--model", "lsr-2"])
        self.assertEqual((args.backend, args.host, args.port, args.model), ("rotctld", "h", 4600, "lsr-2"))
        default = _arguments(["--config", "x.json"])
        self.assertEqual((default.backend, default.port, default.model), ("tmc5160", 4533, None))
        with self.assertRaises(SystemExit):
            _arguments([])


if __name__ == "__main__":
    unittest.main()
