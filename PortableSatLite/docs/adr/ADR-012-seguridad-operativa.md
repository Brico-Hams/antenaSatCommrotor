# ADR-012: Seguridad operativa: el rotor no transmite, finales de carrera NC, parada, límite de viento

**Estado:** Aceptada

## Contexto
Motores en exteriores, personas cerca, radio de 5 W en la misma estructura.

## Decisión
Sin salida de PTT; finales de carrera normalmente cerrados (un cable roto cuenta como pulsado); botón PARAR en la web; límites AZ 0–450°, EL 0–180°; viento máximo recomendado 10 m/s.

## Justificación y evidencia
Cálculo de viento y tensión de dientes (ADR-006).

## Consecuencias y límites
No hay parada mecánica ni parada física de hardware independiente del ESP32; añadir un interruptor de corte de la alimentación de motores en el panel (pendiente).
