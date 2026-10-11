# ADR-010: Interfaz web sin dependencias, en punto de acceso propio (AP+STA), bilingüe

**Estado:** Aceptada

## Contexto
El usuario pide una web servida por el rotor para descargar pases desde un AP en el campo.

## Decisión
AP `SatLite-XXXX` (contraseña configurable en `config.h`), servidor HTTP del propio ESP32, una sola página sin CDN (funciona sin Internet), ES/EN. El modo STA (hotspot del móvil) sirve para bajar los TLE.

## Justificación y evidencia
Probada contra un servidor simulado con los mismos endpoints (`tests/test_webui.py`): carga sin errores, lista pases, inicia el seguimiento, sin desbordamiento horizontal a 390 px.

## Consecuencias y límites
La API no tiene autenticación más allá de la contraseña del AP: cualquiera con la contraseña mueve el rotor (no puede transmitir). No se ha probado en el ESP32 real.
