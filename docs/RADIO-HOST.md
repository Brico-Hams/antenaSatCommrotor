# Independent Linux radio host — v1 frozen contract

## Explicit modular operating profiles (supersedes unconditional tracking gates)

Radio SDR, rotor and antenna are independently usable modules. The integrated
build remains CM5 IO+AUX+two Lime Minis; a deliberately configured standalone
radio may use one or two real Minis. No device omission automatically changes
the build or operating policy.

`--operation-profile INTEGRATED_TRACKING` is the default. It requires all
existing physical/RF/link/lease interlocks **and** valid fresh GNSS/SGP4 and
verified rotor safety/calibration supplied by actual integration. Tracking loss
inhibits TX; it never selects manual mode.

`--operation-profile STANDALONE_MANUAL` is an explicit local launch policy,
without `--rotor`. It uses nominal manually tuned Hz, **no Doppler**, and does
not require GNSS or rotor. It still requires actual SDR-ready, physical arm/
PTT, acknowledged healthy RF path/polarization, authenticated audio session
and lease≤500ms. Each authenticated session must explicitly confirm via
`/profile` set `{"profile":"STANDALONE_MANUAL","confirm":true}` before TX.
The phone cannot override the locally configured profile; reconnect revokes
confirmation. Manual is never a tracking-loss fallback.

`--radio-count 2` requires both explicit unique serials when hardware is
selected. `--radio-count 1 --single-channel VHF` (or UHF) requires standalone
manual mode and exactly that channel's explicit serial; the other serial must
be omitted. There is no auto-first-device/no-device fallback. One-radio audio
start explicitly uses the same `rxChannel` and `txChannel` (the only available
channel); dual-radio audio remains explicit crossband. Single-radio RX/TX
have separate frequency readbacks/LOs and retain one-TX-only policy.
`/status` adds `operationProfile` and `availableChannels`; profiles contains
only actual configured channels, never a fabricated second device.

Standalone RX needs neither GNSS nor rotor nor TX commissioning, but needs
its selected real SDR/rate/USB resources and Linux audio/BLE prerequisites.
Rotor-only deployment runs the rotor service, **not `radio.main`**, and has
no radio-required Soapy plugin/import. The radio package never starts a rotor
unless `--rotor` is supplied; no standalone sensor or motion claim is made.
Standalone antenna use needs its own verified feed/network/mechanical setup.
Integrated assembly requires the separate verified rotor adapter, GNSS/
calibration, RF path, BSP/NC E-stop/watchdog and qualified USB/audio power
topology; this guide does not claim those are commissioned.

This **original** subsystem is independently scoped on **Raspberry Pi
Compute Module 5 (CM5), Linux ARM64**, controlling both three-axis rotor and
radio/audio through the **purchased official CM5 IO board plus a custom
auxiliary board**, not a fully custom high-speed CM5 carrier. The authoritative selected radio
is **two replaceable LimeSDR Mini devices**, not Lime+RTL-SDR V4 (RTL is
RX-only). Both chains are TX capable, with concurrent VHF/UHF RX; only
**one TX at a time** is permitted. No ESP32 is
required. Existing ESP32
firmware/GATT version0.2.0 is **legacy**, unchanged. `radio-host/1.0.0`
remains a distinct radio API even when radio and motion share one computer;
the same native Android APK uses the separate radio service contract.
No Android, legacy firmware, motion-control implementation or Gerbers are
modified by this subsystem.

## Verification boundary / release blockers

Offline DSP, interlocks, wire framing, dispatcher, localhost CAT and API
adapter tests are executable. Physical RF, actual simultaneous RX/TX,
Linux GPIO wiring, Linux BlueZ pairing/MTU/notifications, antenna/filter/
duplexer/isolation, RF output power and Android interoperability are **NOT
verified**. CM5 and two LimeSDR Minis are selected architectural resources, not
physically validated hardware. No RF transmission was
run. Neither FM-only modules nor modified Pluto frequency ranges imply
145 MHz / SSB support. Only actual Soapy module discovery and advertised
frequency/sample-rate ranges are accepted.

