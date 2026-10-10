# Third-axis POL mechanical concept

## Scope and status

This is an original, limited-travel roll stage for the existing two-axis BASE.
It turns the existing antenna saddle about the antenna boresight. It does not
replace or modify either existing AZ/EL transmission, firmware, PCB, or their
exports. The third stage uses one GT2 belt reduction; it is not another copy
of the two-stage 25:1 AZ/EL drive.

**Concept only; not a released or load-qualified mechanism.** CAD/STL checks
validate geometry and mesh closure, not stress, backlash, RF performance,
collisions under load, switch timing, accuracy, or safe operation. The
motor, belt, bearings, metal shaft, stop hardware, switch, RF network, and
cable still need exact procurement, fit checks, and testing. Do not transmit
or mount outdoors on the basis of this drawing.

## Mechanical stack and interfaces

`cad/polarization_station.scad` assembles the POL stage on the original
BASE `output_flange()` and attaches the original `saddle(20)` without editing
either helper. The base plate mates to the existing 60 mm output flange:
four 4.5 mm clearance holes on a 44 mm bolt circle (31.11 mm square), plus
the central 22 mm saddle clearance. The removable boom clamp remains the
same 20 mm-bore part; its four mounting bolts retain the BASE 31.11 mm square.
The saddle origin stays at the POL carrier bolt pattern; the original saddle
bore offset (+35 mm Y, +24 mm Z) is explicitly aligned with the POL bearing/
shaft axis at (+35,+24) mm. This preserves the existing boom/antenna
centerline rather than treating the saddle's CAD origin as its clamp bore.

Two 608 bearings (8 x 22 x 7 mm), 48 mm between centers, support an 8 mm OD
metal hollow shaft on the antenna axis. The initial shaft envelope is 8 mm
OD, 5 mm ID, and 96 mm long. The bore is for one small flexible coax only;
connectors do not pass through it. Specify and inspect the actual shaft
material, wall, concentricity, bearing seats, axial retention, and stiffness.
Do not print the load-bearing shaft in ASA. Bearing-seat clearance and retainer
fit are provisional; print a coupon before making the full frame.

The NEMA14/pulley envelope uses the existing motor-face and 26 mm mounting-hole
assumptions. The 3 mm motor-plate DXF is a template, not a verified cut file:
check the selected motor's pilot, screw pattern, shaft, face, cable exit, and
pulley hub against its manufacturer drawing. The paired cheek DXF is a
90 x 64 mm side-plate template with bearing, retainer, tie-rod, switch/stop,
and motor-plate holes. The assembly shows four 3 mm spacer positions between
the cheek reinforcement and motor plate. Two radial contact-screw positions
retain the rotating carrier to the hollow shaft; set screw length and
installation torque so they grip the tube without punching into the coax
passage. The separate split-clamp cam uses an M3 fastener and likewise needs
verified closure and vibration retention. Its dimensions and material are not machined or
structurally verified. Deburr and verify a physical first article before
installation.

## Transmission and travel

The POL reduction is one purchased 20-tooth:100-tooth GT2 stage (5:1), 2 mm
pitch, 252 mm belt pitch length. The exact open-belt geometry gives about
60.56 mm center distance and more than six engaged teeth on the small pulley.
The purchasing envelope in the CAD is not a custom printed toothed pulley.
Tension, belt width, tooth form, pulley bore/hub, retention, and alignment must
be confirmed with the chosen parts.

At the illustrative 200-step motor and 16 microsteps, 5:1 gives 16,000
commanded microsteps per output revolution, or 0.0225 degrees per command
increment. This is resolution arithmetic, **not** accuracy, repeatability,
backlash, or measured polarization-angle precision.

Initial limits are:

| Boundary | POL angle |
| --- | ---: |
| Commanded soft limit | -80 to +80 degrees |
| Normally-closed switch trip target | -85 and +85 degrees |
| Candidate physical hard-stop target | -90 and +90 degrees |

