# A hivatkozások elemzése és az új terv döntései

Dátum: 2026-10-10. Azonosítók/revíziók a [SOURCES.md](SOURCES.md)
fájlban. Mind a hat helyben kivont szöveget teljes egészében elolvastuk.
„nyomt. o.” a kézikönyv ellenőrizhető nyomtatott oldalszáma;
„PDF-o.” oldalszám nélküli cikk pozíciója, nem kitalált kiadói számozás.

## 1. P1 — Gordon Gibby KX4Z állomásának bevezetése

**Tényleges tartalom.** P1, 1. PDF-o.: VHF/UHF irányított antennák,
szűrőkkel való szétválasztás, orbitális modellel történő célzás, full-duplex
rádió, Doppler és érzékenység. A példa költségtakarékos építésű állomás,
nem integrált hátizsákos készülék. P1, 2. PDF-o.: K3NG Arduino-vezérlő,
motor/aktuátor potenciométerekkel. P1, 3–4. PDF-o.:

- Gpredict: előrejelzés és megjelenítés.
- rigctld/Hamlib: rádióinterfész; szerző IC-820H esetén nehéznek találta
  a MAIN/SUB és mindkét Doppler vezérlését.
- rotctld: kívánt helyzet protokollja, **nem** közvetlen motorvezérlés,
  és nem fizikai szög-visszajelzés.
- SatPC32: Windows-alternatíva, amely a szerző IC-820H rádiójával működött.

**Alkalmazás.** A predikciót, tervezést, motort és rádiót különítsük el.
PortableSatStation normál módja a vezérlőn számolja az SGP4-et, helyi AP-t
ad, TLE-t/helyet/UTC-t tárol PC-függőség nélkül. Opcionális külső protokoll
nem váltja ki a beágyazott SGP4-et.

**Nem vihető át.** A full-duplex igény a szerző állomásáé. Külön TX/RX
frekvenciájú RT-3S ettől nem fog adás közben venni. Az IC-820H működése és
más rádió CAT-parancsa sem bizonyít RT-3S-interfészt.

## 2. P2 — Költségtakarékos vezérlőpanel

**Tényleges tartalom.** P2, 1. PDF-o.: a K3NG bővítése Nano-ra, gombokra,
mozgás/irány-kimenetre, memóriakorlát figyelmeztetéssel. P2, 2–3. PDF-o.:
kapcsolási rajz, kétoldalas PCB és prototípus; LCD/gombok a Nano/csatlakozók
ellentétes oldalán. P2, 4–5. PDF-o.: LM7805, 1A diódák, tranzisztorok,
P-csatornás MOSFET és csatlakozások. P2, 6–7. PDF-o.:

- MOSFET a táp/PWM kapcsolásához; külső, két SPDT relés panelek
  **egyenáramú motor polaritásváltására**.
- Tengelyenként egy relépanel; 0/5V logika és 12V relétáp.
- G-450ADC fordulata kb. 90s; 2A-es tápegység-becslés; magasabb
  bemenetnél a lineáris szabályozó hűtőbordát igényelhet.

**Alkalmazás.** Hasznosítható elv: logika/táp szétválasztása, kézi vezérlés,
zavarvédelem és fokozatos teszt. Az egyenáramú kapcsolást ne vigye át
léptetőmotorra: a NEMA14 kétfázisú áramvezérlő meghajtót,
STEP/DIR/ENABLE jelet, elektromos határokat és gyorsítási profilt igényel.

**Nem vihető át.** Yaesu 2A/90s nem méretezi a NEMA14 akkumulátorát,
áramát vagy sebességét. A 25:1 arány sem igazol kimeneti nyomatékot:
hiányzik a dinamikus nyomaték, hatásfok, backlash és a konkrét hajtómű határa.
A dokumentált panel önmagában nem nyújt AP-t, SGP4-et, GNSS-t vagy valódi északot.

## 3. PC — Panelépítési kézikönyv

**Tényleges tartalom és nyomtatott oldalak**