TX remains unavailable until a **verified tracking source** supplies
range-rate, site and UTC. `TrackingInput` is transport-neutral: future local
Pi SGP4 may call it directly, or an authenticated upstream adapter may call
it after validating its source. Local integration provisions source IDs
with `TrackingInput.provision(source)` and submits samples with
`update(source, rangeRateMps, utc, site)`; rejection/revocation clears state
and inhibits TX. Provenance is established outside this radio boundary,
not inferred from a source name or remote request. Android's audio token
alone does not establish orbit provenance. `Dispatcher.tracking_input`
uses the same boundary for `/tracking`; arbitrary BLE clients remain
untrusted. No SGP4 computation is invented here. A prepared fixed local adapter loader
is described below and now uses the verified actual public RotorController
adapter hook. Physical BSP composition/commissioning remains pending.
There is intentionally no CLI flag that bypasses this blocker.
RX works with no orbit/tracking input. Internal microphone/speaker and
Kenwood K1 electrical wiring remain pending verified hardware. There is no
Bluetooth HFP/A2DP claim: this is transparent bidirectional GATT PCM only.

CM5 CPU headroom, USB topology/throughput and simultaneous
SDR/audio/motion operation are **not physically verified**. Pi4/Zero/Zero2
are not the authoritative base. Motion integration
is separately assigned: Linux GPIO step-pulse timing is not claimed adequate.
TMC5130/5160 SPI internal ramp generation, normally-closed physical E-stop
and an independent hardware watchdog are under evaluation, not implemented
or approved by this radio subsystem. The auxiliary board and integration
remain separate work; no stale two-axis or ESP32 board assumption applies.

The **5 kg maximum applies to the station excluding the external battery**,
not the rotor alone: tripod, radio/RF hardware, SBC, three-axis rotor, antenna, enclosures,
switches, connectors and **all cables** must be included in the parent mass
ledger. No SBC/radio assembly mass is measured or approved here. CM5 with
two LimeSDR Minis are selected; this software neither proves its processing/
BLE/USB capacity nor proves the complete station meets the mass limit.

The shared-SBC sensor requirements explicitly include **GNSS UTC and
position**, **calibrated compass with declination-corrected true heading**,
**IMU inclination**, and **encoders on all three axes**. Sensor drivers,
calibration, declination model, installation/alignment and measured encoder
feedback belong to the separate future Pi integration scope. Connectors or
source IDs are not evidence these sensors exist or operate correctly.

The locally trusted tracking adapter must validate **fresh GNSS site/UTC
and valid current SGP4 state** before submitting Doppler samples. This
radio boundary checks finite/ranged site/range-rate, UTC skew and monotonic
sample age; it cannot itself attest GNSS fix quality, SGP4 validity or
sensor provenance. When GNSS site/UTC or SGP4 state becomes invalid,
integration must revoke that source immediately, not publish zero site,
zero range-rate or synthetic UTC as a fallback. A valid geographic
coordinate of latitude0/longitude0 is not intrinsically invalid; fix
validity must come from the GNSS adapter, never inferred from coordinates.
Revocation clears tracking and inhibits TX; expiry independently inhibits
Doppler TX. RX may return to nominal frequency without claiming valid
tracking. No actual sensor acquisition is implemented by this radio scope.

All station **RF connections shall use standard SMA, 50 Ω, not RP-SMA**,
including radio RF ports, antenna/feed network and RF polarization switch
interconnects. Exact connector gender and cable assembly lengths remain
subject to verified hardware selection and the complete-station mass ledger.
This requirement does not apply to audio: Kenwood K1 microphone/speaker
connections remain audio jacks, with pinout/electrical compatibility pending
verification. No connector or RF impedance compatibility is proven by software.

## Rates, DSP and RF choices

- Audio: normalized float internally; signed S16LE, mono 8,000 sample/s on BLE.
- DSP RF baseband: complex CF32,96,000 sample/s, integer×12 audio conversion.
  Real hardware rate defaults to **1,000,000 sample/s**, configurable
  `--hardware-rate`192k..4M. **Both devices' RX/TX advertised ranges and
  exact rate readbacks must match the requested rate**. 1MSPS is a requested
  configuration, not a claim that physical hardware has applied it.
  Streaming rational interpolation with persistent integer clock counters
  and 257-tap anti-alias FIR converts96k↔hardware rate, preserving block
  continuity. One sample lookahead is retained, never silent-filled.
