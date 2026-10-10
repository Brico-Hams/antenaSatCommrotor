# Original Modular Carrier — PortableSatStation, Revision A

Current authors: **Anatol EA5KAO, Diego EA5JEF, and Pedro Roca Molina**.
See `AUTHORS.md`, `ACKNOWLEDGEMENTS.md`, and `DISCLAIMER.md`: this authorship
applies to original project work, not cited modules, tools, or publications.
The educational reference to [Bricohams](https://bricohams.org) does not imply
commercial endorsement of manufacturers. Work with children/adolescents
requires competent adult supervision; this prototype is not a toy. Do not
transmit without applicable authorization/licence.

## Delivery status and limits

Original **carrier-board** design, not a copy of a commercial controller.
Editable sources: `hardware/PortableSatCarrier.kicad_sch`, `.kicad_pcb`,
`.kicad_pro`, local `.kicad_sym` library and `.pretty` footprints; auditable
generator `hardware/generate-carrier.cjs`. Copper layers are not replaced with
drawings. Gerbers come from KiCad CLI; holes from its Excellon exporter.
`fabrication/PortableSatCarrier-Gerbers-CAD-VERIFIED-NOT-RELEASED.zip`
contains only the seven real Gerber layers, two Excellon files, and Gerber job;
it contains no decorative drawings and does not replace fabrication notes.
**NOT-RELEASED** is intentional: do not send this ZIP to production until the
formal blockers for this revision are cleared.
See **`fabrication/release-status.json`**, ERC/DRC reports, and their hashes:
the existence of a file does not mean it is production-authorized.

**Prototype not assembled or tested. Assembly/use HOLD until the physical and
power verification items below are closed.** ERC/DRC check CAD rules only;
they do not certify safety, RF immunity, temperature, or physical fit of
third-party modules. Symbols represent replaceable modules with passive pins:
ERC does not validate their internal regulators, voltage limits, or firmware.

## Actual electrical architecture

```text
Protected commercial 12 V supply (NOT bare battery / NOT integrated charger)
  + -- external main DC switch -- J1.1 RAW12
                                       |
                             D1 SB560 (anode->cathode)
                                       |
                                 PROTECTED12
                                       |
                    F1 SPT T3.15 A -- FUSED12 -- D2 SMBJ15A -- GND
                        |                  |
                   F2 T2.5 A           F4 T1 A
                        |                  |
                 J2.1 STOP_SEND       J4.1 BUCK12 -> external buck VIN
                        |              J4.2 GND -> buck GND
      external NC POWER contact                    |
      maintained/latching pushbutton          Pololu D24V22F5
      >=5 A BREAK at 12 V DC                      |
                        |                 VOUT -> J5.1 BUCK5
                  J2.2 VMOT                 GND -> J5.2 GND
                        |                         |
                 C1/C2 220u/35 V              F3 T1 A
                        |                         |
               U2/U3 VM -> motors         JP1 removable link
                        |                         |
                       GND                 U1 5V (ESP5)
                                                   |
                                           U1 regulator -> 3V3
                                                sensors + VIO/MS1/MS2

Second isolated NC contact of same button: J3.1 STOP_N -- NC -- J3.2 GND
R2: 10k from STOP_N to 3V3. Open=HIGH=fault; normal=LOW.
```

J2 is **not a GPIO input**: both terminals are positive power-branch conductors.
The full current of both drivers passes through F2, J2, and the external wire/
contact. Use >=0.75 mm² short copper wire with strain relief and terminals/
contacts with documented DC rating. Do not use a signal JST, Dupont, breadboard,
or low-current auxiliary contact in this circuit. Do not jumper J2 for operation.
The external latching button physically disconnects VMOT even if MCU, Wi-Fi, or
firmware locks up; logic/web remain powered upstream of the cutoff. The circuit
stays open while the button is latched. J2.2 actually supplies both drivers;
the path does not depend on a software-controlled relay.

This is not sold as a certified emergency stop. Capacitors retain energy after
opening: measure VMOT decay and actual stopping time. Releasing the latch restores
VMOT: **manually reset and deliberately re-arm the controller** before movement.
If a separate electrical reset is required to stay latched after releasing the
button, this revision does NOT provide it; use an externally certified
contactor/reset control, not a GPIO.

**D2 is downstream of F1**: F1 limits the branch if a TVS fails short. Also
require short-circuit protection/fuse at the source and on the positive cable,
close to the source. Do not connect a battery without that external fuse. D1
blocks reverse polarity, not sustained overvoltage. Use regulated 12 V, 13.8 V
normal maximum; **do not use 24 V**, even if a driver permits it.
SMBJ15A: 15 V standoff, nominal maximum clamp 24.4 V at test pulse; Watterott
specifies VM 5.5–28 V. Cable spikes and regeneration require measurement: a TVS
does not make every supply compatible.

F1/F2/F3/F4 are Schurter SPT 5x20 ceramic time-delay fuses, part numbers
0001.2509 (3.15 A), 0001.2508 (2.5 A), and two 0001.2504 (1 A).
SPT datasheet: 250 VAC / 300 VDC for these values, with DC breaking capacity
specified by manufacturer; do not substitute a fuse rated only for AC.
OGN holder 0031.8201: 22.5 mm pitch, included central NPTH support 2.7 mm.
Values are initial prototype values, not selectivity proof.

## EXACT modules, orientation, and connections

### U1: Espressif ESP32-DevKitC V4, ESP32-WROOM-32E, 38 pins

Not suitable for a generic 30-pin DevKit, C3, S3, or board with different spacing.
Two 19-pin female rows, **2.54 mm** pitch, **25.40 mm** center spacing.
Top view; USB points downward and antenna toward the top edge:

```text
             ANTENNA / no metal or copper beneath antenna
 left x=77 mm                         right x=102.4 mm
  1 3V3        20 GND
  2 EN NC      21 IO23 NC
  3 VP/IO36    22 IO22
  4 VN/IO39    23 TX0 NC
  5 IO34       24 RX0 NC
  6 IO35       25 IO21
  7 IO32       26 GND
  8 IO33 NC    27 IO19
  9 IO25       28 IO18
 10 IO26       29 IO5 NC
 11 IO27       30 IO17
 12 IO14       31 IO16
 13 IO12 NC    32 IO4 NC
 14 GND        33 IO0 NC
 15 IO13       34 IO2 NC
 16 SD2 NC     35 IO15 NC
 17 SD3 NC     36 SD1 NC
 18 CMD NC     37 SD0 NC
 19 5V         38 CLK NC
                    USB
```

NC means deliberately unconnected to the carrier and marked NC in schematic;
flash/strapping pins are not used. NC nets in CAD are not connected to each other.

| Function | GPIO | Polarity / voltage |
|---|---:|---|
| AZ STEP / DIR | 26 / 27 | 3.3 V logic |
| EL STEP / DIR | 14 / 13 | 3.3 V logic |
| Common ENABLE | 25 | Active LOW; R1 10k to 3V3 disables on startup |
| Stop monitor | 34 | NC to GND, open HIGH; external pull-up |
| AZ min / max | 35 / 36 | NC to GND, open HIGH; external pull-up |
| EL min / max | 39 / 32 | NC to GND, open HIGH; external pull-up |
| ESP RX from GNSS / ESP TX to GNSS | 16 / 17 | 3.3 V UART, NOT RS232 or 5 V TTL |
| AZ SDA / SCL | 21 / 22 | I2C0, 3.3 V |
| EL SDA / SCL | 18 / 19 | Separate I2C1 bus, 3.3 V |

GPIO34–39 have no internal pull-ups: R2–R6 are physically on the board.
No 12/24 V industrial input drivers are included.
Remove JP1 **before** connecting USB power: Espressif declares USB, external 5 V,
and external 3V3 mutually exclusive. Never power by two methods. Carrier 3V3
comes only from the DevKit regulator; there is no second regulator in parallel.
Initial maximum external budget: **100 mA** (sensors+GNSS+VIO); measure voltage
drop/temperature while Wi-Fi transmits. Actual capacity depends on selected
DevKit and GNSS.

The buck has NO assumed module footprint or pinout on this board: install
separately and connect only labeled VIN, GND, and VOUT pads of the
**Pololu D24V22F5**. J4.1=VIN, J4.2=GND, J5.1=VOUT 5V, J5.2=GND; leave module
EN and PG unconnected per its documentation. Do not substitute D24V25Fx:
manufacturer warns its pinout differs. Its physical pad positions do not define
carrier placement. Reverse/short/thermal protection belongs to the selected
buck module; verify its output is 5 V before connecting J5/ESP. No GPIO or
sensor connector on the carrier carries BUCK5/FUSED5/ESP5.

### U2/U3: Watterott SilentStepStick TMC2209 **v2.x**

Do not assume interchangeability with A4988 or BTT clones. Female sockets,
two rows of eight, 2.54 mm pitch, 15.24 mm spacing. Top view; left/right pins
start at the top of the manufacturer's drawing:

| Carrier pad | Left | Carrier pad | Right |
|---:|---|---:|---|
| 1 | EN=ENABLE_N | 9 | VM=VMOT |
| 2 | MS1=3V3 | 10 | GND |
| 3 | MS2=3V3 | 11 | M2B |
| 4 | SPREAD=GND | 12 | M2A |
| 5 | PDN_UART NC | 13 | M1A |
| 6 | PDN_UART NC | 14 | M1B |
| 7 | STEP | 15 | VIO=3V3 |
| 8 | DIR | 16 | GND |

MS1=MS2=HIGH and SPREAD=LOW: **1/16**, 1/256 interpolation, stealthChop.
Module has internal PDN_UART pull-down; retain factory jumper, do not convert
to UART or cut SPREAD. Driver DIAG/INDEX auxiliaries are unconnected: no
StallGuard/sensorless homing is implemented. Reference reduction is 25:1;
confirm final mechanical variant and actual microstepping before calibrating
steps/degree.

JM1/JM2, left to right: M2B, M2A, M1A, M1B. M2B/M2A are one coil; M1A/M1B the
other. Measure with an ohmmeter while unpowered. Never plug/unplug a motor
with VMOT present. Adjust VREF per version/sense resistor and Watterott
datasheet, starting at low current. **1 A per phase is a provisional target**,
not a universal potentiometer setting or battery current. Heatsink and airflow
are needed; test temperature.

## Sensors, GNSS, and limit switches

All JSTs are vertical XH **2.50 mm**, not 2.54 mm; use compatible crimps and
mechanical strain relief. Square pad and “1” identify pin 1 on each footprint.

| Connector | Pins 1,2,3,4 |
|---|---|
| J6 external GNSS | 3V3, GND, GNSS_TX (to RX16), GNSS_RX (from TX17) |
| J7 AS5600 AZ | 3V3, GND, AZ_SDA, AZ_SCL |
| J8 AS5600 EL | 3V3, GND, EL_SDA, EL_SCL |
| J9 optional IMU/magnetometer | 3V3, GND, AZ_SDA, AZ_SCL |

AS5600 uses **0x36**; the two sensors must use separate buses. Breakout powered
at 3.3 V, no pull-ups to 5 V. R7–R10 4k7 on board; if breakout already has
pull-ups, calculate equivalent resistance or remove one set. Keep I2C short
(target <30 cm), separated from motor leads. Do not assume reliable long cables
without testing or transceivers.
Optional MPU6050 0x68/0x69 and LIS3MDL 0x1C/0x1E do not collide with AS5600;
use breakouts explicitly compatible with **VIN and 3.3 V logic**. J9 does not
imply firmware integration of these devices.

Suggested GNSS: Adafruit Ultimate GPS breakout 746; check revision, 3.3 V VIN
input, and 3.3 V UART before wiring; use external GNSS antenna separated from
ESP/radio. PCB provides UART/power only, not GNSS antenna, PPS, or RF interface.
A single-antenna GNSS does NOT measure static true heading. AS5600 measures
relative shaft angle; calibrate zero, direction, and physical axis. North/
elevation reference is calibrated manually; magnetometer near motors, steel,
AS5600 magnets, and wiring may be severely distorted. Do not promise automatic
absolute heading or confuse GNSS course-over-ground with antenna orientation.

| NC auxiliary, two pins: signal / GND | GPIO |
|---|---:|
| J3 stop, isolated auxiliary contact | 34 |
| J10 AZ minimum/home | 35 |
| J11 AZ maximum/travel | 36 |
| J12 EL minimum/home | 39 |
| J13 EL maximum/travel | 32 |

Broken wire/actuation=HIGH. These are monitor inputs, not a certified cutoff.
Limit switches do not cut VMOT by themselves. Never share 12 V power contact
with GPIO. Wire all NC circuits before arming; do not install permanent jumpers
to hide faults.

## Fabrication and assembly, step by step

1. Open with KiCad 10.0.7 or later compatible version. Compare
   `connectivity.json` with `firmware/include/board_config.h` and
   `docs/CONTROL.md`; any difference requires regeneration and validation,
   not just correction of a drawing.
2. Run `hardware/validate-export.ps1 -KiCadCli <local-path>\kicad-cli.exe`.
   This script **blocks new export** if ERC, DRC, parity, or connectivity fails;
   creates hashes, Gerber, Excellon, netlist, and placement files.
3. Order FR4, two layers, **finished 70 µm copper (2 oz) on both sides**,
   1.6 mm thickness, solder mask both sides, front/white silkscreen, no blind
   vias, no controlled impedance. Lead-free HASL or ENIG. Outline 180x130 mm;
   four NPTH 3.2 mm. See `fabrication/STACKUP.txt`. Do not automatically accept
   1 oz as substitute. Request electrical netlist test.
4. Inspect Gerber in independent viewer: two copper layers with thousands of
   segments/pads, masks, silk, closed outline, and separate PTH/NPTH. Verify
   mm units and same origin across layers/drill. Do not fabricate `Edge.Cuts`
   alone. KiCad position CSV uses Cartesian Y upward: `PosY=-y` relative to PCB
   coordinates here. Do not invert only one layer or drill file; send the full
   exported set.
5. Measure ESP 19x2/25.40 mm, TMC 8x2/15.24 mm, JST 2.50 mm, terminals 5.08 mm,
   fuse holders 22.50 mm plus center support. Blocking: check body, latch
   orientation, and screw access; original envelopes are conservative, not
   vendor STEP models.
6. Install resistors, D2 (marked K cathode toward positive), ceramic capacitors,
   D1 (band/cathode K toward PROTECTED12), sockets, terminals, and fuse holders.
   C1/C2: positive to VMOT, negative to GND. Do not insert modules.
7. Ohmmeter checks: no short RAW12-GND, VMOT-GND, or ESP5-GND; verify
   J2.2->U2/U3.VM continuity and no J2.1->J2.2 continuity with stop open.
   Verify auxiliary NC never receives 12 V. Inspect soldering and polarity.
8. Bench supply 12 V initially limited to 100 mA, stop latched; measure the
   isolated buck at 5 V before connecting J5; raise current limit only after
   tests. Insert ESP without USB and with appropriate JP1; measure 3V3.
9. Insert drivers without motors; confirm VIO and MS1/MS2=3V3 and EN HIGH.
   With stop latched, VMOT must fall even if Wi-Fi stays active. Test button,
   broken wire, reset, GNSS/encoder loss, and limit disconnection.
10. Connect motors while unpowered, lower VREF, make short moves without loaded
    antenna. Confirm direction, 25:1 scaling, travel, and feedback. Test current/
    temperature for at least 30 minutes before 1 A/phase target. Measure VMOT
    transients during cutoff/braking, including long cable.
11. Mount in external electronics enclosure with insulated M3 spacers. PCB
    origin at upper-left; holes (5,5), (175,5), (5,125), (175,125) mm. Reserve
    >=30 mm from PCB top to enclosure ceiling, not 30 mm above drivers, plus
    screw/USB access and ventilation. It is NOT claimed to fit in rotor cavity.
    Mechanical coordination must use these coordinates and real board size.

Previous 130x70 mm box cannot accept this 180x130 mm board: use a larger
independent box or specific mount, not silent footprint scaling. Initially
reserve >=20 mm around cable entries and >=30 mm from PCB top to ceiling;
verify actual cable bend/access and connector/heatsink heights.
Mechanical created `cad/carrier_enclosure.scad`: **final enlarged revision**
nominal exterior 228x178x43.6 mm plus 2 mm lid and 0.7 mm relief; interior
224x174 mm; PCB corner (24,24), enclosure support centers
(29,29), (199,29), (29,149), (199,149) mm. PCB at z=8 mm, 32 mm free above
nominal 1.6 mm board thickness; that gives nominally 12 mm above a 20 mm driver,
not 32 mm above it.
Final mechanical revision specifies 3.2 mm enclosure M3 clearance holes,
matching actual 3.2 mm PCB holes: verify print clearance; do not force screws or
use a populated PCB as drill template. **Coordinate** compatibility does not
prove physical fit: final lateral margin is 22 mm per edge and panels are
unperforated; define ports/strain relief and cable/screw access with PCB mounted
before closing enclosure. Enclosure is stationary, not on moving axis. Its CAD
solid ASA estimate ~260 g is not measured mass. Additional stationary
`cad/carrier-metal-mount.dxf` is an aluminum **240x196x2 mm** tray, budgeted
~254 g, unmeasured. Include that mass and fasteners in station balance in
addition to carrier/enclosure. These dimensions supersede former 188x138 box
and 200x156 tray; do not fabricate old revisions for this final assembly.
Reported BuildLight budget 3.130–3.200 kg before pending extras exceeds 3 kg:
**mass target is unmet in current budget**; do not hide the increase or claim
the assembly meets it.
AS5600 is on two external output axes: carrier does not impose a hole pattern
for an unselected encoder breakout.

Mass estimate, **not a measurement**: full FR4
`0.180 × 0.130 × 0.0016 × 1850 ≈ 69 g`; hypothetical complete copper at 70 µm
on both sides adds up to ~29 g before subtracting etched areas. Reserve ~100 g
for bare board and **150–220 g for board+modules**, excluding enclosure,
source/battery, external buck, stop, and cables. This does not demonstrate total
station mass; weigh assembly and check margin.

Keep RF 145/435 MHz, coax, motors, and buck separate from GNSS/ESP/sensors.
Metal RF enclosure requires antenna clearance and must not cover the ESP's
integrated antenna. This PCB is not a diplexer, RF filter, amplifier, or
transmitter interface.

## Assembly/use release blockers

- Verify actual modules and dimensions; do not substitute pinouts based on
  resemblance.
- Verify protected commercial supply, cable fuse, and main disconnect.
- Document the **exact** external-button reference, isolated NC contacts,
  current rating, and **DC breaking capacity >=5 A at 12 V**. A “10 A AC” mark
  is insufficient. BOM does not invent a certified part; until selected, motor
  operation is not authorized. Latching is mechanical, not a software relay.
- Test fuse selectivity, short circuit, TVS, regeneration, voltage drop, and
  temperature of D1/traces/terminals/driver under actual worst case.
- Test DevKit 3V3 with Wi-Fi and all peripherals; verify actual budget.
- Verify bench firmware with this pinout and microstepping, calibration/
  mechanical travel, stop, and re-arm. Simulation cannot replace these tests.

## Traceability and licences

Original schematic, PCB, rules/footprints, and technical hardware documentation:
**CERN-OHL-S-2.0**, copyright © 2026 Anatol EA5KAO, Diego EA5JEF, and Pedro Roca
Molina; see `LICENSES/CERN-OHL-S-2.0.txt` and `hardware/LICENSE.txt`.
Original generator, validation script, and tests are **MIT** software with the
same copyright notice; see `LICENSES/MIT.txt`.
No third-party PCB was imported. Manufacturer publications were consulted at
official URLs and are not redistributed in the project; their authors retain
their rights and are not represented as endorsing this prototype. Official
KiCad 10.0.7 was extracted locally from
`https://s3.cern.ch/kicad-downloads/windows/stable/kicad-10.0.7-x86_64.exe`;
not installed globally. KiCad software is GPL; official KiCad libraries are
CC-BY-SA 4.0 with design-use exception. The
`Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open` geometry was
consulted to confirm pitch/support; module figures are not incorporated into
Gerber.

Sources consulted (2026-10-10):

- Espressif DevKitC V4: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- Official schematic: https://dl.espressif.com/dl/schematics/esp32_devkitc_v4-sch.pdf
- TMC2209 v2: https://learn.watterott.com/silentstepstick/pinconfig/tmc2209/
- Watterott schematic: https://github.com/watterott/SilentStepStick/tree/master/hardware
- SPT fuse: https://www.schurter.com/en/datasheet/typ_SPT_5x20.pdf
- D24V22Fx buck: https://www.pololu.com/product/2858
- AS5600: https://ams-osram.com/products/sensor-solutions/position-sensors/ams-as5600-position-sensor

Prices in `bom/pcb.csv` are indicative unit estimates, not quotations; add
crimps, wire, heatsinks, DC stop, supply, enclosure, and shipping. There is no
lithium charger on the board and no functional-safety claim.
