# Web flasher de prototipo (preparado, no publicado)

**PCB/hardware no liberados. No conectar motores durante el flasheo.**
El CI comprueba software y datos de flash; no verifica placas, cableado, movimiento,
estop, homing, calibración, precisión orbital ni RF. Preparar Git no significa
publicar: no se ha hecho push, habilitado Pages ni ejecutado GitHub Actions aquí.

## Qué se compila

`.github/workflows/webflash.yml` trabaja separado del workflow de ingeniería.
Un tag `v*`, push a `main` o `workflow_dispatch` compila el entorno **esp32** real
de `firmware/platformio.ini`. PRs pertinentes compilan/validan artefactos sin
permisos de despliegue, secretos ni `pull_request_target`.

Pins: PlatformIO Core 6.1.18; espressif32 6.10.0;
Arduino-ESP32 3.20017.241212 (Arduino 2.0.17); Xtensa 8.4.0+2021r2-patch5;
ArduinoJson 6.21.5; TinyGPSPlus 1.1.0; Sgp4-Library commit
`7c82d31f9d9a286acde5ef55da8308fc93d2ba96`.
NimBLE-Arduino 1.4.3 se compila para BLE opcional configurado localmente.
La UI LittleFS incluye el asistente de calibración física. BLE usa los handlers
del controlador y autenticación configurada privadamente; no se habilita por
publicar/flashear. La descarga HTTPS por BLE devuelve 409; descargar TLE en el
cliente y transferirlos por el protocolo documentado del controlador/app.
La transferencia grande TLE utiliza `/api/tle/begin`, `/api/tle/chunk` y
`/api/tle/commit`, validación SHA256 y sustitución atómica del cache; catálogo
paginado. El teléfono descarga datos; la propagación SGP4 permanece en el rotor.
Heap, coexistencia radio y calibración física no están validados por compilar.
CI fija además tool-esptoolpy 1.40501.0 (esptool 4.5.1) y
tool-mklittlefs 1.203.210628 (2.3) mediante PLATFORMIO_PLATFORM_PACKAGES,
manteniendo los mismos pins framework/toolchain del controlador.
La configuración real y versiones de paquetes resueltos se incluyen en
`build-info.json`; no se cambia `platformio.ini` desde este workflow.
Node 22 y Python 3.11 están fijados por línea compatible; Actions por major.

