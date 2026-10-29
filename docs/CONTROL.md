# Control autónomo — prototipo ESP32

Proyecto original de Anatol (EA5KAO), Diego (EA5JEF) y Pedro Roca Molina,
contexto educativo Bricohams (`https://bricohams.org`). Consulte AUTHORS,
ACKNOWLEDGEMENTS y DISCLAIMER del proyecto para atribución y límites.
Referencias y dependencias conservan sus propios autores; no se implica respaldo.
Niños/adolescentes requieren supervisión adulta y no deben transmitir sin
autorización/licencia aplicable.

## Alcance y estado

El ESP32 calcula **SGP4 real**, no una aproximación Kepler, a partir de TLE
guardados en LittleFS. GNSS NMEA proporciona UTC y ubicación; el navegador
solamente presenta y envía órdenes. No hay servidor Node, nube ni ordenador
necesarios en campo. La antena dual 145/435 MHz comparte el apuntado.
PTT/CAT **deshabilitados**: no se supone que RT3S opere full dúplex ni tenga CAT.
Configure OpenGD77 y sus canales/Doppler independientemente; los desplazamientos
mostrados usan 145 y 435 MHz nominales, no sustituyen el plan de frecuencias.

Es un prototipo compilado y probado por software, **no validado en campo**.
No se han ensayado motores, GNSS, RF, TLS con los tres servidores, encoders,
latencias bajo tráfico hostil, ni un procedimiento de seguridad certificado.
No es una parada de emergencia funcionalmente certificada.

El control no autoriza ninguna carga/viento de campo. El ejemplo mecánico
de 8 m/s, área 0.06 m² y brazo 0.25 m **no cumple** el margen de seguridad
del cálculo de diseño comunicado; no debe tratarse como límite operativo.
La configuración de 80 000 microsteps/vuelta presupone la reductora efectiva
25:1: confirme ambas etapas, interfaces chaveteadas y relación real en banco.
La masa, equilibrado de la antena y rigidez de piezas ASA requieren medición;
una malla STL o compilación correcta no prueba capacidad mecánica.

Archivos propios:

* `firmware/platformio.ini`, `firmware/include/board_config.h`
* `firmware/include/control_logic.h`, `firmware/src/main.cpp`
* `firmware/include/ble_protocol.h` (framing y autenticación compartida)
* `firmware/.gitignore` (excluye herramientas/builds locales)
* `web/index.html` (interfaz española íntegramente offline)
* `tests/control_logic/test_native/test_main.cpp`
* `tests/control_sgp4.cpp`, `tests/control_web.test.cjs`
* este documento

## Dependencias verificadas y compilación

PlatformIO Core 6.1.18; `espressif32@6.10.0`, `esp32dev` (ESP32 clásico,
WROOM, 4 MB flash), Arduino ESP32 **2.0.17**, paquete
`framework-arduinoespressif32@3.20017.241212`, Xtensa
`8.4.0+2021r2-patch5`; ArduinoJson 6.21.5; TinyGPSPlus 1.1.0.
Bluetooth: **h2zero/NimBLE-Arduino 1.4.3**, licencia raíz Apache-2.0 verificada
en `https://github.com/h2zero/NimBLE-Arduino/blob/1.4.3/LICENSE`. Conserve su
licencia, avisos y los del stack Apache NimBLE al distribuir binarios.
No se usa Bluetooth clásico ni Bluedroid; una conexión BLE máxima.