Use two independent NC switches. An open contact, broken wire, or loss of
switch power must be treated as a limit/fault. Metal stop pins, not printed
ASA tabs, take hard-stop contact. The switch-to-stop 5 degree margin is an
initial layout target only; establish actual actuation and stop angles with a
protractor/jig, then verify deceleration and fault response before enabling
motion. The CAD places each 4 mm stop-pin center 36 mm from roll center and
gives the cam a 34 mm reach, so the nominal pin radius exactly meets the cam
tip at +/-90 degrees. This ideal tangency leaves no tolerance reserve; inspect
and adjust the first article so it cannot bind, bypass the pins, or load the
coax. The bracket and side-plate holes are only a starting installation
template; select a real switch, verify lever/contact location and independently
prove stop-pin first-article clearance at both ends. Never use the step count
as a substitute for either switch or stop.
The +/-90 degree angles are unvalidated candidate targets, not tested travel
limits; first-article switch timing, clearances, hard-stop strength, and cable
service-loop behavior must be verified before motion is enabled.
No continuous rotation and no slip ring are intended.

Route flexible coax on the shaft centerline where practical, keep connectors
outside the 5 mm bore, add strain relief, and provide a service loop suitable
for the full -90 to +90 degree sweep. Select coax from its specified bend
radius and RF loss; inspect it through repeated full-range cycles. Do not let
the cable become a hard stop or carry antenna load.

## Loads, inertia, and balance

Run `node scripts/polarization-report.cjs` for reproducible values from
`calc/polarization.json`. It intentionally models an example antenna only:
0.5 kg, 30 mm CG offset, 0.30 m radius of gyration, 0.06 m2 projected area,
and an 8 m/s calculation-only wind case with assumed air density 1.225 kg/m3,
drag coefficient 1.2, and safety factor 2. The 8 m/s input is **not** an
operating limit. No selected motor's dynamic torque curve is provided, so the
report makes no pass/fail claim about motor capability.

For this example the antenna-only inertia about POL/EL is
`m * (k^2 + e^2) = 0.04545 kg m2`; the 0.5 rad/s2 illustration adds
0.022725 Nm inertial torque before gravity, wind, friction, or hardware.
The example AZ inertia is only the point-mass term `m * r^2 = 0.03125 kg m2`
at a hypothetical 250 mm radius. It omits the array's distributed inertia and
all moving AZ/EL/POL hardware. Those examples must not be summed and called a
whole-rotor rating.

For the same assumptions, wind force is 2.8224 N. The distinct example moment
arms matter: 30 mm pressure-center eccentricity gives 0.084672 Nm about POL;
250 mm pointing-axis arm gives 0.7056 Nm about AZ/EL. The 30 mm antenna CG
offset contributes up to 0.14715 Nm gravity moment about a horizontal POL/EL
axis in the worst example orientation; ideal vertical AZ has no gravity
moment. With the illustrative factor 2, antenna-only POL, EL, and AZ moments
are respectively about 0.463644, 1.7055, and 1.4112 Nm. They exclude rotor
hardware, cable drag, friction, acceleration outside the example, and
uncertainty in real antenna area/CG.

Counterbalancing changes both mass and inertia. A point-mass illustration
would need 0.15 kg at 100 mm radius to balance 0.5 kg at 30 mm; that ballast
is not included in the CAD or mass budget and is not a proposed part. Weigh
the complete rotating antenna/saddle/cable assembly and locate its CG before
choosing a counterweight. Measure complete-axis inertia or derive it from
weighed components and measured radii; repeat the AZ and EL load calculation
including their moving frames, motors, harness, and the POL motor. A POL
motor fixed to the elevation frame still adds EL/AZ load even though it is
not rotating about the POL shaft.

Do not reuse the antenna-only example as the three-axis assembly rating. The
conditional two-axis budget is 3.130-3.200 kg, and no mass or CG has been
measured for the added POL frame, extra motor, coax, or rotating-side RF
networks. Their missing contributions remain explicit in
`calc/polarization.json`; after weighing/CG characterization calculate
additional EL gravity as `m_POL * g * perpendicular_CG_offset_EL`, each axis'
added point-mass inertia as `m_POL * r_axis^2` plus the stage centroidal
inertia, and wind moment using the measured projected area, pressure-center
offset, and an agreed operating wind. Until those inputs exist the numeric
three-axis total is unknown; do not add an invented motor-torque or mass
allowance to the old budget.

## Operational station mass gate

