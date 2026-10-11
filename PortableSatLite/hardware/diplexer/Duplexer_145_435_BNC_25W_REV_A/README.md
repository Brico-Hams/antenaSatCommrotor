DUPLEXER 145 / 435 MHz — BNC — 25 W TARGET — REV A

Architecture
  J1 ANT -> 5th-order Chebyshev LPF -> J2 VHF
  J1 ANT -> 5th-order Chebyshev HPF -> J3 UHF

Filter values are based on the published KI0AG 2m/70cm micro-duplexer:
  LPF: 68 nH, 18 pF, 100 nH, 18 pF, 68 nH
  HPF: 4.7 pF, 16 nH, 3.1 pF, 16 nH, 4.7 pF

Target bands:
  VHF: 144–146 MHz, nominal 145 MHz
  UHF: 430–440 MHz, nominal 435 MHz
  System impedance: 50 ohm
  Power target: 25 W

25 W NOTE
The published KI0AG board was described as a 10 W design. This REV A adapts the
component technology and mechanical construction for a 25 W target, but it is
NOT a laboratory-validated 25 W rating. Verify with a 50-ohm dummy load and VNA.
Start at low power and increase progressively. Check insertion loss, return loss,
and inter-port isolation before connecting radios.

BNC
J1-J3 are specified as TE Connectivity 5415025-1, 50 ohm, 4 GHz, right-angle,
panel-mount, through-hole BNC. The manufacturer explicitly says to use its product
drawing for design activity. The custom footprint in this project is a working
prototype footprint; VERIFY the exact hole pattern against the manufacturer's
drawing before ordering PCBs.

PCB
  80 x 60 mm
  2-layer FR-4, 1.6 mm
  2 oz copper recommended
  Full B.Cu ground plane
  F.Cu ground guard + stitching vias
  Metal enclosure strongly recommended

Tuning
  Measure all 3 ports with a VNA at low power.
  Tune air-core inductors and, if needed, replace C4 by 3.0/3.3 pF or add a tiny
  parallel C0G tuning pad. Do not apply 25 W until the RF response is verified.

Files
  *.kicad_pcb : PCB
  *.kicad_sch : KiCad 8 schematic project record (textual engineering schematic)
  *.sch       : legacy KiCad schematic with actual component symbols; open and
                save in KiCad to convert to a native .kicad_sch.
  fabrication/ : Gerber and Excellon files
