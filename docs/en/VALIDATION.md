# Delivery validation record

Date: 2026-10-10. Status: the ESP32 baseline has digital validation; the CM5
expansion is incomplete and physical acceptance is pending.

## CM5 expansion: current limits

The ESP32 baseline PCB/firmware/Android results below do not validate the new
CM5 auxiliary board or its independent guard.

| New surface | Evidence | Limitation |
| --- | --- | --- |
| Modular documentation and prices | Three Node link/price-consistency tests passed | Not a complete budget or physical test |
| CM5 auxiliary board and guard | Interface map; 11 reported contract tests | No schematic/routed PCB, ERC/DRC, or new Gerbers/BOM/CPL |
| Radio and rotor | Connection to existing adapter and nine reported routes; 57 reported offline tests with an explicit test controller | Real CM5 provider/BSP and guard pending; no proof of physical tracking or TX permission |
| CM5 rotor controller | 29 reported offline tests, including `open_adapter` linking and rejection when the provider is absent | No commissioned CM5 provider; do not replace it with simulation in production |
| BricoHams OS recipe | Local rerun: nine OS tests passed and one Linux/Python test skipped; documentation/prices aggregate: 12 passed, zero failures, one skipped | No pi-gen build or CM5 boot; integrated OS service deliberately not enabled |
| POL mechanics | Seven reported tests; seven printable parts and three DXF templates present; strain relief export and closed mesh reported | 5:1 and 16,000 increments/revolution are not accuracy; soft limits +/-80 degrees, NC targets +/-85, candidate stops +/-90; nominal zero clearance requires tolerance verification |
| CM5 Android | 58 JVM tests, lint/build, and v2 signature reported; 33 lint warnings, no errors. APK: 1,208,309 bytes; SHA-256 recorded below | No physical BLE/RF test; maps/radar remain offline without verified `OrbitSnapshot` mapping |
| Mass and runtime | Targets: <=5 kg excluding only the external battery, and two hours | CM5 assembly including tripod and cables still needs weighing/testing |

**CM5 HOLD:** do not fabricate the new auxiliary board or enable motors/TX
based on the GPIO map or contract tests. Safety circuitry, qualified
electrical interfaces, and actual fabrication assets are missing.

The preserved CM5 debug APK is outside the build outputs:
[PortableSatStation-CM5-debug.apk](../../releases/android/PortableSatStation-CM5-debug.apk).
SHA-256:
`ED52E0881353D7542DDA1FAC5062B372E2EA4BB8489710EDC98386ECF5A77DD7`.
The Android panel queries seven real routes and displays their responses;
it does not turn those JSON responses into a map/radar or confirm that a
position was reached merely by receiving an ACK. Remote CM5 homing/calibration
are not exposed because they require local trusted confirmation.

## Previous ESP32 baseline summary

| Deliverable | Result | Limitation |
| --- | --- | --- |
| Node aggregate | 35/35 passed | Does not measure latency or hardware |
| ESP32 firmware | Compiled; Unity 6/6 and real SGP4 vector | No physical pairing/motors |
| Android | Debug APK, 29 JVM tests, zero lint issues, signature verified | No physical BLE phone |
| WebFlash | Real bundle, nine checks, browser smoke test | No physical USB or remote Pages |
| PCB | ERC/DRC/parity/unconnected count zero; real Gerbers | Manufacturing/operation HOLD |
| CAD | Meshes and mathematics checked; branding integrated | Assembly/torque/wind not tested |
| RF | Documentation and initial dimensions | SWR/gain/isolation not measured |
| Mass | BuildLight 3.130-3.200 kg before pending additions | **Fails** the <=3 kg target |

The sections below include integration history. This summary governs delivery
status; hashes identify specific revisions and must not be mixed when flashing.

**Latest ESP32 aggregate: 35/35 tests passed, zero failures.**
The lid mesh, copper-thickness field, and NVS-overlap fixture were resolved.
Historical failures below are retained for traceability; they are not the
current result. Final PCB/WebFlash/Android reports have been received;
physical acceptance, not compilation of those artifacts, remains pending.
There is no physical antenna/rotor/PCB test and no remote Pages execution.
The aggregate was rerun after adding firmware BLE, USB, TLE transfer, shared
versions, and the larger enclosure: 35/35 passed. Android JVM/build results
are recorded separately.

This record distinguishes digital tests from physical behavior. Historical
ESP32 results do not constitute approval of the CM5 expansion or its hardware.

