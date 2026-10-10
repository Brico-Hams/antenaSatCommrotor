# Build and procurement sequence

## Before buying or printing

1. Read ARCHITECTURE, MECHANICAL, CONTROL, and RF-AND-RADIO.
2. Choose the exact motor; record mass, shaft, length, current, and torque curve.
3. Measure the radio, tripod, diplexer, and alternative antenna. Update CAD
   parameters before printing brackets. Nominal compatibility does not prove fit.
4. Obtain quotes for the three BOM lists. Indicative amounts are not a price or
   availability commitment.
5. Define operating frequencies and simulate/measure the RF architecture.
   Do not buy hybrids based on advertised power without checking their band.
6. Verify tools: OpenSCAD for CAD, the PlatformIO control environment, and
   Node.js for calculations. In this delivery, portable validation programs
   are hosted outside the repository; they are not field dependencies.

## Progressive fabrication

### Iteration A: meshing and assembly

Print coupons and one planetary stage. Assemble and turn it by hand. Confirm
phase, clearance, eccentricity, and torque path. Do not print the entire
assembly before adjusting the first stage.

### Iteration B: controller bench

Assemble ESP32, GNSS, sensors, limits, and stop with unloaded motors. Build
and flash the exact revision and test every fault. The device must remain
disarmed at startup; also verify that drivers and wiring do not enable motors
through a floating GPIO.

### Iteration C: second axis and support

Assemble both reductions, metal shafts, and tripod attachment. Add a balanced
test mass, not a long unvalidated antenna. Measure accuracy/backlash, current,
and temperature. Apply G1.

### Iteration D: antenna and diplexer

Cut metal with adjustment allowance. Published values are starting dimensions;
insulators, coax, diameter, hardware, and other bands change electrical length.
Tune in the final assembly with a VNA. The reflector also needs reliable
conductive joints. Integrate the earlier diplexer only after verifying its
revision, dimensions, and S-parameters.

### Iteration E: field

Begin with reception and compare tracking independently. Transmit only with
authorization and at minimum power, and only after G1-G3. Do not leave the
system unattended or operate in unvalidated wind.

## Changes and revisions

Record every change of module, motor, microsteps, conductor diameter, coax, or
mounting. An RF change requires RF revalidation; a gear, shaft, load, or tripod
change requires mechanical revalidation. Do not let firmware and CAD retain
parameters for different reductions.

Before publishing on GitHub: verify the selected MIT/CERN-OHL-S-2.0 scope,
check dependencies and their notices, check for credentials/private
attachments, and satisfy hardware source-delivery obligations.
