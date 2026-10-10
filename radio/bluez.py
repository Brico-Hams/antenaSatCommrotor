"""Linux BlueZ application, registered over the real system D-Bus.

BlueZ enforces authenticated encryption via characteristic security flags.
One provisioned bonded peer is allowed; multiple connections stop notifications.
"""

import asyncio

from dbus_next import BusType, Variant, DBusError
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property
from dbus_next.constants import PropertyAccess

from .protocol import (SERVICE, CONTROL_RX, CONTROL_TX, AUDIO_RX, AUDIO_TX,
                       ControlAssembler, fragments)

ROOT = "/org/portable_sat_radio"
SERVICE_PATH = ROOT + "/service0"


class GattService(ServiceInterface):
    def __init__(self):
        super().__init__("org.bluez.GattService1")

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> "s":
        return SERVICE

    @dbus_property(access=PropertyAccess.READ)
    def Primary(self) -> "b":
        return True

    @dbus_property(access=PropertyAccess.READ)
    def Includes(self) -> "ao":
        return []

    def properties(self):
        return {"UUID": Variant("s", SERVICE), "Primary": Variant("b", True),
                "Includes": Variant("ao", [])}


class Characteristic(ServiceInterface):
    def __init__(self, server, uuid, index, write=False, audio=False):
        super().__init__("org.bluez.GattCharacteristic1")
        self.server, self.uuid, self.audio = server, uuid, audio
        self.path = SERVICE_PATH + f"/char{index}"
        self.writable = write
        self.notifying = False
        self.value = b""
        self.flags = (["write", "encrypt-authenticated-write"] if write else
                      ["notify", "read", "encrypt-authenticated-read"])

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> "s":
        return self.uuid

    @dbus_property(access=PropertyAccess.READ)
    def Service(self) -> "o":
        return SERVICE_PATH

    @dbus_property(access=PropertyAccess.READ)
    def Flags(self) -> "as":
        return self.flags

    @dbus_property(access=PropertyAccess.READ)
    def Notifying(self) -> "b":
        return self.notifying

    @dbus_property(access=PropertyAccess.READ)
    def Value(self) -> "ay":
        return self.value

    @method()
    def ReadValue(self, options: "a{sv}") -> "ay":
        self.server.validate(options, require_auth=self.audio)
        return self.value

    @method()
    def WriteValue(self, value: "ay", options: "a{sv}"):
        if not self.writable:
            raise DBusError("org.bluez.Error.NotPermitted", "read only")
        peer, mtu = self.server.validate(options, require_auth=self.audio)
        try:
            if self.audio:
                self.server.audio.accept(bytes(value))
                self.server.credit()
            else:
                message = self.server.assembler.feed(bytes(value))
                if message is not None:
                    reply = self.server.dispatcher.dispatch(message, peer, True, True, mtu)
                    self.server.send_control(reply)
                    if message.get("path") == "/ptt" and reply["ok"]:
                        self.server.credit()
        except (ValueError, TypeError) as error:
            if not self.audio:
                self.server.safety.inhibit("BLE-control-frame-fault")
            raise DBusError("org.bluez.Error.Failed", str(error))

    @method()
    def StartNotify(self):
        if self.writable:
            raise DBusError("org.bluez.Error.NotSupported", "not a notify characteristic")
        self.server.validate_peer(require_auth=self.audio)
        self.notifying = True
        self.emit_properties_changed({"Notifying": True})

    @method()
    def StopNotify(self):
        self.notifying = False
        self.emit_properties_changed({"Notifying": False})
        self.server.audio.stop()
        self.server.safety.inhibit("BLE-notify-stopped")

    def send(self, value):
        self.server.validate_peer(require_auth=self.audio)
        if not self.notifying:
            raise ValueError("subscriber not ready")
        self.value = bytes(value)
        self.emit_properties_changed({"Value": self.value})

    def properties(self):
        return {"UUID": Variant("s", self.uuid), "Service": Variant("o", SERVICE_PATH),
                "Flags": Variant("as", self.flags), "Value": Variant("ay", self.value),
                "Notifying": Variant("b", self.notifying)}


class Manager(ServiceInterface):
    def __init__(self, server):
        super().__init__("org.freedesktop.DBus.ObjectManager")
        self.server = server

    @method()
    def GetManagedObjects(self) -> "a{oa{sa{sv}}}":
        result = {SERVICE_PATH: {"org.bluez.GattService1": self.server.service.properties()}}
        for characteristic in self.server.characteristics:
            result[characteristic.path] = {
                "org.bluez.GattCharacteristic1": characteristic.properties()
            }
        return result


class Advertisement(ServiceInterface):
    def __init__(self):
        super().__init__("org.bluez.LEAdvertisement1")

    @dbus_property(access=PropertyAccess.READ)
    def Type(self) -> "s":
        return "peripheral"

    @dbus_property(access=PropertyAccess.READ)
    def ServiceUUIDs(self) -> "as":
        return [SERVICE]

    @dbus_property(access=PropertyAccess.READ)
    def LocalName(self) -> "s":
        return "PortableSatRadio"

    @method()
    def Release(self):
        pass


