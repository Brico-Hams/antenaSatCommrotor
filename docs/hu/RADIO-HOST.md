# Önálló Linux rádiógazdagép — befagyasztott v1 szerződés

## Kifejezett, moduláris üzemeltetési profilok

A rádió-SDR, a rotor és az antenna egymástól függetlenül használható modulok. Az integrált összeállítás CM5 IO+AUX+2 Lime Mini; a szándékosan konfigurált önálló rádió egy vagy két valódi Mini eszközt használhat. Egy eszköz hiánya sem változtatja meg automatikusan az összeállítást vagy az üzemeltetési szabályzatot.

Az alapértelmezett `--operation-profile INTEGRATED_TRACKING`. Ehhez a tényleges integrációnak az összes meglévő fizikai/RF/kapcsolati/bérleti reteszt **és** az érvényes, friss GNSS/SGP4-adatot, valamint az igazolt rotorbiztonságot/-kalibrálást is biztosítania kell. A követés elvesztése letiltja a TX-et; soha nem kapcsol át kézi módra.

A `--operation-profile STANDALONE_MANUAL` kifejezett, helyileg beállított indítási szabályzat, `--rotor` nélkül. Névlegesen, kézi Hz-hangolással működik, **Doppler-korrekció nélkül**, GNSS és rotor nélkül. Ettől függetlenül valódi SDR-kész állapotot, fizikai felfegyverzést/PTT-t, nyugtázott és egészséges RF-útvonalat/polarizációt, hitelesített hangmunkamenetet és legfeljebb 500 ms-os bérletet követel. TX előtt minden hitelesített munkamenetben kifejezetten meg kell erősíteni a profilt a `/profile` útvonalon: `{"profile":"STANDALONE_MANUAL","confirm":true}`. A telefon nem írhatja felül a helyileg konfigurált profilt; újracsatlakozáskor a megerősítés visszavonódik. A kézi mód soha nem a követésvesztés tartaléküzeme.

Hardver használatakor a `--radio-count 2` mindkét kifejezett, egyedi sorozatszámot megköveteli. A `--radio-count 1 --single-channel VHF` (vagy UHF) önálló kézi módot és pontosan az adott csatorna sorozatszámát igényli; a másik sorozatszámot el kell hagyni. Nincs automatikus elsőeszköz- vagy eszközhiányos tartalék. Egy rádiónál a hangindításban az egyetlen elérhető csatornát kell megadni mind `rxChannel`, mind `txChannel` értékeként; két rádiónál a kereszt-sávos kiválasztás továbbra is kifejezett. Az egy rádiós RX/TX külön frekvencia-visszaolvasással/LO-val rendelkezik, és megtartja az egyszerre egy TX szabályt. A `/status` az `operationProfile` és `availableChannels` mezőkkel bővül; a profilok csak ténylegesen konfigurált csatornákat tartalmaznak, kitalált második eszközt soha.

Az önálló RX-hez nem kell GNSS, rotor vagy TX-üzembehelyezés, de szükséges a kiválasztott valódi SDR, mintasebesség, USB-erőforrások, valamint a Linux-hang/BLE előfeltételei. A csak rotoros telepítés a rotor-szolgáltatást futtatja, **nem** a `radio.main` modult, és nem igényel Soapy-bővítményt/-importot. A rádiócsomag csak `--rotor` megadásakor indít rotort; önálló érzékelő- vagy mozgásműködést nem állít. Az önálló antennahasználathoz külön ellenőrzött tápvonal/hálózat/mechanika szükséges. Az integrált összeállításhoz külön ellenőrzött rotoradapter, GNSS/kalibrálás, RF-útvonal, BSP/NC vészleállító/watchdog, valamint minősített USB-/hangtáp-topológia kell; ez az útmutató nem állítja, hogy ezek üzembe vannak helyezve.

Ez az **eredeti** alrendszer önálló hatókörű: **Raspberry Pi Compute Module 5 (CM5), Linux ARM64** vezérli a háromtengelyes rotort, a rádiót és a hangot a **megvásárolt hivatalos CM5 IO panelen és saját kiegészítőpanelen** keresztül; nem teljesen egyedi, nagysebességű CM5-hordozópanelről van szó. A kiválasztott rádió **két cserélhető LimeSDR Mini eszköz**, nem Lime + RTL-SDR V4 (az RTL csak vételre alkalmas). Mindkét lánc adásképes és egyidejű VHF/UHF-vételt biztosít; egyszerre **csak egy adás** engedélyezett. ESP32 nem szükséges. A meglévő ESP32 firmware/GATT 0.2.0-s verziója **örökölt**, változatlan. A `radio-host/1.0.0` külön rádió-API marad akkor is, ha a rádió és a mozgásvezérlés egy számítógépet használ; ugyanaz a natív Android APK külön rádiószolgáltatási szerződést használ. Ez az alrendszer nem módosít Androidot, örökölt firmware-t, mozgásvezérlési megvalósítást vagy Gerber-fájlokat.

## Ellenőrzési határ / kiadást blokkoló feltételek

Az offline DSP, reteszelések, vezetékes keretezés, diszpécser, localhost CAT és API-adapter tesztjei futtathatók. A fizikai RF, tényleges egyidejű RX/TX, Linux GPIO-vezetékezés, Linux BlueZ-párosítás/MTU/értesítések, antenna/szűrő/diplexer/izoláció, RF-kimenő teljesítmény és Android-együttműködés **NINCS IGAZOLVA**. A CM5 és két LimeSDR Mini kiválasztott architekturális erőforrás, nem fizikailag validált hardver. RF-adás nem történt. Sem az FM-only modulok, sem a módosított Pluto-frekvenciatartományok nem bizonyítják a 145 MHz-es/SSB-támogatást. Csak a tényleges Soapy-modulfelderítés és a meghirdetett frekvencia-/mintavételi tartomány fogadható el.

