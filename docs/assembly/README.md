# Guia ilustrada de ensamblaje

Todas las figuras llevan el logo BricoHams, el bloque de titulo y los autores (Anatol EA5KAO, Diego EA5JEF, Pedro Roca Molina). Se generan con `scripts/make_assembly_figs.py` desde los modelos OpenSCAD (`cad/`) y los Gerber, de modo que no divergen del diseno.

> **Estado:** prototipo digital, **no validado fisicamente**. Las figuras son ayudas de montaje, no planos de mecanizado ni pinouts de fabricacion. El rotor BASE vigente es el de **correa GT2** (`cad/belt_station.scad`); el planetario (`cad/station.scad`) es LEGACY.

## Montaje por separado (cada modulo es independiente)
| Modulo | Guia | Figuras |
|---|---|---|
| Rotor AZ/EL (+ POL) | [01-rotor.md](01-rotor.md) | R1-R6 |
| Antena V/U | [02-antena.md](02-antena.md) | A1-A2 |
| Cajas y soporte de radio | [03-cajas.md](03-cajas.md) | C1 |
| Electronica y cableado | [04-electronica.md](04-electronica.md) | E1-E3 |

## Montaje colectivo
[05-integracion.md](05-integracion.md): union de los modulos ya aceptados (I1, I2). Complementa [MODULE-INTEGRATED.md](../MODULE-INTEGRATED.md) y [ASSEMBLY-MULTIMODE.md](../ASSEMBLY-MULTIMODE.md).

## Regenerar las figuras
```
python3 scripts/make_assembly_figs.py   # figuras nuevas (requiere openscad, xvfb, gerbonara, cairosvg)
python3 scripts/brand_svgs.py           # marca los diagramas existentes (idempotente)
```
