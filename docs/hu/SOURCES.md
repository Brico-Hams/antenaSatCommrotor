# Források, nyomon követhetőség és licencek

Lekérdezés dátuma: **2026. október 10.** Nyilvános kutatás és helyi
olvasás; a felhasználó PDF-jeit/szövegeit nem küldtük külső szolgáltatásba.
Az alábbi következtetések az új PortableSatStation-tervre vonatkoznak,
nem a hivatkozott projektek tanúsításai.

## Az új projekt licencei – a felhasználó kifejezett választása

A PortableSatStation **eredeti szoftvere MIT**, **eredeti hardvere
CERN-OHL-S-2.0** licencű, a felhasználó választása szerint. A licencszövegek
és a `NOTICE` hatóköze határozza meg, mely fájlokra vonatkoznak. Ez a
választás **nem módosítja a harmadik felek licenceit**: az SGP4-könyvtár,
dokumentáció vagy külső alkatrész saját közleménye/licence megmarad, és
terjesztés előtt kompatibilisnek kell lennie a tervezett kiadással.
Távoli közzététel nem történt.

Az itt vizsgált referenciákat nem terjesztjük eredeti assetként: ismeretlen
licencű forrást, teljes PDF-et, kereskedelmi modellt, idegen Gerbert vagy
GPL-kódot nem építünk be, majd címkézünk át MIT-re. Későbbi külső anyag
beépítésekor forrást, revíziót, licencet és módosítást kell a `NOTICE`
fájlban rögzíteni, majd terjesztés előtt teljesíteni kell a kötelezettségeket.

### Kiválasztott SGP4-függőség: ellenőrzött licenc

A `firmware/platformio.ini` a **Hopperpop/Sgp4-Library** könyvtárat a
**`7c82d31f9d9a286acde5ef55da8308fc93d2ba96`** commiton rögzíti:

- A vezérlőfejlesztő a letöltött másolatot is ellenőrizte: **1.0.3**
  könyvtár, azonos commit, MIT-licenc, az átvizsgált forrásokban GPL-
   jelölés nélkül. Ez egyezik a nyilvános ellenőrzéssel, de nem helyettesíti
  az egész firmware licencleltárát.
- Forrás/revízió:
  <https://github.com/Hopperpop/Sgp4-Library/tree/7c82d31f9d9a286acde5ef55da8308fc93d2ba96>.
- Közvetlenül megtekintett `LICENSE`:
  <https://github.com/Hopperpop/Sgp4-Library/blob/7c82d31f9d9a286acde5ef55da8308fc93d2ba96/LICENSE>;
  blob **`853b46db127831eb9f8e8a7a8576e41c98619be4`**.
- A gyökérlicenc **MIT**, nem GPL. A copyright-sor pontosan
  „Copyright (c) 2016”, megnevezett jogosult nélkül; az eredeti közleményt
  kell megőrizni, szerzőt nem szabad kitalálni. A README David Vallado
  eredeti kódját és Grady Hillhouse MIT-licencű transzformációit nevezi meg.
  Terjesztés előtt a beépített források vonatkozó fejléceit/közleményeit
  szintén őrizze meg.
- MIT-kötelezettség: a copyright- és engedélyszöveget a másolatokban vagy
  lényegi részekben szerepeltetni kell; a könyvtárat ne tulajdonítsa a
  PortableSatStation szerzőjének. Az ellenőrzött permisszív gyökérlicenc
  önmagában nem írja elő a teljes firmware GPL alatti közzétételét.
- **Ettől a teljes ESP32-bináris nem lesz eredeti MIT-szoftver**:
  a framework, könyvtárak és egyéb összetevők licence/kötelezettsége
  megmarad. A `NOTICE`-nak és vezérlődokumentációnak ezeket külön kell
  leltároznia.
- GPL-implementációra váltáskor újra kell vizsgálni az összeférhetőséget,
  és a terjesztett, linkelt firmware-nél a GPL-t teljesíteni kell; a teljes
  készletet nem szabad csendben MIT-nek címkézni. A felhasználó választása
  csak az eredeti fájlokra érvényes.

## A felhasználó helyi bizonyítékai

