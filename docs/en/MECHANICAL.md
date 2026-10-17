# Modular Portable Station — Original Mechanical Prototype

## FINAL: enclosure with real 22 mm plenums; supersedes following historical dimensions

The final enclosure in `cad\carrier_enclosure.scad` is **224x174 mm interior,
228x178x43.6 mm exterior**, with 2 mm lid and 0.7 mm external lettering.
The 180x130 mm PCB sits at corner **(24,24), z=8**: **22 mm clearance at each
edge**, an initial envelope for reported 20 mm connectors/cables; unlike the
previous design, it does not pretend 2 mm was sufficient. It retains 32 mm from
PCB to ceiling and confirmed 1.6 mm PCB/3.2 mm NPTH dimensions. Posts are now at
**(29,29), (199,29), (29,149), (199,149)**, exactly 170x120 mm center-to-center.
Verify real cable minimum bend radius; 22 mm is designed space, not testing of
every plug.

Removable blind panels remain for drilling to the actual assembly: front
openings x=20..60 and 168..208, z=15..37; side y=25..55 and 123..153.
These panels are not asserted to locate USB/JST/terminal centers without a
measured template. All cables have a plenum before the wall. The battery remains
**separate** on a fixed tray; final battery dimensions are still blocked and it
is not modeled arbitrarily inside the enclosure.

