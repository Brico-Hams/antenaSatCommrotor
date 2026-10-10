# CM5 Linux rotor and tracking host

## Scope and verification boundary

This is the new autonomous Linux rotor subsystem for the Raspberry Pi Compute
Module 5 (CM5). The CM5 is the station's single computer; the selected LimeSDR
Mini is a separate radio device hosted by the radio service. The legacy ESP32
firmware and its BLE protocol remain unchanged. The rotor service is an
independent module that the authenticated Linux Bluetooth/radio host may call;
it does not own the radio, Android app, firmware, or carrier design.

The software is not a safety certification. A CM5/Linux process, a software
fault bit, or a successful SPI write cannot replace the normally-off hardware
motor-power cutoff, six independent normally-closed (NC) axis limits, an
external emergency stop, or an independent hardware watchdog. Those circuits
and their wiring must be frozen and verified on the selected carrier before
any motor motion or RF transmit approval.

The implementation must fail closed when any required feedback is absent,
invalid, stale, uncalibrated, or inconsistent. There is no production
simulated-driver fallback. Simulation belongs only in explicitly named unit
test fixtures.

## Public control hook

The rotor Python package is independent of the radio package and does not
import SDR, PA, Bluetooth, or audio components. Install it as a standalone
package with `python -m pip install .` from `rotor/`, using its isolated
Python environment; run `portable-sat-rotor --config
/etc/bricohams/rotor.json` or `python -m rotor`. Its local
JSON-lines interface accepts one `{"operation": "...", "data": {}}` request
per input line and emits the controller's explicit `{ok, data, error}` reply.
`--local-console` is a local process privilege choice, not a request field;
it must never be enabled by a remote BLE/API adapter.

Both the CLI and radio host require the CM5 platform BSP to register one
Python entry point named `cm5` in the `portable_sat_rotor.hardware` group.
That provider receives the explicit controller-configuration path and must
return a real `RotorController` composed with real sensors, drivers, and the
normally-off power gate. The adapter starts the controller's 50 ms service
loop. There is no built-in simulated or guessed hardware composition. The
revision-A software pin map is frozen in `hardware/cm5/interface.json`, but
the AUX NC/E-stop/watchdog/power-gate safety circuits are routed in the digital review
(hardware/cm5/DESIGN-REVIEW.md) but not qualified, fabricated or released and the compass/IMU BSP is not selected. Until those are verified and
a production BSP provider is installed, startup fails explicitly; this
package is installable without radio software, but physical operation is not
yet commissioned.

The transport adapter owns authentication, request IDs, and the outer radio
host response envelope. It passes only a validated operation and JSON object
to the rotor controller:

```python
RotorController.handle_control(
    operation: str,
    data: Mapping[str, object],
    *,
    local_console: bool = False,
) -> Mapping[str, object]
```

`local_console` is set by the trusted host adapter, never copied from a remote
JSON field. The hook returns `{"ok": bool, "data": object|null,
"error": string|null}` for the radio adapter to place in its normal
request-ID/path envelope. Invalid or unauthorized requests are explicit
errors; they do not return a success-shaped default. The controller is not
permitted to arm, home, or calibrate from BLE. The radio host should poll
`status.data.verifiedHealthy` and `status.data.fault`, not accept a
client-supplied rotor-health value.

Supported operations:

| Operation | Request data | Safety and response contract |
| --- | --- | --- |
| `status` | `{}` | Current machine state, fault, commissioning/verification state, axis positions/targets/limits/encoder age, and sensor validity/age. Missing or invalid readings are `null` with a false validity flag, never zero-filled. |
| `sensorsstatus` | `{}` | Raw validated GNSS, encoder, compass, and IMU readbacks with timestamps/ages and calibration provenance. |
| `home` | `{"confirm":"HOME CM5 ROTOR"}` | Local-console only. Starts a bounded worker, one axis at a time, toward its configured NC switch; timeout is at most 120 seconds per axis. Stops on the switch, timeout, feedback loss, or any fault. Does not persist a one-edge base or claim true AZ. |
| `calibrate` | Explicit surveyed `encoderZeroDeg`, `azBaseTrueDeg`, base-level roll/pitch, declination/source/date, compass hard-/soft-iron and orientation matrices, POL model/source/offset, `carrierVerified:true`, and exact confirmation `CALIBRATE AND ARM CM5 ROTOR` | Local-console only, only while stopped and physically secured. Requires a frozen `mechanics_verified` configuration, fresh sensor/encoder readbacks, and a verified live compass/IMU BSP. `headingMode:"manual"` is rejected; manual heading is unsupported until that BSP is verified. `carrierVerified` is only a local attestation and cannot substitute for released safety circuitry and validated physical return readbacks. Calibration is RAM-only and must be repeated after reboot. |
| `goto` | Absolute `{"azDeg":number,"elDeg":number,"polDeg":number}` | Rejects non-finite/out-of-range values, stale feedback, unhomed axes, active directional limits, or an uncommissioned carrier. All three axis bounds and per-output microstep ratios come from the frozen mechanical configuration. |
| `track` | `{"noradId":integer}` | Requires a current validated TLE, fresh GNSS UTC/site, true-heading calibration, and all motion interlocks. Publishes actual SGP4 subpoint/azimuth/elevation/range/range-rate plus commanded axis angles and timestamps. The locally commissioned `apparent-track` or `cross-track` POL geometry and offset are explicit mechanical conventions, not evidence of a satellite transmitter antenna's polarization; verify each satellite's real polarization separately. |
| `stop` | `{}` | Immediate software stop request and driver ramp-to-stop; cancels active homing and invalidates all home references. Hardware E-stop/watchdog remain the independent safety path. |
| `catalog` | Optional bounded query | Returns actual validated cached satellite records and TLE epochs only. |
| `passes` | Optional `noradId`, bounded interval/count | Bounded prediction job; returns actual predicted rise/culmination/set UTC and geometry. It must not block the motor-service loop. |

The adapter may expose the operations as `/rotor/status`,
`/rotor/sensorsstatus`, `/rotor/home`, `/rotor/calibrate`, `/rotor/goto`,
`/rotor/track`, `/rotor/stop`, `/satellites/catalog`, and `/satellites/passes`
in the host's existing `path`/`op` envelope. Do not create a second
unauthenticated BLE service or allow a remote caller to assert a local-console
principal.

The local-only adapter interface used by an in-host Bluetooth/radio frontend
is `rotor.radio_adapter.open_adapter(controller_config_path)`, returning an
object with `snapshot()`, `dispatch(path, operation, data, peer)`,
`disconnect(peer)`, and `close()`. `snapshot()` returns the rotor-host
`cm5-rotor/v1` safety/tracking object: `sampledMonotonic`,
`hardwareCommissioned`, `gnssValid`, `gnssSampledMonotonic`, `sgp4Valid`,
`trackingSampledMonotonic`, `fault`, `utc` (Unix seconds from the actual
GNSS-backed propagated state), `site` (`[latitudeDeg, longitudeDeg,
altitudeM]`), `rangeRateMps`, and the full `status` object. Invalid data is
`null`/false and includes a fault, never fabricated as a valid zero.

The radio host should poll `snapshot()` every 200 ms or faster so it meets
its present snapshot-age bound; it must use `trackingSampledMonotonic` as
tracking-input receipt time, not the later poll time. The rotor GNSS source
expires after 10 seconds. SGP4 updates every 500 ms; the bridge rejects its
sample once older than 1 second. The host separately refreshes rotor safety
at least every 500 ms. The host must not report verified healthy or valid
Doppler/tracking when any field is absent, stale, uncommissioned, or faulted.
The standalone local CLI is independent of this frontend and of radio/SDR/PA
dependencies; loss of a phone or radio process does not stop a running rotor
tracking session.

Status includes `state`, `fault`, `verifiedHealthy`, `commissioned`,
`calibrated`, `updatedMonotonic`, `axes`, `sensors`, and `satellite`.
Each axis contains `positionDeg`, `targetDeg`, `homed`, `encoderValid`,
`encoderAgeMs`, `minimumLimitClosed`, and `maximumLimitClosed`. Satellite
values include `noradId`, `name`, `utc`, `latitudeDeg`, `longitudeDeg`,
`altitudeKm`, `azimuthDeg`, `elevationDeg`, `rangeM`, `rangeRateMps`,
`apparentTrackAngleDeg`, `siteUtc`, and `gnssAgeMs`. Invalid/unavailable
values remain `null` with a false validity field; they are never replaced by
zero.