| Oldal | Bizonyíték | Új terv szerinti döntés |
|---|---|---|
| nyomt. 1–2. o. | Forrasztásbiztonság, szemvédelem, dióda/elektrolit polaritása és félvezető-orientáció | Jó gyakorlat megtartandó; a szöveg minden kémiai magyarázata nem műszaki specifikáció |
| nyomt. 3. o. | Első szerelési szakasz csak azimut | Üzembe helyezés alrendszerenként/tengelyenként, követés előtt |
| nyomt. 4–5. o. | 2N3904 és ellenállások logikai irányt állítanak elő; MOSFET kapcsolja a motortápot | Az új rendszer irányjele és STEP/DIR meghajtója nem azonos e kimenetekkel |
| nyomt. 6. o. | Szabadonfutó dióda, szűrőkondenzátor, opcionális resetgátló kondenzátor | Meghajtó/induktivitás szerinti védelem; a Nano-kapcsolást ne másolja válogatás nélkül |
| nyomt. 7. o. | Polaritásvédelem, 5V szabályozó, RF-szűrők és kézi gombok | Modern elektronikához/valódi akkumulátorhoz megfelelő DC/DC és védelem kell |
| nyomt. 8. o. | 5V-os potenciométer, korlátozó ellenállás és Nano ADC | 3,3V-os MCU ADC-je **nem fogadja automatikusan** az 5V-os jelet |
| nyomt. 9. o. | 5V ellenőrzése a Nano forrasztása előtt; 16×2 LCD és mechanikai elrendezés | Elektronika csatlakoztatása előtt feszültségmérés; vezetéknek/szerviznek hely |
| nyomt. 10. o. | Rövidzár-ellenőrzés, USB-táp, programozás | Motor nélkül, aztán meghajtókkal és tengelyenként, terhelés nélkül tesztelni |

**Konzisztenciafigyelmeztetés.** A kézikönyv és P2 táblázat néhány
ellenállás-megnevezése/értéke (pl. R2/R3) nem egyezik tisztán. E két
szövegből automatikusan ne készítsen új PCB-t vagy szerelési BOM-ot;
ellenőrzött kapcsolási rajz/revízió az irányadó. Ez a projekt nem építi meg
azt a panelt.

## 4. P3 — Kéttengelyes rotor

**Tényleges tartalom.** P3, 1. PDF-o.: kézi, fix elevációs és kereskedelmi
lehetőségeket ismertet; nem tartós, vízzáró telepítésnek szánja.
P3, 2. PDF-o.: **Yaesu G450ADC** azimut faalapon, emeléshez 12V-os,
**2 hüvelyk löketű** lineáris aktuátor. A nagyon áttételes motor és
90°-os hajtómű próbája fogkárosodás miatt sikertelen. A tengelytől kb.
1 hüvelykre tett csap csak első geometriai közelítés, nem általános
kinematikai megoldás.

P3, 3. PDF-o.: aktuátor belső végállásai és elevációs potenciométer.
P3, 4. PDF-o.: **10mm** tengelyek, PVC/gumi/bilincs adapter,
kb. 15–75° eleváció és 90° fölötti használat mellőzése. Az alsó rotor
a teljes felső szerelvényt forgatja. P3, 5. PDF-o. csak antennás
összeállítási képfeliratot ad.

**Alkalmazás.** Antenna/koax kiegyensúlyozása, erők csapágyakkal való
felvétele, tengely/boom-kapcsolat ellenőrzése és az azimutra ható teljes
fejrész-terhelés figyelembevétele. Az új, ASA-ból tervezett NEMA14/
25:1 bolygóműves rotor nem a faalkatrészek vagy dugattyús kinematika
származéka.

**Nem vihető át.** A G450ADC robusztussága nem bizonyítja, hogy egy
NEMA14-hajtómű radiális/axiális terhelést visel. A kimenő tengelyt
szerkezeti tartó/csapágy tehermentesítse. A bolygóművet ne tekintse
önzárónak: feszültség nélkül ellenőrizze a megtartást/viselkedést.
Az aktuátor végállása nem helyettesíti a léptetőmotor homingját és ütközőit.
Zenitközeli átvonuláshoz olyan tervező kell, amely határt/sebességet tart,
nem önkényes AZ-ugrás vagy nem igazolt mechanikus flip.

## 5. P4 — Keresztpolarizált Yagi-k, 2025. július

**Tényleges tartalom.** P4, 1–2. PDF-o.: polarizációs fading és két sík.
P4, 2–3. PDF-o.: 90° előállítása fázisvezetékkel vagy fizikailag λ/4
hosszirányú eltolással, ortogonális síkokkal és táplálási orientációval.
**20,36 hüvelyk** 2m-en és **6,78 hüvelyk** 70cm-en, azaz 517,144 és
172,212mm. Ezek a referenciaelrendezés síkjai közti eltolások, nem egy
egyetlen kétsávos antenna méretei.

