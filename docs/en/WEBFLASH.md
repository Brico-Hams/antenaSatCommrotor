# Prototype web flasher (prepared, not published)

**PCB/hardware are not released. Do not connect motors while flashing.**
CI checks software and flash data; it does not verify boards, wiring, motion,
E-stop, homing, calibration, orbital accuracy, or RF. Preparing Git does not
mean publishing: no push was made, Pages was not enabled, and GitHub Actions
was not run here.

## What is built

`.github/workflows/webflash.yml` is separate from the engineering workflow.
A `v*` tag, push to `main`, or `workflow_dispatch` builds the real **esp32**
environment in `firmware/platformio.ini`. Relevant PRs build/validate
artifacts without deployment permissions, secrets, or `pull_request_target`.

Pins: PlatformIO Core 6.1.18; espressif32 6.10.0;
Arduino-ESP32 3.20017.241212 (Arduino 2.0.17); Xtensa 8.4.0+2021r2-patch5;
ArduinoJson 6.21.5; TinyGPSPlus 1.1.0; Sgp4-Library commit
`7c82d31f9d9a286acde5ef55da8308fc93d2ba96`.
NimBLE-Arduino 1.4.3 is built for locally configured optional BLE. LittleFS
UI includes the physical-calibration guide. BLE uses controller handlers and
privately configured authentication; publishing/flashing does not enable it.
HTTPS download over BLE returns 409; download TLE on the client and transfer
using the documented controller/app protocol. Large TLE transfer uses
`/api/tle/begin`, `/api/tle/chunk`, and `/api/tle/commit`, SHA-256 validation,
atomic cache replacement, and a paginated catalog. The phone downloads data;
SGP4 propagation remains on the rotor. Compilation does not validate heap,
radio coexistence, or physical calibration.

CI also pins tool-esptoolpy 1.40501.0 (esptool 4.5.1) and tool-mklittlefs
1.203.210628 (2.3) through PLATFORMIO_PLATFORM_PACKAGES, retaining the
controller's framework/toolchain pins. Actual configuration and resolved
package versions are included in `build-info.json`; this workflow does not
change `platformio.ini`. Node 22 and Python 3.11 are pinned by compatible
release line, and Actions by major version.

ESP Web Tools **10.1.0**, license **Apache-2.0** verified in npm and the
package LICENSE. `webflash/package-lock.json` also pins transitive dependencies
and integrity. CI runs `npm ci --ignore-scripts`, copies **all of `dist/`**
to `vendor/esp-web-tools/` without flattening directories, and preserves
chunks/dynamic imports and licenses. It does not use `unpkg latest`, a remote
CDN, or a silent fallback. Browser entry is
**dist/web/install-button.js**, not `dist/install-button.js` with extensionless
imports. The validator checks relative imports in all browser-distribution
chunks. Upstream Arduino 2.0.17/ESP-IDF v4.4.7 sources and license texts
downloaded from public tags are checked against pinned SHA-256; silent changes
to a tag are not accepted. The page initially depends on npm/GitHub to
generate and serve these assets; do not claim the sources alone are an offline
flasher.

## Flash data: never guess offsets

`scripts/build-webflash-proof.py` is a PlatformIO post extra-script.
Its `webflash-proof` target builds firmware and captures actual `$UPLOADCMD`,
`FLASH_EXTRA_IMAGES`, `ESP32_APP_OFFSET`, board/MCU, and packages. **It does
not upload, open a port, or erase a device.** `scripts/build-webflash.cjs`
verifies that recipe and the compiled binaries:

| File | Decimal offset (hex) |
| --- | ---: |
| bootloader.bin | 4096 (0x1000) |
| partitions.bin | 32768 (0x8000) |
| boot_app0.bin | 57344 (0xe000) |
| firmware.bin | 65536 (0x10000) |