| Surface | Evidence | Status |
|---|---|---|
| RF/gearing/load calculations | Node.js 22.16.0, 5/5 tests | Arithmetic approved |
| OBJ/STL reference inspector | 2/2 tests; does not alter input or assume units | Metadata approved |
| Documentation links | Local links resolved, including CONTROL.md | Approved |
| Calculator diagnostics and tests | No VS Code errors | Diagnostics approved |
| Original PDFs | SHA-256 in input-hashes.json; local Xpdf extraction | Recorded |
| ESP32 firmware | Controller compiles; WebFlash provisioning under revision | Compilation approved, not bench |
| Web AP | Syntax/DOM/API test and eight authenticated actions | Digital approved; hardware pending |
| CAD/STL | 34 STL exports; math/inventory tests pass | Partially digital; mass under review |
| Mechanical assembly | No built prototype available | Pending G1 |
| Antenna/diplexer/RF hybrids | No VNA for the assembly | Pending G2 |
| Field tracking | Physical equipment not operated | Pending G3/G4 |

## Environment tools

Initially Node, OpenSCAD, PlatformIO, and pdftotext were unavailable on PATH.
The extension also provided no implementation for configuring a Python
environment. Portable Node and local Xpdf were used in the session's artifact
folder, not globally installed and not in the Intune directory.

Node 22.16.0: official download, ZIP checked against official SHASUMS256:

`21c2d9735c80b8f86dab19305aa6a9f6f59bbc808f68de3eef09d5832e3bfbbd`

Xpdf tools 4.06: `https://dl.xpdfreader.com/xpdf-tools-win-4.06.zip`.
PDFs were not sent to third parties. The two PartIIRotatorcontrol files have
the same SHA-256; they are treated as one duplicated source, not two studies.

## Calculation commands run

```powershell
node --test tests\engineering.test.cjs
node scripts\engineering-report.cjs
```

Result: 5 tests, 5 passed, 0 failures. VS Code's integrated test runner did not
discover the CJS tests; Node's native runner was used.

Latest integrated run of `scripts/validate.ps1`: 12 tests, 12 passed, 0 failures.
The earlier integration failure due to CONTROL.md was resolved when the control
documentation arrived. The web test checks syntax, DOM, API schema, eight
authenticated actions, and safe name rendering; it is not a test on a physical
ESP32. The metadata inspector passed its own two tests; original OBJ/STL inputs
are read without modification. TDS_AV2040 required local rasterization because
its text encoding was corrupt; figures were checked visually.

The initial mechanical delivery exported 34 STL files with OpenSCAD and checked
closed/oriented edges and positive volume. Mechanical tests include involutes,
25:1 ratio, planetary phasing, and 121 ideal gear-mesh positions in section.
They are not a complete station-wide collision sweep or assembly tests.

Initial fully solid ASA-equivalent calculation was 2.641 kg before metal parts.
The <=3 kg target is not demonstrated; geometry optimization and a complete mass
budget were requested. Do not present solid mass as the weight of an infill
print or omit the battery.

Bounded revision: 2.521 kg solid-equivalent ASA, saving 120.45 g. Additional
budget 1.464–2.294 kg; hypothetical printed total 3.208–4.038 kg without
radio/tripod. Does not meet <=3 kg. The user authorized changing the transmission
and prioritizing mass. Lightweight BASE with two GT2 20:100 stages was generated;
previous results are for the planetary variant and do not automatically validate
the new variant.

Last aggregate before PCB/WebFlash completion: 16 tests, 16 passed, 0 failures.
Includes belt mathematics, new meshes, mass audit, documentation, and web
security surfaces. Static interlock checks are not latency tests.

BASE: solid-equivalent ASA 0.862 kg; budget 3.121–4.006 kg and hypothetical
lightened scenario 2.905–3.790 kg. <=3 kg still not demonstrated. Reversible
belts require balance and independent mechanical retention.

Control compiled for ESP32-DevKitC V4/WROOM-32E, no PSRAM:
PlatformIO 6.1.18, espressif32 platform 6.10.0, Arduino 2.0.17. The control
validation reported four Unity tests and an SGP4 Vallado-vector check passing.
Firmware revision reported with frozen PCB pinout has SHA-256
`99B550AF144C31B5B7918F3A5E17D245F108D1C602CB234E8E79358E066045B3`.
LittleFS reported after attribution:
`EDBDB2F968F6CC0DA83A04061E3806A4C7C403735B9C8C3EA44B897F62E8D9C2`.
These hashes identify that revision; later provisioning changes require
recompilation and new hashes.

