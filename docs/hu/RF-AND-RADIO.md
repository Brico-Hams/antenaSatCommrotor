# Multimódusú PortableSatStation: RF, polarizáció és RT-3S – igazolható korlátok

Dátum: 2026-10-10. A források/verziók a [SOURCES.md](SOURCES.md), a PDF-ek
elemzése a [REFERENCE-ANALYSIS.md](REFERENCE-ANALYSIS.md) fájlban.
Névleges cél 145/435 MHz; a teljes rendszer nincs tanúsítva.

## Három különböző fogalom

| Elem | Feladat | Amit NEM bizonyít |
|---|---|---|
| **Diplexer**, három port | Egy közös 50 Ω-os port és két sávág: VHF és UHF; alul-/felüláteresztő szűrés | Nem hoz létre körpolarizációt és nem ad második vevőt a rádióhoz |
| **Full-duplex működés** | Vétel adás közben, megfelelő rádióval/rádiókkal és leválasztással | Két beprogramozott frekvencia vagy dual-watch nem elegendő |
| **90°-os hibrid**, négy elektromos port | Két ortogonális dipólus/sík megfelelő amplitúdójú és fázisú táplálása a saját sávjában; a negyedik, leválasztott port lezárt | Nem választja szét a 145/435 MHz-et és sávon kívül nem biztosít jó tengelyarányt |

A tároló neve DuplexorSpaceQuad, de a README elektromosan **diplexert** ír
le. Ne következtessen „full duplex” működésre a névből.

## Javasolt topológia, körpolarizáció vagy egyidejű vétel feltételezése nélkül

```text
RT-3S: egyetlen RF-port
           |
    opcionális 145/435 diplexer, csak a konkrét példány mérése után
       |                                      |
   VHF-ág                                UHF-ág
       |                                      |
   VHF-antenna                           UHF-antenna
   (kezdetben lineáris)                  (kezdetben lineáris)
```

Körpolarizáció esetén **mindkét** ághoz két ortogonális sík és saját,
karakterizált fázishálózat kell, vagy közösen tervezett és tesztelt fizikai/
elektromos fáziseltolás. Ismeretlen sávú, egyetlen SATCOM-hibridet ne tegyen
a diplexer elé azért, hogy „mindkét sáv körpolarizált legyen”.

A dipólusok orientációja és a portok határozzák meg az RHCP/LHCP irányt.
Dokumentálni kell a megfigyelési konvenciót és kísérletileg ellenőrizni;
a koaxiális kábel színe nem bizonyíték. Ideális kör→lineáris átmenet 3 dB
veszteséggel jár; az ellenkező kézirányú körpolarizáció vesztesége nem
általánosan 3 dB.

## D — A felhasználó nyilvános projektjének pontos hálózata

Ajánlott revízió: `f5c7dc375ed7b9882f52bd7757deaf44cd422b81`,
README/BOM:

| Ág / referencia | Ajánlott revízió értékei |
|---|---|
| VHF aluláteresztő | L1/L3=68nH; L2=100nH; C1/C2=18pF |
| UHF felüláteresztő | L4/L5=15nH; **C3/C5=8.2pF; C4=4.7pF** |
| Történeti UHF-rajz | C3/C5=4.7pF; C4=2.7pF: ne keverje az optimalizálttal |
| Alkatrészek | 0805; nagy Q-jú induktorok (példák: 0805CS-680XJL/101XJL/150XJL); C0G/NP0 >=100V kondenzátorok |
| PCB | 2 rétegű, 1,6 mm FR4, 1 oz réz; szerzője 50 Ω CPWG-t, 1,4 mm vezetéket és 0,25 mm földhézagot ad meg |
| Cél-sáv | 144–146 MHz és 430–440 MHz |

A szerző az eredeti kapcsolási rajz C1/C2 10/18pF értékét kétértelműnek
mondja, és 18pF-et választ. Ne keverje a történeti és optimalizált BOM-ot.
Az alkatrésztűrést, Q-t, ESR-t, SRF-et, áramot és PCB-parazitákat itt nem
ellenőriztük a komponensek adatlapjához.

