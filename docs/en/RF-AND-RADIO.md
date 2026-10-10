# RF, polarization, and RT-3S: verifiable architecture and limits

Date: 2026-10-10. Sources/versions in [SOURCES.md](SOURCES.md); PDF analysis
in [REFERENCE-ANALYSIS.md](REFERENCE-ANALYSIS.md). Nominal target: 145/435 MHz;
this is not certification of the complete assembly.

## Three different concepts

| Item | Function | What it does NOT demonstrate |
|---|---|---|
| **Diplexer**, three ports | One common 50-ohm port and two band branches: VHF and UHF; low-pass/high-pass filters | Does not generate circular polarization or add a second receiver to the radio |
| **Full-duplex operation** | Reception during transmission, with sufficient radio(s) and isolation | Two programmed frequencies or dual-watch are not enough |
| **90-degree hybrid**, four electrical ports | Feeds two orthogonal dipoles/planes with appropriate amplitude and phase within its band; isolated fourth port is terminated | Does not separate 145/435 MHz or provide a good axial ratio out of band |

The repository is named DuplexorSpaceQuad, but its README electrically
describes a **diplexer**. Do not infer “full duplex” from its name.

## Proposed topology, without assuming circular polarization or simultaneous RX

```text
RT-3S: single RF port
           |
    optional 145/435 diplexer, only after testing the actual unit
       |                                      |
   VHF branch                             UHF branch
       |                                      |
   VHF antenna                            UHF antenna
   (initially linear)                     (initially linear)
```

If circular polarization is adopted, **each** branch needs two orthogonal
planes and its own characterized phase network, or a physical/electrical
phase displacement designed and tested as a complete assembly. Do not place
one SATCOM hybrid of unknown band before the diplexer to “make both bands
circular.”

Dipole orientation and ports determine RHCP/LHCP sense. Document the viewing
convention and verify experimentally; coax color is not sufficient. Ideal
circular-to-linear mismatch costs 3 dB; opposite ideal circular handedness
does not have a universal 3 dB loss.

## D — Exact network from the user's public project

Revision `f5c7dc375ed7b9882f52bd7757deaf44cd422b81`, README/BOM:

| Branch / reference | Values in the recommended revision |
|---|---|
| VHF low-pass | L1/L3=68 nH; L2=100 nH; C1/C2=18 pF |
| UHF high-pass | L4/L5=15 nH; **C3/C5=8.2 pF; C4=4.7 pF** |
| Historical UHF schematic | C3/C5=4.7 pF; C4=2.7 pF: do not confuse with optimized values |
| Components | 0805; high-Q inductors (examples 0805CS-680XJL/101XJL/150XJL); C0G/NP0 capacitors >=100 V |
| PCB | 2-layer, 1.6 mm FR4, 1 oz copper; author specifies CPWG 50 ohm, 1.4 mm trace, 0.25 mm ground clearance |
| Target bands | 144-146 MHz and 430-440 MHz |

The author notes ambiguity between 10/18 pF in the original schematic for
C1/C2 and chooses 18 pF. Do not mix historical and optimized BOMs. Component
tolerance, Q, ESR, SRF, current, and PCB parasitics have not been verified
here against datasheets.

### Simulation is NOT measurement

The README attributes ideal simulation values of approximately S11=-31 dB
at 145/435 MHz, insertion loss <0.05 dB, and isolation >49 dB to the
optimized design. Do not treat these as guaranteed specifications or call the
diplexer compatible with this new antenna/radio.

`docs/PRUEBAS.md` sets these physical targets:

| Measurement, other port terminated in 50 ohms | Source criterion |
|---|---|
| RADIO-port S11, branches terminated | <-15 dB in 144-146 and 430-440 MHz |
| RADIO -> VHF | Insertion <0.5 dB at 145; rejection >35 dB at 435 MHz |
| RADIO -> UHF | Insertion <0.7 dB at 435; rejection >35 dB at 145 MHz |
| VHF -> UHF, RADIO terminated | Isolation >35 dB in both bands |
| Power with load/wattmeter | Steps 1 -> 5 -> 10 W, stable VSWR, no appreciable heating |

These are **pending criteria**, not results. Do not test at 10 W until
ratings of the actual unit, connectors, inductors, capacitors, load, and
dissipation are confirmed. “No appreciable heating” is not adequate
qualification: record temperature, duration/duty cycle, power, and VSWR.

0805 alone does not guarantee power handling. The README claims **about
5-10 W** for portable/QRP operation and recommends suitable air-core coils
and capacitors for higher power. Acceptance of the new assembly begins at
minimum power; 10 W is not a certified limit. A 100 V capacitor does not
guarantee RF-current capacity, and a high-Q inductor is not guaranteed to
stay cool.

**Order of magnitude:** 5 W into 50 ohms gives 15.8 V RMS and 22.4 V peak
before VSWR/reactive-network effects. At 35 dB isolation, 5 W ~=37 dBm
would leave approximately 2 dBm in the other branch, before other filters/
losses. That can be enormous compared with a satellite signal. Do not approve
a future receiver/LNA from one rejection figure or assume filter simulation
proves real desensitization performance.

