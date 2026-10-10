# Architecture and Decision Log

## System boundaries

The original target is an amateur FM station for 145/435 MHz, not a commercial
SATCOM terminal or access to military satellites. Commercial reference names
do not imply their performance.

```text
                         local browser
                              |
                        Wi-Fi AP / HTTP
                              |
Internet -- STA/TLS --> ESP32 -- SGP4 -- AZ/EL targets
Manual TLE ----------> cache      ^            |
GNSS UTC/position ----------------+       safe control
true north + level --------------------------+
NC stop / limits / encoders --------------- motors

RT3S -- shared coax -- metal RF diplexer -- VHF port -- VHF network -- VHF antenna
                                         -- UHF port -- UHF network -- UHF antenna
```

A circular-polarization network is a separate function: quadrature hybrid,
two orthogonal dipoles, balanced feed, and handedness control. It does not
replace the diplexer. A single half-duplex transceiver does not become
full-duplex merely by combining two antennas.

## ADR-001: separate repository

**Decision:** a new local Git repository in Documents, `main` branch.
**Reason:** the open directory belongs to Intune; it is unrelated and must not
be contaminated. **Rejected alternative:** reuse the IDE-selected script.
**Consequence:** remote publication requires a later action. The user selected
MIT for software and CERN-OHL-S-2.0 for original hardware.

## ADR-002: electrically distinct bands

**Decision:** two independent radiators and matching networks.
**Reason:** wavelength ratio is 3:1. Scaling a 449.55 MHz UHF design once does
not provide known SWR and pattern in both bands.
**Alternative:** an EM-model-optimized dual-band Yagi.
**Consequence:** more connections; measure each port individually first,
then the complete assembly for mutual coupling.

## ADR-003: crossed dipole with reflector as a starting point

**Decision:** original parametric geometry, mechanical folding, and removable
conductive parts. Empirical dimensions are initial values.
**Reason:** lower cost and volume than a long high-gain Yagi.
**Alternative:** reuse the commercial antenna from the screenshot.
**Consequence:** do not copy its STL files or claim its gain; circular
polarization and pattern require simulation and testing. If they do not meet
requirements, use a lightweight external Yagi with the rotor's same interface.

## ADR-004: decoupled interfaces

**Decision:** removable antenna saddle; rotor accepts booms with adapters and
metal fastening; radio on a fixed base; independent diplexer.
**Reason:** use the antenna by hand, switch to Yagi/SpaceQuad, or remove the
radio. **Consequence:** mechanical universality does not imply load or RF
compatibility. Every external antenna must meet mass, CG, wind, and travel limits.

## ADR-005: NEMA 14 instead of NEMA 17/23

**User decision:** prioritize portability with NEMA 14.
**Reason:** reduce mass, consumption, and volume.
**Consequence:** the NEMA series defines the flange, not torque. Select the
motor/driver using the torque curve at actual speed. Load is limited by
validation; movement of an arbitrary SpaceQuad is not promised.

## ADR-006: two 5:1 planetary stages

**Decision:** fixed ring, input sun, and output carrier at each stage; 25:1
total. **Reason:** compact shaft and distributed reduction.
**Criterion:** R=S+2P; (S+R)/number_of_planets is an integer. Base calculation
uses S=18, P=27, R=72, module 1.5, avoiding undercut of a 12-tooth sun without
correction. **Consequence:** ring pitch diameter 108 mm; the envelope is larger.
It does not honestly fit in a 60 mm case.

## ADR-007: actual accuracy is distinct from resolution

**Decision:** feedback/homing and calibration; nominal microstep 0.0045 degrees.
**Reason:** microstepping does not eliminate elasticity, backlash, magnet
errors, lost steps, or initial-orientation error.
**Consequence:** initial final-accuracy criterion is <=2 degrees RMS in a slow,
windless test; this is not an ultra-precision claim.

## ADR-008: ASA does not replace metal

**Decision:** ASA for chassis/gears; metal shafts, screws, bushings, tripod
insert, and RF components.
**Reason:** favorable UV performance and mass, with anisotropic strength/creep.
**Consequence:** tune tolerances with coupons; do not thread primary loads into
plastic or consider ASA an RF shield.

