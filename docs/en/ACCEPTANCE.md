# Tests and acceptance gates


Step-by-step detail, test bench and per-component checklists: [testing/README.md](testing/README.md).

Record date, Git revision, instruments, operator, assembly, and result.
A criterion that has not been measured is PENDING, not APPROVED by calculation.

## G0: software and digital geometry

1. Build firmware with pinned dependencies.
2. Run orbital, limits, time, and invalid-data tests.
3. Compare SGP4 with an independent implementation for the same TLE/UTC/site:
   target <=0.1 degrees AZ/EL away from zenith, using the same conventions
   and geodesy.
4. Check units: GNSS altitude in metres, library units per its API;
   latitude/longitude in degrees, UTC without local-time correction.
5. Render ALL parts with OpenSCAD; check closed meshes, volume,
   self-intersection, and unexpected components.
6. Review both stages' mesh, planet phase, bearings, shaft, clearances,
   fasteners, and assembly access; rendering does not replace this review.
7. Truncated TLE, bad checksum, old epoch, HTML names, unavailable source,
   and oversized catalog must fail explicitly and must not cause motion.

## G1: mechanics without RF

1. Print coupons for hole, shaft, insert, tooth, and bushing. Measure ASA
   shrinkage and record compensation; do not sand away evidence of failures.
2. Assemble one unpowered stage: smooth full rotation, free planets,
   concentrically supported output. Repeat with two stages.
3. Confirm the second-stage sun is fixed to the first-stage carrier: a
   floating gear cannot transmit torque.
4. Verify physical motor cutoff by stop and NC limits.
5. Boot/reboot/watchdog must not cause rotation or restore homing.
6. Home without antenna: disconnected, stuck, or unreached switch must fault
   on timeout, not cause unlimited movement.
7. Measure backlash with an indicator/protractor during reversal and record
   in degrees.
8. Balance a 0.5 kg target load with CG <=30 mm; use secondary retention and
   a stable bench before the tripod.
9. Test accuracy <=2 degrees RMS during slow movement without wind and
   maximum deviation <=5 degrees. Separate heading error from axis error.
10. Run for 30 minutes under load: no missed steps, loosening, or temperature
    above any component's limit.
11. Validate AZ, EL, and cable limits with calculated stopping margin.
12. Weigh everything, including cables and power: earlier target <=3 kg
    without radio/tripod. Measure packed size; indicative length target
    <=450 mm with radiators disassembled. Do not weigh only the enclosure.

The torque budget in `calc/design.json` shows that the **example** of 8 m/s
wind, 0.06 m2, and 0.25 m arm does NOT meet safety factor 2 with assumed
0.1 Nm motor torque. Therefore 8 m/s is NOT an authorized wind limit. Until
running torque and actual load are measured, operate only on a controlled
bench without wind. Revalidate every alternative antenna.

## G1E: carrier board and WebFlash, before powering motors

1. Freeze schematic/PCB/Gerber revision, module list, and firmware pinout.
   All 16 GPIO signals must match, with no duplicates.
2. Run ERC, DRC, unconnected-net, and schematic/PCB parity checks with the
   documented tool; existence of a Gerber ZIP is not a substitute.
3. Manually inspect footprints, pin 1 and DevKitC/driver orientation,
   trace current, terminals, fuses, TVS, and dissipation.
4. With modules absent, measure net continuity and absence of shorts; apply
   a current-limited supply according to the electrical procedure.
5. Verify 12 V, 5 V, and 3.3 V at their nodes; no GPIO may receive 5 V.
6. Measure ENABLE disabled at startup. Check the physical VMOT cutoff
   independently of the MCU, with logic powered to report the fault.
7. Check open NC and broken-wire behavior for every sensor. Verify external
   pull-ups on input GPIOs without internal pull-ups.
8. Flash only the compatible ESP32, with motors and radio disconnected.
   Verify hash and offsets for application, partitions, and LittleFS.
9. Public image contains no secrets: provision by USB; confirm it does not
   print passwords/token and remains unhomed after SETUP/reboot.
10. NVS is unencrypted: protect physical access; do not copy its contents to
    Git. LittleFS updates may replace TLE/cache: document a prior backup and
    do not confuse preserving NVS with preserving the filesystem.
11. GitHub Actions/Pages needs separate remote testing; a locally approved
    manifest does not prove remote permission or successful deployment.
12. Check that enclosure branding is integrated into the lid without
    overlapping connectors, screws, ventilation, or becoming a loose part.

## G2: passive RF

1. Calibrate the VNA at the connector reference plane, with no radio attached.
2. Measure each dipole/reflector per band and its matching networks.
3. With the assembly deployed, coax and rotor in actual positions: target
   VSWR <=1.5 at the selected center frequency and <=2 on operating channels.
   Document bandwidth; do not extrapolate.
4. Measure each hybrid by band: target amplitude imbalance <=0.5 dB and
   phase 90 +/-5 degrees at selected frequencies; use a suitable isolated-port
   load.
5. Measure diplexer: initial screening target insertion loss <=1 dB per
   branch, return loss >=14 dB, and isolation >=40 dB. For another simultaneous
   receiver, calculate required isolation from TX power and maximum allowed
   receiver level, including margin; 40 dB does not guarantee no desensitization.
6. Pattern, RHCP/LHCP sense, and axial ratio: do not infer them from a
   commercial hybrid or good VSWR; measure/simulate the assembly. Initial
   target axial ratio <=3 dB toward the satellite before claiming circular.
7. Check continuity and repeatability after 50 folds. Plastic hinges cannot
   be the only RF contact.

## G3: reception and control

1. Compare a pass with an independent reference for the same station and TLE.
2. AP without Internet: import TLE, select, predict, and track.
3. Close the phone during a pass: ESP32 calculation/tracking continues.
4. Loss of GNSS, invalid UTC, stale cache, or lost encoder: verify documented
   policy, warning, and safe stop.
5. Below-horizon/not-started pass, cable wrap, zenith, and unreachable speed:
   explicitly reject; do not point at the wrong target.
6. Compare RX noise with converters and motors on/off.
7. Confirm true orientation against a known reference; repeat after moving the
   tripod, and do not reuse calibration at a new location.

## G4: authorized transmission

Only with verified license/authorization, frequencies, and satellite. Begin
at minimum power with a suitable bench load; review network and connector
temperature. Do not transmit through an unmatched network or outside the
verified range of the diplexer/hybrid.

An RT3S does not hear the downlink while transmitting in half-duplex mode.
Use a second receiver to monitor your own downlink and calculate TX
protection. Do not claim full duplex through a passive filter.

## Results sheet

| Test | Revision/instruments | Measured result | State | Action |
| --- | --- | --- | --- | --- |
| G0 | To be completed | See VALIDATION | Partial | Per record |
| G1 | Prototype not assembled | Not measured | Pending | Print and test |
| G2 | VNA required | Not measured | Pending | Match and measure RF |
| G3 | Tracking bench | Not measured | Pending | Verify autonomy |
| G4 | Radio/license | Not measured | Pending | Only after G1-G3 |
