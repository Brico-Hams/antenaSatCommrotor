import unittest

from dbus_next import DBusError, Variant
from dbus_next.service import ServiceInterface

from radio.bluez import BlueZ, Manager
from radio.control import Dispatcher
from radio.protocol import Audio, AUDIO_RX, CONTROL_TX, HEADER
from radio.safety import Safety


class BlueZApiTests(unittest.TestCase):
    """D-Bus export/service logic only; actual Bluetooth adapter is NOT tested."""
    def setUp(self):
        self.safety = Safety(lambda: None)
        self.audio = Audio(self.safety.inhibit)
        self.dispatcher = Dispatcher(self.safety, self.audio, "a" * 64)
        self.peer = "/org/bluez/hci0/dev_00_11_22_33_44_55"
        self.server = BlueZ(self.dispatcher, self.audio, self.safety, self.peer)
        self.server.devices = {self.peer: {"Connected": True, "Paired": True,
                                          "Bonded": True, "Trusted": True}}

    def test_exported_uuids_properties_and_security_flags(self):
        manager = Manager(self.server)
        exported = next(m for m in ServiceInterface._get_methods(manager)
                        if m.name == "GetManagedObjects")
        objects = exported.fn(manager)
        chars = [obj["org.bluez.GattCharacteristic1"] for obj in objects.values()
                 if "org.bluez.GattCharacteristic1" in obj]
        self.assertEqual(len(chars), 4)
        by_uuid = {obj["UUID"].value: obj for obj in chars}
        self.assertIn("encrypt-authenticated-write", by_uuid[CONTROL_TX]["Flags"].value)
        self.assertIn("encrypt-authenticated-read", by_uuid[AUDIO_RX]["Flags"].value)
        self.assertEqual(self.server.audio_tx.flags[0], "write")

    def test_device_bond_token_mtu_and_subscription_gates(self):
        options = {"device": Variant("o", self.peer), "mtu": Variant("q", 247)}
        self.assertEqual(self.server.validate(options), (self.peer, 247))
        with self.assertRaises(DBusError):
            self.server.validate(options, require_auth=True)
        self.dispatcher.authenticated.add(self.peer)
        self.audio.start(8000, 247)
        self.assertEqual(self.server.validate(options, require_auth=True), (self.peer, 247))
        with self.assertRaises(DBusError):
            self.server.validate({"device": Variant("o", self.peer), "mtu": Variant("q", 23)},
                                 require_auth=True)
        self.audio.start(8000, 247)
        self.server.audio_rx.StartNotify()
        self.audio.enqueue_rx(b"\0\0")
        self.assertTrue(self.audio.notify(self.server.audio_rx.send))
        self.assertEqual(HEADER.unpack(self.server.audio_rx.value[:16])[3], self.audio.rx_id)
        self.server.devices[self.peer]["Bonded"] = False
        with self.assertRaises(DBusError):
            self.server.audio_rx.send(b"secret PCM")
        self.server.devices[self.peer]["Bonded"] = True
        self.server.devices["/org/bluez/hci0/dev_FF"] = {"Connected": True}
        with self.assertRaises(DBusError):
            self.server.validate_peer()


if __name__ == "__main__":
    unittest.main()
