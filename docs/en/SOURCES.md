# Sources, traceability, and permissions

Research date: **10 October 2026**. Public research and local reading; the
user's PDFs and their text were not sent to external services. Conclusions
apply to the new PortableSatStation design and are not certification of the
cited projects.

## Licenses for the new project: user's express choice

The user's choice is **MIT** for original PortableSatStation software and
**CERN-OHL-S-2.0** for original hardware. License texts and project-scope
`NOTICE` determine the covered files. This choice **does not change
third-party licenses**: an SGP4 library, documentation, or external part
retains its own notices/license, which must be compatible with the intended
distribution. No remote publication has been made.

The references analyzed here are not redistributed as original assets: no
unknown-license sources, complete PDFs, commercial models, third-party
Gerbers, or GPL code are incorporated and then relabeled MIT. If external
material is added later, record its origin, revision, license, and changes in
`NOTICE`, and comply with its obligations before distribution.

### Selected SGP4 dependency: license checked

`firmware/platformio.ini` pins **Hopperpop/Sgp4-Library** to commit
**`7c82d31f9d9a286acde5ef55da8308fc93d2ba96`**:

- The controller review also checked the downloaded copy: library **1.0.3**,
  same commit and MIT license, no GPL markers in inspected source. This local
  check agrees with public research; it does not replace inventorying the
  firmware's other licenses.
- Source/revision:
  <https://github.com/Hopperpop/Sgp4-Library/tree/7c82d31f9d9a286acde5ef55da8308fc93d2ba96>.
- `LICENSE` directly consulted:
  <https://github.com/Hopperpop/Sgp4-Library/blob/7c82d31f9d9a286acde5ef55da8308fc93d2ba96/LICENSE>;
  blob **`853b46db127831eb9f8e8a7a8576e41c98619be4`**.
- Root license is **MIT**, not GPL. Its copyright line literally says
  “Copyright (c) 2016” with no named holder; preserve the original notice and
  do not invent an author. README credits original code to David Vallado and
  coordinate transformations to Grady Hillhouse under MIT. Preserve
  applicable headers/notices in included sources before distribution.
- MIT obligation: include copyright and permission text in copies or
  substantial portions; do not attribute that library to PortableSatStation's
  author. The checked permissive root license by itself does not require
  publishing all firmware under GPL.
- This **does not make the entire ESP32 binary original MIT software**:
  framework, libraries, and other components retain their licenses and
  obligations. Inventory them separately in `NOTICE`/controller documents.
- If the library is replaced by GPL implementation, reassess compatibility
  and meet GPL requirements for distributed linked firmware; do not silently
  label that combined work MIT. The user's license choice covers only
  original files.

## User's local evidence

**All six extracted texts were read** from locally supplied originals,
including tables and figure captions. Extracted texts are not distributed
in this repository; the table retains their hashes to identify the evidence
without depending on a private working directory.

| ID | Text file / document | Pages with content | SHA-256 of extracted text |
|---|---|---:|---|
| P1 | `SatelliteStationPart1.txt` — Gordon Gibby KX4Z, Part I: Introduction | 4 | `A46CFC72ECFD08243613A93B90E2598879992DFD2EF3500FD76B4882A15C9A8E` |
| P2 | `PartIIRotatorcontrol.txt` — Part II: Inexpensive Manual/Computer-Controlled Rotator Controller | 7 | `156B3CEE7E1C81DF888FAF061CD30D488805EFB4B926963C3BACC7E87EF5C289` |
| P3 | `PartIIIDualAxisRotator.txt` — Part III: Inexpensive Antenna Rotator | 5 | `69AEE5DB54D4E4A44DDA4205037845909FAFB65865FD9A963587DE47E80852D7` |
| P4 | `PartIVCrossPolarizedYagis.txt` — Part IV: Cross-Polarized Yagi's, July 2025 | 13 | `066817AAF5DB4880E3181403E83813943BC78B72B1CCED625FA71E85CC100E9C` |
| PC | `RotatorControllerPCBInstructionManual.txt` — Computer Robotic Antenna Rotator Controller Construction Manual | 10 | `0DF0812407B627CAF765D3D807EE579564D3582EF6A088456167D7E3B99831DC` |
| PT | `SatelliteTargets.txt` — SATELLITES table | 2 | `3166F7BD85882550A639DDB8BE329A9D59649A1133C45FA34A1468FE54D03D63` |
| A | `TDS_AV2040.txt` — Ultralife, AV 2040 UHF Satellite Communication (SATCOM) Antenna | 1 | `0F2937B350CDA2DD364B91E16E611C22865F9538D568B47898CC1B56CD66BCD2` |