Carrier PCB in development: 180x130 mm; does not fit the former 124x64 mm
usable enclosure. Integration of a new enclosure was requested; shared GPIO map
does not prove fit. Gerber/ERC/DRC report pending.

Integration update: 28 Node tests added, 28 passed, zero failures, including
new enclosure for 180x130 carrier, updated mass budget, and manifest/WebFlash
tests. This does not certify the PCB, USB flashing, or remotely executed GitHub
Actions.

Controller includes local USB provisioning at 115200 baud (`setup`, `config`,
`carrier`, `reboot` JSON), so credentials can be set without recompiling. SETUP
disables motors/Wi-Fi/API and invalidates homing/calibration; NVS is unencrypted
and requires physical protection. Reported Unity tests: 5/5. Last binary
reported from isolated build has SHA-256:
`C413748CDDF16C3AFF782FF3663F93D7B9BB613DB90DAF1FD73C067CEF0771CE`.
WebFlash installation must rebuild from the same revision and emit its own
verifiable hashes; do not mix historical revisions. HTTPS stays disabled in
the public image if no CA is configured; manual TLE import is available.
Physical USB was not tested.

Later run with PCB and branding integrated: 35 tests, 31 passed, 4 failed due
to degenerate triangles in the new enclosure lid. Geometry/export correction
was requested without weakening the validator. Lid is not approved while that
failure remains. Five PCB tests passed, including SHA-256 manifest, 38-pin
pinout, and ERC/DRC/parity reports. Final report from PCB owner and physical
review remained pending; this is not an automatic release.

Corrected lid: binary export validated before replacing the file; 9024 triangles,
one connected component, 0.7 mm raised lettering. Reported SHA-256:
`EC5806AA9FF4EB068FBC695D6CEEF794CD9DDE1DB68270D784114A5068320E34`.
Latest aggregate: 35 tests, 33 passed, two integration failures: copper
thickness field in PCB test and WebFlash fixture failing on invalid header
before reaching NVS overlap test. Evidence/fixture correction was requested
without weakening criteria. Final aggregate approval was still pending.

Final enclosure enlarged for wiring: interior 224x174 mm, exterior 228x178 mm,
32 mm above PCB; 22 mm per edge. Four STL files and 240x196x2 mm tray
regenerated; eleven mechanical tests reported passing. Lid retains integrated
branding and one connected component. Updated BuildLight budget is 3.130–3.200 kg
BEFORE pending additions. **The <=3 kg requirement is not met in this revision.**
Do not present earlier lower scenarios as validated final mass.

Final PCB: KiCad 10.0.7, zero pending ERC/DRC/parity/unconnected issues;
180x130 mm, two 2 oz copper layers, 40 components, 17,349 segments, and 55 vias.
Real copper/mask/silkscreen/outline Gerbers, PTH/NPTH Excellon, netlist, and
SHA-256 manifest exported. ZIP:
`fabrication/PortableSatCarrier-Gerbers-CAD-VERIFIED-NOT-RELEASED.zip`.
Production/operation HOLD pending module measurements, exact DC stop, and
physical electrical/thermal qualification.

BLE/Android and guided calibration extension in development. The app will
download TLE over HTTPS and transfer over BLE; ESP32 remains pass/tracking
calculator. Requires new binary and WebFlash rebuild with evidence from the
same revision.

Final reported BLE firmware: NimBLE 1.4.3 (Apache-2.0), bonding, MITM/encryption,
and token; passkey via USB, BLE initially disabled. Shared HTTP/BLE handlers;
callback assembles/enqueues and does not run heavy filesystem/SGP4 work.
TLE begin/chunk/commit/abort with length, SHA-256, sequential offsets; paginated
satellite list. Frozen versions: apiVersion=1, protocolVersion=1,
firmwareVersion=0.2.0-prototype (the 0.3.0-prototype build with API 2 and the
`esp32_nema17` profile compiles but has no board or rotor measurements).
Reported controller build: flash 1,199,509 bytes, static RAM 59,084 bytes.
Firmware SHA-256:
`64194FB5A0FBDB16D5ECBB6233F56D88C587E91C998A8E8A4F621B9C6C185DD3`.
Unity 6/6 and Node control 3/3 reported passing. No physical pairing, BLE
latency, or Wi-Fi/motor coexistence test.