## ADR-009: spur gears for the first iteration

**Decision:** prioritize verifiable gears before double-helical gears.
**Reason:** accessible printing and adjustment; herringbone does not guarantee
zero backlash and adds axial assembly constraints.
**Consequence:** double-helical remains a later variant if measured results
improve. Specific parameters are in the mechanical manual.

## ADR-010: orbital calculations on the ESP32

**User decision:** local SGP4, stored TLEs, valid clock and location.
**Reason:** the browser can disconnect after tracking begins.
**Rejected alternative:** phone/PC sending every point during a pass.
**Consequence:** real orbital library, RAM budget, catalog limits, calculation
frequency; do not replace SGP4 with a circular orbit.

## ADR-011: AP is not Internet

**Decision:** local AP always available; optional STA Internet access; manual
TLE import for offline operation.
**Reason:** an ESP32 disconnected from the Internet cannot download from
CelesTrak through its own AP.
**Consequence:** persistent cache, visible errors, verified HTTPS, and per-TLE
age. HTML ampersands are normalized to `&` in URLs.

## ADR-012: position, time, and orientation are separate states

**Decision:** GNSS for UTC/position; explicitly calibrated true-north reference
and level; homing for mechanical reference.
**Reason:** stationary GPS does not give reliable heading. A magnetometer by
motors, steel, and coax can give incorrect heading; declination varies by place.
**Consequence:** calibrate against known north and use a bubble level as fallback,
not fictitious self-orientation. A tripod change requires recalibration.

## ADR-013: cable and zenith limits

**Decision:** no unlimited AZ rotation; mechanical and logical limits.
**Reason:** protect cables and prevent jamming.
**Consequence:** reject or stop a pass requiring excessive speed or exceeding
limits; do not take the long way around without planning. A configurable
exclusion zone near zenith remains until stable tracking is demonstrated.

## ADR-014: fail safe

**Decision:** disarmed on startup, physical NC stop, physical limits, homing
timeout, latched faults, and explicit rearming.
**Reason:** resets and loss of reference must not cause motion.
**Consequence:** corrupt data, invalid clock, stale TLE, or a lost sensor must
not produce success responses or approximate movement.

## ADR-015: RT3S remains independent

**Decision:** do not modify radio firmware, connect automatic PTT, or claim
generic USB CAT. **Reason:** a radio programming connector is not necessarily
a CAT API. **Consequence:** program OpenGD77 with compatible data; radio Doppler
and rotor tracking are separate calculations that must agree.

## ADR-016: removable RF compartment

**Decision:** integrate physically; do not redesign the prior diplexer without
testing. **Reason:** preserve the user's work and permit independent antenna/
radio use. **Consequence:** verify real dimensions, schematics, isolation, and
power rating of the prior project before cutting a mount or connecting TX.

## ADR-017: mass target is not certified

**Decision:** weigh the complete prototype, not just filament grams.
**Reason:** motors, bearings, shafts, battery, coax, and connectors dominate.
**Consequence:** the earlier <=3 kg target excluded radio and tripod and
included power when evaluating the station; record and redesign if exceeded.

## ADR-018: validation gates

**Decision:** G0 software/CAD, G1 mechanics without RF, G2 passive RF,
G3 receive, G4 authorized transmit.
**Reason:** an STL or unit test does not guarantee a working device.
**Consequence:** do not call the device field-ready before passing G1–G4;
document blockers instead of hiding them.

## ADR-019: mass priority over transmission type

**User-approved revision:** prioritize <=3 kg and permit replacing the planetary
transmission with a lighter transmission while retaining AZ/EL tracking.
**Evidence:** even with bounded lightening, solid-equivalent ASA is 2.521 kg;
hypothetical printed scenario plus components and battery is 3.208–4.038 kg.
The previous target is not met.
**Decision:** BASE with two GT2 20:100 belt stages, 25:1 total; retain the
planetary design as LEGACY. Coordinate the actual ratio with firmware.
**User-rejected alternative:** accept the current planetary mass.
**Consequence:** reassess stiffness, backlash, tension, limits, and behavior
without power. A belt is reversible and is not an EL brake. Do not claim <=3 kg
until weighed or replace a complete budget with the mass of a few STL files.