- Selected backend: SoapySDR **LimeSuite/Lime** driver with one discovered
  physical LimeSDR Mini per VHF/UHF profile. LimeSDR Mini2.x is specified as
  nominal 10 MHz–3.5 GHz, one RX/one TX with independent LO and native
  standard SMA ports. Those nominal specifications **do not bypass actual
  discovery, exact device identity, advertised ranges, full-duplex flags,
  sample-rate support or tuning/rate readback**. Select the exact discovered
  serial for each profile's RX/TX, not a generic other Lime device. Production
  requires `--vhf-serial` and `--uhf-serial`, nonempty and different. Matching
  discovery must identify exactly one driver=lime Mini per serial; missing,
  duplicate or ambiguous selections fail, never pick the first device.
- Speech lowpass: 129-tap Hamming-windowed sinc, 3 kHz. USB: positive-frequency
  analytic signal using 513-tap Hilbert transform and matched 256-sample delay
  on both TX and RX (RX rejects the negative-frequency unwanted sideband).
  AM: carrier envelope `0.5*(1+0.8*audio)` and envelope detector with slow
  carrier tracking. FM: continuous phase, ±2,500 Hz deviation and conjugate
  phase discriminator. Audio output DC blocker approximately 30 Hz.
- RF normalized peak drive is capped at **0.1**; TX gain is set to the
  driver's advertised minimum, not a guessed wattage. This is **not** a
  measured power limit, legal power authorization or PA protection.
- Initial nominal/tuned RF bands: inclusive 144–146 MHz and 430–440 MHz,
  crossband selected audio RX/TX only. Each VHF/UHF device has independent
  RX/TX streams and LO readbacks; **both RX workers run concurrently**.
  Each worker has bounded8-block resource queue,10ms driver read timeout,
  explicit fault on overflow/read failure, never IQ silence fallback.
  Both RX queues are continuously consumed, with no implicit audio mix.
  The selected RF backend is two replaceable LimeSDR Minis, contingent on
  actual device/rate/full-duplex verification.

At1MSPS CF32 application buffers, two RX streams represent16MB/s total and
one TX stream8MB/s additional payload, excluding device wire format, USB
overhead and processing. This is arithmetic, **not measured USB capacity**.
Official CM5 IO board/qualified hub/power topology, simultaneous sustained transfers, ARM64
DSP/BLE scheduling and thermal behavior remain unverified. Queue capacity
is a resource bound, not an assurance of uninterrupted reception.

Both Lime devices use their native USB3 connections. An additional USB
audio interface requires a qualified hub/USB2 host topology, or a separately
validated audio alternative. I2S routing may conflict with SPI1 motion
resources; this radio implementation does not invent a pin allocation,
USB port/hub qualification or I2S solution. BSP, NC E-stop and independent
watchdog commissioning remain mandatory blockers to physical TX approval.
The production hardware rate is requested1MSPS (accepted configured range
192k..4M, hence above100k);96k is **only the internal DSP clock**, not a
claimed Lime hardware rate or old single-device configuration.
- `rangeRateMps > 0` means receding; approaching is negative.
  `RX=baseRX-round(baseRX*rangeRate/c)`,
  `TX=baseTX+round(baseTX*rangeRate/c)`; `c=299792458 m/s`.
  Both shifts and tune readbacks use integer Hz. Verified rates expire
  after 1 second monotonic age or UTC skew >2 seconds. Finite satellite
  rates bounded at ±12,000 m/s, valid site lat/lon/height required. No GNSS
  is fabricated. Stale tracking returns RX to nominal and inhibits TX.

No over-air autotuning: CAT/base-frequency/mode/actual Doppler retuning
first deactivates TX and revokes its lease. A fresh lease is required.
Continuous Doppler updates can consequently cause TX interruptions; do
not bypass this by changing frequency on an active stream.

LimeSDR Mini nominal low-level output is approximately **10 dBm maximum**,
not 5 W. Desired commissioned system output is **5 W FM**, **5 W PEP USB**
and **1 W AM carrier**. These are design objectives, not achieved/measured
output or software promises. A suitable linear PA, mode-dependent drive/
bias, filtering, isolation/duplexing, thermal protection and measured RF
commissioning are required. The software drive amplitude cap is a
**read-only normalized IQ limit0.1**, with minimum advertised TX gain; it
is not a watt estimate, calibration or PA control. External PA commissioning
remains future hardware scope. Startup/discovery/rate configuration never
automatically activates TX; all interlocks remain required.

The separately owned CM5 `RotorController` integration is expected to
provide verified autonomous SGP4/GNSS tracking and three-axis safety state.
Its concrete fields/adapter contract are **not assumed** by this subsystem;
parent coordination will freeze them before adding an adapter. Until then,
the transport-neutral `TrackingInput` and `Safety.rotor_update` boundaries
remain available but unprovisioned in the production CLI, so TX stays denied.

