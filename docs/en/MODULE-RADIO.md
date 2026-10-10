# Standalone module: CM5 SDR radio

## Scope and dependencies

The radio can be built without the rotor or a project-specific antenna,
using compatible external antennas or test loads. It uses a CM5/CM5IO, two
LimeSDR Minis, audio, and protected power. The target output powers require
additional PAs/filters; they are not the output power of the bare SDR.

| Required | Optional or mode-dependent |
| --- | --- |
| CM5/CM5IO, two SDRs identified by serial number, USB/cooling, and power | Mechanical rotor and its three drivers |
| 50-ohm SMA RF paths, receiver protection, and filtering | Project portable antenna |
| Bluetooth PCM audio and mic/speaker if used | GNSS/SGP4/rotor for automatic Doppler |
| Physical TX permit, watchdog, fuses, and qualified TX RF path | Circular RHCP/LHCP networks |
| Linear PAs/filters/suitable load for the 5 W target | External K1 instead of integrated audio |

[RADIO-HOST.md](RADIO-HOST.md) documents interfaces and tests;
[CM5-RF-SELECTION.md](CM5-RF-SELECTION.md) records component evidence.
[ANDROID-DIGITAL.md](ANDROID-DIGITAL.md) distinguishes DSP, generated audio,
transmission, and remote ACK. Do not conflate them.

## Module components and costs

[REFERENCE-PRICES.md](REFERENCE-PRICES.md) and
[reference-prices.csv](../../bom/reference-prices.csv) retain prices and
pending items. Select CM5/CM5IO, SDR x2, and the required RF, AUDIO,
USB-DATA, COOLING, and power categories. Motion sensors, motors, and rotor
mechanics are not mandatory purchases for radio-only operation. Physical TX
permit and its watchdog remain mandatory for TX: removing the motors does
not permit removing protection. The RF BOM above does not automatically
include qualified multimode linear PAs or the full expansion budget.

## Standalone assembly and configuration

1. Select CM5/CM5IO/Lime revisions; record both unambiguous serial numbers
   and VHF/UHF assignments. Do not select the first USB device found.
2. Mount components on a fixed, ventilated base with suitable fasteners and
   shielding; with both USB3 ports occupied, define the audio connection.
3. Prepare external Powerpole/fuse distribution, CM5 regulation, and RF
   branches. Measure voltage/polarity before connecting the computer/SDRs.
4. Prepare SMA cables/terminations, preselection, and RX protection. Remain
   in receive mode without a PA and verified RF path.
5. Install the radio-only profile and the host's published dependencies.
   Configure USB identities and private credentials locally.
6. Verify discovery, sample rates/frequencies read back from hardware, and
   two concurrent RX streams. A requested sample rate is not a verified
   actual rate.
7. Explicitly select the VHF/UHF audio channel and test Bluetooth
   PCM/credits/loss; do not mix SSTV/APRS tones from two receivers.
8. Configure authorized manual frequency/mode. Standalone mode must not
   pretend to have orbital position or enable Doppler without valid data.
9. Test DSP with WAV/test vectors, then real reception. Configure
   mic/speaker/K1 audio only after verifying pinout, bias, and level.
10. For TX, qualify the PA/filters, load, spectrum, temperature, and
    physical permit/watchdog/lease path. Start at minimum power; only one
    TX may be active at a time.

## Mode separation

Receive/manual operation must not depend on the rotor. Automatic Doppler
requires a real, fresh, verified orbital data source, UTC, and station
location; loss of that source must not silently switch to manual
transmission. Actual standalone support must be verified against host code
and tests; this document does not claim it is finished. The 5 W FM, 5 W PEP
USB, and 1 W AM targets still require measurement.