A TX nem érhető el addig, amíg egy **ellenőrzött követési forrás** nem szolgáltatja a tartománysebességet, a helyet és az UTC-időt. A `TrackingInput` átviteli módtól független határfelület: később a helyi Pi SGP4 közvetlenül hívhatja, vagy egy hitelesített upstream adapter teheti meg a forrás ellenőrzése után. A helyi integráció a forrásazonosítókat `TrackingInput.provision(source)` hívással engedélyezi, mintákat pedig `update(source, rangeRateMps, utc, site)` hívással küld be; az elutasítás/visszavonás törli az állapotot és letiltja a TX-et. A proveniencia e rádióhatáron kívül állapítandó meg, nem következtethető ki a forrás nevéből vagy távoli kérésből. Az Android hang-tokenje önmagában nem igazolja a pályaadatok provenienciáját. A `Dispatcher.tracking_input` ugyanazt a határt használja a `/tracking` útvonalhoz; tetszőleges BLE-kliensek továbbra is nem megbízhatók. Itt nem vezetünk be SGP4-számítást vagy átviteli adaptert. Szándékosan nincs olyan CLI-kapcsoló, amely ezt a blokkolást megkerüli.

Az RX pálya-/követési bemenet nélkül működik. A belső mikrofon/hangszóró, valamint a Kenwood K1 elektromos bekötése az igazolt hardverre vár. Bluetooth HFP/A2DP-t nem állítunk: ez kizárólag átlátszó, kétirányú GATT PCM.

A CM5 CPU-tartaléka, USB-topológiája/átbocsátása, valamint az egyidejű SDR/hang/mozgás működés **fizikailag nincs ellenőrizve**. A Pi4/Zero/Zero2 nem az irányadó alap. A mozgásintegráció külön feladat: nem állítjuk, hogy a Linux GPIO lépésimpulzus-időzítése megfelelő. A TMC5130/5160 SPI belső rámpagenerálása, az alaphelyzetben zárt fizikai vészleállító és a független hardveres watchdog értékelés alatt áll; ezt a rádióalrendszer nem valósította meg és nem hagyta jóvá. Az új CM5 hordozópanel és az integráció külön munka; sem régi két tengelyes, sem ESP32-panel feltételezés nem érvényes.

Az **5 kg-os maximum a külső akkumulátort nem tartalmazó teljes állomásra** vonatkozik, nem csak a rotorra: az állványt, rádió-/RF-hardvert, SBC-t, háromtengelyes rotort, antennát, burkolatokat, kapcsolókat, csatlakozókat és **minden kábelt** fel kell venni a szülői tömegnyilvántartásba. Az SBC/radio szerelvény tömegét itt nem mérték meg és nem hagyták jóvá. A CM5 két LimeSDR Minivel kiválasztott; ez a szoftver nem igazolja feldolgozási/BLE/USB-kapacitását, és azt sem, hogy a teljes állomás megfelel a tömeghatárnak.

A megosztott SBC érzékelőkövetelményei kifejezetten tartalmazzák a **GNSS UTC-időt és helyet**, a **kalibrált, deklinációval korrigált valódi irányt adó iránytűt**, az **IMU dőlésszögét**, valamint **mindhárom tengely enkóderét**. Az érzékelő-illesztőprogramok, kalibrálás, deklinációs modell, telepítés/igazítás és mért enkóder-visszajelzés külön, jövőbeli Pi-integrációs munkakörbe tartozik. A csatlakozók vagy forrásazonosítók nem bizonyítják, hogy ezek az érzékelők léteznek vagy megfelelően működnek.

A helyileg megbízhatónak tekintett követési adapternek a Doppler-minták beküldése előtt ellenőriznie kell a **friss GNSS-helyet/UTC-t és az érvényes, aktuális SGP4-állapotot**. Ez a rádióhatár ellenőrzi a véges/tartományon belüli hely- és tartománysebesség-értékeket, az UTC-eltérést és a monoton mintakorokat; a GNSS-fix minőségét, SGP4-érvényességet vagy az érzékelőadatok provenienciáját önmagában nem tudja igazolni. Ha a GNSS-hely/UTC vagy az SGP4-állapot érvénytelenné válik, az integrációnak azonnal vissza kell vonnia a forrást, nem pedig nulla helyet, nulla tartománysebességet vagy szintetikus UTC-t használnia tartalékként. A 0° szélesség/0° hosszúság érvényes földrajzi koordináta, nem érvénytelen önmagában; a fix érvényességét a GNSS-adapternek kell megadnia, koordinátákból nem szabad kikövetkeztetni. A visszavonás törli a követési adatokat és tiltja a TX-et; a lejárat külön is tiltja a Doppler-TX-et. Az RX visszatérhet névleges frekvenciára anélkül, hogy érvényes követést állítana. Ez a rádiós munkakör tényleges érzékelőadat-beszerzést nem valósít meg.

Az állomás valamennyi **RF-csatlakozása szabványos, 50 Ω-os SMA legyen, ne RP-SMA**, beleértve a rádió RF-portjait, az antennát/táplálóhálózatot és az RF-polarizációs kapcsoló összeköttetéseit. A csatlakozónem és a kábelhosszak a hardver igazolt kiválasztásától és a teljes állomás tömegnyilvántartásától függenek. Ez a követelmény nem vonatkozik a hangra: a Kenwood K1 mikrofon-/hangszóró-csatlakozása hangaljzat marad, tűkiosztása/elektromos kompatibilitása még ellenőrzendő. A szoftver nem bizonyít csatlakozó- vagy RF-impedancia-kompatibilitást.

## Mintavételi sebességek, DSP- és RF-választások

