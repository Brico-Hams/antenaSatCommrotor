# Full-station OS installation

The first-boot **integrated** profile installs both the rotor and radio
dependency sets. It is currently a dependency-install profile only, **not an
operational integrated station**: the production rotor `open_adapter`
binding and implementation/validation of the physical arm/PTT, independent
RF-gate, direct limit-stop, watchdog, and E-stop circuits are pending. The
installer explicitly reports this and does not enable or start either
service. The integrated radio wrapper rejects the profile rather than
silently switching to manual operation.

1. Complete Raspberry Pi Imager's local first-user setup and network choice.
2. Choose **3) integrated** at the local BricoHams profile selector. Enter
   the existing local operator login. Match the actual GPIO controller with
   `gpiodetect`/`gpioinfo`; do not assume `gpiochip0`. Installation needs
   Debian and the pinned Python package index.
3. Complete each module's separate mechanical, electrical, antenna, and RF
   installation/acceptance steps. Installing both Python packages is not a
   substitute for those checks.
4. Keep motion and transmission disabled until the production BSP/adapter,
   tracking-source freshness/revocation behavior, physical gate wiring,
   watchdog, E-stop, limits, and independent fail-off circuits have been
   implemented and individually tested.
5. Do not use integrated mode without verified live tracking. Tracking loss
   must inhibit operation; it must never fall back to standalone manual
   transmit. The profile selector is intentionally one-shot. To use
   `radio-only` instead, prepare a separate image/install and select that
   profile before provisioning; do not change the integrated marker by hand.

See the independent [rotor](rotor-only.md), [radio](radio-only.md), and
[antenna](antenna-only.md) installation guides and
[`../../docs/ASSEMBLY-MULTIMODE.md`](../../docs/ASSEMBLY-MULTIMODE.md). No
single integrated commissioning procedure is claimed complete.
