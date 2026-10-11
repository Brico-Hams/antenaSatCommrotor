# ADR-002: La radio (RT3S + OpenGD77) es independiente: el rotor no la controla

**Estado:** Aceptada

## Contexto
OpenGD77 no ofrece CAT/PTT por cable que se pueda dar por supuesto (la documentación del propio proyecto previo marca la subida de keps y el CAT como "experimental / sin verificar"). Una conexión automática de PTT desde un microcontrolador a una radio que transmite es un riesgo de seguridad y de normativa.

## Decisión
El rotor **solo muestra** las frecuencias de bajada/subida corregidas por Doppler (calculadas con la velocidad de rango de SGP4) y el operador las sintoniza, o compara con la pantalla de la radio. Nunca activa PTT.

## Justificación y evidencia
Doppler: f_rx = f0·(1 − ṙ/c), f_tx = f0·(1 + ṙ/c) (`satcore.h`). Con ṙ típico ±7 km/s el desplazamiento es ≈ ±3,5 kHz en 145 MHz y ±10,5 kHz en 435 MHz (ṙ máximo ≈ 7,2 km/s para un LEO a 400 km en el horizonte): se corrige a mano o con la función de satélite de la radio. Se evita el acoplamiento y el riesgo.

## Consecuencias y límites
El operador debe mantener hora y posición coherentes entre radio y rotor (ambos pueden usar GNSS).
