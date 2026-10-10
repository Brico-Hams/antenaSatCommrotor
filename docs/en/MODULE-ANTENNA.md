# Standalone module: portable 145/435 MHz antenna

## Scope and dependencies

The antenna can be built without the rotor, CM5, SDR, battery, or app.
A hand-held mount/tripod and an external radio with compatible interfaces
allow it to operate separately. No commercial SATCOM performance or
measured gain/polarization is claimed.

| Required | Optional |
| --- | --- |
| ASA parts, conductors for both bands, boom/supports, metal fasteners, and 50-ohm SMA coax | AZ/EL/POL rotor |
| Strain-relieved cables, checked connectors, and a verified hand-held mount | Integrated SDR radio |
| Instruments/loads for RF tuning and testing | Diplexer, circular networks, and RHCP/LHCP switching after qualification |

Geometry and materials: [MECHANICAL.md](MECHANICAL.md),
[RF-AND-RADIO.md](RF-AND-RADIO.md), [CAD](../../cad/), and the
[mechanical BOM](../../bom/mechanical.csv). Do not add the complete rotor BOM
to the antenna cost; select only this module's parts. Dated prices and
pending categories are in [REFERENCE-PRICES.md](REFERENCE-PRICES.md) and
[reference-prices.csv](../../bom/reference-prices.csv). For the antenna-only
build, use ASA, RF-INTERCONNECT, RF-FILTER if applicable, HARDWARE fasteners,
and consumables: do not buy the CM5/SDRs/motors just because you follow this
path. The consumed ASA quantity and the conductors/coax need quotes and
reconciliation against the actual parts; there is no closed total.

## Standalone assembly, step by step

1. Check authorized bands/frequencies, CAD revisions, and conductor
   dimensions. Calculated lengths are initial tuning values.
2. Print ASA parts and inspect for cracks, cavities, and fit; conductors,
   shafts, fasteners, and load-bearing threads must be metal.
3. Assemble the boom, supports, and removable VHF/UHF elements according to
   the [mechanical guide](MECHANICAL.md). Do not cut every element to its
   minimum length before testing the prototype.
4. Prepare a feed for each band, conventional 50-ohm SMA cables, mounting,
   and strain relief. Verify center contact and connector gender; do not use
   RP-SMA.
5. Test manual folding and assembly without pulling on coax or using
   connectors as supports. Record the assembled antenna's mass and center
   of gravity (CG).
6. Tune/measure each band with a VNA and then the complete assembly, with
   unused ports properly terminated. Record SWR and coupling.
7. If circular polarization is added, install the per-band networks and
   measure phase, amplitude, handedness, and axial ratio. Mechanical
   rotation does not select RHCP/LHCP.
8. Connect an external radio only after testing, start at minimum power,
   and check temperature/SWR; do not test TX without a suitable load.

## Configuration and acceptance

The antenna alone requires no software. Before transmitting, document
frequency, mode, circular handedness if applicable, cabling, and measured
limits. [ACCEPTANCE.md](ACCEPTANCE.md) defines the RF/mechanical gates; a
correct STL does not prove gain, SWR, or wind resistance. The rotor interface
is removable and is not required for operation.