Initial digital BASE result: 0.862 kg solid-equivalent ASA. Total budget
3.121–4.006 kg; hypothetical lightened scenario 2.905–3.790 kg. The <=3 kg
target remains open and requires selecting components within budget and weighing
the assembly; success cannot be declared based on the lower endpoint of an estimate.

## ADR-020: repairable carrier PCB and verifiable Gerbers

**User-requested extension:** custom controller board with connectors for GNSS,
axis/orientation sensors, motors, power, and protection, plus manufacturing
Gerbers. **Explicit choice:** carrier board with replaceable modules, not
ESP32/drivers/GNSS implemented as discrete ICs.
**Reason:** field repair, lower risk, and lower cost for the first iteration.
**Decision:** editable schematic/PCB, GPIO map consistent with firmware, design
rules, Gerber/Excellon outputs, and BOM with concrete references.
**Consequence:** validate the EXACT module models and dimensions. A generic
DevKit or StepStick name does not prove electrical compatibility. Motor power
cutoff must be independent of software; logic may stay powered to report faults.
**Limit:** files are not released for fabrication merely because they exist;
ERC/DRC, footprint review, current, isolation, continuity, and bench testing are
independent gates. Optional orientation sensors are not implemented in firmware
just because a connector exists. Stationary GNSS still does not measure true north.

## ADR-021: printed Bricohams branding

**User's explicit choice:** raised `BRICOHAMS` and `bricohams.org` text integrated
into the controller-box lid.
**Decision:** geometry connected to the lid, with parametric depth/location
away from screws, ventilation, and connectors; regenerate STL and verify mesh.
**Reason:** durable identification without stickers or loose parts.
**Limit:** do not reproduce an unprovided official logo; text branding implies
neither certification nor third-party endorsement.

## ADR-022: guided calibration and Android BLE

**Explicit extension:** calibration in the web interface and a native Android
app for Bluetooth control. The user selected BLE.
**Decision:** shared control/authentication/state protocol; do not duplicate
commands that could bypass interlocks through another transport. Calibration
separates homing, position/UTC, level, and true north, with state validation
and explicit physical confirmation.
**Consequence:** evaluate memory and Wi-Fi/BLE coexistence on ESP32-WROOM-32E;
recompile and revalidate WebFlash after adding BLE. The app does not enable
motors on connect and does not replace the physical stop.

## ADR-023: phone as TLE bridge, rotor as calculator

**Explicit choice:** app downloads TLEs over HTTPS and transfers them over BLE;
ESP32 calculates autonomous SGP4 passes and tracking. The app queries and shows
results. No phone-calculated trajectory is sent.
**Reason:** update data in the field using the phone's Internet without assuming
the rotor AP provides Internet.
**Consequence:** bounded, atomic fragmented transfer; validate TLE at both ends;
show errors; prohibit cache updates during movement. A TLE list provides neither
satellite frequencies nor true tripod orientation. Losing phone connectivity
does not turn autonomous tracking into manual control or alone invalidate a pass;
the rotor safety policy and validity of UTC/position/sensors govern.

## ADR-024: modular multimode satellite radio extension

**Explicit choice:** integrated radio with replaceable RF modules, 145/435 MHz
full duplex, CAT/Doppler, and control from the same APK. A later request adds AM
and SSB/USB and replaces the intermediate FM-only selection.
**Decision:** verify a genuinely multimode architecture before selecting modules
or producing Gerbers. Keep radio removable and rotor/antenna independent. The
already validated rotor carrier is not automatically validated for RF/audio and
does not receive a new pinout.
**Reason:** (tr)uSDX and uSDX SOTA are HF modularity/CAT references, not 145/435 MHz
RF chains. ATU-100 is neither a transceiver nor a diplexer.
**Consequence:** new cost, mass, consumption, shielding, and RX/TX isolation
review; two configured frequencies do not prove full duplex.

