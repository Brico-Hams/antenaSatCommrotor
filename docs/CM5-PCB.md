# CM5IO auxiliary control PCB

## Scope and release status

This is an original auxiliary control-board design for the official
Raspberry Pi Compute Module 5 IO Board revision 2 (CM5IO rev 2). The CM5
remains installed on CM5IO; this PCB connects only to its 40-pin GPIO header.
It is not a CM5
standalone carrier and does not reproduce or depend on the CM5 high-speed
board-to-board connector pinout.

The selected CM5 candidate is **CM5104016** (wireless, 4 GB RAM, 16 GB eMMC).
The exact CM5 SKU remains a procurement confirmation; it does not change this
GPIO-only interface. Set the CM5IO 40-pin-header VIO jumper to **3.3 V** before
connecting this board. Do not connect a 1.8 V header configuration.

The two LimeSDR Mini devices occupy CM5IO rev 2's two native USB 3 ports. No USB 3
signals are routed through the auxiliary board. The preferred host arrangement
retains CM5IO's separate USB-C power input and USB data/host connectors; they
are not one combined power-and-data connection, and connecting either does not
guarantee that the other is available or host-capable. Treat 5 V / 5 A as a
power-system target only: the source must negotiate the required USB-C PD
contract, the CM5IO input path must support it, and the complete concurrent
load must be measured. A 5 V / 3 A source is not accepted as sufficient for
this design: two LimeSDR Mini peripherals at the stated 600 mA each already
account for 1.2 A, leaving at most 1.8 A for the CM5, CM5IO losses and all
other loads, before peaks. A source marked 5 A is not enough by itself; verify
the negotiated contract and use a properly rated 5 A e-marked USB-C cable
where the negotiated current requires one. Do not infer a generic USB-C
connector or cable supports 5 A.

Keep the auxiliary PCB's power, USB data, and RF interfaces distinct. Do not
feed the two LimeSDR Minis from the auxiliary board's 40-pin header 5 V rail
or route their USB data through the auxiliary PCB. The audio target is onboard
speaker and microphone audio through a USB codec, plus a separate,
not-yet-qualified Kenwood-style K1 dual 3.5 mm / 2.5 mm accessory interface
for UV-5R/UV-82-compatible accessories. This is a compatibility target, not a
verified radio/accessory pinout. The audio jack belongs on a separate DNP
daughterboard; its interconnect header, pin assignment, and harness remain
unfrozen until checked against the actual radio and accessory. Never infer the
BTL (busy-tone lamp) contact to be ground or connect it to audio ground.
Audio return may connect only to the verified ground-referenced audio-driver
return; keep it separate from the BTL contact unless the exact accessory
circuit is verified.
Do not connect audio to the RF, PTT, motor, or limit nets on this PCB.

Digital design files, if present, are not a production release. Gerber,
Excellon, BOM, and CPL exports must be generated from the same reviewed board
revision. PCBA release requires zero KiCad ERC/DRC/unconnected/parity issues,
verified assembly-part numbers and footprints, and completion of the review
items below. No order, upload, or physical test is authorized by this design.
No weight, tracking accuracy, RF power, motor torque, thermal margin, or
5 kg complete-station result is claimed. The external 12 V battery is
explicitly excluded from the 5 kg mass objective.

## External battery, Powerpole, and power conversion contract