- Hang: belsőleg normalizált lebegőpontos; BLE-n előjeles S16LE, mono, 8 000 minta/s.
- DSP RF-alapsáv: komplex CF32, 96 000 minta/s, egész ×12 hangkonverzió. A valós hardversebesség alapértéke **1 000 000 minta/s**, `--hardware-rate` kapcsolóval 192k..4M tartományban állítható. **Mindkét eszköz hirdetett RX/TX-tartományának és pontos visszaolvasott mintasebességének egyeznie kell a kért sebességgel**. Az 1 MSPS kért konfiguráció, nem állítás arról, hogy a fizikai hardver ténylegesen alkalmazta. Folyamatos racionális interpoláció, megőrzött egész órajel-számlálókkal és 257 csapú aliasgátló FIR-szűrővel alakítja a 96k↔hardversebességet, megőrizve a blokkok folytonosságát. Egy mintányi előretekintés megmarad; csenddel történő kitöltés nincs.
- Kiválasztott háttér-illesztő: SoapySDR **LimeSuite/Lime** illesztőprogram, a VHF/UHF-profilhoz felderített fizikai LimeSDR Mini egységenként. A LimeSDR Mini 2.x névleges specifikációja 10 MHz–3,5 GHz, egy RX/egy TX, független LO-val és natív szabványos SMA-portokkal. Ezek a névleges specifikációk **nem helyettesítik a tényleges felderítést, pontos eszközazonosítást, meghirdetett tartományokat, teljes duplex jelzőket, mintasebesség-támogatást vagy hangolási/sebesség-visszaolvasást**. Minden profil RX/TX-éhez a pontosan felderített sorozatszámot válaszd, ne egy általános másik Lime eszközt. Éles üzemben kötelező a nem üres és különböző `--vhf-serial` és `--uhf-serial`. A felderítésnek sorozatszámonként pontosan egy `driver=lime` Mini eszközt kell azonosítania; hiányzó, duplikált vagy kétértelmű kiválasztás hibával leáll, nem választja ki az első eszközt.
- Beszéd-aluláteresztő: 129 csapú, Hamming-ablakos sinc, 3 kHz. USB: pozitív frekvenciájú analitikus jel 513 csapú Hilbert-transzformációval és illesztett 256 mintás késleltetéssel TX-en és RX-en (az RX elutasítja a nem kívánt negatív frekvenciájú oldalsávot). AM: `0.5*(1+0.8*audio)` vivőburkoló, burkolódetektor lassú vivőkövetéssel. FM: folytonos fázis, ±2 500 Hz löket és konjugált fázisdiszkriminátor. A hangkimenet DC-blokkolója körülbelül 30 Hz-es.
- Az RF normalizált csúcshajtása **0,1-re** van korlátozva; a TX-erősítés a meghajtó által hirdetett minimumra áll be, nem találomra feltételezett wattértékre. Ez **nem** mért teljesítményhatár, jogi adási engedély vagy PA-védelem.
- Kezdeti névleges/hangolt RF-sávok: beleértve a 144–146 MHz-et és 430–440 MHz-et, csak kereszt-sávú, kiválasztott hang RX/TX. Minden VHF/UHF-eszköznek saját RX/TX adatfolyama és LO-visszaolvasása van; **mindkét RX-munkaszál egyidejűleg fut**. Minden munkaszál erőforrás-korlátos, 8 blokkos sorral és 10 ms meghajtó-olvasási időtúllépéssel rendelkezik; túlcsordulás/olvasási hiba kifejezett hibát okoz, IQ-csenddel történő tartalék nincs. Mindkét RX-sort folyamatosan fogyasztja a rendszer, implicit hangkeverés nélkül. A kiválasztott RF-háttér két cserélhető LimeSDR Mini, tényleges eszköz-/sebesség-/teljesduplex-ellenőrzéstől függően.

1 MSPS CF32 alkalmazási puffereknél két RX-adatfolyam összesen 16 MB/s-ot, egy TX-adatfolyam további 8 MB/s payloadot jelent, az eszközvezeték-formátum, USB-többlet és feldolgozás nélkül. Ez számtan, **nem mért USB-kapacitás**. A hivatalos CM5 IO panel/minősített hub/táp-topológia, tartós egyidejű átvitel, ARM64 DSP/BLE ütemezés és hőviselkedés továbbra sincs ellenőrizve. A pufferkapacitás erőforráskorlát, nem a megszakításmentes vétel garanciája.

Mindkét Lime eszköz natív USB3-csatlakozást használ. Egy további USB-hangeszközhöz minősített hub/USB2-gazdatopológia vagy külön validált hangalternatíva szükséges. Az I2S-vezetékezés ütközhet az SPI1 mozgás-erőforrásaival; ez a rádiós megvalósítás nem talál ki tűkiosztást, USB-port/hub minősítést vagy I2S-megoldást. A BSP, NC vészleállító és független watchdog üzembe helyezése továbbra is kötelező akadály a fizikai TX jóváhagyása előtt. Az éles hardversebesség kért értéke 1 MSPS (elfogadott konfigurálható tartomány 192k..4M, tehát 100k fölött); a 96k **csak belső DSP-órajel**, nem állítás Lime hardversebességről vagy régi egyeszközös konfigurációról.

- `rangeRateMps > 0` távolodást jelent; közeledés negatív. `RX=baseRX-round(baseRX*rangeRate/c)`, `TX=baseTX+round(baseTX*rangeRate/c)`; `c=299792458 m/s`. Mindkét eltolás és hangolás-visszaolvasás egész Hz-et használ. Az igazolt sebesség 1 másodperces monoton korminőség vagy 2 másodpercnél nagyobb UTC-eltérés után lejár. A véges műholdsebesség ±12 000 m/s-ra korlátozott, érvényes helyszélesség/hosszúság/magasság szükséges. GNSS-adatot nem szintetizálunk. Elavult követési adat esetén az RX névleges frekvenciára áll vissza, a TX pedig letiltódik.

Rádión keresztüli automatikus hangolás nincs: CAT/alapfrekvencia/üzemmód/tényleges Doppler újrahangolása előbb deaktiválja a TX-et és visszavonja a bérletet. Új bérlet szükséges. A folyamatos Doppler-frissítések ezért megszakíthatják az adást; ezt ne kerüld meg úgy, hogy aktív adatfolyam frekvenciáját módosítod.

A LimeSDR Mini névleges kisjelű kimenete körülbelül **legfeljebb 10 dBm**, nem 5 W. A kívánt, üzembe helyezéskor mérendő rendszerkimenet **5 W FM**, **5 W PEP USB** és **1 W AM vivő**. Ezek tervezési célok, nem elért/mért kimenet vagy szoftveres ígéret. Megfelelő lineáris PA, üzemmódfüggő meghajtás/bias, szűrés, izoláció/duplexelés, hővédelem és mért RF-minősítés szükséges. A szoftveres hajtásamplitúdó-korlát **csak olvasható, 0,1-es normalizált IQ-limit**, minimális hirdetett TX-erősítéssel; nem wattbecslés, kalibrálás vagy PA-vezérlés. A külső PA üzembe helyezése jövőbeli hardvermunka. Indítás/felderítés/sebességkonfiguráció soha nem aktiválja automatikusan a TX-et; minden retesz továbbra is szükséges.

