# Standalone module: AZ/EL/POL rotor

## Scope and dependencies

The rotor can be built without LimeSDRs, PA, RF filters, project antenna, or
audio system. Another antenna is acceptable only if its mass, CG, and loads
are qualified. The new variant uses a CM5/CM5IO and auxiliary board; the
two-axis ESP32 variant is a separate historical design and does not
automatically provide the third, POL axis.

| Required | Not required for rotor-only |
| --- | --- |
| Three axes, motors/transmissions, supports, and mounting/tripod | Two LimeSDRs and a high-power radio |
| CM5/CM5IO, auxiliary board, three ramp-generator drivers, and protected power | Bluetooth audio/codec/mic/speaker |
| GNSS, orientation/calibration, encoders and NC limit switches, stop/watchdog | Circular antenna or RHCP/LHCP networks |
| Cables, fuses, Powerpole, and compatible regulation | TX/APRS/SSTV |

Project references: [CM5-ROTOR.md](CM5-ROTOR.md),
[POLARIZATION-MECHANICAL.md](POLARIZATION-MECHANICAL.md),
[MECHANICAL.md](MECHANICAL.md), and [CM5-PCB.md](CM5-PCB.md). These sources
identify what is implemented and what requires bench testing; do not buy
parts for an unfrozen revision as though it were released.

## Module components and costs

See [REFERENCE-PRICES.md](REFERENCE-PRICES.md) and
[reference-prices.csv](../../bom/reference-prices.csv): CM5, CM5IO, DRV x3,
ENC x3, COMPASS, IMU, and GPS are rotor references. MOTION, HARDWARE,
STRUCTURE, PCB-FAB/PCB-PCBA, and POWER-RAILS/HARNESS still need complete
quoting/selection. Select only the consumables and shared parts actually
installed. Do not include SDRs, PA, audio, or RF filters in a rotor-only
purchase. Stop, watchdog, and motion protections are not removed just
because the radio is absent.

## Standalone assembly and configuration

1. Choose compatible rotor and auxiliary-board revisions. Do not use a
   two-TMC2209/ESP32 carrier for a three-axis CM5 configuration.
2. Assemble the structure, metal bearings/shafts, and transmissions with
   power off; check travel and balance. POL is a limited-rotation axis.
3. Install output encoders and six NC limit switches; check the end stops
   and coax service for the antenna to be used.
4. Install CM5/CM5IO and the auxiliary board according to the frozen board
   map, with ramp-mode drivers and compatible logic; do not generate STEP
   pulses in a Linux loop.
5. Install GNSS with a clear view of the sky and a compass/IMU away from
   disturbing magnetic fields. A stationary GPS does not measure north.
6. Wire the external supply, Powerpole/fuses, and regulation; check
   continuity/polarity with the motors disconnected. Do not apply 12 V to
   the CM5.
7. Configure a rotor-only profile in the installer when available: do not
   require or start SDR devices. Verify the actual published commands in
   [CM5-ROTOR.md](CM5-ROTOR.md); do not invent services.
8. Before enabling motion, test stop, watchdog, open cable, and restart with
   safe loads and explicit local commissioning.
9. Home, level, find true north, and set EL/POL zero. Calibrate sensors and
   document declination and the difference measured with motors on and off.
10. Load TLE data, verify UTC/site, and predict a pass; test tracking without
    the antenna or with a qualified test load before installing it.

## Independence and safety

Disabled or absent RF must not prevent qualified motion control. Do not
replace an invalid sensor reading with zero. Test limits, tracking failure,
position loss, and stop on the bench. POL does not change circular
polarization handedness: the rotor-only module does not provide RHCP/LHCP RF
networks. An app or SBC does not replace a physical stop.
