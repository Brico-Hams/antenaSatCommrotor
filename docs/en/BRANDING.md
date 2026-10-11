# BricoHams branding on PCBs and printed parts

Source: `branding/bricohams_horizontal.png` (BH logo + "bricohams"). It is vectorised by
`scripts/make_logo_assets.py` into monochrome polygons (`branding/bricohams_polys.json`) and into the
OpenSCAD module `cad/bricohams_logo.scad` (generated; do not edit by hand). The tagline and the
dots are omitted (details < 0.3 mm).

## PCB (top silkscreen, `F.SilkS`)
`scripts/add_logo_pcb.py` rasterises the Gerbers, finds the most open spot (away from pads/solder-mask
openings, drills, existing silkscreen and the board edge) and adds the logo as Gerber regions
(G36/G37, LPD/LPC) **and** as `gr_poly` triangles in the `.kicad_pcb`, so a new KiCad plot keeps it.

| Board | Position (mm, Gerber coords) | Size | Clearance to nearest feature |
| --- | --- | --- | --- |
| PortableSatCarrier (ESP32) | X 102.5 / Y −126.2 | 40 × 12.2 | 8.3 mm |
| cm5-guard-A | X 243.5 / Y −239.7 | 50 × 15.3 | 21.9 mm |

The SHA-256 values (`fabrication/release-status.json`, `hardware/cm5/reports/manifest-sha256.json`)
and the carrier Gerber ZIP were updated. **Limits:** KiCad was not available, so **ERC/DRC were not
re-run and the Gerbers were not regenerated from KiCad**; the Gerbers were patched directly and checked by
re-reading them with gerbonara. Silkscreen does not alter copper, but the manufacturer must review the
preview. The boards remain without fabrication authorisation (see VALIDATION.md).

## Printed parts (0.6 mm relief)
Lids `enclosure_lid`, `diplexor_lid`, cradle `radio_cradle` (back wall, outer face) and the `carrier` lid.
0.05 mm overlap so no island floats; watertight meshes verified with trimesh.
Gears and structural parts were not touched.

## Illustrations
Assembly figures carry the logo, a title block and the authors line
(Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina · bricohams.org); see
[assembly guide](assembly/README.md). Legacy diagrams were branded with `scripts/brand_svgs.py`.
