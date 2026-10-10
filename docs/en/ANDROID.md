# Native Android: Local BLE Control

Package `org.bricohams.portablesatstation`, native Kotlin, minimum Android 8/API 26,
target/compile SDK 35. Spanish resources by default; English translation follows
the device language. No React, WebView, orbital calculations on the phone,
cloud control service, analytics, phone geolocation, CAT, or PTT.
**INTERNET is authorized solely to download public TLEs over HTTPS**
from the three providers listed below; control and transfer remain local BLE.

**Prototype not field-validated.** Compilation does not validate wiring,
mechanics, RF, functional safety, or rotor accuracy. Use a physical emergency
stop, protected power, verified limits, and adult supervision.

Current authors: **Anatol EA5KAO, Diego EA5JEF, and Pedro Roca Molina**.
[Bricohams](https://bricohams.org) is an educational-outreach reference,
not a certification or implied endorsement by third parties. See also
[authors](AUTHORS.md) and the [disclaimer](DISCLAIMER.md).

## Build and test

On Windows, from `android`:

```powershell
$env:JAVA_HOME = 'path\to\jdk-17'
$env:ANDROID_HOME = 'path\to\android-sdk'
$env:ANDROID_USER_HOME = Join-Path $PWD '.tools\android-user'
.\gradlew.bat --no-daemon testDebugUnitTest lintDebug assembleDebug
Get-FileHash .\app\build\outputs\apk\debug\app-debug.apk -Algorithm SHA256
```

Linux/macOS: `chmod +x gradlew`, then
`./gradlew --no-daemon testDebugUnitTest lintDebug assembleDebug`.

Pinned tools: **AGP 8.7.3 / Kotlin 2.0.21 / Gradle 8.9 / JDK 17 /
platforms;android-35 / build-tools;35.0.0**.
Verify the Gradle distribution using SHA-256
`d725d707bfabd4dfdc958c624003b3c80accc03f7037b5122c4b1d0ef15cecab`.
`gradle-wrapper.jar` is the official Gradle 8.9 binary, SHA-256
`498495120a03b9a6ab5d155f5de3c8f0d986a449153702fb80fc80e134484f17`.
Verification sources:
[distribution](https://services.gradle.org/distributions/gradle-8.9-bin.zip.sha256),
[wrapper](https://downloads.gradle.org/distributions/gradle-8.9-wrapper.jar.sha256).

Isolated local tools were provisioned under `android\.tools` (ignored):
Microsoft JDK 17.0.16+8 from `aka.ms/download-jdk`, ZIP SHA-256
`53f0c9ec64811a9ab968747076653e5500115db7230d244e4ec53577ca5ec8fc`;
Android command-line tools 19.0, file
`commandlinetools-win-13114758_latest.zip`, SHA-256
`98b565cb657b012dae6794cefc0f66ae1efb4690c699b78a614b4a6a3505b003`.
Its SHA-1 `54a582f3bf73e04253602f2d1c80bd5868aac115` was checked against
`https://dl.google.com/android/repository/repository2-1.xml`.
Global Java/SDK installations were not modified, and private source code was
not uploaded to build. `ANDROID_USER_HOME` keeps preferences and the AGP-generated
debug key under `android\.tools\android-user`; the debug key is not versioned
or represented as the author's publication key/certificate.

The `.github/workflows/android.yml` action runs JVM tests, lint, and compilation,
and publishes the **debug** APK and its hash as a downloadable GitHub artifact.
A debug APK uses a tool-generated debug key; it is **not an official
distribution signature** or a fabricated certificate. There is no automatic
store publication. A release distribution requires the author's actual private
key outside the repository through an independent protected process.

### Local evidence (October 10, 2026)

`testDebugUnitTest lintDebug assembleDebug`: **BUILD SUCCESSFUL**.
**29 JVM tests, 0 failures/errors; lint: “No issues found”.**
Coverage includes UUID/version/limit checks against actual controller code,
exact MTU 23/185 framing, UTF-8, size/sequence limits, non-numeric/non-finite
input, failed authentication, malformed status, incompatible versions, call
ordering, paginated catalog, TLE checksum/epoch, an explicit provider subset
with more than 100 entries, atomic cache, HTTPS allowlist without redirects,
and begin/chunk/commit/abort with exact offsets. App **0.2.0-prototype**,
versionCode **2**.

APK: `android\app\build\outputs\apk\debug\app-debug.apk`.
SHA-256:
`47997a78abd87b3aa4e26a33106f9b122a817121dd02c2abc7d6b72717ca399b`.
`apksigner verify` completed; `aapt dump permissions` confirms BLE, location
only through API 30, and INTERNET for HTTPS downloads. This APK is debug-signed,
not a release distribution. Its hashes do not certify hardware or BLE.
Reports: `android\app\build\reports\tests\testDebugUnitTest` and
`android\app\build\reports\lint-results-debug.html`.

The app's **actual HTTPS downloader and parser were run locally on JDK 17**
against the AMSAT endpoint: HTTP 200, **97 satellites, 14434 bytes**, SHA-256
`ec291294636090d712fc901e4a7e3fa15bbeb8366fb771d7aad131b5c8db1ce9`.
This was not only a simulated test response; no private data was uploaded.
CelesTrak and PE0SAT timed out while connecting on this network: no successful
download is claimed and TLS was not weakened or redirected to another URL.
Provider errors preserve the cache. This test **does not** validate TLS/radio
on a real Android device or physical BLE transfer. Provider data changes daily.

## Use and safety

1. Physically configure the rotor BLE with its local passkey and API token.
2. Enter the token in the password field. Saving is explicit; Android Keystore
   retains a non-exportable AES-GCM key and SharedPreferences stores only the IV
   and ciphertext. App backups are disabled.
3. Read the permission explanation and scan. Android 12+ uses
   BLUETOOTH_SCAN/CONNECT; earlier versions require location permission for BLE,
   but no location API is called and no geolocation is obtained or uploaded.
4. Explicitly select the physical device. Android displays the pairing dialog.
   Bonding and token authentication are separate requirements.
5. Connecting and authenticating never sends homing or movement commands and
   never enables the motors.
6. Check status before using the motors. Rehoming/startup requires physical
   calibration again: instrumented leveling, EL output at 0, and measured true
   heading (geography/sun or a compass corrected for declination, away from
   metal). Stationary GNSS does not measure heading. Persistent guide progress
   **is not** calibration; authenticated firmware status is authoritative.

Scanning stops after 15 seconds and when leaving the screen. Explicit
disconnection is available. When the app enters the background, the session
closes; there is no automatic reconnection or automatic motor command on return.
A Bluetooth disconnection **does not replace the physical stop**. Tokens are
not logged, and arbitrary authentication exceptions/JSON are not displayed.
Preferences/files are also excluded from backup and device transfer; the window
blocks screenshots/token previews. These controls do not protect against a
compromised phone/keyboard/OS or root access, and do not prove hardware-backed
Keystore on every phone.

## TLE: phone download and atomic BLE transfer

Download can happen **before connecting BLE**. Choose CelesTrak, AMSAT, or PE0SAT
in the app and tap Download. Only these URLs are allowed:

- `https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle`
- `https://www.amsat.org/tle/current/dailytle.txt`
- `https://tle.pe0sat.nl/kepler/mykepler.txt`

The GET request contains no token, cookies, position, private files, or uploaded
data. There is no analytics. The provider sees the source IP and the ordinary
public request. System TLS/hostname/CA verification remains enabled: no
`TrustAll`, HTTP, user-provided URL, redirects, or insecure fallback. A redirect
or non-200 HTTP status is shown as an error and preserves the last catalog.
Certificates are not overridden and new destinations are not followed.
Connect/read timeout: 15 seconds; reading is bounded by size and a 45-second
deadline between reads. Cancel/background cancels the task, without reconnecting
or publishing. Without network, a file can also be imported through Android's
file picker (`ACTION_OPEN_DOCUMENT`), without general storage permission.

Maximum persisted/transferred size is **48000 bytes, 100 satellites, 64-character
ASCII names, unique five-digit numeric NORAD IDs**, two 69-character lines with
NORAD checksums, matching identifier, and valid epoch. The controller's numeric
fields and ranges are checked; SGP4 is not run on the phone. CRLF is normalized
to LF and a validated canonical catalog is retained. If a provider/file of up to
48000 bytes contains more than 100 valid entries, an explicit selector opens
(up to 300 candidate entries in RAM): choose **1–100**, with no preselection
and no silent truncation. Cancel leaves the previous cache unchanged. Only the
chosen subset is revalidated, saved, and transferred. Files larger than 48000
bytes are rejected before catalogs are reassembled; import a smaller file.
Firmware validation at commit remains authoritative.
The blank positive exponent sign present in AMSAT (including QO-100) is accepted
as in `control_logic.h`, without rewriting lines/checksums or inventing orbital
elements.

The cache exists only in the app's private files and is excluded from backups.
It is replaced only after full validation, writing/syncing a staged file, and
`Files.move(ATOMIC_MOVE, REPLACE_EXISTING)` in the same directory. If atomic
replacement is unavailable, the previous file is preserved; there is no
delete-first fallback. A failed update download does not erase the last valid
cache.

You can transfer the entire catalog or **only the selected TLE**. Both cases
**replace the rotor's entire catalog**; they do not merge or append. The dialog
warns that selection and pass cache are invalidated. Immediately before begin,
the app requests fresh authenticated status and requires idle (`READY`/`DISARMED`),
valid GNSS UTC, and every TLE no older than 14 days and no more than 1 day in
the future, using **rotor UTC**, not the phone clock. It does not automatically
enable motors or tracking. Check GNSS, load the rotor catalog, and select again.

Version 1 contract, checked against actual handlers:

| POST route | Body | Required ACK |
|---|---|---|
| `/api/tle/begin` | `length` integer 1..48000, `sha256` 64 lowercase hex | Positive uint32 `uploadId` |
| `/api/tle/chunk` | `uploadId`, sequential byte `offset`, `text` 1..512 ASCII bytes | `received` exactly equals cumulative bytes |
| `/api/tle/commit` | `uploadId` | HTTP 2xx without error and a string `message` |
| `/api/tle/abort` | `uploadId` | HTTP 2xx without error and a string `message` |

Each chunk also respects the 2048-byte JSON maximum and GATT v1 framing.
Wait for ACK/END before sending the next chunk. Hash, length, offsets, owner,
and TLE validation are checked again by the ESP32; the previous cache remains
until a verified commit. Firmware stages in RAM and atomically replaces in
LittleFS. App global timeout: 5 minutes; per request: 15 seconds. Firmware
invalidates an inactive transfer after 60 seconds. There are no automatic
retries for a command whose execution is uncertain. If commit ACK is lost,
the app **does not assume persistence succeeded or failed**: explicitly
reconnect and query the rotor catalog.

During transfer, the app blocks concurrent mutations. Cancel waits for the
current ACK and sends abort. If STOP is requested during a transfer, the app
waits for that abort before sending stop; this does not replace the physical
emergency stop. If commit has already been sent, abort/reversal is not promised:
the app waits for the actual ACK and queries the rotor if the result is uncertain.
The app states this explicitly. Transfers cannot start while the rotor moves or
tracks. The app does not inject a second concurrent command or claim commit
confirmation before the final ACK.

## Passes and autonomy

The ESP32 runs SGP4 and calculates the next 24 hours; the phone only selects a
satellite from the rotor catalog and queries `/api/passes`. Responses with
`calculating:true` trigger bounded polling: at most 60 requests, 1.5 seconds
apart, each serialized and authenticated. The app displays AOS/LOS in explicit
**UTC with Z** and maximum elevation; it neither substitutes local time for UTC
nor calculates the trajectory. If the limit is reached, it is shown and another
query must be explicit. GNSS UTC, site, and fresh TLEs are required; the firmware
decides whether tracking is safe. Frequencies are not part of the TLE and are
not invented. After confirmed tracking starts, the phone may be closed: the
ESP32 continues autonomously under the firmware contract. No CAT or PTT.

## Contract checked against firmware

UUIDs and framing come from `firmware/src/main.cpp` (`setupBLE`,
`serviceBLE`) and `firmware/include/ble_protocol.h`, not an external service.

| GATT | UUID |
|---|---|
| Service | `c8200001-4e53-4253-9000-000000000001` |
| RX, write with response and authentication/encryption | `c8200002-4e53-4253-9000-000000000001` |
| TX, notifications | `c8200003-4e53-4253-9000-000000000001` |
| Standard CCCD | `00002902-0000-1000-8000-00805f9b34fb` |

BLE JSON version **1**. Each frame is 5–20 bytes:
`0x53, flags, sequenceLo, sequenceHi, payload(1–16 bytes)`.
Flags START=1, END=2; little-endian sequence begins at 0. START|END=3 for a
single fragment. MTU 185 is negotiated (retry with 23); **v1 still uses 20
bytes per frame even with a larger MTU**, as required by the firmware. No
newline, NUL, or partial-string reassembly: UTF-8 is decoded only after END.
Maximum request 2048 bytes; response 8192. Out-of-order sequences, repeated
START, unknown flags, invalid UTF-8, foreign IDs, and oversized messages are
rejected.

A complete `status` response requires **`apiVersion:1`,
`protocolVersion:1`, `firmwareVersion:"0.2.0-prototype"`**; constants checked
against `firmware/include/ble_protocol.h`. Any different version, missing field,
or version represented as a string disables control and disconnects. Firmware
comparison is deliberately exact: even a compatible new version requires
review/updating the app and running its tests.

Request:

```json
{"v":1,"id":1,"path":"/api/status","method":"GET","token":"<entered locally>","body":{}}
```

Response:

```json
{"v":1,"id":1,"code":200,"data":{"mode":"READY","fault":"","homed":true,"calibrated":false}}
```

The response fragment above is **illustrative**, not a complete accepted
status: typed position, UTC, site, and safety fields from the firmware are also
required. `code=401/403` is never accepted even if `data` appears successful.
IDs are positive uint32 values and strictly increase per connection; the app
resets its counter only after closing a connection. The first exchange is
authenticated `GET /api/status`, after bonding, discovery, MTU negotiation, and
CCCD confirmation. No `/auth` route is invented.

Only one GATT operation and one JSON request may be in flight. Each write waits
for `onCharacteristicWrite`; a rejected start gets two bounded retries, but a
motor command with uncertain execution is not resent. Connection/operation/
request timeout: 15 seconds. Authentication, framing, or timeout errors close
the connection and require explicit reselection. STOP has priority in the app
queue but waits for END of the in-flight exchange to avoid mixing responses.
The physical stop is essential: neither BLE nor this queue guarantees emergency
stop latency.

Actual supported routes: GET `status`, `tle`, `passes`; POST `stop`, `clear`,
`home`, `move`, `calibrate`, `site`, `select`, `track`, `catalog`,
`tle/begin`, `tle/chunk`, `tle/commit`, `tle/abort`. The screen uses the actual
paginated `POST /api/catalog` with integer `offset` and `limit:10`, and confirms
`total`, contiguous IDs, and `nextOffset` before enabling selection. “Next page”
is explicit; there are no request loops. Mechanical AZ [-180,180]° and EL
[0,90]°; true heading [0,360)°; site latitude [-90,90]°, longitude [-180,180]°,
altitude [-500,9000] m. Values must be finite numbers; numeric strings and
booleans do not count as numbers. The rotor calculates SGP4 and passes; the
phone needs Internet only to download from a provider; local-file import or
pre-existing TLEs work without Internet. A full GET `tle` exceeding 8192 bytes
is rejected; the screen avoids this limit using the paginated catalog and
supports the rotor's 100 satellites.

The controller shares HTTP/BLE handlers. While one transport owns a movement,
the other cannot start another control command: it receives 409; authenticated
STOP and status queries remain available. The app does not silently take
control. In the checked firmware, losing BLE during manual movement/homing
causes FAULT; already-started autonomous tracking does not depend on keeping the
screen/app open. STOP does not clear faults; `clear` requires rehoming and
recalibration.

## Hardware validation pending

JVM tests verify logic/protocol, not the phone radio. On a real Android device,
still verify: system passkey dialog, rejection without bonding, firmware-required
MITM encryption, MTU 23 and negotiated MTU, permissions 26/30/31/35, timeout,
radio loss, second client, and physical stop. The motors, BLE link, and
calibration are never represented as field-validated.