The authoritative maximum is **5.000 kg for the complete ready-to-operate
station**, including antenna, all three rotor axes and motors, radio, SBC,
enclosure, station-side power hardware, every station cable/connector,
sensors, and tripod. The **external battery pack/BMS is explicitly excluded**
from this cap; record its actual mass separately as carried mass, never as
zero. The station-side power input cable, connector, conversion, fusing, and
protection still count. Use **4.500 kg as the engineering target** to seek a
preferred 0.500 kg measured margin below the maximum; this is a target, not a
promise that the design will meet it. A charger counts in the station total
when carried as part of the ready-to-operate setup.
The external battery exclusion applies to the physical external pack/BMS
only. The Powerpole input connector pair (both mating halves and contacts),
battery-to-station positive/return leads, positive master fuse and holder, all
three branch fuse-and-holder assemblies, and each branch's conductors and
connectors belong in the 5 kg station mass. The required three separately
fused branches are CM5IO regulated 5 V conversion, motor power through the
reviewed NC emergency-stop cutoff path, and RF PA supply. Fuse ratings,
holders, contact parts, wire gauges, lengths, and actual harness masses remain
TBD pending load/fault-current design and selection. The external pack/BMS
mass remains separately carried and measured.
Also include the three AZ/EL/POL encoder sensors and their three mounting
brackets, a remote fixed-base compass/IMU and its mount, and a stationary GPS
receiver, antenna, and mount. Their masses and every associated cable and
connector belong in the operational total.
The specified compute/radio baseline is one Raspberry Pi Compute Module 5
(CM5), two replaceable LimeSDR Mini units, the official CM5IO carrier and selected
thermal solution, the final enclosure, and every installed SDR power
amplifier/filter and its thermal/RF hardware. Count both SDR modules and their
mounts separately, along with auxiliary control/interface electronics,
mounts, and fasteners. Do not include an ESP32.

`station_total = historical_two_axis_estimate - measured_historical_battery_allowance + current_CM5IO_compute_radio_stack + current_POL + tripod + sensors_mounts + station_side_power + all_station_cables_and_connectors`

`transported_total = measured_station_total + measured_external_battery_pack_and_BMS_mass`

Do not count the external battery pack/BMS in `station_total`; it is still a
real carried item and its actual mass must be measured and reported in
`transported_total` (never enter it as zero to make the total computable).
Include both Powerpole connector halves and contacts, battery-to-station
input leads, the master fuse and holder, all three branch wire pairs and
endpoint connectors, and all four fuse/holder assemblies in station mass,
even if a Powerpole mating half is physically attached to the battery lead.
Count each item once. Include an external charger in station mass if carried
with the ready-to-operate setup.

The historical 3.130-3.200 kg estimate includes an unquantified battery
allowance. Keep that allowance TBD; subtract it from the historical number
only when recovered or measured. The previous raw 1.800-1.870 kg difference
to the 5 kg cap is not available station headroom. Since the historical number
also excludes radio and tripod, corrected station total and headroom remain
unknown until the historical allowance is reconciled and the complete current
station inventory is weighed. Do not infer any allowance or station mass from
that raw difference.

The example 12 V, 1 Ah external pack contains 12 Wh nominally and yields at
most 6 W ideal average over two hours, before usable-capacity, conversion, and
reserve losses. It does not establish two-hour station autonomy; the larger
12 V external pack capacity and mass remain TBD and must be selected and
tested against the actual CM5/SDR load. The pack's measured carried mass is
reported separately from the 5 kg station cap. It is not a zero-mass item.

## Powerpole harness restraint and panel interface

The three protected DC branches are individually mass-budgeted: regulated
CM5IO 5 V conversion, motor supply through the reviewed NC emergency-stop
cutoff, and RF PA supply. Weigh the positive-line master fuse and holder,
each branch fuse/holder, each positive/return branch wire run and endpoint
connectors, the battery-to-station wire pair, and the station-assigned
red/black Powerpole connector pair and contacts as separate items. Ratings,
exact contact/housing part numbers, connector keying, wire-gauge/length,
fuse-holder qualification and all fuse values are TBD. The Powerpole family
or housing color is not proof of connector orientation or polarity; cold-check
the exact assemblies with a DMM before power is connected. The external
pack/BMS itself is the only power-entry item excluded from the station cap.