Az eredetik helye: `C:\Users\anatol.lopez\Downloads`; a hat kivont szöveg
**teljes egészében** át lett olvasva a táblákkal és ábrafeliratokkal együtt.
Szövegek:
`C:\Users\anatol.lopez\.copilot\session-state\93e9ed63-2da0-4d79-90a4-39add6c2b259\files\pdf-text`.

| ID | Szövegfájl / dokumentum | Tartalmas oldalak | Kivont szöveg SHA-256 |
|---|---|---:|---|
| P1 | `SatelliteStationPart1.txt` — Gordon Gibby KX4Z, Part I: Introduction | 4 | `A46CFC72ECFD08243613A93B90E2598879992DFD2EF3500FD76B4882A15C9A8E` |
| P2 | `PartIIRotatorcontrol.txt` — Part II: Inexpensive Manual/Computer-Controlled Rotator Controller | 7 | `156B3CEE7E1C81DF888FAF061CD30D488805EFB4B926963C3BACC7E87EF5C289` |
| P3 | `PartIIIDualAxisRotator.txt` — Part III: Inexpensive Antenna Rotator | 5 | `69AEE5DB54D4E4A44DDA4205037845909FAFB65865FD9A963587DE47E80852D7` |
| P4 | `PartIVCrossPolarizedYagis.txt` — Part IV: Cross-Polarized Yagi’s, 2025. július | 13 | `066817AAF5DB4880E3181403E83813943BC78B72B1CCED625FA71E85CC100E9C` |
| PC | `RotatorControllerPCBInstructionManual.txt` — Computer Robotic Antenna Rotator Controller Construction Manual | 10 | `0DF0812407B627CAF765D3D807EE579564D3582EF6A088456167D7E3B99831DC` |
| PT | `SatelliteTargets.txt` — SATELLITES táblázat | 2 | `3166F7BD85882550A639DDB8BE329A9D59649A1133C45FA34A1468FE54D03D63` |
| A | `TDS_AV2040.txt` — Ultralife, AV 2040 UHF Satellite Communication (SATCOM) Antenna | 1 | `0F2937B350CDA2DD364B91E16B611C22865F9538D568B47898CC1B56CD66BCD2` |

**Oldalszámozási konvenció:** PC a kézikönyv nyomtatott 1–10. oldalát
tartalmazza, hivatkozásuk „nyomtatott o.”. A többi szövegben nincs
ellenőrizhető nyomtatott oldalszám: „PDF-o.” a kinyert `form feed`
oldaltöréseiből visszaállított sorszám, 1-től. Ezeket nem tüntetjük fel
kitalált nyomtatott számként. Az üres záró oldaltörés nem külön tartalmas oldal.
A képeket a szöveg nem rekonstruálja; csak a képfelirat szolgál szöveges
bizonyítékként. Kétértelmű grafikus mérethez az eredeti képet kell megnézni.

A sorozat szerző által azonosított oldalai:

- P1: <https://www.nf4rc.club/how-to-docs/satellite-system-part-i-overview/>
- P2: <https://www.nf4rc.club/how-to-docs/satellite-system-part-ii-rotator-control-board/>
- P3: <https://www.nf4rc.club/how-to-docs/satellite-system-part-iii-antenna-dual-axis-rotator-system/>

A hat PDF-re permisszív licencet nem ellenőriztünk. Kritikai összefoglalást
és hivatkozást adunk; **teljes PDF, ábra, kiterjedt táblázat vagy rajz nem
kerül az új projektfájlokba**. Az, hogy egy cikk Gerberre mutat, nem teszi
automatikusan nyílt hardverré a teljes cikket.

### A — Új TDS_AV2040 adatlap: helyben, vizuálisan ellenőrizve

Új helyi eredeti: `C:\Users\anatol.lopez\Downloads\TDS_AV2040.pdf`
(83737 bájt); a koordinátor helyben vonta ki a szöveget, ellenőrzés:
2026-10-10. Egyoldalas adatlap, jól olvasható AV2040 címmel, Ultralife
névvel/URL-lel. Olvasható nyomtatott oldalszám nincs.

