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
same 20 mm-bore part; the four saddle fasteners remain accessible.

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
and motor-plate holes. Its dimensions and material are not machined or
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
motion. Never use the step count as a substitute for either switch or stop.
The +/-90 degree angles are unvalidated candidate targets, not tested travel
limits; first-article switch timing, clearance, hard-stop strength, and cable
service-loop behavior must be verified before motion is enabled. No continuous
rotation and no slip ring are intended.

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

## Mass, BOM, and unresolved procurement

The authoritative maximum is **5.000 kg for the complete operational station**,
including antenna, three axes and motors, radio, SBC, enclosure, tripod,
sensors, station power, and every operational cable and connector. Only the
external battery pack/BMS is excluded; weigh and report it separately as
carried mass, never as zero. All Powerpole mating halves and contacts, input
wires, positive master fuse/holder, three separately fused branch harnesses,
branch fuses/holders, wires/connectors, and any fitted strain relief count
toward the station cap. A carried charger also counts.

Use **4.500 kg as an engineering target**, preserving a preferred measured
0.500 kg reserve; this is not a compliance claim. The historical 3.130-3.200 kg
two-axis budget includes an unknown battery allowance and excludes radio and
tripod. It already includes both AZ/EL motors and the antenna. Subtract the
historical battery allowance only after it is recovered or measured; do not
use the raw 1.800-1.870 kg difference to 5 kg as available headroom. The
corrected total and cap margin remain **unknown** until the historical
allowance and current full inventory are reconciled and weighed.

The current inventory includes CM5, official CM5IO carrier and thermal
solution, **two replaceable LimeSDR Mini units and both mounts**, final
enclosure, PA/filter/shield hardware, auxiliary control/interface electronics,
the third POL motor and complete POL mechanics, full tripod, all three encoder
brackets, remote fixed-base compass/IMU and mount, stationary GPS receiver,
antenna and mount, sensor wiring, every RF branch and SMA connector, and all
remaining station wiring. These selected hardware masses are currently
unmeasured; none may be guessed or omitted. The 69 x 31.4 mm LimeSDR Mini
envelope is a planning reference only, not a fit or mass guarantee. The 12 V,
1 Ah example battery provides 12 Wh nominally / 6 W ideal for two hours before
losses and does not establish the two-hour operating target.

Recalculate EL/AZ loads using measured added POL mass, CG offsets and inertia,
including the motor, frame, wiring, and moving structures. The antenna-only
examples above are not complete-axis ratings; no motor capability or field
torque is claimed. Use `bom/polarization.csv` as an itemized procurement and
weighing checklist, not a vendor-quoted or released BOM.

## RF polarization is a separate function

Turning the antenna mechanically about boresight does **not** convert RHCP to
LHCP. Handedness selection is a separate RF function requiring a compatible
circular antenna with independent orthogonal feed ports on each band and
separately qualified band networks/switching. All RF coax interfaces are
standard-polarity 50-ohm SMA; RP-SMA, BNC, and N-type are excluded from the RF
coax chain. This does not change Baofeng audio/accessory jacks. The proposed
hybrid/switch topology and RF performance are unvalidated; select and test
parts for band, power, phase, loss, isolation, termination, and transition
behavior, with TX interlock. Keep this function electrically independent of
POL motor movement.

The optional `pol_part=10` cable tie-down STL,
`cad/polarization-power-strain-relief.stl`, was rendered with OpenSCAD 2021.01
and mesh-checked as one closed, oriented 3,132-triangle solid (11,769.7 mm3).
This validates mesh topology only, not panel fit, cable retention, print
strength, or Powerpole connector fit.

## Reproduction and acceptance

Render STL and DXF outputs with the local OpenSCAD CLI, selecting numeric
`pol_part` values 1 through 10 in `cad/polarization_station.scad`: frame,
rotor carrier, bearing retainer, limit cam, limit bracket, original BASE
saddle, motor-plate DXF, cheek-plate DXF, coax-interface DXF, and optional
generic power-harness strain-relief plate, respectively. `pol_part=0`
shows the assembly; it is a visualization, not a printable STL. Inspect the physical fit
of the 20 mm saddle, existing flange, actual pulleys/motor, bearings, cable,
stops, and NC switches. Test switch break-before-stop and full cable sweep
with motor power disconnected first; then perform supervised low-speed
bench tests with RF disconnected and independent emergency power isolation.
