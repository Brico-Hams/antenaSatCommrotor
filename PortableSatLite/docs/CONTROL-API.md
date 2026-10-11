# API HTTP del rotor (usada por `firmware/data/index.html`)
Todas las rutas aceptan GET (y POST); respuestas JSON `{"ok":1}` salvo indicación.

| Ruta | Parámetros | Efecto |
|---|---|---|
| `/api/state` | — | estado completo (hora, GNSS, orientación, rotor, objetivo, Doppler, catálogo) |
| `/api/passes` | — | pases de 24 h con elevación máxima ≥ 10° |
| `/api/track` | `sat` (índice del catálogo) | inicia el seguimiento si hay TLE y referencia de norte |
| `/api/stop` | — | para ambos ejes y cancela el seguimiento |
| `/api/goto` | `az`, `el` | mueve a ejes del rotor |
| `/api/goto_true` | `az`, `el` | apunta a az/el verdaderos (409 si no hay referencia de norte) |
| `/api/home` | — | busca finales de carrera EL y AZ (bloquea hasta 90 s por eje) |
| `/api/location`, `/api/location_gps` | `lat`,`lon`,`alt` | posición manual / volver a GNSS |
| `/api/decl` | `deg` | declinación magnética (E positivo) |
| `/api/north` | `deg` o `auto` | norte manual (az verdadero del cero del rotor) / brújula |
| `/api/time` | `unix` | hora del móvil |
| `/api/compass_cal` | `op=start|end` | calibración hard-iron |
| `/api/wifi` | `ssid`,`pass` | credenciales del hotspot para TLE |
| `/api/tle_update` | — | descarga CelesTrak + AMSAT + PE0SAT (texto con el resultado) |
| `/api/tle_upload` | cuerpo POST | TLE pegados a mano |

El mismo contrato lo implementa `tests/mock_server.py`, que se usa para probar la interfaz sin hardware.
