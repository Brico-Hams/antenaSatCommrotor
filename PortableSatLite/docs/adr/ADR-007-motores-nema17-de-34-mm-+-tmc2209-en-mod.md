# ADR-007: Motores NEMA17 de 34 mm + TMC2209 en modo STEP/DIR, corriente limitada

**Estado:** Aceptada

## Contexto
Par suficiente (0,2–0,3 N·m de mantenimiento) y componentes baratos y comunes. Un NEMA23 sería innecesariamente pesado con 25:1.

## Decisión
Dos NEMA17 y dos drivers TMC2209 (STEP/DIR); corriente de funcionamiento al 50–60 % de la nominal; generación de pulsos con FastAccelStepper (hardware, sin jitter por Wi-Fi).

## Justificación y evidencia
Resolución 0,0045°/micropaso, 222 micropasos/s por °/s: el seguimiento necesita ≈ 1–5 °/s (1 100 micropasos/s), muy por debajo del límite del hardware.

## Consecuencias y límites
El firmware no lee todavía los AS5600 (están previstos en el cableado para detectar pasos perdidos); el rotor es lazo abierto con homing a finales de carrera.