## ADR-025: audio, SSTV, and APRS messages

**Explicit choices:** bidirectional Bluetooth audio, integrated speaker and
microphone, Baofeng-style external connectors, ISS SSTV PD120/PD180, and
AX.25 Bell 202 AFSK1200 with APRS messages between callsigns.
**Decision:** transparent audio link separate from the current BLE control link;
do not attribute audio to the rotor's 20-byte frame protocol. Verify accessory
and pinout before calling it Baofeng-compatible. Do not connect a BTL speaker
output directly to a jack ground.
**Reason:** voice compression, AGC, and noise suppression can alter tones needed
for decoding. Audio requires continuity and throughput/coexistence tests in
addition to control authentication.
**Consequence:** independently verifiable PCM decode/encode; generating a WAV
does not equal transmission. Remote APRS ACK differs from local transport ACK.
There is no cellular SMS gateway or guarantee of satellite delivery. PTT must
fail to receive on error, expiry, or disconnection.

## ADR-026: evaluate a single SBC and new carrier

**Later request:** Raspberry Pi Zero or similar for radio, audio, tracking, and
rotor, potentially dispensing with ESP32.
**Provisional decision:** evaluate resources and ports, and keep motion generation
independent from Linux's nondeterministic scheduling. Do not emit STEP pulses in
a Python/Linux loop and call them precise. Consider drivers with integrated
ramp generation and independent physical power cutoff/watchdog; confirm devices
and registers before schematic design.
**Consequence:** ESP32 removal is not approved by testing yet; new PCB/Gerbers
must have identity/revision separate from the original carrier. Linux boot,
Bluetooth failure, or a blocked process must not maintain PTT or dangerous
movement. Previous ESP32 WebFlash does not install a Raspberry Pi system;
document different provisioning if adopted.

## ADR-027: third POL axis and independent circular-handedness selection

**User's explicit choice:** limited axial rotation plus RF switching between
RHCP/LHCP for a compatible circular antenna.
**Decision:** new AZ/EL/POL variant with a third motor, limits, homing, and
calibrated position. Recalculate EL/AZ load for added rotating mass, CG, coax
twist, power, and structure; POL travel/reduction require their own specification,
not an automatic copy of 25:1.
**Reason:** POL can orient linear polarization; axial rotation does not reverse
circular handedness. Select RHCP/LHCP in the verified phase/feed network for
each band, with transmission inhibited.
**Consequence:** do not enable continuous rotation, RF joints, or a third driver
by default. The earlier two-motor carrier does not meet this requirement. The
old budget already exceeded 3 kg; the new axis does not restore that target
without another redesign and measurement.

## ADR-028: complete mass and sensors for the new variant

**Explicit choice:** 5 kg limit including tripod and every operational item;
replaces the earlier 3 kg limit with exclusions.
**Decision:** complete weighed inventory and proposed 500 g reserve (4.5 kg
internal target), not an invented budget for unknown parts. GNSS for site/UTC,
calibrated magnetometer for heading with declination, IMU for tilt, and
independent encoders for AZ/EL/POL.
**Reason:** stationary GPS does not give north and a compass does not give axis
position; motors/currents disturb the magnetometer.
**Consequence:** include mass, power, connectors, mounting, and sensor tests in
the new PCB/docs; three AS5600s require addressing the shared I2C address.
Do not claim PPS, compass, or encoders work just because they are drawn. Invalid
signals must be visible and block dependent functions; manual calibration is
only an explicit, verified procedure, not a silent substitute.

## ADR-029: SMA RF interfaces

**Explicit choice:** conventional 50-ohm SMA to reduce radio, antenna, diplexer,
and polarization-network mass and volume.
**Decision:** no RP-SMA, BNC/N adapters, or coax attached to PCB without strain
relief; verify each part's center contact and gender.
**Consequence:** footprints/dimensions/ratings depend on the actual connector;
measure rather than assume mass savings. Do not use SMA for power, sensors, or
mic/speaker accessories. Earlier BNC variants are historical references, not
the RF interface for this extension.

