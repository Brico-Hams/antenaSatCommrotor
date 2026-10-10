# Reference analysis and decisions for the new design

Date: 2026-10-10. IDs and revisions are in [SOURCES.md](SOURCES.md). All six
locally extracted texts were read in full. “Printed p.” means a verifiable
printed page number in the manual; “PDF p.” is the page position in articles
without verifiable pagination, not an invented editorial page number.

## 1. P1 — Gordon Gibby KX4Z, Introduction to the station

**Actual content.** P1, PDF p. 1, lists directional VHF/UHF antennas,
filter separation, orbital-model pointing, full-duplex radio, Doppler, and
sensitivity. Its example is an economical build, not an integrated backpack
station. P1, PDF p. 2, proposes an Arduino K3NG controller and motors/
actuators with potentiometers. P1, PDF pp. 3-4, distinguishes:

- Gpredict: prediction and display.
- rigctld/Hamlib: radio interface; the author had difficulty controlling
  MAIN/SUB and both Dopplers on the IC-820H.
- rotctld: desired-position protocol, **not** direct motor control or physical
  angle feedback.
- SatPC32: Windows alternative that worked with the author's IC-820H.

**Application.** Preserve separation between prediction, planning, motor,
and radio. PortableSatStation's normal mode should calculate SGP4 in the
controller, provide a local AP, and store TLE/location/UTC without a PC.
An optional external protocol does not replace onboard SGP4.

**Not transferable.** Full duplex is a requirement of the author's station.
An RT-3S with different TX/RX frequencies does not thereby receive while
transmitting. Neither IC-820H operation nor CAT commands for other radios
establish an RT-3S interface.

## 2. P2 — Inexpensive control board

**Actual content.** P2, PDF p. 1, expands K3NG to Nano, buttons, and
movement/direction outputs, warning about memory limits. P2, PDF pp. 2-3,
shows schematic, double-sided board, and prototype; LCD/buttons are on the
opposite side from Nano/connectors. P2, PDF pp. 4-5, lists LM7805, 1 A
diodes, transistors, P-channel MOSFETs, and connections. P2, PDF pp. 6-7,
explains:

- MOSFET for motor power/PWM; external two-SPDT-relay boards for
  **polarity reversal of DC motors**.
- One relay board per axis; 0/5 V logic and 12 V relay supply.
- G-450ADC rotation in about 90 s and an estimated 2 A supply; the linear
  regulator may need a heatsink at higher input voltage.

**Application.** Power/logic separation, manual control, interference
suppression, and progressive testing are reusable principles. Do not transfer
the DC circuit to a stepper: NEMA14 needs a two-phase current driver,
STEP/DIR/ENABLE signals, electrical limits, and acceleration.

**Not transferable.** The Yaesu's 2 A or 90 s does not size the battery,
current, or speed for NEMA14. A 25:1 ratio does not establish output torque;
dynamic torque, efficiency, backlash, and the actual reducer's limit are
missing. The documented board alone does not provide AP, SGP4, GNSS, or
true north.

## 3. PC — Controller-board construction manual

**Actual content and printed pages.**

| Page | Evidence | New design decision |
|---|---|---|
| Printed pp. 1-2 | Soldering safety, eye protection, diode/electrolytic polarity, semiconductor orientation | Retain good practice; do not treat every chemical explanation as a technical specification |
| Printed p. 3 | Initial build for azimuth only | Commission subsystems/axes before tracking |
| Printed pp. 4-5 | 2N3904/resistors generate logic direction; MOSFET switches motor power | New-system direction/STEP-DIR driver are not equivalent outputs |
| Printed p. 6 | Flyback diode, filtering capacitor, optional anti-reset capacitor | Design protection for the actual drivers/inductors; do not indiscriminately copy Nano circuit |
| Printed p. 7 | Polarity protection, 5 V regulator, RF filters, manual buttons | Select DC/DC supply and protection for modern electronics/actual battery |
| Printed p. 8 | 5 V potentiometer, limiting resistor, Nano ADC | A 3.3 V MCU ADC does **not** automatically accept this 5 V interface |
| Printed p. 9 | Check 5 V before soldering Nano; 16x2 LCD and mechanical separation | Verify voltages before connecting electronics; leave cable/service clearance |
| Printed p. 10 | Check shorts, power USB, program | Test without motors, then drivers, then each unloaded axis |

**Consistency warning.** Some resistor designators/values in the manual and
P2 table do not align cleanly (for example R2/R3). Do not generate a new PCB
or assembly BOM by automatically merging both texts; a verified, versioned
schematic must govern. This project does not build that board.

## 4. P3 — Two-axis rotor

