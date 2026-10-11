# ADR-006: Reductor planetario herringbone 5:1 × 5:1 con ASA (según especificación del usuario)

**Estado:** Aceptada con límite

## Contexto
El usuario pide planetario NEMA17, módulo 1,5–2,5, 20°, espina de pescado, ASA; el diseño previo fue "demasiado pesado". La alternativa (correa GT2 25:1) aparece en el repo anterior como la variante ligera.

## Decisión
Un planetario compacto de dos etapas (Zs 12 / Zp 18 / Zr 48, m = 1,5, hélice 25°) con carcasa de una pieza, 3 planetas por etapa y rodamiento de salida 6806.

## Justificación y evidencia
Geometría verificada por interferencia booleana (sol–planeta 0 mm³ en fase; planeta–corona mínimo ≈68 mm³, abierto). Pares y tensiones en `calc/rotor_calc.py`: SF 4,8 (etapa 1) y 1,1 (etapa 2) a rotor parado con 0,25 N·m; con la corriente del driver limitada al 50–60 % el SF de la etapa 2 sube a 1,8–2,1 y aún hay 2,5–3 N·m de par de salida frente a 0,7–1,1 N·m de viento a 10 m/s.

## Consecuencias y límites
No se cuantificó la diferencia de masa frente a la correa GT2 (carcasa ≈ 68 g por eje, motor ≈ 220 g supuestos). Es retroconducible sin corriente. Se queda la opción GT2 como alternativa documentada pero no implementada aquí.
