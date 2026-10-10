# BricoHams PortableSatStation OS

## What this image is

This is a build recipe for a **64-bit Raspberry Pi OS Lite derivative**, named
**BricoHams PortableSatStation OS**. It is for the selected Compute Module 5
(CM5) installed on the official CM5 IO Board revision 2, plus the project's
GPIO-only auxiliary board. It is not a replacement Raspberry Pi OS release,
not an official Raspberry Pi product, and not a hardware-validated image.

The build uses the official Raspberry Pi `pi-gen` `arm64` branch at the full,
fixed commit recorded in [`os/pi-gen.commit`](../os/pi-gen.commit), and the
Trixie `stage2` Lite export. That pinned upstream stage is marked `-lite`.
`pi-gen` documents ARM64 builds on its `arm64` branch and currently defaults
to Trixie. Debian package repositories remain live so security fixes can be
installed; therefore this is a reproducible *recipe*, not a bit-for-bit
reproducible binary image. Record the emitted SHA-256 for each build.

The image intentionally retains Raspberry Pi OS `/etc/os-release`, upstream
package documentation, and first-boot account creation. BricoHams is a
separate console/login banner and image name only. The name Raspberry Pi OS
identifies the upstream base; it does not imply Raspberry Pi endorsement.
The current project authors and upstream notices are copied into
`/usr/share/doc/bricohams-os/`.

## Build on Linux

The Windows development environment does not assemble the Linux disk image.
Use a native Linux host or a Linux VM with Docker Engine, Git, rsync, coreutils,
and at least 60 GiB free on a native Linux filesystem (for example ext4, XFS,
or Btrfs). The build requires Internet access to the pinned Raspberry Pi
repository, Debian Trixie repositories, and the pinned Python package index
dependencies. Do not put pi-gen's work directory on NTFS, `/mnt/c`, a shared
Windows filesystem, or a path containing spaces.

From a clean Linux clone of this repository:

```bash
BUILD_ROOT=/var/tmp/bricohams-os-build \
  bash os/build-image.sh
```

`BUILD_ROOT` must not already contain a `pi-gen` checkout. The image archive
and adjacent `.sha256` file are written to `BUILD_ROOT/artifacts/`. Set
`OUTPUT_DIR` to another location if required. The script refuses to overwrite
an existing image or checksum, checks out the exact `pi-gen` commit, builds
with pi-gen's Docker path, checks the staged root filesystem for credentials
and host keys, and prints the archive checksum. It does **not** flash an SD
card or eMMC, alter a connected device, enable the radio service, or publish a
GitHub release.

The optional manual GitHub Actions image job uses the same recipe. It is
separate from automatic push/PR validation and uploads only the checked image
archive and checksum as a short-lived Actions artifact. Repository visibility
determines who can download Actions artifacts; only request that job if that
distribution is acceptable.

## Included runtime

The base image contains the local first-boot profile selector and build
prerequisites, not either application stack. After the upstream first-user
setup, its tty1 prompt requires an explicit choice: `rotor-only`, `radio-only`,
or `integrated`. It installs only that profile's Debian runtime packages and
project packages into `/opt/bricohams/venv`; radio executables/configuration
and the radio unit are installed only in profiles containing radio. Unselected
project source is removed after profile installation. No profile is silently
inferred.
Rotor-only does not install BlueZ, SoapySDR, LimeSuite, or the LMS7 plugin.
`integrated` installs both dependency sets but is not an operational
integration profile while the rotor provider is pending.

| First-boot selection | Installed stack | Operational boundary |
| --- | --- | --- |
| `rotor-only` | Rotor dependencies; no SDR stack | No motion service until the production CM5 BSP/adapter exists |
| `radio-only` | Radio/SDR dependencies only | Manual-frequency RX; TX stays inhibited pending physical-gate mapping |
| `integrated` | Both dependency sets | No integrated service; no fallback to manual if tracking is absent |
| Antenna-only | No host profile required | Mechanical/RF module is installed and qualified independently |

The profile selector checks the actual project package entry points with
`--help` and imports the SoapySDR Python binding only in radio-containing
profiles; it does not enumerate or initialize physical devices. The radio
systemd unit is copied into `/etc/systemd/system` only for `radio-only` and
`integrated`, and is never enabled by the selector. The project
package manifests remain the authority for API/package identity.
[`os/runtime-requirements.txt`](../os/runtime-requirements.txt) pins rotor's
Python runtime dependencies; [`os/build-requirements.txt`](../os/build-requirements.txt)
pins its PEP 517 build backend. See the independent
[rotor](../os/install/rotor-only.md), [radio](../os/install/radio-only.md),
[antenna](../os/install/antenna-only.md), and
[full-station](../os/install/full-station.md) installation guides.