**Actual content.** P3, PDF p. 1, reviews manual, fixed-elevation, and
commercial options; it does not claim a permanently weatherproof installation.
P3, PDF p. 2, uses a **Yaesu G450ADC** for azimuth on wood and a 12 V linear
actuator with **2-inch** stroke for elevation. An attempt using a highly
reduced motor and 90-degree box failed when gears were damaged. A pin about
1 inch from the axis is an initial geometric approximation, not a general
kinematic solution.

P3, PDF p. 3, uses the actuator's internal end limits and an elevation
potentiometer. P3, PDF p. 4, describes **10 mm** shafts, PVC/rubber/clamp
adaptation, elevation of about 15-75 degrees and no use above 90 degrees.
The lower rotor turns the **entire** upper assembly. P3, PDF p. 5, only
provides a caption for the assembled antennas.

**Application.** Balance antenna/cables, support loads with bearings, verify
shaft-to-boom attachment, and treat azimuth as carrying the complete head.
The new original ASA rotor with NEMA14 and 25:1 planetary reduction is not
derived from the wooden parts or piston kinematics.

**Not transferable.** G450ADC robustness does not prove a NEMA14 reducer
withstands radial/axial loads. Structurally support the output shaft with
bearings. Do not assume the planetary reducer is self-locking; test retention
and behavior without power. An actuator's end switch is not a stepper's
reference or hard stop. Zenith passes require a planner respecting limits/
speed, not arbitrary AZ jumps or an unverified mechanical flip.

## 5. P4 — Cross-polarized Yagis, July 2025

**Actual content.** P4, PDF pp. 1-2, discusses polarization fading and
proposes two planes. P4, PDF pp. 2-3, describes two ways to produce 90
degrees: a phasing line or physical longitudinal offset of lambda/4, with
orthogonal planes/feed orientation. It gives **20.36 inches** on 2 m and
**6.78 inches** on 70 cm, equivalent to 517.144 and 172.212 mm. These are
plane offsets from that reference design, not dimensions for a single
dual-band antenna.

P4, PDF p. 4, uses a nonconductive boom and Cheap Yagi designs: an initial
4-element VHF + 6-element UHF plane, then a second plane with 3 VHF +
5 UHF elements. Element diameters change lengths. P4, PDF pp. 5-7, details
arrow/aluminum, insert, and copper joints with varying results; these are
not repeatable industrial processes. P4, PDF pp. 8-10, tunes with a VNA,
compares front/back, and uses a removable/indexed PVC boom.

P4, PDF p. 9, connects RG58 feeders of electrically corrected lambda/2
through a BNC T; the author reports overall VSWR **2:1-3:1**, not ideal
matching. P4, PDF p. 11, has a caption reporting VSWR 1.2:1 at **444.8 MHz**;
this does not establish VSWR at 435 MHz or a complete useful band. P4,
PDF p. 12, reports approximately **40 dB or better** antenna isolation in
that assembly and reception with a preamplifier, one diplexer side as filter,
IC-820H at about 30 W, and 50 feet of LMR400. P4, PDF p. 13, lists materials
and series links.

**Essential corrections and limits**

- A T with two antennas does not by itself create quadrature or matching.
  Known impedances/phases are needed; the observed case is not a rule for
  other dipoles.
- **Do not** adopt as universal the article's observation that changing
  RHCP/LHCP costs only 3 dB: opposite ideal circular handedness has much
  greater rejection. 3 dB applies to ideal circular vs. ideal linear
  polarization. Actual performance depends on axial ratio, orientation, and path.
- The UHF table across PDF pp. 4-5 contains a contradictory value: initial
  Director 1 is 12.3 inches, while text says “shorten” to 13.1. Record the
  inconsistency; **do not use it as a cutting drawing**. Check source/original
  and measure.
- Polar plot at 30 feet and isolation of that structure do not establish
  absolute gain, axial ratio, or isolation for the new portable antenna.
  Do not automatically add those dB to ideal diplexer values.
- Two VHF planes spaced about lambda/4 increase length, CG, moment, and
  wind area. Do not inherit another antenna's mass or torque budget.

**Application.** First choose verifiable RF architecture: one directional
antenna per band, initially linear if easier to validate, or orthogonal
planes with a **band-specific** phase network. Tune with final ASA/cables/
supports. Circular polarization is pending measurement, not a cosmetic label.

## 6. PT — SatelliteTargets list

**Actual content.** PT, PDF p. 1, mixes FM repeaters (ISS, SO-50, HADES-R)
and VHF-downlink linear transponders; it lists frequencies, centers, and
arming tones/CTCSS. PT, PDF p. 2, includes RS-44 and MESAT1 with linear UHF
downlinks, ISS packet at 145.825, and SONATE-2. It has no validity date or TLE.