class BlueZ:
    def __init__(self, dispatcher, audio, safety, peer_path: str, adapter="/org/bluez/hci0"):
        if not peer_path.startswith(adapter + "/dev_"):
            raise ValueError("provisioned BlueZ bonded device path required")
        self.dispatcher, self.audio, self.safety = dispatcher, audio, safety
        self.peer, self.adapter = peer_path, adapter
        self.assembler = ControlAssembler()
        self.sequence = 0
        self.last_fault = None
        self.devices = {}
        self.bus = None
        self.service = GattService()
        self.control_rx = Characteristic(self, CONTROL_RX, 0)
        self.control_tx = Characteristic(self, CONTROL_TX, 1, write=True)
        self.audio_rx = Characteristic(self, AUDIO_RX, 2, audio=True)
        self.audio_tx = Characteristic(self, AUDIO_TX, 3, write=True, audio=True)
        self.characteristics = [self.control_rx, self.control_tx, self.audio_rx, self.audio_tx]

    def validate_peer(self, require_auth=False):
        connected = [path for path, props in self.devices.items()
                     if props.get("Connected", False)]
        props = self.devices.get(self.peer, {})
        if (connected != [self.peer] or not props.get("Paired")
                or not props.get("Bonded") or not props.get("Trusted")):
            self.safety.inhibit("BLE-peer-security")
            raise DBusError("org.bluez.Error.NotAuthorized", "single provisioned bonded trusted peer required")
        if require_auth and self.peer not in self.dispatcher.authenticated:
            raise DBusError("org.bluez.Error.NotAuthorized", "radio token required")

    def validate(self, options, require_auth=False):
        self.validate_peer(require_auth)
        device = options.get("device")
        if device is None or device.value != self.peer:
            raise DBusError("org.bluez.Error.NotAuthorized", "wrong device")
        if options.get("offset", Variant("q", 0)).value != 0:
            raise DBusError("org.bluez.Error.InvalidOffset", "offset unsupported")
        mtu = options.get("mtu", Variant("q", 0)).value
        if require_auth and mtu != self.audio.mtu:
            self.audio.stop()
            raise DBusError("org.bluez.Error.Failed", "MTU changed; restart audio")
        return self.peer, mtu

    def send_control(self, message):
        for frame in fragments(message, self.sequence):
            self.control_rx.send(frame)
        self.sequence = (self.sequence + 1) & 0xFFFF

    def credit(self):
        self.send_control({"v": 1, "id": "event", "path": "/audio/credit", "ok": True,
                           "data": {"txCredits": self.audio.credits,
                                    "txStreamId": getattr(self.audio, "tx_id", None)},
                           "error": None})

    async def start(self):
        self.bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        tree = await self.bus.introspect("org.bluez", "/")
        root = self.bus.get_proxy_object("org.bluez", "/", tree)
        self.object_manager = root.get_interface("org.freedesktop.DBus.ObjectManager")
        adapter_tree = await self.bus.introspect("org.bluez", self.adapter)
        adapter = self.bus.get_proxy_object("org.bluez", self.adapter, adapter_tree)
        self.gatt = adapter.get_interface("org.bluez.GattManager1")
        self.advertising = adapter.get_interface("org.bluez.LEAdvertisingManager1")
        self.bus.export(ROOT, Manager(self))
        self.bus.export(SERVICE_PATH, self.service)
        for characteristic in self.characteristics:
            self.bus.export(characteristic.path, characteristic)
        self.bus.export(ROOT + "/advertisement0", Advertisement())
        await self.refresh_devices()
        await self.gatt.call_register_application(ROOT, {})
        await self.advertising.call_register_advertisement(ROOT + "/advertisement0", {})

    async def refresh_devices(self):
        objects = await self.object_manager.call_get_managed_objects()
        self.devices = {
            path: {k: v.value for k, v in interfaces["org.bluez.Device1"].items()}
            for path, interfaces in objects.items() if "org.bluez.Device1" in interfaces
        }
        if self.peer in self.dispatcher.authenticated:
            try:
                self.validate_peer()
            except DBusError:
                self.dispatcher.disconnect(self.peer)
                self.assembler.reset()
                for characteristic in self.characteristics:
                    characteristic.notifying = False
                    characteristic.value = b""

    async def pump(self):
        try:
            while True:
                await asyncio.wait_for(self.refresh_devices(), 0.2)
                if (self.safety.fault != self.last_fault and self.control_rx.notifying
                        and self.peer in self.dispatcher.authenticated):
                    self.send_control({"v": 1, "id": "event", "path": "/fault", "ok": True,
                                       "data": {"reason": self.safety.fault,
                                                "rxDropped": self.audio.rx_dropped,
                                                "txFaults": self.audio.tx_faults},
                                       "error": None})
                    self.last_fault = self.safety.fault
                if self.audio.active and self.audio.rx:
                    self.audio.notify(self.audio_rx.send)
                await asyncio.sleep(0.005)
        except BaseException:
            self.dispatcher.disconnect(self.peer)
            raise

    async def close(self):
        self.dispatcher.disconnect(self.peer)
        if self.bus:
            try:
                await self.advertising.call_unregister_advertisement(ROOT + "/advertisement0")
                await self.gatt.call_unregister_application(ROOT)
            finally:
                self.bus.disconnect()
