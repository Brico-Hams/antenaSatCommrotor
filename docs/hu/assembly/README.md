# Illusztrált összeszerelési útmutató

Aktualis spanyol kiegeszitesek:
[alkatreszkatalogus](../../assembly/components/README.md),
[szoftvertelepites](../../assembly/06-instalacion.md),
[projektellenorzes](../../PROJECT-REVIEW.md).
A korabbi magyar lepesek meg nincsenek szinkronizalva ezzel a bovitessel.

Minden ábra tartalmazza a BricoHams-logót, a címblokkot és a szerzőket (Anatol EA5KAO, Diego EA5JEF, Pedro Roca Molina). A `scripts/make_assembly_figs.py` állítja elő őket az OpenSCAD-modellekből (`cad/`) és a Gerber-fájlokból, így nem térhetnek el a tervtől. Az ábrák szövege magyar (`*.hu.svg`); a spanyol és angol változat ugyanabban a mappában van.

> **Állapot:** digitális prototípus, **fizikailag nem validált**. Az ábrák összeszerelési segédletek, nem megmunkálási rajzok és nem gyártási tűkiosztások. A jelenlegi BASE forgató a **GT2 szíjas** kialakítás (`cad/belt_station.scad`); a bolygókerekes (`cad/station.scad`) ÖRÖKÖLT (LEGACY).

## Külön összeszerelés (minden modul független)
| Modul | Útmutató | Ábrák |
|---|---|---|
| AZ/EL forgató (+ POL) | [01-rotor.md](01-rotor.md) | R1-R6 |
| V/U antenna | [02-antena.md](02-antena.md) | A1-A2 |
| Dobozok és rádiótartó | [03-cajas.md](03-cajas.md) | C1 |
| Elektronika és kábelezés | [04-electronica.md](04-electronica.md) | E1-E3 |

## Közös összeszerelés
[05-integracion.md](05-integracion.md): a már elfogadott modulok egyesítése (I1, I2). Kiegészíti a [MODULE-INTEGRATED.md](../MODULE-INTEGRATED.md) fájlt.
