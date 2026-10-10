# Android digital receive and prepared APRS audio

The Android application includes actual PD120/PD180 SSTV image and Bell 202
AFSK1200 AX.25/APRS packet decoding, plus APRS callsign-to-callsign short
message composition and local Bell 202 audio export. The feature is an optional
activity, separate from legacy rotor navigation and its on-wire protocol. The
existing rotor BLE service remains rotor-only and is not reused for radio audio.
Digital DSP remains transport-independent. A separate radio-host activity
implements the documented `radio-host/1.0.0` BlueZ GATT protocol; it does not
reuse the legacy rotor GATT service, parser, MTU or command model.

The SSTV, AFSK/AX.25/APRS decoders and APRS message/audio encoder are
transport-independent Kotlin DSP/protocol components, exercised by JVM
fixtures and reused by both offline import and host-stream receive.
Physical Bluetooth interoperability benchmarks remain required and are not
complete.

The planned station architecture is a Raspberry Pi CM5 host with two
replaceable LimeSDR Mini devices, supporting concurrent VHF/UHF
receive and a one-transmitter-at-a-time policy. No ESP32 audio bridge is part
of this plan. The repository now contains the authoritative Linux/BlueZ
`radio-host/1.0.0` contract and Linux source are authoritative for the
dedicated Android radio activity. The app implements bonded-device selection,
token authentication, version/status parsing, explicit VHF/UHF RX/TX channel
binding, actual MTU negotiation, 8-kHz bidirectional PCM, continuity checks,
absolute TX credits, FM/AM/USB tuning, explicit standalone-manual confirmation,
host polarization capability selection, voice playback, live mic TX, and
APRS audio TX. TX buttons remain disabled unless audio is ready, the app-local
arm confirmation is selected, and a host status no older than two seconds
reports the selected TX channel and required host interlocks. Stale status
disables TX until the user requests a fresh status. Profile readbacks outside
the app's supported VHF/UHF bands for the selected profile are rejected. The
implementation does **not** verify the physical BlueZ link,
the companion computer, LimeSDR, RF path, antenna, law/licensing, drive
levels, or over-air reception/transmission. Keep this service separate from
optional legacy rotor support. The frozen rotor status parser and protocol
remain unchanged. No local SGP4 prediction or guessed radio/rotor API is
introduced here.

The orbit panel in the separate radio-host activity uses only authenticated
host v1 requests and actual `cm5-rotor/v1` replies. It exposes GET
`/rotor/status`, GET `/rotor/sensorsstatus`, GET `/satellites/catalog`, GET
`/satellites/passes` (`noradId`, optional `limit`), SET `/rotor/track`
(`noradId`), SET `/rotor/target` (all three finite `azDeg`, `elDeg`, `polDeg`),
and SET `/rotor/stop`. A successful reply must contain `schema`,
`ok:true`, and object `data`; failures must preserve explicit `ok:false` and a
nonempty `error`, which the UI displays. Unsupported or mismatched routes,
operations, payloads or schemas fail rather than appearing successful.
Remote `/rotor/home` and `/rotor/calibrate` are intentionally not exposed:
the CM5 controller requires trusted local-console confirmation for them.

Host results are shown as returned JSON; the Android app does not invent an
orbit snapshot, reinterpret unknown catalogue/pass fields, propagate TLEs, or
claim a target was reached from command acceptance. `OrbitSnapshotJson` is
proposed-only, not an implementation of a host response schema. The map,
radar, rich pass presentation, radio profiles and measured/requested axis
snapshot therefore remain explicitly unavailable until the host publishes a
verified response model and the app binds it. The rotor routes are separate
from radio-host `/status`; local-only `integration_snapshot()` is not treated
as an Android endpoint.