SGP4: [Hopperpop/Sgp4-Library](https://github.com/Hopperpop/Sgp4-Library)
1.0.3, commit **7c82d31f9d9a286acde5ef55da8308fc93d2ba96**.
Se comprobaron las firmas reales de `Sgp4::init`, `site`, `findsat`,
`satrec.error`, y el cálculo TEME→observador del código fuente fijado.
El wrapper upstream selecciona WGS84; se inicializan explícitamente sus buffers
internos y se pasan copias mutables de las líneas. El ensayo independiente
utiliza WGS72 para comparar con el vector de verificación Vallado 00005:
R=(7022.46529266,-1400.08296755,0.03995155) km,
V=(1.893841015,6.405893759,4.534807250) km/s.
Referencia: [CelesTrak software SGP4](https://celestrak.org/software/vallado-sw.php).
La librería conserva sus avisos/licencias en el gestor de dependencias; no se
vendorizan ni alteran sus fuentes.
Los archivos de software **originales** de este subsistema se publican bajo MIT
según la selección del usuario y el NOTICE del proyecto; el hardware original
bajo CERN-OHL-S-2.0. Esto no atribuye MIT al conjunto de firmware enlazado.
Estas licencias no relicencian bibliotecas, herramientas ni referencias externas:
cada dependencia conserva su propia licencia. No se redistribuyen fuentes de
licencia desconocida ni se ha realizado publicación remota.
Se verificó el archivo `LICENSE` del commit SGP4 fijado: **The MIT License (MIT),
Copyright (c) 2016**, con obligación de conservar aviso de copyright y permiso
en copias o partes sustanciales, también en una distribución del binario que lo
incluya. Evidencia pública:
`https://github.com/Hopperpop/Sgp4-Library/blob/7c82d31f9d9a286acde5ef55da8308fc93d2ba96/LICENSE`.
Su README identifica la transformación de coordenadas de Grady Hillhouse también
como MIT. No se detectó GPL en esta dependencia; otras bibliotecas/Arduino ESP32
y herramientas no quedan relicenciadas por esta comprobación. Antes de distribuir
un binario conserve los avisos de **todas** las dependencias enlazadas y revise
las obligaciones de las versiones concretas del framework.

Con PlatformIO instalado en un entorno de desarrollo:

```powershell
Set-Location .\firmware
pio run -e esp32
pio run -e esp32 -t buildfs
pio run -e esp32 -t upload
pio run -e esp32 -t uploadfs
pio device monitor -b 115200
pio test -e control_native
```

El test nativo necesita GCC/G++ en PATH. En esta máquina faltaban Python utilizable,
PlatformIO y GCC: se descargaron Python embebido 3.11.9, PlatformIO 6.1.18 y
Zig 0.13.0 **únicamente bajo `firmware/.tools`**, sin instalación global.
Los servicios de configuración Python de VS Code no tenían implementación.
El Python embebido requirió esptool 4.5.1 local porque su aislamiento impide
importar el paquete del script externo de PlatformIO.

Pruebas realmente ejecutadas:

* Compilación/enlace ESP32 y generación `firmware.bin`: **SUCCESS**.
* Construcción LittleFS con `index.html`: **SUCCESS**.
* Seis tests Unity compilados/ejecutados con Zig: **6 PASS, 0 fallos**:
  límites/coordenadas, UTC/años bisiestos/caducidad, checksums/epoch TLE,
  límites de velocidad/aceleración/parada/movimiento positivo y negativo,
  validación de credenciales USB y tramas BLE/auth (sin secretos reales).
* Ejecutable contra el SGP4 fijado: vector Vallado epoch **PASS**, tolerancia
  1 m de posición y 1 mm/s de velocidad.
* `node --test tests/control_web.test.cjs`: **PASS** (sintaxis, IDs DOM, ocho acciones
  autenticadas, nombres satelitales renderizados sin HTML y comprobaciones estáticas
  de los interlocks de firmware; no simulan la temporización ni el hardware).
* `pio test -e control_native` inicialmente falló por ausencia de GCC;
  se ejecutó el mismo código Unity con Zig como alternativa, no se presenta
  ese comando como aprobado.

Los binarios en `.pio/build/esp32` son artefactos de desarrollo, no prueba de
flasheo o de funcionamiento físico. Subir LittleFS reemplaza su contenido:
exporte sus TLE antes de actualizar el filesystem.

### Bundle WebFlash/CI (ESP32 clásico únicamente)

CI puede compilar sin `secrets.h`: `board_config.h` contiene credenciales vacías
y `carrierVerified=false`. Esa imagen segura inicia DISARMED, **sin AP operativo**
hasta aprovisionamiento USB local; no requiere recompilar para configurar AP.
No inserte password/token privados en una imagen pública de GitHub Pages.

### Aprovisionamiento USB local (imagen pública)

Desconecte motores/RF. Abra consola serie local 115200 (ESP Web Tools console o
terminal local sin registro/telemetría), envíe cada JSON en una línea terminada LF:

1. `{"cmd":"setup"}`: desconecta Wi-Fi, fuerza ENABLE OFF y fallo de
   provisionamiento, invalida homing/calibración. API queda bloqueada.
2. `{"cmd":"config","ssid":"Nombre elegido","password":"SU_PASSWORD_PRIVADO","token":"SU_TOKEN_ALEATORIO_PRIVADO"}`.
   Sustituya valores: SSID 1..32, password 12..63, token aleatorio 24..128
   caracteres ASCII imprimibles. Opcional `staSsid` y `staPassword` (≥8);
   omitirlos elimina STA guardado. No envíe secretos a servicios remotos ni
   publique el historial de consola.
3. Solo tras validar físicamente placa/driver/polaridades:
   `{"cmd":"carrier","verified":true}`. No inicia ni arma motores.
   `verified:false` revoca autorización de hardware en el siguiente arranque.
4. `{"cmd":"reboot"}`. Arranca DISARMED; conecte al AP seguro configurado y
   abra `http://192.168.4.1`; introduzca token en la página.

Parser máximo 768 bytes/línea; respuestas no repiten secretos. Credenciales
persisten en NVS privado, **no cifrado**: acceso físico al flash puede extraerlas;
este prototipo no configura flash encryption/secure boot. Configuración NVS
no es transacción completa: si falla escritura, permanezca en SETUP y reintente.
No se soporta configurar CA PEM por esta consola; HTTPS exige raíces compiladas
vigentes, mientras importación TLE manual funciona con la imagen pública.
Un operador con acceso USB puede modificar configuración; controle acceso físico.
Homing/calibración nunca se guardan, aun cuando se guarda verificación del carrier.

### Bluetooth LE seguro y Android

La imagen permite AP Wi-Fi y BLE simultáneos; coexistencia y latencias físicas
no están medidas. BLE desactivado de fábrica. En SETUP USB local añada:
`{"cmd":"ble","enabled":true,"passkey":SU_NUMERO_PRIVADO_DE_6_DIGITOS}`.
Use número 100000..999999 elegido localmente, no un passkey global de este
documento. No se imprime. `enabled:false` desactiva BLE tras reboot.
Cambiar configuración BLE elimina bonds almacenados al próximo inicio.
La consola sigue forzando motores OFF; luego `{"cmd":"reboot"}`.

Empareje Android usando diálogo del sistema y el passkey privado, **Secure
Connections, bonding y MITM obligatorios**; nunca aceptar un modo inseguro
alternativo. Introduzca además el token de API local en la app. No se envía a
nube. Toda orden, incluso STOP/status, exige enlace cifrado/autenticado/bonded y
token correcto. Radio/NVS no equivalen a secure boot: proteja acceso físico.

Protocolo GATT **v1**, nombre anunciado `PortableSatStation`:

* Servicio: `c8200001-4e53-4253-9000-000000000001`
* RX escritura **con respuesta ATT**, cifrada/autenticada:
  `c8200002-4e53-4253-9000-000000000001`
* TX notificaciones: `c8200003-4e53-4253-9000-000000000001`

Suscriba TX antes de enviar. MTU 23 mínimo funciona, sin depender de negociar
MTU mayor. Cada trama ≤20 bytes: byte0=0x53; byte1 flags START=1, END=2
(3 para trama única); bytes2/3 secuencia uint16 little-endian, inicio0 y +1;
bytes4..19 contienen 1..16 bytes del JSON UTF-8. No NUL ni flags desconocidos.
No se ejecuta una orden hasta recibir END válido, esquema y autenticación.
Petición ≤2048 bytes, timeout de montaje3 s, una petición/respuesta en vuelo.
Fuera de orden/intercalación/overflow produce error, no ejecución parcial.

Petición completa:
`{"v":1,"id":1,"method":"POST","path":"/api/calibrate","token":"TOKEN_PRIVADO","body":{"trueAz":0,"levelConfirmed":true}}`.
ID entero positivo **creciente por conexión**. GET lleva `body:{}`.
Respuesta completa:
`{"v":1,"id":1,"code":200,"data":{"message":"..."}}`.
`data` usa exactamente el objeto JSON del HTTP; errores de framing sin ID
recuperable llevan id0. Respuesta ≤8192 bytes; catálogos mayores retornan413
y deben consultarse/importarse por HTTP. 429 si cola ocupada;408 timeout.
Espere END de respuesta anterior antes de siguiente petición, excepto STOP
autenticado puede priorizarse e interrumpir respuesta anterior.

Mismos handlers/interlocks para `/api/status`, site, home, move, stop, clear,
calibrate, select, track, passes, tle GET/POST. `/api/update` por BLE retorna409:
HTTPS solo HTTP en reposo. TLE por BLE admite subconjunto que quepa en2048bytes,
no truncamiento silencioso. Firmware no copia una segunda lógica de movimiento.
STATUS añade `controlOwner` (HTTP/BLE/none), `bleConfigured`, `bleConnected`,
`bleSecure`, `encoderZeroVerified`.
STATUS identifica compatibilidad con `apiVersion=2`, `protocolVersion=1` y
`firmwareVersion="0.3.0-prototype"`; úselo como handshake autenticado, no existe
una ruta auth separada.

API 2 (integración con la app Android Bricohams) añade `POST /api/time`
(`{"utcMs":...}`, autenticado): sin GNSS, una app de confianza fija la UTC durante
10 min; la UTC GNSS siempre tiene prioridad (409) y se rechazan saltos de más de
2 s con motores activos. STATUS añade `timeSource` (`none`/`gnss`/`app`) y el
perfil mecánico `microsteps`, `transmissionRatio`, `stepsPerDegree` y
`maxDegPerSecond`. El entorno PlatformIO `esp32_nema17` compila el perfil de bajo
coste: NEMA17 reutilizados con TMC2209 a 1/8, mismas correas 25:1, 40000
micropasos/vuelta y 6,0 °/s máximos. Compilado; sin prueba en placa ni rotor.
Mutaciones de otro transporte durante movimiento se rechazan409; STOP autenticado
siempre accesible. Una desconexión
BLE durante HOME/MOVE manual causa fallo e invalida homing; TRACK autónomo
continúa sujeto a GNSS/TLE/interlocks, sin necesitar móvil conectado.

Notificaciones no tienen garantía de entrega: la app debe detectar secuencia/
timeout y volver a consultar status; nunca asumir ejecución por escritura ATT.
E-stop físico y task de seguridad no dependen del teléfono ni del transporte.
Si el plazo motor supera20ms, fallo; no se certifica coexistencia Wi-Fi/BLE.

### Transferencia TLE grande desde Android (mismo protocolo v1)

El móvil descarga HTTPS de los proveedores permitidos y transfiere **TLE**, no
trayectorias: SGP4, pases y seguimiento continúan calculados en el rotor.
El catálogo admite ≤100 satélites/48 kB; seleccione un subconjunto si excede.
No se trunca silenciosamente. Nuevos POST compartidos HTTP/BLE:

| Ruta | Body / resultado |
|---|---|
| `/api/tle/begin` | `{length:1..48000,sha256:"64 hex lowercase"}` → `{message,uploadId}` |
| `/api/tle/chunk` | `{uploadId,offset,text}` text1..512 bytes UTF-8; offset exacto secuencial → `{message,received}` |
| `/api/tle/commit` | `{uploadId}` → SHA256 y longitud exactos, validación TLE y rename atómico;200 o400, caché anterior conservada ante fallo |
| `/api/tle/abort` | `{uploadId}` →200, conserva caché |
| `/api/catalog` | `{offset:0,limit:10}` limit1..10 → `{total,nextOffset,satellites:[{id,name,epoch,fresh}]}`; nextOffset=-1 final |

Hash y offset se calculan sobre bytes exactos del texto transferido (normalice
antes de calcular SHA256). Begin no reemplaza caché; commit solamente después
de todos los chunks y hash coincidente. Transferencia propiedad HTTP/BLE,
otra mutación bloqueada409; motores no pueden arrancar mientras esté activa.
Inactividad60s aborta RAM, sin tocar caché.
La desconexión BLE aborta inmediatamente su transferencia RAM y libera el
propietario, sin cambiar la caché persistida.
Los trabajos de hash/validación/flash se ejecutan en loop/handlers, **nunca en
callback BLE**; callback de desconexión solamente libera la transferencia RAM,
y callback RX solo ensambla y encola
una petición validada de tamaño limitado. Consultas `/api/passes` siguen
incrementales/idle-only; Android consulta `calculating` hasta false. La app
no necesita ni implementa SGP4 para proporcionar trayectoria al rotor.

### Asistente de calibración web/app (procedimiento)

Interfaz web muestra pasos y estado HOME/motores/nivel/norte/encoders/sitio/UTC.
Haga HOME con contacto físico; espere READY, mueva EL0, nivele con instrumento
y observe referencia de **norte verdadero**, no GNSS estacionario. Con AS5600
habilitados se toman ceros de salida al HOME y se exige `encoderZeroVerified`.
POST calibrate requiere homed, reposo/ENABLE OFF, EL0 y nivel confirmado;
offset=rumboActual−AZmecánico. No existe sensor IMU/magnetómetro automático
implementado. Repetir calibración tras reset/rehome/cambio de montaje.

```powershell
pio run -d firmware -e esp32
pio run -d firmware -e esp32 -t buildfs
```

Layout comprobado contra `default.csv` del framework fijado; chip ESP32 clásico
DevKitC V4 WROOM-32E, flash 4 MB, sin PSRAM. No reutilizar en S3/C3/WROVER.

| Parte | Ruta de compilación | Offset hex / decimal |
|---|---|---|
| bootloader | `firmware/.pio/build/esp32/bootloader.bin` | 0x1000 / 4096 |
| tabla | `firmware/.pio/build/esp32/partitions.bin` | 0x8000 / 32768 |
| OTA inicial | `$PLATFORMIO_CORE_DIR/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin` | 0xe000 / 57344 |
| aplicación | `firmware/.pio/build/esp32/firmware.bin` | 0x10000 / 65536 |
| LittleFS web | `firmware/.pio/build/esp32/littlefs.bin` | 0x290000 / 2686976 |

La partición filesystem se llama `spiffs` pero se formatea LittleFS, tamaño
0x160000 (1 441 792 bytes). **Incluya LittleFS**, de lo contrario `/` devolverá
503. El manifiesto ESP Web Tools puede usar las cinco partes con offsets
anteriores; para binario combinado use esptool 4.5.1:

Antes de cualquier flash desconecte motores y RF y use una fuente protegida.
Una imagen de prototipo no certifica ni aprueba la placa conectada.

```powershell
esptool.py --chip esp32 merge_bin -o combined.bin --flash_mode dio --flash_freq 40m --flash_size 4MB `
  0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin `
  0x10000 firmware.bin 0x290000 littlefs.bin
```

Ejecute en una carpeta con las cinco partes; la imagen combinada se escribe
a offset **0x0**. El bundle conserva avisos de dependencias enlazadas y no
relicencia el conjunto como MIT. Flashear filesystem o borrar chip destruye
TLE/NVS locales: una interfaz WebFlash debe avisar claramente al operador.

## Cableado y aprovisionamiento obligatorios

`board_config.h` fija el mapa acordado para **ESP32-DevKitC V4 de 38 pines,
WROOM-32E sin PSRAM**. `carrierVerified=false` mantiene motores/GNSS
inhabilitados hasta comprobar físicamente el carrier y confirmar por consola USB
`cmd carrier` (o establecerlo a true en una compilación privada).
No sirve para WROVER, S3/C3 ni módulos de distinta distribución de headers.
Verifique eléctricamente el mapa real antes de flashear. La comprobación
rechaza duplicados, pines flash/reservados/strapping/consola, salidas ≥34,
y solapamientos de buses/UART. GPIO34–39 no tienen pull-up interno:
instale resistencias externas en toda entrada de seguridad.

Mapa net→GPIO congelado con el diseño PCB:

| Interfaz | GPIO |
|---|---|
| AZ STEP / DIR | 26 / 27 |
| EL STEP / DIR | 14 / 13 |
| ENABLE común activo LOW | 25 |
| E-stop NC | 34 |
| AZ mínimo / máximo NC | 35 / 36 |
| EL mínimo / máximo NC | 39 / 32 |
| GNSS RX / TX del ESP32 | 16 / 17 |
| AS5600 AZ SDA / SCL | 21 / 22 |
| AS5600 EL SDA / SCL | 18 / 19 |

GPIO16/17 se autorizan exclusivamente para WROOM-32E, donde están disponibles;
no use WROVER/PSRAM. Pull-ups externos 10 kΩ en ENABLE y cinco entradas NC.
Driver acordado: **Watterott TMC2209 SilentStepStick en modo standalone**,
MS1=MS2=3.3 V para 1/16 conforme a su referencia de módulo; motor UART/DIAG
no se cablean/controlan por este firmware. Compruebe revisión y orientación de
headers contra la documentación PCB y fabricante antes de insertar.

* Driver STEP/DIR externo por eje, corriente ajustada al NEMA14 y alimentación
  dimensionada. No alimente el motor desde el ESP32. Ajuste físicamente
  **16 microsteps**, motor 200 pasos/vuelta, planetario 25:1:
  **80 000 microsteps/vuelta de salida**, 222.222… microsteps/grado.
  La base ligera actual sustituye el planetario por **dos etapas GT2 compradas
  de 20:100 dientes**: 5×5=25:1, conservando esos comandos por vuelta.
  El planetario es variante opcional anterior, no la transmisión base.
  Verifique dientes, microsteps y relación instalada; no se asumen perfiles
  GT2 impresos ni poleas sin planos.
* ENABLE común activo LOW, **pull-up externo que mantiene OFF incluso durante
  reset**. Si el driver usa otra polaridad, adapte el circuito/código antes.
* E-stop **normalmente cerrado a masa**; cable abierto/HIGH dispara fallo.
  Debe cortar físicamente la potencia/enable de drivers, independientemente
  del firmware. La entrada solo supervisa ese circuito.
* Cuatro finales físicos **NC a masa**: AZ mínimo/máximo y EL mínimo/máximo.
  HIGH/abierto significa límite alcanzado o cable interrumpido. Una apertura
  durante homing no puede distinguir avería de contacto real: el procedimiento
  exige liberar y reaproximar, pero sigue requiriendo verificación física.
  Use hardware supervisado para una instalación definitiva.
* AZ mínimo está en **−180°**, máximo en **+180°** mecánicos. EL mínimo en 0°,
  máximo en 90°. Ajuste finales, margen físico y referencias reales con útiles;
  el software no puede determinar dónde están instalados.
* UART GNSS NMEA a 9600 configurable, niveles 3.3 V, RX/TX asignados.
* Preferible dos AS5600 **en la salida**, no en el motor antes de la reductora.
  Dirección I2C 0x36 por bus separado, pull-ups a 3.3 V, `encoders=true`,
  pines y polaridades de encoder configurados. Se comprueba presencia del
  imán y rango; referencia en homing y fallo después de tres lecturas de
  discrepancia >3°/pérdida, muestreo 100 ms, timeout I2C 5 ms.
  Resolución angular ≈0.088°, sin medir backlash/rigidez. El encoder absoluto
  no distingue vueltas completas; los finales y cableado siguen obligatorios.

Configure password AP ≥12 y ≤63 caracteres, token aleatorio ≥24 y únicos
(preferiblemente 32 bytes aleatorios codificados). Vacíos desactivan AP/API.
No publique firmware/config con secretos reales. Opcional: SSID/password STA
y **CA PEM vigente** de los proveedores en `tlsRoots`; no se incluye una CA
inventada ni se usa `setInsecure()`. STA es solo acceso saliente: no exponga
puerto 80 a una red no confiable. El HTTP local lleva token sobre Wi-Fi protegido,
no tiene TLS local; limite acceso a operadores autorizados.

## Flujo y seguridad

1. Arranque siempre **DISARMED, ENABLE OFF**. Homing nunca se persiste.
2. Compruebe e-stop/cableado, ordene HOME. AZ busca mínimo, retrocede 700
   microsteps hasta liberación y hace nueva aproximación; luego EL igual.
   Debounce 30 ms, timeout **240 s por eje**, fallo si recorrido previsto
   no encuentra/libera contacto. No use otro final como sustituto del mínimo.
3. Mueva a posición conocida con EL=0. Nivele base con nivel/inclinómetro;
   establezca rumbo **verdadero** actual con referencia fiable.
   `/api/calibrate` calcula offset=rumboActual−AZmecánico.
   GNSS estacionario **no proporciona heading**, ni nivelación.
   Manual es el fallback explícito: no se implementa IMU/compás automático.
4. UTC necesita mensajes GNSS actualizados <3 s, año 2024–2099 válido.
   Ubicación automática exige fix y altitud <5 s; manual persistida permite
   sitio fijo, **no sustituye UTC GNSS**. Un salto de UTC >2 s en movimiento
   dispara fallo.
5. Importe TLE, seleccione satélite y consulte pases. Rechaza checksums,
   número NORAD distinto, campos orbitales inválidos y formato no compatible.
   Solo NORAD numérico (sin Alpha-5/OMM), máximo **100 satélites/48 kB**.
6. Mueva cerca del AZ/EL esperado; TRACK solo inicia sobre horizonte y
   requiere calibración, homing, UTC, sitio y TLE vigente. Adquisición/desfase
   >15° dispara fallo para evitar giro de búsqueda inesperado.
7. STOP corta movimiento y deshabilita drivers, no limpia fallos. STOP durante
   homing invalida referencia. Fallo duro invalida homing/calibración y exige
   CLEAR con e-stop cerrado, HOME y nueva calibración. Ante movimiento manual
   sin alimentación o cambio de montaje: CLEAR/HOME/calibración de nuevo.

AZ es coordenada mecánica limitada ±180; el rumbo verdadero se transforma con
offset de calibración. No se hace unwrap ilimitado. Saltos >180° a través del
corte de cable disparan fallo/reposicionamiento. EL 0..90. Velocidad máxima
500 microsteps/s (=2.25°/s), aceleración 300 microsteps/s². Task motor separada,
un pulso máximo por iteración sin ráfagas de recuperación; dt>20 ms durante
movimiento dispara fallo. Pulsos/dirección con márgenes 3 µs. La tarea de
predicción procesa cuatro posiciones por vuelta y no bloquea para un pase entero.
Consultar/iniciar pases se rechaza con motores en movimiento; un cálculo pendiente
se pausa durante movimiento. Descargar TLE también se rechaza con motores activos.
La supervisión física usa una tarea independiente del servidor HTTP, además del
corte de potencia físico obligatorio; aún falta medir el peor caso en hardware.
No garantiza velocidad suficiente cerca de cenit: pruebe seguimiento/backlash
en banco; no hay planificación previa certificada de pases mecánicamente inviables.
TRACK rechaza EL≥89° y dispara fallo al entrar en esa zona. Una propagación
SGP4 adelantada 1 s comprueba velocidades AZ/EL: si exceden 2.25°/s, se detiene
con fallo; esto no garantiza margen de aceleración ni reemplaza el ensayo físico.
Motores deshabilitados en reposo pueden perder posición; con encoders se vigila,
sin ellos el operador debe rehome tras cualquier desplazamiento.
Una variante ligera por correas es retroaccionable: STOP, fallo, reset y reposo
deshabilitan el driver y **no mantienen la antena por par eléctrico**.
Balancee la carga y emplee freno/retención mecánica independiente para impedir
caída o giro peligroso al cortar alimentación. AS5600 detecta discrepancias,
pero no retiene la carga. El objetivo ≤3 kg excluye radio/trípode e incluye
alimentación; no es una masa medida ni autorización de carga.

## HTTP API local

Todas las rutas `/api/*`, incluidas GET, requieren header
`X-Control-Token: <token configurado>`. Sin CORS, sin estado por GET, sin comodines,
sin cookies; token mantenido solo en memoria de la página (no localStorage).
POST usa `Content-Type: application/json`; respuestas JSON. 200 éxito,
202 orden iniciada, 400 esquema inválido, 401 token, 409 precondición,
502 descarga fallida. `{"message":"..."}` o `{"error":"..."}`.
La parada web no sustituye e-stop físico.

| Método/ruta | Cuerpo / resultado |
|---|---|
| GET `/api/status` | mode/fault, hardwareConfigured, enabled, homed, calibrated, level, utc/utcValid, siteValid/manualSite/lat/lon/alt, northOffset, azMechanical/el, skyAz/skyEl/rangeKm/rangeRateKmS, doppler145Hz/doppler435Hz, trackingBlocker, selected, download, staConnected, encoders, pttCat=false |
| POST `/api/site` | `{"manual":true,"lat":40.4,"lon":-3.7,"alt":650}`. Todos obligatorios; false vuelve a GNSS. Detenido; invalida cálculo orbital/lista de pases |
| POST `/api/home` | `{}`. Homing físico asíncrono, calibra posición mecánica solamente |
| POST `/api/move` | `{"az":0,"el":0}` AZ **mecánico**, no rumbo verdadero; no requiere calibración/UTC para permitir montaje |
| POST `/api/stop` | `{}`. Deshabilita sin limpiar FAULT |
| POST `/api/clear` | `{}`. Limpia fallo con e-stop cerrado; invalida homing/calibración |
| POST `/api/calibrate` | `{"trueAz":0,"levelConfirmed":true}` rumbo verdadero actual, EL=0 y reposo obligatorios |
| GET `/api/tle` | `{"satellites":[{"id":0,"name":"...","epoch":unix,"fresh":true,"line1":"...","line2":"..."}]}` |
| POST `/api/tle` | `{"text":"nombre\n1 ...\n2 ...\n"}`. Reemplazo completo validado y persistente; no mezcla parcial |
| POST `/api/select` | `{"id":0}` índice de la lista actual, no NORAD; se reinicia al importar |
| GET `/api/passes` | Inicia/consulta cálculo: `calculating`, `stepSeconds=10`, `passes:[{aos,los,peak,maxEl,partial}]`; tiempos Unix UTC. Ventana 24 h, horizonte geométrico 0°, resolución temporal 10 s, posible pérdida de pases muy breves. Caché 60 s; parcial indica ventana truncada |
| POST `/api/track` | `{}`. Sigue seleccionado actual (no agenda futura); finaliza al bajar del horizonte |
| POST `/api/update` | `{"provider":"celestrak"}` o `amsat` / `pe0sat`; reposo, STA conectado, UTC GNSS y CA PEM requeridos |

Proveedores exactos, no URL arbitraria:

* CelesTrak amateur: `https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle`
* AMSAT: `https://www.amsat.org/tle/current/dailytle.txt`
* PE0SAT: `https://tle.pe0sat.nl/kepler/mykepler.txt`

HTTPS valida hostname, cadena y tiempo GNSS. Redirects deshabilitados;
Content-Length positivo ≤48 kB requerido (chunked se rechaza), conexión 5 s,
lectura 8 s. Cambios de formato, TLS, DNS, límites de lista o respuesta fallida
son **explícitos**; conserve/importación manual de un subconjunto si el proveedor
excede 100 satélites. No se afirma que las tres respuestas actuales se hayan
descargado con el ESP32. AP aislado no puede obtener Internet.

LittleFS escribe `/tle.new` y renombra atómicamente a `/tle.txt` tras validar;
error conserva la caché anterior en RAM/destino. Nunca se formatea automáticamente
si no monta. Sitio/offset en NVS; confirmación de nivel/homing/calibración **no**
se restaura. TLE antiguo/futuro inhibe tracking (>14 días o >1 día futuro),
aunque la descarga reciente no cambia su epoch orbital.

## Ensayos pendientes antes de antena real

Con motores desacoplados: validar polaridad ENABLE, e-stop físico ante reset y
bloqueo del procesador, apertura de cable, cada final y timeout; dirección,
microsteps/reductora y montaje AS5600. Medir latencias máximas con HTTPS/SGP4/Wi-Fi.
Ensayar pérdida GNSS, salto UTC, TLE corrupto/viejo, fallos de escritura y corte
de alimentación, pérdida de imán/bus, atasco, backlash, límite de cable, cenit.
Después banco de carga y referencia angular independiente; solo después
ensayo RF a baja potencia atendido. No existe auto-home persistente,
dual-GNSS heading, IMU, perfil dinámico de viento, cola de pases automática,
control full dúplex ni automatismo de transmisión.