Final transfer revision: BLE disconnect immediately aborts upload in RAM and
releases ownership, preserving persisted cache. Reported recompiled firmware
SHA-256:
`143A541D86F87922459371FB4F7E5C2B615AC8932382A9E2521BDFC0362EFF81`.
This supersedes the prior hash for that revision; WebFlash must be rebuilt with
the same change. TLE import does not require GNSS fix, but tracking still
requires valid UTC/site/TLE.

Real-provider validation: AMSAT HTTPS returned a catalog containing blank
positive exponent signs. Controller and app parsers were adjusted without
altering lines or weakening checksum. Unity 6/6 and real SGP4 check reported
passing. Firmware after correction:
`549B1DAB4121E490E355D6259675483B8C752780CF0B7A52CDEB4CBC568BAD02`.
Download by Android code: 14,434 bytes, 97 valid satellites, SHA-256
`ec291294636090d712fc901e4a7e3fa15bbeb8366fb771d7aad131b5c8db1ce9`.
CelesTrak and PE0SAT timed out in desktop check; cache is preserved and TLS
was not disabled. This test does not guarantee future provider availability.

Final WebFlash: real build and bundle generated from current source tree,
including header fix for AMSAT. Nine checks against real artifacts passed and
local browser smoke test (HTTP 200, warning gate, local dialog imports) passed,
without opening USB. Bundle firmware matches SHA-256 `549B1D...BAD02`.
LittleFS SHA-256:
`866C1AF7C5B1FFE96C5DCC4DCF8C692383DDDE28FEF7C772581148DC37D12256`.
Bundle metadata links source/config/UI, package versions, and npm lock.
Flash used 1,199,553 bytes; static RAM 59,084 bytes. LittleFS can vary between
builds due to metadata; validate its actual hash rather than assuming binary
reproducibility.

ESP Web Tools requires `new_install_prompt_erase=true` to show erase initially
unchecked; false can automatically erase non-Improv devices. Warning and
confirmation are retained. Pages requires a prototype-only approval variable
and protected reviewed environment; GitHub CI was not published or run.

## Final Android evidence

APK: `android/app/build/outputs/apk/debug/app-debug.apk`, 980,724 bytes.
SHA-256:
`47997a78abd87b3aa4e26a33106f9b122a817121dd02c2abc7d6b72717ca399b`.
Build succeeded, 29 JVM tests without failures, zero lint issues, and debug
signature verification passed. This is not a release signature or store
distribution. Prepared CI can regenerate artifacts; build directory is not
versioned source.

HTTPS download limited to three providers, file import, private atomic cache,
full/selected BLE transfer, rotor status preflight, up to 60 pass queries, and
UTC handling. Credentials encrypted with Android Keystore; INTERNET permission
is used for authorized download, without uploading tokens/private data to
providers. Rotor still calculates SGP4 and receives no phone-generated
trajectory. Real AMSAT test passed; CelesTrak/PE0SAT timeouts are documented.
Android/BLE/motors have not been tested as one physical assembly.

The 8 m/s wind example **FAILED** the torque budget with safety factor 2. The
test **PASSES precisely because it detects this limit**; it does not validate
operation in that wind.

## Verification 2026-10-11 (review environment, no hardware)

| Suite | Result | Notes |
| --- | --- | --- |
| `node --test "tests/*.test.cjs"` | 66/66 | `npm test` fixed for Node 22 |
| `pytest tests/rotor tests/radio_host` | 86 passed | helper `test_controller` renamed (pytest collected it as a test); `PYTHONPATH=.:radio:rotor` |
| Native control logic (Unity, g++) | 6/6 | `tests/control_logic/test_native` |
| OpenSCAD 2021.01 render of the logo parts | watertight | 4 parts |
| Android JVM, KiCad ERC/DRC, `control_sgp4.cpp`, OS image | **not executed** | no network for Gradle, no KiCad, no pinned SGP4 library, no Docker/Debian mirrors |

## Interpretation

A compiled orbital library does not confirm wiring, sensor accuracy, or complete
tracking without bench tests. An exported mesh does not confirm fit, assembly,
strength, or meshing. Initial dimensions do not guarantee RF matching or gain.
Outstanding limits are described in ACCEPTANCE.md and RISKS.md.