**Host PCM transmission is not a verified radio transmission.** Composed
packets may still be exported as WAV offline. The separate radio screen can
send PCM to the authenticated host only after fresh status, local confirmation,
the host's reported physical arm/PTT input indications and RF interlocks,
audio credits and the
short PTT lease pass. It releases the lease on completion, stop, failure,
backgrounding, timeout or disconnect. A host accepting PCM or PTT does not
prove RF output, over-air reception, APRS delivery or ACK. No automatic
speaker-playback PTT, A2DP/HFP digital-radio transport, APRS-IS/mobile-SMS
gateway, encryption, or hardcoded digipeater route is provided.

The host status fields `physicalArm` and `physicalPtt` describe physical input
indications; `physicalPtt` does not confirm independent GPIO PTT output
feedback. The Linux host checks active-high PTT request outputs against
independent active-low MCP23017 GPA4/GPA5 feedback inputs and GPA6/GPA7 fault
inputs before granting or maintaining a lease. Android does not receive those
GPIO feedback pins as separate `/status` fields: host lease acceptance is
required before PCM streaming, and denial fails closed. This is not evidence
of RF output or over-air transmission.

## Dedicated radio-host audio

From the main screen open **Separate radio host**. Connect only to an
explicitly selected, already bonded BLE host. The user supplies its private
64-hex token at connection time; the app does not persist or log it. BlueZ
must require authenticated secure pairing and protected characteristics;
being bonded in Android is not itself proof of MITM quality. Host-side
authentication, protocol version and safety policy are authoritative.

The radio service is distinct from the rotor service and uses the frozen
contract in `docs/RADIO-HOST.md`: UUID `c8201001-4e53-4253-9000-000000000001`;
host→Android control notify/read `c8201002-4e53-4253-9000-000000000001`;
Android→host control write-with-response `c8201003-4e53-4253-9000-000000000001`;
host→Android PCM notify `c8201004-4e53-4253-9000-000000000001`; and
Android→host PCM write-with-response `c8201005-4e53-4253-9000-000000000001`.
Android subscribes/authenticates, parses current status, subscribes audio,
then negotiates actual ATT MTU ≥247 before a user explicitly starts a stream.
PCM is mono S16LE at 8000 samples/s with the 16-byte little-endian
version/flags/stream/sequence/sample-index header and at most 114 samples per
packet at MTU247. The app requires ordered sequence/sample counters and the
selected stream ID; a malformed, stale or discontinuous frame stops audio and
invalidates the capture. It never fills missing samples. Every audio start
requires explicit RX/TX channel fields. With the current two-Lime build this
means opposite-band VHF/UHF selections, never same-channel or mixed streams.
The documented one-radio standalone build accepts the same sole channel for
RX and TX. The Android status display shows each configured profile's serial,
actual RX/TX frequency and sample-rate readbacks, RX-read count, queue depth
and fault.
The host's 1 MSPS SDR hardware rate/readbacks are distinct from its 96 kSPS
internal complex DSP baseband and the 8 kSPS BLE audio stream. These are
reported/configuration values, not proof of physical LimeSDR application or
RF function. There is no audio streaming before explicit start, and host
operation-profile, actual channel and band validation still control.

An RX capture is bounded to 240 seconds and 1,920,000 S16 samples (about
3.7 MiB), then stopped and decoded. Stop/decode also stops host audio and
releases any active TX lease first. Digital decoders require the user-selected
PD120, PD180 or AX.25/APRS mode. The optional voice monitor is an explicit
Android playback action using decoded host PCM; it has a 16-packet queue,
stops rather than concealing queue loss, and cannot enable PTT. Android
playback output is not represented as an A2DP/HFP transparent audio link.

Voice TX requires a user-selected built-in/USB/wired input and explicit
`RECORD_AUDIO` permission; Bluetooth system microphone inputs are excluded.
The integrated microphone hears speaker/environment audio, **not RF**. PCM
is streamed to the host as captured (not recorded or speaker-played), bounded
to 240 seconds, and stopped if queue/credit/write/status/interlock/lease
checks fail. Live APRS TX uses the app's existing AX.25 UI/FCS/HDLC
bit-stuffing/NRZI/Bell 202 encoder and the same gated PCM stream. The user
must configure callsign, addressee, optional explicit digipeater path and
message ID, confirm unencrypted legal content, then explicitly confirm the
host lease/send dialog. APRS requires host-reported FM. The UI says only that
the **host accepted PCM**; received ACK/rej content is not matched to a local
message or used to assert delivery.

