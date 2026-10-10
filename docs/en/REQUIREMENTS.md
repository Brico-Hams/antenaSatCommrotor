# Requirements and traceability

| ID | Requirement | Implementation / evidence | Acceptance |
| --- | --- | --- | --- |
| R01 | 145/435 antenna | CAD and RF-AND-RADIO | VNA on both bands, assembled |
| R02 | Foldable and portable | MECHANICAL, removable parts | Measure packed size and complete mass |
| R03 | AZ/EL tracking | CONTROL, SGP4 | Orbital reference and two-axis bench |
| R04 | Operate without a phone | ESP32 calculation | Close browser during tracking |
| R05 | Web AP interface | web and firmware | Connect locally without Internet |
| R06 | Update TLE | STA/TLS/import | Visible errors and consistent cache |
| R07 | UTC location | GNSS and validity state | Reboot, no fix, clock loss |
| R08 | Orientation/level | Separate true-heading calibration | Measure angular error |
| R09 | RT3S OpenGD77 | Independent support and operation | Verify actual version and channels |
| R10 | Earlier diplexer | Modular RF integration | Confirm dimensions and S-parameters |
| R11 | Photographic tripod | Metal insert | Load and torsion test |
| R12 | Interchangeable antennas | Boom adapters | Verify mass/CG per antenna |
| R13 | NEMA14/25:1 ASA | CAD, calculations | Manual rotation, torque, heating |
| R14 | Movement safety | NC limits, faults | Physical stop independent of browser |
| R15 | Git and documentation | Independent repository | Persistent files and history |
| R16 | Low budget | Indicative BOM | Local quotes, no invented prices |
| R17 | Reference material | SOURCES, REFERENCE-ANALYSIS | Citations per PDF and license limits |
| R18 | Carrier PCB and Gerber | hardware, fabrication, PCB | ERC/DRC and nets; verify footprints/current |
| R19 | Connectable sensors | Common PCB/CONTROL map | Two AS5600 without address conflict and GNSS |
| R20 | Power protection | Fuse, polarity, overvoltage, and motor cutoff | Electrical tests before motors/RF |
| R21 | Guided web calibration | UI and shared control | Homing/north/level and explicit errors |
| R22 | Android BLE app | android, firmware BLE | Pairing/authentication, permissions, phone tests |
| R23 | TLE via phone | HTTPS download, atomic BLE transfer | Valid catalog, errors, no truncation of cache |
| R24 | Rotor-computed passes in app | ESP32 SGP4 and BLE query | No phone dependency during pass |
| R25 | Integrated 145/435 full-duplex FM, AM, and SSB/USB radio | Requested expansion; multimode RF architecture to verify | Measure reception during TX in both band combinations, spectrum, and desensitization |
| R26 | CAT and Doppler in the same APK | New integration pending; do not attribute CAT to RT3S | Actual TX/RX frequencies, readback, errors/interlocks |
| R27 | SSTV PD120/PD180 on Android | Local audio decoder development | Known PCM vectors and image, then over-radio test |
| R28 | AX.25 AFSK1200 and APRS | Callsign messaging/decoding development | Actual CRC, NRZI, bit stuffing, recipient, ID, and ACK |
| R29 | Bidirectional Bluetooth PCM audio | Transparent link separate from existing rotor BLE | Verify sample continuity, visible losses, latency, coexistence |
| R30 | Internal speaker and mic, Baofeng-style accessory | Audio interface and board pending | Exact accessory pinout, bias, PTT, isolation, no feedback |
| R31 | Send APRS messages over radio | Modulation/transport require independent validation | Do not claim sent by generating audio or delivered without remote ACK |
| R32 | Evaluate Raspberry Pi Zero or similar for radio and rotor without ESP32 | Feasibility requested; no SBC approved by selection/test | Measure USB/CPU/RAM/Bluetooth, deterministic movement, independent stop |
| R33 | Update PCB/Gerbers and system documentation | New revision conditioned on module/SBC selection | ERC/DRC, footprints/pinout, current, audio, RF, mechanics; do not reuse ESP32 carrier approval |
| R34 | Limited axial-rotation third POL axis | Three-motor mechanical/control design in development | Verify travel, homing, NC limits, encoder, cables, mass/CG, torque |
| R35 | RHCP/LHCP RF switching | Independent of POL rotation; requires compatible circular antenna | Measure phase/amplitude, axial ratio, isolation, and TX-inhibited switching on both bands |
| R36 | Complete mass <=5 kg | Replaces earlier 3 kg limit with exclusions | Weigh the operational set: antenna, three axes, radio/SBC, enclosure, sensors, cables, and tripod together; EXCLUDE only the external battery (R47) |
| R37 | GNSS, compass, and tilt in new variant | GNSS/UTC, magnetometer and IMU, plus AZ/EL/POL encoders | Calibration, declination/true north, interference, visible validity, safe fault response |
| R38 | 50-ohm SMA RF connectors | Antenna, radio, diplexer, and RHCP/LHCP networks; exclude RP-SMA and BNC/N adapter chains in new variant | Verify gender/contact, footprint, power, coax, strain relief, and ground; audio/power do not use SMA |
| R39 | CM5 + LimeSDR Mini, no ESP32 | Subsequently selected architecture; one replaceable full-duplex RF module | Test carrier, USB, resources, power/battery, cooling, independent stop |
| R40 | Android features inspired by Look4Sat/Robot36 | First selected version: catalog/passes, map/radar, alerts, frequencies/Doppler, three axes, PD120/180, APRS | Per-feature test matrix; do not claim full equivalence or copy UI/code without license |
| R41 | Two LimeSDR Minis for simultaneous VHF/UHF RX | Replaces interim choice of one SDR; each chain is TX-capable | Identify by serial, verify two real streams, audio selection, filtering, desensitization; initially one TX active |
| R42 | Spanish, English, and Hungarian documentation | Complete synchronized editions; glossary, diagrams/legends, assembly, warnings, and rationale | Per-document coverage, links, source revision/hash review; do not alter original licenses |
| R43 | Reference prices for all components/materials | BOM with quantities, model, date, EUR sources, comparable mean, VAT/shipping, and separately listed tools | Verify subtotals and coverage; pending price/allowance is neither a purchase nor zero cost |
| R44 | Illustrations in assembly instructions | Figures linked to steps and component map with BOM IDs | Match part/material/step, drawing revision, and conceptual-drawing limitations |
| R45 | JLCPCB Gerber + BOM + CPL package | Actual Gerbers/drill files, BOM with exact LCSC numbers, CPL in mm/side/rotation, separate manual/DNP list | ERC/DRC/connectivity, designator/source/orientation/supplier-code correspondence; no order or physical release by default |
| R46 | USB-C for power and data | Confirmed preference; retain SMA RF and K1 audio | Verify port role/speed and power, PD/cable/current limits; never apply incompatible voltage to CM5 |
| R47 | External battery excluded from 5 kg limit | Replaces initial battery inclusion; retain two-hour target with external capacity to be sized | Record external mass and cost separately; verify usable energy/current/regulation; 12 Wh does not prove two hours |
| R48 | BricoHams custom operating system | Official Raspberry Pi OS ARM64, branding/banner, project components/services, secure local provisioning | Reproducible source/version; distinguish built image from recipe; verify CM5 boot/dependencies/permissions; no shared credentials or auto-arming |
| R49 | Powerpole and distribution fuses | External 12 V Powerpole input, main fuse near battery, and CM5/motor/RF branches | Verify polarity, crimp/wire gauge, DC/interrupt ratings, time-current/inrush, temperature and coordination; BMS does not replace fuse |
| R50 | Evaluate power EMI filters | Common-mode/damped differential filtering, decoupling and branch segregation | Measure current, saturation, DCR/drop, regulator stability, inrush/transients and received noise; do not confuse DC filtering with RX/TX isolation |
| R51 | Independent modules and general guide | Antenna, rotor, and SDR radio each have dedicated materials/assembly/configuration guides; integration is separately illustrated | Support rotor without SDR, manual radio without rotor, and antenna without software; shared BOM without duplicating CM5/power |

The R25-R31 expansion replaces the interim FM-only choice for the new radio,
but preserves the independent RT3S/rotor operation from the first delivery.
It does not turn FM modules into SSB or declare an RF chain implemented merely
because controls exist in the app. Reopen mass, consumption, cooling, and cost
before releasing a new PCB/enclosure.

The later request for one SBC reopens the decision to keep an ESP32: it is an
evaluation, not a verified replacement.

## Non-goals of the first iteration

- Military SATCOM coverage or compatibility with the commercial antenna in the photo.
- Full-duplex using an RT3S; SSB on an FM/DMR radio.
- Moving any SpaceQuad antenna without verifying load or installing without calibration.
- Guaranteed sub-degree accuracy with printed parts absent testing.
- Unlimited power, certified IP waterproofing, or resistance to any wind.
- Automating CAT/PTT with an unverified protocol.

## Pending data from the actual equipment

Exact motor and torque curve, RT3S dimensions with battery/case, connector and
coax measurements, tripod reference and rated load, diplexer VNA results,
selected power supply, printer tolerances, actual mass/CG, and local magnetic
field if a magnetometer is added.