**Application.** It shows that “145/435” are bands, not one unique channel
pair, and that each satellite needs mode, TX/RX, tone, and ephemeris. The
table **must not be imported as an authorized operating list**. Verify with
AMSAT/operator before transmitting and select a mode compatible with the radio.

**Not transferable.** RT-3S FM/DMR does not become SSB/CW by loading RS-44,
AO-7, or another linear transponder. Packet requires an appropriate data path/
modem; mechanical tracking does not itself provide AX.25. The AO-7 FCC
exemption mentioned applies to another jurisdiction, not automatic local
permission. ISS can change modes: do not guarantee that two historical
entries work simultaneously.

## 7. L — LibreSat as a system reference, not measured prototype

The public revision uses Pi Zero 2 W + RP2040 and NEMA17 with **printed
25:1 cycloidal** reduction, not NEMA14 with the new original planetary
design. README: actuator diameter 94 mm, approximately 45 mm plus motor,
two 61810 bearings, and an AS5600 encoder on the motor's rear shaft.
MECHANICAL: 5 mm front motor shaft, 6803 bearings **17x26x5 mm**, 61810
**50x65x7 mm**, stub dia. 20 x 250 mm inserted 42 mm, and antenna about
200 mm from actuator face.

It also specifies ASA for outdoor parts, tripod adapters, a 60 cm cable loop
centered at AZ 225 degrees for 0-450-degree range, and 300-500 mm mast
extension for some booms >1.1 m. These are **LibreSat dimensions**, not
guaranteed-compatible PortableSatStation parts.

SIZING assumes antenna 1 kg, area 0.1 m2, pressure arm 0.15 m, imbalance
20 mm, wind 10 m/s, and 75% efficiency. It calculates EL 1.30 Nm, AZ
1.10 Nm, average 4.1 W, and simulated step/flip results. Do not reuse those
safety factors, autonomy, or pointing errors as new-design results. README
itself acknowledges the complete assembly is not yet built/measured.

**Lessons:** retain local AP, offline TLE, clock/location, cable-wrap planner,
balanced mounting, and recalibration. A motor-mounted encoder detects missed
steps but **does not measure backlash or slip after the reducer**. Saved step
counts do not recover orientation after unpowered motion. A GNSS antenna gives
position/UTC, not absolute heading of a stationary station. Level/gravity give
tilt, not azimuth. True north requires an explicit method with calibration,
declination if using a magnetometer, and interference detection.

## 8. B/T/C — Shape references

Blog B states **449.550 MHz** and calculates active length `0.92*c/(2f)`,
reflector 1.05 times active length, and spacing 0.225 lambda. Evaluated only
as an initial estimate:

| Frequency | Total active | Total reflector | Spacing |
|---|---:|---:|---:|
| 145 MHz | 951.066 mm | 998.619 mm | 465.195 mm |
| 435 MHz | 317.022 mm | 332.873 mm | 155.065 mm |

These are complete lengths, not individual arms, and do not form a validated
dual-band design. Scale difference requires a dedicated architecture;
dielectric support, tube diameter, inter-band proximity, and feed network
shift impedance/pattern. “SATCOM” or AV-2040 resemblance does not guarantee
145/435 coverage.

T only provides a verifiable title; no dimensions or license. C states
commercial/private-use/NoAI terms; its model is not copied or traced into a
derivative. General functional inspiration (folding, tripod, portability)
does not authorize reproduction of third-party geometry.

## 9. Decisions and integration blockers

1. **New original design**, ASA structure; NEMA14 25:1 planetary only after
   exact model/real data selection. Test creep, temperature, bearings, load,
   and fasteners. `calc/design.json` uses a 200-step motor, 16 microsteps,
   and 25:1: **80,000 output microsteps/revolution** is nominal command
   resolution, not measured accuracy. 0.1 Nm motor torque and 0.7 per-stage
   efficiency are assumptions; the 8 m/s wind example **does not meet**
   required safety margin and does not authorize that speed or establish a
   safe wind limit.
2. **Onboard AP and SGP4 tracking** independent of RT-3S. Without valid UTC/
   position/TLE or calibrated north/level, do not claim valid tracking.
3. **Manually assisted radio**, with OpenGD77 Doppler only if build is checked;
   no invented CAT, PTT control, or assumed full duplex.
4. **Optional, unmeasured diplexer**, geometry published in
   [RF-AND-RADIO.md](RF-AND-RADIO.md). Allow clearance for plugs, radio, and
   coax flex; do not use connector as structural support.
5. **Polarization separated by band.** Do not order hybrids until band, phase,
   power, and isolated port are known; QCN-3+ excluded for 145 MHz.
