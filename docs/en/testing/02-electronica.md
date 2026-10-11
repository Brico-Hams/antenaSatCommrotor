# Electronics: power, drivers and sensors

Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.

## PWR — Power, protection and stop

**Expected component behaviour.** With the stop pressed no motor can receive power even if firmware or host hang; the CM5 and logic stay powered to report the fault. Releasing the stop does NOT resume motion: re-arm and repeat homing.

### PWR-01
- [ ] **Action:** With no motors or radio, connect the bench supply with current limit at 0.2 A and raise to the nominal 12 V.
- **Expected behaviour:** Stable idle current and no heating; nothing hot to the touch after 2 min.
- **Pass criterion:** Current below the limit without hitting it; correct polarity (check first with a series diode/LED).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PWR-02
- [ ] **Action:** Measure 12 V, 5 V and 3.3 V at their nodes (board/CM5IO/auxiliary) at idle and under load.
- **Expected behaviour:** Three rails within ±5 % with no sag when motors start.
- **Pass criterion:** No GPIO sees more than 3.3 V; 12 V never reaches the CM5 (CM5-PCB).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PWR-03
- [ ] **Action:** With motors connected at 12 V, press the emergency stop and measure VMOT at each driver.
- **Expected behaviour:** VMOT falls to 0 V on every axis; logic/CM5 stay alive and report ESTOP.
- **Pass criterion:** VMOT < 1 V; ESTOP_AUX_N (BCM10) goes active-high; no residual motion.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PWR-04
- [ ] **Action:** With the system stopped, kill and restart the host (kill -9 the service and reboot) while the stop is pressed.
- **Expected behaviour:** The physical cut holds: no axis moves on reboot.
- **Pass criterion:** Zero motion; state after boot is DISARMED with homing not restored (G1-5).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PWR-05
- [ ] **Action:** Stop the WATCHDOG_HEARTBEAT (BCM11) with motors armed on the bench and no mechanical load.
- **Expected behaviour:** Motor permit drops and drivers are disabled (EN high).
- **Pass criterion:** Cut-off time measured on a scope and recorded; the exact watchdog design is unselected, do not invent a value.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PWR-06
- [ ] **Action:** Provoke a blown-fuse condition (remove it) and a cut limit-sensor wire on each NC input.
- **Expected behaviour:** Explicit software fault and motors inhibited.
- **Pass criterion:** Open wire = HIGH = fault; never interpreted as a healthy limit (LOW = healthy).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PWR-07
- [ ] **Action:** Measure ripple and transients on VMOT and 5 V with a scope (short ground spring) while the three motors accelerate and stop.
- **Expected behaviour:** Spikes and sag within what drivers and CM5 tolerate.
- **Pass criterion:** No CM5 resets, no driver fault; record peak-to-peak (EMI gate of CM5-PCB).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### PWR-08
- [ ] **Action:** Run 30 min with motors in slow alternating motion and measure temperature with a thermal camera/thermocouple on drivers, DC/DC, fuse and Powerpole connectors.
- **Expected behaviour:** Thermal stabilisation with no continuous drift.
- **Pass criterion:** No part exceeds its datasheet limit; connector voltage drop < 50 mV per contact at working current.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

## DRV — Motor drivers (TMC5160 v1.5 on CM5; TMC2209 on the ESP32 carrier)

**Expected component behaviour.** Each driver powers up DISABLED (EN high); it is enabled only with the common hardware permit plus a per-axis request. STEP/ramp pulses come from the driver (TMC5160 ramp mode over SPI), never a Linux loop.