Current independent DXF tray: **2 mm aluminum, 240x196**, four M5 on 180x30
pattern and two M4 matching the ears; nominal mass 254 g before holes. Do not
thin the support or remove parking hardware to compensate. Final ASA enclosure:
base 149,957.5, lid 81,678.9, two 3,102.0 panels and two 2,502.0 panels mm³,
total ~242,844.5 mm³/**259.84 g solid ASA**. Smooth lid at this size ~81,095.6
mm³; connected relief adds 583.3 mm³/~0.624 g. Total BASE ASA ~**1.009 kg solid**.

Updated broad budget: **3.522–4.407 kg solid**, hypothetical 75%-material ASA
scenario **3.270–4.155 kg**, including 254 g tray and battery. The old
conditional BuildLight 2.679 kg, enclosure increase ~147.42 g, tray 254 g, and
150–220 g assembled carrier instead of 100 g yield **~3.130–3.200 kg**, BEFORE
pending buck/stop/cables. **The <=3 kg target is unmet in the current budget and
not physically demonstrated.** Figures 2.748/2.916 and 184x134/188x138 mm
enclosures in historical sections below are **SUPERSEDED**, not the current
assembly. Another design/physical-selection decision is needed to meet the
mass target; this extension solves wiring space, not compliance with <=3 kg.

The four final STL files were exported through staged files and passed the
unchanged validator; lid has 9,024 triangles and one connected component.
Final lid SHA-256:
`0C3E09D586A310A8FE5F26B071AE8EC72EA61FE250C590C94FEAFCA405B06B79`.
Liberation Sans Bold font is included; no platform substitution. Tray DXF and
CSG were updated. Tests check 44 mm additional space per dimension, relative
posts, headroom, meshes, and additional mass; physical fit remains pending.

### Actual 180x130 PCB carrier: current stationary modular enclosure

Hardware report records routed board **180x130 mm**, holes at
**(5,5), (175,5), (5,125), (175,125)** from PCB corner. **The old enclosure,
124x64 mm interior, does not fit and must not be bought/printed for this board.**
It is not replaced by a fictitious future smaller PCB.

`cad\carrier_enclosure.scad` models a new original enclosure:
188x138x43.6 mm exterior plus 2 mm lid, 184x134 interior, 2 mm walls/base,
PCB at z=8 (6 mm posts above 2 mm base), **32 mm above the provisional 1.6 mm
PCB**, plus 2 mm below the lid. PCB corner (4,4), case holes
(9,9), (179,9), (9,129), (179,129), with 170x120 mm spacing matching report.
Hardware report confirms **1.6 mm PCB and 3.2 mm M3 holes**; CAD was updated.
Verify Gerber/drill and fabricated PCB before assembly. PCB origin is upper-left
with positive coordinates; symmetric rectangular pattern matches; do not invert
labels/connectors when transferring into CAD. M3 through-bolts, washers, and
nuts; no ASA threads; do not put components over the posts.

Two removable panels for 40x22 mm front openings and two 30x22 mm side openings.
They are **blind covers**, not invented connector holes: drill/regenerate from
actual connectors and location, with clearance for plugs/coax/cable bend radius.
Hardware reports ESP ~10 mm and drivers/heatsinks 15–20 mm, within 32 mm
headroom; driver/power lower-left, GNSS/sensors right. This is reported
orientation, not inferred connector-hole positions. GNSS/IMU and two AS5600s
remain modular connections; physical AS5600s remain at their respective axes.
Transparent 32 mm envelope illustrates headroom, not routed components.
Enclosure and battery remain **stationary on the tray/tripod** or as an
independent module near rotor; protect cable and provide strain relief. Do not
load the large box onto the antenna/AZ flange.

`cad\carrier-metal-mount.dxf`: stationary 2 mm aluminum plate, 200x156, two M4
matching enclosure ears and four M5 for tripod/tray clamps on 140x30 mm pattern.
Through-fasteners, washers, nuts, insulating spacers; no fictitious fit inside
rotor. Cut/deburr and check support capacity; nominal plate ~168.5 g before
holes **is counted**. Do not use a bare tray as a handle or antenna support;
backing/reinforcement/actual clamp and wiring add to the reserve.

Four new selectors exported in `cad\carrier-stl`: `base`, `lid`, `port40`,
`port30` (print two of each panel). CSG in `cad\carrier-assembly.csg`,
script `cad\export-carrier.ps1`. Four CGAL STL files and two Node tests passed.
Total solid volume with four panels 170,138.6 mm³/~**182.05 g ASA**, replacing
old enclosure/lid 112.0 cm³/~113.04 g: increase **69.01 g**.
Current BASE ASA 0.862 -> **0.931 kg solid**; no fictitious PCB mass reduction.

Prior BuildLight 2.679 kg becomes nominally **2.748 kg**, 252 g reserve, if
entire increase is reserved and every remaining limit is met. With prior 75%
ASA scenario and increase also fully reserved: ~2.934 kg, only 66 g margin.
**The 100 g populated 180x130 PCB target remains unweighed**; bare nominal
1.6 mm FR4 alone is ~69 g at 1.85 g/cm³, before copper, ESP32, drivers,
connectors, and GNSS, and can substantially exceed 100 g. New enclosure/plate
narrows the target; weigh electronics and battery before claiming <=3 kg.
Candidate 21 mm motor remains incompatible with current base. No conditional
mass table constitutes mechanical/electrical approval or measurement.

**User-selected branding:** 180x130 carrier lid integrates raised
`BRICOHAMS` and `bricohams.org`, without inventing an official logo. Parameters
`brand_name`, `brand_url`, `brand_raise=0.7`,
`brand_font="Liberation Sans:style=Bold"`; `LiberationSans-Bold.ttf` is included
in portable OpenSCAD 2021.01. No reliance on system Arial substitution. With
another OpenSCAD, install/select that family or visually verify and rerender.
Text centered on two lines, 12/8 mm, away from screws/corners/ports; starts at
z=1.95 and ends at 2.7: 0.05 mm overlap with 2 mm lid makes a connected solid.
0.03 mm offset stabilizes contours for printing; this is not reverse engraving
or a floating plate. Print lid flat side on bed and lettering upward; does not
reduce 32 mm interior headroom or add RF metal.

Branded lid **52,398.9 mm³** vs. 51,815.6 smooth: delta 583.3 mm³,
~**0.624 g ASA** nominal. Real binary STL: 9,024 triangles, closed/oriented
edges, no degenerates; test checks text in CAD and increased rendered volume.
First ASCII output created degenerates and was rejected; final binary export
with stabilized contours passed. Four carrier STLs rerendered, CSG/plate DXF
regenerated. Prior unbranded enclosure mass needs +0.624 g; immaterial to
3 kg acceptance, for which no physical weighing or approval exists.
Exporter now writes `*.pending.stl`, validates, and only then replaces final STL,
so parallel tests cannot read an incomplete render. Validator retains
degenerate-triangle criterion and adds connected-component count: branded lid
is **one component**, not floating letters. Final rerender and eleven mechanical
tests passed. Final lid SHA-256:
`EC5806AA9FF4EB068FBC695D6CEEF794CD9DDE1DB68270D784114A5068320E34`.

The carrier manufacturer has not weighed a board: reserve ~100 g conservative
bare board and **150–220 g for assembled ESP/TMC/heatsinks/terminals**, plus
pending external buck/stop/cables. The previous 100 g populated-electronics
target is no longer defensible. Replacing it with 150–220 g adds 50–120 g:
conditional BuildLight ~**2.966–3.036 kg**, before pending additions and
resolving the incompatible 21 mm motor. Even favorable end leaves ~34 g margin;
high end exceeds 3 kg. **No ready candidate meets <=3 kg**; do not present a
provisional sum as acceptance.

Hardware requests >=30 mm **above the PCB**, now confirmed; 32 mm meets this
interpretation nominally for 20 mm components, not 30 mm clear above components.
Reported connector locations: module USB to right, >=68; JST I/O near x=157;
motors at edge y=120; DC near x=12/y=18 on left (PCB origin upper-left).
These are component locations, not enclosure-opening centers: panels remain
blind until plug/cable and mounted-board measurements. Keep reported 20 mm
clear for lateral connectors/cables; 2 mm old lateral margin **does not
provide 20 mm**, so USB/terminals facing wall require open panel or a local/
external enlargement. Do not claim wiring fits with lid closed before checking.

Reported commercial Pololu D24V22F5 buck, 17.8x17.8x8 mm, needs **separate,
insulated mounting** on fixed tray/enclosure, held by a verified-size bracket
and screws, not floating above PCB. No module holes are invented and it is not
integrated outside the enclosure limit without drawing. Final protected battery
dimensions and AS5600 breakout are not yet selected: fabrication/assembly
blockers. Earlier 16x16 sensor pattern remains provisional, not imposed by
carrier PCB.

## Current BASE: belt reduction, mass priority

By explicit user decision, transmission may change to pursue <=3 kg including
battery, excluding radio/tripod. **Current BASE: `cad\belt_station.scad`.**
`cad\station.scad` retains the prior planetary design intact as optional
**LEGACY**; do not add both BOMs or build both. Planetary sections below describe
LEGACY only. Retained: AZ ±180, EL 0..90, removable antenna, stationary radio,
AS5600, NC limits, metal UNC tripod interface, and unvalidated RF geometry.

BASE has two **GT2, 2 mm pitch, 20:100** stages, exactly 5:1 x 5:1 = **25:1**.
200 full steps x 16 microsteps x 25 retains **80,000 output steps/revolution**,
as communicated to controller. This does not imply actual 0.0045° resolution/
accuracy. All toothed pulleys are **purchased metal**, not ASA GT2 teeth with
unverified profile. CSG shows declared purchase envelopes, not manufacturable
pulley models or guaranteed SKU availability. Four continuous purchased GT2
belts, **126 teeth/252 mm, 6 mm wide**.

### Centers, tensioning, supports, and physical transmission

Pitch radii: 20T=6.3662 and 100T=31.8310 mm. Exact open-belt length:
`2 sqrt(C²−(R−r)²)+π(R+r)+2 asin((R−r)/C)(R−r)`.
Solved **C=60.56301755 mm**; envelopes do not overlap. 20T pulley contact:
**130.2718° / 7.237 teeth**. Do not assume torque capacity from this number;
consult belt manufacturer using speed/tension and motor curve.
Centers per reducer: motor x=-C, intermediate x=0, output x=+C, all y=0.
Two belt planes at z=15..21 and 28..34 (local coordinates).

6082 aluminum plates, **3 mm**, nominal 187.126x86; front z=0..3, rear
z=54..57. Cutting DXFs:
`cad\belt-front-plate.dxf`, `cad\belt-rear-plate.dxf`; AZ tray
`cad\belt-tray.dxf`. Plates are **not ASA STL**.
48 mm outside-diameter ASA cups support 608 (8x22x7) and 6000 (10x26x8),
two each per axis. Front 3..13, rear 44..54; bearings seat against metal
plate and outer cup lip. Align without force before tightening. Inner bearing
faces, ~40 mm apart, support steel shafts: **8x60 intermediate and 10x89 output**,
two of each, not printed motor shaft. Differential movement of cups bends shafts;
adjust both supports together and check coaxiality.

* Stage 1: pulleys z=14..26, including flanges/hubs.
* Stage 2: z=27..39. Hub1/hub2 gap **1 mm**.
* Rear cups start at 44: **5 mm** from hub2.
* Rear plate ends at 57; load flange begins at 60, 3 mm gap.
* Flange 60..78, magnet 81..93, sensor 95..98; shaft ends at 89.
* Purchased 100T pulleys: flange OD <=66.662, total axial width <=12, hub OD
  <=30. 20T pulleys: width <=12, hub OD <=18. **Measure actual drawing before
  purchase**; many commercial hubs are longer and will not fit without redesign.
* Motor shaft protrusion **>=26 mm from face** to reach first pulley; a short
  NEMA14 is not automatically suitable. 26 mm hole spacing and 35 mm face are
  provisional.
* Intermediate shaft joins first-stage 100T pulley to second-stage 20T pulley
  by metal key/collars or correctly sized pins. Output 100T pulley and flange
  join 10 mm steel via key/pin; no adhesive/ASA transmission. Pin/keyway holes
  weaken sections; machine and test.

**Real tension adjustment:** 3 mm horizontal slots in motor mount and both
intermediate supports, not a decorative idler. Output is fixed; moving
intermediate toward negative x increases C2. Move motor farther negative to
restore C1. +/-1.5 per part permits small pretension, not compensation for an
incorrect belt. Four M3 screws per cup and large washers; motor uses four M3.
Tighten after adjustment to belt manufacturer's maximum tension. Add M4
adjustment screws and locknuts on metal tabs or use a distance gauge; do not
use flexible ASA as tension reference. Excess tension loads bearings/shaft.
Actual hubs must keep screw heads/collars clear of belt plane.

AZ: reducer face 45 mm above base; motor z=11..45 remains clear. Four 36 mm
metal spacers support front plate over fixed tray z=6..9; motor is not suspended
from plastic. EL sits on 3 mm folded aluminum bracket with reinforcements/
rivets or screws, sharing M4 flange interface. EL shaft is 60 mm above support
base; 86 mm-high plates extend 17 mm above it. 38x38 window clears EL motor;
four M4 case fasteners. Cups/plates form structural load path; folded profile/
reinforcement requires real metal fabrication and stiffness test, not printing
its envelope.

AS5600 mounts to rear plate through two 20 mm metal spacers and printed bracket,
**not rotating with output**. Diametric 6x2 magnets on output shafts.
Radio/enclosures remain on fixed tripod tray (not rerendered in BASE view);
antenna/saddle/NC mounting reused. Specific cams, belt guards, actual wiring,
and checking heads/hubs/keys remain outstanding: **integration design only,
not assembly-tested or operationally ready**. CSG shows honest envelopes;
purchased metal parts are not exported as printable STL. Check AZ/EL sweeps,
sensor vs saddle, coax, supports, and complete battery before energizing.

### Backdrive, load, and transport

Belts are **reversible/backdrivable**; do not ascribe planetary self-locking or
an unpowered motor brake to them. Balance antenna and stow low/immobilized with a
**metal parking pin or independent strap to frame**, removed before motoring.
Power loss may drop EL: support/remove antenna before cutting power; keep people
clear below. Reduce holding current only after thermal/safety test. Retain
provisional 500 g load/CG <=30 mm and prior wind tests; do not transfer ASA
torque/efficiency to belt. Belt efficiency is unmeasured.

### Initial comparative mass and decision criterion (before 180x130 carrier)

BASE printing shares accessories but not the 34 heavy reducer parts. Four new
STLs (`base`, `cup608`, `cup6000`, `encoder_support`) exported to `cad\belt-stl`;
common parts remain in `cad\stl`. **Solid-equivalent ASA 0.862 kg**, vs LEGACY
2.521 kg. Bxx quantities in CSV replace Pxx/Mxx; shared groups B08..B10 detail
selectors, not additional components.

Mass budget after subsequent motor/battery/cable selection: metal motors
0.24–0.36, eight pulleys 0.16–0.24, belts 0.020–0.035, eight bearings
0.130–0.150, steel shafts 0.169, four plates+EL support+tray 0.680–0.780,
spacers/hardware 0.150–0.250, antenna/RF/coax 0.360–0.580, controller/battery
0.350–0.580 kg. Four 187x86x3 plates contribute up to 0.521 kg before holes;
folded support/tray completes reserve.

**Solid: 3.121–4.006 kg.** Hypothetical 75%-material ASA example (NOT 75%
infill or slicer result): **2.905–3.790 kg**. Favorable endpoint nominally
enters <=3 with only 95 g margin and no weigh-in: **target unproven**. Heavy
selection exceeds it. Acceptance requires weighing every group, actual slicer
report, and **complete assembled mass <=3.000 kg**, including battery but
excluding radio/tripod. Do not thin bearing seats, teeth, or shafts to disguise
it. If purchases exceed budget, stop and review machined metal structure or
architecture before fabrication; do not publish a <=3 kg station claim.

BASE validation: four CGAL STL without warnings, closed/oriented edges; plate
DXFs and assembly CSG. Node test confirms centers, exact length, ratio, wrap,
stack, and meshes. Two variants: six Node tests passed. No strength analysis,
supplier drawing, full collision sweep, or physical test was performed.
`cad\export-belt.ps1`, `tests\mechanical-belt.test.cjs`,
`tests\mechanical-belt-mass.cjs` reproduce export/audit.

### Initial BuildLight: candidate selection (superseded by carrier update above)

Document review of manufacturer products (October 10, 2026), with no purchase,
weighing, or additional structural modifications:

* [Pololu 1207 / SOYO SY35ST26-0284A](https://www.pololu.com/product/1207):
  **130 g published per motor**, NEMA14 35x35x26 mm, 200 steps/rev, 280 mA/phase,
  7.4 V nominal coil, holding torque 650 g·cm ~=0.0637 Nm.
  **D5 shaft protrudes 21 mm: NOT compatible with current BASE mount requiring
  26 mm.** Do not approve or claim fit. A later revision might orient 20T pulley
  hub toward motor, with commercial drawing and new axial check, or specify
  metal coupling/support; do not extend shaft with ASA. Current and dynamic
  curve require testing; holding torque does not authorize 500 g.
* [TalentCell YB1203000-USB](https://talentcell.com/lithium-ion-battery/12v/yb1203000-usb.html):
  manufacturer publishes **“About 190g”**, 11.1 V/3000 mAh ~=33.3 Wh nominal,
  output **9–12.6 V / 3 A maximum** and 5 V/2 A maximum. 190 g is not guaranteed:
  weigh unit. Keep away from rain/moisture, do not open pack, use correct charger.
  Compatibility with protection/carrier/regulator pending PCB review; do not
  power motors from 5 V output or assume regulated 12 V. Reserve margin for
  undervoltage and simultaneous loads.

Reject lightweight 1S battery with improvised boost: losses/current and protection
may fail. Do not reduce 3 mm thickness, steel supports, bearings, or mechanical
parking retention to lower the number.

The following is a **conditional BuildLight purchase/fabrication plan**: only
motor and battery have published product masses; others are **group mass caps**,
not supplier figures. Accept a group only after drawing/selection/weighing at or
below its cap. This is not a closed BOM or <=3 kg demonstration.

| Group | Cap/candidate kg | Basis and condition |
|---|---:|---|
| All ASA parts/enclosures | 0.460 | Slicer/weigh target; solid is 0.862; infill does not guarantee it |
| Two Pololu 1207 motors | 0.260 | 130 g each published; 21 mm mount currently incompatible |
| Eight metal pulleys | 0.160 | Purchase cap; actual drawing/mass pending |
| Four belts | 0.020 | Purchase cap; verifiable GT2 specification pending |
| Eight bearings | 0.130 | Purchase cap; retain 4x608/4x6000 |
| Steel shafts 8x60 and 10x89 | 0.169 | Geometric calculation; supports unchanged |
| 3 mm plates, EL support, and tray | 0.680 | Geometry/density and reserve; no thinning |
| Spacers, screws, keys, U-bolts, parking | 0.150 | Group cap; do not omit brake/parking or hardware |
| Antennas, fiber, coax, RF networks | 0.360 | Aluminum group cap; gain/mass not validated |
| PCB, drivers, GNSS, wires, fuse, protection | 0.100 | PCB hardware goal pending; includes connectors |
| TalentCell YB1203000-USB | 0.190 | Manufacturer says “about”; weigh it |
| **Conditional subtotal** | **2.679** | Not measured mass or approved assembly |
| Reserve to 3.000 | **0.321** | Extra wires, deviations, motor adaptation, enclosure enlargement |

**<=3 kg priority is not physically met**: ASA 0.460 kg requires 53.4% of
solid volume; only a slicer report with correct walls/reinforcements can show
whether it is achievable without weakening. Prior 75% material estimate was
0.646 kg. If slicer requires 0.646, subtotal rises to 2.865 and reserve falls
to 0.135. The 21 mm motor needs mechanical revision; PCB footprint may exceed
124x64 interior and require a new enclosure, consuming reserve. Do not hide
dependencies to present a fictitiously approved option.

Illustrative autonomy for 33.3 Wh pack: assuming 80% usable energy (26.6 Wh),
measured total consumption later of 10/15/20 W would give 2.66/1.77/1.33 h.
Not tested runtime and excludes radio. Actual active time depends on motor
current, drivers, Wi-Fi/GNSS, braking, and losses; do not promise a full day.
Consider lower-Wh alternative only after electrical/safety requirements and
published mass/current limits; do not omit battery from budget.

BuildLight acceptance: compatible drawings, assembly/load test, slicer <= cap,
each group weighed, and total <=3.000 kg **including PCB and battery**. If a
gate fails, revisit selection/design; do not relabel this conditional budget as
ready product. Cited motors/battery have not been purchased.

Original parametric design, not reconstruction of a commercial product or copy
of third-party files/screenshot. **Prototype not assembled, load-tested, or RF
validated.** Correct STL does not prove mechanism, strength, collision-free
motion, or good SWR. User selected **CERN-OHL-S-2.0 for original hardware** and
**MIT for original software**, scoped in `NOTICE.md`/`LICENSES`. External
references retain their own licences; unknown-licence sources are not
redistributed here. This local delivery does not imply remote publication.
For authorship/acknowledgements see project AUTHORS, ACKNOWLEDGEMENTS, and
DISCLAIMER created by coordinator for Anatol EA5KAO, Diego EA5JEF, and Pedro
Roca Molina. Educational initiative [Bricohams](https://bricohams.org) does not
imply endorsement of manufacturers or cited projects. Minors/adolescents
require adult supervision; no transmission without applicable authorization/
licence. Before flashing, disconnect motors/RF, use protected supply, and verify
pinout; flashing prototype does not certify approved hardware.
Indicative target: **<=3 kg without tripod or radio**; not measured mass.
Complete geometry shows envelopes and main parts. Screws, nuts, wiring, braids,
limit cams, hybrids, and metal lining are installed per this guide; they are
not printable STL.

## Files and standalone use

* `cad\station.scad`: open in OpenSCAD; `part="assembly"` displays assembly.
* `cad\parameters.scad`: parameters in mm/degrees, ASA, clearances, frequencies.
* `cad\gears.scad`: calculated real involutes, not decorative teeth.
* `cad\mechanical.scad`: reducers, supports, and interfaces.
* `cad\antenna.scad`: distinct antennas for 145 and 435 MHz.
* `cad\export.ps1`: CGAL render of each part and STL validation.
* `tests\mechanical-math.cjs`: calculations/flank sampling; no Node packages.
* `tests\mechanical-stl.cjs`: finite triangles, closed oriented edges, no
  degenerate triangles, positive oriented volume.
* `bom\mechanical.csv`: base quantities, materials, indicative budget.

Export selectors: `sun1`, `sun2`, `planet`, `ring`, `carrier1`, `carrier2`,
`motor_plate`, `intermediate_plate`, `output_plate`, `keeper608`, `keeper6000`,
`spacer15`, `spacer9`, `spacer38`, `spacer6` (auxiliary), `tripod_base`,
`output_flange`, `elevation_bracket`, `saddle20`, `saddle25`, `saddle32`,
`flat_adapter`, `limit_bracket`, `magnet_holder`, `sensor_bracket`,
`radio_cradle`, `enclosure`, `enclosure_lid`, `diplexor_box`, `diplexor_lid`,
`antenna_hub`, `band_bridge`, `arm_socket`, `coupon`.
`gearbox`, `antenna145`, `antenna435`, and `assembly` are assembly views:
do not print their union as one part. `assembly.csg` preserves assembly. No
assembly STL is exported that fuses moving parts into a solid.

Official **OpenSCAD 2021.01 Windows x64 ZIP** was downloaded from
<https://files.openscad.org/OpenSCAD-2021.01-x86-64.zip>, isolated under
`cad\tools`, not installed globally. To reproduce:

```powershell
Set-Location 'C:\Users\anatol.lopez\Documents\PortableSatStation'
& '.\cad\export.ps1' -Node 'LOCAL_PATH\node.exe'
& 'LOCAL_PATH\node.exe' '.\tests\mechanical-math.cjs'
```

Another official executable may be supplied with `-OpenSCAD`. Individual logs
are in `cad\stl\*.render.log`. Node used during creation is in session's isolated
tools directory; it is not a CAD dependency and is not installed system-wide.

## Reducer: two planetary stages per axis

Initial choice is **spur**, not double helical: avoids manufactured axial force,
eases contact measurement, reduces time/cost. Herringbone may reduce net axial
thrust but **does not eliminate backlash**, flex, or printing error. No
unverified helix is offered as a supposedly ready option.

Module 1.5, pressure angle 20°, sun **18**, planet **27**, internal ring **72**,
three planets at 120°. Pitch radii 13.5/20.25/54 mm; planet centers at
**33.75 mm**. Ring OD **124 mm** for 6.125 mm wall behind roots, deliberately
larger than ~114 mm thin-wall envelope. Gear useful width 12 mm; physical ring
17 mm.

* `R=S+2P=72`, valid internal and external meshing.
* `(S+R)/3=30`, integer assembly condition for three planets.
* Fixed ring: `i=1+R/S=5`; two stages yield **25:1**.
* Theoretical minimum without profile correction `ceil(2/sin²20°)=18`;
  no 12-tooth sun without profile shift. No hidden profile shift.
* External addendum `rp+m`, root `rp-m-0.25m`; ring addendum `rp-m`,
  root `rp+m+0.25m`. Nominal radial clearance **0.375 mm**.
* Reduce each wheel thickness by `backlash/2=0.125 mm` at pitch circle:
  nominal total tangential allowance **0.25 mm per pair**, not guaranteed
  output backlash. Test 0.20/0.25/0.30 with coupons. ASA wear increases play.
* Ring uses **internal involute**, widening tooth toward outer root. Fixed-ring
  orientation includes 2.5° phase for teeth only; tie holes remain at 30+60k°.
  Sun phase 0°; planets `center angle+180−180/27`. Do not arbitrarily change phases.

### Axial stack per reducer

Local coordinates refer to motor face `z=0`. Spacers/supports maintain actual
gaps; do not stack STLs in table order without measurement.

| Part | z interval, mm | Detail |
|---|---:|---|
| Provisional motor | -34..0 | 35 mm face; final motor drawing governs |
| Motor plate | 0..8 | provisional 26 pitch, M3, 23 center opening |
| Sun1 hub / teeth1 | 4..12 / 12..24 | motor shaft 5, radial M3 insert/screw |
| Fixed ring1 | 9..26 | six M3 rods |
| Planets1 / shoulders | 12..24 / 10..33 | OD6 ID4 L12 metal bushings |
| Carrier1 / hub | 26..32 / 32..40 | 2 mm from tooth faces |
| Intermediate shaft8 | 26..62 | steel; pins at z36 and 58 |
| 608 plate / bearing | 41..50 / 42..49 | retainer 50..53; axial play to tune |
| Sun2 hub / teeth2 | 54..62 / 62..74 | 1 mm free from retainer |
| Fixed ring2 | 59..76 | spacers9 from z50 |
| Planets2 / shoulders | 62..74 / 60..83 | washers/nuts behind carrier |
| Carrier2 / hub | 76..82 / 82..90 | steel output shaft10, pin z86 |
| Output support1 | plate91..101, 6000:92..100 | retainer 101..104 |
| Output support2 | plate110..120, 6000:111..119 | retainer120..123; centers 19 apart |
| Shaft10 | 76..153 | L77, pins z86/136/149 |
| Load flange | 124..142 | disk124..130, hub130..142 |
| Magnet carrier | 145..157 | fits last 8 mm of shaft; pin z149 |
| PCB support | 159..162 | nominal magnet gap2 mm; adjust to actual PCB |

Two **6000 10x26x8** bearings at output per axis; **608 8x22x7** intermediate.
Do not call a shaft-10 bearing a 608. Bearings support outer ring on 1 mm step.
Retainers have center opening ID+1; use shims only on outer ring so inner ring
does not bind. Do not rely on press-fit in ASA. Twelve planets use **bronze
6x4x12** bushings and steel4 shoulders; no fictitious impossible-diameter
commercial bearing is modeled.

Carrier1 **physically drives sun2** via shaft8 with two M3 pins. Carrier2 and
flange connect to shaft10 with metal pins. Drill shafts with perpendicular
template, deburr and fatigue-test: holes reduce section and initiate cracks.
M3 through-bolts with locknuts, not printed threads or adhesive as sole drive.
Do not transmit significant load only with a set screw.

### Assembly and adjustment

1. Verify selected NEMA14 drawing: 35 mm is nominal class, not certified body
   35, pitch26, length34, shaft5, or torque. Adjust CAD before printing.
2. Print coupon: holes 8.0/8.1/8.2/8.3. Test actual steel; initial diametral
   `fit` 0.25. Also test seats22/26, inserts, rod4, and M4.
3. Clean roots, burrs, and bridges. Assemble one sun/planet/ring pair.
   Check full smooth hand rotation, mark contact with ink. Keep ASA-compatible
   lubricant away from RF connectors.
4. Install sun1 and motor. Assemble 3 planets in specified orientation, bushings,
   shoulders, washers, carrier1. Set measured axial play **0.2–0.4 mm**.
   Shoulders clamp carrier, not planets; commercial shoulder length may require
   washers/cutting; do not assume ordinary screw fit.
5. Install shaft8, 608 plate, spacers15, bearing, retainer. Carrier/hub ends at
   40; plate begins at 41; hub must not contact plate.
6. Install sun2 from z54 and pin at z58; ring2 from z59, second planet set,
   carrier2.
7. Install spacers15, support1, spacers9, support2. Align both 6000s with
   temporary shaft before tightening rods; do not force them with screws.
8. Install shaft10, flange/pin z136, magnet carrier/pin z149. Mount AS5600
   coaxially on selected PCB. 16x16 pattern is provisional. Support foot on
   fixed second plate at z120, two M3 at x=-55/y=+/-10, tower x=-66..-62.
   Attach to **stationary axis support**, not magnet carrier; no antenna load
   passes through PCB/magnet. Check real PCB thickness/solder joints: printed
   plate is not electronics. Sensor must NOT rotate with flange/saddle/EL
   support over AZ; attach foot only to that axis' own housing.
9. Repeat for EL. EL motor face bolts to support cheek using six M3; 38x38
   opening clears provisional 35 mm motor. Relieve wires at entry.
10. AZ base z0..12; spacers38 raise reducer face to 50, leaving motor z16..50.
    Without lift the motor collides with base/tripod. AZ rods ~180, EL ~130;
    cut only after measured stack.
11. AZ flange z174..192 supports EL. EL saddle mounts from local z130 of EL
    axis, 22 mm encoder gap, boom offset laterally 35 and height24. Sensor is
    in free plane at z159 over plastic (saddle ends154); even boom32 stays
    outside sensor bridge (plate ends x12/y+/-12) through EL0..90. EL shaft is
    84 mm above base plate: reducer lower edge clears base and AZ sensor bridge.
    Bolt four positions +/-15.556 mm (31.112 square); physically check screw and
    sensor clearance.
12. Install four NC switches, adjustable metal cams, and independent mechanical
    stops. Bracket pattern18 mm provisional; measure switch. Fasten to plates/
    base, not adhesive. CAD exports brackets but no fictitious universal cam:
    make cam for actual switch and braking margin. Measure actuation before
    **AZ +/-180 and EL 0/90**; begin with software limits +/-170 and 5..85.
    Never allow continuous AZ rotation: coax/cables wind up.

## Interfaces, portability, and radio

Complete antenna detaches using four M4 screws at flange/saddle; disconnect
hybrid coax before lifting. RF booms are 20 mm fiberglass with selected
structural adapter 20/25/32. Saddles use two **metal M5 U-bolts** at x +/-22,
legs y=35+/-(diameter/2+5), leg spacing 30/35/42 mm. Select actual U-bolt with
that spacing and >=45 mm usable length, metal spreader plate, large washers,
and locknuts; do not crush tube. For flat face use `flat_adapter`, common M4
and four M5 on 54x36, all metal through-fastened. Do not print load-bearing
threaded clamps.

Tripod: captured metal **1/4-20 UNC nut** (initial AF11.1, height5.6),
accessible by removing base, plus commercial metal **3/8-16 to 1/4-20 adapter**.
No printed UNC threads. Check screw length: no bottoming; distribute pressure,
add metal nut retainer and tripod safety tether. Base does not certify tripod
stability/head or lateral capacity. In wind/uneven ground secure legs/ballast
and keep people clear below.

RT3S remains on **fixed base/tripod tray**, not AZ flange/antenna.
Initial envelope 61x39x131 mm plus 2 mm clearance per side is **provisional;
measure user's radio**, including clips, PTT button, connectors, and battery.
Cradle does not validate weatherproofing or fit; hand-test first, two straps
through slots plus third safety tether. Do not block cooling, speaker, controls.
Radio removable without removing antenna.

Enclosures shown beside base require a **fixed metal tray** on tripod; they are
not intended to hang in air or from antenna. Independent diplexer box
80x70x35 and removable lid with M3. Change dimensions/openings for selected
diplexer/connectors. ASA does **not shield RF**: line inside walls/base
74x64x32 and lid with 0.3 mm aluminum sheet, conductive joints, metal-metal
fasteners/contact points, and RF grounding per equipment. Avoid burrs/shorts
with insulating spacers. No EMC, weatherproofing, or plastic-paint shielding
claim. Electronics enclosure 130x70x45 with lid, cable glands, drip loops; do
not energize in rain.

Optional envelope reference: public `DuplexorSpaceQuad` project,
commit `f5c7dc375ed7b9882f52bd7757deaf44cd422b81`, publishes SMA PCB 37x23 mm,
box 45.2x27.6x14.1 mm (Amphenol 132289, two M2x10), or BNC PCB 55.5x33 mm,
box 59.9x37.6x23.5 mm (Amphenol B6252HB-NPP3G-50, two M2x12). Published values,
**not measurements of our unit**. Both nominally fit within our 74x64x32
compartment, but do not prove space for three connectors, plugs, nuts, coax,
or bend radius. Generic 10 mm CAD openings are **not SMA/BNC templates**:
modify after measuring actual connectors or route cable to gland.

That project estimates footprint connector dimensions: SMA tab 9.6x1.9,
axis PCB+0.4, 6.8 mm opening; BNC body 14.8 above PCB, axis PCB+7.5,
14.9 mm opening. Verify with caliper before drilling/fastening; do not load
board using approximate connectors. Its 2/2/1.6 mm walls/base/roof and 0.15
tolerance do not replace ASA calibration here. It is a **three-port diplexer**,
not quadrature hybrid; crossed dipoles still need two separate 90° networks.
Ideal simulations and 5–10 W indication for 0805 do not certify actual power,
loss, compatibility, or temperature. Its CAD files/circuit are not reused here.

## Original antenna: two crossed arrays with reflector

Do not scale a 449 MHz design and claim dual-band performance. Each band has
two orthogonal dipoles and two orthogonal reflectors, with its own initial
geometry calculated as:

```text
lambda_mm = 299792.458 / f_MHz
driven_tip_to_tip = lambda_mm / 2 * 0.92
reflector_tip_to_tip = driven_tip_to_tip * 1.05
separation = 0.225 * lambda_mm
```

| Band | λ mm | Driven dipole end-to-end | Reflector end-to-end | Plane spacing |
|---|---:|---:|---:|---:|
| 145 MHz | 2067.53 | 951.07 | 998.62 | 465.20 |
| 435 MHz | 689.18 | 317.02 | 332.87 | 155.07 |

These dimensions are **starting estimates**, not simulated/measured gain,
pattern, SWR, polarization, or matching. Effects of hinges, braids, booms,
reflector, box/radio, and **VHF/UHF mutual coupling** are unvalidated.
Illustrative 80 mm lateral spacing between booms is not verified RF separation.
Mechanical balance by boom displacement does not certify RF pattern.
Printed bridge with three 20 mm holes joins both RF booms and central 175 mm
structural boom. M4 through-bolts, large washers, metal collars; do not rely on
ASA threads. Bridge is 50 mm from longitudinal balance plane to avoid saddle
section; both arrays' centers align longitudinally, but differing mass requires
actual balance. Diameters 25/32 are structural boom/saddle alternatives; RF
booms and bridge remain 20 mm; use metal/dielectric adapter sleeve when changing
structure.

### Cutting, hinges, and transportable sections

Provisional rod diameter 4 mm. Central 24 mm gap is included in end-to-end
length: each geometric arm is `L/2-12`, ~463.53 mm driven VHF and 487.31 mm
reflector. M4 hinge at radius36: fixed conductive stub r12..28 (**16 mm**);
distal conductive arm from r46; 18 mm hinge gap bridged with **flexible copper
braid**. Actual electrical length changes formula: make all braids identical
and tune on VNA; ASA gap is not conductor. Steel M4 pivot and M3 cross-pin at
radius42 positively lock deployed. M3 screw at r54 retains rod with inserts/
metal sleeve, not ASA thread. Do not use friction as sole lock.

| Metal part | Quantity | Nominal geometric length, mm | Suggested initial oversize cut |
|---|---:|---:|---:|
| Stubs r12..28, both bands | 16 | 16 | 16, do not trim for tuning |
| VHF distal driven | 4 arms, each two segments | 429.53 = 214.77+214.77 | 2x220 per arm |
| VHF distal reflector | 4 arms, each two segments | 453.31 = 226.65+226.65 | 2x232 per arm |
| UHF distal driven | 4 | 112.51 | 118 each |
| UHF distal reflector | 4 | 120.44 | 126 each |
| VHF joint sleeve | 8 | 50, OD8 ID4 | Fit ID to actual metal |
| Dielectric VHF boom | 2 segments | ~245 each | 465.20 plane-to-plane assembled |
| Dielectric UHF boom | 1 | ~180 | 155.07 plane-to-plane |

**Conductive** brass/aluminum sleeves: **butt joint** (do not subtract 50 from
length), 25 insertion per side, two positive 2 mm perpendicular metal pins/
screws, clean aluminum and compatible anti-oxidation compound. Do not drill
4 mm rod for M3 without strength review. Small pins for RF sleeves differ from
M3 reducer shaft pins. Sleeve position in view is illustrative envelope; place
at actual joint between halves. Remove outer sections and split VHF boom; no
metal/boom section exceeds 450 mm. Assemble with length stops, orientation marks,
anti-rotation, and lock; a loose telescoping joint does not preserve resonance
or continuity. Fold hinges and tie arms for transport; `antenna_arm_angle=90`
view is kinematic illustration, not validation of all braid/sleeve interference.

Reflector elements must be electrically continuous: join opposing halves using
**metal bridges around the boom**, outside the crossing; maintain different
heights for crossing axes. Do not bridge the driven dipole terminals together
or to the boom. Arms and reflector detach independently at hubs/hinges; document
sequence and retain locking hardware.

A **matched 50 Ω feed** does not come from printing a hub. Fit per-band matching/
balun for each dipole and an external 90° hybrid with equal-length leads for the
chosen polarization; reverse phase for opposite circular handedness only after
verification. Use two **separate** networks, then an actual 145/435-compatible
diplexer rated for power/loss. Do not parallel two dipoles expecting 50 Ω or
attribute 50 Ω to this geometry. RF metal only, no printed wires. Tune at low
power on VNA, each band separately first, then combined on actual station.
Trim symmetrically in small increments. Observe licence and RF-exposure rules;
keep people away from rods, energized antenna, and moving parts.

Component reference: current manufacturer QCN-3+ datasheet states 220–470 MHz:
435 is in range, **145 is outside**. Do not treat it as dual-band hybrid or
extrapolate to unconfirmed `QCN-3` reference without suffix. No CMX/Anaren model
selected without verifiable datasheet.

External references do not replace tests of this station: LibreSat states its
v1.0 was not built/measured as a system and uses NEMA17/cycloidal 25:1, not our
NEMA14/planetary. Its load, wind, and efficiency assumptions are not transferable
ratings. Official maintained LibreDMR/OpenGD77 guide confirms RT3S satellite
screen with TX/RX Doppler, azimuth/elevation, manual location/UTC, and
Keplerian data from CPS; it does not demonstrate CAT or full duplex. Our cradle
still requires physical measurement.

## Load, torque, wind, and mass: targets, not certified capacity

Initial antenna target **maximum 500 g**, CG **<=30 mm** from EL axis, measured
with complete antenna/coax and booms adjusted. Gravity torque:
`0.5×9.81×0.03 = 0.147 Nm`. Illustration places boom near center, but physical
balance is required; reduce moment by moving saddle, moderate counterweight, or
accessories off antenna. Entire EL reducer mass adds AZ inertia. Do not raise
heavy antenna merely because motor has holding torque.

Example, **not a sold motor specification**: assumed NEMA14 dynamic torque
0.08 Nm, efficiency 0.65 per stage: `0.08×25×0.65²=0.845 Nm` theoretical
output. Check actual curve vs speed/current, losses, temperature, ASA stiffness.
Holding torque is not assumed to be dynamic torque. Until tested, limit demand
to **0.5 Nm per axis** with margin; this is not a tested mechanism or tooth/pin
rating.

Conservative wind example: density 1.225 kg/m³, Cd 1.3, equivalent area 0.12 m²,
arm 0.15 m, wind 8 m/s:
`T = 0.5*rho*Cd*A*v²*arm = 0.917 Nm`, plus gravity 0.147 = **1.064 Nm**:
**exceeds** both 0.5 cap and 0.845 example. Do not treat gust as allowable.
At 5 m/s: 0.358+0.147 ~=0.505 Nm, already marginal. Initially test indoors/
calm; fold/disassemble as wind rises; tripod/cables add torque. Do not guarantee
use at 5 m/s or 3 kg. Never leave active unattended.

CSV budgets are planning ranges **per complete line**, not shop prices or quotes.
Pxx has no separate cost because filament is counted in M24. Do not double-count
alternative saddles/flat adapter or electronics in another BOM. Plastic mass is
estimated from solid STL volume and ASA density ~1.07 g/cm³; infill changes
result, metal/reinforcement/coax increase mass. Weigh each assembled part; if
over 3 kg, target has failed.

### Validation performed, October 10, 2026

* OpenSCAD 2021.01 rendered **34 individual STL selectors** with CGAL, no
  ERROR/WARNING in 34 logs; assembly generated as CSG.
* All 34 STLs passed closed consistently oriented edges, non-degenerate
  triangles, and positive volume. This is not physical contact/collision
  certification or exhaustive self-intersection analysis.
* Node 22.16 validated 25:1 ratio, closure30, minimum18 teeth, radial clearances,
  and 121 positions of one sun-tooth revolution: sampled planet contour does
  not intrude into sun or ring material. One planet set is symmetric equivalent.
  Ideal spur contact ratio: external 1.580 and internal 1.944.
  Also checked motor/base, EL shaft/base, and encoder bridge vs boom32 in allowed
  quadrant. Not a full assembly sweep.
* Nominal inventory **131 printed parts**, excluding alternative flat adapter.
  Optimized solid-equivalent volume: **2.521 kg ASA** at 1.07 g/cm³.
  **Printing all parts solid exceeds 3 kg after adding metal, motors, coax.**
  Infill/reinforcement and actual mass require review before claiming light
  assembly; infill mass not calculated.
* Mechanical/RF CSV planning range: **€248–671**, not a quote; excludes radio/
  tripod and controller electronics from separate BOM.

Nothing has been printed, assembled, wind/torque/mass tested, or RF matched.
External roots use a discretized radial transition to base circle, not a
tool-generated trochoid; active flanks are real involutes. Do not assign teeth
an ISO/AGMA fatigue rating.

### Bounded optimization and mass budget

Lower fields in base were hollowed while keeping 3 mm top skin, perimeter,
central nut boss, and six 14 mm ribs toward rods. Only inner lid faces were
lightened while retaining 1.6 mm roof, edges, and central rib. Involutes/roots,
carriers, shafts, bearing seats, EL cheek, and motor fasteners were untouched.
These ribs are retained geometry, **not calculated/tested strength**; verify
base after lightening.

| STL | Previous volume, mm³ | New volume, mm³ |
|---|---:|---:|
| tripod_base | 233270.3 | 130922.3 |
| enclosure_lid | 27191.2 | 20331.2 |
| diplexor_lid | 16691.2 | 13331.2 |

Nominal solid ASA saving **120.45 g**, plastic assembly 2.641 -> 2.521 kg.
Three STLs rerendered with CGAL and checked; all 34 final meshes revalidated
by inventory. Runner `tests\mechanical.test.cjs`: three validations passed
(math, inventory, optimization/mass), including two optimization unit tests.
`export.ps1 -Only tripod_base,enclosure_lid,diplexor_lid` regenerates subset
without skipping per-STL validation.

Solid gear+carrier subset weighs nominal 0.579 kg; remainder 1.942 kg.
**Sensitivity example**, NOT slicer result: retaining 100% gears/carriers and
60% of remaining solid volume gives 1.744 kg ASA. This 60% is a hypothetical
global material fraction, **not 60% infill**: walls/ribs/skins strongly affect
result. Do not guarantee mass or reduce load-bearing supports for a target.
Use actual slicer report including supports/brim.

| Additional group | Planning mass, kg |
|---|---:|
| Two subsequently selected NEMA14 motors | 0.24–0.40 |
| Two 608 and four 6000 bearings | 0.09–0.12 |
| Steel shafts 8x36 and 10x77, two each | 0.1234 nominal geometry |
| 12 M3 rods, six 180 and six 130 | 0.1032 nominal geometry |
| 12 steel4 shoulders, without heads/nuts | 0.0272 nominal geometry |
| Bushings/pins/fasteners/U-bolts/adapter | 0.12–0.22 |
| RF rods and **aluminum** sleeves, fiber booms | 0.25–0.40 |
| Coax/90° networks/diplexer/liner | 0.18–0.30 |
| Controller/drivers/wiring | 0.08–0.15 |
| Portable power/battery | 0.25–0.45 |
| Subtotal without ASA, radio, or tripod | **1.464–2.294** |

Actual motor/bearing/radio/battery need datasheet/weighing. Steel values use
7.85 g/cm³; drilled holes and heads are excluded and reserved under fasteners.
Copper/brass instead of aluminum can significantly increase RF mass.
Tray/reinforcement/belts can add reserve; ranges are not invented vendor weights.

Even hypothetical 1.744 kg print scenario totals **3.208–4.038 kg**; solid gives
**3.985–4.815 kg**. **<=3 kg target NOT achieved or demonstrated by this robust
124 mm design**, with power included. Do not call it a 3 kg station. Pursuit
requires a new physical decision (machined/optimized metal plates, external
power not carried, smaller architecture, or tested structural revision); do not
speculatively thin teeth/supports. Weigh complete antennas too: 500 g target
may be exceeded by braids/coax/hardware.

### Mechanical integration status

Torque path and motor/shaft/bearing dimensions are defined and rendered.
NEMA14 **26 mm pitch is provisional** and shaft5 accepted only after purchased
motor drawing. No universal NEMA14 fit claim. Full CSG is not a verified final
assembly: specific cams/stops, heads/nuts/washers, final diplexer/cable mounts,
and their motion envelopes are missing. Coaxial alignment, pins, axial play,
real PCB/wiring require bench assembly. Dimension tests are explicit partial
checks, **not proof of no collisions**. Final classification: reproducible
modular CAD prototype, not operational station or assembly-tested.

## ASA printing, failures, and acceptance

Orient gears with axis Z, 0.15–0.20 mm layers, >=5 perimeters, teeth/hubs 100%
local infill; large parts 30–45% and ribs with >=5 perimeters initially. Do not
reduce ring perimeters near screws. Flat plates on bed; brim if needed. EL
support/hinges are flex-loaded: consider printing on edge or metal reinforcement
and test anisotropy. Ream holes only; do not file involutes to hide misalignment.
Do not heat bearings for assembly. Tune tolerances to actual material/lot/
printer, not a global scale.

ASA produces emissions: use enclosure and extraction/ventilation appropriate
to manufacturer; avoid inhalation and occupied living spaces. Do not promise
that a sealed enclosure without extraction protects. Hot bed/hotend; gloves
for metal handling and eye protection for drilling/cutting. ASA withstands
weather better than PLA but can creep in sun/load and is not certified for
thermal stability.

Reject: root cracks, nuts crushing ASA, bent pins, oval bushings, retainer
rubbing shaft, locked planets, enlarged hinge slots, missing pin, taut coax,
increasing backlash, or loose magnet. Measure output backlash both directions
with dial indicator; do not infer it from motor steps. Confirm AS5600 on output
shaft during lost steps. An NC limit open must stop; test broken wire and
emergency behavior first with motor disconnected. Mechanical stops do not
replace electrical cutoff.

Pending field acceptance: complete manual cycle, collision/cable check at
AZ +/-180 and EL 0..90, 100 unloaded cycles, 100 with increasing load,
torque/current/temperature/backlash measurements, power failure, NC limits,
tripod stability, antenna/magnet retention, actual mass, SWR/pattern/RF exposure,
and continuity after repeated folding. These tests have not been performed.