A külön kezelt CM5 `RotorController` integrációtól várható az igazolt autonóm SGP4/GNSS-követés és háromtengelyes biztonsági állapot szolgáltatása. Konkrét mezőit/adapter-szerződését ez az alrendszer **nem feltételezi**; a szülői koordináció befagyasztja azokat adapter hozzáadása előtt. Addig az átviteltől független `TrackingInput` és `Safety.rotor_update` határfelület elérhető, de éles CLI-ben nincs engedélyezve, ezért a TX tiltott marad.

### Előkészített `--rotor` gazdaintegrációs kapu (bekötés függőben)

A `--rotor PATH` a `{"v":1,"controllerConfig":"relative-or-absolute-path"}` objektumot olvassa. Tetszőleges Python-modul, mock-választó vagy üzembehelyezési felülbírálás nem fogadható el. Az előkészített betöltő a rögzített helyi `rotor.radio_adapter.open_adapter(controllerConfigPath)` modult és az `snapshot()`, `dispatch(path,op,data,authenticatedPeer)`, `disconnect(authenticatedPeer)`, `close()` metódusokat követeli meg. **Ezek javasolt bekötési követelmények, nem állítások a meglévő RotorController nyilvános metódusairól.** Hiányzó modul/gyár/metódus esetén a kifejezett integráció hibával leáll; nincs tartalék megoldás. A szülőnek kell biztosítania/megerősítenie a tényleges adaptert, mielőtt végpontok közötti működés állítható.

Snapshot-séma: `sampledMonotonic` (azonos gazdagép monoton másodpercei), `hardwareCommissioned:true` (tényleges háttér-illesztő tanúsítása, nem konfiguráció), `gnssValid:true`, `sgp4Valid:true`, `fault:null` (vagy hiba-karakterlánc), `rangeRateMps`, `utc` Unix-másodperc, `site:[lat,lon,heightM]`. Legnagyobb snapshotkor 200 ms; lekérdezés 50 ms-onként, határidő 200 ms. A régi időbélyegek nem frissülnek pusztán lekérdezéstől. Érvénytelen GNSS/SGP4/BSP/watchdog/rotorállapot visszavonja a követést/TX-et. Ez az előkészített átviteli réteg nem bizonyít hardverhitelesítést és nem valósít meg tényleges érzékelőket.

A hitelesített rádiós munkamenet-azonosító változatlanul jut át az adapterhez, a régi ESP32-munkamenetektől elkülönítve. A javasolt új CM5-névterű útvonalak megőrzik a v1 borítékot: `/rotor/status` get, `/rotor/stop` set, `/rotor/target` set, amely **mindhárom** véges `azDeg`, `elDeg`, `polDeg` mezőt megköveteli (nincs hiányzó POL-/két tengelyre visszaeső alapérték). A `/rotor/track` elutasított, amíg a tényleges vezérlő payload-szerződése nincs meg. A tényleges úthatárokat/követési payloadot és a régi kompatibilis útvonal-aliasokat a szülőnek a valós RotorController-metódusok alapján kell befagyasztania; ismeretlen, feltételezett régi útvonalakat el kell utasítani. A válaszoknak `schema:"cm5-rotor/v1"` sémát és kifejezett AZ/EL/POL tengelyállapotot kell azonosítaniuk; a rendszer soha nem állíthatja, hogy ESP32 firmware 0.2.0, és a POL-t nem azonosíthatja CP-kéziséggel. Ez a munkakör nem talál ki igazolt mechanikai POL-tartományt.

## Biztonság / fizikai integráció

Indításkor a rendszer hatástalanított, adásra nem kulcsolt, munkamenet és bérlet nélküli, az SDR pedig nem kész állapotú. A GPIO felfegyverzési bemenet és a helyi fizikai PTT két **különálló**, aktív magas szintű gpiod v2 bemenet, lehúzással. Egy harmadik aktív magas kimenet vezérli a **külső, normál állapotban kikapcsolt RF-kaput**. Távoli parancs egyik fizikai bemenetet sem állíthatja be.

Minden TX feltétele: hitelesített, csatlakoztatott hangmunkamenet; fizikai felfegyverzés; fizikai PTT; a helyileg beállított üzemeltetési profil feltételeinek teljesítése (az `INTEGRATED_TRACKING` profilban friss, ellenőrzött követés és mozgásbiztonsági állapot, a `STANDALONE_MANUAL` profilban munkamenetenkénti kifejezett megerősítés); tényleges sikeres RX-olvasás és beállított TX-adatfolyam; érvényes kereszt-sávú frekvenciák, illetve egy rádiónál az engedélyezett egycsatornás útvonal; le nem járt bérlet; nyugtázott/beállt RF-polarizáció. A kézi mód nem követésvesztési tartalék, és egyik profil sem írhatja felül a fizikai/RF/kapcsolati reteszeket.

### Befagyasztott A revíziós gyártási rádiókérések — hardveres TARTÁS

A `hardware/cm5/interface.json` a mérvadó és változatlan. A
`RadioGPIOProduction` gyártási adapter **kizárólag a BCM22 VHF PTT-kérésért
és a BCM23 UHF PTT-kérésért felel**. A közös, 0x20 című MCP23017-et úgy
olvassa, hogy **nem konfigurálja és nem írja a motor-/enkóder-GPIO-kat**:
BANK0 szükséges, a GPA4..7 bemenet kell legyen. A GPA4 =
`PTT_VHF_FEEDBACK_N`, a GPA5 = `PTT_UHF_FEEDBACK_N` különálló
érintkező-/érzékelőbemenet; a GPA6/7 aktív alacsony PA-hibabemenet. Minden
`_N` végű jel alacsony szinten aktív; a külső felhúzás/nyitott
visszajelzés nem ad engedélyt. Kérés előtti beragadt visszajelzés, mindkét
visszajelzés aktív állapota, PA-hiba, hibás irányú/bankú GPIO vagy I²C-hiba
mindkét kérést inaktívvá teszi. A kimeneti kérés visszaolvasása **nem
hardveres engedély**, és soha nem RF CP-nyugta.

