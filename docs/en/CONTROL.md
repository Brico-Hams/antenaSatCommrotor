# Autonomous Control — ESP32 Prototype

Original project by Anatol (EA5KAO), Diego (EA5JEF), and Pedro Roca Molina,
in the Bricohams educational context (`https://bricohams.org`). See the project
AUTHORS, ACKNOWLEDGEMENTS, and DISCLAIMER for attribution and limitations.
References and dependencies retain their own authorship; no endorsement is
implied. Children/adolescents require adult supervision and must not transmit
without applicable authorization/licence.

## Scope and status

The ESP32 calculates **real SGP4**, not a Kepler approximation, from TLEs stored
in LittleFS. NMEA GNSS provides UTC and location; the browser only displays and
sends commands. No Node server, cloud, or computer is required in the field.
The 145/435 MHz dual-band antenna shares pointing. PTT/CAT are **disabled**:
RT3S full duplex or CAT is not assumed. Configure OpenGD77 and its channels/
Doppler independently; displayed offsets use nominal 145 and 435 MHz and do
not replace a frequency plan.

This is a software-compiled and tested prototype, **not field-validated**.
Motors, GNSS, RF, TLS with all three servers, encoders, latency under hostile
traffic, and a certified safety procedure have not been tested. This is not a
functionally certified emergency stop.

The controller does not authorize any field load or wind condition. The
mechanical example of 8 m/s, 0.06 m² area, and 0.25 m arm **does not meet** the
reported design-calculation safety margin; it must not be treated as an
operational limit. The 80,000-microsteps/revolution configuration assumes an
effective 25:1 reducer: verify both stages, keyed interfaces, and actual ratio
on a bench. Antenna mass/balance and ASA-part stiffness require measurement;
a valid STL mesh or successful compile does not prove mechanical capacity.

Project-owned files:

* `firmware/platformio.ini`, `firmware/include/board_config.h`
* `firmware/include/control_logic.h`, `firmware/src/main.cpp`
* `firmware/include/ble_protocol.h` (shared framing and authentication)
* `firmware/.gitignore` (excludes local tools/builds)
* `web/index.html` (fully offline Spanish interface)
* `tests/control_logic/test_native/test_main.cpp`
* `tests/control_sgp4.cpp`, `tests/control_web.test.cjs`
* this document

## Verified dependencies and build

PlatformIO Core 6.1.18; `espressif32@6.10.0`, `esp32dev` (classic ESP32,
WROOM, 4 MB flash), Arduino ESP32 **2.0.17**, package
`framework-arduinoespressif32@3.20017.241212`, Xtensa
`8.4.0+2021r2-patch5`; ArduinoJson 6.21.5; TinyGPSPlus 1.1.0.
Bluetooth: **h2zero/NimBLE-Arduino 1.4.3**, root Apache-2.0 licence checked at
`https://github.com/h2zero/NimBLE-Arduino/blob/1.4.3/LICENSE`. Preserve its
licence/notices and those for the Apache NimBLE stack when distributing binaries.
Classic Bluetooth and Bluedroid are not used; at most one BLE connection.