An optional generic cable tie-down plate is defined as `pol_part=10` in
`cad/polarization_station.scad`; its additive STL export,
`cad/polarization-power-strain-relief.stl`, was rendered with OpenSCAD 2021.01
and mesh-checked as one closed, oriented 3,132-triangle solid (11,769.7 mm3).
Its drawing envelope is 48 x 84 x 3 mm, with four 3.4 mm panel-fastener holes
and four pairs of 3.4 mm cable-tie holes at 12 mm pair pitch. The tie pairs are
provisional restraint points for the incoming lead and each of three outgoing
branches. This is a generic cable restraint, **not a Powerpole connector
mount**: panel spacing, cable/tie fit, printed strength, strain relief and
pull resistance require first-article fit and test. If installed, weigh the
plate, ties and mounting fasteners into the station cap.

A connector-specific Powerpole panel bracket is intentionally deferred: no
exact connector housing, contact, panel-retention feature or manufacturer
outline has been selected and verified. Do not scale this generic restraint,
the SMA interface, or a family-name envelope into a claimed connector fit.
Only release a separate panel bracket after matching the exact selected
housing drawing, retaining hardware, mating arrangement and required panel
thickness.

The inherited baseline excludes the tripod, so weigh and include the complete
selected operational tripod once in the current station total. Its historical
accounting convention treats legacy cables/connectors as included, but verify
that against the physical inventory before sign-off and include any missing
contribution exactly once. Count the antenna and historical battery allowance
once in the baseline reconciliation; the external battery pack/BMS is carried
separately and excluded from the cap. The prior baseline does not establish that the new
encoders, their three brackets, GPS receiver/antenna, compass/IMU, their mounts,
or their sensor wiring are included; count all of them as added mass pending
physical inventory and weighing. Record individual sensor masses in the
mass-budget inputs and procurement checklist, then include each item once in
the aggregate sensor/mount term. Put their harness and connectors in the
separate `sensor_cables_and_connectors` term; the `other_additional...` term
must exclude both that harness and the separately counted RF coax/connector
items. The prior baseline does not establish a compatible CM5 compute stack,
LimeSDR Mini, or their installed radio chain. Weigh and count separately the
CM5 module, official CM5IO carrier, selected heatsink/cooling solution, mounts, one
replaceable LimeSDR Mini, final enclosure, SDR PA modules, filters, shields,
and remaining radio hardware. Do not double-count any included part inside an
assembly mass. The RF roll-up also has separate terms for the SMA
bulkhead jack, its metal interface plate, the POL-axis coax/service-loop
assembly, each of four antenna-feed coax assemblies, and any remaining
component-mounted RF connectors/adapters. The four branches are 145 MHz feed A
and B plus 435 MHz feed A and B; each has its own mass entry and may not be
represented by one shared jumper mass. Include connector mass in its named
cable assembly or connector term once. radio/SBC/enclosure additions are currently unknown, as are the masses of
both LimeSDR Mini units and their mounts, auxiliary station electronics, and
all current additions. Do not assign a station total or available margin from
the historic estimate.

The LimeSDR Mini 69 x 31.4 mm outline is a planning envelope supplied for this
design, not a mass value, fit guarantee, or verified board-revision drawing;
height, connector keep-outs, mounting, and cooling clearances remain TBD. The
official CM5IO carrier selection and CM5 thermal arrangement may require
mechanical changes; verify those with the selected parts. No fit to the old
radio box is implied or claimed.

The GPS antenna stays stationary on the station and must have a clear sky view;
it is not mounted on the rotating boom. The compass/IMU is a separate heading
reference, not an encoder. Mount it on the fixed base away from motors and RF
power hardware; ideally do not share a motor or RF-power housing. Check for
magnetic bias in the assembled, powered station. Do not infer a heading,
heading accuracy, or GPS performance from this mechanical concept. Do not
assume an exact stock module or invent a bracket fit: compass/IMU module and
mount dimensions, GPS receiver/antenna modules and mount dimensions, and their
locations remain TBD. Select the components and record their measured masses
before releasing the hardware selection against the 5 kg limit.

The POL motor is a third, additional motor, and its mass, cost, current, shaft,
and dynamic torque are TBD. The POL frame, shaft, bearings, pulley,
reinforcement, switches, coax/RF additions, and any counterbalance also need
weighing. Since the historical two-axis estimate also omits radio and tripod
and has an unreconciled battery allowance, its raw 1.800-1.870 kg difference
from 5 kg is **not available headroom**. The report leaves corrected station
mass and remaining headroom unknown until the battery allowance is reconciled
and all current station hardware, radio, tripod, and cables/connectors are
weighed. Hardware selection is gated on completing this
mass roll-up; do not claim compliance until the complete configured station
is weighed at or below 5.000 kg. Use `bom/polarization.csv` as a
procurement-and-weighing checklist, not a vendor-quoted or released BOM.