ESP Web Tools manifest: `chipFamily: "ESP32"` (classic WROOM, **not C3**).
No fictitious binary or combined image padded from offset 0 that could destroy
NVS is created or published. Four separate parts are used. If the controller
version still serves `/index.html` from LittleFS, CI builds `buildfs` and
includes a fifth `littlefs.bin`, with offset/size read from **partitions.bin**
(current default 0x290000/0x160000). This replaces the UI and saved TLE; back
them up first. If the controller embeds UI in program flash, only four parts
are needed: do not upload a filesystem image out of habit. The generator
checks the actual code.

Validation covers ESP32 headers, part count, real command offsets, safe
relative paths, SHA-256/length of every binary, sector overlap, actual
application/filesystem partition sizes, and NVS from the real partition
table. `SHA256SUMS`, manifest, and full commit identify the download.
`build-info.json` also links SHA-256 of the relevant source tree: each file in
firmware/src, firmware/include, web, and platformio.ini. The generator
compares that tree to the one captured by PlatformIO; if a header, UI, or
configuration changed after testing, it requires a rebuild. Actual package
versions and npm lock hash identify dependencies. Binary hashes can differ by
build path/toolchain/metadata: never substitute a hash from another build.
A local build without a first commit or with uncommitted changes is labelled
`local-prototype+uncommitted`; `sourceSha` is null, never a fabricated SHA.
The synthetic test at `tests/webflash.test.cjs` is not a sample firmware; it
exists only in ignored test directories. CI also validates its real bundle.

## Credentials and updates

Public build requires `carrierVerified=false` and empty `apPassword`,
`apiToken`, `staSsid`, and `staPassword` in `board_config.h`. If
`firmware/include/secrets.h` or `firmware/secrets.ini` exists, the build fails
BEFORE compilation. Never use GitHub Secrets to insert Wi-Fi passwords/tokens
into publicly distributed firmware. On virgin NVS, empty controller values
disable AP/API until local USB provisioning, without rebuilding. Compatible
existing NVS retains credentials and carrier verification; startup is always
DISARMED and never restores homing/calibration.

Provision **privately and locally** per `docs/CONTROL.md`; do not upload
configuration to Pages, Git, or public artifacts. After installation, close
the ESP Web Tools port and open a local USB console at 115200 baud:
`{"cmd":"setup"}` enters SETUP, disables Wi-Fi and motors, and invalidates
calibration; `cmd config` saves SSID, a user-selected AP password of 12-63
characters, and user-selected token of 24-128 ASCII characters to NVS (exact
fields/validation in CONTROL.md); `{"cmd":"reboot"}` applies changes and boots
disarmed. Do not share terminal/screenshot content containing credentials.
Do not send `cmd carrier` with `verified=true` until the board has been
physically checked. BLE requires explicit local enablement and a user-owned
passkey. This flasher does not invent a protocol, enable Improv Wi-Fi
automatically, or expose a token.

NVS is not encrypted: physical/USB access permits reading or changing
configuration; storing credentials there does not protect against physical
extraction. JSON lines accept up to 768 bytes. `tlsRoots` remains empty in the
public image, so HTTPS updates are rejected; manual TLE import remains
available after AP configuration. Do not claim the current public binary can
download TLE over HTTPS without configuring trust roots.

Normal writes do NOT touch NVS: default 0x9000-0xdfff. The manifest requires
erase confirmation (`new_install_prompt_erase: true`); **Erase device** is
unchecked by default. Actual ESP Web Tools 10.1.0 code was checked:
**false triggers automatic erase on devices without Improv Serial**, so do
NOT use false to preserve NVS. **Do not select “Erase device”** in ESP Web
Tools except when total erasure is intended, a backup exists, and the dialog
is explicitly confirmed. NVS may be preserved only with the same partition
table; layout migration requires a reviewed strategy/backup. Never restore
homing/calibration as automatic motion authorization.

## Enable Pages only when the owner decides

1. Create the remote/URL using the chosen account/repository. These files do
   not invent a URL; consult the actual URL returned by GitHub deployment.
2. In GitHub: **Settings → Pages → Source: GitHub Actions**.
3. Create **webflash-pages** environment, configure **Required reviewers**
   for manual approval, restrict branches to `main`, and disable bypass if
   possible. Confirm the repository plan/visibility supports that protection.
