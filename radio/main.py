"""Linux runtime. No test backend, no remote physical arm, no RF demo command."""

import argparse
import asyncio
import contextlib
import json
import logging
import signal
import struct
import sys
import threading
import time
from pathlib import Path

from .control import Cat, Dispatcher, private_token
from .dsp import Demodulator, Modulator
from .protocol import Audio
from .safety import Safety
from .soapy import discover

LOG = logging.getLogger("radio")


class Physical:
    """Local gpiod v2 lines: active-high arm/PTT; independent active-high RF gate."""
    def __init__(self, chip, arm, ptt, gate, safety):
        import gpiod
        from gpiod.line import Direction, Value, Bias
        if len({arm, ptt, gate}) != 3:
            raise ValueError("GPIO arm/PTT/gate lines must differ")
        self.Value = Value
        self.arm, self.ptt, self.gate, self.safety = arm, ptt, gate, safety
        self.lines = gpiod.request_lines(chip, consumer="portable-sat-radio", config={
            (arm, ptt): gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_DOWN),
            gate: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        })
        self.running = True
        self.thread = threading.Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def monitor(self):
        try:
            while self.running:
                arm = self.lines.get_value(self.arm) == self.Value.ACTIVE
                ptt = self.lines.get_value(self.ptt) == self.Value.ACTIVE
                if not arm or not ptt:
                    self.lines.set_value(self.gate, self.Value.INACTIVE)
                self.safety.physical(arm, ptt)
                enabled = self.safety.check() and self.safety.transmitting
                self.lines.set_value(self.gate, self.Value.ACTIVE if enabled else self.Value.INACTIVE)
                time.sleep(0.01)
        except BaseException:
            self.safety.physical_arm = False
            self.safety.physical_ptt = False
            with contextlib.suppress(Exception):
                self.lines.set_value(self.gate, self.Value.INACTIVE)
            with contextlib.suppress(Exception):
                self.safety.inhibit("GPIO-fault")

    def close(self):
        self.running = False
        self.lines.set_value(self.gate, self.Value.INACTIVE)
        self.thread.join(timeout=1)
        self.lines.release()


async def run(args):
    from .bluez import BlueZ
    if sys.platform != "linux":
        raise RuntimeError("hardware runtime requires Linux BlueZ/gpiod/SoapySDR")
    backend = None
    physical = None
    ble = None
    server = None
    rotor = None
    radio_gpio = None
    tasks = []
    stopped = asyncio.Event()
    def stop_tx():
        if physical:
            physical.lines.set_value(physical.gate, physical.Value.INACTIVE)
        if backend:
            backend.stop_tx()

    safety = Safety(stop_tx)
    safety.allowed_profile = args.operation_profile
    safety.operation_profile = args.operation_profile
    audio = Audio(safety.inhibit)
    dispatcher = Dispatcher(safety, audio, private_token(Path(args.token_file)))
    # Local SGP4 or authenticated upstream integration provisions TrackingInput.
    # No orbit source is trusted automatically by the radio runtime.
    try:
        if args.radio_gpio:
            if args.gpio_chip:
                raise ValueError("production revision-A requests cannot share generic GPIO mode")
            from .gpio_production import open_production
            # No external safety circuit provider exists yet. Do NOT infer it
            # from output GPIO or a mutable configuration commissioning flag.
            radio_gpio = open_production(args.radio_gpio, args.gpio_contract, guard=None)
        if args.operation_profile == "STANDALONE_MANUAL" and args.rotor:
            raise ValueError("standalone manual radio has no rotor dependency; run rotor separately")
        if args.rotor:
            from .rotor_integration import RotorIntegration, open_rotor
            rotor = RotorIntegration(open_rotor(args.rotor), safety, dispatcher.tracking_input)
            with contextlib.suppress(ValueError, PermissionError, KeyError, TypeError):
                rotor.refresh()
            dispatcher.rotor = rotor
        if args.radio_count == 1:
            if args.operation_profile != "STANDALONE_MANUAL" or args.single_channel is None:
                raise ValueError("one radio requires explicit standalone profile and single channel")
            selected = args.vhf_serial if args.single_channel == "VHF" else args.uhf_serial
            other = args.uhf_serial if args.single_channel == "VHF" else args.vhf_serial
            if not selected or other:
                raise ValueError("single radio requires exactly its explicit serial, not fallback")
            from .dual import DualLime
            backend = DualLime(args.vhf_serial, args.uhf_serial, args.hardware_rate,
                               single_channel=args.single_channel)
            safety.available_channels = backend.channels
            safety.rx_channel = safety.tx_channel = args.single_channel
            safety.rx_hz = safety.tx_hz = 145900000 if args.single_channel == "VHF" else 435100000
            safety.profile_status = backend.status
        elif args.vhf_serial and args.uhf_serial:
            from .dual import DualLime
            backend = DualLime(args.vhf_serial, args.uhf_serial, args.hardware_rate)
            safety.profile_status = backend.status
        elif args.vhf_serial or args.uhf_serial:
            raise ValueError("two explicit unique VHF/UHF Lime Mini serials required")
        elif args.single_channel:
            raise ValueError("--single-channel requires explicit one-radio build, not auto fallback")
        if backend and radio_gpio:
            backend.rf_guard = radio_gpio
        if args.gpio_chip is not None:
            if any(x is None for x in (args.arm_line, args.ptt_line, args.gate_line)):
                raise ValueError("all three physical GPIO lines required")
            physical = Physical(args.gpio_chip, args.arm_line, args.ptt_line, args.gate_line, safety)
        ble = BlueZ(dispatcher, audio, safety, args.peer)
        await ble.start()
        server = await Cat(safety).listen(args.cat_port)
        if backend:
            backend.start_receivers()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, stopped.set)
        tasks = [asyncio.create_task(ble.pump()), asyncio.create_task(dual_radio_loop(
            backend, safety, audio, ble
        )), asyncio.create_task(stopped.wait())]
        if rotor:
            tasks.append(asyncio.create_task(rotor.pump()))
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            task.result()
    finally:
        safety.sdr_ready = False
        # Drop external gate before any potentially failing driver call.
        if physical:
            physical.close()
        with contextlib.suppress(Exception):
            safety.inhibit("shutdown")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        if server:
            server.close()
            await server.wait_closed()
        if ble:
            with contextlib.suppress(Exception):
                await ble.close()
        if backend:
            backend.close()
        if rotor:
            rotor.close()
        if radio_gpio:
            radio_gpio.close()