### A szimuláció NEM mérés

A README az optimalizált, **ideális** szimulációnak S11≈−31dB-t tulajdonít
145/435MHz-en, behelyezési veszteséget <0,05dB-nek és leválasztást >49dB-nek.
Ezek nem garantált specifikációk, és nem bizonyítják, hogy a diplexer
kompatibilis az új antennával/rádióval.

A `docs/PRUEBAS.md` fizikai célokat határoz meg:

| Mérés, másik port 50 Ω-ra zárva | A forrás kritériuma |
|---|---|
| S11 RADIO-port, lezárt ágak | <−15dB 144–146 és 430–440MHz-en |
| RADIO→VHF | Behelyezési veszteség <0,5dB 145MHz-en; elnyomás >35dB 435MHz-en |
| RADIO→UHF | Behelyezési veszteség <0,7dB 435MHz-en; elnyomás >35dB 145MHz-en |
| VHF→UHF, RADIO lezárva | Leválasztás >35dB mindkét sávban |
| Teljesítmény terheléssel/vattmérővel | 1→5→10W fokozatok, stabil SWR, észrevehető melegedés nélkül |

Ezek **még nem teljesített kritériumok**, nem mérési eredmények.
10W-os próbát ne végezzen, amíg a példány, csatlakozók, induktorok,
kondenzátorok, terhelés és hőelvezetés besorolása nincs előbb ellenőrizve.
Az „észrevehető melegedés nélkül” nem megfelelő minősítés: hőmérsékletet,
időt/munkaciklust, teljesítményt és SWR-t kell rögzíteni.

Az 0805 méret önmagában nem garantál teljesítményt. A README hordozható/
QRP használatra **kb. 5–10W**-ot állít, nagyobb teljesítményhez légmagos
tekercset/megfelelő kondenzátort ajánl. Az új összeállítás elfogadási
vizsgálata minimális teljesítménnyel indul; a 10W nem tanúsított határ.
A 100V-os kondenzátor sem garantál RF-áramot, a nagy Q-jú induktor sem
garantálja a melegedés elmaradását.

**Nagyságrendi példa:** 5W / 50Ω esetén 15,8V RMS és 22,4V csúcs adódik,
mielőtt az SWR-t és reaktív hálózatot figyelembe vennénk. Ha a leválasztás
35dB lenne, 5W≈37dBm körülbelül 2dBm-et hagyna az ellenkező ágban,
további szűrés/veszteség előtt. Ez a műholdas jelhez képest óriási lehet.
Későbbi vevő/LNA elfogadását ne egyetlen elnyomási szám alapján hagyja jóvá,
és ne feltételezze, hogy egy szimulált szűrő bizonyítja a valós
deszenzitizáció hiányát.

A műanyag doboz **nem RF-árnyékoló**. Földsík/via segíthet, de nem helyettesíti
az árnyékolást. Vezetőszalag/festék folyamatos elektromos kötést, biztonságos
csomópont-távolságot, szigetelésellenőrzést és utólagos tesztet igényel;
ASA dobozt próba nélkül ne nevezzen tömítettnek vagy árnyékoltnak.

### A közzétett pontos geometria és mechanikai blokkoló

| Közzétett interfész | SMA | BNC |
|---|---:|---:|
| PCB | 37×23mm | 55,5×33mm |
| Külső doboz | **45,2×27,6×14,1mm** | **59,9×37,6×23,5mm** |
| Csatlakozó | Amphenol132289, él-/bulkhead | AmphenolB6252HB-NPP3G-50, PCB-re merőleges |
| Rögzítés | 2×M2×10 önmetsző | 2×M2×12 önmetsző |
| PCB-furatok | 2×Ø2,2mm, földelt fémezett | 2×Ø2,2mm, földelt fémezett |