Plastic enclosure **does not shield**. Ground planes/vias help but do not
replace RF shielding. Conductive tape/paint requires continuous electrical
bonding, safe clearance from nodes, isolation verification, and subsequent
testing; do not claim an ASA enclosure is sealed or shielded without tests.

### Published EXACT geometry and mechanical hold

| Published interface | SMA | BNC |
|---|---:|---:|
| PCB | 37 x 23 mm | 55.5 x 33 mm |
| Outer enclosure | **45.2 x 27.6 x 14.1 mm** | **59.9 x 37.6 x 23.5 mm** |
| Connector | Amphenol 132289, edge/bulkhead | Amphenol B6252HB-NPP3G-50, right-angle PCB |
| Fastening | 2 x M2 x 10 self-tapping | 2 x M2 x 12 self-tapping |
| PCB holes | 2 x dia. 2.2 mm, plated to ground | 2 x dia. 2.2 mm, plated to ground |

Parameters from `docs/MONTAJE.md`: SMA flange 9.6 mm wide and 1.9 mm thick,
axis “PCB+0.4 mm,” 6.8 mm pitch for 1/4"-36 thread. BNC body 14.8 mm above
PCB, axis “PCB+7.5 mm,” front 14.9 mm. Wall/floor/roof 2.0/2.0/1.6 mm;
lip clearance 0.15 mm. BNC pins <=2.5 mm below PCB.

**The README explicitly says connector dimensions are estimates from KiCad
footprints.** The outer dimensions above are published values, not
measurements of the user's hardware. Measure the actual enclosure/connectors
with calipers; do not assume “PCB+” gives the new mount's height datum
without checking the CAD section. Test the base before the final lid.

Keep the mount/clip parametric, do not load connectors, preserve screw access,
and separate electronics from motors. The envelope also needs room for a nut,
BNC coupling, SMA plug, strain relief, and the coax manufacturer's minimum
bend radius. Those allowances are not automatically included in the outer
dimensions. Do not invent hole coordinates; retrieve `board_geometry.json`
if direct PCB support is intended and compare it with the actual board.

## H/M — Hybrids: selection pending by band, not power

| H candidate | README claim | Manufacturer evidence obtained | Decision |
|---|---|---|---|
| CMX03A03 | 200 W + G150N 50-ohm load | No readable band/power datasheet obtained | Do not select for 145/435 MHz |
| “RF Power,” presumed Florida RF Labs | 200 W, uncertain identity | No unambiguous model/datasheet | Exclude from purchase BOM |
| Anaren 10260-3 | 250 W, old | No readable datasheet in this research | Band/limits pending; do not certify |
| QCN3, called QCN-3 in BOM | 15 W, two 100-ohm 2512 2 W resistors | Mini-Circuits **QCN-3+** specifies **220-470 MHz** | 435 MHz is in specified band; **145 MHz is not**. Identify suffix/unit; do not use as dual-band |

The 225-400 MHz hypothesis for QCN-3+ is not confirmed: the manufacturer
source consulted states 220-470 MHz. Do not automatically extrapolate this
to the no-suffix component or marketplace copies. Nominal band alone does not
establish acceptable loss/phase at 435 MHz under our loads.

**Verified H link bug:** the QCN3 SMA link points to `GERBER-CmxSma.zip`.
Do not fabricate that file as if it were a QCN3 board.

Two 100-ohm resistors in parallel are nominally 50 ohms and sum to 4 W
nominally, **not a validated RF load** and not proof of 15 W handling. The
isolated port can absorb significant power with mismatched loads; conservatively
size it for the network's worst case. Verify dissipation, mounting, impedance
through 435 MHz, rating, and temperature. A 150 W air-cooled load without a
suitable heatsink is not equivalent to 150 W continuous.

## O0/O1 — What the RT-3S can actually do with OpenGD77

The older requested O0 guide only establishes VFO operation with different
TX/RX for cross-band/split; it does not establish current RT-3S satellite
screen support. Maintained O1 guide (`2289ba75...`, 2026-03-10) lists
**MD-UV380 (RT-3S)** and documents:

1. **Satellite Screen:** predicts the next 24 hours from location, date, and
   time; displays AZ/EL and automatically corrects Doppler on **TX and RX
   frequencies**.
2. User must enter location/date/time and load **Keps via CPS**. Loading
   recent Keps also sets date/time.
3. RT-3S/UV380 has an RTC according to that guide; this does not prove the
   current accuracy or the state/battery of the actual radio.
4. Frequencies and CTCSS are loaded with CPS data; changes require editing
   data/satellites.txt for the corresponding CPS.
5. SO-50: SK1 during TX applies its arming tone per the guide; verify current
   satellite status/mode.
6. Live screen offers types 1 FM Voice, 2 APRS, 3 Beacon; beacon does not
   permit TX. This does not mean every satellite in a local table is radio-
   compatible.