**A betűkódolás hibás:** például a „Right Hand Circular” szóalak
„5LJKW +DQG &LUFXODU”-ként eltolódik, a számértékek eltűnnek.
A korlátot a koordinátor helyileg, 140dpi-n raszterizált
`pdf-text\TDS_AV2040-000001.png` képpel oldotta meg. Az alábbi számok
az 1. PDF-oldal vizuális olvasatából valók, **nem a kódolás találgatásából**.

Az **Ultralife / Trivec-Avant** adatlap kelte **2010. NOV. 23.**, dokumentum
**UBI-05273, REV:-**. Közölt értékek: 240–400MHz sáv; VSWR 1,5:1; jobb
körpolarizáció; AV2040-3: +7,0dBic 240–400MHz; AV2040-2: +11,0dBic
240–318MHz; AV2040-1: +9,0dBic 240–400MHz; 200WattsCW; 3dB tengelyarány;
6,5 font; BNC male; fekete kivitel; AV2040-3 NSN 5985-01-149-2576.
Ezek **kereskedelmi termék közölt specifikációi**, nem az új terv teljesítménye
és nem itt végzett mérések.

**145MHz és 435MHz egyaránt kívül esik a 240–400MHz sávon.** Az adatlap nem
ad nyitott/összecsukott hossz-, szélesség- vagy térfogatméretet. A leírás
„foldable, manpack” antennát mond, a fotón táska/szerkezet látható, de sem
méretet, sem másolási engedélyt nem ad. Képpontokat nem alakítunk méretté.

Az Ultralife régi `/ECommerce/` útvonalain próbált nyilvános adatlap-keresés
404-et adott; a gyártó mai főoldala elérhető, de nem igazolja az AV2040
specifikációit. Az eredeti PDF-megjelenítő nem megbízható mappa miatt 403-at
adott; a **helyi képet** később sikerült elolvasni. A PDF-et/assetet nem
küldtük külső szolgáltatásba. A gyártó lábjegyzete szerint az adatok
tájékoztató jellegűek, nem teljesítménygaranciák és változhatnak.

A hivatkozás mellett kapott külső OBJ/STL licence e kutatásban nem igazolt:
**nem terjesztjük, nem építjük be eredeti hardverként**. A kereskedelmi
adatlap sem ad engedélyt geometria reprodukálására. A kereskedelmi licencek
és a fordítás/másolat jogi hatályának részletes korlátait az eredeti
jogszövegek határozzák meg; ezek a magyar összefoglalók nem helyettesítik azokat.

## Nyilvános referenciaprojektek és eszközök

### D — A felhasználó diplexere

<https://github.com/anatolbricoham/DuplexorSpaceQuad>

- Kért ág: `main`.
- Vizsgált commit: **`f5c7dc375ed7b9882f52bd7757deaf44cd422b81`**,
  2026-09-30.
- Olvasott fájlok: `README.md`, `LICENSE`, `docs/MONTAJE.md`,
  `docs/PRUEBAS.md`, `BOM/BOM_SMA.csv`, `BOM/BOM_BNC.csv`.
- Rögzített hivatkozás:
  <https://github.com/anatolbricoham/DuplexorSpaceQuad/tree/f5c7dc375ed7b9882f52bd7757deaf44cd422b81>.
- Licenc: MIT, copyright 2026 anatolbricoham. A hatálya alá tartozó
  anyag adaptálását és terjesztését a szerzői jogi és licencértesítés
  megőrzésével engedi; a külső anyagok jogait külön kell ellenőrizni.
  Itt értékeket és interfészeket dokumentálunk, az áramkört/CAD-et nem
  másoljuk.
- Ebben a revízióban **nincs kisbetűs `bom/` könyvtár**: a listák a
  `BOM/` alatt találhatók. A `bom/` lekérdezése sikertelen volt; a
  tényleges könyvtárra javítottuk.
- A README S-paraméterei **ideális szimulációból** származnak, míg a
  PRUEBAS függőben lévő elfogadási feltételeket határoz meg. Az olvasott
  fájlokban nem találtunk fizikai példányon végzett mérés eredményeit.

### LibreSat rotor (L)

