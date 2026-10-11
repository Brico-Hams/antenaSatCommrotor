# Pre-fabrication gate for the PCBs

Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.

## PCB — Pre-fabrication gate for the PCBs (ESP32 carrier and cm5-guard-A)

**Expected component behaviour.** No board is ordered or manufactured until every item of this gate is APPROVED with a measurement and date. A Gerber ZIP or a render does not replace ERC/DRC or the bench.

### PCB-01
- [ ] **Action:** Open each project in KiCad and run ERC, DRC, "unconnected items" and schematic/PCB parity with the documented version.
- **Expected behaviour:** Zero errors and zero unjustified warnings.
- **Pass criterion:** Report saved under reports/; the silkscreen logo added by script requires a DRC re-run (pending in this revision).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PCB-02
- [ ] **Action:** Check each fabrication file against its SHA-256 in reports/manifest-sha256.json and fabrication/release-status.json (sha256sum).
- **Expected behaviour:** All hashes match.
- **Pass criterion:** Any difference = do not manufacture; regenerate the manifest with the repository script.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PCB-03
- [ ] **Action:** Load the Gerbers in an independent viewer (KiCad Gerber Viewer, Tracespace or gerbv) and review layers, drills, outline and the BricoHams logo on silkscreen.
- **Expected behaviour:** Complete layers, logo legible without overlapping pads or holes.
- **Pass criterion:** Logo clearance ≥ 8 mm (carrier) and ≥ 21 mm (guard-A) per BRANDING.md; no silkscreen on pads.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PCB-04
- [ ] **Action:** Build the equivalent circuit on the bench (real modules + prototype wiring) for each block: power, drivers, sensors, stop/watchdog.
- **Expected behaviour:** Each block passes the PWR, DRV and SNS tests on the bench.
- **Pass criterion:** All tests of those sections APPROVED before ordering the board.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PCB-05
- [ ] **Action:** With the GPIO-contract tester (bench, see BENCH) walk the 26 signals of interface.json: every output drives its LED, every input answers its switch.
- **Expected behaviour:** The 26 signals match BCM, header pin and default safe level.
- **Pass criterion:** Zero crossed or duplicated signals; all outputs at their safe level after reboot.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PCB-06
- [ ] **Action:** Check footprints against datasheets: pin 1, orientation and pitch of DevKitC, SilentStepStick, MCP23017, TCA9548A, connectors and fuses; print the PCB 1:1 on paper and place the real modules on it.
- **Expected behaviour:** All footprints physically fit.
- **Pass criterion:** No module clashes with another, with enclosure screws or the lid (G1E-12).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PCB-07
- [ ] **Action:** Review trace/power-track current budget (width, copper, drop) with the three motors' current and the fuse.
- **Expected behaviour:** Calculated drop and temperature within limits.
- **Pass criterion:** Calculated and confirmed by bench measurement (PWR-02, PWR-08).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PCB-08
- [ ] **Action:** Prepare the order: BOM, CPL (references, coordinates, side, rotation), DNP/manual-module list, manufacturer DFM and confirmation of exact LCSC parts.
- **Expected behaviour:** Order has no blocking DFM warnings; no order is sent without explicit approval.
- **Pass criterion:** Everything APPROVED and checked by a second person; do not pay until PCB-01…07 are closed.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

[Back to the index](README.md)