SGP4: [Hopperpop/Sgp4-Library](https://github.com/Hopperpop/Sgp4-Library)
1.0.3, commit **7c82d31f9d9a286acde5ef55da8308fc93d2ba96**.
Actual signatures of `Sgp4::init`, `site`, `findsat`, `satrec.error`, and the
pinned source's TEME-to-observer calculation were checked. The upstream wrapper
selects WGS84; its internal buffers are explicitly initialized and mutable
copies of the lines are passed. The independent test uses WGS72 to compare with
Vallado verification vector 00005:
R=(7022.46529266,-1400.08296755,0.03995155) km,
V=(1.893841015,6.405893759,4.534807250) km/s.
Reference: [CelesTrak SGP4 software](https://celestrak.org/software/vallado-sw.php).
The library retains its notices/licences in the dependency manager; its sources
are neither vendored nor modified.

This subsystem's **original software** is published under MIT as selected by
the user and recorded in the project NOTICE; original hardware is under
CERN-OHL-S-2.0. This does not assign MIT to the linked firmware as a whole.
These licences do not relicense libraries, tools, or external references; each
dependency retains its own licence. Unknown-licence sources are not redistributed
and no remote publication has occurred.
The pinned SGP4 commit's `LICENSE` was checked: **The MIT License (MIT),
Copyright (c) 2016**, requiring preservation of copyright and permission notices
in copies or substantial portions, including a distributed binary containing it.
Public evidence:
`https://github.com/Hopperpop/Sgp4-Library/blob/7c82d31f9d9a286acde5ef55da8308fc93d2ba96/LICENSE`.
Its README also identifies Grady Hillhouse's coordinate transformation as MIT.
No GPL was detected in this dependency; this check does not relicense other
libraries, Arduino ESP32, or tools. Before distributing a binary, preserve
notices for **all** linked dependencies and review obligations for the exact
framework versions.

With PlatformIO installed in a development environment:

```powershell
Set-Location .\firmware
pio run -e esp32
pio run -e esp32 -t buildfs
pio run -e esp32 -t upload
pio run -e esp32 -t uploadfs
pio device monitor -b 115200
pio test -e control_native
```

The native test needs GCC/G++ on PATH. This machine lacked usable Python,
PlatformIO, and GCC; embedded Python 3.11.9, PlatformIO 6.1.18, and Zig 0.13.0
were downloaded **only under `firmware/.tools`**, not installed globally.
VS Code's Python environment configuration services had no implementation.
Embedded Python required local esptool 4.5.1 because its isolation prevents
importing the package from PlatformIO's external script.

Tests actually run:

* ESP32 compile/link and `firmware.bin` generation: **SUCCESS**.
* LittleFS build containing `index.html`: **SUCCESS**.
* Six Unity tests compiled/run with Zig: **6 PASS, 0 failures**:
  limits/coordinates, UTC/leap years/expiry, TLE checksums/epoch, speed/
  acceleration/stop/positive and negative motion limits, USB credential
  validation, and BLE frames/authentication (no real secrets).
* Executable against pinned SGP4: Vallado epoch vector **PASS**, tolerance
  1 m position and 1 mm/s velocity.
* `node --test tests/control_web.test.cjs`: **PASS** (syntax, DOM IDs, eight
  authenticated actions, satellite names rendered without HTML, and static
  firmware interlock checks; no timing or hardware simulation).
* `pio test -e control_native` initially failed because GCC was absent; the same
  Unity code was run with Zig as an alternative. That command is not represented
  as passing.

Binaries in `.pio/build/esp32` are development artifacts, not proof of flashing
or physical operation. Uploading LittleFS replaces its contents: export TLEs
before updating the filesystem.

### WebFlash/CI bundle (classic ESP32 only)

CI can compile without `secrets.h`: `board_config.h` has empty credentials and
`carrierVerified=false`. This safe image starts DISARMED, with **no operational
AP** until local USB provisioning; configuring the AP does not require a rebuild.
Do not embed private passwords/tokens in a public GitHub Pages image.

### Local USB provisioning (public image)

Disconnect motors/RF. Open a local 115200 serial console (ESP Web Tools console
or local terminal without logging/telemetry), and send each JSON on a line ending
in LF:

1. `{"cmd":"setup"}` disconnects Wi-Fi, forces ENABLE OFF and provisioning
   fault, invalidates homing/calibration, and blocks the API.
2. `{"cmd":"config","ssid":"Chosen name","password":"YOUR_PRIVATE_PASSWORD","token":"YOUR_RANDOM_PRIVATE_TOKEN"}`.
   Substitute values: SSID 1..32, password 12..63, random token 24..128
   printable ASCII characters. Optional `staSsid` and `staPassword` (>=8);
   omitting them removes stored STA settings. Do not send secrets to remote
   services or publish console history.
3. Only after physically validating board/driver/polarities:
   `{"cmd":"carrier","verified":true}`. This does not start or arm motors.
   `verified:false` revokes hardware authorization at the next boot.
4. `{"cmd":"reboot"}`. It starts DISARMED; connect to the configured secure AP
   and open `http://192.168.4.1`; enter the token on the page.

Parser maximum: 768 bytes/line; responses do not repeat secrets. Credentials
persist in private NVS, **not encrypted**: physical flash access can extract
them; this prototype does not configure flash encryption/secure boot. NVS
configuration is not a full transaction: if writing fails, remain in SETUP and
retry. This console does not support configuring a CA PEM; HTTPS requires current
compiled-in roots, while manual TLE import works with the public image. An
operator with USB access can change configuration; control physical access.
Homing/calibration are never saved, even when carrier verification is saved.

### Secure Bluetooth LE and Android

The image permits simultaneous Wi-Fi AP and BLE; coexistence and physical
latencies are unmeasured. BLE is disabled by default. In local USB SETUP add:
`{"cmd":"ble","enabled":true,"passkey":YOUR_PRIVATE_SIX_DIGIT_NUMBER}`.
Use a locally selected number 100000..999999, not a passkey published in this
document. It is not printed. `enabled:false` disables BLE after reboot.
Changing BLE configuration deletes stored bonds at next startup. The console
continues to force motors OFF; then send `{"cmd":"reboot"}`.

Pair Android using the system dialog and private passkey; **Secure Connections,
bonding, and MITM are mandatory**; never accept an insecure alternative. Also
enter the local API token in the app; it is not sent to the cloud. Every command,
including STOP/status, requires encrypted/authenticated/bonded link and correct
token. Radio/NVS are not secure boot: protect physical access.

GATT **v1**, advertised name `PortableSatStation`:

* Service: `c8200001-4e53-4253-9000-000000000001`
* RX write **with ATT response**, encrypted/authenticated:
  `c8200002-4e53-4253-9000-000000000001`
* TX notifications: `c8200003-4e53-4253-9000-000000000001`

Subscribe to TX before sending. Minimum MTU 23 works without negotiating a
larger MTU. Each frame <=20 bytes: byte 0=0x53; byte 1 flags START=1, END=2
(3 for a single frame); bytes 2/3 uint16 little-endian sequence, starting at 0
and incrementing by 1; bytes 4..19 contain 1..16 bytes of UTF-8 JSON. No NUL or
unknown flags. A command executes only after valid END, schema, and authentication.
Request <=2048 bytes, assembly timeout 3 s, one request/response in flight.
Out-of-order/interleaving/overflow produces an error, not partial execution.

Complete request:
`{"v":1,"id":1,"method":"POST","path":"/api/calibrate","token":"PRIVATE_TOKEN","body":{"trueAz":0,"levelConfirmed":true}}`.
ID is a positive integer **increasing per connection**. GET uses `body:{}`.
Complete response:
`{"v":1,"id":1,"code":200,"data":{"message":"..."}}`.
`data` uses exactly the HTTP JSON object; framing errors without recoverable ID
use id 0. Response <=8192 bytes; larger catalogs return 413 and must be queried/
imported using HTTP. 429 means queue busy; 408 is timeout. Wait for END of the
previous response before the next request, except authenticated STOP may be
prioritized and interrupt the previous response.

Same handlers/interlocks for `/api/status`, site, home, move, stop, clear,
calibrate, select, track, passes, and TLE GET/POST. `/api/update` over BLE
returns 409: HTTPS updates are HTTP-only and require idle state. BLE TLE accepts
only a subset fitting in 2048 bytes; it never silently truncates. Firmware does
not duplicate motion logic.
STATUS adds `controlOwner` (HTTP/BLE/none), `bleConfigured`, `bleConnected`,
`bleSecure`, and `encoderZeroVerified`.
STATUS identifies compatibility using `apiVersion=2`, `protocolVersion=1`,
and `firmwareVersion="0.3.0-prototype"`; use this authenticated handshake; there
is no separate auth route.

API 2 (Bricohams Android integration) adds `POST /api/time`
(`{"utcMs":...}`, authenticated): without GNSS, a trusted app sets UTC for
10 min; GNSS UTC always has priority (409) and jumps above 2 s are rejected
while motors run. STATUS adds `timeSource` (`none`/`gnss`/`app`) and the
mechanical profile `microsteps`, `transmissionRatio`, `stepsPerDegree` and
`maxDegPerSecond`. The PlatformIO environment `esp32_nema17` builds the low-cost
profile: reused NEMA17 with TMC2209 at 1/8, same 25:1 belts, 40000
microsteps/rev and 6.0 deg/s maximum. Compiled; not tested on a board or rotor.
Mutations from the other transport during movement return 409; authenticated
STOP remains available. BLE disconnection during manual HOME/MOVE causes a
fault and invalidates homing; autonomous TRACK continues subject to GNSS/TLE/
interlocks without a connected phone.

Notifications are not guaranteed to be delivered: the app must detect sequence/
timeout and re-query status; never assume execution based on ATT write. Physical
E-stop and the safety task do not depend on the phone or transport. If motor-task
duration exceeds 20 ms, it faults; Wi-Fi/BLE coexistence is not certified.

### Large TLE transfer from Android (same v1 protocol)

The phone downloads TLEs over HTTPS from allowed providers and transfers **TLEs**,
not trajectories: SGP4, pass calculation, and tracking remain on the rotor. The
catalog supports <=100 satellites/48 kB; select a subset if larger. No silent
truncation. New shared HTTP/BLE POST routes:

| Route | Body / result |
|---|---|
| `/api/tle/begin` | `{length:1..48000,sha256:"64 lowercase hex"}` -> `{message,uploadId}` |
| `/api/tle/chunk` | `{uploadId,offset,text}`; text 1..512 UTF-8 bytes; exact sequential offset -> `{message,received}` |
| `/api/tle/commit` | `{uploadId}` -> exact SHA-256/length, TLE validation, atomic rename; 200 or 400; previous cache preserved on failure |
| `/api/tle/abort` | `{uploadId}` -> 200, preserves cache |
| `/api/catalog` | `{offset:0,limit:10}`; limit 1..10 -> `{total,nextOffset,satellites:[{id,name,epoch,fresh}]}`; final nextOffset=-1 |

Hash and offset are calculated over exact transferred text bytes (normalize
before calculating SHA-256). Begin does not replace the cache; commit occurs
only after all chunks and matching hash. Transfer has HTTP/BLE ownership; other
mutations are blocked with 409 and motors cannot start while active. After
60 seconds inactive transfer RAM is aborted without changing the cache.
BLE disconnection immediately aborts its RAM transfer and releases ownership
without changing persisted cache.
Hash/validation/flash work runs in loop/handlers, **never in BLE callbacks**;
the disconnect callback only releases transfer RAM, while the RX callback only
assembles and enqueues a size-bounded validated request. `/api/passes` queries
remain incremental/idle-only; Android polls `calculating` until false. The app
does not need or implement SGP4 to provide a trajectory to the rotor.

### Web/app calibration assistant (procedure)

The web interface shows steps and HOME/motor/level/north/encoder/site/UTC status.
Perform HOME with physical contact; wait for READY, move EL to 0, level with an
instrument, and establish **true north** (not stationary GNSS). With AS5600
enabled, output zero positions are taken at HOME and `encoderZeroVerified` is
required. POST calibrate requires homed, idle/ENABLE OFF, EL=0, and confirmed
level; offset=true heading minus mechanical AZ. No automatic IMU/magnetometer
sensor is implemented. Repeat calibration after reset/rehoming/mount change.

```powershell
pio run -d firmware -e esp32
pio run -d firmware -e esp32 -t buildfs
```

Layout was checked against the pinned framework's `default.csv`; classic ESP32
DevKitC V4 WROOM-32E, 4 MB flash, no PSRAM. Do not reuse on S3/C3/WROVER.

| Part | Build path | Hex / decimal offset |
|---|---|---|
| bootloader | `firmware/.pio/build/esp32/bootloader.bin` | 0x1000 / 4096 |
| partition table | `firmware/.pio/build/esp32/partitions.bin` | 0x8000 / 32768 |
| initial OTA | `$PLATFORMIO_CORE_DIR/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin` | 0xe000 / 57344 |
| application | `firmware/.pio/build/esp32/firmware.bin` | 0x10000 / 65536 |
| LittleFS web | `firmware/.pio/build/esp32/littlefs.bin` | 0x290000 / 2686976 |

Filesystem partition is named `spiffs` but formatted as LittleFS, size 0x160000
(1,441,792 bytes). **Include LittleFS** or `/` returns 503. ESP Web Tools
manifest may use the five parts with offsets above; for a combined binary, use
esptool 4.5.1:

Before any flash, disconnect motors and RF and use a protected supply. A
prototype image does not certify or approve the connected board.

```powershell
esptool.py --chip esp32 merge_bin -o combined.bin --flash_mode dio --flash_freq 40m --flash_size 4MB `
  0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin `
  0x10000 firmware.bin 0x290000 littlefs.bin
```

Run in a folder containing all five parts; the combined image is written at
offset **0x0**. The bundle retains notices for linked dependencies and does not
relicense the whole as MIT. Flashing the filesystem or erasing the chip destroys
local TLE/NVS: a WebFlash interface must clearly warn the operator.

## Mandatory wiring and provisioning

`board_config.h` fixes the agreed map for **38-pin ESP32-DevKitC V4,
WROOM-32E without PSRAM**. `carrierVerified=false` keeps motors/GNSS disabled
until the carrier is physically checked and confirmed through USB console
`cmd carrier` (or set true in a private build). Not suitable for WROVER, S3/C3,
or modules with different header layout. Electrically verify the actual map
before flashing. Checks reject duplicates, flash/reserved/strapping/console
pins, output-only-incompatible pins >=34, and bus/UART overlap. GPIO34–39 have
no internal pull-up: install external resistors on every safety input.

Net-to-GPIO map frozen with PCB design:

| Interface | GPIO |
|---|---|
| AZ STEP / DIR | 26 / 27 |
| EL STEP / DIR | 14 / 13 |
| Common active-LOW ENABLE | 25 |
| NC E-stop | 34 |
| AZ min / max NC | 35 / 36 |
| EL min / max NC | 39 / 32 |
| GNSS RX / TX of ESP32 | 16 / 17 |
| AS5600 AZ SDA / SCL | 21 / 22 |
| AS5600 EL SDA / SCL | 18 / 19 |

GPIO16/17 are authorized only for WROOM-32E, where available; do not use
WROVER/PSRAM. External 10 kΩ pull-ups on ENABLE and five NC inputs.
Agreed driver: **Watterott TMC2209 SilentStepStick in standalone mode**,
MS1=MS2=3.3 V for 1/16 per its module reference; motor UART/DIAG are not wired
or controlled by this firmware. Check module revision and header orientation
against PCB documentation and manufacturer before insertion.

* External STEP/DIR driver per axis, current set for NEMA14 and appropriately
  rated supply. Do not power the motor from ESP32. Physically set **16
  microsteps**, 200-step/revolution motor, planetary 25:1:
  **80,000 output microsteps/revolution**, 222.222… microsteps/degree.
  Current lightweight BASE replaces the planetary with **two purchased GT2
  stages of 20:100 teeth**: 5×5=25:1, retaining those commands per revolution.
  Planetary is an earlier optional variant, not the base transmission. Verify
  tooth counts, microsteps, and installed ratio; no printed GT2 profiles or
  undocumented pulleys are assumed.
* Common active-LOW ENABLE, **external pull-up keeps it OFF even during reset**.
  Adapt circuit/code first if driver polarity differs.
* E-stop is **normally closed to ground**; open cable/HIGH faults. It must
  physically cut driver power/enable independently of firmware. Input only
  monitors that circuit.
* Four physical **NC-to-ground** limit switches: AZ min/max and EL min/max.
  HIGH/open means limit reached or wire interrupted. An opening during homing
  cannot distinguish failure from actual contact: procedure requires release
  and re-approach but still needs physical verification. Use supervised hardware
  for a permanent installation.
* AZ minimum is **-180°**, maximum **+180°** mechanical. EL minimum 0°,
  maximum 90°. Adjust switches, physical margin, and real references with tools;
  software cannot determine their installed positions.
* Configurable NMEA GNSS UART at 9600, 3.3 V levels, assigned RX/TX.
* Prefer two AS5600s **at the output**, not at motor before reducer. I2C address
  0x36 on separate buses, pull-ups to 3.3 V, `encoders=true`, configured pins
  and encoder polarities. Magnet presence/range are checked; reference at homing
  and fault after three discrepancy >3°/loss readings, 100 ms sampling, 5 ms
  I2C timeout. Angular resolution ~0.088°, does not measure backlash/stiffness.
  Absolute encoder does not distinguish full rotations; limit switches and
  wiring remain mandatory.

Configure AP password >=12 and <=63 characters and a unique random token >=24
(preferably 32 random bytes encoded). Empty values disable AP/API. Do not publish
firmware/config with real secrets. Optional STA SSID/password and **current CA
PEM** for providers in `tlsRoots`; no invented CA or `setInsecure()`. STA is
outbound-only: do not expose port 80 to an untrusted network. Local HTTP carries
the token over protected Wi-Fi and has no local TLS; restrict access to authorized
operators.

## Operation and safety

1. Always starts **DISARMED, ENABLE OFF**. Homing is never persisted.
2. Check E-stop/wiring; command HOME. AZ seeks minimum, backs off 700
   microsteps to release, and approaches again; then EL likewise. Debounce
   30 ms, timeout **240 s per axis**, fault if expected travel does not find/
   release contact. Do not substitute another limit for minimum.
3. Move to known position at EL=0. Level base with a level/inclinometer; set
   current **true heading** from a reliable reference.
   `/api/calibrate` computes offset=true heading minus mechanical AZ.
   Stationary GNSS **does not provide heading or leveling**.
   Manual calibration is explicit fallback; automatic IMU/compass is not
   implemented.
4. UTC needs GNSS messages updated <3 s and valid year 2024–2099. Automatic
   location needs fix and altitude <5 s; persisted manual site permits fixed
   site, **not a substitute for GNSS UTC**. UTC jump >2 s during motion faults.
5. Import TLE, select satellite, query passes. Reject bad checksums, mismatched
   NORAD number, invalid orbital fields, and unsupported format. Numeric NORAD
   only (no Alpha-5/OMM), maximum **100 satellites/48 kB**.
6. Move near expected AZ/EL; TRACK starts only above horizon and requires
   calibration, homing, UTC, site, and fresh TLE. Acquisition/error >15° faults
   to avoid unexpected search rotation.
7. STOP halts motion and disables drivers; it does not clear faults. STOP during
   homing invalidates reference. Hard fault invalidates homing/calibration and
   requires CLEAR with E-stop closed, HOME, and new calibration. After manual
   movement without power or mounting change: CLEAR/HOME/calibrate again.

AZ is a mechanical coordinate limited to ±180; true heading is transformed
using calibration offset. There is no unlimited unwrap. Jumps >180° across the
cable limit fault/reposition. EL 0..90. Maximum speed 500 microsteps/s
(=2.25°/s), acceleration 300 microsteps/s². Separate motor task, at most one
pulse per iteration and no catch-up bursts; dt>20 ms while moving faults.
Step/direction pulses have 3 µs margins. Prediction task processes four
positions per cycle and does not block for an entire pass.
Pass query/start is rejected while motors move; pending calculation pauses
during movement. TLE download is also rejected during movement. Physical
monitoring runs independently of HTTP server, in addition to mandatory physical
power cutoff; worst-case hardware response remains unmeasured.
Adequate speed near zenith is not guaranteed: test tracking/backlash on a bench;
there is no certified advance plan for mechanically infeasible passes.
TRACK rejects EL>=89° and faults on entering that zone. SGP4 propagated 1 s
ahead checks AZ/EL rates; exceeding 2.25°/s stops with fault. This does not
guarantee acceleration margin or replace physical testing. Disabled motors at
rest may lose position; with encoders discrepancies are monitored, without
them the operator must rehome after any displacement.
A lightweight belt variant is backdrivable: STOP, fault, reset, and idle disable
the driver and **do not hold the antenna by electrical torque**. Balance load
and use an independent mechanical brake/retainer to prevent falling or hazardous
rotation when power is cut. AS5600 detects discrepancies but does not retain
load. The <=3 kg target excludes radio/tripod and includes power; it is not
measured mass or load authorization.

## Local HTTP API

All `/api/*` routes, including GET, require header
`X-Control-Token: <configured token>`. No CORS, GET state changes, wildcards, or
cookies; token is held only in page memory (not localStorage). POST uses
`Content-Type: application/json`; responses are JSON. 200 success, 202 command
started, 400 invalid schema, 401 token, 409 precondition, 502 download failed.
Responses are `{"message":"..."}` or `{"error":"..."}`. Web stop does not
replace physical E-stop.

| Method/route | Body / result |
|---|---|
| GET `/api/status` | mode/fault, hardwareConfigured, enabled, homed, calibrated, level, utc/utcValid, siteValid/manualSite/lat/lon/alt, northOffset, azMechanical/el, skyAz/skyEl/rangeKm/rangeRateKmS, doppler145Hz/doppler435Hz, trackingBlocker, selected, download, staConnected, encoders, pttCat=false |
| POST `/api/site` | `{"manual":true,"lat":40.4,"lon":-3.7,"alt":650}`. All required; false returns to GNSS. Rotor stopped; invalidates orbital calculations/pass list |
| POST `/api/home` | `{}`. Asynchronous physical homing; calibrates mechanical position only |
| POST `/api/move` | `{"az":0,"el":0}`. AZ is **mechanical**, not true heading; calibration/UTC not required for setup |
| POST `/api/stop` | `{}`. Disables without clearing FAULT |
| POST `/api/clear` | `{}`. Clears fault with E-stop closed; invalidates homing/calibration |
| POST `/api/calibrate` | `{"trueAz":0,"levelConfirmed":true}`. Current true heading; EL=0 and idle required |
| GET `/api/tle` | `{"satellites":[{"id":0,"name":"...","epoch":unix,"fresh":true,"line1":"...","line2":"..."}]}` |
| POST `/api/tle` | `{"text":"name\n1 ...\n2 ...\n"}`. Full validated persistent replacement; no partial merge |
| POST `/api/select` | `{"id":0}`. Index in current list, not NORAD; resets on import |
| GET `/api/passes` | Starts/queries calculation: `calculating`, `stepSeconds=10`, `passes:[{aos,los,peak,maxEl,partial}]`; Unix UTC times. 24 h window, geometric 0° horizon, 10 s resolution, may miss very short passes. 60 s cache; partial marks truncated window |
| POST `/api/track` | `{}`. Tracks currently selected object (does not schedule future pass); ends below horizon |
| POST `/api/update` | `{"provider":"celestrak"}` or `amsat` / `pe0sat`; idle, STA connected, GNSS UTC, and CA PEM required |

Exact providers; arbitrary URLs are not accepted:

* CelesTrak amateur: `https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle`
* AMSAT: `https://www.amsat.org/tle/current/dailytle.txt`
* PE0SAT: `https://tle.pe0sat.nl/kepler/mykepler.txt`

HTTPS validates hostname, chain, and GNSS time. Redirects are disabled;
positive Content-Length <=48 kB is required (chunked is rejected), connect
timeout 5 s, read timeout 8 s. Format/TLS/DNS/list-limit/response failures are
**explicit**; preserve/use a manual subset if a provider exceeds 100 satellites.
No claim is made that the ESP32 has downloaded all three responses successfully.
An isolated AP cannot access the Internet.

LittleFS writes `/tle.new` then atomically renames to `/tle.txt` after validation;
on error, the previous cache remains in RAM/destination. Never auto-format if
mount fails. Site/offset are in NVS; level confirmation/homing/calibration are
**not** restored. Stale/future TLE inhibits tracking (>14 days old or >1 day
future), even if the download itself was recent.

## Tests still required before using a real antenna

With motors disconnected: validate ENABLE polarity, physical E-stop during
reset and processor lockup, open-circuit response, each limit and timeout;
direction, microsteps/reducer, and AS5600 mounting. Measure maximum latency
under HTTPS/SGP4/Wi-Fi. Test GNSS loss, UTC jump, corrupt/old TLE, write failure
and power loss, magnet/bus loss, jam, backlash, cable limit, and zenith.
Then bench load and independent angular reference; only after that, attended
low-power RF tests. There is no persistent auto-home, dual-GNSS heading, IMU,
dynamic wind profile, automatic pass queue, full-duplex control, or transmit
automation.