### DRV-01
- [ ] **Action:** With no motor, power up and read each TMC5160 version/IOIN register over SPI (CS0 AZ, CS1 EL, CS2 POL).
- **Expected behaviour:** All three answer with the expected chip version.
- **Pass criterion:** Valid reply on all three CS; if not, check SPI1 wiring (MOSI BCM20, MISO BCM19, SCLK BCM21).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### DRV-02
- [ ] **Action:** With motors connected and EN high, check the shafts turn freely by hand (no holding torque).
- **Expected behaviour:** No holding torque with the driver disabled.
- **Pass criterion:** Free rotation = driver really disabled.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### DRV-03
- [ ] **Action:** Compute phase current from your board's sense resistor and the motor rated current, set IRUN/IHOLD and measure one phase with a clamp/ammeter.
- **Expected behaviour:** Measured RMS current ≈ computed.
- **Pass criterion:** Within ±10 % and never above the motor rated current; do not copy another NEMA14's value.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### DRV-04
- [ ] **Action:** Turn one axis exactly 10 motor revolutions through the driver ramp and count with a mark/encoder.
- **Expected behaviour:** Mechanical turn = expected steps (200 steps × 16 microsteps × ratio).
- **Pass criterion:** Accumulated error < 1 motor step; make sure you do not count interpolated 256 microsteps as real steps.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### DRV-05
- [ ] **Action:** Provoke a driver fault (simulated over-temperature or disconnect a phase with the driver off) and watch FAULT_AZ_N/EL_N/POL_N (BCM24/25/26).
- **Expected behaviour:** The fault is signalled and motors are inhibited; no automatic retry.
- **Pass criterion:** Fault visible in host status and in the app; clearing requires rehome.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### DRV-06
- [ ] **Action:** Measure driver temperature after 10 min at working current in a closed enclosure.
- **Expected behaviour:** Stable temperature.
- **Pass criterion:** Below the datasheet limit with margin; otherwise add heatsink/ventilation and repeat.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

## SNS — Sensors: AS5600, NC limit switches, GNSS, compass/IMU

**Expected component behaviour.** A missing or out-of-range sensor produces an explicit fault, never an invented value. A stationary GNSS does NOT give heading.

### SNS-01
- [ ] **Action:** Scan I2C1 through the TCA9548A multiplexer (0x70): select each channel and read the AS5600 (0x36).
- **Expected behaviour:** One AS5600 per channel; the multiplexer reset (BCM13) recovers the bus.
- **Pass criterion:** All three AS5600 answer one at a time; two on one channel without a multiplexer fails the scan (expected).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SNS-02
- [ ] **Action:** Read AS5600 STATUS (MD/ML/MH) and AGC with the magnet at the mounting distance; rotate 360°.
- **Expected behaviour:** MD=1 (magnet detected), ML=MH=0, AGC mid-range; angle monotonic 0 to 4095.
- **Pass criterion:** No MH/ML over the whole turn; diametric magnet centred; flip direction if the rotation is reversed.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SNS-03
- [ ] **Action:** Compare the AS5600 angle with a protractor/indicator at 8 positions.
- **Expected behaviour:** Reading agrees with the reference.
- **Pass criterion:** Error ≤ 0.5° (12-bit resolution ≈ 0.088°); record deviation and mechanical play.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SNS-04
- [ ] **Action:** Actuate each limit switch (AZ min/max, EL min/max, POL min/max) and watch BCM4, 5, 6, 7, 8, 9.
- **Expected behaviour:** Healthy = LOW; actuated or cut wire = HIGH.
- **Pass criterion:** All six respond; the motor is inhibited in the limit direction; software does NOT replace the physical stop.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SNS-05
- [ ] **Action:** GNSS outdoors or at a window: wait for a fix and compare UTC and position with a known reference; measure PPS (BCM27) on a scope.
- **Expected behaviour:** Valid NMEA, 1 Hz PPS.
- **Pass criterion:** UTC error < 1 s versus reference; stable PPS; coordinates and altitude in the units the software uses (altitude in metres).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SNS-06
- [ ] **Action:** Remove the GNSS antenna and watch time/site state in the host.
- **Expected behaviour:** UTC/site become invalid after the grace time; tracking blocked.
- **Pass criterion:** Explicit warning and safe stop (G3-4); never keeps tracking on stale UTC silently.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SNS-07
- [ ] **Action:** Compass/IMU: point the antenna at a known true heading (sun/reference) with motors off and on; note the difference.
- **Expected behaviour:** Stable, repeatable reading away from metal.
- **Pass criterion:** Deviation documented with declination corrected; if active motors change the reading, move the sensor away (remote compass).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

[Back to the index](README.md)