The boot block is limited to the frozen CM5IO auxiliary-board bus map:

```ini
dtparam=i2c_arm=on
enable_uart=1
dtoverlay=spi1-3cs,cs0_pin=18,cs1_pin=17,cs2_pin=16
```

It enables I2C1 on BCM 2/3, SPI1 with CS0/CS1/CS2 on BCM 18/17/16, and the
GNSS UART pins BCM 14/15. The pinned pi-gen stage1 command line enables
`console=serial0,115200`; the image stage verifies and removes that exact
console token before using the pins for GNSS, retaining the local `tty1`
console. It deliberately does not enable or remap SPI0. The official
Raspberry Pi SPI1 overlay documents these chip-select defaults and
parameters. Confirm the actual CM5IO booted device nodes, UART alias, GPIO
permissions, and every peripheral readback on the assembled board before
connecting or energizing hardware.

The frozen revision-A software map is copied from
[`hardware/cm5/interface.json`](../hardware/cm5/interface.json) into the
image at `/usr/share/bricohams-os/cm5-interface.json`. The BCM mapping is
frozen; the auxiliary board remains not designed/fabricated/released. At
first boot, the local selector displays `gpiodetect` and asks the operator
to choose the actual `/dev/gpiochipN` after checking `gpioinfo` against the
CM5IO mapping. The OS deliberately does not assume the BCM controller is
`gpiochip0`.

After the local selector chooses a GPIO chip, a systemd safe-state holder
drives and holds BCM11 watchdog heartbeat LOW, BCM12 motor-arm request LOW,
BCM13 TCA9548A reset HIGH, and BCM22/23 PTT requests LOW. These are request
signals, not hardware permits: BCM11 does not establish a watchdog permit and
BCM12 does not itself gate motor power. The holder starts at boot only to
reassert fail-off request levels; this is not hardware commissioning and does
not home, arm, move, key PTT, or start transmission. It periodically
reasserts the inactive output values; systemd restarts it on provider errors.
A failed or recovering provider is not evidence of safety: independent
hardware pulls/gates must remain fail-off.

MCP23017 GPA0..GPA2 are per-axis enable *requests*. On expander reset or power
loss, its pins must return to inputs and external pulls must keep all three
requests deasserted. The OS does not write expander registers or treat those
request pins as hardware permits. BCM11/12 and expander-request defaults must
remain fail-off across cold boot, reboot, service restart, GPIO-provider
recovery, and expander reset/power loss. GPIO ownership/recovery or power loss
still depends on external default-off pulls and independent hardware;
software initialization is not a safety gate. No motion or transmission is
permitted until the independent safety circuits are designed, built, and
qualified.

The GPIO map used by the OS is: I2C1 BCM2/3; AZ/EL/POL NC limit pairs
BCM4/5, 6/7, 8/9; E-stop auxiliary monitor BCM10; watchdog output BCM11;
motor-arm request BCM12; TCA reset BCM13; UART0 TX/RX BCM14/15; SPI1 CS2/1/0
BCM16/17/18 and MISO/MOSI/SCLK BCM19/20/21; VHF/UHF PTT requests BCM22/23;
driver faults BCM24/25/26; and optional GNSS PPS BCM27. GPIO0/1 (physical
ID_SD/ID_SC) remain reserved. MCP23017 GPA0/1/2 are AZ/EL/POL enable requests
and GPA3 motor-permit feedback; GPA4/5 are PTT feedback and GPA6/7 PA faults.
The TCA9548A at I2C1 `0x70` uses channels 0/1/2 for the AS5600 encoders, 3
for the compass, and 4 for the IMU; the MCP23017 is at I2C1 `0x20`.

Only I2C1/SPI1/UART0 from the frozen map are configured; the build rejects
existing conflicting SPI/I2C/UART overlays or parameters rather than trying
to guess how to repair stale overlays. It preserves pi-gen's official CM5
`nospi10` overlay, which disables SPI0 aliases rather than assigning a bus. GPIO4..10 and 24..27 remain software
monitor inputs; they do **not** implement the required direct hardware limit
stop path or safety-rated E-stop/watchdog/EN/PTT circuits.

Power follows the frozen architecture: external 12 V nominal battery, excluded
from the 5 kg whole-station mass objective; CM5IO USB-C power input separate
from the USB data/host connection; and a conditional, negotiated 5 V/5 A
target that still requires CM5IO rating and full concurrent-load verification.
Never apply raw 12 V to CM5IO USB-C 5 V or its 40-pin 5 V rail. The target
does not claim a completed converter, PD contract, or qualified supply.

