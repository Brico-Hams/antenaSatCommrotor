# Software, CM5 hosts and OS image

Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.

## SW — Software, CM5 hosts and operating-system image

**Expected component behaviour.** All software is tested on a development computer before touching hardware. Building or passing tests does NOT validate wiring, mechanics or RF.

### SW-01
- [ ] **Action:** At the repository root run: node --test "tests/*.test.cjs"
- **Expected behaviour:** All tests pass (66 in the 2026-10-11 review).
- **Pass criterion:** 0 failures; any failure blocks the remaining gates.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SW-02
- [ ] **Action:** Run: PYTHONPATH=.:radio:rotor python3 -m pytest -q tests/rotor tests/radio_host
- **Expected behaviour:** Rotor controller and radio host tests.
- **Pass criterion:** 0 failures (86 passed in the review).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SW-03
- [ ] **Action:** Build and run the native control logic (tests/control_logic/test_native) with g++ and Unity; run node scripts/engineering-report.cjs.
- **Expected behaviour:** Limit/time/state logic and engineering calculations.
- **Pass criterion:** 6/6 native tests; the engineering report flags no failures.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SW-04
- [ ] **Action:** Compare SGP4 with an independent implementation (same TLE, UTC and site) at 10 instants of a pass.
- **Expected behaviour:** AZ/EL difference.
- **Pass criterion:** ≤ 0.1° away from zenith (G0-3); same conventions and geodesy.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SW-05
- [ ] **Action:** Feed bad data: truncated TLE, bad checksum, old epoch, HTML names, dead source, catalogue too large.
- **Expected behaviour:** Explicit failure in every case.
- **Pass criterion:** No motion and the valid cache is not corrupted (G0-7).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SW-06
- [ ] **Action:** Render all parts with OpenSCAD and check closed mesh, volume and absence of unexpected components (including the lids with the embossed logo).
- **Expected behaviour:** Watertight meshes.
- **Pass criterion:** All parts watertight; rendering does not replace review of meshing, clearances and assembly access (G0-5/6).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SW-07
- [ ] **Action:** Flash the BricoHams OS image (os/build-image.sh on Linux with Docker, or the build-os.yml workflow) to the card/eMMC and boot the CM5.
- **Expected behaviour:** BricoHams banner appears on the console and in /etc/issue; local login with bricohams / Brico123.
- **Pass criterion:** Change the password with passwd on first login; SSH disabled (port 22 closed: nmap/ss); no secrets, keys or Wi-Fi in the image. The image has NOT been built or booted so far.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### SW-08
- [ ] **Action:** On the CM5 run gpiodetect/gpioinfo and select the /dev/gpiochipN that exposes the frozen BCM offsets; start the profile selector (rotor-only, radio-only, integrated).
- **Expected behaviour:** Profile installed and /etc/bricohams/profile written only after success.
- **Pass criterion:** No module service starts by itself; the safe-state holder starts after the GPIO map check; a failed install leaves a pending marker.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

[Back to the index](README.md)