SAF WAV export remains a separately prepared offline waveform, not a host
send. Do not play it into a radio microphone, use voice-activated PTT, or
assume exported or host-accepted PCM was transmitted. For safe RF bench
validation, independently follow applicable local amateur-radio rules, host
hardware documentation and qualified dummy-load/isolation procedures.

## Choosing and connecting the audio source

Open **Digital receive · SSTV / APRS** from the existing app screen. The
activity enumerates audio inputs reported by Android and selects USB audio
first when a USB audio input is present; otherwise it selects the built-in
microphone, or the first reported input. A user can change the selection and
refresh the list. The chosen Android input is explicitly routed through
`AudioRecord.setPreferredDevice`; if that route is not actually active, capture
fails visibly instead of silently switching to the microphone.

For direct receive audio, use an isolated, appropriately attenuated USB audio
interface connected to the radio/receptor audio output. Check the radio and
interface specifications and make a safe, isolated connection before
connecting. Do not connect speaker-level output directly to a phone input
unless the particular interface is rated for it. A phone's built-in
microphone hears the receiver speaker or ambient sound: **it is not an RF
receiver** and is subject to room noise, AGC and echo. No audio input itself
receives or tunes RF. A separate receiver/radio and antenna are required.

Live capture is initiated by an explicit button, then a disclosure and the
Android `RECORD_AUDIO` permission request. Recording is restricted to this
visible foreground activity and stops when the user selects **Stop and
decode**, navigates away, the audio input fails, or the strict 240-second
bound is reached. A 48 kHz capture reserves no more than about 23 MiB for
16-bit mono audio; processing works on the same background worker. Leaving
the screen stops and discards an unfinished capture. No background service,
cloud upload, audio telemetry, PTT, radio-CAT operation or phone-location
access is added.

Bluetooth headset/SCO system audio is not used as a radio-host transport or
microphone source. The dedicated GATT audio transport is separate and follows
the Linux contract; physical host pairing, MTU, notification timing, stream
continuity and audio quality still require hardware interoperability testing.
The existing rotor BLE service/MTU behavior remains untouched.

## Local file input and export

**Import PCM WAV** uses Android's Storage Access Framework document picker. The
decoder reads only RIFF/WAVE linear PCM (format tag 1), 8/16/24/32-bit
little-endian samples, 1 or 2 interleaved channels, and sample rates
8000–48000 Hz. Stereo is averaged to mono. A WAV is limited to 50 MiB and
240 seconds, including before resampling; unsupported/compressed WAV, malformed
chunks, truncated data and out-of-range audio fail explicitly. The reader
resamples accepted audio to 11025 Hz with a windowed-sinc low-pass before FM
demodulation. Float WAV, IEEE-float WAV, compressed WAV, WAV extensible format,
and non-WAV inputs are not supported. Exported AFSK audio is mono signed
16-bit little-endian PCM at 8000 samples/s, preserving the 1200/2200 Hz Bell
202 tones; import resamples it through the same receive pipeline.

`PcmSource`/`PcmSink` pass mono signed-16 samples in bounded blocks. Each block
carries a monotonically increasing sequence and first-sample counter;
collection and WAV writing reject gaps instead of filling or hiding missing
audio. Current adapters are Android `AudioRecord` capture and bounded local
PCM/WAV import/export. The metadata is an internal continuity contract, **not**
a proposed Bluetooth GATT wire format; any future adapter must implement the
separately documented radio-host framing, sequence and sample-counter rules,
not infer them from this internal PCM API.

Successful SSTV output is shown at its native 640 × 496 pixels and can be
saved as PNG through the SAF document picker. Successfully decoded AX.25
frames can be saved as UTF-8 text through the same picker. The log includes
source/destination/path, frame-control information and printable APRS
interpretation, and only lists frames whose AX.25 FCS passed validation. These
logs are local only; their actual destination and retention are selected by
the user.

