# Power, wiring, and electrical separation

This document defines the electrical architecture, not a fabricated PCB or a
compatibility claim for every available module. The user has also requested a
module-carrier PCB with schematic, Gerbers, sensor connections, and
protection. Its development is tracked separately; not all DevKit or StepStick
modules are assumed to have the same footprint. See ADR-020. Final GPIO
assignments and controller connections are in CONTROL.md and its firmware.

## Power tree

```text
protected commercial 12 V supply, nominal; range verified with drivers
  |
  +-- fuse sized for cable/current -- main switch
        |
        +-- physical motor-power cutoff via accessible stop
        |     +-- AZ driver -- AZ motor
        |     +-- EL driver -- EL motor
        |
        +-- 5 V DC/DC -- ESP32 board
                    +-- 3.3 V regulation for compatible sensors

RT3S: own independent battery
RF: passive equipment in metal enclosure; no automatic PTT
```

Use a protected commercial supply/battery with verified protection and its
proper charger. Do not improvise a lithium pack. The stop must inhibit motion
even if firmware or the browser hangs. The NC contact monitored by software
is complementary to the hardware cutoff; it is not a certified safety relay.

## Drivers and current

A TMC2209 or equivalent limits phase current; calculate the setting from its
board, sense resistor, and motor RMS current rating, not by copying a value
from another NEMA14. Confirm actual 16-microstep mode: 80,000
steps/revolution assumes a 200-step/revolution motor, 16 microsteps, and
25:1, not the driver's 256-step internal interpolation.

Place decoupling near VMOT per the manufacturer, protect against reversed
polarity, provide ventilation, and verify temperatures in a closed enclosure
in sunlight. Do not connect/disconnect a motor while its driver is powered.
Review the common logic/driver ground and separation between power, coax, and
GNSS.

## Sensors and wiring

- ESP32 inputs do not tolerate 5 V unless a documented level adaptation is used.
- AS5600 devices share an I2C address: separate buses or use a multiplexer;
  two sensors on the same bus without distinct addresses will not work.
- Magnet orientation, distance, and axis matter. Verify out-of-range fields
  and rotation before trusting feedback.
- Serial GNSS must have compatible logic levels; its antenna needs open sky
  and does not provide azimuth reference while stationary.
- Wire NC so a cut cable causes a fault. Confirm electrical and logical
  polarity with motors disconnected.
- Travel limits need physical placement and stopping margin; drawing them or
  limiting software variables is not enough.

## RF all-in-one, but modular

Separate the diplexer metal enclosure and RF networks from drivers and
converters. ASA is an enclosure material, not shielding. Secure connectors
and provide strain relief; do not let coax weight load the RT3S SMA.
The radio mount must leave PTT, volume, display, battery, and antenna
connection accessible. Do not specify an SMA adapter before checking its
gender and thread on the actual unit.

Compare received noise with motors/DC-DC on and off. If it rises, correct
filtering, placement, shielding, and return paths before TX. RF/diplexer
connections are separate from any assumed USB radio-control interface.

## Energy autonomy: method, not a promised figure

Measure tracking, idle, homing, and Wi-Fi power. Usable energy is measured at
the supply output, not cell capacity multiplied by 12 V when the manufacturer
specifies mAh at another voltage.

`hours = usable_Wh / average_W`

Arithmetic-only example: 30 Wh usable and 8 W average -> 3.75 h. This is not
an estimate for this station until current is measured. Record margin for
cold, aging, and converter derating.
