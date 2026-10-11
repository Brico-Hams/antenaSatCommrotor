# System integration (G3 / G4)

Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.

## SYS — System integration and gates G3 / G4

**Expected component behaviour.** With every module accepted separately, integrate in this order: mechanics without RF, passive RF, receive and control, and only last authorised transmission. Nothing is reused after changing location: recalibrate.

### SYS-01
- [ ] **Action:** Track a real satellite pass and compare with an independent reference, same station and TLE.
- **Expected behaviour:** Pointing throughout the pass.
- **Pass criterion:** Pointing error within the antenna beam (G3-1); commanded vs. measured AZ/EL log.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SYS-02
- [ ] **Action:** Without Internet (own AP): import TLE, select, predict and track; close the app during the pass.
- **Expected behaviour:** Tracking continues on the controller.
- **Pass criterion:** Calculation and tracking do not depend on the phone (G3-2/3).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SYS-03
- [ ] **Action:** Provoke: GNSS loss, invalid UTC, old cache, lost encoder, pass below horizon, zenith, cable wrap and unreachable speed.
- **Expected behaviour:** Documented policy, warning and safe stop in each case.
- **Pass criterion:** Explicitly rejected; never points at a wrong target (G3-4/5).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SYS-04
- [ ] **Action:** Confirm true north against a known reference; move the tripod and repeat calibration.
- **Expected behaviour:** True orientation confirmed at each location.
- **Pass criterion:** Calibration is not reused at a new location (G3-7).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SYS-05
- [ ] **Action:** Weigh the operating set and measure endurance on the chosen battery in a 2-hour continuous run.
- **Expected behaviour:** Measured mass and endurance.
- **Pass criterion:** ≤ 5 kg without the external battery and 2 h target endurance demonstrated by test, not calculation.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SYS-06
- [ ] **Action:** G4, licensed only: test transmission into a load at minimum power, then an authorised real pass; watch temperature of networks and connectors.
- **Expected behaviour:** Clean transmission; no TX with an unmatched network or outside the diplexer/hybrid range.
- **Pass criterion:** Only one TX active; monitoring your own downlink requires a protected second receiver; full-duplex is not claimed with a passive filter.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

[Back to the index](README.md)