## ADR-030: CM5 and one replaceable full-duplex SDR

**Explicit choice:** Raspberry Pi Compute Module 5 and LimeSDR Mini. The user
confirmed retaining transmit/full duplex after clarification that RTL-SDR Blog
V4 is receive-only.
**Decision:** CM5 for calculation/control/audio and one SDR with independent
RX/TX; supersedes intermediate Pi Zero/Pi 4 and two-module proposals.
**Consequence:** no validated CM5 carrier or multiwatt RF output exists yet.
Select revisions/cooling, high-speed USB, power, linear PAs, and filters through
testing. Keep the earlier ESP32 rotor only as a separate historical variant.

## ADR-031: Android scope inspired by other applications

**Explicit choice:** first version with catalog/passes, map/radar, alerts,
frequencies/Doppler, AZ/EL/POL control, ISS SSTV PD120/PD180, and APRS messaging.
Not full Look4Sat/Robot36 equivalence.
**Decision:** feature/status/test matrix, original implementation, and license
review before reusing libraries or assets.
**Consequence:** a map without real orbital data does not prove tracking; a
synthetic image tests DSP, not RF reception. Android alerts depend on permissions,
clock, and OS restrictions.

## ADR-032: two SDRs for simultaneous reception on two bands

**Later explicit choice:** two LimeSDR Minis, not Lime plus RTL-SDR; supersedes
the intermediate one-SDR selection in ADR-030.
**Decision:** identify one chain by serial number for VHF and one for UHF, with
two concurrent receivers and TX capability per chain. Conservative initial
policy: only one TX active; do not assume authorization for simultaneous
transmission on two bands. Explicitly select VHF/UHF audio for the decoder; do
not mix two tone channels.
**Consequence:** recalculate USB, power, heat, mass, filters, and protection for
both receivers. Two connectors/software instances do not establish simultaneous
reception in the presence of TX.

## ADR-033: official CM5IO plus original auxiliary board for PCBA

**Explicit choice:** purchased official CM5IO plus original auxiliary board
with Gerbers/BOM/CPL for JLCPCB. A single custom high-speed CM5 carrier is
rejected for this revision.
**Decision:** CM5IO handles CM5 mounting and two native USB 3 ports; original
auxiliary board handles three drivers, sensors, and interlocks with verified
interfaces. Do not distribute official files under the project's license.
**Consequence:** include CM5IO, cooling, cabling, and auxiliary board in mass
and price. A third USB audio device requires a specified host/hub; two occupied
USB ports do not create a fictitious third. Configure CM5IO VIO to 3.3 V if the
auxiliary board uses that logic; 1.8 V is not interchangeable without interface
review.

## ADR-034: USB-C and external battery

**Explicit choices:** prefer USB-C for power and data while retaining SMA RF
and K1 audio; exclude the external battery from the 5 kg limit. Retain the
two-hour runtime objective and permit an external battery larger than 12 V /
1 Ah. **Decision:** record battery transported mass separately, include its
cost, and size current, energy, and regulation from measured consumption.
12 Wh nominal supports only 6 W average for two hours before losses; it must
not be called sufficient. The battery is the only mass exclusion; tripod,
radio, and cables remain included. Verify voltage by port and USB-C/PD role;
never connect 12 V directly to a CM5 5 V rail.

## ADR-035: module-based assembly and software

**Explicit request:** independent antenna, rotor, and radio documentation and
assembly guides, plus an illustrated general manual. **Decision:** provide
four entry points—MODULE-ANTENNA, MODULE-ROTOR, MODULE-RADIO, and
MODULE-INTEGRATED—with rotor-only, radio-only, and integrated profiles that
do not assume nonexistent hardware dependencies. **Consequence:** standalone
manual radio operation does not require the rotor/SGP4, but still requires
real TX permission and an RF path; integrated Doppler must not silently fall
back to manual. Rotor-only does not start SDR or depend on audio. Antenna-only
does not require a computer. The integrated BOM avoids duplicating CM5,
carrier, and power while keeping shared components traceable.
