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
| `/api/key` | `key` (16+ caracteres) | clave para la Wi-Fi de casa; **solo desde el punto de acceso** del ESP32 |

## Acceso desde la Wi-Fi de casa (STA)
Las peticiones que llegan por el punto de acceso «SatLite-XXXX» no piden clave (uso en campo con el móvil).
Las que llegan por la Wi-Fi de casa exigen el parámetro `key` en **todas** las rutas `/api/`; mejor en el
cuerpo de un POST (`application/x-www-form-urlencoded`) que en la URL. Sin clave puesta, por la red de casa
se responde 403. La clave y el norte manual (`/api/north`) se guardan en la NVS y sobreviven al reinicio.
Sin MPU6050, con norte manual se supone la base nivelada (instalación fija).

El servicio `bricohams-rotor` del kit SDR (manual 49 de bricohams-sdr) usa `/api/goto_true` así para
seguir los pases que graba `bricohams-satrec`.

El mismo contrato lo implementa `tests/mock_server.py`, que se usa para probar la interfaz sin hardware.
