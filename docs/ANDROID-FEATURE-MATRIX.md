# Android FIRSTVERSION feature matrix

This is an original, bounded native implementation inspired by selected capabilities,
**not full Look4Sat feature parity**. Nothing here asserts live tracking, verified RF
output, decoder parity, or physical antenna operation. The orbit view initially reads
“NOT LIVE — host integration pending”; no demonstration orbit is substituted.

| Requested feature | Implemented in this delivery | Integration pending / physical verification |
| --- | --- | --- |
| Catalogue, filters, favorites | Native catalogue rows; name/NORAD filters; favorites-only view; device-private SharedPreferences keyed by real NORAD ID | Host must supply actual NORAD IDs and translate selection into its own slot identifiers. Existing rotor catalogue slot `id` is **not** NORAD identity. No catalogue downloader added here. |
| Passes | Bounded host-supplied AOS/peak/LOS Unix-second UTC list; maximum elevation and partial-pass label | Rotor remains owner of SGP4/pass prediction. Activity must feed valid observer-specific predictions. Field validation does not establish orbital accuracy. |
| Map | Original offline equirectangular geographic graticule, observer point, actual supplied satellite subpoint and timestamped ground track; date-line jumps not drawn across world | Schematic global coordinate diagram, **not country cartography/street mapping**. No downloaded map assets, tile server, user-location upload, or phone-side propagation. No points means no orbit displayed. |
| AZ/EL radar | North-up visible-sky plot of actual supplied trajectory/tracking samples, below-horizon exclusion, center=zenith/horizon=outer ring | Feed observer-specific host samples; field alignment, acquisition and antenna pointing physically untested. |
| AOS alerts | Explicit per-satellite opt-in, private receiver, immutable PendingIntent, notification channel, visible Android 13+ permission button/status, **inexact** AlarmManager scheduling | Apply manifest entries below; Activity requests runtime permission only on explicit tap. Host refresh/disconnect callbacks must be wired. No exact-alarm permission, WorkManager dependency, guaranteed alarm/Doze claim, background networking or reboot restore. After reboot/app force-stop, reconnect/resume for recalculation/rescheduling. |
| Frequencies / Doppler | Explicit supplied nominal UL/DL Hz, requested corrected Hz, adapter-acknowledged Hz, mode/support flag, unknown values retained as unknown | No radio model/frequency invented; no Doppler calculation here. Radio owner must provide real profile/support and RF acknowledgement semantics. Software ACK is not measured RF. Hardware/over-air verification pending. |
| Three axes | Separate measured vs host-requested AZ/EL/POL display, bounded numeric request form, optional host callback, measured POL radar marker | Mechanical POL angle is **not** an RHCP/LHCP switch. Marker is a schematic orientation reference, not a measured electromagnetic polarization field. Callback must route through existing authenticated/calibrated/safety-gated control session; no direct actuator endpoint is added here. Hardware motion/calibration untested. |
| SSTV PD120 / PD180 | Orbit layer deliberately does not own or duplicate decoder implementation | DSP owner owns existing native decoder, receive UI and evidence. Integration/real audio testing must be recorded by that owner; no Robot36-parity claim. |
| APRS | Orbit layer deliberately does not own or duplicate AX.25/APRS receive implementation | DSP owner owns existing receive decoder and tests. Radio/over-air and audio interface verification pending. |

## Activity integration contract

All hooks are in `org.bricohams.portablesatstation.orbit`. The parent/DSP owner, not this
delivery, changes MainActivity, resources, Gradle or the manifest.

```kotlin
val overview = SatelliteOverviewView(activity)
overview.onSatelliteSelected = { noradId: Int -> /* translate actual NORAD ID into host selection */ }
overview.onAxesRequested = { target: ThreeAxisState -> /* existing safety-gated control session */ }
overview.onNotificationPermissionRequested = {
    // API >= 33: Activity.requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), requestCode)
}
// UI thread; use only authenticated/validated actual host state:
overview.submitSnapshot(snapshot: OrbitSnapshot?)
// Disconnect, host error, unavailable identity or incompatible model:
overview.submitSnapshot(null)
// onResume and after the notification permission result:
overview.refreshAlertPermission()
```

The comments above are integration placeholders, **not working transport code**.
Before entering the form, obtain actual host state. Do not populate sample frequencies
or copy local form values into measured axes/RF acknowledgement. Profile support is an
explicit host/adapter assertion, not inferred from the mode name.

`OrbitSnapshot` copies/bounds collection inputs and exposes read-only lists:
100 catalogue entries, 720 ground-track points, 100 passes, 360 radar points, 32 profiles.
Scalar nested models are immutable. It checks finite angle/Hz ranges, positive
Unix-second UTC (through 2100), chronological track ordering, distinct NORAD IDs and
selected identity. Pass/radar samples require an observer. Freshness requires a
connected source and current UTC between `generatedUtc` and `validUntilUtc`.
Old supplied data remains labelled stale/offline, never live.

