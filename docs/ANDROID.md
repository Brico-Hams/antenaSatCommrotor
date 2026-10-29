# Android nativo: control BLE local

Paquete `org.bricohams.portablesatstation`, Kotlin nativo, Android 8/API 26 mínimo,
SDK objetivo/compilación 35. Recursos españoles por defecto; traducción inglesa
con el idioma del dispositivo. No React, WebView, cálculo orbital en el teléfono,
servicio de control en nube, analítica, geolocalización del teléfono, CAT ni PTT.
**INTERNET está autorizado únicamente para descargar TLE públicos por HTTPS**
de los tres proveedores fijados más abajo; control/transferencia siguen siendo BLE local.

**Prototipo no validado en campo.** Compilar no valida cableado, mecánica, RF,
seguridad funcional ni exactitud del rotor. Use parada de emergencia física,
alimentación protegida, límites comprobados y supervisión adulta.

Autores actuales: **Anatol EA5KAO, Diego EA5JEF y Pedro Roca Molina**.
[Bricohams](https://bricohams.org) es una referencia de divulgación educativa,
no una certificación ni un respaldo implícito de terceros. Consulte también
[autores](../AUTHORS.md) y [aviso](../DISCLAIMER.md).

## Compilar y probar

En Windows, desde `android`:

```powershell
$env:JAVA_HOME = 'ruta\al\jdk-17'
$env:ANDROID_HOME = 'ruta\al\sdk-android'
$env:ANDROID_USER_HOME = Join-Path $PWD '.tools\android-user'
.\gradlew.bat --no-daemon testDebugUnitTest lintDebug assembleDebug
Get-FileHash .\app\build\outputs\apk\debug\app-debug.apk -Algorithm SHA256
```

Linux/macOS: `chmod +x gradlew` y
`./gradlew --no-daemon testDebugUnitTest lintDebug assembleDebug`.

Herramientas fijadas: **AGP 8.7.3 / Kotlin 2.0.21 / Gradle 8.9 / JDK 17 /
platforms;android-35 / build-tools;35.0.0**.
La distribución Gradle se verifica con SHA-256
`d725d707bfabd4dfdc958c624003b3c80accc03f7037b5122c4b1d0ef15cecab`.
`gradle-wrapper.jar` es el binario oficial Gradle 8.9, SHA-256
`498495120a03b9a6ab5d155f5de3c8f0d986a449153702fb80fc80e134484f17`.
Fuentes de verificación:
[distribución](https://services.gradle.org/distributions/gradle-8.9-bin.zip.sha256),
[wrapper](https://downloads.gradle.org/distributions/gradle-8.9-wrapper.jar.sha256).

Se aprovisionaron herramientas locales aisladas en `android\.tools` (ignorado):
Microsoft JDK 17.0.16+8 desde `aka.ms/download-jdk`, ZIP SHA-256
`53f0c9ec64811a9ab968747076653e5500115db7230d244e4ec53577ca5ec8fc`;
Android command-line tools 19.0, archivo
`commandlinetools-win-13114758_latest.zip`, SHA-256
`98b565cb657b012dae6794cefc0f66ae1efb4690c699b78a614b4a6a3505b003`.
Su SHA-1 `54a582f3bf73e04253602f2d1c80bd5868aac115` fue contrastado
con `https://dl.google.com/android/repository/repository2-1.xml`.
No se modifica Java/SDK global ni se sube código privado para construir.
`ANDROID_USER_HOME` mantiene preferencias y clave debug generada por AGP
en `android\.tools\android-user`; la clave debug no se versiona ni se presenta
como clave/certificado de publicación del autor.

La acción `.github/workflows/android.yml` ejecuta pruebas JVM, lint y compilación,
y publica el APK **debug** y su hash como artefacto GitHub descargable. Un debug
APK usa la clave de depuración generada por las herramientas; **no es una firma
de distribución oficial** ni un certificado inventado. No hay publicación
automática en tiendas. La distribución release requiere la clave privada real
del autor fuera del repositorio, mediante un proceso protegido independiente.

### Evidencia local (10 de octubre de 2026)

`testDebugUnitTest lintDebug assembleDebug`: **BUILD SUCCESSFUL**.
**29 pruebas JVM, 0 fallos/errores; lint: “No issues found”.**
Incluye comprobación de UUID/versiones/límites contra el código real del
controlador, framing exacto MTU 23/185, UTF-8, límites de tamaño/secuencia,
entrada no numérica/no finita, autenticación fallida, estado malformado,
versiones incompatibles, orden de llamadas, catálogo paginado, checksum/epoch
TLE, subconjunto explícito de proveedor con más de 100 entradas, caché atómica,
allowlist HTTPS sin redirecciones y begin/chunk/commit/abort
con offsets exactos. App **0.3.0-prototype**, versionCode **3**.

APK: `android\app\build\outputs\apk\debug\app-debug.apk`.
SHA-256:
`47997a78abd87b3aa4e26a33106f9b122a817121dd02c2abc7d6b72717ca399b`.
`apksigner verify` completado; `aapt dump permissions` confirma BLE, ubicación
solo hasta API 30 e INTERNET para las descargas HTTPS. Este APK está firmado para depuración,
no para una distribución release. Sus hashes no certifican hardware ni BLE.
Reportes: `android\app\build\reports\tests\testDebugUnitTest` y
`android\app\build\reports\lint-results-debug.html`.

Se ejecutó **el downloader HTTPS y el parser reales de la app en JDK 17 local**
contra el endpoint AMSAT: HTTP 200, **97 satélites, 14434 bytes**, SHA-256
`ec291294636090d712fc901e4a7e3fa15bbeb8366fb771d7aad131b5c8db1ce9`.
No es solo una respuesta simulada en tests; no se subieron datos privados.
CelesTrak y PE0SAT agotaron el plazo de conexión en esta red: no se afirma que
hayan descargado ni se sustituye por TLS inseguro/otro URL. Los errores de
proveedor conservan la caché. Esta prueba **no** valida TLS/radio en un Android
real ni la transferencia BLE física. Los datos de proveedor cambian diariamente.

## Uso y seguridad

1. Configure físicamente el BLE del rotor con su passkey y token API locales.
2. Introduzca el token en el campo de contraseña. «Guardar» es explícito;
   Android Keystore conserva una clave AES-GCM no exportable y SharedPreferences
   únicamente IV y ciphertext. Backups de la aplicación deshabilitados.
3. Lea la explicación de permisos y busque. Android 12+ usa
   BLUETOOTH_SCAN/CONNECT; versiones anteriores requieren ubicación para BLE,
   pero no se llama a una API de ubicación ni se obtiene/sube geoposición.
4. Seleccione explícitamente el dispositivo físico. Android presenta el diálogo
   de emparejado. Bonding y autenticación por token son requisitos separados.
5. Conexión y autenticación nunca envían homing, movimiento ni habilitan motores.
6. Consulte estado antes de usar motores. Rehome/arranque requieren calibración
   física nuevamente: nivelación instrumentada, salida EL=0, y rumbo verdadero
   medido (geografía/sol o brújula corregida por declinación, lejos de metal).
   GNSS estacionario no mide rumbo. El progreso persistente de la guía **no**
   constituye una calibración; el estado autenticado del firmware es autoritativo.

La búsqueda se detiene a los 15 segundos y al salir de la pantalla. Desconexión
explícita disponible. Al pasar a segundo plano se cierra la sesión; no hay
reconexión automática ni envío automático de órdenes motoras al volver.
Una desconexión Bluetooth **no sustituye la parada física**. No se registran
tokens ni se muestran excepciones/JSON de autenticación arbitrarios.
También se excluyen preferencias/archivos del backup y transferencia entre
dispositivos; la ventana impide capturas/previsualizaciones del token. Estos
controles no protegen frente a un teléfono/teclado/OS comprometido o acceso root,
ni demuestran que el Keystore sea hardware-backed en todos los teléfonos.

## TLE: descarga telefónica y transferencia atómica BLE

Se puede descargar **antes de conectar BLE**. Elija CelesTrak, AMSAT o PE0SAT
en la app y pulse Descargar. Los únicos URL admitidos son:

- `https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle`
- `https://www.amsat.org/tle/current/dailytle.txt`
- `https://tle.pe0sat.nl/kepler/mykepler.txt`

Petición GET sin token, cookies, posición, archivos privados ni subida de datos.
No hay analítica. El proveedor ve la IP de origen y la petición pública normal.
Se mantiene la verificación TLS/hostname/CA del sistema; no hay
`TrustAll`, HTTP, URL proporcionado por el usuario, redirecciones ni fallback
inseguro. Una redirección/HTTP distinto de 200 se muestra como error y conserva
el último catálogo. No se corrigen certificados ni se siguen destinos nuevos.
Timeout conexión/lectura 15 s; lectura acotada por tamaño y plazo 45 s entre
lecturas. Cancelar/segundo plano cancela la tarea, sin reconectar ni publicar.
Sin red también se puede importar un archivo mediante el selector Android
(`ACTION_OPEN_DOCUMENT`), sin permiso general de almacenamiento.

Máximo persistido/transferido **48000 bytes, 100 satélites, nombres de 64 caracteres ASCII, NORAD
numérico de cinco dígitos único**, dos líneas de 69 caracteres con checksum
NORAD, mismo identificador y epoch válido. Se comprueban los campos numéricos
y rangos del controlador, sin ejecutar SGP4 en el teléfono. Se normaliza CRLF
a LF y se conserva un catálogo canónico validado. Un proveedor/archivo de hasta
48000 bytes con más de 100 entradas válidas abre un selector explícito
(máximo 300 entradas candidatas en RAM): elija **1–100**, sin preselección ni
truncamiento silencioso. Cancelar no modifica la caché anterior. Solo el
subconjunto elegido se vuelve a validar, guarda y transfiere. Archivos de más de
48000 bytes se rechazan antes de reensamblar catálogos; importe un archivo menor.
La validación del firmware al commit sigue siendo autoritativa.
El signo positivo de exponente en blanco, presente en AMSAT (incluido QO-100),
se acepta como en `control_logic.h`, sin reescribir líneas/checksums ni inventar
elementos orbitales.

La caché vive únicamente en archivos privados de la app y está excluida de
backups. Solo se reemplaza tras validar por completo, escribir/sincronizar un
archivo staged y efectuar `Files.move(ATOMIC_MOVE, REPLACE_EXISTING)` en el mismo
directorio. Si no puede reemplazarse de manera atómica se conserva el archivo
anterior; no hay fallback delete-first. Descargar una actualización fallida
no borra la última caché válida.

Puede transferir el catálogo completo o **solo el TLE elegido**. Ambos casos
**reemplazan todo el catálogo del rotor**, no mezclan/añaden; el diálogo advierte
que selección y caché de pases se invalidan. La app solicita un estado fresco
autenticado justo antes del begin y exige reposo (`READY`/`DISARMED`), UTC GNSS
válida y edad de cada TLE dentro de 14 días, futuro máximo 1 día, usando
**UTC del rotor**, no el reloj telefónico. No habilita motores ni seguimiento
automáticamente. Consulte GNSS, cargue el catálogo rotor y seleccione de nuevo.

Contrato v1 contrastado con handlers reales:

| POST ruta | Body | ACK requerido |
|---|---|---|
| `/api/tle/begin` | `length` entero 1..48000, `sha256` 64 hex minúsculas | `uploadId` uint32 positivo |
| `/api/tle/chunk` | `uploadId`, `offset` byte secuencial, `text` 1..512 bytes ASCII | `received` exactamente acumulado |
| `/api/tle/commit` | `uploadId` | respuesta HTTP 2xx sin error y `message` string |
| `/api/tle/abort` | `uploadId` | respuesta HTTP 2xx sin error y `message` string |

Cada bloque respeta también el máximo JSON de 2048 bytes y framing GATT v1.
Se espera ACK/END antes de enviar el siguiente bloque. Hash, longitud, offsets,
propietario y validación TLE se comprueban otra vez en ESP32; la caché anterior
permanece hasta un commit verificado. El firmware hace staging en RAM y
reemplazo atómico en LittleFS. Timeout global app 5 minutos, por petición 15 s;
el firmware invalida una transferencia inactiva tras 60 s. No hay reintentos
automáticos de una orden con ejecución incierta. Si se pierde el ACK del commit,
la app **no asume éxito ni fracaso de persistencia**: reconecte explícitamente
y consulte el catálogo del rotor.

Durante la transferencia la app bloquea mutaciones concurrentes. Cancelar espera
el ACK en curso y envía abort. PARAR solicitado durante una transferencia espera
ese abort antes de enviar stop; no sustituye a la parada física de emergencia.
Si commit ya fue enviado, no se promete abortar/revertir: se espera el ACK
real y se consulta el rotor cuando sea incierto. La app lo indica explícitamente.
No se pueden comenzar transferencias mientras el rotor mueve/trackea. La app
no inyecta una segunda orden concurrente ni afirma haber confirmado commit antes
del ACK final.

## Pases y autonomía

El ESP32 calcula SGP4 y próximas 24 h; el teléfono solo selecciona un satélite
del catálogo rotor y consulta `/api/passes`. Respuestas `calculating:true`
activan consultas acotadas a 60 peticiones, espaciadas 1,5 s, cada una
serializada y autenticada. La app presenta AOS/LOS en **UTC explícito con Z** y
elevación máxima, sin sustituir hora local por UTC ni calcular trayectoria.
Si se agota el límite se muestra y la siguiente consulta debe ser explícita.
UTC GNSS, sitio y TLE fresco son necesarios; el firmware decide si el
seguimiento es seguro. Las frecuencias no forman parte del TLE y no se inventan.
Tras iniciar seguimiento confirmado, el teléfono puede cerrarse: el ESP32
continúa de manera autónoma según el contrato firmware. No hay CAT ni PTT.

## Contrato contrastado con firmware

Las UUID y el framing proceden de `firmware/src/main.cpp` (`setupBLE`,
`serviceBLE`) y `firmware/include/ble_protocol.h`, no de un servicio externo.

| GATT | UUID |
|---|---|
| Servicio | `c8200001-4e53-4253-9000-000000000001` |
| RX, write con respuesta y autenticación/cifrado | `c8200002-4e53-4253-9000-000000000001` |
| TX, notificaciones | `c8200003-4e53-4253-9000-000000000001` |
| CCCD estándar | `00002902-0000-1000-8000-00805f9b34fb` |

Versión JSON BLE **1**. Cada trama mide 5–20 bytes:
`0x53, flags, sequenceLo, sequenceHi, payload(1–16 bytes)`.
Flags START=1, END=2; secuencia little-endian desde 0. START|END=3 para
un único fragmento. Se negocia MTU 185 (reintento 23); **v1 sigue usando 20
bytes por trama incluso con MTU mayor**, conforme al firmware. No newline,
NUL ni reensamblado de cadenas parciales: UTF-8 se decodifica solo después
de END. Máximo petición 2048 bytes; respuesta 8192. Se rechazan secuencias
fuera de orden, START repetidos, flags desconocidos, UTF-8 inválido, IDs
ajenos y mensajes demasiado grandes.

La respuesta completa de `status` exige **`apiVersion:2`,
`protocolVersion:1`, `firmwareVersion:"0.3.0-prototype"`**, constantes
contrastadas con `firmware/include/ble_protocol.h`. Cualquier versión distinta,
campo ausente o versión en forma de cadena deshabilita el control y desconecta.
La comparación de firmware es deliberadamente exacta: una nueva versión,
incluso compatible, requiere revisar/actualizar la app y ejecutar sus pruebas.

Petición:

```json
{"v":1,"id":1,"path":"/api/status","method":"GET","token":"<introducido localmente>","body":{}}
```

Respuesta:

```json
{"v":1,"id":1,"code":200,"data":{"mode":"READY","fault":"","homed":true,"calibrated":false}}
```

Este último fragmento es **ilustrativo**, no un estado completo aceptado:
se requieren además los campos tipados de posición, UTC, sitio y seguridad
presentes en el firmware. Nunca se acepta `code=401/403`, aunque `data`
parezca indicar éxito. IDs positivos uint32 y estrictamente crecientes por
conexión; la app reinicia su contador únicamente al cerrar una conexión.
El primer intercambio es `GET /api/status` con token, después de bonding,
descubrimiento, MTU y confirmación CCCD. No se inventa una ruta `/auth`.

Una única operación GATT y una única petición JSON en vuelo. Cada write
espera `onCharacteristicWrite`; un inicio rechazado tiene dos reintentos
acotados, no se reenvía una orden motora cuya ejecución sea incierta.
Plazo de conexión/operación/petición: 15 segundos. Error de autenticación,
framing o timeout cierra la conexión y exige selección explícita de nuevo.
PARAR tiene prioridad en la cola de la app, pero espera END del intercambio
en curso para no mezclar dos respuestas. La parada física es indispensable:
ni BLE ni esta cola garantizan una latencia de parada de emergencia.

Rutas reales admitidas: GET `status`, `tle`, `passes`; POST `stop`, `clear`,
`home`, `move`, `calibrate`, `site`, `select`, `track`, `catalog`,
`tle/begin`, `tle/chunk`, `tle/commit`, `tle/abort`. La pantalla
usa el catálogo real paginado `POST /api/catalog` con `offset` entero y
`limit:10`, y confirma `total`, IDs contiguos y `nextOffset` antes de habilitar
su selección. «Siguiente página» es explícito, sin bucles de peticiones.
AZ mecánico [-180,180]°
y EL [0,90]°; rumbo verdadero [0,360)°; sitio lat [-90,90]°, lon [-180,180]°,
alt [-500,9000] m. Valores numéricos finitos obligatorios; cadenas numéricas
y booleanos no cuentan como números. El rotor calcula SGP4 y pases; el
teléfono solo necesita Internet para descargar desde un proveedor; puede
importar un archivo local o utilizar TLE preexistentes sin Internet.
GET `tle` completo que exceda 8192 bytes se rechaza; la pantalla evita ese límite
mediante el catálogo paginado y admite los 100 satélites del rotor.

El controlador comparte handlers HTTP/BLE. Mientras un transporte posee un
movimiento, el otro no puede iniciar otra orden de control: devuelve 409;
STOP y consulta de estado siguen disponibles con autenticación. La app no
intenta apropiarse silenciosamente del control. En el firmware contrastado,
perder BLE durante movimiento manual/homing ocasiona FAULT; seguimiento
autónomo ya iniciado no depende de conservar la pantalla/app abierta.
STOP no borra fallos; `clear` exige rehome y nueva calibración.

## Validación pendiente de hardware

Las pruebas JVM verifican lógica/protocolo, no la radio del teléfono. Sigue
pendiente comprobar en un Android real: diálogo de passkey, rechazo sin bonding,
cifrado MITM exigido por firmware, MTU 23 y MTU negociado, permisos 26/30/31/35,
timeout, pérdida de radio, segundo cliente y parada física. Nunca se afirma que
los motores, el enlace BLE o la calibración estén validados en campo.

## Revisión 2026-10-11: descarga TLE, sincronización BLE, marca y ayuda

Cambios **no compilados con Gradle** en el entorno de revisión (sin red a Maven/SDK). La lógica de `TleCatalogue` y `TleDownload`
se compiló con `kotlinc` en JVM y se ejecutó una comprobación; las pruebas JVM (`./gradlew testDebugUnitTest`) siguen pendientes.

| Hallazgo | Causa probable | Corrección |
| --- | --- | --- |
| Fallos de descarga sin explicación útil | cualquier código HTTP o tiempo agotado se mostraba como "TLE inválido: tle_http_…" o como un error genérico | mensajes específicos: límite de uso (403/429), redirección (301/302/303/307/308), no encontrado, servidor y tiempo agotado; la caché válida se conserva |
| Una descarga con líneas con blancos finales fallaba | el analizador exigía líneas exactas de 69 caracteres sin espacios finales | `TleCatalogue.parse` ignora espacios/CR/tabuladores finales (no cambia el contenido validado ni el checksum) |
| Transferencia a la Raspberry cortada a los 300 s | temporizador total fijo, con 512 caracteres por trozo sobre tramas BLE de 20 bytes | detección de bloqueo: se reinicia (60 s) con cada ACK; sin avance en 60 s se cancela y desconecta |
| Fallo de conexión BLE `133` | estado transitorio habitual de Android sin reintento | hasta 2 reintentos automáticos en `BleTransport` (no en `RadioHostBleTransport`, pendiente) |
| Sin logo ni ayuda | — | logotipo y autores en las tres pantallas (`Branding.kt`), icono de lanzador BricoHams, botón Ayuda (`HelpActivity`; textos offline en `res/raw`, `res/raw-en`, `res/raw-hu`) |

**Nota sobre proveedores:** la verificación anterior (arriba) descargó 97 satélites de AMSAT, pero CelesTrak y PE0SAT agotaron el plazo desde esa red.
En esta revisión una herramienta de lectura web recibió un `302` de AMSAT hacia `http://`, algo que la app rechazaría (sin redirecciones ni texto plano),
pero no pudo reproducirse con la app, así que **no** se desactivó ningún proveedor. Si un proveedor falla desde su red, la app lo explica y sugiere otro;
anote cuál funciona en el registro de pruebas (APP-03). El proveedor ve la IP de la conexión.

Pendiente de verificar en teléfono real: los tres proveedores desde la red del usuario, transferencia BLE completa de un catálogo grande
y el reintento del error 133. Pruebas: [testing/07-app-android.md](testing/07-app-android.md).