### Actual `--rotor` public-hook binding (physical BSP still required)

`--rotor PATH` reads `{"v":1,"controllerConfig":"relative-or-absolute-path"}`.
No arbitrary Python module, mock selector or commissioning override is
accepted. The prepared loader requires fixed local module
`rotor.radio_adapter.open_adapter(controllerConfigPath)` and methods
`snapshot()`, `dispatch(path,op,data,authenticatedPeer)`,
`disconnect(authenticatedPeer)`, `close()`. These methods are verified in
the actual `rotor/radio_adapter.py`. Its factory requires **exactly one**
installed entry point group`portable_sat_rotor.hardware`, name`cm5`,
which receives the existing controller config path and returns an actual
`RotorController`; no mock/dummy production composition is provided.
Missing module/factory/BSP aborts explicit integration, with no fallback.
This software hook binding is not physical end-to-end commissioning.

Snapshot schema: `sampledMonotonic` (same-host monotonic seconds),
`hardwareCommissioned:true` (actual backend attestation, not config),
`gnssValid:true`, `sgp4Valid:true`, `fault:null` (or fault string),
`rangeRateMps`, `utc` Unix seconds, `site:[lat,lon,heightM]`,
`gnssSampledMonotonic`, `trackingSampledMonotonic`, and nested `status`.
Maximum snapshot age200ms, GNSS/SGP4 source age1s; poll50ms, deadline200ms.
Tracking retains the older GNSS/SGP4 sample timestamp; a newly retrieved
snapshot cannot refresh old orbit/fix state. Old timestamps are never
refreshed merely by polling. Invalid GNSS/SGP4/BSP/watchdog/rotor state
revokes tracking/TX. This prepared transport does not prove hardware
attestation or implement actual sensors.

Radio authenticated session identity is passed unchanged to the adapter,
distinct from legacy ESP32 sessions. Verified actual CM5 routes retain
the v1 envelope: `/rotor/status` get, `/rotor/sensorsstatus` get,
`/rotor/home` set, `/rotor/calibrate` set, `/rotor/stop` set,
`/rotor/target` set **requires all three** finite `azDeg`, `elDeg`, `polDeg`
(no missing-POL/two-axis defaults), `/rotor/track` set `{"noradId":integer}`,
`/satellites/catalog` get, `/satellites/passes` get. Controller validates
all operation payloads, mechanical limits, homing and calibration, rather
than the radio inventing them. Unknown presumed legacy aliases are rejected.
Status/stop/home/calibration/catalog remain callable before GNSS tracking
readiness; unavailable tracking inhibits TX but must not prevent homing.
Snapshot validity errors retain the host service for diagnostics, while
transport/deadline failures stop the integration fail-closed.
Actual controller `ok`, `data`, `error` are preserved in the outer v1
response, adding `schema:"cm5-rotor/v1"`; denied motion is never reported
as successful radio dispatch. Never claim ESP32 firmware0.2.0 or equate
POL with CP handedness.
This scope does not invent a verified mechanical POL range.

## Safety / physical integration

### Frozen revision-A production radio requests — hardware HOLD

`hardware/cm5/interface.json` is authoritative and unmodified. Production
adapter `RadioGPIOProduction` owns **only BCM22 VHF PTT request and BCM23
UHF PTT request**. It reads the shared MCP23017 at0x20 **without configuring
or writing motor/encoder GPIO**: BANK0 required, GPA4..7 must be inputs.
GPA4=`PTT_VHF_FEEDBACK_N`, GPA5=`PTT_UHF_FEEDBACK_N` are independent
contact/sense inputs; GPA6/7 are active-low PA faults. All suffix `_N`
signals assert LOW; external pull-ups/open feedback never imply permission.
Stuck asserted feedback before request, both asserted, PA fault, wrong
direction/bank or I2C failure deassert both requests. Request output
readback is **not a hardware permit** and never an RF CP acknowledgement.

A live independent external guard must attest actual commissioned circuit,
local physical arm/PTT, NC E-stop, watchdog and RF-path health with
monotonic age≤50ms. Config is root-owned/not writable by other users and
requires explicit commissioning, but **that flag alone cannot establish
hardware trust**. `radio/gpio-hold.example.json` deliberately has
`hardwareCommissioned:false`. `--radio-gpio PATH --gpio-contract PATH`
fails closed because the physical external guard provider/circuit remains
unimplemented. It cannot silently use the generic GPIO path; simultaneous
`--gpio-chip` is rejected. Parent must bind the verified shared BSP guard
before physical commissioning. No CP-switch pin routing is invented.