Egy élő, független külső őrnek kell tanúsítania a ténylegesen üzembe
helyezett áramkört, a helyi fizikai felfegyverzést/PTT-t, az NC
vészleállítót, a watchdogot és az RF-út állapotát; az adat monoton
időbélyege legfeljebb 50 ms régi lehet. A konfiguráció root tulajdonú,
mások által nem írható, és kifejezett üzembe helyezést igényel, de
**önmagában ez a jelző nem igazolja a hardverbe vetett bizalmat**.
A `radio/gpio-hold.example.json` szándékosan
`hardwareCommissioned:false` értéket tartalmaz. A
`--radio-gpio PATH --gpio-contract PATH` hibával, biztonságos leállással
zár, mert a fizikai külső őr szolgáltatója/áramköre még nincs megvalósítva.
Nem válthat csendben általános GPIO-útra; a `--gpio-chip` egyidejű
megadása elutasított. A fizikai üzembe helyezés előtt a szülőnek kell
bekötnie az ellenőrzött, közös BSP-őrt. CP-kapcsoló-tűk kiosztását nem
találjuk ki.

A kétláncos adapter képes ezt az őrt használni, és az SDR TX-aktiválása
előtt független PTT-visszajelzést követel, amelyet minden védett íráskor
újraértékel. A Stop először mindkét GPIO-kérést elengedi, akkor is, ha az
egyik eszközmeghajtó hibázik. A lekérdezés és a Python-határidők nem
helyettesítik a független hardveres kaput/watchdogot. **Ez gyártási adapter
kódja, kizárólag teszt-I/O-val ellenőrizve; nem kiadott vagy fizikailag
igazolt biztonsági hardver.**

### Az RF-polarizáció nem a mechanikai POL-forgatás

A megerősített harmadik rotormotor **korlátozott úton mozgó, tengelyirányú POL-forgatás**. A jelölt ±90°-os mechanikai tartomány továbbra is TBD; folyamatos forgatást vagy mozgáspanel-tűkiosztást nem feltételezünk. A tengely körüli forgatás **nem változtatja meg** a körpolarizáció kéziségét. RHCP/LHCP-hez külön RF-kapcsoló/hálózat és kompatibilis körpolarizált antenna szükséges.

Az RF-enumok: `LINEAR`, `RHCP`, `LHCP`. Egy mód sem hirdethető meg vagy jelenthető konfiguráltnak, ha az antenna/hálózat/kapcsoló képességét helyileg nem ellenőrizték. Az alapértelmezett futtatókörnyezetben **nincs jóváhagyott RF-kapcsoló-adapter**, ezért a képességlista üres, a konfigurált állapot null, a TX pedig tiltott. Ez kiadási blokkolás, nem szimulált siker. A `PolarizationSwitch` előbb visszavonja a bérletet és sikeresen leállítja a TX-et, majd a kapcsolási írások előtt tényleges TX-ki nyugtát követel. A helyileg integrált `GPIOAcknowledgedSwitch` valódi gpiod kimeneti vonalakat és **független érintkező/érzékelő bemeneti vonalakat** használ, ellenőrzött igazságtáblával és mért beállási idővel; a kimeneti latch visszaolvasása nem elegendő. A helyileg megadott TX-ki visszajelzési callbacknek az RF-kapu/SDR kikapcsolt állapotát kell ellenőriznie, nem csupán visszaadnia a szoftver által kért állapotot. A konfigurált érték null marad, amíg le nem jár a beállási idő **és** a visszajelzés nem egyezik. Visszajelzés-eltérés/-vesztés ugyanazon bérlet-/kapu-watchdogon keresztül tiltja a TX-et. A kapcsolókérés nem újítja meg automatikusan a PTT-t.

A mozgásintegrációnak ellenőrzött helyi biztonsági forrásból `Safety.rotor_update(fault, verified=True)` értéket kell szolgáltatnia; `fault=null` csak egészséges állapotban lehet, az adatot pedig 500 ms-on belül frissíteni kell. Ismeretlen/nem megbízható/elavult állapot vagy bármely rotorhiba blokkolja a TX-et; a vészleállító/watchdog/meghajtóhibákat itt meg kell jeleníteni. BLE-kliensek nem jelenthetik egészségesnek a rotort, és nem létesíthetik ezt a bizalmi kapcsolatot. A háromtengelyes meghajtóintegráció, fizikai NC vészleállító-vezetékezés és független watchdog ellenőrzése külön feladat.

A bérlet 1–500 ms; az Androidnak legfeljebb 200 ms-onként kell megújítania. Elengedés, szétkapcsolás, hibás/hiányos PCM, sor-/kredit-hiba, hangleállítás, CAT-időtúllépés/szétkapcsolás, SDR-időtúllépés/rövid írás/aktiválási-deaktiválási hiba, elavult követés/bérlet vagy GPIO-hiba visszavonja a TX-et. 50 ms-ot meghaladó PCM-éhezés szünetelteti a TX-et; nullákkal nem gyártunk hangot. A nem kulcsolt állapotban beérkező mikrofonkeretek eldobódnak, és későbbi PTT-nél nem játszódnak vissza.

A független GPIO-watchdog 10 ms-onként lekérdez, és a meghajtóleállítás előtt eldobja a fizikai kaput. A meghajtó olvasási/írási időtúllépése 10 ms. Az ütemezés, operációsrendszer-hiba vagy elakadt natív meghajtó nem biztosít kemény valós idejű biztonságot: a fizikai TX-jóváhagyás előtt **kötelező a külső, alapállapotban kikapcsolt kapu + hardveres watchdog + igazolt kioldó-vezetékezés**. A Linux-folyamat kilépése önmagában nem megbízható elektromos kapu. A unit tesztek nem bizonyítják, hogy az RF ténylegesen leáll.

