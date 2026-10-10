# Transport and field operation manual

## Modules to transport

- Antenna: removable boom, radiators and reflectors, RF networks, and coax.
- Rotor: AZ/EL and saddle without radio or antenna.
- Control: ESP32, GNSS, power, stop, and removable RF module.
- RT3S radio with its own battery and removable mount.
- Photographic tripod and metal adapter.

Do not use cables as handles. Protect RF joint threads and contacts. The
<=450 mm packed-length target requires disassembling long sections: a
475.5 mm VHF arm cannot magically fit by folding without being split.

## Assembly

With power disconnected, open the tripod on stable ground and verify metal
attachment and secondary retention. Do not assume that a camera's stated
vertical capacity authorizes lateral torque. Fit the rotor, connect limits,
motors, and sensors; use strain relief.

Deploy the antenna with positive locks and metal contacts; balance EL with
its final coax installed. Do not hang the RT3S or battery enclosure from the
boom tip. Keep people outside the rotation envelope.

## Position, UTC, level, and north

A GNSS fix gives position, not the orientation of a stationary tripod. Level
the base and determine true north from a known reference. If using a compass,
correct for declination using a current source and keep it away from motors,
shafts, and magnets; confirm deviation after assembling the complete station.

Do not enter local time as UTC. Record altitude and units; at a mountain site,
observer elevation and horizon obstructions are separate considerations.
Homing calibrates only the mechanical axis.

## TLE in the field

Update before departure; keep the cache and a manual copy. At the site:

- AP allows a local browser but does not provide Internet.
- With STA/hotspot available, download from a permitted provider.
- Without Internet, import a TLE with a recent epoch and confirm the satellite.
- Check the epoch's actual age, not only the download time.

Do not treat TLEs as a frequency list. Confirm the active transponder, mode,
and frequencies from current satellite-operator sources.

## During a pass

Confirm the radio is set to the correct satellite, UTC/site agree, and tracking
is armed. Verify that the pass is reachable within controller AZ/EL limits,
speed, and zenith exclusion.

OpenGD77 can manage its own satellite operation according to model/version;
follow the manual for the installed version. CAT is not promised. An RT3S in
half-duplex cannot hear the downlink while transmitting.

The web interface is not a physical emergency stop: keep the hardware stop
accessible. If there is wind, erratic motion, new RX noise, or a loose
connector, stop and diagnose; do not force tracking.

## Disassembly

Stop, confirm motors are still, disconnect power, unload EL, and remove the
antenna. Remove the radio/RF module for independent use. Do not fold dipoles
or disengage planetary gears while motors are enabled. Store dry; do not
infer waterproofing from an ASA enclosure.

## Independent use

The antenna can be used with a manual mount and its RF network. The rotor can
use another antenna within the verified load envelope. The diplexer can be
connected externally without the control enclosure. The RT3S continues to
work on its own battery outside the mount.