The hardware contract records an **ECO-WORTHY 12 V / 30 Ah LiFePO4** pack
(variant `40308275183822`) as a reference candidate only, not an approved or
procured pack. Confirm the delivered model, rated capacity, BMS/current limits,
and connectors from its exact documentation. Its 14.6 V full-charge figure is
provisional pending that confirmation; at least 30 V input-component rating
is only a preliminary stress-screening target, to be re-evaluated against the
verified pack voltage window and transients. The nominal 360 Wh calculation
applies only if 30 Ah is verified; the two-hour objective requires measured
whole-system battery-side average load and a justified usable-energy fraction.
Use the required isolated 5 V auxiliary-logic regulator and a separate motor
rail; their ratings and implementation remain unfrozen. The battery is
excluded from the 5 kg mass tally, but tripod and all other station equipment
remain in scope.

Only the radio-containing profiles install `bluez`, `python3-soapysdr`,
`soapysdr-tools`,
`soapysdr-module-lms7`, and Debian's LimeSuite tools for actual device
discovery. No BricoHams boot action flashes or updates Lime FPGA firmware;
inspect installed package notices and supported hardware procedure before
any manual firmware action.
No GPS daemon is configured to seize the GNSS UART. In radio-only mode,
BCM22/23 PTT request assignments are frozen but no GPIO-request flags are
passed to the daemon. The corresponding isolated outputs, physical
arm/PTT/independent RF-gate circuits, PA feedback and verified guard provider
are not implemented/tested. The host remains manual-frequency RX only and
cannot be treated as TX commissioned.

This image does not configure a station Wi-Fi access point or claim that the
project's web UI is installed as an offline control service. The operator
chooses network settings locally at first boot; in radio-only profile the
manually started host exposes its documented encrypted Bluetooth GATT
interface and localhost CAT endpoint.
The radio API's audio transport is signed S16LE, mono, 8,000-sample/s PCM;
this does not imply HFP/A2DP or a verified physical audio interface.

## First boot and profile selection

1. Use Raspberry Pi Imager's first-boot setup, or the upstream local setup
   wizard, to create the real operator account and configure the intended
   network. The upstream locked first-user placeholder is configured locally
   during first boot; no password, Wi-Fi profile, SSH key, BlueZ peer, radio
   token, serial number, or tracking source is baked into this image. SSH
   remains disabled unless an operator deliberately configures it.
2. After upstream first-user setup, the BricoHams selector runs on local tty1.
   Choose the explicit module profile and enter the existing local operator
   login. Profile installation needs network access to Debian and the pinned
   Python package index. Inspect `gpiodetect`/`gpioinfo`, then select the
   exact `/dev/gpiochipN` that exposes the frozen BCM offsets. The selected
   profile is retained as a pending marker if installation fails, preventing
   a retry from mixing dependency sets. `/etc/bricohams/profile` is recorded
   only after successful installation. No module service is enabled or
   started; a separate safe-state holder is started after the GPIO map check.
   If installation fails, read the console error, restore network access,
   and reboot to retry the same selector choice.
3. On the local console, verify the OS, selected profile, and interfaces:

   ```bash
   cat /etc/os-release
   cat /etc/bricohams/profile
   grep -A8 'BEGIN BRICOHAMS' /boot/firmware/config.txt
   grep -o 'console=[^ ]*' /boot/firmware/cmdline.txt
   ls -l /dev/spidev1.* /dev/i2c-1
   ```

   Device-node names are expectations to check, not proof of a working bus.
   The image does not home motors, move an axis, key PTT, start transmission,
   or flash device firmware on boot.
4. For `radio-only`, pair and trust the intended control device using local
   BlueZ tools. Read its actual `Device1` path from
   `busctl tree org.bluez /org/bluez`; discover the two real Lime devices with
   `portable-sat-radio --discover` or `SoapySDRUtil --find`. Discovery does
   not verify throughput, an antenna path, or RF safety.