P4, 4. PDF-o.: nemvezető boom és Cheap Yagi terv, kezdetben 4 VHF +
6 UHF elem, a másik síkban 3 VHF + 5 UHF elem. Az elemátmérő módosítja
a hosszokat. P4, 5–7. PDF-o.: nyílvessző/alumínium kötések, betétek és
réz, változó eredménnyel; nem ismételhető ipari folyamat. P4, 8–10.
PDF-o.: VNA-s hangolás/elöl-hátul összehasonlítás és indexelhető,
szétszedhető PVC boom.

P4, 9. PDF-o.: sebességtényezővel korrigált elektromos λ/2 RG58
betáplálások BNC T-vel; a szerző általánosan **2:1–3:1 SWR**-t közöl,
nem ideális illesztést. P4, 11. PDF-o. képaláírása 1,2:1 SWR-t ad
**444,8MHz-en**; ez nem bizonyít 435MHz-es SWR-t vagy teljes sávot.
P4, 12. PDF-o.: kb. **40dB vagy jobb** antennák közti leválasztást közöl
a saját szerelékében; előerősítős vétellel, diplexer egyik oldalát
szűrőként használva, IC-820H ~30W, 50 láb LMR400 koaxszal.
P4, 13. PDF-o.: anyagokat és sorozathivatkozásokat sorol fel.

**Lényeges pontosítások és korlátok**

- A két antennát összekötő T önmagában nem hoz létre kvadratúrát vagy
  illesztést. Ismert impedancia és fázis kell; a megfigyelt eset nem
  általános szabály más dipólusokra.
- **Ne** fogadja el univerzális kritériumként a cikk állítását, hogy RHCP/
  LHCP-váltás mindössze 3dB veszteség. Ideális, ellenkező kézirányú
  körpolarizáció erősebb elnyomást ad; 3dB ideális kör és lineáris
  polarizáció közt érvényes. Valós eredmény a tengelyaránytól,
  orientációtól és terjedési úttól függ.
- A 4–5. PDF-o. UHF-táblája ellentmondó: kezdeti Director 1 értéke
  12,3 hüvelyk, a szöveg szerint pedig „rövidül” 13,1-re.
  Az ellentmondást rögzítjük; **vágási rajzként nem használjuk**.
  Eredetit/forrást ellenőrizni és mérni kell.
- A 30 lábról felvett iránydiagram és a szerkezet leválasztása nem igazol
  abszolút nyereséget, tengelyarányt vagy az új hordozható antenna
  leválasztását. Nem adhatók hozzá automatikusan az ideális diplexer dB-jei.
- Két, kb. λ/4 távolságú VHF-sík hat a hosszra, tömegközéppontra,
  nyomatékra és szélfelületre. Más antenna tömege/nyomatéki büdzséje
  nem ruházható át.

**Alkalmazás.** Előbb ellenőrizhető RF-architektúrát válasszon:
sávonként egy irányított antenna, kezdetben lineáris polarizációval, ha
az megkönnyíti a validálást; vagy ortogonális síkok sávonkénti
**külön fázishálózattal**. A végleges ASA/koax/tartóval kell hangolni.
A körpolarizáció mérésre váró bővítés, nem díszítő címke.

## 6. PT — SatelliteTargets lista

**Tényleges tartalom.** PT, 1. PDF-o.: FM átjátszók (ISS, SO-50, HADES-R)
és VHF lefelé irányuló lineáris transzponderek; frekvenciák, középfrekvenciák
és aktiváló/CTCSS-hangok. PT, 2. PDF-o.: RS-44 és MESAT1 lineáris UHF
downlink, ISS packet 145.825 és SONATE-2. Nincs érvényességi dátum vagy TLE.

**Alkalmazás.** Megmutatja, hogy „145/435” sáv, nem egyetlen csatornapár;
műholdanként mód, TX/RX, hang és efemerida szükséges. A táblázat **nem
importálható engedélyezett üzemi listaként**. Adás előtt AMSAT/üzemeltető
adatát ellenőrizze, és a rádióval kompatibilis FM-et válasszon.

