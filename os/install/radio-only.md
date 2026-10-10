# Radio-only OS installation

The first-boot profile installer offers `radio-only`. It installs the radio
Python package and only its host dependencies: BlueZ, ALSA utilities,
SoapySDR, LimeSuite/LMS7 support, NumPy/SciPy, DBus, and GPIO support. It
does not install the rotor Python package, `sgp4`, or a rotor service.

1. Complete Raspberry Pi Imager's local first-user setup and network choice.
2. On the local console, choose **2) radio-only** in the BricoHams profile
   selector. Enter the login of the existing local operator account. Match
   the actual GPIO controller with `gpiodetect`/`gpioinfo`; do not assume
   `gpiochip0`. Package installation requires network access to Debian and the
   pinned Python package index.
3. Pair the intended Bluetooth control device locally and discover the real
   Lime serials. Configure the identity file with `sudo bricohams-radio-config`
   using the exact locally observed values. This writes identities only; it
   does not start or enable a service.
4. Review the radio host documentation and bench requirements before
   explicitly starting `bricohams-radio.service`. Its unit wrapper selects
   `STANDALONE_MANUAL`; frequencies are operator selected. It does not invent
   GNSS/rotor tracking and does not fall back from lost tracking.
5. TX remains inhibited and uncommissioned. BCM22/23 request and MCP23017
   feedback pins are frozen in revision A, but the physical arm/PTT inputs,
   isolated outputs, independent RF gate, PA feedback circuits, and verified
   guard provider are not implemented/tested. The OS safe-state holder keeps
   both requests LOW; a frozen pin map does not establish working hardware.

See [`../../docs/MODULE-RADIO.md`](../../docs/MODULE-RADIO.md) and
[`../../docs/RADIO-HOST.md`](../../docs/RADIO-HOST.md). SDR discovery is not
proof of RF path, stream stability, safe transmit, or regulatory compliance.