**Page convention:** PC has printed page numbers 1-10, cited as “printed
page.” The other texts have no verifiable printed page numbers; “PDF p.”
means ordinal page reconstructed from form-feed page breaks in the extraction,
starting at 1. These ordinals are not presented as invented printed page
numbers. A final empty page break is not another content page. Images are not
reconstructed from text; only their captions are textual evidence. Consult
the original image to resolve an ambiguous graphical dimension.

Web pages in the series identified by the author:

- P1: <https://www.nf4rc.club/how-to-docs/satellite-system-part-i-overview/>
- P2: <https://www.nf4rc.club/how-to-docs/satellite-system-part-ii-rotator-control-board/>
- P3: <https://www.nf4rc.club/how-to-docs/satellite-system-part-iii-antenna-dual-axis-rotator-system/>

No permissive license was verified for the six PDFs. This project provides
critical synthesis and references; it **does not include complete PDFs,
figures, extensive tables, or schematics** from them. An article linking a
Gerber does not make all its content open hardware.

### A — New TDS_AV2040 datasheet: locally verified visual reading

New local original: `C:\Users\anatol.lopez\Downloads\TDS_AV2040.pdf`
(83,737 bytes); text extracted locally by the coordinator and reviewed
2026-10-10. One-page datasheet, readable title AV2040 and Ultralife brand/URL.
No readable printed page number.

**The extraction has defective font encoding:** words such as “Right Hand
Circular” appear shifted as “5LJKW +DQG &LUFXODU”, and numerical values
disappear. This limitation was resolved by reading **the locally rendered
140-dpi image**: `pdf-text\TDS_AV2040-000001.png`. Values below come from
visual reading of PDF page 1, **not from guessing the encoding**.

The **Ultralife / Trivec-Avant** datasheet, dated **23 NOV 2010**, document
**UBI-05273, REV:-**, states: 240-400 MHz band; 1.5:1 VSWR; right-hand
circular; AV2040-3 +7.0 dBic 240-400 MHz, AV2040-2 +11.0 dBic 240-318 MHz,
AV2040-1 +9.0 dBic 240-400 MHz; 200 Watts CW; 3 dB axial ratio; 6.5 pounds;
male BNC; black finish; AV2040-3 NSN 5985-01-149-2576. These are **published
commercial-product specifications**, not new-design performance or tests
performed here.

**Both 145 MHz and 435 MHz are outside 240-400 MHz.** This page has no
dimensional length, width, or deployed/folded volume. Description confirms
“foldable, manpack” and the photo shows a bag/structure, but provides no
measurements or permission to copy. Pixels are not measured as dimensions.

Attempts to retrieve the public datasheet via old Ultralife `/ECommerce/`
routes returned 404; the current manufacturer's homepage was reachable but
does not substantiate AV2040 specifications. The original PDF viewer returned
403 because the folder was untrusted; the **local image was later read
successfully**. Neither PDF nor assets were sent to external services.
Manufacturer footer says the data are for reference only, not a performance
warranty, and subject to change.

External OBJ/STL accompanying the reference have no license confirmed in
this research: **they are not redistributed or incorporated as original
hardware**. The commercial datasheet also does not authorize reproducing its
geometry. The coordinator handles geometric metadata and permissions
separately.