## Implemented signal and frame formats

### PD120 and PD180 SSTV

The selected demodulator uses a 31-tap windowed Hilbert analytic signal and
sample-to-sample quadrature phase difference to recover audio instantaneous
frequency (FM). It detects the analog SSTV header (two 300 ms 1900 Hz leaders
separated by 10 ms at 1200 Hz), then decodes the 30 ms VIS start/data/parity/
stop symbols. The low-to-high VIS data bits are decoded as 1100 Hz = 1 and
1300 Hz = 0; parity is checked and only VIS `0x5f` PD120 and `0x60` PD180 are
accepted. Explicitly chosen mode and decoded VIS must agree.

The image decoder uses the two mode line durations (PD120 component scan
121.6 ms; PD180 183.04 ms), each 20 ms horizontal 1200 Hz sync and 2.08 ms
1500 Hz porch. It verifies every line sync and porch. A transmitted line group
contains 640 samples for Y0, Cr (R−Y), Cb (B−Y) and Y1; its shared 4:2:0
chrominance is expanded across the adjacent Y rows and converted to RGB. The
result is the complete 640 × 496 image; missing lines/sync, bad VIS/parity,
wrong mode, short data, silence or signal outside the supported component
frequency limits is an error rather than a partially or synthetically filled
image. Headers must be within 5 ms of the decoder's coarse alignment and
composite line timing follows the nominal standard; large clock drift,
transmitter sync warble, extreme noise and severe fades may be rejected.

### Bell 202 AFSK1200 / AX.25 / APRS

The AFSK receiver uses the same measured FM-audio frequency, samples 1200
symbols/s at symbol centers and recognizes the Bell 202 1200 Hz mark and
2200 Hz space tones. It decodes NRZI (no transition = one, transition = zero),
detects `0x7e` HDLC flags, removes a stuffed zero after five consecutive data
ones, assembles LSB-first octets and bounds frames to 512 bytes. AX.25
destination, source and up to eight digipeater addresses, SSIDs and repeated
flags are parsed; both UI and non-UI control/PID-bearing packets are logged.
Frames are displayed only after their little-endian AX.25 FCS passes CRC-16/
X.25 (reflected polynomial `0x8408`, initial/final XOR `0xffff`). Duplicate
valid frames in the same recording are presented once. A recording with no
valid frame reports failure; a failed CRC is never labelled a packet.

Printable APRS UI packets with PID `0xf0` are interpreted as APRS text.
Implemented presentations include uncompressed `!`/`=` positions,
timestamped `/`/`@` positions, `:` messages and `>` statuses/queries, plus
the original printable payload as appropriate. Standard
`DDMM.hhN`/`DDDMM.hhE` coordinates are checked and displayed in signed decimal
degrees. Other printable APRS content remains text; compressed/base-91
positions, Mic-E, telemetry, object/item-specific semantics, addressees or
paths beyond the basic AX.25 address representation, and non-UI/APRS
application payloads are not decoded as such. The bytes of non-printable
application payloads are not base64-encoded in the UI; the text logger marks
those payloads as not rendered.

### APRS short messages and prepared audio

The message form is a callsign-to-callsign APRS radio message (not cellular
SMS and not an APRS-IS/internet gateway). A valid station callsign and SSID are
required. Incoming APRS messages, `ack` and `rej` responses are parsed with
their APRS addressee and optional 1–5 character message ID. The inbox filters
valid-FCS received packets to the exact configured callsign-SSID, and displays
only messages directed there. It is scoped to the current decoded capture/file
and is not a persistent store. A received `ack`/`rej` is shown as received
protocol text; it is **never correlated to a prepared/exported local WAV** and
does not change any sent/delivered state.

