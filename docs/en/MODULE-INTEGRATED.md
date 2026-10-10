# General assembly: combining standalone modules

## Select only what is needed

| Goal | Entry point |
| --- | --- |
| Antenna only, with external/manual radio | [MODULE-ANTENNA.md](MODULE-ANTENNA.md) |
| Rotor only, with the user's compatible antenna | [MODULE-ROTOR.md](MODULE-ROTOR.md) |
| SDR radio only, with external antennas/loads | [MODULE-RADIO.md](MODULE-RADIO.md) |
| Complete station | This document and [ASSEMBLY-MULTIMODE.md](ASSEMBLY-MULTIMODE.md) |

In the integrated assembly, the CM5 is shared by radio/rotor: do not count
two CM5s, two CM5IOs, or two power systems when combining standalone BOMs.
Removing a module does not authorize bypassing interlocks on which it
depends.

## Integration sequence

1. Separately complete and accept antenna mechanics/RF, rotor
   motion/sensors, and radio reception/audio.
2. Set up the tripod and fixed base. The CM5, radio, heatsinks, and external
   battery do not rotate with the antenna. Verify stability and CG.
3. Attach the antenna to the rotor through the removable interface; check
   three-axis load/travel, coax, and strain relief.
4. Interconnect band-specific SMA RF paths, a qualified circular network if
   used, and handedness selection independently of POL rotation. Keep TX
   inhibited.
5. Install Powerpole/fuse distribution, converters, and EMI filtering
   according to the frozen schematic; check voltage drops, temperature, and
   transients.
6. Select the `integrated` software profile when implemented, SDR
   identities, and local credentials. Do not auto-arm at startup.
7. Calibrate UTC/location, level/north, and AZ/EL/POL zero; test sensor,
   limit, clock, Bluetooth, process, and stop/watchdog faults.
8. Validate passes/map/radar and Doppler with real orbital data; test audio,
   SSTV/APRS, and visible error reporting before TX.
9. Qualify TX/full duplex with instruments and a load: both VHF/UHF
   directions, harmonics (145 x 3 = 435 MHz), blocking, and heating.
10. Weigh the operating assembly including tripod/cables, excluding only
    the external battery under the current decision; record battery mass
    separately. Verify <=5 kg and the two-hour runtime target by test.

## Illustrations, components, and issues

The [illustrated guide](ASSEMBLY-MULTIMODE.md) relates figures, component
IDs, external materials, and steps. Concept drawings are not machining
templates or production pinouts.
[TROUBLESHOOTING-MULTIMODE.md](TROUBLESHOOTING-MULTIMODE.md) covers
calculated issues, checks, and stop gates. Close price lists using specific
references/dates and distinguish reusable tools, consumables, shared parts,
and pending items. Current observations are in
[REFERENCE-PRICES.md](REFERENCE-PRICES.md) and
[reference-prices.csv](../../bom/reference-prices.csv). Do not add the
electronic subtotal to the electronic-plus-ASA subtotal: they are
alternatives. Budget the external battery even though it is excluded from
the 5 kg limit; its reference does not include the charger. Do not claim a
complete cost while categories remain pending or quantities are unapproved.

This index does not certify that physical integration has been tested.
[VALIDATION.md](VALIDATION.md), [ACCEPTANCE.md](ACCEPTANCE.md), and the
specific PCB/Gerber/BOM/CPL revision take precedence.