Sensor status also exposes `motorPermitHealthy`, `driverFaultsClear`,
`interlockAgeMs`, and `interlocksValid`. A fresh validated motor-permit return, E-stop/watchdog readbacks, and all
three revision-A active-low driver-fault inputs (BCM24-26) are required for
commissioning and motion. The fault GPIOs must only be reported clear after
the BSP has validated their physical input circuits and observed the inactive
HIGH level. Missing, stale, faulted, or unvalidated returns block both. The
MCP23017 feedback polarity is conditional on its physical circuit definition;
a GPIO request or software translation is not evidence that the independent
permit chain is released.

### Rotor health forwarded to shared PTT safety

The trusted local adapter must refresh the radio host's
`Safety.rotor_update(fault, verified=True)` no less often than every 500 ms.
`verified=True` is permitted only when the complete commissioned hardware
chain is present and fresh: controller/driver readbacks, all three encoder
channels, all six NC limits, external E-stop/watchdog health, required GNSS
and attitude inputs, valid calibration, and no active/following-error fault.
Otherwise it must report an unverified/faulted rotor state. Unknown, stale,
unverified, or faulty rotor state inhibits shared physical PTT. BLE clients
cannot report rotor health or clear a rotor fault.

Faults latch. Recovery requires the cause to be gone, valid fresh readbacks,
the prescribed local inspection/reset, and a new explicit local arm action.
Linux thread cleanup and an SPI stop command are best-effort software actions;
they are not substitutes for the independent electrical cutoff.

## Axis, feedback, and motion requirements

