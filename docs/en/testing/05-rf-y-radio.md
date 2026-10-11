# Antenna, RF and SDR radio

Each test is a checkbox: tick it only with the measurement, date and instrument recorded in the register.

## ANT — Antenna and passive RF (VNA, hybrid, diplexer)

**Expected component behaviour.** With rotor and coax in real position, SWR ≤ 1.5 at the centre frequency and ≤ 2 on operating channels. A good SWR does NOT prove circular polarisation or gain: measure or simulate the assembly.

### ANT-01
- [ ] **Action:** Calibrate the VNA (OPEN, SHORT, LOAD, THRU) at the connector plane, with no radio connected.
- **Expected behaviour:** Verification with a 50 Ω load: SWR ≈ 1.0.
- **Pass criterion:** Valid calibration before every measurement series (G2-1).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### ANT-02
- [ ] **Action:** Measure each dipole/reflector per band (VHF 145 MHz, UHF 435 MHz) with the assembly deployed, coax and rotor in real positions.
- **Expected behaviour:** SWR curve and minimum frequency.
- **Pass criterion:** SWR ≤ 1.5 at centre and ≤ 2 on channels; document the bandwidth without extrapolating (G2-3).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### ANT-03
- [ ] **Action:** Measure the hybrid per band: amplitude and phase between outputs with the other port terminated at 50 Ω.
- **Expected behaviour:** Imbalance and phase.
- **Pass criterion:** Imbalance ≤ 0.5 dB and phase 90° ± 5° at the chosen frequencies (G2-4); suitable isolated load.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### ANT-04
- [ ] **Action:** Measure the 2 m/70 cm diplexer: insertion loss per branch, return loss and isolation between branches.
- **Expected behaviour:** S21, S11 and cross S21.
- **Pass criterion:** Loss ≤ 1 dB per branch, return ≥ 14 dB and isolation ≥ 40 dB as a screening (G2-5); 40 dB does not guarantee no desensitisation with TX.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### ANT-05
- [ ] **Action:** Repeat SWR after 50 fold/unfold cycles and check RF contact continuity.
- **Expected behaviour:** SWR and continuity without drift.
- **Pass criterion:** SWR variation < 0.1 and stable continuity; plastic hinges are not the only RF contact (G2-7).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### ANT-06
- [ ] **Action:** Measure or simulate pattern, RHCP/LHCP sense and axial ratio with the complete assembly (antenna + coax + rotor).
- **Expected behaviour:** Axial ratio towards the satellite.
- **Pass criterion:** Axial ratio ≤ 3 dB to claim circular polarisation (G2-6); without this data only linear/crossed is claimed.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### ANT-07
- [ ] **Action:** With a receiver and a generator (or SDR as source), measure the minimum detectable level with rotor and converters off and on.
- **Expected behaviour:** Noise floor with and without motors.
- **Pass criterion:** Difference documented; the noise rise with active motors must be acceptable for the target signal (G3-6).
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

## RAD — SDR radio (2 × LimeSDR Mini + CM5) and audio

**Expected component behaviour.** The radio works in receive without the rotor, with two SDRs identified by serial number (VHF and UHF). TX stays inhibited: it is enabled only with the physical permit, watchdog and lease after qualification with a load.

### RAD-01
- [ ] **Action:** Connect both LimeSDRs over USB and check discovery; note the two serial numbers and the VHF/UHF assignment.
- **Expected behaviour:** Two distinct devices recognised.
- **Pass criterion:** Never "the first USB found": explicit selection by serial number.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### RAD-02
- [ ] **Action:** Request rates and frequencies and read them back from the hardware; open two concurrent RX streams (VHF and UHF).
- **Expected behaviour:** Values read back from hardware.
- **Pass criterion:** A requested rate is not a verified rate: record the read-back; no sample drops in 10 min.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### RAD-03
- [ ] **Action:** Feed a reference tone/FM and verify demodulation on VHF and UHF; test DSP first with WAV/vectors, then real reception.
- **Expected behaviour:** Correct demodulated audio.
- **Pass criterion:** SNR and distortion recorded; SSTV/APRS tones from the two receivers are not mixed.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### RAD-04
- [ ] **Action:** Test the Bluetooth PCM audio transport (S16LE, mono, 8000 samples/s): credits, drops and reconnect.
- **Expected behaviour:** Continuous stream with no gaps.
- **Pass criterion:** No underruns in 10 min; the active VHF/UHF channel is selected explicitly; the transport does not imply HFP/A2DP.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### RAD-05
- [ ] **Action:** With no physical TX permit, try PTT from the host/app and from GPIO (PTT_VHF_REQUEST BCM22, PTT_UHF_REQUEST BCM23).
- **Expected behaviour:** PTT refused; isolated outputs open (inhibited); PTT feedback consistent.
- **Pass criterion:** No TX possible without permit, watchdog and lease; test with a 50 Ω load, never an antenna.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

### RAD-06
- [ ] **Action:** Only with licence and authorisation: qualify TX at minimum power into a load: spectrum, harmonics (145×3 = 435 MHz), blocking and temperature.
- **Expected behaviour:** Clean spectrum and stable temperature.
- **Pass criterion:** Harmonics and spurs within limits; only one TX active; G4 only after G1-G3 are approved.
- _Measured result ____ · Date ____ · Instrument ____ · Status: PENDING_

[Back to the index](README.md)