**Geometry metadata supplied by coordinator, local read-only inspection:**
`tinker.obj`, 10,416 vertices, 20,964 faces, 1 object, SHA-256
**`e231ba603e352d31570a9db748208d7c32dd5116dec796b633858a7191910a00`**;
binary STL, 20,964 triangles, SHA-256
**`f40f044336ad46a0434f8fc512e112d51cf68c6c80ddca6992bfc786a474b71a`**.
Both have envelope **194 x 115.798 x 33 in unspecified units**. Do not call
these millimetres without unit evidence. The envelope describes mesh/part
layout, **not assembled or folded antenna dimensions**.

No copyright/license declaration was found in inspected OBJ/MTL headers;
absence of a notice **does not mean public domain or permission to derive**.
The coordinator's local inspector returns metadata and does not redistribute
the mesh. This analysis does not import the mesh into new CAD or make
derivatives.

## Public repositories consulted

### D — User's diplexer

<https://github.com/anatolbricoham/DuplexorSpaceQuad>

- Requested branch: `main`.
- Commit consulted: **`f5c7dc375ed7b9882f52bd7757deaf44cd422b81`**, 2026-09-30.
- Files read: `README.md`, `LICENSE`, `docs/MONTAJE.md`, `docs/PRUEBAS.md`,
  `BOM/BOM_SMA.csv`, `BOM/BOM_BNC.csv`.
- Stable link:
  <https://github.com/anatolbricoham/DuplexorSpaceQuad/tree/f5c7dc375ed7b9882f52bd7757deaf44cd422b81>.
- License: MIT, copyright 2026 anatolbricoham. Covered material may be
  adapted/redistributed while retaining copyright and license; check rights
  for any external material. This project records values/interfaces but does
  not copy circuit/CAD.
- **There is no lowercase `bom/` in this revision:** lists are in `BOM/`.
  A `bom/` query failed and was corrected to the actual directory.
- README S-parameters are from **ideal simulation**, whereas PRUEBAS defines
  pending criteria. No physical-unit measurement results were found in files read.

### L — User's LibreSat

<https://github.com/anatolbricoham/libresat-rotator-HAM>

- Requested branch: `master`.
- Commit: **`a23fe016108cf6d1209eb15140df74d0469e5e38`**, 2026-10-01.
- Files read: `README.md`, `LICENSE`, `docs/MECHANICAL.md`,
  `docs/SIZING.md`.
- Stable link:
  <https://github.com/anatolbricoham/libresat-rotator-HAM/tree/a23fe016108cf6d1209eb15140df74d0469e5e38>.
- Hardware: **CERN-OHL-S-2.0**, strongly reciprocal. Firmware/software:
  **GPL-3.0-or-later**. Documentation/images: **CC BY-SA 4.0**. These
  external licenses remain unchanged even though new-project original
  software is MIT. A software derivative may not simply be declared MIT
  without meeting GPL obligations. Check actual directories and file scope
  before reuse.
- README acknowledges **v1.0 has not yet been built and measured as a complete
  assembly**. Its tests/simulations do not certify fabrication, torque,
  autonomy, or physical safety.
- PortableSatStation adopts general requirements/ideas as references; its new
  NEMA14 + 25:1 planetary mechanics and autonomous controller are designed
  separately, without transferring its parts or figures as though they
  belonged to this rotor.

### O0 — OpenGD77 guide explicitly requested

<https://github.com/open-ham/OpenGD77/blob/b843c1f050ebcfdb7aea7fad9182af13bc5ef3e6/docs/OpenGD77_User_Guide.md>

- Repository commit: **`b843c1f050ebcfdb7aea7fad9182af13bc5ef3e6`**,
  2022-05-19.
- Full text examined for satellite references. VFO frequency section explains
  different TX/RX and **cross-band/split**. It does not include Satellite
  Screen or identify RT-3S in the title.
- This historical revision is **insufficient** to substantiate current RT-3S
  satellite features.

### O1 — Maintained guide complementing O0

<https://github.com/LibreDMR/OpenGD77_UserGuide>

- Pinned commit: **`2289ba75afebd044b85d38f03b6e279defe3645d`**, 2026-03-10.
- Text:
  <https://github.com/LibreDMR/OpenGD77_UserGuide/blob/2289ba75afebd044b85d38f03b6e279defe3645d/OpenGD77_User_Guide.md>.