**Nem vihető át.** Az RT-3S FM/DMR nem lesz SSB/CW az RS-44, AO-7 vagy
más lineáris transzponder betöltésétől. A packet megfelelő adatút/modem
nélkül nem működik; a mechanikai követés önmagában nem ad AX.25-öt.
Az AO-7-re említett FCC-mentesség más joghatóságé, nem automatikus helyi
engedély. Az ISS módot válthat; két történeti bejegyzés egyidejű
működését ne garantálja.

## 7. L — LibreSat: rendszerreferencia, nem mért prototípus

A nyilvános revízió Pi Zero 2 W + RP2040 és NEMA17 **nyomtatott, 25:1
cikloidális áttétel**, nem új NEMA14/bolygómű. README: Ø94mm aktor,
kb. 45mm-rel a motoron túl; két 61810 csapágy; AS5600 a motor hátsó tengelyén.
MECHANICAL: 5mm motor kimenőtengely, 6803 **17×26×5mm**, 61810
**50×65×7mm** csapágy, Ø20×250mm tengelycsonk, 42mm betolás, antenna
kb. 200mm-re az aktuátor felületétől.

ASA-t ír le kültéri elemekhez; állványadaptert; 60cm kábelhurkot AZ225°
középpel, 0–450° tartományhoz; 300–500mm mast hosszabbítást bizonyos
>1,1m boomokhoz. Ezek **LibreSat-méretek**, nem garantáltan kompatibilis
PortableSatStation-alkatrészek.

A SIZING 1kg antenna, 0,1m² felület, 0,15m szélnyomási kar, 20mm
egyensúlyhiba, 10m/s szél és 75% hatásfok értékekből indul. EL-re 1,30Nm,
AZ-re 1,10Nm, átlagosan 4,1W-ot és flip-es léptetés szimulációját számolja.
E biztonsági tényező, autonómia és célzási hiba nem eredménye az új tervnek.
A README maga is elismeri, hogy az összeállítást nem építették meg/mérték meg.

**Tanulság:** helyi AP, offline TLE, óra/hely, kábelcsavarási tervező,
kiegyensúlyozott szerelés és újrakalibrálás megtartandó. A motoron lévő
encoder érzékeli a lépésvesztést, de **nem méri az áttétel utáni holtjátékot
vagy megcsúszást**. A lépésszám mentése nem állítja vissza a tájolást,
ha a szerelék feszültség nélkül elmozdult. Egyantennás GNSS pozíciót/UTC-t
ad, nem álló állomás abszolút irányát. A szint/gravitáció dőlést ad, nem
azimutot. Valódi északhoz explicit módszer, kalibrálás, magnetométer
esetén deklináció/interferenciadetektálás szükséges.

## 8. B/T/C — Geometriai hivatkozások

B blogja **449.550MHz**-et ad meg, aktív elemhosszként
`0.92·c/(2f)`-et számít, reflektor 1,05× ezt, térköz 0,225λ.
Csak első becslésként értékelve:

| Frekvencia | Aktív teljes hossz | Reflektor teljes hossz | Térköz |
|---|---:|---:|---:|
| 145MHz | 951,066mm | 998,619mm | 465,195mm |
| 435MHz | 317,022mm | 332,873mm | 155,065mm |

Teljes hosszak, nem karonkénti méretek, és nem validált dualband terv.
A léptékkülönbség saját architektúrát igényel; dielektromos tartó,
csőátmérő, sávok közelsége és táplálóhálózat eltolja az impedanciát/
sugárzási mintát. A „SATCOM” vagy AV-2040-re hasonlító megjelenés nem
garantál 145/435MHz-es fedést.

T csak ellenőrizhető címet ad, méretet/licencet nem. C feltételei:
kereskedelmi/magánhasználat/NoAI; modelljét nem másoljuk, követett
származékot nem készítünk. Az általános funkcionális inspiráció
(összecsukhatóság, tripod, hordozhatóság) nem jogosít idegen geometria
reprodukálására.

## 9. Integrációs döntések és blokkolók

1. **Eredeti új terv**, ASA szerkezet; NEMA14/25:1 bolygómű csak pontos
   modell/adatok rögzítése után. Kúszást, hőmérsékletet, csapágyat,
   terhelést és rögzítést próbával ellenőrizze. A `calc/design.json`
   200 lépés/fordulat, 16 microstep, 25:1 áttétel értékei alapján
   **80000 microstep/kimeneti fordulat** névleges parancsfelbontás, nem
   mért pontosság. A 0,1Nm motor és fokozatonként 0,7 hatásfok feltételezés;
   a 8m/s példaszél **nem teljesíti** az előírt biztonsági tartalékot,
   nem engedélyez ilyen szélben működést, és nem ad biztonságos szélhatárt.