## Bluetooth GATT v1 szerződés (befagyasztva)

Az alábbi UUID-k mind különböznek a rotor UUID-itől:

| Cél | UUID | Tulajdonságok |
|---|---|---|
| Szolgáltatás | `c8201001-4e53-4253-9000-000000000001` | elsődleges |
| Control RX (gazdagép → Android) | `c8201002-4e53-4253-9000-000000000001` | notify/read |
| Control TX (Android → gazdagép) | `c8201003-4e53-4253-9000-000000000001` | write with response |
| Audio RX (gazdagép → Android) | `c8201004-4e53-4253-9000-000000000001` | notify/read |
| Audio TX (Android → gazdagép) | `c8201005-4e53-4253-9000-000000000001` | write with response |

A BlueZ a valódi `GattService1`, `GattCharacteristic1`, ObjectManager és `LEAdvertisement1` objektumokat exportálja a **rendszer D-Buszon**, regisztrálja a GattManager1/LEAdvertisingManager1 szolgáltatásokat, és `PropertiesChanged` eseményt küld a Value változásakor. A Linux-adapternek támogatnia kell a periféria módot. Párosítás/kötés az operációs rendszer biztonságos, hitelesített párosításával (MITM/passkey vagy numerikus összehasonlítás) történjen; a `encrypt-authenticated-write/read` karakterisztika-jelzőket a BlueZ kényszeríti ki. Csak egy előre engedélyezett Device1 útvonal csatlakozhat, bonded/paired/trusted/connected állapotban. Második kapcsolat megszakítja az adatfolyamokat. Nem létező `Encrypted` Device1 tulajdonságból ne következtess titkosításra; a hitelesített biztonsági jelzők jelentik a biztonsági határt. A hagyományos Just Works párosítás elégtelen lehet.

A vezérlőcsomag pontosan 20 bájt:
`magic[0]=0x53`, `flags[1]`: 0. bit START, 1. bit END, más bitek nullák;
`sequenceLE16[2:4]`; JSON UTF-8 töredék `[4:20]`.
Üzenetenként egy szekvenciaszám van, minden töredék azonos szekvenciát használ;
a végső nulla-padding csak az újraösszeállítás után távolítható el. A JSON maximum 4096 bájt. Interleaving, túlcsordulás és szekvenciaeltérés elutasítva. A töredezés formátuma azonos egy 20 bájtos rotorcsatornáéval, a szolgáltatás/API nem azonos.

Kérések:
`{"v":1,"id":"client-unique-id","path":"/status","op":"get","data":{}}`

Válaszok:
`{"v":1,"id":"client-unique-id","path":"/status","ok":true,"data":{},"error":null}`

Az események `id:"event"` azonosítót és ugyanezt a válaszburkolatot használják. Hitelesítési token nem kerül válaszba, státuszba, naplóba vagy a tárolóba.

| Útvonal / művelet | Kérésadat | Válasz / hatás |
|---|---|---|
| `/auth` set | `{"token":"64-hex-private-token"}` | `{"fw":"radio-host/1.0.0"}` |
| `/status` get | `{}` | kötelező `profiles` VHF/UHF kulcsokkal és serial,rxHzReadback,txHzReadback,rxRateReadback,txRateReadback,rxReady,rxReads,queueDepth,fault,txActive mezőkkel; `rxChannel`,`txChannel`,`txPolicy:"ONE_TX_ONLY"`, továbbá névleges/tényleges Hz, mód, reteszek és számlálók |
| `/profile` set | `{"profile":"STANDALONE_MANUAL","confirm":true}` | a helyileg beállított kézi profil kifejezett, hitelesített munkamenet-megerősítése; a kliens nem állíthatja át a helyi profilt |
| `/radio` set | opcionális `rxHz`, `txHz`, `mode`=`FM`/`AM`/`USB` | bérlet visszavonása/hangleállítás, kereszt-sáv ellenőrzése |
| `/rf/polarization` get | `{}` | `{requested,configured,ready,capabilities}`; `configured` null, amíg nincs hardveres beállás/nyugta |
| `/rf/polarization` set | `{"mode":"LINEAR"}` vagy `RHCP`/`LHCP` | TX-ki nyugta, igazolt kapcsolóképesség és beállás szükséges; nincs automatikus PTT |
| `/audio/start` set | `{"rate":8000,"mtu":247,"rxChannel":"VHF","txChannel":"UHF"}` vagy fordított csatornák | `{"rate":8000,"rxStreamId":uint32,"txStreamId":uint32,"txCredits":16,"rxChannel":"VHF","txChannel":"UHF","txPolicy":"ONE_TX_ONLY"}` |
| `/audio/stop` set | `{}` | mindkét PCM-adatfolyam leállítása, bérlet visszavonása |
| `/ptt` set | `{"enabled":true,"leaseMs":500}` | csak minden retesz teljesülése esetén ad bérletet |
| `/ptt` set | `{"enabled":false}` | azonnali tiltás |
| `/tracking` set | `{"rangeRateMps":number,"utc":unixSeconds,"site":[lat,lon,heightM]}` | **csak helyileg engedélyezett, igazolt követési forrás**; korábbi bérlet érvénytelenítése |
| `/audio/credit` event | csak gazdagép-kimenet | `{"txCredits":0..16,"txStreamId":uint32-or-null}` abszolút rendelkezésre álló ablak |
| `/fault` event | csak gazdagép-kimenet | `{"reason":string-or-null,"rxDropped":counter,"txFaults":counter}` |

Iratkozz fel a Control RX-re a `/auth` előtt; hitelesíts, iratkozz fel az Audio RX-re, kérj legalább 247-es kialkudott ATT MTU-t, majd indítsd a hangot. A kérés `mtu` értékének egyeznie kell a **tényleges BlueZ WriteValue opciók MTU-jával**. Ismeretlen/alacsony MTU, nem 8000-es sebesség vagy MTU-változás elutasítva; 8 kHz-es hangot ne állíts 20 bájtos vezérlőkeretekről. A kötés nem helyettesíti a tokent.