5. In `radio-only`, write only non-secret identities to the root-owned config,
   readable only by the radio service group. The config tool validates the peer path,
   serials, and supported hardware-rate range; it does not pair devices,
   assert commissioning, or enable a unit:

   ```bash
   sudo bricohams-radio-config \
     --peer /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF \
     --vhf-serial ACTUAL_VHF_MINI_SERIAL \
     --uhf-serial ACTUAL_UHF_MINI_SERIAL \
     --hardware-rate 1000000
   ```

   Replace every example with locally discovered values. The unit is not
   enabled at boot; the config tool neither starts nor enables it. Its
   randomly generated authentication token is stored at
   `/var/lib/bricohams/radio/token` with private permissions; transfer it to
   a trusted client only over an operator-controlled local channel. Never put
   that token in this repository, a Wi-Fi file, or a build artifact.
   To change identities later, stop the unit, edit the non-secret JSON
   locally with `sudoedit /etc/bricohams/radio-host.json`, then restore
   owner/group/mode:

   ```bash
   sudo chown root:bricohams-radio /etc/bricohams/radio-host.json
   sudo chmod 0640 /etc/bricohams/radio-host.json
   ```

   The service validates the full schema again before each start.
   The radio service selects `STANDALONE_MANUAL`: no GNSS/rotor Doppler is
   assumed, and there is no tracking-loss fallback. After pairing and RX
   bench checks, an operator may explicitly start it with
   `sudo systemctl start bricohams-radio.service`; inspect its journal and
   status. Do not enable it at boot without a separate approved procedure.
   Manual TX remains inhibited. BCM22/23 request pins and MCP23017 feedback
   assignments are frozen, but isolated PTT outputs, physical arm/PTT and
   independent RF-gate circuits, PA feedback circuits, and the verified
   guard provider remain hardware/release blockers. The safe-state holder
   keeps both PTT requests LOW.
6. For `rotor-only`, the software package is isolated from SDR dependencies,
   but its production CM5 BSP/`open_adapter` is pending: no motion service is
   installed or started. For `integrated`, both packages are installed but
   the radio wrapper rejects startup; it cannot fall back to manual operation
   if tracking/rotor integration is absent. An antenna-only build needs no OS
   profile. Follow the separate profile guides linked above.

## Safety and validation boundary

The banner, bus overlays, and safe-state holder do not validate the board.
The custom-board documentation still requires direct hardware motor-limit
stop paths, independent motor-power cutoff, normally-closed limits,
E-stop/watchdog and per-axis EN verification, isolated PTT, selected TMC5160
board settings, encoder/sensor calibration, GNSS validation, RF filtering/
isolation, and measured RF tests. Software start, stop, status, or successful
SPI readback is not a substitute for independent hardware safety. The project
does not claim that the station has achieved its 5 W design objective, that
the CM5 can sustain both Lime USB streams, or that the complete station meets
its mass limit.

The rootfs stage fails if it sees saved Wi-Fi credentials, authorized SSH
keys, SSH host keys, a radio config/token, or an enabled radio unit. Upstream
`/usr/share/doc` notices are retained; pi-gen's BSD 3-Clause license is also
installed with the project notices. The BricoHams stage does not vendor
firmware or branding assets. Firmware/resources supplied by the official OS
or Debian packages retain their package notices. No script flashes or updates
Lime FPGA firmware; check the installed LimeSuite package notices and its
hardware-compatible update procedure before any manual firmware operation.

## Upstream references

- [Raspberry Pi OS and computer documentation](https://www.raspberrypi.com/documentation/)
- [Raspberry Pi Compute Module documentation](https://www.raspberrypi.com/documentation/computers/compute-module.html)
- [Official CM5 device-tree selection documentation](https://github.com/raspberrypi/documentation/blob/62ba0a0c2dd5030fe9b19458fa9bd174a451f79b/documentation/asciidoc/computers/compute-module/cm-peri-sw-guide.adoc)
- [Official Raspberry Pi pi-gen ARM64/Trixie source at the pinned commit](https://github.com/RPi-Distro/pi-gen/tree/d346cd53562b3c6b4f94c9155175f814258c456d)
- [Pinned pi-gen kernel command line](https://github.com/RPi-Distro/pi-gen/blob/d346cd53562b3c6b4f94c9155175f814258c456d/stage1/00-boot-files/files/cmdline.txt)
- [Raspberry Pi `enable_uart` and serial-console behavior](https://github.com/raspberrypi/documentation/blob/62ba0a0c2dd5030fe9b19458fa9bd174a451f79b/documentation/asciidoc/computers/config_txt/boot.adoc)
- [Official Raspberry Pi Linux SPI1 overlay documentation](https://github.com/raspberrypi/linux/blob/4103a989a46196239b830bd07693277e42b8f992/arch/arm/boot/dts/overlays/README)
- [Raspberry Pi CM5IO and auxiliary-board pin contract](CM5-PCB.md)
- [Linux radio host API and verification boundary](RADIO-HOST.md)
- [Linux rotor host API and verification boundary](CM5-ROTOR.md)