The dual-chain adapter can consume this guard and requires independent PTT
feedback before SDR TX activation, reevaluating feedback at each guarded
write. Stop drops both GPIO requests first, even if one device driver fails.
Polling and Python deadlines are not substitutes for the independent
hardware gate/watchdog. **This is production-adapter code with test-only
I/O verification, not released or physically verified safety hardware.**

Boot starts unarmed, unkeyed, no session, no lease and SDR-not-ready. GPIO
arm and local physical PTT are active-high **separate** gpiod v2 input lines
with pull-down. A third active-high output controls an **external normally
off RF gate**. Remote commands never set either physical input.
All TX requires: authenticated connected audio session, physical arm,
physical PTT, fresh verified tracking, actual successful RX read + setup
TX stream, valid crossband frequencies, unexpired lease, acknowledged/
settled RF polarization and fresh verified motion safety status.

### RF polarization is not mechanical POL roll

The confirmed third rotor motor is **POL axial roll, limited travel**.
Its candidate ±90° mechanical range remains TBD; no continuous rotation
or motion-board pinout is assumed here. Axial roll does **not** change
circular-polarization handedness. A separate RF switch/network and
compatible circular antenna are required for RHCP/LHCP.

RF enums are `LINEAR`, `RHCP`, `LHCP`. No mode is advertised or reported
configured without locally verified antenna/network/switch capability.
The default runtime has **no approved RF switch adapter**, so capabilities
are empty, configured is null and TX is denied. This is a release blocker,
not a simulated success. `PolarizationSwitch` first revokes the lease and
successfully stops TX, then requires actual TX-off acknowledgement before
switch writes. A locally integrated `GPIOAcknowledgedSwitch` uses real
gpiod output lines and **independent contact/sense input lines** with a
verified truth table and measured settle time; output-latch readback is
not sufficient. Its locally supplied TX-off feedback callback must verify
the RF gate/SDR off condition, not merely return the software requested state.
Configured remains null until settle time elapsed **and** feedback matches.
Feedback mismatch/loss inhibits TX through the same lease/gate watchdog.
Switch requests do not automatically renew PTT.

Motion integration must deliver `Safety.rotor_update(fault, verified=True)`
from a verified local safety source, fault=null only when healthy, refreshed
within 500 ms. Unknown/untrusted/stale status or any rotor fault blocks TX;
E-stop/watchdog/driver faults must appear here. BLE clients cannot report
the rotor healthy or provision this trust. Three-axis driver integration,
NC physical E-stop wiring and independent watchdog verification remain
separate tasks.

Lease is 1–500 ms; Android must renew at most every 200 ms. Release,
disconnect, malformed/gapped PCM, queue/credit faults, audio stop, CAT
timeout/disconnect, SDR timeout/short write/activation/deactivation fault,
expired tracking/lease and GPIO faults revoke TX. PCM starvation >50 ms
pauses TX; no zeros are manufactured. Microphone frames received while
unkeyed are discarded, not replayed on later PTT.
The independent GPIO watchdog polls every 10 ms and drops the physical
gate before driver stop. Driver read/write timeouts are 10 ms. Scheduling,
OS failure or a wedged native driver cannot provide a hard real-time safety
guarantee: **external normally-off gate + hardware watchdog + verified
release wiring are mandatory before physical TX approval**. Linux process
exit alone is not a reliable electrical gate. Do not interpret unit tests
as proof that RF actually stops.

## Bluetooth GATT contract version 1 (frozen)

The UUIDs below are all distinct from the rotor:

| Purpose | UUID | Properties |
|---|---|---|
| Service | `c8201001-4e53-4253-9000-000000000001` | primary |
| Control RX (host → Android) | `c8201002-4e53-4253-9000-000000000001` | notify/read |
| Control TX (Android → host) | `c8201003-4e53-4253-9000-000000000001` | write with response |
| Audio RX (host → Android) | `c8201004-4e53-4253-9000-000000000001` | notify/read |
| Audio TX (Android → host) | `c8201005-4e53-4253-9000-000000000001` | write with response |