**Kötelező, frissített v1 mezők:** minden `/audio/start` kérésben kifejezetten meg kell adni a különböző VHF/UHF `rxChannel` és `txChannel` értékeket. A régi, egy rádióra vonatkozó, e mezőket elhagyó kérések elutasítandók. A hangfejléc/UUID/verzió változatlan; sikeres indításkor minden adatfolyam-azonosító a megadott csatornához kötődik. A kiválasztás módosítása új indítást/azonosítókat igényel, és visszavonja a PTT-t. Az Androidnak a PCM/APRS/SSTV címkézésénél ezt az adatfolyam–csatorna leképezést kell követnie; nem feltételezheti a VHF-et és nem keverheti a folyamokat. A `profiles`/csatorna/`txPolicy` státusz felváltja az elavult egy láncra vonatkozó sémát; a kliens nem következtethet arra, hogy egyetlen kész lánc azt jelenti, mindkettő kész. Mindkét profilt figyelni kell; bármelyik hibája letiltja a globális TX-et.

### Pontosan befagyasztott v1 státuszséma

A `/status` get a standard válaszburkolatban az alábbi adatkulcsokat adja: `fw`, `rxHz`, `txHz`, `mode`, `actualHz` (rendezett `[RX,TX]`), `sdrReady`, `tx`, `physicalArm`, `physicalPtt`, `trackingFresh`, `rfPolarization` (`requested`, `configured`, `ready`, `capabilities`), `rotorFault`, `rotorReady`, `profiles`, `rxChannel`, `txChannel`, `txPolicy:"ONE_TX_ONLY"`, `operationProfile`, `availableChannels`, `driveAmplitudeLimit:0.1`, `fault`, `rxDropped`, `txFaults`, `txCredits`.

Két hardverprofil konfigurálásakor a `profiles` pontosan `VHF` és `UHF` elemet tartalmaz; mindegyik mezői: `serial`, `rxReady`, `rxHzReadback`, `txHzReadback`, `rxRateReadback`, `txRateReadback`, `rxReads`, `queueDepth`, `fault`, `txActive`. Konfigurált hardver nélkül a `profiles` üres és `sdrReady` false — ne adj sikeresnek látszó üres hardverprofilt.

Az irányok a gazdagép nézőpontjából értendők, a `radio/protocol.py` alapján ellenőrizve: **1002 gazdagép→Android vezérlő notify/read**; **1003 Android→gazdagép vezérlő write-with-response**. Audio1004 gazdagép→Android notify/read; audio1005 Android→gazdagép write-with-response. A 1002/1003 korábbi megfordított értelmezését felülírja ez a táblázat és a megvalósítási konstansok. Az UUID-végződések, 1-es keretezési verzió és 16 bájtos hangfejléc változatlan a két rádiós frissítésben.

A hangkeretek fejléce mindkét irányban **16 bájt**:

| Eltolás | Mező |
|---|---|
| 0 | verzió `1` |
| 1 | flag `0` (fenntartott, ismeretlen érték elutasítva) |
| 2–3 | fenntartott LE16 `0` |
| 4–7 | streamId LE32 |
| 8–11 | sequence LE32 |
| 12–15 | sampleIndex LE32 |
| 16… | páros hosszúságú, tömörítetlen PCM S16LE mono |

A payload maximuma `min(actualMTU-3-16,228)` bájt, MTU247-nél legfeljebb **114 minta**; egy mintánál rövidebb csomag elutasítva. Az RX/TX adatfolyam-azonosítók és számlálók egymástól függetlenek, minden sikeres indításkor nulláról indulnak, modulo 2³². A szekvencia csomagonként eggyel, a sampleIndex az adott csomag mintáinak számával nő. Csendes padding, újraküldéses elfedés vagy nullakitöltés nincs.

A TX-küldő minden csomagért egy kreditet használ fel; a kezdeti ablak 16. A kredit-események abszolút pillanatfelvételek; figyelmen kívül kell hagyni a jelenlegi adatfolyam-életciklushoz nem illő `txStreamId` értéket, és a krediteket nem szabad deltákként összeadni. Használj write-with-response írást és sorosított vezérlőtranzakciókat. A TX-sor kapacitása 16; vételi túlcsordulás/lyuk/duplikáció/átrendeződés/hibás adatfolyam-azonosító/hibás fejléc hibát okoz és leállítja a hangot.

Az RX-sor kapacitása 16; túlcsorduláskor nő az eldobott keretek számlálója, az adatfolyam leáll és státusz/hiba jelentendő, nem történik csendes csonkolás. Az értesítések kibocsátásszáma nem bizonyítja, hogy az Android megkapta őket; az Androidnak KÖTELEZŐ ellenőriznie az RX-szekvenciát/sampleIndexet és jeleznie saját veszteségét. Hiba után a hangot kifejezetten újra kell indítani. Egyetlen szolgáltatás sem osztozik a rotor hang- vagy vezérlőállapotán.

A token gazdagépprivát, szabályos fájlban tárolandó; alapérték `~/.local/state/portable-sat-radio/token`, csak tulajdonos számára olvasható jogosultsággal (0600), új létrehozáskor a szülőkönyvtár 0700. A telefonon kívüli, biztonságos provisionálás során titokként védd. Szimbolikus linket/egyéb számára olvasható fájlt el kell utasítani. A Windows unit tesztek nem bizonyítják a POSIX jogosultságkezelést.

## Localhost CAT-részhalmaz

Eredeti megvalósítás, nem firmware-másolat. A TCP kizárólag **127.0.0.1** címre köt, alapértelmezett portja 4532; az ASCII-parancsokat `;` zárja. `FA;` lekérdezi az RX-et: `FA00145900000;`; `FB;` lekérdezi a TX-et; beállítás pontosan 11 decimális frekvenciajeggyel. `MD;`, `MD2;` USB, `MD4;` FM, `MD5;` AM. **Az MD1 LSB nem támogatott**, válasza `?;`. `RX;` letiltja a TX-et. A `TX;` mindig elutasított (`?;`): a CAT nem igazolhatja a BLE-munkamenetet, fizikai bemeneteket vagy bérletet. A nem támogatott/hibás parancsra `?;` érkezik. A sikeres beállítások nem adnak adatot, Kenwood-stílusban. A parancsgyűjtés 256 bájtra korlátozott, a bejövő adat tétlenségi időtúllépése 2 s. A CAT titkosítatlan/helyi, és soha nem távoli hálózati PTT API.