For composition, enter source callsign-SSID, destination callsign-SSID,
1–67 printable ASCII message characters, an optional 1–5 alphanumeric message
ID, and an optional explicit comma-separated digipeater path (maximum eight
valid callsigns). An empty path is allowed; no universal/default route is
inserted. The user must explicitly attest that the contents are lawful,
unencrypted amateur-radio text. This attestation is not content inspection,
encryption detection, a licensing check, or permission to transmit. The app
does not encrypt text and does not provide a field for creating encrypted RF
content.

Preparing forms an AX.25 UI frame with APRS destination identifier `APRS`,
PID `0xf0`, user-entered APRS addressee/message/message-ID, optional configured
digipeaters, computed X.25 FCS, HDLC flags/bit stuffing and NRZI. It then
generates continuous-phase Bell 202 1200/2200 Hz audio and a mono 8000 Hz
signed 16-bit PCM RIFF/WAVE file through the SAF picker. The WAV starts and
ends with silence and includes a fixed flag preamble/trailer. **The exported
audio is only prepared modulation—not a sent packet.** It is not played
automatically, is not connected to PTT, has no RF acknowledgement path, and
must not be played into a radio microphone or used to trigger voice-activated
PTT.

The separate radio-host screen now implements live APRS PCM delivery over the
documented authenticated BLE audio service, gated by local confirmation,
fresh host status, host arm/PTT and RF interlocks, credits, and a short PTT
lease. This is a software path to the host, **not verified RF send**; no
host-accepted frame is represented as transmitted, received, or delivered.
The SAF-exported WAV remains offline-only and is never automatically played or
sent. An external bench workflow is not integration or evidence of a working
RF path: if an appropriately licensed operator independently tests exported
audio, use the radio's documented auxiliary/data input through correctly
rated galvanic isolation and attenuation, a power-rated dummy load (not an
antenna), a permitted test frequency/mode, and a separately operated physical
PTT. Start at a safe low level, confirm the waveform and modulation at the
load using independent receive/measurement equipment, and release PTT
manually. Never connect speaker-level output directly, never route through
the microphone or voice-activated PTT, and do not treat WAV export as
authorization to transmit.

### Bounded processing and visible errors

Both live and imported audio pass through the same PCM normalizer and
demodulator. Accepted capture duration is strictly bounded to 240 seconds;
sample-rate, PCM format, WAV/RIFF chunk sizes, AX.25 frame length and decoder
cancellation are bounded. A requested mode is required for every processing
operation. Unsupported input, CRC/parity failures, absent frames/header,
missing image sync, invalid sample levels, stale/cancelled UI jobs and SAF
errors do not produce success-shaped fallback results. When the receive
screen is dismissed, the active recorder is stopped/released and decoding or
document I/O is cancelled.

These bounds limit ordinary memory and processing, but this prototype has not
undergone adversarial-parser or device-fuzz testing. It does not authenticate
the origin of received radio data; do not treat any decoded packet as trusted
commands or security evidence.

## Reproducible JVM verification

The all-Kotlin synthetic fixtures exercise end-to-end decoder behavior without
requiring an SDR, radio, RF transmission, or external decoder:

* Hilbert/phase-difference FM demodulation at 1200, 1500, 1900 and 2300 Hz.
* Synthetic full-length PD120 (`0x5f`) and PD180 (`0x60`) headers at both
  11025-Hz and 8000-Hz source PCM rates, VIS parity, all 248 separately
  sync-verified composite rows, Y/Cr/Cb/Y pixel assembly.
* Random PCM no-signal rejection, corrupted VIS parity and selected-mode
  mismatch rejection.
* WAV PCM ingest and malformed/compressed input rejection.
* AX.25 `123456789` X.25 CRC check `0x906e`, checked known APRS position frame
  with its independently computed little-endian FCS, AFSK tones, stuffing,
  NRZI, HDLC flags, parsed addresses, APRS position, and valid/invalid CRC and
  random-noise rejection.
* APRS message body/addressee/ID and ACK/rej parsing, callsign/path/message
  bounds, configured-station inbox filtering, and end-to-end composed UI frame
  → FCS → HDLC stuffing/NRZI → Bell 202 8000-Hz S16LE PCM → WAV → WAV ingest
  and resample → AX.25/APRS decode round-trip.