6. **Physical-fit blocker:** diplexer connector flange/front heights are
   explicitly the author's estimates. Keep final interface CAD parametric
   until the actual unit is measured with calipers.
7. **Approval blocker:** no complete physical test of new rotor, antenna, or
   RF network. Simulations, sources, and CAD do not justify “ready to transmit.”
8. **User-selected licenses:** MIT original software and CERN-OHL-S-2.0
   original hardware. External references keep their own licenses; unknown
   sources are not redistributed, and LibreSat GPL is not changed. Engineering
   synthesis does not include its files. No remote publication in this phase.

### Autonomous tracking conditions, not APIs inferred from appearance

- **SGP4 propagation actually runs on ESP32**, using TLE, UTC, and location;
  a phone is an interface, not a hidden prediction computer. Do not call an
  API implemented without the complete input-validation -> calculation ->
  planning -> safe-control path.
- Missing, invalid, or expired UTC blocks automatic motion. GNSS location
  saved across shutdown is a **cache with metadata**, not a fresh valid
  position or a current fix after boot. Confirm/acquire location/UTC and
  validate TLE age.
- Geographic/true AZ and mechanical AZ are not interchangeable: transform
  by north offset and choose equivalent +/-360-degree solution **within
  mechanical and cable limits**, without normalizing a forbidden angle into
  a permitted one. Test crossings 359->0, nonzero offset, and travel edges.
- At zenith, geographic azimuth is singular; do not generate unlimited motion
  to follow it. Reject passes reaching/exceeding zenith limit without proven
  continuous trajectory, speed, and mechanical margin. Do not claim zenith
  tracking through a flip the geometry/planner cannot perform.
- Manual TLE import is mandatory offline. Automatic download, if offered,
  needs end-to-end HTTPS **certificate verification** and response/TLE
  validation; omit it if it cannot be implemented end to end. Never replace
  TLS validation with `setInsecure`.
- Tests must explicitly cover boot without UTC, invalid UTC, GNSS cache after
  reboot, AZ offset/cable wrap, zenith target, validity loss during tracking,
  and import failure. AP/endpoints do not replace these tests or a real
  firmware build.
- **Latency is safety:** with motors enabled, reject HTTPS downloads or long
  blocking predictions; alternatively use incremental calculation with
  continuous service and demonstrated stop latency. A 10-second HTTP timeout
  in the same loop can starve stop, homing, and limits. Physical stop needs
  independent supervision and/or suitable hardware cutoff, not completion of
  a web handler.
- Limit prediction to selected satellite and bounded horizon. Status queries
  must not repeatedly recalculate a full catalog or trigger downloads. Bound
  catalog/TLE size and per-request work before moving motors.
- A target beyond reachable speed, travel, or zenith constraints produces an
  **explicit API failure** and no motion; silently clipping angle and
  returning “success” does not achieve the request. Stop logic cannot wait
  for a long-running handler during tracking.
- TLE names and imported text are untrusted input: show with `textContent` or
  equivalent escaping, never `innerHTML`. Orbital validation does not
  authorize markup injection into the AP.

## 10. A — AV2040 datasheet added: visually verified comparison

The new local one-page `TDS_AV2040.txt` extraction was read in full. Because
figures were lost through font mapping, the locally rendered page at 140 dpi,
`TDS_AV2040-000001.png`, was read visually. Source: **Ultralife/Trivec-Avant,
23 Nov 2010, UBI-05273 REV:-**, PDF p. 1. Numbers were not guessed from the
encoding.

**Published AV2040 commercial data:** 240-400 MHz, VSWR 1.5:1, right-hand
circular, 3 dB axial ratio, 200 W CW, 6.5 lb (about 2.948 kg), male BNC.
Variant gains: AV2040-3 +7.0 dBic 240-400 MHz; AV2040-2 +11.0 dBic
240-318 MHz; AV2040-1 +9.0 dBic 240-400 MHz. These are manufacturer
datasheet claims, **not performance of the new 145/435 MHz design or physical
verification of our station**.

**Both target frequencies, 145 and 435 MHz, are outside 240-400 MHz.**
449.550 MHz from the blog is also outside: the blog describes its own
retuned build, not evidence the factory product extends its band. Datasheet
shows/describes folding/manpack, but **publishes no deployed/folded dimensions
or bag volume**, nor defines what is included in mass. Do not obtain dimensions
or CG from the photo.

Design application: portability/folding are reasonable functional
requirements, but antenna, polarization, and 145/435 support need their own
design and measurement. Do not inherit 200 W, 3 dB axial ratio, 7/9/11 dBic,
or 2.9 kg as specifications for the ASA original. No external files are
included absent a verified license.
