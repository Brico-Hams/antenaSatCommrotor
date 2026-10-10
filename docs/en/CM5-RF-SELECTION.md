# CM5/RF selection: evidence, interfaces, and exclusions

Collection date: 2026-10-10. This record distinguishes a component's
documented capability, the architecture choice, and assembly performance
that requires bench verification. It is not a manufacturing release.

## Current architecture

CM5 with the purchased official CM5IO, original AZ/EL/POL auxiliary board,
and two replaceable LimeSDR Minis. Two concurrent VHF/UHF receivers; both
chains are TX-capable, but the initial policy permits only one active TX.
The new variant has no ESP32; retain the earlier design as historical.

| Item | Primary evidence | Limitation |
| --- | --- | --- |
| CM5 | [Official datasheet](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008180-DS-7-cm5-datasheet.pdf) | Check the exact RAM/eMMC/wireless variant, temperature, power consumption, and mounting |
| CM5IO | [Pinned official documentation](https://github.com/raspberrypi/documentation/blob/62ba0a0c2dd5030fe9b19458fa9bd174a451f79b/documentation/asciidoc/computers/compute-module/introduction.adoc) | Two native USB3 ports; qualify peripherals, current, and USB2 role in the complete assembly |
| LimeSDR Mini 2.x | [Pinned hardware documentation](https://github.com/myriadrf/LimeSDR-Mini-v2/blob/bcab0b65506c7c9dbee2a79a76a951aa8f1cd48d/docs/v2.4/index.rst) | 10 MHz-3.5 GHz; one RX/one TX per module, female SMA, 69 x 31.4 mm; verify weight of the exact revision |
| Lime full duplex | [Manufacturer page](https://www.crowdsupply.com/lime-micro/limesdr-mini-2) and [concurrent RX/TX example](https://github.com/myriadrf/LimeSuite/blob/699d05b7212aa612a9802c219dd6621be88c77db/src/examples/dualRXTX.cpp) | Module capability, not receiver immunity to its PA/antenna signal |
| Lime sample rates | [Pinned API](https://github.com/myriadrf/LimeSuite/blob/699d05b7212aa612a9802c219dd6621be88c77db/src/API/LimeSDR_mini.cpp) | This classic API advertises a range starting at 100 ksample/s; query the real device, do not assume 96 ksample/s RF |
| TMC5160 v1.5 | [Watterott pinout](https://learn.watterott.com/silentstepstick/pinconfig/tmc5160/) and [pinned schematic](https://github.com/watterott/SilentStepStick/blob/098b7518b0de31e6a12fda78c68ae2666b81fbb6/hardware/SilentStepStick-TMC5160_v15.pdf) | Check exact module straps/configuration/clock/current/cooling; these details do not apply to arbitrary StepSticks |

The 4 GB RAM/16 GB eMMC CM5 wireless variant is a purchasing candidate,
not a performance measurement or a required change for other models. Do not
infer the mass of the CM5, SDR, heatsink, or carrier from their dimensions.

## Deterministic motion and GPIO

Three independent ramp-generator drivers can let Linux request positions
without synthesizing STEP pulses in a nondeterministic loop. The proposed
SPI1 allocation uses GPIO16/17/18 for chip selects and GPIO19/20/21 for
MISO/MOSI/SCLK. I2C GPIO2/3 and UART GPIO14/15 are reserved for sensors and
GNSS. **This allocation is not an approved netlist**: the auxiliary board's
frozen and tested interface map takes precedence. Freezing a map does not
mean it has been physically tested.

For Watterott TMC5160 v1.5: open the SD_MODE jumper for the documented
motion-controller mode, SPI_MODE=VIO, SD_MODE=GND, VIO=3.3 V; EN high
disables outputs; CLK=GND selects the internal clock. CS needs an external
pull-up. DCO is an output, not nSLEEP. Check clock frequency and tolerance
for velocity/acceleration conversions. Do not apply these details to another
revision without checking its schematic.

CM5IO can select 1.8/3.3 V logic; the 3.3 V auxiliary board requires a
compatible configuration. Drivers do not replace NC limit switches,
encoders, homing, or a Linux-independent power cutoff/watchdog.

## USB, audio, and power

The two Lime units occupy the two native USB3 ports. An additional USB audio
codec requires a qualified host connection/powered hub; do not assume a
third port. An I2S alternative requires review for conflict with SPI1.
Link speed does not guarantee application throughput.

CM5IO documents 5 V/5 A power; at 5 V/3 A, peripherals are limited to
600 mA according to the cited documentation. Check the actual supply,
USB-C negotiation, and cable. An external 12 V LiFePO4 battery requires an
appropriate converter; do not connect 12 V to USB-C/the CM5 5 V rail.

Transparent Bluetooth audio at 8 ksample/s, S16LE mono, requires
128 kbit/s per direction and 256 kbit/s full duplex, before headers and
retries. Do not treat the ESP32's 20-byte BLE control frames as proof of
audio capability. The new interface, loss handling, and credit model are
described in [RADIO-HOST.md](RADIO-HOST.md); physical Android/CM5 testing
remains pending.

## Why the referenced devices are rejected as direct RF chains

- [(tr)uSDX](https://dl2man.de/) and
  [uSDX SOTA](https://antrak.org.tr/blog/usdx-sota-modular-all-mode-sdr-hf-transceiver-for-qrp-operations/)
  are HF references; their form factor/CAT does not establish 145/435 MHz
  capability.
- SA8x8 and equivalent FM solutions have no AM/USB implementation verified
  by this selection. Do not claim SSB merely because the app has a mode
  selector.
- RTL-SDR Blog V4 is receive-only; by itself it does not satisfy APRS/voice
  transmission.
- The Pluto's nominal lower limit of 325 MHz does not cover 145 MHz without
  modifications; do not treat an unsupported tuning range as guaranteed.
- The ATU-100 is an antenna tuner, not a duplexer, PA, or VHF/UHF transceiver.

The original licenses of referenced projects are not replaced by the new
work's MIT/CERN licenses. Official CM5IO source files are not redistributed
or adapted under an assumed unidentified open license; CM5IO is purchased
and its documentation is cited for study.

## RF power: separate blocker

Targets: 5 W FM, 5 W PEP USB, and 1 W AM carrier. Lime output is low power,
approximately +10 dBm maximum depending on revision/frequency; it is not
multiwatt output. Linear PAs and per-band filters remain subject to selection
and testing.

5 W is approximately 37 dBm; increasing from 10 dBm to 37 dBm requires an
ideal 27 dB gain before losses. This does not establish safe gain: consider
maximum gain, compression, IMD, transients, and independent drive limiting.
An AM carrier at 1 W with 100% modulation ideally reaches 4 W PEP; the chain
needs headroom and spectral verification. Do not reuse an HF class-E PA as a
linear USB amplifier.

145 MHz x 3 = 435 MHz: a VHF TX harmonic can fall in the UHF receiver band.
Two SDRs, a diplexer, and RHCP/LHCP selection do not prove isolation. With
appropriate loads and instruments, measure receiver desensitization,
blocking, harmonics, SWR, temperature, and IMD, starting at minimum power.
Do not switch an RF network under TX unless its specific rating has been
verified.

Reception, PTT permission, mechanical POL selection, and circular
polarization handedness are independent functions. Axial rotation does not
change RHCP/LHCP. Do not enable TX solely because a software response
succeeded: physical permission, a confirmed RF path, and verified feedback
from the actual chain are also required.