A `docs/MONTAJE.md` SMA-paraméterei: 9,6mm széles és 1,9mm vastag karima,
tengely „PCB+0,4mm”, 6,8mm osztás 1/4″-36 menetes csatlakozóhoz.
BNC-test 14,8mm-rel a PCB fölött, tengely „PCB+7,5mm”, elülső sík 14,9mm.
Fal/alj/tető: 2,0/2,0/1,6mm; peremhézag 0,15mm. BNC-lábak legfeljebb
2,5mm-rel lóghatnak a PCB alá.

**A README kifejezetten becslésnek nevezi a csatlakozóméreteket, KiCad-
lábnyomokból.** A külső méretek közzétett adatok, nem a felhasználó hardverének
mérései. A dobozt és valódi csatlakozókat tolómérővel mérje; az új tartónál
ne tulajdonítson a „PCB+” méretnek magassági origót CAD-metszet ellenőrzése
nélkül. Végleges fedél előtt próbálja fel az alapot.

Maradjon paraméteres, csatlakozókat nem terhelő tartó/bilincs, csavarhozzáférés
és elektronika-/motor-távolság. A burkoló méretéhez hozzáadandó a kontraanya,
BNC-csatolás, SMA-dugó, húzásmentesítés és a gyártó szerinti minimális
koaxhajlítási sugár; ezeket a külső méret nem tartalmazza automatikusan.
Furatkoordinátát ne találjon ki; közvetlen PCB-támaszhoz keresse elő a
`board_geometry.json` fájlt, és vesse össze a valós példánnyal.

## H/M — Hibrid: sáv szerint kell kiválasztani, nem teljesítmény alapján

| H-jelölt | README állítása | Megszerzett gyártói bizonyíték | Döntés |
|---|---|---|---|
| CMX03A03 | 200W + G150N 50Ω terhelés | Nem találtunk olvasható sáv-/teljesítmény-adatlapot | 145/435MHz-re ne válassza |
| „RF Power”, állítólag Florida RF Labs | 200W, bizonytalan azonosítás | Nincs egyértelmű modell/adatlap | Vásárlási BOM-ból kizárva |
| Anaren10260-3 | 250W, régi | E keresésben nem volt olvasható adatlap | Sáv/határ függőben; nem tanúsított |
| QCN3, a BOM-ban QCN-3 | 15W, két 100Ω/2512, 2W-os ellenállás | Mini-Circuits **QCN-3+**: **220–470MHz** | 435MHz benne, **145MHz kívül**. Suffix/példány azonosítandó; dualbandként nem alkalmazható |

A QCN-3+ 225–400MHz-es feltételezése nincs megerősítve: a megkérdezett
gyártói forrás 220–470MHz-et ad meg. Ezt nem terjesztjük ki automatikusan
suffix nélküli alkatrészre vagy piactéri másolatra. A névleges sáv önmagában
nem bizonyít elfogadható veszteséget/fázist 435MHz-en a mi terheléseink mellett.

**H-valós hiba:** a QCN3 alatti SMA-link a `GERBER-CmxSma.zip` fájlra mutat.
Ne gyártsa úgy ezt a fájlt, mintha QCN3-as PCB volna.

Két 100Ω párhuzamosan névleg 50Ω és összesen 4W, **nem validált RF-terhelés**,
és nem bizonyítja a 15W elviselését. A leválasztott port rosszul illesztett
terhelés esetén jelentős teljesítményt vehet fel; konzervatív határként a
hálózat legrosszabb esetére méretezendő. Ellenőrizze a hőelvezetést,
szerelést, 435MHz-ig terjedő impedanciát, besorolást és hőmérsékletet.
Egy levegőben megadott 150W-os terhelés sem feltétlenül képes megfelelő
hűtés nélkül 150W folyamatos disszipációra.

## O0/O1 — Az RT-3S tényleges OpenGD77-képessége

A kért régi O0 útmutató csak eltérő TX/RX frekvenciájú VFO-t igazol
cross-band/split használathoz; nem igazol RT-3S-t vagy aktuális
műholdképernyőt. A karbantartott O1 útmutató (`2289ba75…`, 2026-03-10)
igen felsorolja az **MD-UV380(RT-3S)** modellt, és dokumentálja:

1. **Satellite Screen:** következő 24 órát jelez előre hely, dátum és idő
   alapján; AZ/EL-t mutat és automatikusan korrigálja a **TX- és RX-
   frekvenciák** Doppler-eltolását.
2. A felhasználó beírja a helyet és dátumot/időt, és CPS-szel betölti a
   **Keps** adatokat. Friss Keps betöltése az útmutató szerint a dátumot/időt
   is beállítja.
3. E leírás az RT-3S/UV380-at RTC-vel rendelkezőnek mondja, de ez nem
   bizonyítja a pontosságot vagy a felhasználó készülékében lévő elem állapotát.
4. A frekvenciát és CTCSS-t a CPS adataival kell betölteni; módosításhoz
   a megfelelő CPS `satellites.txt` adatait kell szerkeszteni.
5. SO-50: az útmutató szerint adás közbeni SK1 alkalmazza az aktiváló tónust;
   az aktuális állapotot/módot ellenőrizze.
6. Az élő képernyőn 1 FM Voice, 2 APRS, 3 Beacon típus van; beacon esetén
   nincs TX. Ez nem jelenti azt, hogy a helyi táblázat minden műholdja
   kompatibilis a rádióval.
7. A „Sat / Manual” és „Auto” az LOS utáni következő műholdra váltást
   szabályozza. Itt a „Manual” nem feltétlenül jelent kézi Dopplerállítást.
   Különítse el a műholdválasztást a frekvenciakorrekciótól.

### Használati terv kitalált CAT nélkül

- Rögzítse a rádió modelljét/firmware-buildjét és a CPS verzióját; mentse a
  codeplugot/konfigurációt. Ellenőrizze, hogy a valós rádió Satellite menüje
  megjelenik és helyesen számol.
- Előkészítésként CPS-szel töltse be a Keps/adatokat; az RT-3S és vezérlő
  UTC/hely értékét szinkronizálja. A rotor AP-ja **nem tölti be varázsütésre
  a CPS-t**.
- A rotor önállóan SGP4-et számol és AZ/EL-t mozgat. Az RT-3S-t a
  billentyűzetről/PTT-vel kezelje, az integrált Dopplerét használva, ha a
  build támogatja. Alternatíva: előbeállítás/kézi Doppler, ha nincs ilyen funkció.
- Hasonlítsa össze az előrejelzést/időt/frekvenciákat; eltérő TLE, UTC vagy
  hely akkor is eltérést okoz, ha mindkét képernyő működik.
- **RT-3S CAT**, élő USB-vezérlőprotokoll, távoli PTT, full-duplex és
  adás közbeni vétel nincs ellenőrizve. Ne implementálja Yaesu/IC-820H
  parancsokkal vagy nem létező API-val.
- Ne keverje össze a DMR-t, digitális hotspotot vagy CPS-programozást a
  műholdas CAT-porttal. Ezzel az FM/DMR hordozható készülékkel ne ígérjen SSB/CW-t.

## Minimális fizikai elfogadási terv

1. **Dokumentáció/kábelek:** azonosítsa a valós alkatrészeket, pinoutot/
   portokat, csatlakozókat, kábel VF-et és minimális hajlítási sugarat.
   Feszültség nélkül vizsgálat/folytonosság.
2. **Külön antennák:** kalibrált VNA a valódi referencia-síkon; S11 és
   sávszélesség mérése végleges tartón, rendezett koaxszal. Rögzítse a
   hajtott állapotot és a rotor közelségét.
3. **Külön diplexer:** SOL/through; 100–500MHz söprés >=401 ponttal;
   szabad portokon 50Ω terhelés; minden út/reflexió mérése. Mentse a
   Touchstone-adatot, képeket, dátumot és beállítást. A 35dB leválasztás
   előtt mérje meg a zajpadlót/dinamikatartományt.
4. **Polarizációs hálózat, ha van:** veszteség, amplitúdó-/fáziskülönbség,
   illesztés és leválasztott port sávonként. Sugárzott kézirány/tengelyarány/
   mintázat, meghatározott módszerrel és geometriával.