ESP Web Tools **10.1.0**, licencia **Apache-2.0** verificada en npm y en el
LICENSE del paquete. `webflash/package-lock.json` fija también dependencias
transitivas/integridad. CI ejecuta `npm ci --ignore-scripts`, copia **todo dist/**
a `vendor/esp-web-tools/` sin aplanar directorios y conserva chunks/imports
dinámicos y licencias. No usa `unpkg latest`, CDN remoto ni fallback silencioso.
La entrada de navegador es **dist/web/install-button.js**, no el módulo
dist/install-button.js con imports sin extensión. El validador comprueba los
imports relativos de todos los chunks de la distribución de navegador.
Fuentes upstream Arduino 2.0.17/ESP-IDF v4.4.7 y textos de licencia descargados
desde tags públicos se verifican contra SHA256 fijados, no se aceptan cambios
silenciosos de un tag.
La página depende inicialmente de npm/GitHub para generar y servir estos activos;
no afirmar que los fuentes solos sean un flasher offline.

## Datos de flash: nunca offsets adivinados

`scripts/build-webflash-proof.py` es un extra-script post de PlatformIO.
Su target `webflash-proof` construye firmware y captura `$UPLOADCMD`,
`FLASH_EXTRA_IMAGES`, `ESP32_APP_OFFSET`, placa/MCU y paquetes reales.
**No ejecuta upload, no abre puerto y no borra un dispositivo.**
`scripts/build-webflash.cjs` verifica esa receta y los binarios compilados:

| Archivo | Offset decimal (hex) |
|---|---:|
| bootloader.bin | 4096 (0x1000) |
| partitions.bin | 32768 (0x8000) |
| boot_app0.bin | 57344 (0xe000) |
| firmware.bin | 65536 (0x10000) |

Manifest ESP Web Tools: `chipFamily: "ESP32"` (clásico WROOM, **no C3**).
No se crea un binario ficticio ni se publica una imagen combinada rellenada
desde 0 que pudiera destruir NVS. Se usan cuatro partes separadas.
Si la versión del controlador aún sirve `/index.html` desde LittleFS, CI
construye `buildfs` e incluye una quinta parte `littlefs.bin`, con offset/tamaño
obtenidos de **partitions.bin** (actual default: 0x290000/0x160000).
Esto reemplaza UI y TLE guardados; hacer copia antes. Si el controlador incorpora
la UI en flash de programa, sólo se necesitan cuatro partes: no subir una imagen
de filesystem por costumbre. El generador comprueba el código existente.

Validación: headers ESP32, número de partes, offsets de comando real, rutas
relativas seguras, SHA256/longitud de cada binario, solapamiento de sectores,
tamaño de partición de aplicación/filesystem y NVS de tabla real.
`SHA256SUMS`, manifest y commit completo permiten identificar la descarga.
`build-info.json` vincula también SHA256 del árbol fuente relevante: todos los
archivos firmware/src, firmware/include, web y platformio.ini, con hashes
individuales. El generador compara ese árbol contra el capturado por PlatformIO;
si cambió una cabecera, UI o configuración desde la prueba, exige recompilar.
Versiones reales de paquetes y hash del lock npm identifican dependencias.
Hashes de binarios pueden diferir entre rutas de build/toolchains/metadata:
no se sustituye el hash del artefacto real por el de otro build.
Una compilación local sin primer commit o con cambios sin commit se etiqueta
`local-prototype+uncommitted`; `sourceSha` es null, nunca un SHA inventado.
La prueba sintética bajo `tests/webflash.test.cjs` no es un firmware de ejemplo:
vive únicamente en directorios de test ignorados. CI además valida su bundle real.

## Credenciales y actualización

La compilación pública exige `carrierVerified=false` y
`apPassword`, `apiToken`, `staSsid`, `staPassword` vacíos en `board_config.h`.
Si aparecen `firmware/include/secrets.h` o `firmware/secrets.ini`, falla ANTES
de compilar. Nunca usar GitHub Secrets para insertar contraseñas WiFi/tokens en
firmware distribuido públicamente. En NVS virgen el controlador con valores
vacíos desactiva AP/API hasta provisioning USB local, sin recompilar.
Con NVS previa compatible conserva credenciales y verificación de carrier;
siempre arranca DISARMED y no restaura homing/calibración.

Provisionar **privadamente y localmente** según `docs/CONTROL.md`, sin subir
configuración a Pages, Git o artefactos públicos. Después de instalar, cerrar
el puerto ESP Web Tools y abrir consola USB local a 115200 baudios:
`{"cmd":"setup"}` entra en SETUP, desactiva WiFi y motores e invalida calibración;
`cmd config` guarda SSID, password AP propia de 12–63 caracteres y token propio
de 24–128 ASCII en NVS (campos y validación exactos en CONTROL.md);
`{"cmd":"reboot"}` aplica los cambios y arranca desarmado.
No compartir terminales/screenshots con credenciales. No enviar `cmd carrier`
con verified=true hasta comprobar físicamente la placa. BLE requiere activación
local explícita y passkey propia. Este flasher no inventa protocolo, no habilita
Improv WiFi automáticamente y no expone un token.
NVS no está cifrada: acceso físico/USB permite leer o modificar configuración;
guardar credenciales allí no constituye protección frente a extracción física.
Las líneas JSON admiten hasta 768 bytes. `tlsRoots` sigue vacío en la imagen
pública, por lo que las actualizaciones HTTPS se rechazan; la carga manual de
TLE sigue disponible después de configurar el AP. No afirmar que el binario
público actual pueda descargar TLE HTTPS sin configurar raíces de confianza.

La escritura normal NO toca NVS: default 0x9000–0xdfff. El manifest exige
confirmación de borrado (`new_install_prompt_erase: true`); la casilla
**Erase device** aparece desmarcada por defecto. Se verificó el código real de
ESP Web Tools 10.1.0: **false provoca borrado automático en dispositivos sin
Improv Serial**, por eso NO se debe utilizar false para conservar NVS.
**No seleccionar “Erase device”** en ESP Web Tools salvo intención de borrado
total, copia previa y confirmación explícita en su diálogo. Conservar NVS sólo
es válido con la misma tabla de particiones; migrar layouts requiere una
estrategia/copia revisada. Nunca restaurar homing/calibración como autorización
automática de movimiento.

## Habilitar Pages, sólo cuando el propietario lo decida

1. Crear remoto/URL con la cuenta/repositorio elegidos. No hay una URL inventada
   en estos archivos; consultar la URL real que devuelve el deployment de GitHub.
2. En GitHub: **Settings → Pages → Source: GitHub Actions**.
3. Crear entorno **webflash-pages**, configurar **Required reviewers** para
   aprobación manual, restringir ramas a `main` y desactivar bypass si es posible.
   Comprobar que el plan/visibilidad del repositorio permite esa protección.
4. Sólo después de revisar el prototipo y configurar reviewers, establecer
   variable de repositorio **WEBFLASH_PAGES_APPROVED=prototype-only**.
   Sin ella el job deploy no corre. No establecerla si no se pueden exigir
   reviewers: descargar artefactos manualmente sin publicar.
5. Push a `main` (si aprobado) o dispatch desde `main` con `deploy_pages=true`.
   Tags generan artefactos versionados pero no despliegan Pages; PRs nunca.
   Dispatch desde otra rama tampoco despliega.

Permisos `contents: read` para build; `pages: write` e `id-token: write`
exclusivamente en deploy condicionado y con entorno protegido. No se necesita
PAT ni introducir secretos. Aprobar deployment no convierte hardware en
producto liberado: las advertencias PROTOTIPO permanecen en la página.
El artefacto de Actions se llama `webflash-<commit SHA>`; contiene la página,
bins reales, hashes, metadata, notices/licencias y fuentes/objetos para relink.
Los archivos de cumplimiento/fuente upstream son grandes; no se descargan al
flashear, sólo las partes del manifest. Conservarlos en la distribución.
No se crean GitHub Releases ni se mueve un tag desde el workflow.

## Navegador, permisos y privacidad

Pages debe servir HTTPS. Web Serial requiere **Chrome o Edge de escritorio**
en contexto seguro; Firefox/Safari/móvil no son una alternativa compatible.
Abrir directamente, no iframe; políticas empresariales pueden bloquear USB.
El permiso de puerto es opcional y sólo aparece al pulsar Conectar.
Denegarlo/cancelarlo no flashea nada: volver a intentar o usar PlatformIO local.
Elegir por etiqueta/puerto el **ESP32-DevKitC V4 38-pin WROOM-32E**; no inferir
pinout por aspecto. Desconectar alimentación de motores y actuadores; sólo USB.

La librería de tercero se sirve desde Pages, pero todo dato serie queda local.
El script de módulo usa `crossorigin="anonymous"`; los assets son same-origin,
no se requiere CDN ni se concede a un tercero acceso al puerto por CORS.
No hay subida de código/firmware privado, contraseñas/tokens ni telemetría propia.
GitHub recibe solicitudes web normales de activos públicos. npm y repositorios
upstream se consultan en CI para dependencias: nada del código privado del
usuario se envía a un servicio de flashing.

## Validar localmente (sin placa)

Desde raíz, Node 22/Python 3.11/PlatformIO disponibles:

```powershell
Push-Location webflash
npm ci --ignore-scripts --registry=https://registry.npmjs.org
Pop-Location
$env:PLATFORMIO_EXTRA_SCRIPTS = 'post:../scripts/build-webflash-proof.py'
python -m platformio run -d firmware -e esp32
python -m platformio run -d firmware -e esp32 -t webflash-proof
python -m platformio run -d firmware -e esp32 -t buildfs
node scripts\build-webflash.cjs
node --test tests\webflash.test.cjs
node scripts\build-webflash.cjs --validate build\webflash
```

Si el generador indica avisos/licencias upstream ausentes, ejecutar también el
paso “Preserve upstream source and license” del workflow antes de empaquetar.
Los binarios, herramientas y outputs van a `build/` y `.pio/` ignorados;
node_modules de webflash está ignorado. No incorporar binarios al Git.
Instalar siempre desde el directorio webflash: no ejecutar npm install sin
paquete desde raíz con --prefix, ni añadir dependencias file:.. o links locales.
El generador rechaza dependencias no registry y junctions/symlinks al recorrer
avisos para evitar recursion accidental dentro del proyecto/SDK Android.
Para una copia manual, servir **build\webflash** por HTTPS o localhost:
no abrir `webflash/index.html` en `file:` ni asumir que los activos existan.
Los errores de compilación o verificación detienen generación/despliegue.

## Licencias y educación

Autores: **Anatol EA5KAO**, **Diego EA5JEF**, **Pedro Roca Molina**;
agradecimiento a [Bricohams](https://bricohams.org/).
Ver `AUTHORS.md`, `ACKNOWLEDGEMENTS.md`, `DISCLAIMER.md` y `NOTICE.md`.
Bricohams se cita como organización de divulgación científica para niños
y adolescentes. La autoría actual no sustituye la de bibliotecas ni fuentes
consultadas: las referencias no implican colaboración, patrocinio ni aval.
Software original MIT; SGP4 MIT verificado en biblioteca instalada;
ESP Web Tools/NimBLE-Arduino Apache-2.0; ArduinoJson MIT; TinyGPSPlus/Arduino-ESP32 LGPL-2.1
y SDK con sus avisos originales. No declarar todo el binario MIT-only.
Bundle conserva textos, fuente exacta de dependencias, objetos relinkables y
links/versiones upstream; mantenerlos al redistribuir. Revisar obligaciones
de SDK/componentes antes de comercializar. Hardware conserva su licencia
CERN-OHL-S-2.0 separada.

Uso educativo con supervisión adulta para menores; no montaje peligroso por
niños y nunca RF/TX sin autorización/licencia aplicable. Ninguna prueba de CI
es evidencia de aceptación física, de compatibilidad eléctrica o RF.
