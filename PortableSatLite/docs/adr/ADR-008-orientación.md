# ADR-008: Orientación: GNSS (posición/hora) + acelerómetro (inclinación) + magnetómetro o norte manual

**Estado:** Aceptada

## Contexto
El usuario exige que la unidad conozca su ubicación, orientación y elevación para afinar el apuntado. Un GNSS parado no da rumbo.

## Decisión
GNSS NMEA para lat/lon/alt/UTC; MPU6050 para la vertical; QMC5883L para el rumbo compensado por inclinación, con declinación configurable; alternativa de **norte manual** (azimut verdadero del cero del rotor) y hora/posición manuales desde el móvil si no hay GNSS. Si no hay referencia de norte válida el seguimiento se **inhibe** (no se supone 0).

## Justificación y evidencia
La matemática (`satcore.h`) se comparó con un modelo independiente de matrices de rotación sobre 2000 casos aleatorios de inclinación (hasta ±20°), rumbo y declinación: error < 2·10⁻⁶ ° (limitado por la precisión del texto de entrada), ida y vuelta 5·10⁻¹⁰ °. Esto corrige el error que produce una base inclinada: sin compensar, una inclinación de 5° puede desplazar el apuntado hasta 5°.

## Consecuencias y límites
El magnetómetro debe ir lejos de motores/acero (pod en la base del trípode) y se calibra con la estación completa (hard-iron min/max girando la base). La calibración soft-iron no está implementada.