## RF polarization is a separate function

All RF coax interfaces in this concept use standard-polarity **50-ohm SMA**;
RP-SMA, BNC, and N-type are not allowed in the RF coax chain. This requirement
applies to RF/coax connections only: do **not** replace or adapt Baofeng
handset, speaker, microphone, or other audio/accessory jacks to SMA. Those
existing audio interfaces are unchanged.

The fixed-base coax entry is a dimensioned interface, not a selected or
measured connector. `cad/polarization-coax-interface.dxf` defines a provisional
30 x 22 x 3 mm metal tab with a 6.5 mm bulkhead clearance hole for a nominal
1/4-36 UNS SMA coupling thread, two 3.4 mm strain-relief holes on 10 mm centers
at a 6 mm offset, and two 3.4 mm mounting holes on 24 mm centers. Measure the
actual purchased SMA jack, thread, nut, panel-thickness allowance, and mass;
confirm it fits the 3 mm tab before release. The matching cable-tie holes are
the only defined strain-relief provision here; select and test the actual
tie/grommet and coax path. Connectors remain outside the shaft's 5 mm bore.

Choose lightweight 50-ohm coax only after its loss/power/frequency rating and
minimum bend radius are checked for the selected cable and complete route.
Record the mass of the shaft service-loop trunk and the four individual antenna
feed jumpers with their ends. Coax types, lengths, bend radii, and assembled
masses are all TBD; lightweight construction must not be treated as evidence
that the RF or mechanical requirements are met.

Turning the antenna mechanically about boresight does **not** convert RHCP to
LHCP. Handedness selection requires a compatible circular antenna with
independent orthogonal feed ports for each band. As a conceptual topology, each
band has its own 90-degree quadrature hybrid: the orthogonal antenna feeds go
to the two hybrid output ports; an RF-rated DPDT transfer switch cross-connects
the radio source to one hybrid input and a 50-ohm rated termination to the
other. Swapping source and load between hybrid inputs reverses the relative
feed phase and therefore selects the opposite handedness, assuming a compatible
antenna and the actual hybrid's port/phase convention. This is an unvalidated
network concept, not a selected schematic or RF design.

Implement one independently qualified network/switch for each of 145 MHz and
435 MHz. A single coax passing the hollow roll shaft requires a compatible
145/435 MHz diplexer on the rotating assembly before the band-specific
networks and its reciprocal mate at the radio end; this added rotating mass is
also TBD. The existing linear-polarized prototype antenna is not compatible:
use an antenna with the appropriate independent orthogonal feeds per band.
Verify each hybrid's phase balance, bandwidth, insertion loss, isolation, RF
power, loads, connectors, and antenna convention with VNA/known signal before
operation. Switches, coupling networks, 50-ohm terminations, control, and
transmit interlock remain unselected and unmeasured. Keep this RF control
electrically independent from the POL motor; inhibit RF transmit during switch
transitions and on uncertain/faulted switch state. The switch's voltage,
current, fail state, break-before-make behavior, interlock, and reflected-power
handling require explicit design and test. No commercially available part,
power rating, or measured RF result is claimed here.

## Reproduction and acceptance

Render STL and DXF outputs with the local OpenSCAD CLI, selecting numeric
`pol_part` values in `cad/polarization_station.scad`: 1 frame, 2 rotor carrier,
3 bearing retainer, 4 limit cam, 5 limit bracket, 6 original BASE saddle,
7 motor-plate DXF, 8 cheek-plate DXF, and 9 coax-interface DXF. `pol_part=0`
shows the assembly; it is a visualization, not a printable STL. Inspect the physical fit
of the 20 mm saddle, existing flange, actual pulleys/motor, bearings, cable,
stops, and NC switches. Test switch break-before-stop and full cable sweep
with motor power disconnected first; then perform supervised low-speed
bench tests with RF disconnected and independent emergency power isolation.
`pol_part=10` selects the optional generic cable-tie strain-relief plate; it
does not fit or retain a Powerpole connector housing. Preserve all existing
exports and export this as a new STL without overwriting another part.