4. Only after reviewing the prototype and configuring reviewers, set the
   repository variable **WEBFLASH_PAGES_APPROVED=prototype-only**. Without
   it, the deploy job does not run. Do not set it if reviewers cannot be
   required; download artifacts manually without publishing.
5. Push to `main` (if approved) or dispatch from `main` with
   `deploy_pages=true`. Tags produce versioned artifacts but do not deploy
   Pages; PRs never deploy. Dispatch from another branch does not deploy.

Build permissions are `contents: read`; `pages: write` and `id-token: write`
are exclusive to the gated deploy job with protected environment. No PAT or
secrets are needed. Approving deployment does not release hardware as a
product: PROTOTYPE warnings remain on the page. The Actions artifact is named
`webflash-<commit SHA>` and contains the page, real binaries, hashes, metadata,
notices/licenses, and source/objects for relinking. Upstream compliance/source
files are large; they are not downloaded while flashing, only manifest parts
are. Retain those files in distribution. The workflow does not create GitHub
Releases or move a tag.

## Browser, permissions, and privacy

Pages must serve HTTPS. Web Serial requires **desktop Chrome or Edge** in a
secure context; Firefox/Safari/mobile are not compatible alternatives.
Open directly, not in an iframe; enterprise policies may block USB. Port
permission is optional and appears only after pressing Connect. Denial/cancel
does not flash anything; retry or use local PlatformIO. Select the
**ESP32-DevKitC V4 38-pin WROOM-32E** by label/port; do not infer pinout from
appearance. Disconnect motor/actuator power; use USB only.

The third-party library is served from Pages, but all serial data stays local.
The module script uses `crossorigin="anonymous"`; assets are same-origin, no
CDN is needed, and no third party receives port access through CORS. There is
no upload of private code/firmware, passwords/tokens, or own telemetry.
GitHub receives ordinary web requests for public assets. npm and upstream
repositories are consulted in CI for dependencies; no private user code is
sent to a flashing service.

## Validate locally (without a board)

From the root, with Node 22/Python 3.11/PlatformIO available:

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

If the generator reports missing upstream notices/licenses, also run the
workflow's “Preserve upstream source and license” step before packaging.
Binaries, tools, and outputs go to ignored `build/` and `.pio/`; webflash
node_modules is ignored. Do not commit binaries. Always install from the
webflash directory: do not run package-less npm install from the root with
`--prefix`, or add `file:..` dependencies/local links. The generator rejects
non-registry dependencies and junctions/symlinks while walking notices to
avoid accidental recursion into the project/Android SDK. For manual hosting,
serve **build\webflash** over HTTPS or localhost: do not open
`webflash/index.html` using `file:` or assume assets exist. Build or
verification errors stop generation/deployment.

## Licenses and education

Authors: **Anatol EA5KAO**, **Diego EA5JEF**, **Pedro Roca Molina**;
acknowledgements to [Bricohams](https://bricohams.org/). See
`AUTHORS.md`, `ACKNOWLEDGEMENTS.md`, `DISCLAIMER.md`, and `NOTICE.md`.
Bricohams is cited as a scientific outreach organization for children and
adolescents. Current authorship does not replace that of libraries or
consulted sources; references do not imply collaboration, sponsorship, or
endorsement. Original software MIT; installed SGP4 MIT verified;
ESP Web Tools/NimBLE-Arduino Apache-2.0; ArduinoJson MIT; TinyGPSPlus/
Arduino-ESP32 LGPL-2.1 and SDK retain their original notices. Do not claim
the entire binary is MIT-only. The bundle retains texts, exact upstream
dependency source, relinkable objects, and upstream links/versions; preserve
them on redistribution. Review SDK/component obligations before commercial
use. Hardware has its separate CERN-OHL-S-2.0 license.

Educational use by minors requires adult supervision; children must not
perform hazardous assembly, and RF/TX must never be used without applicable
authorization/license. No CI test certifies safety, legal authorization,
or hardware compatibility.
