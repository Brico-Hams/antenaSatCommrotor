# Riesgos y mitigaciones
| Riesgo | Gravedad | Mitigación / estado |
|---|---|---|
| Firmware sin compilar en ESP32 | alta (bloquea) | `docs/TESTING.md` paso 2; lógica crítica ya probada en PC |
| Diente de la etapa 2 con SF 1,1 a rotor parado | alta | limitar corriente al 50–60 % (SF 1,8–2,1); si se rompe, perfil +0,3 o ancho de cara 20 mm |
| Retroconducción por viento con el rotor sin energía | media | mantener energizado, lastrar, bajar la antena con > 10 m/s |
| Brújula inútil junto a motores | media | pod remoto en la base o norte manual |
| Híbrido que no cubra 145 y 435 MHz | media | verificar hoja de datos antes de comprar (ADR-004) |
| Desfase/ROE reales distintos del modelo | media | ajuste con NanoVNA; transformadores medidos con VF real |
| TLE falsos por HTTPS sin validar | baja | checksum + fuentes múltiples; usar un hotspot propio |
| La API web sin autenticación | baja | contraseña WPA2 del AP (`config.h`: cámbiala) |
| Diplexor de 25 W no validado en laboratorio | baja a 5 W | VNA y carga de 50 Ω antes de transmitir |
| Plegado: varillas de aluminio afiladas/ojos | media | puntas romas, protectores en los extremos |