- Sections read: model header, Satellite Screen, Polar view, Satellite
  individual predictions, Satellite live data, Squelch and Power, Sat
  (Satellite follow mode), and date/location references.
- Its README says the guide was separated from the old repository for license
  reasons and remains GPL 2. Only the English version is maintained.
- This guide names **MD-UV380 (RT-3S)** and documents integrated Doppler. The
  guide revision does not identify the radio user's installed firmware:
  record build, CPS, and a backup before use.
- <https://www.opengd77.com> reports interactive forum closure due to bot
  traffic and points to static archive <https://www.opengd77.com/archive/index.html>.
  Do not assume old routes remain available; `/downloads/MDUV380/Firmware/`
  returned 404.

### H — Hybrid boards

<https://github.com/SatcomRadio/Hybrid_Couplers/blob/master/README.md>

Public README read 2026-10-10. It presents circular-polarization boards,
not a 145/435 MHz diplexer. Claims CMX03A03 200 W, “RF Power” 200 W,
Anaren 10260-3 250 W, and QCN3 15 W, **without specifying operating band**.
These are README claims, not accredited tests. No applicable Gerber license
was verified; they are not incorporated into this project.

**Checked link error:** “QCN3 / SMA version” points to `GERBER-CmxSma.zip`,
not a QCN3 Gerber. Do not order that PCB assuming it is the QCN3 design.

### M — Manufacturers and availability

- Mini-Circuits **QCN-3+**:
  <https://www.minicircuits.com/WebStore/dashboard.html?model=QCN-3%2B>
  explicitly states “LTCC 90° Hybrid, **220-470 MHz**, 50 Ω.” Consulted
  2026-10-10. Includes 435 MHz, excludes 145 MHz. Do not confuse it with the
  README's no-suffix name.
- Linked datasheet: <https://www.minicircuits.com/pdfs/QCN-3+.pdf>. Response
  was binary PDF, not a readable extraction of limit table; **no specific
  power, phase, or isolation figures are attributed to that sheet**.
- No readable manufacturer datasheet obtained for **CMX03A03** or
  **Anaren 10260-3**. Anaren queries failed through transport/DNS/TLS and the
  TTM index returned 403; a tentative CMX route did not resolve.
  DigiKey/Coilcraft returned 403 on routes queried. No bands or current/Q/SRF
  limits are invented. Exact identification and original datasheets are
  purchase prerequisites.

## Visual antenna references

- **B — Blog**, April 2020 archive:
  <https://blog.tomasbrincil.cz/?m=202004>. Explanation and three formulas
  read; describes a **449.550 MHz** design inspired by AV-2040. No explicit
  STL/OBJ license verified. Access to linked files is not permission to
  derive from them.
- **T — Thingiverse 5904442**:
  <https://www.thingiverse.com/thing:5904442>. Only title **“AV-2040 MilSat
  Antenna by German_Panda”** was accessible. Details, dimensions, files, and
  license were unavailable in this query; no geometry/RF validation is claimed.
- **C — Cults screenshot supplied to the project**: stated terms
  **commercial / private use / NoAI**. Screenshot is not a derivative-work
  license. Commercial pieces are not traced, reproduced, or adapted from it,
  and those files are not submitted for generative analysis. No assets are
  included without a complete verifiable listing/license.

## Evidence still needed to close the design

1. Exact NEMA14 motor part number, shaft, supplier hole dimensions; torque/
   backlash/efficiency and resistance of new 25:1 planetary stage through
   fabrication and test.
2. Actual diplexer enclosure, connector, and cable dimensions; published flange/
   front dimensions are estimates.
3. VNA for antennas and assembled network, polarization/axial ratio, and
   power test of the actual unit.
4. Manufacturer datasheets for hybrid candidates in both bands. High power
   without a band specification is insufficient.
5. Exact RT-3S firmware/CPS and local Satellite-screen test. The user's radio
   and any CAT protocol have not been tested.
6. Current satellite ephemeris/status: historical lists are examples, never
   authorization to transmit.
