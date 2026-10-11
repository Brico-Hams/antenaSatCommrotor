# ADR-005: Elementos: varilla de aluminio de 3 mm; boom de PVC; plegado con bisagras impresas

**Estado:** Aceptada

## Contexto
Presupuesto bajo, transportable en montaña. El artículo usa varilla de 1/8" o "arrow blanks" y boom no conductor para no corregir longitudes.

## Decisión
Varilla de aluminio de 3 mm (soldadura/brazing), boom de conduit PVC de 16 mm en 2 tramos, brazos giratorios `hinge_arm` + bridas `cross_hub_16` impresas en ASA.

## Justificación y evidencia
Masa de varillas calculada = 162 g; el boom de PVC no distorsiona el modelo NEC (que no lo incluye, como en el artículo). El carbono **no** vale: es conductor.

## Consecuencias y límites
Las bisagras impresas son una primera iteración sin probar; el contacto del elemento activo (partido) requiere terminales soldados/atornillados con alivio.
