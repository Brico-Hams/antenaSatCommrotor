# Android control and TLE-transfer acceptance

These criteria are pending tests, not claims of implementation. The final BLE
contract must match the firmware that is actually built.

## Connection and authorization

1. On Android 12 or later, denial of scan/connect permissions must produce a
   warning, not infinite reconnection or a hidden exception. On earlier
   versions, check the system location requirements for BLE scanning.
2. Select the device explicitly. UUIDs and contract version must match; do not
   connect to the first device advertising a similar name.
3. Verify the pairing/encryption required by firmware and the locally
   configured control token; an incorrect token must not execute commands.
4. The token must not appear in logs, unencrypted preferences, error captures,
   or build files. Protect its key with Android Keystore.
5. Connecting, disconnecting, or restarting the app must not arm motors or
   restore homing.
6. Simultaneous Android and web clients must not bypass busy state/interlocks.

## Protocol and errors

1. Negotiate MTU and test the minimum too: fragment and reassemble messages
   according to the contract; do not assume a TLE fits in one write.
2. Request ID, length, sequence, lost fragment, and timeout errors must be
   clear and must not apply partial messages.
3. An unrecognized response or different version must not be presented as
   success.
4. Notifications and callbacks must not block the UI or safe rotor control.
5. The rotor must not perform heavy filesystem/SGP4 work inside a BLE callback;
   it must delegate to its documented safe mechanism.

## Calibration

1. Show separate states for homing, UTC/position, level, true north, and
   encoder zero when used. A stationary GNSS receiver does not give heading.
2. Finite values, ranges, and units must match firmware.
3. Reject calibration during movement/tracking and when prerequisites are
   incomplete; do not silently clamp to a valid value.
4. The user confirms physical verification. The app must not assume readings
   from unimplemented tilt/orientation sensors.
5. Moving the tripod or repeating homing invalidates the relevant state per
   policy.

## TLE over the phone's Internet connection

1. Use HTTPS from permitted sources; no insecure TLS or cleartext HTTP.
2. A network error preserves the last valid catalog and shows its age; a
   redownload must not make the TLE epoch appear newer.
3. Validate length, checksum, epoch, and catalog limits.
4. Transfer atomically: BLE interruption must not leave a truncated cache.
5. Update TLE only when the rotor is in a permitted state, without suspending
   the stop function.
6. Frequencies are not derived from TLE; configure the radio separately.

## Passes and autonomy

1. The app queries passes calculated by SGP4 on the ESP32; UTC must be
   unambiguous.
2. Select the same satellite in list/pass/tracking views without confusing
   indices after catalog updates; use the NORAD identifier.
3. Horizon, cable limits, acquisition, zenith, and speed: the rotor must
   explicitly reject impossible destinations.
4. If the app is closed during a pass, the rotor continues autonomously ONLY
   if data, sensors, and safety state remain valid.
5. The physical stop must work without phone, Bluetooth, or browser.

## Android delivery

Build the APK with pinned versions and retain its hash/commit. Parser/UI tests
are not equivalent to testing with a phone and rotor. Prepared GitHub Actions
does not imply a remote run or store distribution; protect the release
signing key outside the repository.
