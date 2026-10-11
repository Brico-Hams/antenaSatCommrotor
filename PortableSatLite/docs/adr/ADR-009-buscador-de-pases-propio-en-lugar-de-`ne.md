# ADR-009: Buscador de pases propio en lugar de `nextpass()` de la librería

**Estado:** Aceptada

## Contexto
`Sgp4::nextpass()` avanza una órbita cada vez y busca el máximo local.

## Decisión
Barrido cada 30 s sobre 24 h y bisección de AOS/LOS a 1 s (`tracker.h::find_passes`).

## Justificación y evidencia
Prueba con ISS (36 h): la librería devolvió 6 pases y **omitió** los de 18°, 11° y 14,6° de elevación máxima; el buscador propio encontró los 6 de referencia con error ≤ 9 s y ≤ 0,34° en elevación máxima (`tests/test_tracker.py`).

## Consecuencias y límites
Coste de CPU (≈ 2900 evaluaciones/satélite/24 h) → corre en una tarea de baja prioridad en el otro núcleo y se recalcula cada 10 min.
