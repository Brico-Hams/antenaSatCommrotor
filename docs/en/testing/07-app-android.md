# Android app

Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.

## APP — Android app (branding, help, TLE download and BLE sync)

**Expected component behaviour.** The app downloads TLEs over HTTPS from CelesTrak, AMSAT or PE0SAT and stores them in a validated private cache; only the controller computes orbits. Transfer to the Raspberry/rotor is local BLE, with a 60 s stall detector, and the last valid cache is never overwritten on failure.

### APP-01
- [ ] **Action:** Install the debug APK (GitHub Actions android.yml) on an Android 8-11 phone and an Android 12+ phone; open the app.
- **Expected behaviour:** The BricoHams logo, the authors line (Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina) and bricohams.org appear; the launcher icon is the BH logo.
- **Pass criterion:** Logo visible on all three screens (main, digital receiver, radio host) and in Help; no clipping in dark/light mode.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-02
- [ ] **Action:** Tap Help on each screen with the phone in Spanish, English and Hungarian.
- **Expected behaviour:** The help text for that screen opens in the phone language (es, en or hu); with no network.
- **Pass criterion:** Help legible and error-free; button names quoted match the interface (the interface is es/en; Hungarian quotes both).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-03
- [ ] **Action:** With Internet, try the three providers (CelesTrak, AMSAT, PE0SAT) one by one with Download TLE.
- **Expected behaviour:** Progress in bytes and a "download complete" message; catalogue in the local list.
- **Pass criterion:** Entries > 0 with recent epoch from at least one provider; record which of the three (CelesTrak, AMSAT, PE0SAT) answers from your network and which do not.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-04
- [ ] **Action:** Repeat the CelesTrak download several times in a row, then in airplane mode.
- **Expected behaviour:** After several downloads in a row CelesTrak may answer 403/429; in airplane mode it fails on network.
- **Pass criterion:** Specific usage-limit message (wait a few hours/other provider) or failed-download message; the last valid cache is kept; no misleading "TLE invalid: tle_http_…".
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-05
- [ ] **Action:** Import a valid local TLE file, then one with a bad checksum, a truncated one and one with trailing blanks on lines.
- **Expected behaviour:** Valid and trailing-blank files import; bad/truncated give an explicit error.
- **Pass criterion:** The cache changes only after validation and atomic replacement; errors show the reason.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-06
- [ ] **Action:** Download a catalogue with more than 100 satellites.
- **Expected behaviour:** A subset (maximum 100) must be chosen.
- **Pass criterion:** With 101 ticked the dialog refuses; with ≤ 100 it saves.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-07
- [ ] **Action:** Scan rotors (15 s), explicitly select the rotor, confirm the passkey and save the encrypted token.
- **Expected behaviour:** Authenticated connection with versions verified.
- **Pass criterion:** "Authenticated and versions verified" message; connecting does NOT enable motors. If it fails with error 133 the app retries up to 2 times before reporting.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-08
- [ ] **Action:** With valid UTC and READY/DISARMED mode, tap Transfer catalogue; watch progress in bytes until "transfer complete".
- **Expected behaviour:** The TLEs reach the controller (Raspberry/CM5); the host shows the updated catalogue in the same order.
- **Pass criterion:** Total time recorded (≈ 512 characters per chunk over 20-byte frames); catalogue hash matches in app and host; no offset errors.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-09
- [ ] **Action:** During the transfer power off the rotor or move the phone away; wait 60 s with no progress.
- **Expected behaviour:** The transfer is cancelled and disconnected with a timeout message; the previous catalogue on the controller is untouched.
- **Pass criterion:** The host's previous catalogue is not altered (atomic transfer with commit); retry works after reconnecting.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-10
- [ ] **Action:** Choose a satellite from the controller catalogue and query passes; compare AOS/LOS with an independent reference (same station and TLE).
- **Expected behaviour:** Consistent passes; the controller computes, not the phone.
- **Pass criterion:** AOS/LOS difference < 30 s; pass-query limit reported to the user if the calculation does not finish.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### APP-11
- [ ] **Action:** Digital receiver: play an SSTV WAV and an APRS 1200-baud WAV through speaker/cable to the phone audio input.
- **Expected behaviour:** SSTV image and AX.25 packets decoded; log can be saved.
- **Pass criterion:** Correct decoding with reasonable audio level; no TX from the app.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

[Back to the index](README.md)