The power source is an external battery with a **12 V nominal** interface;
the battery pack is excluded from the 5 kg equipment-mass objective. Battery
reference is the ECO-WORTHY 12 V 30 Ah LiFePO4 product variant
`40308275183822` ([vendor listing](https://es.eco-worthy.com/products/bateria-litio-lifepo4-12v-30ah?currency=EUR&country=ES&variant=40308275183822)).
This is a candidate, not a procurement or pack-electrical freeze: verify the
exact delivered model, 30 Ah capacity, internal BMS limits, continuous/peak
current, connector, and datasheet before relying on them. Do not assume the
listing establishes the pack's charge voltage, cutoff, or maximum load.
LiFePO4 full-charge voltage **14.6 V is provisional only** and may be used
for component stress screening only after confirming it for the exact pack.
Until then, battery chemistry-specific full/low voltage and all ratings remain
unfrozen; Ã¢â‚¬Å“12 V nominalÃ¢â‚¬Â is not a 12 V maximum rating. The 30 Ah label
corresponds to 360 Wh only if the exact delivered model and rated capacity
are confirmed; it does not prove autonomy. The battery is externally carried,
not installed in the station mass tally, and excluded from its 5 kg objective.
Do not connect any raw battery voltage to CM5IO's 5 V USB-C power input or its
40-pin 5 V pin.

The battery uses a separate, modular **Anderson Powerpole 15/30/45 family**
red/black battery-harness interface, with the actual crimp contacts selected
from that family for the verified wire gauge and load. Do not choose a 15 A,
30 A, or 45 A contact rating by nominal label alone: confirm the exact contact
part, wire range, crimp tool, housing, temperature/derating, voltage, and
continuous/peak-current suitability against the manufacturer's primary
datasheet and the measured system load before BOM/footprint freeze. Mating
red/black housings are to be used with correct polarity/keying; validate
mechanical mating and polarity against the actual battery harness.

Use a battery cable/pigtail with the mating Powerpole pair and terminate it
at an **exactly selected, current-rated PCB terminal connector**. Do not put a
Powerpole housing footprint or a bare, unidentified Powerpole contact directly
on the PCB. The board-side connector must be selected from a verified
manufacturer part/datasheet for the actual conductor size, PCB footprint,
current, temperature rise, and mating compatibility. Until selected, neither
the PCB terminal footprint nor the Powerpole contact, wire gauge, or current
rating is frozen.

Required power sequence is battery positive -> pack-adjacent main DC fuse ->
main disconnect/service isolation -> protected distribution, with separate
DC-rated branch fuses for (1) the CM5IO 5 V USB-C converter, (2) the motor
supply/converter, and (3) each PA/RF supply branch as applicable. Fuse and
holder voltage/current/interrupt ratings must suit the selected pack and load.
Do not select arbitrary fuse amperages: measure continuous, startup, stall,
and transmit peaks; verify fuse time-current/inrush behavior and thermal
derating; and ensure each fuse does not exceed the safe current rating of
every protected wire, connector/contact, PCB terminal, and holder. The pack
BMS is not a substitute for the external pack-adjacent fuse or branch fuses.
The latching DC-rated E-stop remains an independent motor-supply stop path;
the battery service disconnect and fuse do not replace it.

### Battery input EMI / power-integrity design gate

The battery-entry design is not a generic ideal LC filter and no component
values or high-current choke are selected. Pre-layout topology to evaluate is:

1. Powerpole battery harness and a verified rated PCB terminal; battery-side
   pack-adjacent fuse; main service disconnect.
2. Reverse-polarity protection sized for the verified pack current and fault
   energy; a coordinated TVS/transient clamp that remains inactive over the
   verified normal pack range; controlled inrush.
3. An optional common-mode choke must carry **both** DC positive and return
   through the intended coupled windings, selected and derated for maximum
   continuous and transient current, winding DCR, saturation, temperature rise,
   insulation, and fault behavior. Never put a small-signal ferrite or
   300 mA-class bead in series with a 5 A CM5IO supply path. Its insertion
   impedance must be checked at the conducted-noise frequencies of interest;
   it is not by itself an RF emissions or receiver-desense solution.
4. An optional connector/header filter module is TBD and is not populated or
   assigned an invented footprint. Any module/header requires an exact
   interface, contact/copper rating, polarity, location, approved part,
   assembly state, and documented impedance/current data. If testing proves
   an off-board filter necessary, add a separately rated, documented module
   interface and re-run schematic parity, ERC, DRC, connectivity, thermal and
   manufacturing checks before exporting a new board revision.
5. A differential input filter, only if justified by converter-vendor guidance
   and measured impedance, must be deliberately damped and checked with the
   actual converter input impedance, cable/source impedance, capacitance and
   ESR over operating modes. Do not blindly cascade high-Q LC sections: a
   switching converter's negative incremental input impedance can destabilize
   an undamped input filter. Prove startup, load-step, line-step, brownout,
   current-limit and recovery stability with representative source impedance
   and both CM5IO/motor branches operating.
6. Fused, separated branches for the CM5IO 5 V USB-C converter, motor power,
   and each PA/RF supply branch as applicable; use local decoupling at each
   converter/load and keep high-di/dt motor/PA loops physically separate from
   CM5 5 V logic, GNSS, compass, encoders and audio. Define a deliberate return
   and shield/chassis strategy; do not use an unreviewed shield bond or motor
   return path through sensor/audio ground.

Select no common-mode choke, differential inductor/capacitor, bead, ferrite,
TVS or fuse current until the exact part datasheets, measured branch loads,
startup/stall/transmit currents, wiring and converter stability guidance are
available. Any ferrite must meet DC-bias/saturation and DCR drop requirements
at the actual branch current. Quantify regulator input and output ripple,
transient response, temperature rise, conducted noise, CM5IO 5 V droop/
undervoltage behavior and recovery; verify Linux stability under simultaneous
two-LimeSDR streaming, motor starts/motion and radio transmission.

Do not equate conducted power filtering with antenna-port filtering or RF
desense control. Preserve the SMA RF paths; measure receiver sensitivity/
desense and transmit spurs/harmonics at the SMA ports over 145/435 MHz
operating cases after integration. In particular, the 145 MHz third harmonic
near 435 MHz requires actual emission testing; neither a DC input choke nor
unmeasured insertion loss establishes compliance or RF coexistence.

The autonomy objective is at least **2 hours** at a defined representative
whole-system duty cycle. Pack capacity must be strictly greater than **1 Ah**
at 12 V nominal (>12 Wh), but 12 Wh is only a minimum floor and does **not**
establish two-hour runtime. Size from measured average battery-side load,
including CM5/CM5IO, both LimeSDRs, audio, control electronics, conversion
losses, and the agreed radio-transmit and motor-motion duty cycle. Use
`required nominal Wh >= measured average battery-side W * 2 h / usable-energy fraction`
with the usable-energy fraction determined for the selected pack, temperature,
age, cutoff, and reserve. Independently size protection, wiring, connectors,
and regulators for measured startup and peak currents.

The CM5IO supply path is separate from the auxiliary-board battery input:
convert the battery to a correctly implemented, negotiated USB-C 5 V supply
for CM5IO, targeting 5 V / 5 A only after checking CM5IO's actual input
specification and measuring the full load. Do not send raw 12 V to a USB-C
power pin, the 40-pin header, or the CM5. Source/cable capability, PD
negotiation and any required 5 A e-marker must all be verified together.

The auxiliary PCB's 12 V nominal battery input must have a chemistry-compatible
pack protection/BMS path, pack-adjacent fuse, reverse-polarity protection,
short-circuit/overcurrent protection, and appropriately rated, protected
conversion stages for each selected rail. Include transient suppression (TVS
or equivalent selected to the verified pack and converter limits) and
controlled inrush; the suppressor must stay inactive at normal maximum pack
voltage and its clamp/energy rating must coordinate with protection and
converter absolute-maximum ratings. A TVS by itself does not establish surge
immunity. For conservative front-end
component stress screening, target battery-input components rated for at
least 30 V; this is a design margin, not proof that the battery can or should
operate at 30 V. Revisit the rating against the actual pack voltage window,
transients, protection coordination, and selected components before release.
The 5 V logic rail must use an isolated regulator from the battery input;
select and verify the converter's input range, output/load rating, isolation,
EMI, thermal behavior, and fault handling. Motor-supply conversion remains
separate and is not assumed isolated; its supply must be independently
interrupted by the DC-rated latching E-stop path. Actual battery full/minimum
voltage, motor voltage/current, fuse values, connector, and regulator parts remain
unfrozen; these candidate ratings do not authorize layout or release. Do not route the
LimeSDRs' load through the 40-pin 5 V rail. Keep the motor-supply, logic,
CM5IO USB-C power and USB data paths distinct and verify returns, inrush,
noise, and fault behavior before release. This battery/power clarification
does not replace the existing SMA RF paths or separate external K1 audio
target; neither RF nor audio is routed through USB-C power.

## Frozen 40-pin GPIO contract (revision A)

BCM GPIO numbers below are Linux GPIO numbers, not physical header pin
numbers. Direction is from the CM5IO/CM5 perspective. This map is frozen for
the rotor controller and radio hardware adapter. Changing a BCM or header pin
requires a versioned interface revision and coordinated software update.
Pulls and hardware gates listed below are design requirements, not evidence
that hardware has been fabricated or verified.

| BCM GPIO | Header pin | Net / purpose | Direction / polarity / reset contract |
|---:|---:|---|---|
| 2 | 3 | I2C1 SDA, mux/safety-expander bus | Bidirectional, 3.3 V |
| 3 | 5 | I2C1 SCL, mux/safety-expander bus | Open-drain/released HIGH, 3.3 V |
| 4 | 7 | AZ minimum NC limit | Input; LOW=closed/healthy, HIGH=open/fault |
| 5 | 29 | AZ maximum NC limit | Input; LOW=closed/healthy, HIGH=open/fault |
| 6 | 31 | EL minimum NC limit | Input; LOW=closed/healthy, HIGH=open/fault |
| 7 | 26 | EL maximum NC limit | Input; LOW=closed/healthy, HIGH=open/fault |
| 8 | 24 | POL minimum NC limit | Input; LOW=closed/healthy, HIGH=open/fault |
| 9 | 21 | POL maximum NC limit | Input; LOW=closed/healthy, HIGH=open/fault |
| 10 | 19 | E-stop auxiliary NC monitor | Input; LOW=closed/healthy, HIGH=open/fault |
| 11 | 23 | External watchdog heartbeat | Output; CM5 supplies heartbeat edges |
| 12 | 32 | Motor arm request | Output; HIGH=request, external pulldown means reset=OFF |
| 13 | 33 | TCA9548A RESET_N | Output; LOW=reset, external pull-up means reset=inactive |
| 14 | 8 | GNSS UART TX | Output; idle HIGH, CM5 TX to receiver RX |
| 15 | 10 | GNSS UART RX | Input; receiver TX to CM5 RX, 3.3 V |
| 16 | 36 | SPI1 CS2, POL driver | Output; active LOW, external pull-up |
| 17 | 11 | SPI1 CS1, EL driver | Output; active LOW, external pull-up |
| 18 | 12 | SPI1 CS0, AZ driver | Output; active LOW, external pull-up |
| 19 | 35 | SPI1 MISO | Input; 3.3 V |
| 20 | 38 | SPI1 MOSI | Output; idle LOW, 3.3 V |
| 21 | 40 | SPI1 SCLK | Output; idle LOW, 3.3 V |
| 22 | 15 | VHF PA PTT request | Output; HIGH=request, external pulldown means reset=OFF |
| 23 | 16 | UHF PA PTT request | Output; HIGH=request, external pulldown means reset=OFF |
| 24 | 18 | AZ driver diagnostic | Input; LOW=fault, buffer/level limits to 3.3 V |
| 25 | 22 | EL driver diagnostic | Input; LOW=fault, buffer/level limits to 3.3 V |
| 26 | 37 | POL driver diagnostic | Input; LOW=fault, buffer/level limits to 3.3 V |
| 27 | 13 | GNSS PPS | Input; optional timing pulse, not a fix-valid signal |

The 26 exposed BCM GPIOs are completely allocated by this table. In
particular, GPIO0/1 (physical ID_SD/ID_SC) are reserved and not used.

Frozen SPI1 wiring is MOSI GPIO20, MISO GPIO19, SCLK GPIO21, with CS2/CS1/CS0
on GPIO16/17/18 respectively. Linux SPI device naming and overlay selection
must be confirmed against the booted CM5IO image; the BCM line assignment
does not itself configure a Linux overlay. I2C1 serves the TCA9548A at the
default address 0x70; channels 0, 1, and 2 serve the three AS5600 encoders,
channel 3 the compass, and channel 4 the IMU. Channels 5-7 are not connected
unless a later revision assigns them. GNSS uses UART0 GPIO14/15; PPS is
optional and uses GPIO27. GPIO0/1 (physical ID_SD/ID_SC) are reserved.

The OS integration contract is SPI1, I2C1, and UART0 on the assignments above.
Do not enable or alias SPI0 in place of SPI1, and do not let stale device-tree
overlays reassign these BCM pins. Verify the actual CM5IO boot-image overlay
names and resulting `/dev/spidev*`, I2C, UART, and GPIO line identities on the
target image before adapter integration. At every cold boot, reboot, service
restart, GPIO-provider recovery, and expander reset, initialize motor-arm,
per-axis enable, and both PTT requests to their inactive states. No OS service,
overlay, or application may automatically arm motors or request transmit on
startup. Software defaults do not replace the required external hardware
fail-off gates.

The common motor-arm GPIO is a request, not a safety-rated enable. The frozen
software pin assignment uses an MCP23017 at I2C address 0x20: GPA0/1/2 are
per-axis AZ/EL/POL enable requests (HIGH=request, external pulldown=OFF during
reset); GPA3 is motor-permit feedback, GPA4/5 are VHF/UHF PTT feedback, and
GPA6/7 are VHF/UHF PA fault inputs. These expander lines are software
observability/requests, not safety functions; their exact circuits and
connector interfaces remain blockers. Expander reset, power loss, or
unconfigured pins must never assert driver enable. Each active-low driver EN
must also be gated by independent hardware requiring a healthy external
watchdog and closed E-stop chain. An expander output is not a safety function.

The physical, latching E-stop must independently interrupt the motor supply
through a DC-rated external contact/contactor sized for the selected supply
and motors. A software monitor or a PCB GPIO is not that power-cut path.
Loss of watchdog, E-stop chain, or logic power must inhibit all three motor
drivers and both PTT outputs. PTT request pins each have external pulldowns
and must pass through separately isolated, fail-off outputs; their external
ratings, connector pinouts, and feedback availability remain unselected.

Six NC limit contacts are separate circuits, one per travel end; every open
switch or broken wire is a fault. They are frozen as GPIO monitor inputs only.
No direct hardware hard-limit path to the selected driver's ramp input is
verified or allocated yet. **Do not move the motors** until the schematic
adds and validates a direct hardware limit/driver-stop path. Do not connect a
5 V or 12 V switch circuit to a CM5 GPIO.

## Hardware blockers (do not treat as board release)

- Add a separately verified, normally-off hardware path for all six hard
  limits; BCM limit monitoring alone is not sufficient.
- Select and prove an external watchdog circuit and its timeout/startup
  polarity. BCM11 is a heartbeat **output**; watchdog expiry must physically
  deassert driver enables and both PTT outputs, independent of Linux.
- Freeze a DC-rated latching E-stop/contact/contactor, supply-current
  protection, and the motor-supply cut path. GPIO10 monitors an isolated
  auxiliary NC contact only.
- Freeze per-axis EN gating, including CM5 GPIO12 arm request, MCP23017
  outputs GPA0..2, expander-reset behavior, and external default-off pulls.
- Freeze the two PTT isolation/connector circuits and PA feedback electrical
  limits. GPIO22/23 are logic-level requests, not PA drive outputs.
- Freeze and validate the actual UV-5R/UV-82 radio and K1 accessory pinout,
  separate jack-daughterboard header, ground reference, and audio/BTL
  separation before populating or connecting that interface.
- Complete the onboard speaker/microphone path: a public USB codec candidate
  is TI PCM2902C, but its host connection, microphone front end, speaker
  amplifier, analog levels, and RF coexistence have not been designed or
  qualified. Do not treat the codec candidate as a completed audio circuit.
- Qualify the CM5IO USB host topology and powered-hub/power budget for two
  LimeSDR Minis plus audio. No audio USB host port or hub is frozen.
- Verify CM5IO's separate USB-C power-input and USB data/host connector roles,
  exact supported PD input contract/current, source negotiation, and complete
  concurrent-load margin. A 5 V / 5 A target is not a board rating or evidence
  of available power. Measure the complete system, including two LimeSDRs,
  CM5/CM5IO, audio, losses, and startup/transmit peaks.
- Verify that any source and 5 A e-marked cable actually negotiate the required
  Type-C/PD current; do not use a passive or unverified USB-C breakout,
  resistor-only substitute, or assumed 5 A cable.
- Select the external 12 V nominal battery chemistry, real full/low-voltage
  window, capacity above 1 Ah, continuous/peak current, pack protection/BMS,
  pack-adjacent fuse, Powerpole contact/housing/wire combination, PCB
  terminal connector, and tested two-hour system duty cycle. The
  current pack reference is an ECO-WORTHY 12 V 30 Ah LiFePO4 candidate; verify
  the exact item/model, stated capacity, BMS, and current limits from the
  delivered pack documentation. Its vendor listing alone does not confirm
  14.6 V charge voltage, minimum voltage, discharge current, or runtime. Treat
  14.6 V as provisional for component stress screening only after that
  confirmation. The 30 Ah label would be 360 Wh nominal only if verified.
  Battery mass is excluded from the 5 kg objective; tripod, radio, and all other
  station equipment remain included. The >12 Wh capacity floor alone does not
  satisfy the two-hour objective.
  - Design and rate the battery-to-CM5IO 5 V USB-C power converter for the
    verified CM5IO input and negotiated contract; raw battery voltage must never
    reach CM5IO's 5 V input or 40-pin 5 V header. Separately freeze and rate the
    auxiliary **isolated 5 V logic** converter and separate motor conversion
    rails, protection, returns, inrush handling, and fault behavior. Freeze the
    pack-adjacent main fuse/disconnect and DC-rated branch fuses for CM5IO,
    motor, and PA/RF power. Set fuse ratings only after measured load, cable,
    connector, holder, inrush, and time-current coordination; BMS protection is
    not a substitute. Use at least
    30 V input-rating components for conservative preliminary battery-front-end
    stress screening, then verify against the exact pack window and transients
    before freezing any ratings.
- Do not route auxiliary-board or LimeSDR load current through the CM5IO
  40-pin 5 V header. Verify the complete power budget and startup/transmit
  peaks before selecting regulators, current limits, fuses, conductors, or
  copper widths.
- Complete the measured battery-entry EMI/power-integrity review before
  routing: evaluate a DC-current-rated common-mode choke in both supply and
  return, any exact connector/header-filter module, and a damped differential
  input filter against the chosen converters' stability/input-impedance
  guidance. Do not insert a generic ferrite or high-Q ideal LC without
  current-rating and stability evidence. Measure power droop, ripple,
  transients, thermal rise, Linux stability, receiver desense and harmonics;
  the 145 MHz third-harmonic case near 435 MHz remains a separate RF test.
- Validate the Watterott module's physical socket keying and the exact
  v1.5 schematic/pad order; verify the diagnostic signal's voltage and
  buffering before BCM24..26.
- Verify all named sensor/GNSS breakout revisions, their cables and pinouts,
  module current budget, SPI/I2C/UART overlays, and CM5IO rev 2 host/audio
  topology.
- Source exact JLCPCB/LCSC part numbers and assembly packages. Until then,
  do not manufacture PCBA BOM/CPL placeholders or represent the build as
  assembly-ready.
- Defer component pricing until exact, sourceable manufacturer and LCSC part
  numbers are verified; no price estimate is supported by the current design.
- Bench-qualify motor current/thermal margins, ramp/limit behavior, watchdog,
  E-stop, PTT default-open, RF/audio coexistence, and final enclosure/5 kg
  complete-station mass before field operation.

## Replaceable external modules

The frozen software sensor contract uses these manufacturer-specific external
breakouts; their exact board revisions, physical connectors, and cables still
need confirmation. They are not footprints placed on this PCB. Auxiliary PCB
sensor connectors are assigned a keyed 4-pin I2C interface (GND, 3V3, SDA,
SCL); do not represent it as JST-SH or STEMMA QT unless the exact footprint,
pin order, and cable assembly are validated:

| Function | Selected module | Interface |
|---|---|---|
| AZ/EL/POL encoder, 3x | Adafruit AS5600 Magnetic Angle Sensor, PID 6357 | I2C, 0x36; separate TCA9548A channels 0/1/2 |
| Compass | Adafruit LIS3MDL 3-axis magnetometer, PID 4479 | I2C; TCA9548A channel 3 |
| IMU | Adafruit LSM6DSOX 6-DoF breakout, PID 4438 | I2C; TCA9548A channel 4 |
| GNSS | Adafruit Ultimate GPS Breakout, PID 746 | UART0 3.3 V logic, optional PPS |

Use 3.3 V sensor power and logic. Verify the chosen breakout revision,
installed pull-ups, actual connector pin-1 orientation, magnetic encoder
mounting/air gap, and sensor cable routing before connection. Calibrate and
validate the compass away from motors, steel, encoder magnets, power wiring,
and RF hardware; the PCB does not establish true heading. The external
breakouts and cables are not in the PCBA BOM or CPL.

## SilentStepStick TMC5160 v1.5

Only the Watterott SilentStepStick TMC5160 v1.5 is in scope; do not substitute
another TMC5160 carrier by name alone. The board-level interface uses SPI1
with a unique pulled-up chip select per axis. Respect the module's v1.5
configuration: leave its SD_MODE jumper open, which selects the ramp
controller through the documented external pull-down; set SPI_MODE to VIO;
connect CLK to GND for the internal clock; hold EN at VIO for disabled; and
fit an external pull-up at each CS. Verify the actual module revision and
jumper state before socketing.

The Watterott v1.5 drawing identifies the top-side pin order. Viewed with the
module's MOSFETs facing up, left column top-to-bottom is EN, SDI/CFG1,
SCK/CFG2, CS/CFG3, SDO/CFG0, DCO, STEP, DIR; right column top-to-bottom is
VM, GND, M2B, M2A, M1A, M1B, VIO, GND. Confirm the downloaded, pinned v1.5
schematic and module keying against the physical module before assigning
socket pad numbers. Do not use a TMC2209 footprint.
Driver clock tolerance, programmed current, cooling, VMOT range, limit
polarity, stop ramp, and physical limit response require driver-datasheet
review and bench tests.

## Audio interface and CM5IO USB/RF separation

The onboard audio target is a USB codec with speaker and microphone paths.
TI PCM2902C is a public codec candidate, not a released or validated circuit;
the microphone front end and speaker amplifier still need actual parts,
schematic design, and level/power checks. The CM5IO host connection remains
unfrozen. Do not consume either native USB 3 port for audio when both are
occupied by LimeSDR Minis. Verify any alternate CM5IO host path or powered hub
for host role, bandwidth, power, and simultaneous-radio behavior. Do not
assume the USB-C connector is a host port.

CM5IO's USB-C power input and USB data/host connection are separate interfaces;
do not describe them as one combined cable/port or infer a data-host role from
the power connection. Confirm the exact board-revision connector roles and
configuration from the CM5IO documentation and bench tests.

The supply design target is 5 V / 5 A only after negotiation and power-budget
verification. The two LimeSDR devices' stated 600 mA each consume 1.2 A,
leaving only 1.8 A on a 5 V / 3 A source for CM5/CM5IO and all remaining loads.
Therefore 5 V / 3 A is not an acceptable design assumption. A 5 V / 5 A
label, USB-C plug, or cable does not prove that current is available: qualify
the source's negotiated PD/current capability, the CM5IO input rating, and the
cable's 5 A e-marker where required. Measure startup, sustained concurrent
radio/audio, and transmit peaks. Do not load the auxiliary-board 40-pin 5 V
rail with the two LimeSDRs; keep their power and native USB 3 data on the
verified CM5IO power/host paths.

The external-radio target is a Kenwood-style K1 dual 3.5 mm / 2.5 mm jack
compatible with UV-5R/UV-82 accessories. Neither an exact radio/accessory nor
its pinout has been verified. Keep the jack on a separate daughterboard and
leave that connector interface DNP until the jack-to-header wiring, electrical
levels, and isolation are measured and documented. Do not assign radio
accessory contacts from a generic K1 diagram, and never use a BTL contact as
an assumed ground. Audio return may connect only to the verified
ground-referenced audio-driver return. The daughterboard header pinout is
intentionally not defined yet.

The auxiliary PCB contains no SMA connector, RF trace, radio audio jack, or
LimeSDR USB data connection. Keep the two LimeSDR chains, PA/filter paths,
onboard audio, and external-radio audio electrically independent. PA PTT
interfaces are separate from audio and remain disabled until the selected PA
pinout, PTT voltage/current, and fail-off behavior are tested. Neither an
unpopulated connector nor a codec candidate demonstrates working audio, and
this board is not evidence that either 5 W FM or 5 W PEP, USB 1 W,
full-duplex RF, or audio performance has been achieved.

## Fabrication and verification gates

1. Freeze the exact CM5IO revision, 40-pin VIO jumper at 3.3 V, exact CM5 SKU,
   Watterott driver revision, and external cable/module connector orientations.
2. Check schematic-to-PCB parity, 40-pin mapping, every TMC5160 v1.5 socket
   pad against its primary schematic, limit polarity, watchdog truth table,
   E-stop cut path, and isolated PTT outputs.
3. Run KiCad 10 ERC and DRC with all severities, schematic parity, and
   unconnected-item checks. Resolve every violation; do not disable checks to
   make a report green.
4. Export Gerber copper/mask/silkscreen/outline and PTH/NPTH Excellon with the
   same board origin. Independently inspect the CAM, board outline, drill
   files, connector orientation, netlist, and assembly keep-outs.
5. Generate JLCPCB BOM and CPL from the same validated PCB. CPL Designator
   values must be the exact unique reference designators assigned in the
   schematic/PCB; the radio's Ã¢â‚¬Å“K1Ã¢â‚¬Â accessory-interface name is not a PCB
   reference designator. Use the JLCPCB placement columns
   `Designator,Mid X,Mid Y,Layer,Rotation`; coordinates are board placement
   centers in mm, and each reference/side/orientation must be checked against
   the assembled board view before upload. Exclude DNP parts from assembly
   placements and mark them explicitly in the BOM. Only populate LCSC numbers
   verified against the exact manufacturer part and package. Mark manual
   through-hole sockets, headers, modules, and DNP parts explicitly; do not
   create false placements for them. No CPL rows or reference designators are
   issued yet because there is no validated CM5 auxiliary PCB.
6. Bench-test current limits, power-up/reset states, all NC cable-open
   faults, watchdog timeout, E-stop power interruption, all three driver
   disable paths, per-axis limit response, SPI readback, TCA9548A recovery,
   encoder magnet status, GNSS fix/PPS, isolated PTT default-open state, and
   RF/audio interference before enabling any motion or transmission.

## Primary references

- [Raspberry Pi CM5 and CM5IO documentation](https://www.raspberrypi.com/documentation/computers/compute-module.html)
- [Raspberry Pi CM5 datasheet](https://pip.raspberrypi.com/documents/RP-008180-DS)
- [Watterott TMC5160 SilentStepStick pin configuration](https://learn.watterott.com/silentstepstick/pinconfig/tmc5160/)
- [Watterott SilentStepStick TMC5160 v1.5 schematic (pinned revision)](https://github.com/watterott/SilentStepStick/blob/098b7518b0de31e6a12fda78c68ae2666b81fbb6/hardware/SilentStepStick-TMC5160_v15.pdf)
- [TI TCA9548A product page](https://www.ti.com/product/TCA9548A)
- [TI PCM2902C USB audio codec](https://www.ti.com/product/PCM2902C)
- [Adafruit AS5600 PID 6357](https://www.adafruit.com/product/6357)
- [Adafruit LIS3MDL PID 4479](https://www.adafruit.com/product/4479)
- [Adafruit LSM6DSOX PID 4438](https://www.adafruit.com/product/4438)
- [Adafruit Ultimate GPS PID 746](https://www.adafruit.com/product/746)

## Guard A routed engineering review (2026-10-10, second step)

An original connected schematic and routed two-layer review board are in
`hardware/cm5/cm5-guard-A.kicad_sch` and `.kicad_pcb`. KiCad10.0.7 reports
**ERC0, DRC0, unconnected0, schematic-parity0** under the documented rules.
See [current decisions, rule changes and unresolved qualification](../hardware/cm5/DESIGN-REVIEW.md).
The update adds a manual rearm latch with asynchronous fault reset, fixed
12.7mm TMC5160 socket-column geometry, four physical SMA passive feed-throughs,
and a candidate DNP fused/protected input and common-mode EMI branch. Powerpole
remains the external harness-to-terminal architecture required above.
Fuse inserts/current ratings, reverse/transient/inrush behavior, converters,
PD, thermal/current capacity, RF/USB impedance, modules, sourcing and physical
safety tests are **not qualified**. The converter remains external/unselected.
Clean digital checks do not close those gates. Gerber/Excellon and candidate
BOM/CPL are review snapshots under `fabrication/NOT_FOR_MANUFACTURE`.
**NOT FABRICABLE; no order, battery/motor/PA operation or physical validation
is claimed or authorized.** The frozen interface JSON is unchanged.
