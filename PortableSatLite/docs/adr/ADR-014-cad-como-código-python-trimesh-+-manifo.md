# ADR-014: CAD como código Python (trimesh + manifold3d) en lugar de OpenSCAD

**Estado:** Aceptada

## Contexto
El entorno de trabajo no tenía OpenSCAD ni acceso a apt.

## Decisión
`cad/gears.py` y `cad/build_all.py` generan los STL y `cad/parts.json` (volumen, caja, estanqueidad, masa).

## Justificación y evidencia
Permitió **verificar** el engrane con intersecciones booleanas y obtener masas reales del modelo. Todas las piezas salen estancas (watertight).

## Consecuencias y límites
Menos legible para quien solo conozca OpenSCAD; los parámetros están arriba de `build_all.py`.
