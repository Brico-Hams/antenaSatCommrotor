# Liability and educational-use notice

PortableSatStation is an **experimental engineering prototype**. It is not a
certified product, toy, safety device, emergency communications system, or
commercial SATCOM terminal. It is provided without warranty, subject to
applicable licenses and to the extent permitted by law. This notice does not
exclude rights or liabilities that cannot legally be excluded.

## Validation status

Calculations, software tests, compilation, and mesh checks do not demonstrate
electrical/mechanical safety, load capacity, waterproofing, wind resistance,
VSWR, gain, RF isolation, or real tracking accuracy. Consult
[VALIDATION.md](VALIDATION.md) and pass the gates in
[ACCEPTANCE.md](ACCEPTANCE.md).

An exported Gerber is not a reviewed or tested circuit board. Do not send it
for manufacture without checking footprints, connections, design rules,
current, dissipation, protection, and the assembled design. Flashing firmware
does not validate the hardware to which it is connected.

## Radio and regulations

Transmit only with the applicable authorization/license, bands, power, and
legal conditions, and follow the satellite operator's instructions. References
to commercial or military equipment do not authorize its use or access to its
systems. Do not transmit with RF networks that have not been measured.
An RT3S half-duplex radio does not become full-duplex by adding a diplexer.

## Movement, power, and fabrication

Disconnect power before assembly, folding, changing cables, or changing
drivers. Keep a physical stop independent of the browser/firmware and keep
people outside the movement envelope. Do not use motors to hold an unsafe load
after power loss. Validate the tripod, restraints, balance, and limits.

Use protected commercial supplies/batteries and suitable chargers. Do not
improvise battery packs or bypass fuses/protection. Do not connect motors/RF
during first boot or flashing. ASA printing, machining, and soldering require
appropriate equipment, ventilation, and protection as specified by their
manufacturers.

## Children and adolescents

Educational use associated with [Bricohams](https://bricohams.org) must be
supervised by a competent adult. Prioritize simulations and reception.
Minors must not access moving parts, tools, soldering, batteries, energized
circuits, or transmitters without supervision. Do not publish minors'
personal locations, credentials, or identifying data in the repository,
flashing website, or shared logs.

## Third parties, marks, and data

Cited marks and authors retain their rights. No endorsement, sponsorship, or
collaboration with original authors is implied. TLEs and external services
may fail or be outdated. Check epoch and validity; do not use them for
critical decisions.

Current authors are **Anatol EA5KAO, Diego EA5JEF, and Pedro Roca Molina**.
Earlier work and dependencies are attributed separately.