* PCM source/sink copying, 8000-Hz mono S16LE WAV ingest/export, exact sample
  preservation, and explicit sequence/sample-counter gap rejection.
* CM5 `cm5-rotor/v1` envelope and request-route validation for the seven
  remote actions exposed in Android, including strict target/track/passes
  payloads, explicit host errors, and rejection of local-console-only
  home/calibrate actions.

Run the tests, all Android JVM tests, lint and the application build from
`android` using the repository's isolated `.tools` JDK/SDK and Gradle caches:

```powershell
$env:JAVA_HOME = (Resolve-Path .tools\jdk\jdk-17.0.16+8).Path
$env:GRADLE_USER_HOME = (Resolve-Path .tools\gradle).Path
$env:ANDROID_HOME = (Resolve-Path .tools\sdk).Path
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat --no-daemon :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
```

Passing synthetic tests establish deterministic DSP/protocol fixture
behavior, **not** RF-receiver interoperability, an app launch/rendering
test, live audio routing on a specific handset, or reception from an
operational ISS/transmitter. Verify those on supported Android phones with the
specific, correctly routed receiver setup and reference recordings before
field use.

## Verified debug artifact

The build verified for this change is the debug APK below (signed with the
local Android debug key; it is not a release/distribution signing identity):

* `android/app/build/outputs/apk/debug/app-debug.apk`
* SHA-256: `ED52E0881353D7542DDA1FAC5062B372E2EA4BB8489710EDC98386ECF5A77DD7`.
* APK Signature Scheme v2 verification passed.
* Signer: local Android debug key, certificate SHA-256
  `c7ca5c0533cd3db2d189c5e3402042c1d2e565bde2f49264501190e17154ed7b`.
* Current verification: all 58 Android JVM tests passed with no failures or
  errors; `lintDebug` and `assembleDebug` passed. APK v2 signature verification
  passed. Lint reports 33 warnings and no errors, including untranslated orbit
  UI strings and draw-allocation warnings.

## Primary specification/reference trail

* Martin Emmerson, *Image Communication on Short Waves* (free English
  translation, including standard SSTV theory and the SSTV mode tables):
  [SSTV Handbook](https://www.sstv-handbook.com/).
* Martin Emmerson, *Image Communication on Short Waves*, contents and
  downloads (2019 edition):
  [author's download page](https://www.sstv-handbook.com/download/sstv-handbook.pdf).
* N7CXI-mode-derived, source-visible PD waveform parameters and scan-line
  layout (use for reproducible cross-implementation checks; not incorporated
  or copied as application code):
  [pdSSTV JS mode definitions](https://github.com/pefech/js-sstv/blob/3b2e296677420f6543021ca1a19e469174ab32de/src/sstv/modes.js).
* Independent Open Source SSTV receiver mode table (PD VIS codes, component
  duration, line geometry, 640 × 496 rows):
  [QSSTV, mode parameter table](https://github.com/ON4QZ/QSSTV/blob/8c27d6d169d8c6c197eb47b2089870e39bc06a02/src/sstv/sstvparam.cpp).
* TAPR, *AX.25 Amateur Packet-Radio Link-Layer Protocol, Version 2.2*,
  including HDLC flags, bit stuffing, address/control/information fields and
  FCS. The TAPR publication endpoint returned 404 during this task; the
  source is retained here for traceability:
  [TAPR AX.25 publications](https://www.tapr.org/published.html).
* APRS Working Group, *APRS Protocol Reference, Version 1.0.1*. Its original
  APRS.org PDF endpoint denied automated retrieval during this task; the
  reference is linked for human verification:
  [APRS101 specification](https://www.aprs.org/doc/APRS101.PDF).

Original decoder source was written in Kotlin for this app; the third-party
SSTV references informed only the interoperable format and timing facts. No
external decoder package or restricted/GPL implementation is embedded.
