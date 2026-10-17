# Guia ilustrada de ensamblaje

Idiomas: [English](../en/assembly/README.md) · [Magyar](../hu/assembly/README.md). Las figuras en inglés y húngaro están en `fig/*.en.svg` y `fig/*.hu.svg`.

Las figuras R/A/C/E/I llevan el logo BricoHams, el bloque de titulo y los
autores (Anatol EA5KAO, Diego EA5JEF, Pedro Roca Molina). Se generan con
`scripts/make_assembly_figs.py` desde OpenSCAD y Gerber. Son instantaneas:
hay que regenerarlas al cambiar los fuentes; su existencia no demuestra
que correspondan automaticamente a la ultima revision.

El [catalogo visual de componentes](components/README.md) aporta una ficha
SVG por fila de las doce BOM de mecanica, electricidad, RF, PCB, conjunto,
POL, auxiliar CM5, PortableSatLite, PF-01, Eggbeater, QFH y previos.
Son pictogramas de identificacion
con especificacion y procedencia, no renders ni geometria inventada.

> **Estado:** prototipo digital, **no validado fisicamente**. Las figuras son ayudas de montaje, no planos de mecanizado ni pinouts de fabricacion. El rotor BASE vigente es el de **correa GT2** (`cad/belt_station.scad`); el planetario (`cad/station.scad`) es LEGACY.

## Montaje por separado (cada modulo es independiente)
| Modulo | Guia | Figuras |
|---|---|---|
| Rotor AZ/EL (+ POL) | [01-rotor.md](01-rotor.md) | R1-R6 |
| Antena V/U | [02-antena.md](02-antena.md) | A1-A2 |
| Antena portable PF-01 (nueva candidata) | [Diseno y montaje PF-01](../ANTENNA-PORTABLE.md) | PF-deployed/front/folded/hinge |
| Eggbeater TX/RX por banda | [Montaje Eggbeater](../ANTENNA-EGGBEATER.md) | EB-145/435 iso/front y CAD |
| QFH TX/RX por banda | [Montaje QFH](../ANTENNA-QFH.md) | QFH-145/435 iso/front y CAD |
| Previo solo RX y bypass TX | [Montaje y proteccion](../ANTENNA-PREAMPS.md) | Rutas RF y secuencia de montaje |
| Cajas y soporte de radio | [03-cajas.md](03-cajas.md) | C1 |
| Electronica y cableado | [04-electronica.md](04-electronica.md) | E1-E3 |

## Montaje colectivo
[Elegir alternativa](../ANTENNA-OPTIONS.md) antes de sumar materiales;
no montar las tres antenas como un unico conjunto ni duplicar kits RF.
Ver [canales AMSAT y techo 25 W](../SATELLITE-COMMS.md).

[05-integracion.md](05-integracion.md): union de los modulos ya aceptados (I1, I2). Complementa [MODULE-INTEGRATED.md](../MODULE-INTEGRATED.md) y [ASSEMBLY-MULTIMODE.md](../ASSEMBLY-MULTIMODE.md).

## Instalacion y configuracion

[06-instalacion.md](06-instalacion.md): elegir variante, validar fuentes,
preparar ESP32, CM5/OS y Android, y pasar al banco sin activar funciones
no comisionadas. Ver tambien la [revision de cobertura](../PROJECT-REVIEW.md).
Las ampliaciones de esta revision estan en espanol; los enlaces de idiomas
no implican que sus guias antiguas ya esten sincronizadas.

## Regenerar las figuras

Catalogo de componentes sin dependencias, en Windows:

```powershell
node scripts\component-catalog.cjs
node scripts\component-catalog.cjs --check
```

Despieces existentes, en un entorno con sus dependencias instaladas:

```
python3 scripts/make_assembly_figs.py   # figuras nuevas (requiere openscad, xvfb, gerbonara, cairosvg)
python3 scripts/brand_svgs.py           # marca los diagramas existentes (idempotente)
```

La nueva validacion detecta fichas no regeneradas y enlaces rotos. No
reexporta STL, no cambia Gerbers ni autoriza fabricar las placas.