### Proposed adapter JSON (NOT a frozen host API or endpoint)

`OrbitSnapshotJson.parse(JSONObject)` requires all keys below; unavailable objects
and frequencies must be **explicit JSON null**, arrays must be explicit arrays.
No `optDouble` fallback, invented subpoint, guessed Kepler elements, success
endpoint or conversion of rotor slot ID into NORAD ID is permitted.

* Root: `schemaVersion: 1`, integer `generatedUtc`, `validUntilUtc`, boolean
  `sourceConnected`, nullable integer `selectedNoradId`.
* `catalogue`: `{noradId, name}`.
* Nullable `observer`: `{name, latitude, longitude, altitudeMeters}`.
* Nullable `subpoint` and `groundTrack` entries: `{utc, latitude, longitude}`.
* `passes`: `{aosUtc, peakUtc, losUtc, maxElevation, partial}`.
* Nullable `tracking` and `radarTrack` entries: `{utc, azimuth, elevation}`.
* Nullable `measuredAxes` / `requestedAxes`: `{azimuth, elevation, pol}` in degrees.
* `radioProfiles`: `{name, mode, supported, uplinkHz, downlinkHz,
  requestedUplinkHz, requestedDownlinkHz, acknowledgedUplinkHz,
  acknowledgedDownlinkHz}`; all six frequency fields nullable integer Hz.

An Activity can construct immutable models directly instead of using this proposed
JSON. Only use a field after the actual host contract supplies it with the correct
identity, time, observer and units. Legacy `PassData.aos/peak/los` may be adapted as
Unix seconds, but does not by itself supply observer/NORAD/subpoint/groundtrack/RF
state. Empty/unknown values are preferable to fabricated state.

## Exact manifest integration requirements

Under `<manifest>` (alongside existing permissions):

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

Inside `<application>`:

```xml
<receiver
    android:name=".orbit.PassAlertReceiver"
    android:enabled="true"
    android:exported="false" />
```

No Gradle changes/dependencies, exact alarm permissions, intent filters or boot
receiver are requested. Receiver registration is checked before reporting a schedule.
Permission/channel denial visibly cancels scheduled notifications. AOS changes
cancel/replace the matching NORAD alarm. Past/partial/unavailable passes are not
scheduled. Host selection changes and explicit disconnect clear obsolete scheduled
alerts while preserving opt-ins. Receive-time checks suppress revoked opt-ins,
replaced AOS predictions and alerts delayed more than 15 minutes.

## Original implementation and upstream license boundaries

Official sources verified for feature inspiration, not downloaded/copied source:

* Look4Sat: <https://github.com/rt-bishop/Look4Sat>;
  license <https://github.com/rt-bishop/Look4Sat/blob/main/LICENSE> is **GPL-3.0**.
  Its source/resources/map assets are not incorporated into this original layer.
  MIT licensing of original project code does not relicense GPL upstream work:
  importing GPL code would require a separate distribution/licensing review.
* Robot36: <https://github.com/xdsopl/robot36>;
  <https://github.com/xdsopl/robot36/blob/2af2390954aa248725042ba6b1332bbcca68c357/LICENSE>
  is Ahmet Inan's permissive use/copy/modify/distribute grant with warranty disclaimer
  (2024). It is **not labelled MIT or GPL by that LICENSE**. No decoder code/assets
  were copied here. Cite that actual text rather than assuming a license from a
  repository name or an earlier version.

No tile, country-outline, logo, screenshot, waveform or other copyrighted map/UI
asset is bundled by the orbit implementation. Coordinate grid and native controls
are authored here.

## Validation and limits

Standalone Kotlin 2.0.21 compilation against the existing Android SDK 35 plus JUnit
4.13.2 succeeded for all orbit source files and **10 orbit tests**. This avoided
concurrent Gradle/build-output writes. Tests live in `tests/android/orbit` and are
already included by the existing Android test source mapping. Owning build runner
may execute:

```text
:app:testDebugUnitTest --tests "*.OrbitModelsTest" --tests "*.OrbitSnapshotJsonTest"
```

Tests cover copied immutable lists, limits, chronology, strict schema/null/type/ID
handling, real coordinate projection, north/east radar geometry, freshness,
past/partial/millisecond AOS rejection, NORAD filters, unknown RF fields and POL
bounds. Android runtime permission dialogs, SharedPreferences persistence,
AlarmManager/notification delivery, drawing/accessibility/device layouts, host
integration, SGP4 accuracy and physical RF/rotor operation remain unverified on
device. Permission and alarm claims require device testing, not JVM proof.
