# Testing: components, behaviour and bench

This section describes HOW to test every PortableSatStation component **before the PCBs are manufactured** and before the station is integrated: test bench, checklists, expected behaviour and pass criteria. It complements gates G0-G4 in [ACCEPTANCE.md](../ACCEPTANCE.md) and the record in [VALIDATION.md](../VALIDATION.md).

> **Status:** digital prototype, **not physically validated**. Nothing below has been measured yet: every test is PENDING until result, date and instrument are recorded. Criteria with a `Gn-m` reference come from ACCEPTANCE.md; the others are engineering values **proposed** by this review that must be confirmed or adjusted with the first prototype. Building or passing software tests does not validate wiring, mechanics or RF.

## How to use this section
1. Build the bench from [01-banco-de-pruebas.md](01-banco-de-pruebas.md) by levels (B0 → B4).
2. Run the checklists in order: electronics → PCB gate → mechanics → RF/radio → software/OS → Android app → system.
3. Record every result in [registro-pruebas.csv](registro-pruebas.csv) (one row per test) with date, Git revision, instruments and operator.
4. **Stop:** if a safety test fails (PWR, DRV-02/05, SNS-04, MEC-05) do not proceed to loaded motors or RF.
5. Do not order any PCB until the [pre-fabrication gate](03-puerta-pcb.md) is closed.

## Safety
Adult supervision, accessible emergency stop, current-limited supply, unloaded motors in early tests, eye protection when drilling/sanding, no transmitting without a licence, 50 Ω load (not an antenna) for every TX test, 12 V never on the CM5 header.

## Test map
| Document | Sections | Gate |
|---|---|---|
| [01-banco-de-pruebas.md](01-banco-de-pruebas.md) | Test bench design | — |
| [02-electronica.md](02-electronica.md) | Electronics: power, drivers and sensors (PWR, DRV, SNS) | G1E |
| [03-puerta-pcb.md](03-puerta-pcb.md) | Pre-fabrication gate for the PCBs (PCB) | G1E |
| [04-mecanica.md](04-mecanica.md) | Rotor mechanics (MEC) | G1 |
| [05-rf-y-radio.md](05-rf-y-radio.md) | Antenna, RF and SDR radio (ANT, RAD) | G2 / G4 |
| [06-software-y-os.md](06-software-y-os.md) | Software, CM5 hosts and OS image (SW) | G0 |
| [07-app-android.md](07-app-android.md) | Android app (APP) | G3 |
| [08-sistema.md](08-sistema.md) | System integration (G3 / G4) (SYS) | G3 / G4 |

Figures with the BricoHams logo and authors: T1 (bench), T2 (GPIO tester), T3 (mechanical fixture) in `fig/`.

Record: [registro-pruebas.csv](registro-pruebas.csv). Assembly: [assembly guide](../assembly/README.md). App help: `android/app/src/main/res/raw*/`.