5. **Teljes szerelék:** illesztés/antennakölcsönhatás, sávleválasztás és
   kábelhatás mérése AZ/EL változtatásakor. Tartó/koax csere után ismételni.
6. **Teljesítmény terhelésre:** alacsonyan kezdeni, csak igazolt besoroláson
   belül növelni. Hőmérséklet/SWR/idő és alkatrész szerinti tűrt legrosszabb
   illesztés; finomhangolás alatt ne sugározzon antennára.
7. **Motor-EMI:** vétel összehasonlítása kikapcsolt/hold/mozgó meghajtóval,
   DC/DC-vel és működő AP-vel. Zaj esetén áthelyezés/szűrés.
8. **Üzem:** előbb vételi átvonulás, az aktuális műhold/mód és jogosultság
   ellenőrzése, ésszerűen kis teljesítmény. Ne telítse LNA-t/vevőt
   „leválasztásmérés” ürügyén.

Jelenlegi állapot: **az architektúra indokolt, az RF-jelöltek és próbák
meghatározottak; az antenna/diplexer/hibrid és rádió–rotor rendszer még NINCS
megmérve vagy jóváhagyva.**

## A — Összevetés az új AV2040 kereskedelmi adatlappal

A helyi `TDS_AV2040.pdf`, 1. PDF-oldal **összecsukható/manpack UHF SATCOM
antennát** azonosít. A szövegkinyerés betűkódolás miatt elveszíti a
számjegyeket; az értékeket helyben, 140dpi-re raszterizált
`TDS_AV2040-000001.png` képről olvasták. Gyártó Ultralife/Trivec-Avant,
**2010 NOV 23, UBI-05273 REV:-**. Az adatok kereskedelmi adatlapból
származnak, nem a PortableSatStation méréséből.

| Szempont | A rendelkezésre álló adatlapbizonyíték | Következmény |
|---|---|---|
| 145MHz | Kereskedelmi sáv **240–400MHz** | **145MHz sávon kívül**, VHF-fedezet nincs igazolva |
| 435MHz | Kereskedelmi sáv **240–400MHz** | **435MHz sávon kívül**, SATCOM megjelenés nem bizonyít kompatibilitást |
| VSWR | Közölt 1,5:1 | Sávon kívülre vagy új tervre nem vihető át |
| Polarizáció | Jobb kör; 3dB tengelyarány | Nem garantálja a mi fázishálózatunkat/tengelyarányunkat |
| Változatonkénti nyereség | 2040-3: +7dBic 240–400; 2040-2: +11dBic 240–318; 2040-1: +9dBic 240–400MHz | Ne keverje a változatokat/sávokat, és ne tulajdonítsa ezeket az ASA-antennának |
| Teljesítmény | Közölt 200WattsCW | Nem az új hibrid/PCB/diplexer besorolása |
| Összecsukhatóság | Összecsukható/manpack leírás | Funkcionális igény, nem licenc vagy geometriai méret |
| Nyitott/összecsukott méret | **A vizuális oldalon nincs méretezés** | Nincs ellenőrizhető hossz/szélesség/térfogat; fotót ne kezeljen tervként |
| Tömeg | 6,5 font ≈2,948kg adatlap szerint | Ne vigye át az ASA-tervre sem tömeget, sem CG-t |
| Csatlakozó | BNC male | Az interfészt/vezetéket ellenőrizze; ne tévessze össze a diplexer BNC female portjával |

A 449.550MHz frekvencia a **B bloghoz** tartozik, nem az A adatlaphoz,
és a kereskedelmi 240–400MHz sávon kívül esik. A blog átdolgozott terve
másik konstrukció, nem bizonyítja a gyári AV2040 sávbővítését. Az AV2040
**funkcionális referencia, nem specifikáción belüli 145/435MHz alternatíva**.
A fényképen nincs összecsukási méret, ismeretlen licencű OBJ/STL nem kerül
terjesztésre. A gyártói lábjegyzet szerint az adatok csak tájékoztatók,
nem teljesítménygaranciák és változhatnak.
