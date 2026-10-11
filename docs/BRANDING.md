# Marca BricoHams en PCB y piezas impresas

Fuente: `branding/bricohams_horizontal.png` (logo BH + "bricohams"). Se vectoriza con
`scripts/make_logo_assets.py` a polígonos monocolor (`branding/bricohams_polys.json`) y al
módulo OpenSCAD `cad/bricohams_logo.scad` (generado; no editar a mano). El eslogan y los
puntos se omiten (detalles < 0,3 mm).

## PCB (serigrafía superior, `F.SilkS`)
`scripts/add_logo_pcb.py` rasteriza los Gerber, busca el hueco más despejado (lejos de pads/aperturas
de máscara, taladros, serigrafía existente y borde) y añade el logo como regiones Gerber
(G36/G37, LPD/LPC) **y** como triángulos `gr_poly` en el `.kicad_pcb` para que un nuevo trazado de KiCad lo conserve.

| Placa | Posición (mm, coords. Gerber) | Tamaño | Holgura al elemento más cercano |
| --- | --- | --- | --- |
| PortableSatCarrier (ESP32) | X 102,5 / Y −126,2 | 40 × 12,2 | 8,3 mm |
| cm5-guard-A | X 243,5 / Y −239,7 | 50 × 15,3 | 21,9 mm |

Se actualizaron los SHA-256 (`fabrication/release-status.json`, `hardware/cm5/reports/manifest-sha256.json`)
y el ZIP de Gerbers del carrier. **Límites:** KiCad no estaba disponible, por lo que **no se repitieron ERC/DRC ni se
regeneraron los Gerbers desde KiCad**; los Gerbers se parchearon directamente y se comprobaron releyéndolos con
gerbonara. La serigrafía no altera cobre, pero el fabricante debe revisar la vista previa. Las placas
siguen sin autorización de fabricación (ver VALIDATION.md).

## Piezas impresas (relieve de 0,6 mm)
Tapas `enclosure_lid`, `diplexor_lid`, cuna `radio_cradle` (pared trasera, cara exterior) y tapa del `carrier`.
Solapamiento de 0,05 mm para que ninguna isla quede flotando; mallas estancas verificadas con trimesh.
No se tocaron los engranajes ni piezas estructurales.
