# Rotor mechanics

Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.

## MEC — Rotor mechanics (AZ / EL / POL)

**Expected component behaviour.** Axes turn smoothly without a motor, belts hold tension, physical stops halt before cables are damaged and the drive loses no steps under the target load. 8 m/s wind is NOT an authorised limit until real torque is measured.

### MEC-01
- [ ] **Action:** Print test coupons (hole, shaft, insert) and measure ASA shrinkage with calipers; print bearing cups and keepers.
- **Expected behaviour:** Measured dimensions against nominal.
- **Pass criterion:** Compensation recorded; 608/6000 fit without forcing or visible play; no sanding to hide faults.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-02
- [ ] **Action:** Assemble the belt gearbox WITHOUT motor (20T:100T ×2 = 25:1, 252 mm GT2 belts); turn the output by hand one full revolution.
- **Expected behaviour:** Smooth, even rotation, no tooth skipping or belt rubbing.
- **Pass criterion:** Even hand torque; belt aligned and clear of plates; 1 mm gap between stages.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-03
- [ ] **Action:** Measure belt tension (deflection under load at mid-span) using the ±1.5 mm slots; repeat after 30 min.
- **Expected behaviour:** Tension stable after run-in.
- **Pass criterion:** No slipping or tension loss >10 %; screws with threadlocker/washers, none loosening.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-04
- [ ] **Action:** Confirm the 2nd stage input pulley is fixed to the 1st stage output shaft (does not float) and the output shaft is held by two bearings.
- **Expected behaviour:** Torque transmitted with no slipping with the motor locked and torque applied by hand at the output.
- **Pass criterion:** Zero relative rotation between pulley and shaft; concentric output.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-05
- [ ] **Action:** Homing without antenna with the limit switch: a) connected, b) disconnected, c) stuck, d) not reached.
- **Expected behaviour:** a) sets AZ=-180°, EL=0°; b,c,d) fault with timeout.
- **Pass criterion:** Never unbounded motion; the fault requires rehome (G1-6).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-06
- [ ] **Action:** Measure backlash by reversing direction with a dial indicator or protractor on each axis.
- **Expected behaviour:** Value in degrees per axis.
- **Pass criterion:** Recorded and compensated in software; indicative target ≤ 1°; consistent with SNS-03.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-07
- [ ] **Action:** Balance the target load (0.5 kg antenna) and measure the CG relative to the axis; test with secondary retention on a stable bench before the tripod.
- **Expected behaviour:** CG within 30 mm of the axis.
- **Pass criterion:** CG ≤ 30 mm; EL axis does not fall when power is cut or is retained (rest torque without motor).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-08
- [ ] **Action:** Slow tracking in calm air: sweep each axis and compare encoder position with a reference protractor/indicator at 10 positions.
- **Expected behaviour:** Error per position.
- **Pass criterion:** Accuracy ≤ 2° RMS and maximum deviation ≤ 5° (G1-9); separate heading error from axis error.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-09
- [ ] **Action:** Run 30 min of alternating motion under the target load; check lost steps, loosening and temperature.
- **Expected behaviour:** Return position identical to the start.
- **Pass criterion:** No lost steps (final error < 1°), no loose screws, temperatures within limits (G1-10).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### MEC-10
- [ ] **Action:** Weigh the complete operating set (includes tripod, radio and cables; excludes the external battery, weighed separately) and measure the folded bulk.
- **Expected behaviour:** Total mass and dimensions.
- **Pass criterion:** Mass ≤ 5 kg per the current requirement (the earlier ≤ 3 kg is historical); record battery mass separately.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

[Back to the index](README.md)