async def radio_loop(backend, safety, audio, ble, clock=time.monotonic):
    """Single-chain test harness retained solely for isolated starvation tests."""
    mode = safety.mode
    demod, mod = Demodulator(mode), Modulator(mode)
    last_audio = None
    stream_id = None
    while True:
        safety.check()
        if backend is None:
            safety.sdr_ready = False
            await asyncio.sleep(0.01)
            continue
        try:
            if mode != safety.mode or stream_id != getattr(audio, "tx_id", None):
                mode, stream_id = safety.mode, getattr(audio, "tx_id", None)
                demod, mod = Demodulator(mode), Modulator(mode)
                last_audio = None
            frequencies = safety.frequencies()
            if frequencies != (backend.rx_hz, backend.tx_hz):
                safety.tuning = True
                safety.inhibit("Doppler-or-CAT-retune")
                backend.tune(*frequencies)
                safety.tuning = False
            # Native calls have 10ms timeout; gate watchdog runs independently.
            iq = await asyncio.to_thread(backend.receive)
            safety.sdr_ready = backend.ready
            pcm = demod.process(iq)
            if pcm:
                audio.enqueue_rx(struct.pack("<" + "h" * len(pcm), *[
                    round(max(-1, min(1, x)) * 32767) for x in pcm
                ]))
            if safety.check() and audio.active:
                packet = audio.consume()
                if packet is None:
                    if last_audio is not None and clock() - last_audio > 0.05:
                        safety.inhibit("TX-PCM-gap")
                        audio.stop()
                        ble.credit()
                else:
                    samples = struct.unpack("<" + "h" * (len(packet) // 2), packet)
                    output = mod.process([x / 32768 for x in samples])
                    if safety.check():
                        safety.transmitting = True
                        await asyncio.to_thread(backend.transmit, output, safety.check)
                        last_audio = clock()
                    ble.credit()
            else:
                # Unkeyed microphone frames must not become stale future RF audio.
                if audio.consume() is not None:
                    ble.credit()
            await asyncio.sleep(0)
        except BaseException as error:
            safety.sdr_ready = False
            safety.tuning = False
            safety.inhibit("radio-loop-fault")
            LOG.error("radio stopped: %s", error)
            raise


async def dual_radio_loop(backend, safety, audio, ble, clock=time.monotonic):
    demods = {channel: Demodulator(safety.mode) for channel in ("VHF", "UHF")}
    mod = Modulator(safety.mode)
    lifecycle = None
    last_audio = None
    while True:
        safety.check()
        if backend is None:
            safety.sdr_ready = False
            await asyncio.sleep(0.01)
            continue
        try:
            new_lifecycle = (safety.mode, getattr(audio, "tx_id", None),
                             safety.rx_channel, safety.tx_channel)
            if new_lifecycle != lifecycle:
                lifecycle = new_lifecycle
                demods = {channel: Demodulator(safety.mode) for channel in ("VHF", "UHF")}
                mod = Modulator(safety.mode)
                last_audio = None
            rx, tx = safety.frequencies()
            vhf, uhf = (rx, tx) if safety.rx_channel == "VHF" else (tx, rx)
            channels = tuple(backend.chains)
            if len(channels) == 1:
                chain = backend.chains[channels[0]]
                if (rx, tx) != (chain.rx_hz, chain.tx_hz):
                    safety.tuning = True
                    safety.inhibit("single-manual-retune")
                    backend.tune_single(rx, tx)
                    safety.tuning = False
            elif ((vhf, uhf) != (backend.chains["VHF"].rx_hz, backend.chains["UHF"].rx_hz)):
                safety.tuning = True
                safety.inhibit("dual-Doppler-or-CAT-retune")
                backend.tune(vhf, uhf)
                safety.tuning = False
            # Both RX queues are consumed continuously, even if only one audio
            # source is selected. There is no implicit summing/mixing.
            for channel in channels:
                iq = await asyncio.to_thread(backend.receive, channel)
                pcm = demods[channel].process(iq)
                if channel == safety.rx_channel and pcm:
                    audio.enqueue_rx(struct.pack("<" + "h" * len(pcm), *[
                        round(max(-1, min(1, value)) * 32767) for value in pcm]))
            safety.sdr_ready = backend.ready
            packet = audio.consume()
            if safety.check() and audio.active:
                if packet is None:
                    if last_audio is not None and clock() - last_audio > 0.05:
                        safety.inhibit("TX-PCM-gap")
                        audio.stop()
                        ble.credit()
                else:
                    values = struct.unpack("<" + "h" * (len(packet) // 2), packet)
                    iq = mod.process([x / 32768 for x in values])
                    if safety.check():
                        safety.transmitting = True
                        await asyncio.to_thread(backend.transmit, safety.tx_channel, iq, safety.check)
                        last_audio = clock()
                    ble.credit()
            elif packet is not None:
                ble.credit()
            await asyncio.sleep(0)
        except BaseException:
            safety.sdr_ready = False
            safety.tuning = False
            safety.inhibit("dual-radio-loop-fault")
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover", action="store_true", help="Read actual Soapy advertisements; no TX")
    parser.add_argument("--vhf-serial", help="exact discovered LimeSDR Mini VHF serial")
    parser.add_argument("--uhf-serial", help="different discovered LimeSDR Mini UHF serial")
    parser.add_argument("--hardware-rate", type=int, default=1000000,
                        help="hardware IQ rate; exact advertised/readback required (default1MSPS)")
    parser.add_argument("--peer", help="provisioned bonded BlueZ Device1 path")
    parser.add_argument("--rotor", help="explicit v1 RotorController integration config path")
    parser.add_argument("--radio-gpio", help="root-owned revision-A production request config (hardware HOLD)")
    parser.add_argument("--gpio-contract", default="hardware/cm5/interface.json",
                        help="frozen revision-A interface contract")
    parser.add_argument("--operation-profile", choices=("STANDALONE_MANUAL", "INTEGRATED_TRACKING"),
                        default="INTEGRATED_TRACKING", help="local policy; never tracking-loss fallback")
    parser.add_argument("--radio-count", type=int, choices=(1, 2), default=2)
    parser.add_argument("--single-channel", choices=("VHF", "UHF"))
    parser.add_argument("--token-file", default="~/.local/state/portable-sat-radio/token")
    parser.add_argument("--cat-port", type=int, default=4532)
    parser.add_argument("--gpio-chip")
    parser.add_argument("--arm-line", type=int)
    parser.add_argument("--ptt-line", type=int)
    parser.add_argument("--gate-line", type=int)
    args = parser.parse_args()
    if args.discover:
        print(json.dumps(discover(), indent=2))
        return
    if not args.peer:
        parser.error("--peer provisioned bonded device required")
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(run(args))
    except (Exception, KeyboardInterrupt) as error:
        LOG.error("Radio host unavailable: %s", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