7. “Sat / Manual” versus “Auto” controls switching to the next satellite
   after LOS. **“Manual” here does not necessarily mean manual Doppler.**
   Distinguish satellite selection from frequency tuning.

### Use plan without inventing CAT

- Record firmware model/build and CPS version; save the codeplug/configuration.
  Confirm the Satellite menu appears and calculates correctly on the actual radio.
- Load Keps/data with CPS before departure; synchronize RT-3S and controller
  UTC/location. The rotor AP does **not magically load CPS**.
- Rotor calculates SGP4 and moves AZ/EL autonomously. Operate RT-3S by keypad/
  PTT and use its built-in Doppler only if the build supports the described
  feature. Otherwise use presets/manual Doppler adjustment.
- Compare prediction/time/frequencies on both; TLE, UTC, or location mismatch
  causes misalignment even if each screen works.
- **RT-3S CAT**, live USB control protocol, remote PTT, full duplex, and
  reception during TX have not been verified. Do not implement them using
  Yaesu/IC-820H commands or an imaginary API.
- Do not confuse DMR, digital hotspot, or CPS programming with a satellite
  CAT port. Do not promise SSB/CW on this portable FM/DMR radio.

## Minimum physical acceptance plan

1. **Documentation/cables:** identify actual components, pinouts/ports,
   connectors, coax velocity factor and minimum bend radius. Inspect and check
   continuity unpowered.
2. **Individual antennas:** calibrated VNA at actual reference plane; measure
   S11/bandwidth on final mount, with coax routed. Record fold state and rotor proximity.
3. **Separate diplexer:** SOL/through calibration; sweep 100-500 MHz at
   >=401 points; terminate free ports in 50 ohms; measure every route and
   reflection. Save Touchstone, photos, date, and setup. Check noise floor/
   dynamic range before attributing 35 dB isolation.
4. **Polarization network, if any:** measure loss, amplitude/phase difference,
   match, and isolated port per band. Radiated handedness/axial-ratio/pattern
   test with defined method and geometry.
5. **Complete assembly:** measure antenna interaction/matching, band isolation,
   and coax effects as AZ/EL vary. Repeat after mount/coax changes.
6. **Power into load:** start low; increase only within demonstrated rating.
   Record temperature/VSWR/duration and tolerance of worst mismatch per
   component; do not indiscriminately transmit into an antenna during setup.
7. **Rotor EMI:** compare reception with drivers off/hold/moving, DC/DC, and
   AP on. Relocate/filter if noise appears.
8. **Operation:** first satellite pass receive-only; verify current satellite/
   mode, authorization, and minimum reasonable power. Do not “test isolation”
   by saturating an LNA/receiver.

Current state: **architecture justified; RF candidates and tests defined;
antenna/diplexer/hybrids and radio-rotor assembly still NOT measured or approved.**

## A — Added AV2040 datasheet comparison

The new local `TDS_AV2040.pdf`, page 1, identifies a foldable/manpack **UHF
SATCOM antenna**. Text extraction loses figures due to font encoding; page was
read visually from locally rendered `TDS_AV2040-000001.png` at 140 dpi.
Manufacturer Ultralife/Trivec-Avant, **23 Nov 2010, UBI-05273 REV:-**.
Values below are published datasheet information, not measurements of
PortableSatStation.

| Aspect | Available datasheet evidence | Consequence for PortableSatStation |
|---|---|---|
| 145 MHz | Commercial band **240-400 MHz** | **145 MHz out of band**; no VHF coverage established |
| 435 MHz | Commercial band **240-400 MHz** | **435 MHz out of band**; SATCOM appearance does not establish compatibility |
| VSWR | 1.5:1 published | Do not extrapolate out of band or to the new design |
| Polarization | Right-hand circular; 3 dB axial ratio | Does not guarantee our phase network or axial ratio |
| Gain by version | 2040-3: +7 dBic 240-400; 2040-2: +11 dBic 240-318; 2040-1: +9 dBic 240-400 MHz | Do not confuse versions/bands or assign these dBic values to the ASA antenna |
| Power | 200 W CW published | Not a rating for new hybrid/PCB/diplexer |
| Folding | Described as foldable/manpack | Functional requirement, not license or geometric dimension |
| Deployed/folded dimensions | **No dimensions are published on the visually reviewed page** | No verifiable length/width/volume; do not measure a photograph as a drawing |
| Mass | 6.5 lb in datasheet | Do not transfer mass or CG to the original ASA design |
| Connector | Male BNC | Check interface/jumper; do not confuse with diplexer BNC female |

449.550 MHz belongs to **blog B**, not datasheet A, and is also outside the
commercial 240-400 MHz band. The blog is a distinct retuned construction,
not evidence the factory AV2040 extends its band. AV2040 remains a **functional
reference, not a 145/435 MHz alternative within specification**. The photo
has no folded dimensions, and OBJ/STL of unverified license are not distributed
with this project. Manufacturer footer says data are for reference, not a
performance warranty, and subject to change.