<https://github.com/anatolbricoham/libresat-rotator-HAM>

- Kért ág: `master`.
- Commit: **`a23fe016108cf6d1209eb15140df74d0469e5e38`**, 2026-10-01.
- Átolvasott fájlok: `README.md`, `LICENSE`, `docs/MECHANICAL.md`,
  `docs/SIZING.md`.
- Stabil hivatkozás:
  <https://github.com/anatolbricoham/libresat-rotator-HAM/tree/a23fe016108cf6d1209eb15140df74d0469e5e38>.
- Hardver: **CERN-OHL-S-2.0**, erősen kölcsönös. Firmware/szoftver:
  **GPL-3.0-or-later**. Dokumentáció/képek: **CC BY-SA 4.0**. Ezek a külső
  licencek érintetlenek maradnak, még ha az új projekt eredeti szoftvere MIT
  is. A LibreSat szoftveréből származó mű nem nevezhető egyszerűen MIT-nek a
  GPL-kötelezettségek teljesítése nélkül. Újrahasználat előtt ellenőrizze a
  tényleges könyvtárat és fájlonkénti hatókört.
- A README elismeri, hogy a **v1.0 nincs még teljes rendszerként megépítve
  és megmérve**. Tesztjei/szimulációi nem tanúsítanak gyártást, nyomatékot,
  autonómiát vagy fizikai biztonságot.
- A PortableSatStation általános követelményeket/ötleteket vesz át
  referenciaként; az új NEMA14 + 25:1 bolygómű mechanikája és autonóm
  vezérlője külön terv, annak alkatrészeit/számait nem ruházza át.

### O0 — Kifejezetten kért OpenGD77 útmutató

<https://github.com/open-ham/OpenGD77/blob/b843c1f050ebcfdb7aea7fad9182af13bc5ef3e6/docs/OpenGD77_User_Guide.md>

- Tárolócommit: **`b843c1f050ebcfdb7aea7fad9182af13bc5ef3e6`**, 2022-05-19.
- A műholdas utalásokat keresve teljes szövegét megvizsgáltuk. A VFO-
  frekvenciafejezet eltérő TX/RX frekvenciát és **cross-band/split** módot
  magyaráz. Nincs Satellite Screen fejezet, és a cím nem azonosít RT-3S-t.
- Ez a történeti revízió **önmagában nem igazolja az RT-3S aktuális
  műholdfunkcióit**.

### O1 — Karbantartott útmutató, O0 kiegészítése

<https://github.com/LibreDMR/OpenGD77_UserGuide>

- Rögzített commit: **`2289ba75afebd044b85d38f03b6e279defe3645d`**,
  2026-03-10.
- Szöveg:
  <https://github.com/LibreDMR/OpenGD77_UserGuide/blob/2289ba75afebd044b85d38f03b6e279defe3645d/OpenGD77_User_Guide.md>.
- Átolvasott fejezetek: modellfejléc, Satellite Screen, Polar view,
  Satellite individual predictions, Satellite live data, Squelch and Power,
  Sat (Satellite follow mode), dátum-/helyhivatkozások.
- A tároló README-je szerint licencokokból vált külön a régi tárolótól,
  és GPL 2 hatálya alatt marad; csak az angol verziót tartják karban.
- Az útmutató megnevezi az **MD-UV380 (RT-3S)** modellt, és integrált
  Dopplert ír le. Az adott útmutató-revízió nem azonosítja automatikusan a
  felhasználó rádiójába telepített firmware-t: használat előtt rögzítse a
  buildet, CPS-t és mentést.
- A <https://www.opengd77.com> közli az interaktív fórum botforgalom miatti
  bezárását, és a statikus archívumot ajánlja:
  <https://www.opengd77.com/archive/index.html>. A régi útvonalak elérhetőségét
  nem feltételezzük; `/downloads/MDUV380/Firmware/` 404-et adott.

### H — Hibridpanelek

<https://github.com/SatcomRadio/Hybrid_Couplers/blob/master/README.md>