2. **Fedélzeti AP és SGP4-követés**, az RT-3S-től függetlenül.
   Érvényes UTC/hely/TLE és kalibrált észak/szint nélkül nincs érvényes
   követési állítás.
3. **Kézzel segített rádió**, OpenGD77 saját Dopplerével, ha a build
   ellenőrzött; kitalált CAT, PTT-vezérlés vagy feltételezett full-duplex nélkül.
4. **Opcionális, mérésre váró diplexer**, közzétett geometriája:
   [RF-AND-RADIO.md](RF-AND-RADIO.md). Dugónak, rádiónak és koaxhajlításnak
   hagyjon helyet; csatlakozó ne legyen szerkezeti tartó.
5. **Sávonként külön polarizáció.** Hibridet csak sáv, fázis, teljesítmény
   és izolált port ismeretében rendeljen; QCN-3+ 145MHz-re kizárva.
6. **Fizikai blokkoló:** a diplexer karima-/csatlakozómagasságát szerzője
   is becslésnek nevezi. Végső interfész-CAD maradjon paraméteres a valós
   példány tolómérős mérése előtt.
7. **Elfogadási blokkoló:** az új rotor/antenna/RF-hálózat teljes fizikai
   próbája még nem történt. Szimuláció, forrásanyag és CAD nem indokolja
   a „adásra kész” állítást.
8. **Felhasználó választotta licencek:** eredeti szoftver MIT, eredeti
   hardver CERN-OHL-S-2.0. Külső referenciák saját licence megmarad;
   ismeretlen forrás és LibreSat GPL-szoftver nem terjesztett. Mérnöki
   összefoglalója nem tartalmazza azok fájljait. Ebben a fázisban nincs
   távoli közzététel.

### Az autonóm követés feltételei – ne látszat-API legyen

- A **valódi SGP4-propagáció ESP32-n fut** TLE-ből, UTC-ből és helyből;
  a mobil kezelőfelület, nem rejtett pályaszámító. API csak akkor
  implementált, ha teljes út van a bemenetvalidálástól a számításon/
  tervezésen át a biztonságos vezérlésig.
- Hiányzó, hibás vagy elavult óra/UTC blokkolja az automatikus mozgást.
  Kikapcsolás után tárolt GNSS-hely **metaadatos cache**, nem friss pozíció
  vagy új indításkor érvényes fix. Meg kell erősíteni/be kell szerezni a
  helyet/UTC-t és ellenőrizni a TLE korát.
- Földrajzi/valódi AZ és mechanikai AZ nem felcserélhető: észak-offset
  alapján kell átalakítani, és a ±360°-os megfelelő értékek közül csak
  **mechanikai és kábelhatáron belülit** választani. Tilos tiltott szöget
  úgy normalizálni, hogy megengedettnek tűnjön. Tesztelendő 359°→0°,
  nem nulla offset és mozgástartomány-szélek.
- A zenitben a földrajzi azimut szinguláris; ne adjon korlátlan követési
  mozgást. Utasítást el kell utasítani, ha zenithatárt elér/túllép, és
  nincs bizonyított folytonos pálya, sebesség és mechanikai tartalék.
  Geometria/tervező által nem támogatott flip fölötti követést ne állítson.
- Kézi TLE-import kötelező offline működéshez. Automatikus letöltés csak
  **tanúsítvány-ellenőrzéses HTTPS-szel** és válasz/TLE-validálással
  kínálható; teljes körű megvalósítás hiányában el kell hagyni.
  TLS-validálást soha ne helyettesítsen `setInsecure`-rel.
- A tesztek fedjék le a UTC nélküli indítást, érvénytelen UTC-t, restart
  utáni GNSS-cache-t, AZ-offsetet/kábelcsavarodást, zenitcélt,
  követés közbeni érvényességvesztést és hibás importot. AP/API-létezés
  nem helyettesíti ezeket vagy a valódi firmware-fordítást.