BlueZ exports real `GattService1`, `GattCharacteristic1`, ObjectManager and
LEAdvertisement1 over the **system D-Bus**, registers GattManager1/
LEAdvertisingManager1, and emits PropertiesChanged for Value. The Linux
adapter must support peripheral mode. Pair/bond using OS secure
authenticated pairing (MITM/passkey or numeric comparison); characteristic
flags `encrypt-authenticated-write/read` are enforced by BlueZ. Only one
provisioned Device1 path, bonded/paired/trusted/connected, may be connected.
A second connection stops streams. Do not infer encryption from a
nonexistent `Encrypted` Device1 property; authenticated security flags
are the security boundary. Stock Just Works pairing may be insufficient.

Control packets are exactly 20 bytes:
`magic[0]=0x53`, `flags[1]` bit0 START, bit1 END, other bits zero;
`sequenceLE16[2:4]`; JSON UTF-8 fragment `[4:20]`.
One sequence per complete message, all fragments same sequence;
final zero padding removed only after reassembly. Maximum JSON 4096 bytes.
Interleaving, overflow and sequence mismatch rejected. Fragmentation is
the same **format** as a 20-byte rotor channel, not the same service/API.

Requests:
`{"v":1,"id":"client-unique-id","path":"/status","op":"get","data":{}}`

Responses:
`{"v":1,"id":"client-unique-id","path":"/status","ok":true,"data":{},"error":null}`

Events use `id:"event"` and the same reply envelope. No authentication
token is included in replies, status, logs or repository.

| Path / operation | Request data | Response / effect |
|---|---|---|
| `/auth` set | `{"token":"64-hex-private-token"}` | `{"fw":"radio-host/1.0.0"}` |
| `/status` get | `{}` | mandatory `profiles` keyed VHF/UHF with serial,rxHzReadback,txHzReadback,rxRateReadback,txRateReadback,rxReady,rxReads,queueDepth,fault,txActive; `rxChannel`,`txChannel`,`txPolicy:"ONE_TX_ONLY"` plus nominal/actual Hz, mode, interlocks and counters |
| `/radio` set | optional `rxHz`, `txHz`, `mode`=`FM`/`AM`/`USB` | revoke lease/stop audio, validate crossband |
| `/rf/polarization` get | `{}` | `{requested,configured,ready,capabilities}`; configured null unless hardware settled/acknowledged |
| `/rf/polarization` set | `{"mode":"LINEAR"}` or `RHCP`/`LHCP` | TX-off acknowledgement, verified switch capability and settling required; no automatic PTT |
| `/audio/start` set | `{"rate":8000,"mtu":247,"rxChannel":"VHF","txChannel":"UHF"}` or reversed channels | `{"rate":8000,"rxStreamId":uint32,"txStreamId":uint32,"txCredits":16,"rxChannel":"VHF","txChannel":"UHF","txPolicy":"ONE_TX_ONLY"}` |
| `/audio/stop` set | `{}` | stop both PCM streams, revoke lease |
| `/ptt` set | `{"enabled":true,"leaseMs":500}` | lease only if every interlock satisfied |
| `/ptt` set | `{"enabled":false}` | immediate inhibit |
| `/tracking` set | `{"rangeRateMps":number,"utc":unixSeconds,"site":[lat,lon,heightM]}` | **locally provisioned verified tracking source only**, invalidate previous lease |
| `/audio/credit` event | host output only | `{"txCredits":0..16,"txStreamId":uint32-or-null}` absolute available window |
| `/fault` event | host output only | `{"reason":string-or-null,"rxDropped":counter,"txFaults":counter}` |

Subscribe Control RX before `/auth`, authenticate, subscribe Audio RX,
request negotiated ATT MTU >=247, then start audio. The request's `mtu`
must match the **actual BlueZ WriteValue options MTU**. Unknown MTU,
insufficient MTU, non-8000 rate or MTU change is rejected; do not claim
8 kHz audio in 20-byte control frames. Bonding does not substitute for token.

**Mandatory updated v1 keys:** `rxChannel` and `txChannel` must be explicit
VHF/UHF, different, in every `/audio/start`. Older single-radio start
requests lacking them are rejected. Audio header/UUID/version remain
unchanged; successful start binds each stream ID to its declared channel.
Changing selection requires a new start/new IDs and revokes PTT. Android
must label PCM/APRS/SSTV using this stream-to-channel mapping, not assume
VHF or mix streams. `profiles`/channel/`txPolicy` status replaces the stale
single-chain schema; clients must not infer that one ready chain means both
are ready. Both profiles are monitored; a fault inhibits the global TX.