## Telepítés / validálás (globális pip-telepítés nélkül)

Python >=3.11. A külön rádióprojekt setuptools-t használ; nem volt meglévő Python-csomagkezelő. Linuxon a disztribúció csomagkezelőjével telepítsd a disztribúciós SoapySDR Python-kötéseket és a **tényleges eszköz-illesztőprogramot**. A SoapySDR szándékosan nem általános pip/üres függőség. Hozz létre system-site-packages hozzáférésű projekt-venvet, hogy látható legyen a disztribúciós Soapy:

```sh
python3 -m venv --system-site-packages radio/.venv
radio/.venv/bin/python -m pip install -e ./radio
radio/.venv/bin/python -m unittest discover -s tests/radio_host -v
radio/.venv/bin/python -m radio.main --discover
```

A felderítés csak olvasási művelet; a parancs nem aktivál TX-et. Az üres felderítési eredmény üres lista, nem működő hardver. Importhiba/nem támogatott meghajtó/tartomány/sebesség/hiba leállítja a műveletet. Teszt-IQ-háttér CLI-ből nem választható.

Futáskor kötelező a `--peer /org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX`. A fizikai modulok ellenőrzése után a **mindkét** `--vhf-serial` és `--uhf-serial` kapcsolóhoz a pontos, egyedi felderítési sorozatszámot add meg. Sorozatszámok nélkül BLE/CAT futhat, de az SDR-kész állapot hamis marad. GPIO-opciók: `--gpio-chip`, `--arm-line`, `--ptt-line`, `--gate-line`; GPIO nélkül a fizikai arm/PTT hamis marad. A D-Bus-jogosultságok, biztonságos operációsrendszer-párosítás és Linux-telepítés ezen a Windows munkaállomáson nem ellenőrzött.

A tesztek **kifejezetten csak tesztekhez** injektált API-objektumokat, illetve szintetikus IQ/PCM-adatokat használnak; RF-et soha. A teszt FM/AM/USB ismert tónus-visszacsatolási erősítését/korrelációját/frekvenciáját/SSB-oldalsávsáv-elutasítását, streaming blokk-invarianciáját, egész Hz-es Doppler-irányt, kapulejáratot/elengedést/hibákat, keretezést/MTU-t/sor-/kredithasználatot, JSON-hitelesítést és localhost CAT-socketeket. A DSP-tesztek a mért eredményeket és elfogadási tűréseket kiírják. Nincs négyszögjelű FM-helyőrző és sikeresnek látszó hardverszimuláció.

### Rögzített munkaállomási bizonyíték

Windows Python 3.13.14 a `radio\.venv` környezetben; numpy és dbus-next csak ebbe a projektkörnyezetbe telepítve. A VS Code Python-környezet- és teszteszközökkel próbálkoztunk, de ezek nem voltak elérhetők/nem találták meg ezeket az unittest fájlokat; végrehajtható ellenőrzésként a kifejezett venv `unittest` szerepel.

Mind a **45 offline unittest eset sikeres**, többek között előkészített rotorhatár-bizalmi/frissességi/háromtengelyes/munkamenet-tesztek (nem tényleges RotorController-integráció), kettős futtatókörnyezet kiválasztott hang-/egyedi TX-útvonalválasztás, két kifejezett sorozatszám, egyetlen TX-arbitrázs, korlátozott kettős RX-sor hibák, hardversebesség-visszaolvasás, racionális streaming/alias-elutasítás, RF-kapcsoló TX-ki/beállás/visszajelzés/hardver nélküli esetek, rotorhiba/frissesség és átviteltől független helyi követés (ESP32/BLE nélkül), forrásbizalom/visszavonás, PCM-éhezés/nullakitöltés nélküli működés és fizikai kapu a meghajtóleállítás előtti tesztek (kizárólag tesztcélú I/O).

A setuptools wheel `portable_sat_radio_host-1.0.0-py3-none-any.whl` sikeresen buildel (a figyelmen kívül hagyott helyi `radio\dist` buildkimenet). A CLI `--help` és a fordításellenőrzés nem inicializál RF-hardvert.

Ismert 700 Hz-es, 0,45 amplitúdójú PCM → IQ → PCM eset, az első szűrőbeállási szakaszt figyelmen kívül hagyva és determinisztikus mintakésleltetést keresve:

| Mód | Frekvencia Hz | Korreláció | Erősítés | Maradék RMS |
|---|---:|---:|---:|---:|
| FM | 699,429 | 0,999755 | 1,020135 | 0,007186 |
| AM | 699,429 | 0,999704 | 1,020002 | 0,007895 |
| USB | 699,429 | 0,999543 | 1,018134 | 0,009795 |

Elfogadás: frekvenciahiba <2 Hz, korreláció >0,995, erősítés 0,94–1,06, maradék RMS <0,025. A nem kívánt 1 kHz-es USB-oldalsáv elnyomása **63,99 dB TX és RX**, elvárt értéke >25 dB. Ezek digitális mérések, nem analóg RF-tisztasági vagy teljesítménymérések.

További 96k↔1MSPS újramintavételezési eredmények: az 1 kHz-es komplex tónus 1000,000000 Hz-en, 0,999765 amplitúdóval állt elő (frekvenciatűrés 0,1 Hz, erősítés ±0,02); a 100 kHz-es sávon kívüli tónus lefelé mintavételezésből származó alias-elnyomása 66,01 dB (>40 dB). PCM→mód IQ→1MSPS→96k→PCM 700 Hz-es tónus 699,529 Hz-cel állt elő; erősítések FM 1,020141, AM 1,020569, USB 1,018227 (frekvencia ±2 Hz, erősítés 0,94–1,06). A folyamatos egész/felezett blokkok kimenetei 1e-12 pontossággal egyeznek. Ezek a szintetikus tesztek nem mérik a valódi Lime/USB-viselkedést.