A nyilvános README olvasása 2026-10-10-én. Körpolarizációs paneleket mutat,
nem 145/435MHz-es diplexert. CMX03A03 200W, „RF Power” 200W, Anaren 10260-3
250W és QCN3 15W állítás szerepel benne, **munkasáv megadása nélkül**.
Ezek a README állításai, nem igazolt mérések. A Gerberlicencet nem
ellenőriztük; fájlokat nem építünk be.

**Ellenőrzött linkhiba:** „QCN3 / SMA version” a `GERBER-CmxSma.zip`
fájlra mutat, nem QCN3-gerberre. Ne rendeljen úgy PCB-t, mintha QCN3-as terv
lenne.

### M — Gyártók és elérhetőség

- Mini-Circuits **QCN-3+**:
  <https://www.minicircuits.com/WebStore/dashboard.html?model=QCN-3%2B>
  kifejezetten „LTCC 90° Hybrid, **220–470 MHz**, 50 Ω” specifikációt mutat;
  ellenőrizve 2026-10-10. Tartalmazza a 435MHz-et, kizárja a 145MHz-et.
  Ne tévessze össze a README „+” nélküli megnevezésével.
- Hivatkozott adatlap: <https://www.minicircuits.com/pdfs/QCN-3+.pdf>.
  A válasz bináris PDF volt, a határtáblázat nem nyerhető ki olvashatóan;
  **az adatlapnak nem tulajdonítunk konkrét teljesítmény-, fázis- vagy
  leválasztási értéket**.
- CMX03A03-hoz és Anaren 10260-3-hoz nem találtunk olvasható gyártói
  adatlapot. Anaren-lekérdezés szállítási/DNS/TLS hibával végződött,
  TTM-index 403-at adott; egy feltételezett CMX-útvonal nem oldódott fel.
  A vizsgált DigiKey/Coilcraft útvonalak 403-at adtak. Sávot, áramhatárt,
  Q-t vagy SRF-et nem találunk ki. Vásárlási feltétel a pontos azonosítás
  és eredeti adatlap.

## Vizuális antennareferenciák

- **B — Blog**, 2020. áprilisi archívum:
  <https://blog.tomasbrincil.cz/?m=202004>. A leírás és három képlet
  áttekintve; AV-2040 inspirációjú, **449.550MHz** tervet ad meg.
  STL/OBJ-kifejezett licenc nem igazolt. A hivatkozott fájl elérése nem
  jelent származék készítésére engedélyt.
- **T — Thingiverse 5904442**:
  <https://www.thingiverse.com/thing:5904442>. Csak az
  **„AV-2040 MilSat Antenna by German_Panda”** cím volt elérhető.
  Részlet, méret, fájl, licenc e vizsgálatkor nem állt rendelkezésre;
  geometriát vagy RF-et nem állítunk validáltnak.
- **C — A projekthez adott Cults-képernyőkép**: jelzett feltételei
  **kereskedelmi / magánhasználat / NoAI**. A kép nem származtatási licenc.
  Nem követünk le, másolunk vagy adaptálunk kereskedelmi alkatrészt belőle,
  és a fájlokat nem vetjük generatív elemzés alá. Ellenőrizhető teljes adatlap/
  licenc nélkül assetet nem építünk be.

## A terv lezárásához hiányzó bizonyíték

1. Pontos referencia szerinti NEMA14-méretek, tengelyek/furatok gyártói
   adatai; új 25:1 bolygómű nyomatéka, holtjátéka, hatásfoka/ellenállása
   gyártás és teszt útján.
2. Diplexer tényleges doboz-, csatlakozó- és kábelméretei; a közzétett
   karima/front méretbecslés.
3. Antennák/összeszerelt hálózat VNA-mérése, polarizáció/tengelyarány és
   a konkrét példány teljesítménytesztje.
4. Mindkét sáv hibridjelöltjének azonosított adatlapja. A nagy teljesítmény
   sávadat nélkül nem megfelelő specifikáció.
5. Az RT-3S pontos firmware/CPS-e és helyi Satellite-képernyőpróba.
   A felhasználó rádióját/CAT-protokollját nem vizsgáltuk.
6. Aktuális műhold-efemerida és állapot: a történeti listák példák,
   nem adási engedélyek.