The selected driver modules are three Watterott SilentStepStick TMC5160 v1.5
boards. [Watterott's v1.5 pin guide](https://learn.watterott.com/silentstepstick/pinconfig/tmc5160/)
states EN is active-low (VIO/high disables the motor outputs), SPI requires
`SPI_MODE=VIO`, internal motion-controller mode requires the SD_MODE jumper
opened so its v1.5 pulldown selects SD_MODE=GND, and grounding CLK selects the
internal clock. DCO is a dcStep output, not a sleep input.

The software pin assignments are frozen at revision A in
[`hardware/cm5/interface.json`](../../hardware/cm5/interface.json) and
[`CM5-PCB.md`](CM5-PCB.md): SPI1 MISO/MOSI/SCLK use BCM19/20/21 and
CS2/CS1/CS0 use BCM16/17/18 for POL/EL/AZ respectively. I2C1 is BCM2/3;
the TCA9548A is at 0x70, with encoder channels 0/1/2, compass channel 3, and
IMU channel 4. GNSS uses UART0 BCM14/15 and optional PPS BCM27. NC limits use
BCM4-9, E-stop monitor BCM10, watchdog heartbeat BCM11, motor-arm request
BCM12, mux reset BCM13, and driver diagnostics BCM24-26. The MCP23017 at 0x20
provides axis-enable requests on GPA0-2 and feedback/fault readbacks on
GPA3-7.

The runtime axis binding follows the JSON contract: AZ opens SPI1 chip select
0 (`/dev/spidev1.0`, BCM18), EL chip select 1 (`/dev/spidev1.1`, BCM17), and
POL chip select 2 (`/dev/spidev1.2`, BCM16), using
`LinuxSpidevTransport.for_cm5_axis()`. Those device-node names still require
the target CM5 device-tree overlay to expose and verify the frozen SPI1
mapping; software constants do not verify the live platform.

Polarity is taken from the `gpio` entries in `interface.json`: all six NC
limit inputs (BCM4-9) and the E-stop monitor (BCM10) are healthy LOW; the
limits' open-wire level is HIGH. Driver fault inputs `FAULT_AZ_N`,
`FAULT_EL_N`, and `FAULT_POL_N` on BCM24/25/26 are active LOW (HIGH is the
inactive electrical level, not independent proof of driver health). MCP23017
GPA3-7 are feedback/fault signals whose LOW meaning is conditional on their
exact circuits being defined. Do not infer motor permit, PTT feedback, or PA
health from an expander read alone.

These assignments define software signals only. The NC hard-limit stop
circuits, external watchdog, physical E-stop power interruption, driver-enable
gating, and expander/fail-off circuits remain design/release blockers. GPIO
requests, monitor inputs, and successful SPI transactions are not hardware
permits. **Do not move motors** until the separate direct hardware limit path,
watchdog, E-stop, and normally-off enable chain have been designed, built,
released, and their physical permit/feedback return paths have been validated.
Until then `hardwareCommissioned`/`verifiedHealthy` must remain false; inhibit
all motor motion and all PTT/transmit. The revision-A contract identifies the
hardware as routed digital review, not fabricated and not commissioned, so a local calibration
confirmation cannot commission it. Measure/qualify the driver's actual internal clock before
configuring its ramp formulas; do not substitute a nominal oscillator
frequency.

The mechanical ratios remain configuration inputs until the mechanics agent
freezes them. Current working figures are explicitly provisional: AZ and EL
25:1 with a 200-full-step motor at 16 microsteps (80,000 motor microsteps per
output revolution), and POL 5:1 (16,000 microsteps/revolution) with candidate
physical hard-stop travel of +/-90 degrees. POL uses a proposed
20:100 single belt stage; its initial software bounds are +/-80 degrees and
its two NC switch trip targets are +/-85 degrees, before the candidate stops.
For the illustrative 200-step motor at 16 microsteps, POL is 16,000 commanded
microsteps/output revolution (0.0225 degrees per command increment, not
accuracy). These are documentation alignment values, not a frozen or
validated motion configuration. Do not enable an axis until measured ratio,
switch actuation, stop clearance/strength, full cable service-loop sweep,
payload balance, and encoder feedback have passed first-article verification.

The mechanical report's example antenna-only CG and inertia values are not
whole-axis ratings. Reweigh the POL stage and payload, measure the assembled
center of gravity and axis inertia, then recalculate added EL/AZ gravity and
inertial loads including the POL motor/frame, harness, and moving structure.
Do not infer motor torque adequacy or field load capability from the example;
the selected motor dynamic torque curve and physical load tests remain
required.

Linux GPIO must never generate step pulses. A TMC5160 v1.5 may execute
the ramp internally using position-mode `RAMPMODE`, `XTARGET`, `VMAX`,
`AMAX`, and `DMAX`. No velocity conversion or ramp register may be treated as
verified until checked against the selected chip datasheet and its clock,
microstep, and board configuration. The SPI adapter must use the chip's
5-byte frames and documented pipelined read semantics, validate returned
register/status values, deassert chip select correctly, and surface bus faults.
A successful syscall/write alone is not a driver-ready response. The exact
carrier, board pinout, SPI mode/clock, enable polarity, power-good, and driver
fault wiring are still hardware-selection/bench-verification items.

There are three independent output encoders and six NC limits (minimum and
maximum on AZ, EL, and POL). Motion is prohibited if any encoder is missing,
stale, magnet-invalid, outside plausible range, or inconsistent with driver
position. A limit input is healthy only when its NC circuit is verified closed;
open circuit, loss of input, or contradictory state is a fault. Directional
limit checks stop motion before the hard stop. During motion, an asserted
minimum/maximum switch is accepted only if the target is in the direction away
from that switch; a switch active toward the commanded target immediately
faults and stops the rotor. No axis is moved after a fault merely to attempt
recovery.

The proposed encoder implementation uses one AS5600 at I2C address `0x36` per
axis, selected through a TCA9548A channel (proposed channels 0, 1, and 2).
The TCA9548A's channel-select behavior and the AS5600 magnet-status/raw-angle
register interpretation must be verified against their primary datasheets and
the selected carrier. Every sample records the selected channel, monotonic
read time, raw angle, and MD/MH/ML status. Require magnet detected (MD=1) and
neither field-too-strong nor field-too-weak (MH=0, ML=0); reject stale or
invalid readings. No encoder absence or sensor-bus error is converted into a
plausible angle.

Three AS5600 encoder modules are selected, on mux channels 0/1/2 at 0x36.
Compass channel 3 and IMU channel 4 are reserved by the revision-A software
interface, but their components, circuits, and BSP have not been selected.
The compass and IMU hardware selection is not frozen. Until exact primary
datasheets, carrier wiring, axis orientation, sample validity checks, and
calibration procedure are recorded, only an injected `SensorInputs` boundary
with validated timestamped readbacks is allowed; it is not a production
hardware driver. Tilt compensation uses measured accelerometer inclination.
True heading requires a live compass/IMU BSP, assembled-system
hard-/soft-iron calibration, and an explicit, bounded declination with
source/date provenance. Manual heading calibration is rejected until the
selected compass/IMU BSP is verified. Missing declination is not zero and
GNSS coordinates alone do not provide heading.

The requested AZ/EL slew limit is 2.25 degrees/second. POL's proposed
1 degree/second remains provisional until the mechanical configuration is
frozen. Motion is driven by a monotonic-time service with a single owner for
each hardware bus/driver, bounded command queue, deadline monitoring, and
following-error checks. Any Python worker exception, missed service deadline,
driver fault, sensor timeout, or power-gate enable/disable error faults the
system and attempts disable/stop; electrical protection must independently
stop power if software does not run.

Homing is finite (maximum two minutes per axis), operates only under the
commissioned local procedure, and uses only that axis's NC minimum input. It
must stop immediately on timeout, failed switch transition, loss of encoder,
unexpected maximum-switch state, driver error, E-stop, or watchdog fault.
Homing establishes only a session-local mechanical reference; it does not
persist a one-edge base, infer geographic north, or replace calibration.

## GNSS, SGP4, and satellite outputs

GNSS parsing uses actual NMEA sentences with checksum validation and valid
receiver fix status. UTC and site are accepted only from a coherent fix and
are invalidated after ten seconds without a fresh valid update. A missing,
invalid, or stale fix never falls back to `(0, 0)`, a host wall clock, or a
synthetic epoch.

Satellite positions use the pinned `sgp4` Python distribution, based on
Vallado's SGP4/SDP4 implementation, with a known Vallado test vector in unit
tests. TLE line numbers, fixed-width fields, checksums, NORAD identity, epoch,
and propagated-state error are validated. TLE replacement is atomic; the
cache is bounded (48 KiB and 100 NORAD IDs). Unsupported or expired element
sets are not silently refreshed or replaced by fabricated data.

SGP4 TEME position and velocity are transformed consistently to the
Earth-fixed/local topocentric frame. Range rate is computed from relative
position and relative velocity (including the site's Earth-rotation velocity),
not by finite-differencing two separately sampled positions. A finite,
validated result is timestamped with the exact GNSS UTC used. Acquisition is
not requested below 15 degrees elevation. The 89-degree zenith guard avoids
the azimuth singularity; crossing it or an unreachable/cable-wrap target must
be handled as a bounded safe stop/replan, never as a command to spin through
an axis limit.

Pass prediction is a bounded background job, runs only while idle or with
proven service headroom, and yields to motor servicing. The normal motor and
fault-monitor loops must not wait for network/TLE downloads or pass
calculations. `catalog`, `passes`, `track`, and status outputs expose only
actual validated satellite IDs, names, UTC, coordinates, angles, range rate,
and freshness. Android may display those actual values; it must not present a
placeholder target as live tracking.

## Dependencies and validation

Keep the rotor's Python dependency manifest separate from `radio/`. Pin the
SGP4 package version exactly and record its upstream license/notice; do not
vendor the library. Hardware access libraries are selected only with the
frozen Linux carrier and installed in a project-local environment or by the
Linux distribution package manager as appropriate. Do not install Python
packages globally.

Unit tests use strictly named simulated driver/sensor fixtures and exercise
the controller and fault transitions without physical motion. Required tests
include NMEA checksums and freshness; Vallado SGP4 position/velocity and
topocentric range-rate vectors; TLE validation/cache bounds; encoder magnet
status/age; every NC/E-stop/watchdog/driver fault; bounds and provisional
speed limits; homing timeout; explicit local-only commissioning; thread
failure and stop behavior; API success/error shape; and radio-host rotor
health freshness/inhibit integration.

Software tests cannot verify the carrier, motor current/thermal limits,
mechanical load, stop wiring, watchdog independence, encoder alignment,
compass magnetic interference, GNSS installation, radio/PTT behavior, or
CM5 timing under load. These remain explicit commissioning and field-test
blockers. Linux is not a hard real-time operating system.
