# Rotor-only OS installation

The first-boot profile installer offers `rotor-only`. It installs the rotor
Python package and its pinned runtime requirements (`sgp4`, `smbus2`,
`pyserial`, and Linux `spidev`), plus the Linux GPIO/I2C/SPI support packages.
It does **not** install BlueZ, SoapySDR, LimeSuite, LimeSDR plugins, or radio
host services, radio executables, or the radio systemd unit.

1. Complete Raspberry Pi Imager's local first-user setup and network choice.
2. On the local console, choose **1) rotor-only** in the BricoHams profile
   selector. Enter the login of the existing local operator account. Package
   installation requires network access to Debian and the pinned Python
   package index.
3. Reboot or sign in again so the operator account receives the GPIO, I2C,
   SPI, and serial-device groups. Verify the CM5IO device nodes against the
   actual board before connecting hardware. The selector asks for the exact
   `/dev/gpiochipN`; use `gpiodetect` and `gpioinfo` to match BCM offsets to
   the frozen contract. The OS safe-state holder keeps the arm and watchdog
   requests inactive and holds those lines. Taking ownership requires a
   future approved runtime/service change; the current image does not enable
   motion.
4. The package currently has no production CM5 BSP/`open_adapter` provider.
   `portable-sat-rotor --config ...` reports that missing provider; it is not
   a usable motion service yet. The profile never enables a motion unit,
   homes an axis, or moves a motor. Do not create a fake adapter or test
   movement with an unqualified board.

The profile is useful for keeping the rotor Python/runtime dependency set
separate from the SDR stack. It is not a commissioning claim. See
[`../../docs/MODULE-ROTOR.md`](../../docs/MODULE-ROTOR.md),
[`../../docs/CM5-ROTOR.md`](../../docs/CM5-ROTOR.md), and
[`../../docs/CM5-PCB.md`](../../docs/CM5-PCB.md) for module and hardware gates.