- **A latencia biztonsági kérdés:** engedélyezett motorral HTTPS-letöltés
  vagy blokkoló hosszú predikció elutasítandó; elfogadható alternatíva
  csak inkrementális számítás folyamatos kiszolgálással és bizonyított
  leállítási késleltetéssel. Egy 10s-os HTTP-timeout ugyanabban a ciklusban
  megakadályozhatja a STOP/homing/határolók kiszolgálását. Fizikai leállítás
  független felügyeletet és/vagy megfelelő hardveres megszakítást igényel,
  nem várhat a web-handlerre.
- Az előrejelzés a kiválasztott műholdra és korlátozott horizontra terjedjen.
  Állapotlekérdezés ne számolja újra ismételten az egész katalógust, és ne
  indítson letöltést. Katalógus/TLE mérete és kérésenkénti munka korlátozandó.
- Elérhetetlen sebességű, mozgáshatárt vagy zenitkorlátot átlépő cél
  **kifejezett API-hibát** és mozgásmentességet eredményezzen. Szög csendes
  levágása és „sikeres” válasz nem jelenti a cél elérését. Követés közben
  a STOP nem várhat hosszú handlerre.
- A TLE-név és minden importált szöveg nem megbízható bemenet:
  `textContent`-tel vagy egyenértékű escape-pel jelenjen meg, soha ne
  `innerHTML`-ként. Orbitálisan érvényes import sem jogosít markup-injekcióra
  az AP-n.

## 10. A — Új AV2040-adatlap: vizuálisan ellenőrzött összehasonlítás

Az új, helyi, **egyoldalas** `TDS_AV2040.txt` teljes kinyerését elolvastuk;
a betűkódolás miatt hiányzó számok észlelése után a helyi 140dpi-s
`TDS_AV2040-000001.png` oldalt vizuálisan is megvizsgáltuk.
Forrás: **Ultralife/Trivec-Avant, 2010 NOV 23, UBI-05273 REV:-**,
1. PDF-o. A számokat nem a kódolás találgatásával állítottuk vissza.

**A kereskedelmi AV2040 közölt adatai:** 240–400MHz, VSWR 1,5:1,
jobb körpolarizáció, 3dB tengelyarány, 200W CW, 6,5 font (≈2,948kg),
BNC male. Változatonkénti nyereség: AV2040-3 +7,0dBic 240–400MHz;
AV2040-2 +11,0dBic 240–318MHz; AV2040-1 +9,0dBic 240–400MHz.
Ezek a gyártói adatlap adatai, **nem az új 145/435MHz-es terv eredményei
és nem fizikai vizsgálataink**.

**Mindkét célfrekvencia, 145 és 435MHz, kívül esik a 240–400MHz sávon.**
A blog 449.550MHz-e is kívül esik; a blog saját, újrahangolt megvalósítása,
nem a gyári termék sávbővítésének bizonyítéka. Az adatlap leírja/mutatja
az összecsukhatóságot/manpack kialakítást, de **nem ad nyitott/összecsukott
méretet vagy táskatérfogatot**, és nem határozza meg, mit tartalmaz a tömeg.
A fotóból méretet vagy CG-t nem vezetünk le.

A hordozhatóság/összecsukhatóság ésszerű funkcionális követelmény, de
145/435MHz-hez saját antenna, polarizáció és tartó tervezése/mérése szükséges.
Ne örökölje a kereskedelmi termék 200W, 3dB tengelyarány, 7/9/11dBic,
2,948kg vagy rotor-terhelési adatát. A gyártó szerint az adatok tájékoztatók,
nem teljesítménygaranciák, változhatnak. Ismeretlen licencű külső OBJ/STL
**nem terjesztett**; az új terv eredeti geometriájú, a koordinátor kezeli
a metaadatokat/hozzájárulást. Méretblokk továbbra is nyitott, mert az adatlap
nem ad méretet, nem azért, mert a kép olvashatatlan.

A koordinátor helyi metaadat-ellenőrzése a `tinker.obj` fájlban 10416
csúcsot/20964 lapot/1 objektumot, a bináris STL-ben 20964 háromszöget talált.
A burkoló 194×115,798×33 **ismeretlen egységben** egyezik. A nyomon követési
SHA-256 a SOURCES fájlban van. Ezt a háló/darabok elrendezésének dobozát
nem tekintjük összeszerelt antenna méretének, összecsukási méretnek vagy
milliméter-skálának. A vizsgált OBJ/MTL-fejlécekben licenc nincs megadva;
geometria nem kerül származtatott tervbe.