### Exact frozen v1 status schema

`/status` get returns the standard reply envelope with these data keys:
`fw`, `rxHz`, `txHz`, `mode`, `actualHz` (ordered `[RX,TX]`),
`sdrReady`, `tx`, `physicalArm`, `physicalPtt`, `trackingFresh`,
`rfPolarization` (`requested`, `configured`, `ready`, `capabilities`),
`rotorFault`, `rotorReady`, `profiles`, `rxChannel`, `txChannel`,
`txPolicy:"ONE_TX_ONLY"`, `driveAmplitudeLimit:0.1`, `fault`,
`rxDropped`, `txFaults`, `txCredits`.
With dual hardware configured, `profiles` has exactly `VHF` and `UHF`;
each contains `serial`, `rxReady`, `rxHzReadback`, `txHzReadback`,
`rxRateReadback`, `txRateReadback`, `rxReads`, `queueDepth`, `fault`,
`txActive`. With no hardware configured `profiles` is empty and
`sdrReady` false—never success-shaped dummy profiles.

Direction names are from the host perspective, verified against
`radio/protocol.py`: **1002 is host→Android control notify/read**;
**1003 is Android→host control write-with-response**. Audio1004 is
host→Android notify/read; audio1005 is Android→host write-with-response.
Any earlier report reversing1002/1003 is superseded by this table and
the implementation constants. UUID suffix, framing version1 and16-byte
audio header are unchanged for the dual-radio update.

Audio frames, both directions, have **16-byte header**:

| Offset | Field |
|---|---|
| 0 | version `1` |
| 1 | flags `0` (reserved, reject unknown) |
| 2–3 | reserved LE16 `0` |
| 4–7 | streamId LE32 |
| 8–11 | sequence LE32 |
| 12–15 | sampleIndex LE32 |
| 16… | even-length PCM S16LE mono, no compression |

Payload maximum `min(actualMTU-3-16,228)` bytes, maximum **114 samples**
at MTU247; packets shorter than one sample rejected. RX/TX independent
stream IDs, counters start at zero on each successful start, modulo 2³².
Sequence advances once per packet; sampleIndex advances by samples in
that packet. No silent padding, retransmission concealment or zero fill.
TX sender spends one credit for each packet; initial window16. Credit
events are absolute snapshots; ignore a `txStreamId` not matching the current
stream lifecycle and do not add credits as deltas. Use write-with-response and serialized
control transactions. TX queue capacity16; receive overflow/gap/duplicate/
reordering/bad stream ID/malformed header faults and stops audio.
RX queue capacity16; overflow counts dropped frame, stops stream and
reports status/fault rather than silently truncating. Notification emission
counts are not proof of remote Android receipt; Android MUST validate RX
sequence/sample index and report its own loss. Restart audio explicitly
after a fault. No service shares rotor audio or rotor control state.

Token persistence is a host-private regular file, default
`~/.local/state/portable-sat-radio/token`, owner-only permissions0600
and parent0700 when newly provisioned. Protect it as a secret during
out-of-band phone provisioning. Symlinks/world-readable files rejected.
Windows unit tests do not prove POSIX permission behavior.

## Localhost CAT subset

Original implementation, not copied firmware. TCP bound **127.0.0.1**
only, default port4532; ASCII commands terminated by `;`.
`FA;` query RX `FA00145900000;`, `FB;` query TX; set with exactly
11 decimal frequency digits. `MD;`, `MD2;` USB, `MD4;` FM, `MD5;`
AM. **MD1 LSB is unsupported** and returns `?;`.
`RX;` inhibits TX. `TX;` is always denied (`?;`): CAT cannot attest
the BLE session, physical inputs or lease. Unsupported/malformed commands
return `?;`. Successful sets return no data, Kenwood-style. Bounded
256-byte command accumulation, 2-second receive idle timeout.
CAT is unencrypted/local-only and never a network remote PTT API.

## Installation / validation (no global pip installs)

Python >=3.11. Separate radio project uses setuptools; no existing Python
manager was present. On Linux install distro SoapySDR Python bindings and
the **actual device driver** using the distribution's package manager.
SoapySDR is intentionally not a generic pip/dummy dependency. Create a
project venv with system-site-packages so distro Soapy is visible:

```sh
python3 -m venv --system-site-packages radio/.venv
radio/.venv/bin/python -m pip install -e './radio[integration-test]'
radio/.venv/bin/python -m unittest discover -s tests/radio_host -v
radio/.venv/bin/python -m radio.main --discover
```

Discovery only is read-only; the command does not activate TX. An empty
discovery is an empty list, not working hardware. Import errors/unsupported
driver/range/rate/faults abort operation. No test IQ backend is selectable
from CLI.

Runtime requires `--peer /org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX`.
Supply exact unique discovery serials for **both** `--vhf-serial` and
`--uhf-serial` only after physical module verification. Without serials
BLE/CAT can run but SDR-ready remains false. GPIO options are
`--gpio-chip`, `--arm-line`, `--ptt-line`, `--gate-line`; without GPIO
physical arm/PTT remain false. D-Bus permissions, secure OS pairing and
Linux deployment are not validated on this Windows workstation.

Tests use **explicit test-only** injected API objects and synthetic IQ/PCM;
never physical RF. Test FM/AM/USB known tone roundtrip gain/correlation/
frequency/SSB sideband rejection, streaming block invariance, integer-Hz
Doppler direction, gate expiry/release/faults, framing/MTU/queue/credit,
JSON authentication and localhost CAT sockets. Measured results and
acceptance tolerances are printed by the DSP tests. No square-wave FM
placeholder, no success-shaped hardware simulation.

### Recorded workstation evidence

Windows Python 3.13.14 in `radio\.venv`, numpy and dbus-next installed only
into that project environment. VS Code Python environment and test tools
were attempted but unavailable/not discovering these unittest files;
explicit venv `unittest` is the executable verification.
All **57 offline unittest cases pass**, including actual public-adapter
binding with test-only controller and reply propagation/source-age checks,
production-guard denial
preventing SDR TX, revision-A independent
feedback/stuck/double-contact/PA-fault/guard-link tests, explicit standalone manual
confirmation/no-Doppler/no-rotor policy, no automatic fallback and single-radio
selection, plus prepared rotor boundary
trust/staleness/three-axis/session tests (not actual RotorController integration),
dual runtime selected-audio/
single-TX routing, dual explicit serials,
single-TX arbitration, bounded dual RX queue faults, hardware-rate readback,
rational streaming/alias rejection, RF switch TX-off/settle/
feedback/no-hardware cases, rotor fault/freshness and transport-neutral local
tracking (without ESP32/BLE), source trust/revocation, PCM-starvation/no-fill and
physical-gate-before-driver-stop tests (explicit test-only I/O).
The setuptools wheel `portable_sat_radio_host-1.0.0-py3-none-any.whl`
builds successfully (ignored local `radio\dist` build output).
CLI `--help` and compile validation do not initialize RF hardware.
The `integration-test` extra supplies the actual rotor module's import
dependencies for the repository public-adapter test. It does not install
or fabricate a hardware BSP. Standalone radio installation may omit this
extra; integrated deployment separately installs the real rotor package
and qualified CM5 hardware provider.

Known 700 Hz, 0.45-amplitude PCM → IQ → PCM, ignoring initial filter
settling and searching deterministic sample delay:

| Mode | Frequency Hz | Correlation | Gain | Residual RMS |
|---|---:|---:|---:|---:|
| FM | 699.429 | 0.999755 | 1.020135 | 0.007186 |
| AM | 699.429 | 0.999704 | 1.020002 | 0.007895 |
| USB | 699.429 | 0.999543 | 1.018134 | 0.009795 |

Acceptance: frequency error <2 Hz, correlation >0.995, gain0.94–1.06,
residual RMS <0.025. USB unwanted 1 kHz sideband rejection measured
**63.99 dB TX and RX**, required >25 dB. These are digital measurements,
not analog RF purity or power measurements.

Additional96k↔1MSPS resampler measurements: 1kHz complex tone recovered
1000.000000Hz, amplitude0.999765 (frequency tolerance0.1Hz, gain±0.02);
100kHz out-of-band tone downsampling alias suppression66.01dB (>40dB).
PCM→mode IQ→1MSPS→96k→PCM700Hz tone recovered699.529Hz, gains
FM1.020141, AM1.020569, USB1.018227 (frequency±2Hz, gain0.94–1.06).
Streaming whole/split-block outputs match within1e-12. These synthetic
tests do not measure real Lime/USB behavior.
