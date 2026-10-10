# PortableSatStation multimódusú rendszer: összeszerelés és konfigurálás

Revízió: 2026-10-10. Ez integrációs útmutató és kiadási kapuk gyűjteménye, nem gyártási rajz, elektromos bekötési terv vagy adási engedély.

## 1. Építési állapot és biztonsági határ

A tervezett állomás a 145/435 MHz körüli amatőr műholdas üzemet célozza FM, AM és USB módban, adás közbeni teljes duplex vétellel, Doppler/CAT-tal, PD120/PD180 SSTV-vel és hívójelek közötti AX.25 Bell 202 AFSK1200 üzenetküldéssel. Ezek rendszerkövetelmények, nem bizonyítékok arra, hogy a megfelelő hardver/szoftver megvalósult.

A kiválasztott sávban, de soha nem két egyidejű TX-szel elérendő kimeneti cél: 5 W FM vivő, 5 W PEP USB és 1 W AM vivő 100%-os szinuszos modulációnál, később minősítendő PA-láncon keresztül. Az AM-cél ideálisan 4 W PEP-nek felel meg; névleges 5 W PEP-lánccal való kompatibilitása a mért linearitástól, szűrőveszteségtől és elegendő torzítás-/headroom-tartaléktól függ. Ezek tervezési célok, nem mért vagy engedélyezett üzemi eredmények. Mindkét LimeSDR Mini kis teljesítményű gerjesztő marad (frekvenciától/revíziótól függően körülbelül legfeljebb +10 dBm), nem állomás-PA. AM/USB esetén a PA topológiája lineáris legyen; e burkolómegőrző módokhoz E osztályú PA-t ne használj. Az akkumulátor-, táp-, biztosíték-, vezeték- és hőkeret pontos alkatrészek és legrosszabb terhelési tényezők mérése előtt nyitott.

A mechanikai cél három vezérelt tengely: azimut (AZ), eleváció (EL) és korlátozott tengelyirányú forgás/polarizációs orientáció (POL). A POL harmadik mechanikai tengely az antenna tengelye körül; javasolt előzetes tervezési védősávja ±90°, de tényleges útja, végállásai, áttétele, motorja, enkódere, kábelútja és homingmódszere **TBD a mechanikai modell és fizikai felülvizsgálat elkészültéig**. A ±90° nem jóváhagyott parancstartomány, és abból ütközőt gyártani tilos. Folyamatos POL-forgás nincs a hatókörben, hacsak egy későbbi terv nem minősít megfelelő RF-forgóátvezetést és további forgó csatlakozásokat; ilyen most nincs kiválasztva vagy besorolva.

A POL mozgása **nem** vált RHCP-ről LHCP-re vagy fordítva. Külön RF-kéziségválasztó szükséges, kompatibilis körpolarizált antennához való, sávfüggő 145 és 435 MHz-es kvadratúra-/táplálási hálózattal. A kiválasztott kapcsolási topológia szándékosan változtassa meg a relatív táplálási fázist/előjelet, vagy használjon erre a célra tervezett, igazolt táplálásút-választó hálózatot. Ne cserélj fel önkényesen antenna-portokat, ne feltételezd, hogy a csatlakozó megfordítása kéziséget vált, és TX közben ne válts RF-állapotot. Az RF-választó független, reteszelt alrendszer, nem a POL-motor funkciója.

Az új architektúra megerősítetten Raspberry Pi Compute Module 5 (CM5), hivatalos CM5 I/O-panel és külön tervezésű segédpanel a három motortengelyhez, érzékelőkhöz, hanghoz és biztonsághoz, továbbá **két cserélhető LimeSDR Mini modul**. A tervezett VHF/UHF vételi utak együtt működhetnek, mindkét modul TX-képes. A biztonsági alapállapot pontosan egy aktív TX-utat enged; két egyidejű adás tilos. A jelenlegi CM5-konfigurációs jelölt vezeték nélküli, 4 GB RAM-mal és 16 GB eMMC-vel; vásárlás előtt igazold a pontos rendelhető SKU-t. A panelrevíziók, a CM5 I/O és a segédpanel közötti összeköttetés, USB-hangút, RF-szűrők/duplexelés/izoláció, RX-hang/csatornaválasztó, lineáris PA, hangkodek, Bluetooth-hangátvitel, csatlakozótű-kiosztás és a segédpanel terve/kiadása **még nincs kiadva vagy teljesen minősítve**. Mindkét LimeSDR Mini natív RF-kimenete kis teljesítményű (frekvenciától függően körülbelül legfeljebb +10 dBm; ellenőrizd a pontos revízió dokumentációját és mérését), nem az állomás kimeneti célja. Külön minősítendő PA-lánccal a feltételes, szűrt kimeneti célok: 5 W FM vivő, 5 W PEP USB és 1 W AM vivő 100%-os szinuszos modulációnál (ideális PEP 4 W). AM/USB lineáris PA-t igényel, nem E osztályút. Fizikailag ellenőrizd az erősítést, szűrőveszteséget, torzítást/headroomot, kibocsátást, hőt, izolációt és vevődeszenzitizációt.

Mindkét RX-csatorna működhet együtt. A Bluetooth-hang egyszerre egy RX-csatornát választ ki; a kettőt nem keveri és nem dekódolja együtt. A TX kiválasztása különálló. A hardveresen kikényszerített retesz legfeljebb egy aktív TX-utat engedjen, és indítás/reset/elavult vezérlés/hiba után mindkét TX-utat letiltva állapotba tegye.

A hivatalos CM5 I/O-panel a megerősített CM5-alap/hordozó; az egyedi segédpanel ettől különálló NYÁK, nem helyettesíti annak nagysebességű interfészeit. A két USB 3 út közvetlenül a két LimeSDR Mini modulhoz van fenntartva. Használat előtt ellenőrizd a fizikai portkiosztást és az egyidejű áteresztést a kiválasztott CM5/I/O-panel-revízión. A hanghoz minősített, táplált USB-hubot vagy dokumentált/konfigurált USB 2 gazdautat kell használni; az út, hubmodell, tápkeret és audioeszköz **TBD**. Ne állítsd, hogy a hub vagy USB-hangút már kiválasztott, bekötött vagy ellenőrzött. Ne feltételezz egyedi nagysebességű USB 3 mezzanine-t a hivatalos I/O-panel helyettesítőjeként. Az interfészdokumentáció és a segédpanel tervének felülvizsgálata/befagyasztása előtt ne rendelj csatlakozótűt, fejlécsort, tápértéket vagy footprintet.

A segédpanelre tervezik a háromtengelyes motor-, enkóder/végállás-, hang- és biztonsági interfészeket. Kapcsolási rajza, a CM5 I/O-panelhez szabályozott összeköttetése, pontos csatlakozó-/fejléc-hozzárendelése, NYÁK-állományai, valamint a JLCPCB BOM- és CPL-exportja még tervezési/kiadási szállítandó elem, nem létező, jóváhagyott gyártási állomány. JLCPCB-megrendelés előtt a BOM/CPL-t ellenőrizd a befagyasztott terv, footprint, forgatás, oldal és pontos gyártói cikkszám alapján. Az 5,000 kg-os állomásmérés tartalmazza a CM5-öt, hivatalos I/O-panelt, segédpanelt, mindkét LimeSDR-t, a kiválasztott USB-/hanghardvert, PA-/szűrőláncot, hőhardvert, árnyékolást és beépített kábeleket. A külső akkumulátorcsomag/BMS tömege az állomási korlátból a legutóbbi utasítás szerint kimarad, de külön mérendő/jelentendő; a teljes akkumulátorrendszer ára beleszámít a projekt költségébe. Ha a töltőt magaddal viszed, az üzemkész állomás tömegébe számít. Ez az architektúra nem bizonyítja a tömegkorlát teljesülését.

A jelenlegi 180×130 mm-es ESP32-hordozópanel és 228×178 mm-es burkolat a régi AZ/EL rotorkontrollerhez tartozik; nem footprint, burkolat, kapcsolási rajz vagy kiadás a CM5/SBC rádiópanelhez. E dokumentum alapján ne vezetékezz és ne rendelj új panelt.

A meglévő hordozópanel CAD- és digitális ellenőrzéssel rendelkezik, de dokumentációja szerint a prototípus nincs szerelve és a gyártási csomag nincs kiadva. A motorok feszültség alá helyezése előtt le kell zárni a stopkapcsoló, tápút, tényleges modulok és más kiadási blokkolók kérdését. A mechanikai CAD és névleges alkatrészértékek sem jelentenek fizikailag összeszerelt állomást. A régi AZ/EL rendszer körülbelül 3,130–3,200 kg-os tömegterve történeti becslés, a rádiót és állványt kihagyta, és nem mért tömeg vagy sikeres megfelelési eredmény az újratervezésre. A teljes, üzemkész állomás megerősített maximuma **5,000 kg**, benne állvány, antenna, mindhárom motor/rotortengely, rádiók, SBC, kábelek, burkolatok és szükséges szerelési/megtartó hardver, de a külső akkumulátorcsomag/BMS tömege nélkül. Az akkumulátorcsomagot/BMS-t külön kell mérni és jelenteni; tömege az összesített hordozott tömeg része marad. A javasolt tervezési cél **legfeljebb 4,500 kg**, 0,500 kg tartalékkal; egyik határ/cél sincs megmérve vagy igazolva.

**Feltétlen leállítási feltételek**

- Ne gyárts, ne ültess be és ne helyezz feszültség alá új multimódusú NYÁK-ot jóváhagyott kapcsolási rajz, pontos modulrevízió/méret, tűkiosztás, védelmi terv és gyártási kiadás nélkül.
- Ne csatlakoztass pusztán külseje alapján kiválasztott hangkiegészítőt, hangszóró-/mikrofon-aljzatot, SDR-t, rádiót, akkumulátort vagy koaxot. A Baofeng/K1 jellegű 3,5/2,5 mm hang/PTT interfész nem SMA RF- vagy tápcsatlakozó. A tartozék tűkiosztása, mikrofonbias, PTT-viselkedés, hangszint és hangszórókimeneti topológia megoldatlan.
- Szerelés közben ne adj. RF-modul, kimeneti szűrő, műterhelés-besorolás, csatlakozó-teljesítménybesorolás és teljes duplex izoláció nincs kiválasztva.
- Bármilyen motorteszt alatt legyen fizikai, reteszelhető motor-tápmegszakító és mindhárom tengelyre függetlenül ellenőrzött, normálisan zárt (NC) leállítási út. A POL-hoz saját korlátozott út és két NC végállás kell; biztonsági reteszként ne hagyatkozz Linuxra, Bluetoothra, Wi-Fire vagy alkalmazásra.
- A szíjhajtású eleváció a motor tápjának megszűnésekor visszahajtható lehet. Táp leválasztása előtt mechanikus parkolócsappal/rögzítővel biztosítsd a mozgó terhet; senki ne álljon alatta.
- Adás alatt soha ne csatlakoztass forró koaxot és ne válts RHCP/LHCP RF-kapcsolót. Ne adj antennára, nyitott portra vagy nem igazolt terhelésre.

## 2. Az állomás elvi összeállítása

Az ábrák **eredeti, elvi illusztrációk**. Nem méretezett CAD-rajzok, fúrási sablonok, paneltervek, kábel-tűkiosztások vagy gyártási exportok.

![FIG-01 ábra: a CM5-alapú, háromtengelyes multimódusú rendszer elvi architektúrája](../diagrams/multimode-architecture.svg)

![FIG-02 ábra: a háromtengelyes állomás alkatrészeinek elvi robbantott ábrája](../diagrams/multimode-exploded.svg)

![FIG-03 ábra: a régi ESP32-vezérlő határai, csak referenciaként](../diagrams/legacy-controller-boundary.svg)

**FIG-01 blokkjelmagyarázat:** a rögzített oldalon található a CM5 és a külön
segédpanel, a két közvetlen USB 3-as LimeSDR-út, az RX-hang és a védett táp;
az USB-hang gazda/hubja még nyitott. Mindkét SDR vételre használható, de
legfeljebb egyetlen TX-út lehet aktív. A 145/435 MHz-es, sávonkénti
RHCP/LHCP RF-út különválik a POL mechanikától. A mozgó oldalon az antenna,
korlátozott POL-forgás, EL-nyereg és AZ-alap van. A hárommotoros, enkóderes,
végállásos interfész, POL-út és kábel-torziós hurok még tervezési kapu;
folyamatos forgás és minősítetlen RF-csúszógyűrű nincs.

**FIG-02 számozott jelmagyarázat:** 1 — állvány/ellenőrzött fém tartó és
másodlagos megtartás; 2 — rögzített fém tálca/adapter; 3 — védett, még
kiválasztandó akkumulátor; 4 — fizikai stop/tápmegszakító, három tengely
lefedése még igazolandó; 5 — jelölt CM5, hivatalos I/O-panel és külön
segédpanel, tűkiosztás TARTÁS; 6 — VHF/UHF LimeSDR Mini pár, két közvetlen
USB 3 kapcsolat, kétsávos RX-cél és legfeljebb egy aktív TX; 7 — hang/
hangszóró/mikrofon és még fejlesztés alatt álló kétirányú Bluetooth-hang,
3,5/2,5 mm csak hang/PTT, nem SMA/táp; 9a — AZ hajtás (BASE koncepció,
összeszerelés nincs tesztelve); 9b — EL-nyereg/hajtás, amelyre a POL tömege
és CG-je is hat; 9c — korlátozott tengelyirányú POL-forgás, úthossza TBD,
a ±90° csupán javaslat; 10 — kompatibilis körantenna és külön 145/435
táplálási utak, axiális arány sávonként/kéziségenként mérendő; 11 —
független RF-kéziségválasztó, hagyományos 50 Ω SMA, csatlakozó-érintkező
ellenőrzése, PTT tiltása → kapcsolás → állapotellenőrzés → TX-engedély;
12 — GNSS-vevő/antenna, hely és UTC, UART/PPS TBD; 13 — távoli iránytű és
alapszög-IMU. Az álló GNSS nem ad irányt, a régi hordozó pedig csak két
enkódert és négy végállást tartalmaz. A narancs szaggatott út korlátozott
POL-torziós hurok, nem folyamatos forgás vagy minősítetlen csúszógyűrű.
Mindkét ábra koncepcionális: nem méretezett rajz, tűkiosztás vagy gyártási
kiadás.

Az SBC, akkumulátor, RF/hangburkolat és árnyékolása az állvány/alap rögzített részén marad. A könnyű antennabölcső és sugárzó szerelvény AZ, EL és korlátozott tengelyirányú POL forgást végez. Így a nehéz számítógép és akkumulátor nem kerül mozgó tengelyre. A mechanikai POL-forgás nem RF-kéziségváltás. Az architektúra-ábrán jelölt RF-választó elektromosan független a POL-tól, sávonkénti és TX közben tiltott.

A koax/vezérlő kábelkötegnek illeszkednie kell a jóváhagyott AZ/EL/POL burkolóhoz. Ennek és a kábel kiválasztásáig a hajlítási sugár, torziós élettartam, tehermentesítés, elvezetés és forgócsatlakozás nyitott tervezési bemenet. Korlátozott kábelhurok helyett ne használj folyamatos forgást, nem minősített csúszógyűrűt vagy általános koaxforgót.

### Moduláris építés és előfeltételek

Ez az útmutató az integrált összeszerelési folyamatot írja le, de nem követeli
meg, hogy minden modult együtt építs meg. Az alábbi szakaszokban tartsd meg a
modulhatárokat:

| Modulazonosító | Önálló hatókör | Előfeltételek és kizárások |
|---|---|---|
| `MOD-ROTOR` | Állványinterfész, rögzített tálca, AZ/EL/POL-mechanika, parkolórögzítés, motorok, enkóderek, NC-végállások és mozgásbiztonság | Az antenna- és rádiómodulok nélkül is szerelhető, konfigurálható és tesztelhető. Terheletlen próbához rögzített állványt és inert műterhet használj. Élő antenna tömegét csak az antenna-modul és a mechanikai terhelési burkoló elfogadása után add hozzá. |
| `MOD-ANTENNA` | Antenna/sugárzó, 145/435 MHz-es táplálási utak, SMA-koax és sávonkénti RHCP/LHCP-táplálási/kapcsolóinterfészek | Saját biztonságos tartó és RF-mérőkészülékek szükségesek; önálló szereléshez/méréshez rotor, CM5 vagy LimeSDR nem kell. A rotor/terhelési kapu teljesítése előtt az antennát ne használd rotorpróba-terhelésként. |
| `MOD-RADIO` | CM5 + hivatalos CM5 I/O-panel + kiadott segédpanel + két LimeSDR Mini modul, RF-/audio-konfiguráció és tápinterfészek | Rotor és antenna nélkül is konfigurálható/próbapadon tesztelhető, névleges RF-lezárásokkal/forrásokkal és jóváhagyott audio-készülékkel. A segédpanel, táp, tűkiosztás, USB és TX-retesz kapui továbbra is érvényesek; az önálló építés nem jelent felmentést. |
| `MOD-INTEGRATED` | Egyesített, üzemkész állomás | Elfogadott `MOD-ROTOR`, `MOD-ANTENNA` és `MOD-RADIO` interfészeket, továbbá a teljes tömeg-, biztonsági, RF-, táp- és terepi elfogadási kapuk teljesítését igényli. |

Az „opcionális” azt jelenti, hogy egy elem nem szükséges az adott modul
önálló építéséhez; nem jelenti azt, hogy elhagyható egy olyan integrált
tesztből, amely függ tőle. Az állvány/szerelvény, biztonságos tartók, névleges
RF-terhelések vagy antennák, mérőeszközök, akkumulátor és töltő a konkrét
próbák szerint külső felszerelések; nem válnak észrevétlenül a modul beépített
anyagává. Ez a táblázat nem helyettesít modulonkénti BOM-ot. A külön
modulútmutatók önálló szállítandó dokumentumok; a projektintegrátor akkor
hivatkozik rájuk, ha rendelkezésre állnak. Itt még nem létező útmutatóra
nincs hivatkozás.

### Alkatrésztérkép és kiadási állapot

| No. | Szerelési elem | Állapot és integrációs megjegyzés |
|---:|---|---|
| 1 | Állvány és talajmegtámasztás | A meglévő interfész fém fényképezőgép-állványra való rögzítés. Azonosítsd és mérd le a tényleges állványt/fejet; ellenőrizd a szerkezeti besorolást teljes állomásra, szerelvényre, mért külső súlypontra, oldal-/csavaró terhelésre, szintezésre és rögzítésre. |
| 2 | Rögzített fém tálca/adapter | Csak az álló alap megtámasztása. A mechanikai CAD fém tálcát/tartót tartalmaz; végmérete és az új SBC/radio teher illeszkedése nincs jóváhagyva. Nyomtatott műanyag menet nem lehet elsődleges teherút. |
| 3 | Védett akkumulátor vagy táp | Pontos gyártó/típus, kimeneti tartomány, áram/használható energia, biztosíték, töltő és tömeg TBD. Két SDR RX-út, CM5, motorok, feltételes egyetlen aktív TX PA-terhelés és átalakítási veszteségek alapján méretezd. Csak sértetlen, védett kereskedelmi terméket és a hozzá tartozó töltőt használj; mérd az üzemidőt/áramot/hőviselkedést. Maradjon álló helyen. |
| 4 | Fő leválasztó, biztosítékok, motor-stop | A régi NYÁK értékei/útvonalai nem helyettesítik az új tervet. A pontos, reteszelhető, DC-re minősített stopalkatrész régi kiadási blokkoló; az új rendszer besorolása és resetviselkedése TBD. |
| 5 | CM5, hivatalos I/O-panel, segédpanel és tárhely | A hivatalos CM5 I/O-panel az alap/hordozó; a CM5 konfigurációs SKU-ja jelölt, még ellenőrizendő. A külön segédpanel, annak CM5IO-interfésze, tápellátása, hőmegoldása, tárhelye, OS-képe és mozgásinterfésze még tervezendő/dokumentálandó/tesztelendő. A segédpanel nem készült el és nincs gyártásra kiadva. |
| 6 | Árnyékolt RF-/hangrekesz | Két cserélhető LimeSDR Mini a tervezett kettős VHF/UHF RX-hez; mindkettő TX-képes, de hardveres biztonsági alapállapot csak egy aktív TX-utat enged, egyidejű adást soha. Az RX-hang egyszerre egy csatornát választ; keverés/kettős dekódolás nincs. Az USB 3 gazda/hubtopológia, pontos modulrevízió, feltételes lineáris PA, szűrők, árnyékolás és hőtervezés minősítendő. A modul kimenete kis teljesítményű (frekvencia/revízió függvényében ≈+10 dBm max), nem a feltételes állomáscél: 5 W FM vivő, 5 W PEP USB, 1 W AM vivő 100% modulációnál (4 W ideális PEP). Mindenhol hagyományos 50 Ω SMA, minden pontos interfészt ellenőrizni kell. Az ASA önmagában nem RF-árnyékolás. |
| 7 | Hang és kezelőszervek | Belső hangszóró/mikrofon, valamint külső Baofeng/K1 jellegű kiegészítő; a külön 3,5/2,5 mm hang/PTT-aljzat nem SMA RF vagy táp. Pontos aljzatkiosztás, tűkiosztás, bias, PTT és BTL/hangleválasztás ellenőrizetlen. |
| 8 | RF- és vezérlő kábelköteg | Hagyományos 50 Ω SMA az antenna, VHF/UHF diplexer, hibrid/CP-port, mindkét LimeSDR Mini, feltételes PA-/szűrőlánc és átvezetők között. Koax/hossz, SMA-csatlakozónem/középérintkező, kábelbesorolás, árnyékolás, sávfüggő táplálás, AZ/EL/POL kábelút és torziós élettartam TBD; RP-SMA, BNC-alap vagy adapterlánc nincs. |
| 9 | AZ/EL/POL mechanika és visszajelzés | Az új tervhez három független kimeneti enkóder (tengelyenként egy) és hat független NC-végállás (tengelyenként kettő), továbbá kemény ütközők és megfelelő hibakezelés kell. A jelenlegi BASE CAD és régi vezérlő csak AZ/EL-t ír le; POL és új hat-végállás/három-enkóder megvalósítás nincs kiadva. Érzékelőtípus, interfész, csatorna, út és terhelés TBD; összeszerelési/terhelési teszt nincs jelentve. |
| 10 | Forgó antennabölcső és sugárzók | A 145/435 MHz-es antenna-geometria csak kiinduló koncepció. Illesztés, kéziség, axiális arány, iránykarakterisztika, csatolás, hajtogatott érintkezők, tényleges tömeg/súlypont és koaxhatás mérendő. Számítógép/akkumulátor ne kerüljön a mozgó szerelvényre. |
| 11 | Független RF-kéziségválasztó | Sávonkénti 145/435 MHz körkörös táplálás-/fázishálózat, kompatibilis körpolarizált antennához való, RF-re minősített RHCP/LHCP-váltás. Az RF-állapot különálló a POL-helyzettől; TX alatt tiltott, a beállt állapot ellenőrzendő. Minden RF-port szabványos 50 Ω SMA; tényleges alkatrész-csatlakozónem/érintkező és besorolás TBD. |
| 12 | GNSS-vevő és antenna | A helyhez/UTC-hez szükséges; a vevő/antenna, elhelyezés, UART, elektromos szintek, üzenetformátum és PPS elérhetősége nincs kiválasztva/ellenőrizve. PPS csak a kiválasztott modul dokumentációjának és jelszintjeinek igazolása után használható. Az álló GNSS-fix nem ad irányt. |
| 13 | Távoli iránytű-magnetométer és alapszög-IMU | Iránybecsléshez és dőléskompenzációhoz szükséges; az érzékelő, rögzítés, interfész, NYÁK-tűk és kalibráció nincs megvalósítva/kiadva. Motoroktól, RF-teljesítménytől, nagyáramú vezetékektől és ferromágneses anyagtól távoli, mágnesesen csendes helyre szereld; a kész szerelvényt kalibráld, független kézi valódiirány-referenciával ellenőrizd. |

### Három tengely és körpolarizáció határai

A pozícióvektort `(AZ, EL, POL)` alakban kezeld. A POL korlátozott tengelyirányú forgatás, nem azimut-körbefordítás és nem polarizációs módválasztó. Az előzetes ±90° mechanikai védősáv csak javaslat a mechanikai modellhez; amíg a modell nem határozza meg a biztonságos utat, minden számszerű POL-cél/parancs nem érhető el. Az új tervhez független kemény ütközők, két NC-végállás, enkóder-visszajelzés, watchdog-hibakezelés, harmadik motor-meghajtó csatorna, megfelelően biztosított/táplált harmadik tengelyág szükséges. Besorolást, áramkört, csatlakozót, polaritást, tűkiosztást és közös vagy független biztonsági lekapcsolási ágat az ellenőrzött kapcsolási rajzban kell meghatározni; itt nincs vezetékszintű útmutatás.

### GNSS-, iránytű-, enkóder- és végállás-integráció

A GNSS és az iránytű külön érzékelő, szerepük eltérő. A kiválasztott vevő GNSS-e helyet és UTC-t ad; álló állomásnak **nem** ad irányt. A GNSS-antennát csak a kiválasztott vevő jóváhagyott RF-/tápkövetelményei szerint csatlakoztasd. UART-ot csak a vevő és SBC interfész, logikai szintek, protokoll és csatlakozó ellenőrzése után használj. A PPS opcionális/nem megvalósított marad, amíg a pontos modul nem dokumentálja a feszültségszinteket, impulzus-polaritást/szélességet, időzítési viselkedést, és a hordozópanel nem kínál igazolt bemenetet. Jóváhagyott GNSS/UART/PPS tűkiosztás nincs.

AZ, EL és POL tengelyhez egy-egy független kimeneti enkódert, tengelyenként két, összesen hat NC-végállás-érintkezőt kell biztosítani. Az új befagyasztott kapcsolási rajzon mind a hat végállás, enkóder-interfész, hibaválasz és motor-tápmegszakítás szerepeljen, függetlenül tesztelve. A régi ESP32 hordozó két AS5600 enkódere és négy AZ/EL NC bemenete nem teljesíti a háromtengelyes követelményt. AS5600-osztályú érzékelők esetén azonos eszközök I2C-címe `0x36`; minden eszköz külön igazolt I2C-buszt vagy kiválasztott/validált buszmultiplexert kapjon. Ne feltételezd három azonos című érzékelő együttműködését egy buszon, és ne következtesd, hogy a régi panel buszvezetékezése másolható SBC-hordozóra.

Az iránytűt/magnetométert és dőlés-IMU-t mereven a rögzített alapon, a jóváhagyott elrendezés szerint motoroktól, motorvezetékektől/meghajtóktól, PA/adó-vevő és RF-tápláló hardvertől, akkumulátortól/nagyáramú vezetékezéstől és ferromágneses szerkezeti/csavaranyagoktól távoli, mágnesesen csendes helyre szereld. A kész állomás végleges összeállításában kalibráld a mágneses környezetet (hard-/soft-iron hatások és érzékelő-alap igazítása is); a hely/dátum dokumentált helyi mágneses deklinációjával add meg a valódi irányt. Dőléskompenzációra az IMU mért alapszögét használd. Mentsd el a módszert, deklinációs forrást/dátumot, érzékelő orientációját és validálási eredményeket; megmagyarázatlan eltolást ne nullázz ki.

A GNSS/iránytű-vezetékezés **TBD az SBC-hordozópanel és tűkiosztás befagyasztásáig**. Elsőként a vevőkimenetet és UTC-t üzembe kell helyezni motor/RF-táp nélkül. Ezután rögzített állomással, antenna/adás nélkül mérd az irányt kikapcsolt motorokkal, majd minden motor-meghajtó bekapcsolt/működtetett állapotával, a 29. lépés biztonságos feltételei között; naplózd a változást/zavart. RF-/tápzavar csak RF-biztonsági kapuk után, megfelelő műterhelésű, ellenőrzött próbán értékelhető; más esetben RF maradjon letiltva, a vizsgálat függőben. Terepi validáláskor az irányt hasonlítsd össze a helyszínen, kézzel meghatározott, független valódiirány-referenciával; ellenőrizd az alapszöget és GNSS hely/időt, ismételd meg biztonságos motor ki/be állapotban. Az érvényes álló GNSS-fix soha nem helyettesítheti az irányt; érvénytelen/elavult/nem elérhető/eltérő iránytűadatot hibaként/TARTÁSként kell jelezni, nem nulla fokkal vagy csendes tartalékkal helyettesíteni.

### Revízió-A GPIO-monitor térkép — referencia, nem bekötési engedély

A [hardware/cm5/interface.json](../../hardware/cm5/interface.json) A revíziójú
szoftverintegrációs szerződése az alábbi hat, alaphelyzetben zárt
végállás-monitor bemenetet rendeli hozzá. A fizikai fejléc tűszámai a
[CM5-PCB.md](CM5-PCB.md) szerinti auditálást segítik; a BCM-szám és a
fejlécpozíció azonosító, nem utasítás terepi bekötésre. A szerződés szerint
az egészséges, zárt NC-érintkező LOW, a nyitott érintkező vagy szakadt vezeték
HIGH állapotot jelez:

| Jel | BCM GPIO | CM5IO fizikai fejléc tű |
|---|---:|---:|
| AZ minimum NC-monitor | 4 | 7 |
| AZ maximum NC-monitor | 5 | 29 |
| EL minimum NC-monitor | 6 | 31 |
| EL maximum NC-monitor | 7 | 26 |
| POL minimum NC-monitor | 8 | 24 |
| POL maximum NC-monitor | 9 | 21 |

Az E-stop kiegészítő monitor BCM GPIO10 / fizikai fejléc 19
(egészséges: LOW; nyitott/hiba: HIGH); **csak monitorbemenet**. A BCM GPIO12
a közös motor-élesítési **kérés**; az MCP23017 GPA0/GPA1/GPA2 az AZ/EL/POL
engedélyezési kérése. Ezek a szoftveres/bővítőjelek nem hardveres engedélyek,
és nem szakítják meg a motor tápját. A revízió-A JSON kifejezetten jelzi,
hogy a NYÁK-hardver még nincs megtervezve vagy gyártva, az NC-bemenetek nem
független hardveres stopok, a külső kemény végállás/watchdog/E-stop
védőáramkörök pedig továbbra is kiadási blokkolók. Bármilyen motoros mozgás
előtt meg kell tervezni, felül kell vizsgálni és tesztelni a külön
névlegesített, reteszelő E-stop tápmegszakítást és a független
keményvégállás/meghajtó-stop utat. Kizárólag chatből, ábrából vagy ebből a
szövegből vett tűtérkép alapján ne vezetékezz, ne helyezz feszültség alá és
ne mozgasd a motort.

Körpolarizált antennához sávonként külön RF-állapotot határozz meg `RHCP` vagy `LHCP` értékkel. A kompatibilis körkörös táplálásnak névleges 145 és 435 MHz-en saját, helyes fázisú ortogonális út kell. Az RF-kapcsoló gyártó/terv szerint igazolt táplálási fázist vagy útvonalat válasszon, ami megfordítja a relatív kvadratúra-kéziséget. Méréssel igazold mindkét kéziséget; csatlakozó/port átnevezése nem bizonyíték. Kapcsolóút frekvencia-, teljesítmény-, beiktatási veszteség-, izoláció-, illesztetlenség-, tranziens- és break-before-make besorolása dokumentálandó. Reteszeld a kapcsolást úgy, hogy PTT tiltott, RF-táp hiányzik és a választott állapot beállt/igazolt legyen TX előtt. Pusztán szoftveres parancs nem biztonsági mechanizmus.

Mérd meg az axiális arányt **mindkét sáv, mindkét RHCP/LHCP-beállítás** esetén, a jóváhagyott frekvenciasávban és előírt rámutatási/mérési geometriában. A projekt kezdeti körantenna-célja műholdirányban ≤3 dB axiális arány; ezt tesztelni kell, nem előrejelzés. A kiválasztott antennát/táplálást/kapcsolót egy szerelvényként mérd. Alacsony VSWR, kapcsolóparancs, fázishálózati szimuláció vagy mechanikai forgatás nem bizonyít axiális arányt.

## 3. Anyagok és külső eszközök

Ez összevont tervezési ellenőrzőlista, nem ajánlat vagy kiadott beszerzési BOM. Lásd [multimode-assembly.csv](../../bom/multimode-assembly.csv). Az alábbi szíjhajtás-mennyiségek csak a jelenlegi mechanikai BASE-t írják le; nem zárják le az új RF/SBC rendszertervet.

### Azonosítandó külső anyagok/hardverek

- A pontos meglévő állvány, fém adapter, tálca, rögzítők és másodlagos biztonsági megtartás. Vásárlás előtt azonosítsd a tényleges állvány menetét/illeszkedését. Mérd le a megvásárolt állvány/fej tömegét; ne használj katalógus-becslést. Ellenőrizd a gyártói értékeket és a szerelvényt a teljes állomás mért tömegére/külső súlypontjára, excentrikus, oldalirányú és csavaró terheléssel.
- Jelenlegi BASE hajtás: négy zárt GT2 szíj, 126 fog / 252 mm hossz / 6 mm szélesség; nyolc fém szíjtárcsa (négy 20 fogú, négy 100 fogú); négy 608 csapágy (8×22×7 mm), négy 6000 csapágy (10×26×8 mm), két 8×60 mm közbenső acéltengely, két 10×89 mm kimeneti acéltengely. A kiválasztott alkatrészek valós agyszélességét, tengelykialakítását, igazítását, szíjfeszítési határát és hézagait ellenőrizd.
- Harmadik POL-tengely, a mechanikai modell függvényében: egy motor, dedikált harmadik meghajtó/tápág, korlátozott forgású tartó/kemény ütközők, egy kimeneti enkóder, két NC-végálláskapcsoló és watchdog/hibaretesz. Pontos alkatrész, táp, út, áttétel, csatlakozó/tűkiosztás és tömeg TBD. A javasolt ±90° nem kiadott tartomány. A régi hordozó tartalék csatlakozóját ne feltételezd.
- A jelenlegi CAD 3 mm-es 6082 alumíniumlemez-elemeket ír elő; a rajzon meghatározott lemezek/tartók és valós tömegük vágás előtt ellenőrzendő a legfrissebb CAD/DXF alapján. Korábbi bolygómű-elrendezést vagy régi 180×130 mm-es ESP32-hordozót ne gyárts új SBC-tartónak.
- Szerelési hardver: fém átmenőcsavarok, alátétek, önzáró anyák, tengelyreteszek/csapok/gyűrűk, szíjfeszítő elemek, tehermentesítés, kábelbilincsek és másodlagos rögzítés jóváhagyott rajzok/tényleges terhelések alapján. Hossz, szilárdság és meghúzási nyomaték TBD, ahol rajz/gyártói specifikáció nem adja meg.
- RF-út: megfelelő besorolású 50 Ω koax/csatlakozók, sávfüggő illesztés/szűrés, duplexer/izolációs hálózat, külön 145 és 435 MHz-es kvadratúra-/táphálózat és RF-re minősített RHCP/LHCP fázis-/táplálásválasztó. Kiválasztott interfész: hagyományos 50 Ω SMA antenna, VHF/UHF diplexer, hibrid/CP táplálás, SDR/radio és RF-átvezető között. RP-SMA tilos. Vásárlás előtt minden illeszkedő pár mindkét végén rögzítsd a középérintkező típusát (tüske/foglalat) és kapcsolóanya nemét; az „SMA” megnevezés önmagában nem igazolja az illeszkedést. Használj közvetlenül kompatibilis csatlakozást, ne adapterláncot. Csatlakozó/kábel tömege, paneltartás, tehermentesítés, hajlítási sugár és gyártói szerelési nyomaték TBD; ne találj ki nyomatékot és a koax ne terhelje a NYÁK átvezetőjét. Régi BNC csak történeti lehetőség, nem alapinterfész. A választó TX ellen reteszelt legyen. Ne csak wattérték alapján vásárolj hibridet, és ne feltételezd, hogy tetszőleges portcserével kéziség váltható.
- Rádiólánc: két cserélhető LimeSDR Mini biztosítja a szándékolt egyidejű kétsávos VHF/UHF RX-et; mindkettő képes TX-re, de biztonságos üzemben csak egy aktív TX-út lehet. Bluetooth-hang egyszerre egy RX-csatornát választ; a kettő keverése/dekódolása nincs. Modulonkénti natív kimenet kis teljesítményű, frekvenciától/revíziótól függően körülbelül legfeljebb +10 dBm; a pontos hardvert ellenőrizd/mérd. Feltételes szűrt kimeneti célok: 5 W FM vivő, 5 W PEP USB, 1 W AM vivő 100% szinuszos moduláció mellett (4 W ideális PEP); ezek nem elért teljesítmények. Lineáris PA és sáv-/harmonikus-szűrő szükséges. +10 dBm (10 mW) és 5 W (36,99 dBm) között a veszteségek/headroom előtt körülbelül 27 dB ideális erősítés kell; mérd az erősítés/kompresszió tényleges keretét. Az 5 W PEP lánc csak akkor képes az ideális 4 W AM PEP-re, ha szűrő után a kimenet és a mért torzítás/headroom megengedi; az AM vivő/moduláció maradjon ezen ellenőrzött kereten belül. AM/USB-hez E osztályú PA tilos. Engedélyezett üzem előtt minősítsd a kibocsátást, hőt, izolációt, deszenzitizációt.
- CM5-elektronika: a mérlegelt build része a CM5, egyedi hordozó, ellenőrzött USB 3 mezzanine/interfész, tápátalakítás/-elosztás és hőmegoldás. Próbapadi vizsgálat előtt ellenőrizni kell a pontos hivatalos CM5 I/O-dokumentumokat és CM5/LimeSDR-összekötést; az I/O panel csak próbapadi értékelés, nem egyedi termékhordozó vagy egyedi NYÁK-validálási eredmény.
- A külső hang külön tartozék-interfész: Baofeng/K1 jellegű 3,5/2,5 mm aljzat hang/PTT, nem SMA és nem táp. Aljzattérkép, tartozék-tűkiosztás, mikrofonbias és PTT-viselkedés nem ellenőrzött; méret/külső alapján ne vezetékezz.
- Árnyékolt RF-burkolat, vezető kötés/kötőanyag, hőkezelés és elektromosan szigetelő távtartók. Az árnyékolási hatás, hézagok, kötés és hőáram a kiválasztott alkatrészekkel igazolandó.
- Pontos SBC, SDR/adó-vevő, szűrők, kapcsoló/duplex elemek, hangkodek, hangszóró, mikrofon, Bluetooth-interfész, külső tartozék, csatlakozók, biztosítékok és védett táp: **TBD; jóváhagyott alkatrész/tűkiosztás nincs**.

### Próbapadi műszerek, tesztkészülékek és kéziszerszámok

- Tolómérő, derékszög, egyenes léc, szintező, megfelelő mérleg, mérőóra vagy ezzel egyenértékű eszköz tengelyigazítás, kimeneti játék és ütés ellenőrzésére. A mérleg legyen alkalmas a teljes állomás és egyes modulok mérésére; rögzítsd az azonosítót, felbontást és kalibrálási/ellenőrzési állapotot.
- Jóváhagyott kötőelemekhez való kéziszerszám; fémalkatrészekhez ellenőrzött fúró-/sorjázó szerszám; szemvédelem. Nyomatékszerszám csak akkor kell, ha kiválasztott kötőelem/gyártó nyomatékot ír elő.
- Kisfeszültségű üzembe helyezéshez áramkorlátozott labor táp; DMM/ohmmérő; megfelelő szondás oszcilloszkóp; tápelemek hőmérése. Ismeretlen áramkörű híd/BTL hangszórókimenetet ne mérj földelt szkópszondával.
- Passzív RF-ellenőrzéshez legalább 100–500 MHz-es, kalibrált VNA, SOL kalibráló standard/kábel és ismert 50 Ω lezárás. Mentsd a kalibrált S-paraméteradatot és tesztkonfigurációt. Axiális arány/kéziség karakterizálásához megfelelő kalibrált antenna-mérőhely/referenciaantenna és polarizációmérési módszer kell; a VNA önmagában nem mér sugárzott axiális arányt.
- Későbbi, engedélyezett RF-próba előtt: spektrumanalizátor vagy kalibrált vevő, megfelelő csillapítók/csatolók és 50 Ω műterhelés, amelynek frekvenciatartománya, csatlakozója, csúcsteljesítménye, átlagteljesítménye és terhelési tényezője meghaladja a jóváhagyott próbáét. A „50 Ω” felirat önmagában nem elég.
- Számítógép és adatgyűjtés naplókhoz. SBC-specifikus programozó/debug hardver TBD az SBC/hordozó kiválasztásáig. Ne feltételezd, hogy a régi ESP32 WebFlash Linux SBC-t konfigurál.

### A teljes állomás lemért leltára

Az üzemkész konfiguráció tényleges alkatrészeivel töltsd ki. Csak mért részösszegeket írj be; szükség esetén további sort adj hozzá. BOM-becslés, katalógus szerinti állványtömeg és a régi 3,130–3,200 kg érték nem használható mérésként.

| Szerelvény | Mennyiség / tartalom | Mért részösszeg (kg) | Azonosító / megjegyzés |
|---|---|---:|---|
| Állvány és fej | Ténylegesen vásárolt állvány/fej |  |  |
| Állomás-szerelvény, tálca, adapter, megtartás | Teljes állványinterfész és szükséges rögzítés |  |  |
| AZ/EL rotor és motorok | Minden beépített AZ/EL szerkezet, motor, tengely, szíj, csapágy |  |  |
| POL tengely és motor | Szerelt forgómechanika, motor, tartó, enkóder, ütközők, támaszok |  |  |
| Antenna/tápláló szerelvény | Sugárzók, táphálózat, rögzítések és állandó RF-kapcsoló |  |  |
| Rádiók és RF-lánc | Két LimeSDR Mini, kiválasztott PA-út, szűrők, duplex/izoláció, RF-árnyékolás, szükséges USB-hub |  |  |
| SBC és vezérlőelektronika | SBC, tárhely, hordozó, vezérlő- és biztonsági elektronika |  |  |
| Beépített állomástáp | Átalakítók, biztosítékok, leválasztók, állomásoldali akkumulátor-bemeneti csatlakozó/polaritásvédelem és elosztás; a külső akkumulátorcsomag/BMS nélkül |  |  |
| Külső energiarendszer (külön) | A felhasználó által megadott hivatkozás: [ECO-WORTHY LiFePO4 12 V, 30 Ah, 40308275183822 változat](https://es.eco-worthy.com/products/bateria-litio-lifepo4-12v-30ah?currency=EUR&country=ES&variant=40308275183822) / DE-L13060202003-1 cikkszám („1 Pack”, csak akkumulátor). A gyártói oldal 12,8 V-ot, 30 Ah-t, 360 Wh-t, 3,55 kg-ot, 183 × 176 × 83 mm-t, M5 kivezetéseket, legfeljebb 14,6 V-os töltést és 10 V-os kisütési lekapcsolást tüntet fel. Az oldal legfeljebb 30 A töltő-/kisütőáramot is jelez, és azt írja, hogy a lítiumakkumulátorok BMS-t tartalmaznak, de a pontos BMS-adatokat és típushoz tartozó adatlapot nem ellenőriztük. A termékszöveg 3,55 kg-ot ad meg, miközben a hivatkozott változat szállítási tömegének metaadata nulla; a tömeg nem igazolt, a leszállított csomagot le kell mérni. A feltüntetett energia ellentmond a 12,8 V × 30 Ah = 384 Wh számításnak; tervezési referenciaként csak az alacsonyabb, közzétett 360 Wh használható, nem mért hasznos energiaként. Az akkumulátor/BMS tömege kimarad az 5,000 kg-os állomáskorlátból, de külön mérendő/jelentendő; az ára maradjon a projekt teljes költségében. Az állomásoldali átalakító, biztosíték, csatlakozó, polaritásvédelem és vezetékezés beleszámít az állomás tömegébe; a töltő is, ha magaddal viszed. A hivatkozott változat csak akkumulátor; az oldalon külön feltüntetett 5 A-es töltő külön változat, nem bizonyíték arra, hogy a kiválasztott opcióhoz töltő jár vagy kompatibilis. A kétórás autonómia nincs igazolva; lásd az alábbi energiaszámítást és az [árhivatkozásokat/forrásjegyzeteket](REFERENCE-PRICES.md). |  |  |
| Kábelek/csatlakozók | Szükséges RF-, táp-, vezérlő-, hang- és külső kábelek |  |  |
| Burkolat/hőhardver | Szerelt burkolat, árnyékolás, hűtőbordák, hűtés |  |  |
| Egyéb szükséges üzemi elemek | Üzemkész állapothoz szerelt vagy vitt tételek |  |  |
| **Teljes üzemkész állomás tömege** | **A beépített/vitt állomássorok összege; az állvány/fej beleszámít, csak a külső akkumulátorcsomag/beépített BMS tömege marad ki** |  | **A megadott mérési bizonytalansággal együtt ≤5,000 kg kell legyen** |

A leltár mellé rögzítsd a mérleg azonosítóját, felbontását és kalibrálási/ellenőrzési állapotát. Mérd meg a teljes állomás külső súlypontját az állványcsatlakozáshoz képest, és a módszert/eredményt csatold a tesztrekordhoz. Ellenőrizd a tényleges állvány/szerelvény besorolását a teljes tömeg/súlypont és a vonatkozó excentrikus, oldalirányú, csavaró terhelések mellett. A külön javasolt tervezési cél ≤4,500 kg; rögzítsd, hogy a 0,500 kg tartalék igazolt-e, ne feltételezd. A vitt tömeget is jelentsd: az állomás tömege plusz a külön lemért külső akkumulátorcsomag/BMS, valamint minden külön vitt töltő vagy tartozék. A tömegkorlát alóli kivétel nem csökkenti a szállítási tömeget vagy a költséget.

## 4. Szakaszos összeszerelés és konfigurálás

Minden lépés az 1. szakasz TARTÁS-kapuinak hatálya alatt áll. A pipa azt jelenti, hogy a megnevezett ellenőrzést a tényleges revízión megfigyelték és rögzítették; nem jelenti, hogy számítás, render vagy szoftverteszt sikeres volt.

Az ábrák elvi referenciák, nem méretezett gyártási rajzok. **FIG-01** a rendszer-/kapcsolatblokk áttekintése; **FIG-02** a fizikai alkatrészek robbantott térképe (számozott buborékok megfelelnek a fenti térképnek); **FIG-03** a régi, kizárólag két tengelyes ESP32 határábrája. Minden számozott lépéshez tartozik ábra és pontos tervezési BOM-azonosító/mennyiség. Az `1 set` mennyiség készlet marad, mert jóváhagyott rajz/gyártói definíció nem határozta meg az elemek számát; kötőelem/fogyóeszköz mennyiségét ne találd ki. A „None” azt jelenti, hogy ellenőrzési/konfigurációs lépés nem használ fel további beépített elemet. A tesztműszerek és újrahasználható szerszámok külön szerepelnek a BOM-ban, nem adódnak a tömeghez és nem számolandók újra beépített alkatrészként; ha üzemkész állomástartozékként csomagolod őket, egyszer mérd le hordozott eszközként.

| Lépés | Alkalmazandó modul / előfeltétel | Ábra | A lépés BOM-elemei és mennyiségei |
|---:|---|---|---|
| 1 | Közös leltár; más modul nem kell | FIG-01, FIG-02, FIG-04 | MMA-015 ×1 CM5-jelölt; MMA-050 ×1 hivatalos CM5 I/O-panel; MMA-017 ×2 LimeSDR Mini (csak azonosítás/címkézés; még ne szereld vagy vezetékezd be) |
| 2 | `MOD-ROTOR`; antenna/radio nem kell | FIG-02 | MMA-002 ×1 tálcareferencia; MMA-004 ×4 szíj; MMA-005 ×4 20T tárcsa; MMA-006 ×4 100T tárcsa; MMA-007 ×4 608 csapágy; MMA-008 ×4 6000 csapágy; MMA-009 ×2 közbenső tengely; MMA-010 ×2 kimeneti tengely; MMA-011 ×1 lemez-/tartóalkatrész-készlet |
| 3 | Bármely önálló modul vagy `MOD-INTEGRATED`; csak a felsorolt tartalmat mérd | FIG-01, FIG-02, FIG-04 | Mérd le a BOM-mennyiség szerinti állomástételeket: MMA-001–MMA-012, MMA-014–MMA-021, MMA-023–MMA-028, MMA-035–MMA-044, MMA-046–MMA-050, valamint MMA-052, ha kiválasztott/beépített; számítsd bele az MMA-017 ×2-t. A külső MMA-013 akkumulátorcsomagot/BMS-t külön mérd (a hivatkozott ECO-WORTHY 30 Ah változat közzétett referencia-tömege 3,55 kg; a tényleges példányt is mérni kell), és hagyd ki az 5,000 kg-os állomásrészösszegből; a teljes akkumulátorrendszer költsége szerepeljen a projektleltárban. A töltő beleszámít az állomástömegbe, ha üzemkész felszerelésként viszik; különben jelentsd külön. Az állomásoldali bemeneti kábel/átalakító/biztosíték tömege számít. MMA-034 ×1 mérleg/szerszám újrahasználható; csak akkor számít, ha viszik. A tesztelésre szánt MMA-022, MMA-029–MMA-034, MMA-045 és MMA-051 kimarad, hacsak ténylegesen nem viszik az üzemkész konfigurációban. |
| 4 | Közös biztonsági előkészítés; az adott modulnak megfelelően rögzítsd | FIG-02 | Nincs új beépített anyag; MMA-001 ×1 állvány/fej, ha ezt választják alátámasztásnak; MMA-012 ×1 rögzítő, ha az adott tengely/terhelés megköveteli; MMA-034 ×1 újrahasználható biztonsági/ellenőrző szerszámkészlet |
| 5 | `MOD-ROTOR`; antenna/radio nélkül | FIG-02 | MMA-001 ×1 állvány/fej; MMA-002 ×1 tálca/adapter; MMA-003 ×1 ellenőrzött kötőelem-/másodlagosrögzítés-készlet |
| 6 | `MOD-ROTOR`; antenna/radio nélkül | FIG-02 | MMA-004 ×4 szíj; MMA-005 ×4 20T tárcsa; MMA-006 ×4 100T tárcsa; MMA-007 ×4 608 csapágy; MMA-008 ×4 6000 csapágy; MMA-009 ×2 közbenső tengely; MMA-010 ×2 kimeneti tengely; MMA-011 ×1 tartókészlet |
| 7 | `MOD-ROTOR`; antenna/radio nélkül | FIG-02 | Nincs további beépített állomásanyag; MMA-034 ×1 újrahasználható ellenőrzőszerszám-készlet |
| 8 | `MOD-ROTOR`; antenna/radio nélkül | FIG-02 | MMA-012 ×1 fém parkolórögzítő |
| 9 | `MOD-ROTOR`; inert próbakészülék, nem élő antenna | FIG-02 | MMA-051 ×1 inert, nem vezető mechanikai műterhelés-/vizsgálókeret-készlet (tesztkészülék, nem élő antenna és nem beépített tömeg) |
| 10 | `MOD-ROTOR`; antenna/radio nélkül, antennaterhelés még nincs felszerelve | FIG-02, FIG-04 | MMA-035 ×1 POL-motor/-tartó; MMA-036 ×1 Watterott TMC5160 v1.5 POL-meghajtó; MMA-037 ×3 enkóder; MMA-038 ×6 NC-végállás; MMA-039 ×1 watchdog/retesz; MMA-040 ×1 védett ág/kábelköteg; MMA-003 ×1 jóváhagyott mechanikai rögzítőkészlet |
| 11 | `MOD-ROTOR`; antenna/radio nélkül | FIG-02 | MMA-034 ×1 újrahasználható mérőeszköz-készlet; MMA-037 ×3 enkóder és MMA-038 ×6 kapcsoló csak akkor, ha már beépítették hézagellenőrzéshez |
| 12 | `MOD-INTEGRATED`; elfogadott rotorinterfész; a radio illesztése csak makett | FIG-01, FIG-02, FIG-04, FIG-05 | MMA-002 ×1 fix tálca; MMA-003 ×1 szerelvényhardver-készlet; külső MMA-013 akkumulátorrendszer külön dokumentálva; MMA-014 ×1 leválasztó/stop; MMA-020 ×1 árnyékolt burkolat; MMA-028 ×1 Powerpole/biztosíték/kábelköteg-készlet; MMA-049 ×1 átalakítókészlet; MMA-050 ×1 hivatalos CM5 I/O-panel; MMA-047 ×1 segédpanel, csak kiadás után |
| 13 | `MOD-INTEGRATED`; elfogadott rotor- és antennakábel-interfész | FIG-01, FIG-02 | MMA-021 ×1 SMA/koax-készlet; MMA-028 ×1 védett vezetékezés/tehermentesítés; MMA-040 ×1 POL-ág/kábelköteg; MMA-044 ×1 korlátozott forgású szervizhurok |
| 14 | `MOD-INTEGRATED`; minden modul tápmentes | FIG-01, FIG-02, FIG-05 | MMA-020 ×1 burkolat/kötés; MMA-021 ×1 koaxkészlet; MMA-028 ×1 vezetékezés/Powerpole/biztosítékelosztás; MMA-049 ×1 tápátalakító-/hőalkatrész-készlet |
| 15 | `MOD-INTEGRATED`; kiadott burkolat-/NYÁK-/mechanikai rajzok szükségesek | FIG-01, FIG-02, FIG-04 | MMA-047 ×1 segédpanel; MMA-050 ×1 hivatalos CM5 I/O-panel; MMA-020 ×1 burkolat. Fúrási fogyóanyag nincs megadva; TARTÁS a kiadott mechanikai rajzig és a beültetett alkatrészek hézagellenőrzéséig. |
| 16 | Csak `LEGACY`; nem `MOD-RADIO` lépés | FIG-03 | Csak a régi ESP32 NYÁK-referenciája; új állomás-BOM-tétel nincs. Külön engedélyezés esetén használd a régi NYÁK saját kiadott BOM-ját. |
| 17 | Csak `LEGACY`; nem `MOD-RADIO` lépés | FIG-03 | Csak régi teszt; új állomás-BOM-tétel nincs. A régi próbapadi tápegység/biztosíték/tesztanyag csak saját jóváhagyott eljárásból vehető. |
| 18 | Csak `LEGACY`; nem `MOD-ROTOR` háromtengelyes konfiguráció | FIG-03 | Csak régi biztonsági teszt; új állomás-BOM-tétel nincs. NC-teszthez áthidaló/jumper nem használható. |
| 19 | Csak `LEGACY`; nem `MOD-ROTOR` háromtengelyes konfiguráció | FIG-03 | Csak régi AZ/EL-számítás/referencia; új állomás-BOM-tétel nincs. |
| 20 | `MOD-RADIO` kiadási kapu; a modulok közötti interfészek TARTÁS állapotúak | FIG-01, FIG-04 | MMA-015 ×1 CM5-jelölt; MMA-050 ×1 hivatalos CM5 I/O-panel; MMA-017 ×2 SDR; MMA-047 ×1 segédpanel; MMA-048 ×1 kettős USB-topológia; MMA-014 ×1 stop; MMA-028 ×1 vezetékezés/védelem (csatlakozás előtt jóváhagyott dokumentumok szükségesek) |
| 21 | `MOD-RADIO`; próbapadi konfigurációhoz rotor/antenna nem kell | FIG-01, FIG-04 | MMA-015 ×1 CM5; MMA-050 ×1 hivatalos CM5 I/O-panel; MMA-047 ×1 segédpanel; MMA-048 ×1 kettős SDR-kapcsolat; MMA-052 ×1 csak akkor, ha minősített, táplált USB-hangúthoz választják |
| 22 | `MOD-RADIO`; próbapadi OS/provisioning, rotor/antenna nélkül | FIG-01, FIG-04 | MMA-015 ×1 CM5; MMA-050 ×1 hivatalos CM5 I/O-panel; tárhely-/szoftverkonfiguráció; új beépített BOM-tétel nincs |
| 23 | `MOD-ROTOR` meghajtókonfiguráció; a segédpanel kiadása függőség | FIG-01, FIG-04 | MMA-016 ×1 determinisztikus mozgás-/biztonsági interfész; MMA-036 ×1 kiválasztott Watterott TMC5160 v1.5 POL-meghajtó; MMA-037 ×3 enkóder; MMA-038 ×6 NC-végállás; MMA-039 ×1 watchdog; MMA-040 ×1 védett POL-ág; MMA-047 ×1 segédpanel |
| 24 | `MOD-ROTOR`; determinisztikus mozgás- és stoptervezés/-teszt | FIG-01, FIG-04 | MMA-016 ×1 determinisztikus mozgás-/biztonsági interfész; MMA-036 ×1 kiválasztott POL-meghajtó; MMA-037 ×3 enkóder; MMA-038 ×6 NC-végállás; MMA-039 ×1 watchdog/retesz; MMA-040 ×1 védett ág; MMA-051 ×1 inert rögzítő-/tesztkészülék |
| 25 | `MOD-RADIO` SDR-próba; fizikai antenna-/kéziségvizsgálathoz csak a `MOD-ANTENNA` kell | FIG-01, FIG-02, FIG-04 | MMA-017 ×2 SDR; MMA-018 ×1 feltételes PA-/hőhardver-készlet, ha kiválasztották; MMA-019 ×1 szűrő/duplexer; MMA-021 ×1 RF-kábelköteg; MMA-022 ×1 besorolt RF-próbakészülék; MMA-041 ×1 145 MHz-es táplálás; MMA-042 ×1 435 MHz-es táplálás; MMA-043 ×1 RF-kéziségválasztó; MMA-045 ×1 mérőkészlet; MMA-048 ×1 kettős USB |
| 26 | `MOD-RADIO`; CAT/Doppler-próba, antenna/rotor nélkül | FIG-01 | MMA-017 ×2 SDR; MMA-022 ×1 besorolt RF-próbakészülék; MMA-031 ×1 spektrumanalizátor/kalibrált vevő, ha a kiadott próbafolyamat előírja |
| 27 | `MOD-RADIO`; hangpróba; külső rádió/tartozék választható és külön minősítendő | FIG-01, FIG-02, FIG-04 | MMA-023 ×1 hangválasztó/kodek; MMA-024 ×1 hangszóró/mikrofon; MMA-025 ×1 külső hang/PTT-tartozék; MMA-026 ×1 Bluetooth-átviteli készlet; MMA-052 ×1 csak táplált USB-hub kiválasztása esetén |
| 28 | `MOD-RADIO`; loopback/helyi adatfeldolgozás, rotor/antenna nélkül | FIG-01, FIG-04 | MMA-017 ×2 SDR; MMA-022 ×1 besorolt RF-próbakészülék; MMA-023 ×1 választó/kodek; MMA-026 ×1 Bluetooth-átvitel; MMA-052 ×1 csak minősített USB-hanghoz választva |
| 29 | `MOD-INTEGRATED`; bekötés közben a tápforrás legyen leválasztva | FIG-01, FIG-05 | MMA-013 ×1 külső akkumulátor-referencia (bekötés alatt maradjon leválasztva); MMA-028 ×1 Powerpole-/tápkábelköteg/biztosítékok; MMA-032 ×1 áramkorlátozott tápegység; MMA-033 ×1 DMM/szkóp készlet (újrahasználható mérőeszköz) |
| 30 | `MOD-RADIO` logika/GNSS-próba; vevőellenőrzéshez rotor/antenna nem kell | FIG-01 | MMA-027 ×1 GNSS-vevő-/antenna-készlet; MMA-033 ×1 mérőeszköz-készlet; MMA-015 ×1 CM5; MMA-046 ×1 iránytű/IMU csak a későbbi rotor-/alapellenőrzéshez |
| 31 | `MOD-ROTOR`; háromtengelyes motorpróba rögzített inert terheléssel, antenna/RF nélkül | FIG-01, FIG-02, FIG-04 | MMA-012 ×1 parkolórögzítő; MMA-035 ×1 POL-motor; MMA-036 ×1 Watterott TMC5160 v1.5; MMA-037 ×3 enkóder; MMA-038 ×6 NC-végállás; MMA-039 ×1 watchdog; MMA-040 ×1 tápág; MMA-051 ×1 inert próbakészülék |
| 32 | `MOD-RADIO` vételi próba és `MOD-ROTOR` iránytű-ellenőrzés; integráció csak az egyesített terepi teszthez | FIG-01 | MMA-017 ×2 SDR; MMA-019 ×1 RF-szűrő/izoláció; MMA-021 ×1 RF-kábelköteg; MMA-027 ×1 GNSS-vevő-/antenna-készlet; MMA-029 ×1 SOL-készlet; MMA-030 ×1 VNA; MMA-031 ×1 spektrumanalizátor/kalibrált vevő; MMA-032 ×1 tápegység; MMA-046 ×1 iránytű/IMU |
| 33 | `MOD-RADIO` TX-próba, antenna/rotor nélkül; besorolt próbakészülék szükséges | FIG-01 | MMA-017 ×2 SDR (csak egy TX-út engedélyezve); MMA-018 ×1 feltételes lineáris PA-/hőhardver; MMA-019 ×1 szűrők; MMA-022 ×1 besorolt műterhelés-/csillapítókészlet; MMA-031 ×1 analizátor; MMA-032 ×1 tápegység |
| 34 | `MOD-INTEGRATED`; minden beépített modul és állomásoldali hardver | FIG-01, FIG-02, FIG-04 | Mérd le újra a beépített/vitt állomástételeket BOM-mennyiségben: MMA-001–MMA-012, MMA-014–MMA-021, MMA-023–MMA-028, MMA-035–MMA-044, MMA-046–MMA-050, valamint MMA-052, ha beépített; számítsd bele az MMA-017 ×2-t, kiválasztott PA-/szűrő-/hang-/hőtételeket, állványt/fejet, minden tengelyt, érzékelőt, állomásoldali tápkábelt/átalakítót/biztosítékot és rögzítést. Az MMA-013 külső akkumulátor/BMS tényleges tömegét külön jegyezd fel (a pontosan hivatkozott 30 Ah változat közzétett referencia-tömege 3,55 kg; mérd le a tényleges példányt); tömege nem része az állomáskorlátnak, de az összesített hordozott tömeg és projektköltség része. A töltő beleszámít, ha viszik. Az MMA-022, MMA-029–MMA-034, MMA-045 és MMA-051 teszt-/fejlesztési tétel csak akkor számít, ha ténylegesen csomagolják; az MMA-034 ×1 mérleg/szerszám újrahasználható, és csak akkor tartozik bele, ha viszik. Beépített tételt ne számolj kétszer. |

### A szakasz — azonosítás és előkészítés

1. Rögzítsd a projekt/BOM revíziót, legfrissebb CAD/DXF fájlneveket, kezelőt, dátumot és minden fizikai modul azonosítóját. Minden tárgyat címkézz **régi ESP32 rotor**, **új SBC/radio-jelölt** vagy **tesztberendezés** kategóriával. A régi hordozó footprintjét ne keverd az új panelrajzokba.
2. Hasonlítsd össze a gyártott mechanikai alkatrészeket a jelenlegi BASE rajzokkal. Repedt, vetemedett vagy nem nyomon követhető teherhordó alkatrészt utasíts el. A tényleges alkatrészeken ellenőrizd a csapágyat, tengelyméretet, tárcsafog/agyméretet, szíjprofilt/hosszt és lemezvastagságot. A régebbi bolygómű-szerelvény és szerelési méretei nem csereszabatosak a jelenlegi szíjas BASE-szel.
3. A rögzített terhet (tálca, védett táp, stop, SBC/radio burkolat) és a mozgó terhet (háromtengelyes rotor, bölcső, antenna) külön szerelvényként rendezd el. Kezdj lemért tömeg- és külső súlypontleltárt; vedd bele a tényleges állványt/fejet, szerelvényt/adaptert, antennát, minden motort/rotorrészt, rádiót, SBC-t, kábeleket, burkolatokat, kötőelemeket és szükséges megtartást. A külső akkumulátorcsomag/BMS tömegét külön mérd és jelentsd, de hagyd ki az 5,000 kg-os állomásrészösszegből; a töltőt és az állomásoldali akkumulátor-bemeneti hardvert a fenti szabály szerint kezeld. Valós alkatrészt/szerelvényt mérj; ellenőrizetlen katalógus-/örökölt becslést ne írj be mért értékként. Az üzemkész állomás nem haladhatja meg az **5,000 kg-ot**; a javasolt tervezési cél **legfeljebb 4,500 kg**, 0,500 kg tartalékkal. A cél még nincs igazolva; a régi 3,130–3,200 kg becslés (rádió és állvány nélkül) nem megfelelési eredmény.
4. Jelölj ki összeszerelési kizárási zónát, és rögzítsd az állványt. Tengelyek alatti munka közben AZ, EL, POL legyen mechanikusan rögzítve és tápmentes.

### B szakasz — rotor-modul (`MOD-ROTOR`), antenna és rádió nélkül

Ez az önálló rotorszerelési útvonal. Stabil, rögzített állvány vagy próbakeret
szükséges; az antenna és a rádió nem előfeltétel. Terheletlen mechanikai
vizsgálatkor csak inert műterhet használj. Az antenna-/rádiómodul tételei
kimaradnak, kivéve ha egy későbbi integrált elfogadási lépés kifejezetten
megköveteli őket.

5. Ellenőrzött fém kötőelemmel illeszd az állványt a fém adapterhez/tálcához.
   Ellenőrizd a menetkapcsolatot, hogy nem ütközik fel, kontrollált kézi
   terhelés alatt nem fordul/elcsúszik, és van külön másodlagos megtartás.
   A fényképezőgép-terhelési adat önmagában nem bizonyítja az oldalirányú
   nyomatéki terhelhetőséget. Ellenőrizd a tényleges állványt és szerelvényt
   a teljes állomástömeg és mért külső súlypont mellett; értékeld a
   szerelvény excentrikus, oldalirányú és csavaró terhelését.
6. A jelenlegi szíjhajtás minden fokozatát a legfrissebb CAD és gyártói méretek
   alapján szereld: a fém csapágytartókat és tengelyeket derékszögben illeszd,
   a vásárolt tárcsákat a hozzájuk tartozó tengelyre tedd, igazítsd a
   szíjsíkokat, a gyártó előírásán belül feszítsd meg a szíjakat, majd rögzítsd
   az állítóelemeket. Ne feszíts ASA-tartó hajlításával, ne találj ki nyomatékot
   és ne helyettesítsd a tárcsákat nyomtatott alkatrésszel.
7. Terheletlen tengelyeket kézzel forgass át több teljes fordulaton. Jegyezd
   fel az akadást, szíjfutást, ütést, tengelyirányú játékot, irányváltási
   holtjátékot és a kötőelemek elmozdulását. Akadás/eltérés esetén állj meg és
   javíts; motorral ne kényszerítsd helyre az illesztést.
8. Az elevációs terhet különálló fém parkolócsappal vagy rögzítővel tartsd meg.
   Még az antenna felhelyezése előtt igazold, hogy a rögzítő megtartja a
   terheletlen mozgó szerelvényt. Ne támaszkodj léptetőmotor-tartónyomatékra
   vagy bekapcsolt meghajtóra zuhanás elleni védelemként.
9. Először a bölcsőt és nem vezető/inert műterhet szereld fel. A projekt
   ideiglenes antennakorlátja 500 g, a súlypont pedig az elevációs tengelytől
   30 mm-en belül legyen; ezek igazolandó tervezési korlátok, nem bizonyított
   teherbírások. A mozgó tömeg/súlypont-keretbe számítsd bele a POL-motort,
   enkódert, kábelt és tartókat. A terhelést csak dokumentált
   készülék-/próbatervezettel növeld, parkolórögzítővel, kiürített zónával és
   független mechanikus ütközővel.
10. A harmadik POL-tengelyt csak akkor integráld, ha mechanikai modellje
    meghatározta az utat, kemény ütközőt, megtámasztást/csapágyazást,
    enkóderhelyet, motor-/meghajtó-interfészt és kábelvezetést. A javasolt
    ±90° nem jóváhagyott út. Szerelj fel két NC-végállást és szoftvertől
    független mechanikus ütköző/megtartást, majd motorok nélkül, kézzel
    ellenőrizd a teljes korlátozott utat. Folyamatos forgatás nincs.
11. Mérd meg a tényleges antenna, bölcső és POL-tengely tömegét/súlypontját.
    Kézzel ellenőrizd az AZ/EL/POL összesített mozgási burkolóját, beleértve
    a kötőelemeket, három tengely ütközőit, a kábelek torziós/szervizhurkos
    kialakítását és minden parkolási helyzetet. Élő antennát még ne szerelj fel.

### Önálló antennamodul (`MOD-ANTENNA`), rotortól és rádiótól függetlenül

Az antennamodul külön, stabil tartón összeszerelhető és vizsgálható; ehhez
nem szükséges rotor, CM5 vagy LimeSDR. Ez nem engedély koncepcionális ábrából
történő gyártásra: csak kiadott antenna-/táplálásrajzokat és pontos
alkatrészrevíziókat használj, a még ki nem választott antennageometriát,
RF-kapcsolóáramkört és névleges értékeket pedig tartsd TARTÁS alatt.

| Sorrend | Ábra / alkatrészazonosítók | BOM-tételek és külső előfeltételek |
| --- | --- | --- |
| A1 — azonosítás és mérés | FIG-02 #10 antenna, #11 önálló választó | MMA-041 ×1 145 MHz-es táplálás; MMA-042 ×1 435 MHz-es táplálás; rögzítsd az antenna/táplálás tényleges tömegét és súlypontját. |
| A2 — különálló rögzítés | FIG-02 #10 | Stabil, önállóan minősített antennatartó/szerelvény; a rotort ne használd szerelőkeretként vagy teherhordóként. MMA-034 ×1 készlet újrahasználható mérőeszköz. |
| A3 — RF-interfészek ellenőrzése | FIG-01, FIG-02 #8/#10/#11 | MMA-021 ×1 készlet hagyományos 50 Ω-os SMA-koax; MMA-043 ×1 választó, kizárólag pontosan kompatibilis jóváhagyott eszköz/terv esetén. Ellenőrizd az SMA középérintkezőjét, a csatlakozópár nemét, a frekvencia-/teljesítménybesorolást és a gyártói nyomatékot; RP-SMA és adapterlánc tilos. |
| A4 — sávonkénti/kéziség szerinti jellemzés | FIG-01, FIG-02 #10/#11 | MMA-029 ×1 SOL-készlet és MMA-030 ×1 VNA a kalibrált impedancia-/S-paraméter-ellenőrzéshez; MMA-045 ×1 megfelelő axiálisarány-/polarizációmérő készlet és kalibrált mérési lehetőség. A jóváhagyott tápláló/fázishálózattal külön vizsgáld a 145 és 435 MHz-et RHCP és LHCP állapotban. A VNA visszaverési vesztesége önmagában nem mér axiális arányt. |
| A5 — a választó biztonságos igazolása | FIG-01, FIG-02 #11 | MMA-043 ×1 pontos RF-választó és MMA-045 ×1 besorolt izoláció-/beiktatásiveszteség-mérési lehetőség. Letiltott TX és kikapcsolt RF-táp mellett igazold a dokumentált vezérlési állapotot, beállási időt, sávonkénti útvonalakat és izolációt. TX közben RF-állapotot váltani tilos; tetszőleges portcsere nem bizonyít kéziségváltást. |

A kiválasztott táphálózatnak és kapcsolónak szándékosan kell létrehoznia az
igazolt relatív fázist/kéziséget; a tengelyirányú POL-forgatás nem fordítja
meg az RHCP/LHCP állapotot. Minden sávhoz és kéziséghez rögzítsd a kalibrált
mérési elrendezést, referenciasíkot, frekvenciatartományt, geometriát,
állapotot és eredményt. A modult csak akkor csatlakoztasd a rotorhoz, ha
elfogadták a rotor mechanikai terhelési kapuját, valamint az antennamodul
RF-/fizikai interfészét.

### C szakasz — integrált mechanikai illesztés (`MOD-INTEGRATED` only)

E lépések az önálló modulokat egyesítik. Ne végezd őket rotor-, antenna- vagy
rádió-önálló konfiguráció részeként; a makett nem engedélyez feszültség alá
helyezést vagy adást.

12. Csak jóváhagyott rögzített tálcát és burkolatot szerelj. Az akkumulátor és
    az SBC/RF-burkolat a rögzített tartón legyen, ne az AZ/EL/POL forgó
    szerkezeten. A könnyű POL-tengely és antenna csak a modellben meghatározott
    korlátozott úton mozoghat. Biztosíts szellőzést és árnyékolt RF-teret úgy,
    hogy ne akadályozd a hűtést és ne hozz létre nem ellenőrzött vezető utat.
13. Minden berendezést tápmentesen tartva készíts makett-koax- és
    vezérlőkábel-elrendezést az AZ/EL/POL teljes útján. Tartsd be a kiválasztott
    kábelgyártó minimális hajlítási sugarát és torziós ciklushatárát; csatlakozó
    ne viselje a kábel húzását, kábel ne kerülhessen szíj/tengely/fogaskerék
    útjába, hurok ne feszüljön végállásnál, és a köteg ne akadjon parkoláskor.
    A POL-koax csak a jóváhagyott korlátozott forgáshoz igazodjon. Csúszógyűrűt
    csak kiválasztott és minősített RF-egység esetén használj. Hiba esetén
    feszültség alá helyezés előtt módosítsd a nyomvonalat. Az antenna,
    VHF/UHF diplexer, hibrid/CP-portok, mindkét LimeSDR Mini, PA-/szűrőlánc és
    RF-átvezetések hagyományos 50 Ω-os SMA csatlakozásait egységesítsd. Vásárlás
    vagy csatlakoztatás előtt a pontos gyártói rajz alapján ellenőrizd a
    középérintkezőt és a kapcsolóanya nemét; RP-SMA és régi BNC ne kerüljön az
    alapinterfészbe, adapterláncot kerüld. Az SMA-kábelt függetlenül rögzítsd;
    tömegét és csatlakozónyomatékát a kiválasztott gyártó adata határozza meg,
    addig TARTÁS. A Baofeng/K1 jellegű 3,5/2,5 mm jack csak külső hang/PTT,
    nem SMA RF vagy táp; tűkiosztás/bias TARTÁS.
14. A koaxot/árnyékolt RF-utat fizikailag válaszd el a motorvezetékektől,
    kapcsolóüzemű szabályozóktól, GNSS-antennától/táplálástól és érzékeny
    hangtól. A jóváhagyott elektromos terv határozzon meg egy szándékos
    árnyékolási/földelési rendszert; brumm miatt ne adj önkényes
    árnyékoláskötést és ne emeld fel a védőföldet.
15. Elvi SVG-méretek alapján ne fúrj burkolat-/NYÁK-nyílásokat. Előbb a
    jóváhagyott, beültetett szerelvény tényleges csatlakozóit, dugóit,
    kábelkivezetéseit és szervizhézagait mérd meg.

### D szakasz — régi digitális vezérlő, csak referencia

16. A meglévő ESP32-hordozó csak saját NYÁK-kiadási blokkolóinak [PCB.md](PCB.md) szerinti lezárása után szerelhető. Ez **két tengelyes AZ/EL** panel, két TMC2209 foglalattal (U2/U3), két motorcsatlakozóval és négy NC mozgás/home bemenettel. A 180×130 mm méret, 38 tűs DevKitC V4, csatlakozók, 12 V motorút, külső buck, közös driver-enable és stopáramkör kizárólag e revízióhoz tartoznak. Nincs benne harmadik POL-meghajtó, POL-enkóderinterfész, POL NC-végállás, külön POL watchdog/tápág vagy kiadott háromtengelyes biztonsági viselkedés. Külön ellenőrzött hardverterv nélkül nem vezérelheti a megerősített háromtengelyes célt. Ez **nem** bekötési útmutató az SBC/radio újratervezéshez.
17. Kiadott régi panel próbájához annak saját szerelési sorrendjét és pontos gyártó/modul revízióit kövesd. Modulbehelyezés előtt, táp nélkül folytonosságot és zárlatot mérj. A hordozó saját elfogadási eljárásával ellenőrizd próbapadi tápot, külső biztosítékot, motor-tápmegszakítót, izolált NC-monitort, külső buck kimenetet és 3,3 V logikát. Első logikai táppróbán motorok leválasztva.
18. Táp nélkül igazold NC-stop és végállás-érintkezőket szakadásként, majd ellenőrizd, hogy a fizikai motor-tápmegszakító firmware-től független. Reset/újraindítás után motor kimenet tiltott legyen, homing/mozgás/PTT ne induljon.
19. Az ESP32 AZ/EL alap 16 mikrolépést és két 5:1 fokozatot használ 25:1-re (azokkal a pontos feltételekkel 80 000 parancsolt mikrolépés/kimeneti fordulat). Ez nem igazolja a pozíciópontosságot vagy új SBC impulzusmódszert. Motor/meghajtó/szíj/mikrolépés/áttétel változásakor számolj újra és tesztelj. Ezek az adatok nem határoznak meg POL-áttételt/motort/mikrolépést/utat/felbontást.

### E szakasz — új SBC/radio; jóváhagyásig ne lépj túl a maketten

20. Új panel gyártása előtt hagyj jóvá verziókezelt interfészcsomagot: pontos SBC-/rádiómodul-azonosítók/revíziók; háromtengelyes rajz; tápsínek/csúcsáramok; jóváhagyott csatlakozók/tűkiosztás; a hivatalos CM5 I/O-panel revíziója és a segédpanel szabályozott illesztése; felülvizsgált segédpanel-kapcsolási rajz/NYÁK, valamint JLC BOM/CPL audit; fizikai, nyomva tartásos adási PTT-viselkedés; PTT-ki watchdog/NC-stop; hőhatárok; biztosíték; föld-/árnyékolási terv; RF-blokkdiagram; firmware/OS-verziók; teszt-/kiadási jóváhagyás. A JLC BOM cikkszámait, footprintjeit, szerelési oldalát és alkatrészforgatását ellenőrizd a befagyasztott terv alapján; minden ismeretlen mező TARTÁS.
21. A FIG-04-et a panel-stack koncepcionális referenciájaként használd: CM5 modul a hivatalos CM5 I/O-panelen; a külön gyártott segédpanel a felülvizsgált háromtengelyes motor-/érzékelő-/hang-/biztonsági interfész. A vezeték nélküli, 4 GB RAM-os, 16 GB eMMC-s CM5-konfiguráció jelölt, nem befagyasztott beszerzési SKU. Ne helyezd egymásra és ne csatlakoztasd a segédpanelt, amíg a mechanikai rögzítése és az összeköttetése nincs kiadva. A két LimeSDR Mini az erre kijelölt két USB 3 úton, modulonként külön közvetlen kapcsolattal működik, a pontos I/O-panel-revízió és az egyidejű működés ellenőrzése után. Az USB-hangút még nincs eldöntve: minősíts táplált USB-hubot vagy dokumentált/konfigurált USB 2 gazdautat. Ne feltételezd, hogy hub létezik, hangot visz vagy az útját már tesztelték. A végül kiválasztott megoldás számára hagyj elegendő helyet és tömegkeretet.
22. Linux-képet/provisionálást csak SBC-támogatás, tárhelyintegritás, boot, frissítés/helyreállítás, erőforráskeret és offline működés ellenőrzése után válassz. Indítás/szolgáltatás-újraindítás nem indíthat motort/PTT-t. Feltételezett fejlécszámozás alapján ne kösd STEP/DIR-t GPIO-ra.
23. A harmadik, POL-tengely meghajtójának választása a Watterott TMC5160 v1.5 modul. A jóváhagyott konfigurációs szándék: SPI1-vezérlés, nyitott ramp-mode jumper, valamint a letiltott/kikapcsolt állapotú EN magas szinten tartása indításkor, resetkor és hiba esetén. A segédpanel kapcsolási rajzának kiadása vagy alkatrészrendelés előtt ellenőrizd a pontos modulrevízió kézikönyvét, órajel-forrását/tűrését, jumper jelentését, EN-polaritását és biztonságos jelszintjeit, valamint a választott SPI-interfészt. Az órajel tűrését rögzítsd a mozgás időzítési/hibakeretében; áramkorlátozott próbapadi tápról, leválasztott motorral igazold a ramp-viselkedést, konfiguráció-visszaolvasást, letiltott állapotot és hibakezelést. Ezt ne fordítsd CM5 fejléc-tűsorra, és ne következtesd ki a másik két tengely meghajtóját.
24. Mozgási impulzusgenerálást/leállítást determinisztikus, felülvizsgált hardveres/vezérlési útra bízd. Teljes CPU/lemez/Wi-Fi/Bluetooth/SDR/hang terhelés mellett igazolj korlátozott időzítést. Szokásos Linux/Python ciklusból nem szabad automatikusan precíz STEP-generátorra következtetni.
25. Mindkét cserélhető LimeSDR Mini RX-utat a pontos revízió gyártói dokumentuma alapján konfiguráld. Egyidejű kétsávos VHF/UHF-vétel, támogatott FM/AM/USB mód, oszcillátorpontosság, mért be-/kimeneti szint és mindkét USB 3 kapcsolat vizsgálandó párhuzamos működésben. Hub-döntés előtt ellenőrizd a CM5 gazdaportot/átbocsátást; port/hub topológiát ne feltételezz. Mindkét modul TX-képes, de hibainjektálással tesztelt hardveres alapállapot legfeljebb egy aktív TX-utat engedjen; kettős TX soha. Bluetooth-hang egyszerre csak egy kiválasztott RX-csatornát vigyen; keverés/dekódolás nincs. Modulonkénti natív RF-kimenet kis teljesítményű (frekvenciától függően körülbelül +10 dBm max; pontos revízió/mérés ellenőrzendő), nem feltételes 5 W állomáskimenet. Feltételes cél: 5 W FM vivő, 5 W PEP USB, 1 W AM vivő 100% szinuszos modulációnál (4 W ideális PEP); még el nem ért, lineáris PA-t és sáv-/harmonikus-szűrőket igényel, AM/USB-hez E osztály nem alkalmas. Névleges szerelvényen mérd a tényleges szűrt kimenetet, AM modulációmélységet/PEP-et, USB PEP-et, linearitást, mellékharmonikusokat, tápáramot és hőmérsékletet. Ellenőrizd a szűrő/interfészveszteség utáni PA torzítás-/headroom-tartalékot; a névleges 5 W PEP önmagában nem igazolja az 1 W AM vivőt. A vevőizolációt a kiválasztott PA-kimenetre, ne csak LimeSDR kisjelű szintjére számold újra. Minden támogatott módban teszteld mindkét kereszt-sáv kombinációt: 145 TX/435 RX, majd 435 TX/145 RX, a nem aktív TX hardveres tiltásával. Mindkét RX együtt működhet, de a Bluetooth-választó csak egyet útvonalaz, nem kever/dekódol kettőt. Egyidejű két TX tilos akkor is, ha mindkét modul képes adni. Azonos sávú egyidejű RX/TX igényhez külön teszt kell. Két frekvenciavezérlő/antenna-port nem bizonyít adás közbeni vételt. Minden támogatott sávhoz definiálj külön RHCP/LHCP RF-állapotot. A sávfüggő körbetápláló hálózat/kapcsoló igazolt relatív táplálási fázist/kéziséget váltson; önkényes portcsere nem elég. Kapcsolás csak PTT-ki/RF-tápmentes állapotban, beállásának igazolásával; TX közben kapcsolni tilos, RF-kéziséget POL-szögből levezetni tilos.
26. CAT/Dopplert rögzített frekvencia-visszaolvasással és próbapadi RF-forrással/terheléssel teszteld antenna csatlakoztatása előtt. Ellenőrizd uplink/downlink korrekciót, előjelet, kerekítést, frissítési frekvenciát, elavulást, frekvenciahatárokat és vezérlésvesztést. E dokumentumban CAT-parancsprotokoll nincs jóváhagyva.
27. Először csak vételi hang-loopbacket validálj. A Bluetooth-hang külön kétirányú adatút; a régi rotor BLE-vezérlő kapcsolata nem hangátvitel. Ellenőrizd a mintavételt/formátumot, csatornatérképet, veszteséget/késést, adat-tónust károsító AGC/zajkapuzás hiányát és bontáskori biztonságos némítást. Belső hangszóró/mikrofon és külső tartozék bekötését igazolt rajzból ellenőrizd, ne általános csatlakozónévből.
28. Helyi SSTV/AX.25 feldolgozást ismert PCM/WAV tesztvektorokkal, képekkel, AX.25 FCS/CRC-vel, NRZI/bit stuffinggal, hívójel/címzéssel és duplikáció/újraküldés viselkedéssel teszteld. Előbb loopback. Helyileg dekódolt keret vagy létrehozott hangminta nem bizonyít RF-adást vagy távoli kézbesítést.

### F szakasz — bekapcsolási kapuk és terepi előkészítés

29. Akkumulátor, mindhárom motorcsatorna, adó-vevő és antenna leválasztva; vizsgáld át a szerelvényt és végezz pont-pont folytonosság-, polaritás- és izolációmérést a jóváhagyott kapcsolási rajz alapján. Rögzíts műszert/mért értékeket. Ismeretlen tű, váratlan folytonosság vagy dokumentálatlan feszültség blokkolja a bekapcsolást.
30. Csak a jóváhagyott logikai tápágat tápláld áramkorlátozott forrásról, az új panel eljárásával. Ellenőrizd a sínek feszültségét/hullámosságát, bootnaplót, hőviselkedést és alap kimeneti állapotokat. Teszteld stopérintkező nyit/zárlat, watchdog-lejárat, OS-összeomlás, újraindítás, tárhelyhiba és hálózatvesztés esetét. Kimenet biztonságosan hibázzon: se motor, se PTT. Motor/RF-táp nélkül helyezd üzembe a GNSS-helyet/UTC-t; dokumentáld a vevő/protokoll érvényességét. UART/logikai interfészt, valamint PPS-t csak dokumentált/jóváhagyott modul, tűkiosztás és elektromos jelviselkedés mellett ellenőrizz; máskülönben a PPS kifejezetten nem elérhető.
31. Minden motorcsatornát antenna/RF nélkül, először mechanikusan rögzített inert teherrel tesztelj. Ellenőrizd AZ, EL, POL irányát, sebesség/gyorsulási korlátokat, mind a hat külön NC-végállás választ (tengelyenként kettőt), mindhárom külön enkóderolvasást, watchdog-időtúllépést, leállási késést, tápmegszakítást és reset utáni hatástalanítást. Mérd a mozgást/hőt, szoftverértékből ne következtess. Két tengelyes régi hordozópanelt/két meghajtócsatornáját ne használd háromtengelyes vezérlőként. A POL kemény ütközőit és NC-bemeneteit külön-külön ellenőrizd; számszerű utat csak kiadott mechanikai modellből határozz meg, független watchdoggal és tesztelt, megfelelően biztosított meghajtótáppal.
32. RF-vételi próbán zárd le megfelelően a nem használt portokat, használj ismert jelgenerátort, és hasonlítsd össze az RX zaját/érzékenységét SBC, kijelző, szabályozó, Bluetooth és motorok ki/be állapotában. Iránytűt a teljes szerelvényen kalibráld: rögzítsd az érzékelő/alap igazítását, hard-/soft-iron kalibrálást, helyet/dátumot/deklináció forrását és az IMU-alap dőléskompenzációt. Rögzített állomással, motor nélkül mérj irányt, majd ismételd meg minden motor-meghajtó bekapcsolt/működtetett állapotában, a 29. lépés biztonságos feltételei között. Hasonlítsd össze a terepen függetlenül, kézzel meghatározott valódiirány-referenciával; az álló GNSS-fix nem irány. Érvénytelen/elavult iránytű hibaként, soha nem nulla fokként jelentendő. RF-/tápzavar csak RF-biztonsági kapuk után, jóváhagyott ellenőrzött elrendezésben vizsgálható; egyébként függőben és RF-táp kikapcsolva. TX előtt az összes érintett passzív RF- és vevő-túlterhelési teszt legyen sikeres.
33. Későbbi adási teszt csak megfelelő licenccel/engedéllyel, ellenőrzött frekvenciával/móddal, jóváhagyott teljesítményhatárral, névleges műterheléssel, RF-árnyékolással/csillapítással, hőmérséklet-figyeléssel, valamint a fizikai PTT-t azonnal elengedni/tápot megszakítani képes kezelővel történhet. A PTT-nek kezelői elengedésre, watchdog-lejáratra, bontásra, hibára és újraindításra el kell engednie; áramköre még nincs megtervezve. A legalacsonyabb jóváhagyott teljesítményről indulj. Ezután mindkét RX-csatorna aktív és egy-TX-retesz próbája mellett vizsgáld az RX-deszenzitizációt. Ellenőrizd, hogy a Bluetooth-választó egyszerre egy RX-et útvonalaz. Minden RF-kéziség csak PTT tiltva és RF-táp nélkül tesztelhető; a beállt állapot legyen igazolt, mielőtt retesz engedne TX-et. Biztonságos próbapadi eredmény nem általános terepi engedély.
34. Szállítás előtt kapcsold le a tápot, elevációt mechanikusan rögzítsd, akkumulátort a gyártó szerint izoláld, szabad RF-csatlakozót távolítsd el/fedd le, antennaelemeket külön rögzítsd. Mérd le a teljes üzemkész állomást egy leltárként: állvány/fej, szerelvény/adapter, antenna, AZ/EL/POL rotor és mindhárom motor, rádiók, SBC, akkumulátor, kábelek, burkolatok, kötőelemek és szükséges megtartás. Rögzítsd az alkatrésztömegeket, szerelvénytömeget, mérlegazonosítót/felbontást/ellenőrzési állapotot és a külső súlypontot az állványhoz képest. Elfogadás csak akkor, ha a mért összeg a megadott bizonytalansággal **legfeljebb 5,000 kg**. A javasolt cél **legfeljebb 4,500 kg**; külön dokumentáld, teljesült-e a 0,500 kg tartalék. Ne találj ki állványtömeget és ne hagyd ki az összegből.

## 5. Mérnöki indoklás és számítási ellenőrzések

### RF-izoláció: mért rendszerkövetelmény

Csak gerjesztő-tervezési példában használható egy LimeSDR Mini hozzávetőleges, kis teljesítményű +10 dBm maximuma; frekvencia/pontos revízió szerint ellenőrizendő. Két modul nem engedélyez két aktív adót:

`Pexciter ~= +10 dBm` (körülbelül 10 mW/modul); nem garantált kimeneti specifikáció.

Ha hipotetikus passzív hálózat csak 35 dB TX→RX izolációt ad, az egyszerű szivárgási becslés `+10 - 35 = -25 dBm` a vevőúton, további szűrés/veszteség előtt. Ez még erős jel lehet; nem bizonyítja, hogy a vevő túléli vagy folytatja a vételt. Ez gerjesztő-példa, nem a kért 5 W PA-kimenet szivárgási becslése (a szűrő/interfészveszteség előtt körülbelül +37 dBm). Az egyetlen aktív TX-út kiválasztott, mért PA-kimenetén számold újra az izolációt, elutasítást és bemeneti védelmet.

**Csak tervezési példaként**, ha kiválasztott vevő referenciasíkján a megengedett maradék -90 dBm, a +10 dBm forrás ideális izolációs kerete `10 - (-90) = 100 dB`, mérnöki tartalék, illesztetlenség, harmonikusok, burkolatszivárgás, kábelcsatolás és mérési bizonytalanság előtt. A +10 dBm közelítő/frekvenciafüggő, -90 dBm szemléltető, nem általános vevőhatár. Későbbi lineáris PA-nál annak mért teljesítményével/kibocsátásával számolj újra. A tényleges keretet a jóváhagyott RX-blokkolási/kompressziós határ és a kívánt jel határozza meg.

145 MHz harmadik harmonikusa 435 MHz, közvetlenül a másik kért amatőrsávba esik. Harmonikus-szűrés, árnyékolás, antenna-csatolás, vezetett szivárgás és vevő-túlterhelés külön tesztelendő. A sávnév szerinti szűrés nem elég; mérd a teljes rádiókat/hálózatot/kábelköteget/antennákat végleges helyükön. Ne feltételezd, hogy a passzív diplexer duplexer vagy teljes duplex-képesség.

### A hangátvitel-kapacitás nem Bluetooth-garancia

Tömörítetlen, kétirányú 8 kHz / 16 bit / mono PCM nyers adatsebessége:

`8000 minta/s * 16 bit/minta * 2 irány = 256 000 bit/s összesen`

vagy összesen 32 000 bájt/s, irányonként 16 000 bájt/s, időbélyegek, keretezés, újraküldés, kodek/stack-többlet és vezérlőforgalom előtt. Szemléltető 247 bájtos ATT MTU és 3 bájt ATT-többlet után 244 bájt marad; jövőbeli 16 bájtos hangfejléc esetén 228 PCM-bájt használható. Ez `16000 / 228 = 70.2` csomag/s irányonként. Ez alsó becslés a csomagolásra, nem garancia a Bluetooth profil/stack áteresztésére vagy késésére. A régi rotor BLE minimum 23-as MTU-jánál a 20 bájtos ATT-érték és hangfejlécek túl kicsik ahhoz, hogy működő hangszolgáltatást feltételezzünk. A hangnak saját, mért átvitel kell, amely nem éhezteti ki a stop/vezérlőforgalmat.

### Feltételes PA-, akkumulátor-, hő-, tömeg- és mozgáskeretek

#### Kétórás autonómia-cél (nem mért tervezési becslés)

A kért üzemidő **2 óra** mindkét LimeSDR Mini vételi útjával, CM5-tel,
Bluetooth-hanggal, szakaszos AZ/EL/POL-mozgással és csak ideiglenesen
**20%-os TX-adási aránnyal** számol. A 20% példabemenet, nem jóváhagyott
üzemprofil és nem mért adási arány. A szabályozott terhelési síneken
értelmezett összteljesítmény:

- `P_idle`: a CM5, két SDR vétel, Bluetooth, hang és szakaszos
  motorhasználat átlagos bemeneti teljesítménye a terhelési síneken adás
  közben nem. A mozgás csak akkor tartozzon bele ebbe az alapállapotba,
  ha a jellemző aktivitási ütemet is meghatározták.
- `P_tx`: a teljes terhelési állapot teljesítménye az adási időszak alatt,
  beleértve a két RX-et, CM5-öt, Bluetooth-t, egy aktív TX-utat, PA-t és
  jellemző motorhasználatot. Ez a teljes üzemállapot teljesítménye, nem a
  PA többletfogyasztása.
- `duty`: ideiglenes TX-arány, jelenleg a példában `0.20`.
- `eta_converter`: mért vagy dokumentált, akkumulátortól a terhelésig
  értelmezett összesített átalakítási hatásfok, 0 és 1 között.
- `margin`: a bizonytalanságra, öregedésre és tartalékra szánt, kifejezetten
  meghatározandó/dokumentálandó energiatartalék; nem tekinthető mért adatnak.

Kétórás küldetéshez az ideiglenes, akkumulátoroldali energiaigény:

`E_battery_Wh = 2 h * (P_idle + (P_tx - P_idle) * duty) / eta_converter * (1 + margin)`

Ha csak a kért, ideiglenes adási arányt helyettesítjük be:

`E_battery_Wh = 2 h * (P_idle + (P_tx - P_idle) * 0.20) / eta_converter * (1 + margin)`

A jelenlegi, felhasználó által megadott akkumulátor-referencia az
[ECO-WORTHY 12 V 30 Ah, 40308275183822 változat](https://es.eco-worthy.com/products/bateria-litio-lifepo4-12v-30ah?currency=EUR&country=ES&variant=40308275183822),
DE-L13060202003-1 SKU-val, „1 Pack” (csak akkumulátor) néven. A gyártói
oldal 12,8 V-ot, 30 Ah-t, 360 Wh-t, 3,55 kg-ot, 183 × 176 × 83 mm-es
méretet, M5-ös kivezetéseket, legfeljebb 14,6 V töltőfeszültséget, 10 V-os
kisütési lekapcsolást és legfeljebb 30 A töltő-/kisütőáramot sorol fel. Az
oldal belső BMS-t is említ, de a pontos BMS-modell, áram-/időhatárai,
védelmi küszöbei és az adott modellhez tartozó adatlap nem ellenőrzött.
12,8 V × 30 Ah = 384 Wh, nem a közzétett 360 Wh; konzervatív referencia-
számításhoz az alacsonyabb, közzétett 360 Wh-t használd, nem mért vagy
garantált hasznos energiaként. A termékleírás 3,55 kg-ot közöl, de a
hivatkozott áruváltozat szállítási tömegének metaadata nulla. A tömeget
nem ellenőrzött, közzétett adatként kezeld; mérd le a leszállított
akkumulátort, és a tényleges külső tömegét rögzítsd.

Kizárólag ideális felső korlátot szemléltető példaként két órára:
`12 V * 30 Ah = 360 Wh`, így a névleges aritmetika
`360 Wh / 2 h = 180 W` átlagteljesítmény. Ez nem jelenti, hogy az
akkumulátor 360 Wh hasznos energiát ad le, hogy az állomás fogyasztása
180 W, vagy hogy sikerül a kétórás küldetés. Helyettesítsd be a mért
`P_idle`, `P_tx`, tényleges TX-arány, átalakítási hatásfok és tartalék/
derating értékeit a fenti képletbe, majd igazold az összeszerelt állomás
üzemidejét. A korábban említett 12 V / 1 Ah, 12 Wh csomagot felváltja ez
az akkumulátor-referencia; annak ideális, kétórás felső korlátja veszteség
előtt 6 W lett volna.

A pontosan hivatkozott változat csak akkumulátor, nem az ettől különböző
„12 V 30 Ah 5 A-es töltővel” termékváltozat. Ne feltételezd, hogy töltő
mellékelt vagy kompatibilis: töltés előtt szerezd be a pontos töltő
adatlapját, és az adott akkumulátor dokumentációja alapján ellenőrizd a
LiFePO4 töltési profilt, feszültséghatárt (a lista 14,6 V maximumot ad
meg), áramot, csatlakozót/polaritást és leállítási viselkedést. Ne tölts
rögtönzött, kétvezetékes USB-C kapcsolaton át. Amíg ezek az ellenőrzések
és egy tényleges időzített próba nem sikeres, az akkumulátor csak tervezési
referencia, nem kiválasztott/minősített táprendszer.

Nem indokolt számszerű üzemidő, amíg nincs dokumentálva a `P_idle`,
`P_tx`, átalakítási hatásfok, akkumulátor-feszültségtartomány, hasznos
kapacitás deratingje és tartalék. A 360 Wh gyártói címke/referencia, nem
mért hasznosenergia-eredmény. Mérd a sínfogyasztást az akkumulátor teljes
feszültségtartományában, beleértve az indítást, mindkét SDR-adatfolyamot,
Bluetooth-t/hangot, szakaszos mozgást és névleges lezárt vizsgálóterhelésbe
vezetett jellemző, egyetlen-TX-időszakokat. A megengedett akkumulátor/BMS-
értékek túllépése nélkül ellenőrizd az alacsony töltöttségi lekapcsolást
és az impulzus alatti feszültségesést. Ne névleges Ah-ból számolj
üzemidőt: az engedélyezett feszültségtartományon belüli használható
energiából, valamint a mért átalakítás, hőmérséklet és öregedés határaiból
válassz kapacitást, majd időzített, kétórás, jellemző próbával igazold.
Az üzemidő és autonómia a próba sikeréig nem igazolt.

#### Sínek és a teljes akkumulátorrendszer elszámolása

Tervezési legrosszabb esetként **5 V, 5 A rendelkezésre álló CM5 I/O-panel
bemeneti kerettel** számolj, a két LimeSDR USB-sínterhelését is beleértve.
USB-C-t tápra és adatra csak akkor részesítsd előnyben, ha a tényleges
panel-/modulinterfész támogatja; egyébként tartsd meg a jóváhagyott/natív
interfészt. Az 5 V / 5 A forrásnak ezt az áramot a CM5 I/O-panel bemenetén
kell tudnia; minősítsd a pontos forrást, a hivatalos panel USB-C
tápbemeneti viselkedését és a kábelt. A megvalósítás szerint, ahol
szükséges, megfelelő 5 A-es/e-jelölt USB-C-kábel kell. Ne feltételezd,
hogy egy USB-C dugó önmagában 5 A-t egyeztet vagy szolgáltat, hogy
megvalósult az USB Power Delivery, vagy hogy bármely USB-C adatport egyben
tápbemenet is. Ellenőrizd a hivatalos panel dokumentációját, és minden
tényleges port szerepét külön jelöld: paneltáp-bemenet, USB host/adat
(beleértve a két SDR-kapcsolatot), illetve adott esetben provisioning/
programozási adat. A táp- és adatfunkció különböző; ne állítsd, hogy egyetlen
csatlakozó szolgálja ki egyszerre az állomástápot, mindkét SDR-adatkapcsolatot
és a provisioninget. Az egyes csatlakozók szerepe/topológiája a pontos
panel ellenőrzéséig függőben marad.

Az 5 A bemeneti tápköltségvetés, amely mindkét LimeSDR USB-terhelését
tartalmazza, nem jelenti bármely különálló downstream port áramképességét.
A downstream USB-áramkorlátokat/védelmeket a hivatalos CM5 I/O-dokumentáció
és a pontos SDR-revíziók szerint ellenőrizd. A szokásos 5 V / 3 A periféria-
keret, körülbelül 600 mA USB-terhelési kerettel, önmagában nem bizonyítja,
hogy két LimeSDR buszról táplálható. Egyidejű kétvevős vétel, CM5-terhelés
és audio-próba alatt mérd külön a buszterhelést és a teljes bemeneti áramot.

A külső, 12 V-osztályú akkumulátort névleges csatlakozón keresztül tápláld
be; legyen dokumentált polaritás, kulcsolt/jelölt vezetékezés,
polaritásfordítás elleni védelem és az akkumulátorhoz közeli forrásoldali
biztosíték. A kiválasztott termék dokumentációjából és terhelési
mérésekből rögzítsd az üzemi/teljesen töltött feszültséget, lekapcsolási
feszültséget, folyamatos/csúcsáramot, csatlakozónévleges értéket,
biztosíték típusát/értékét, vezeték-keresztmetszetet és védelmi működést.
Az ECO-WORTHY referenciánál a gyártó legfeljebb 14,6 V töltést és 10 V-os
kisütési lekapcsolást sorol fel; ezeket a pontos akkumulátor/BMS-
dokumentáció és a leszállított példány ellenőrzéséig nem igazolt
listaadatként kezeld. A megadott 30 A-es töltési/kisütési maximum nem
határozza meg a BMS áram/idő görbéit, a csatlakozó/vezeték terhelhetőségét,
az állomás biztosítékát vagy a biztonságos motoráramot. A biztosíték
értékét ne csak a névleges feszültségből vagy akkumulátorkapacitásból vezesd le.

Biztosíts külön szabályozott, névlegesen **12 V-os motor-meghajtósínt**
megfelelő áram- és tranziens-tartalékkal a külső akkumulátor teljes-töltés
és lekapcsolás közötti teljes feszültségtartományában; a jelölt akkumulátor
maximális töltőfeszültsége 14,6 V, nem 12 V. Ellenőrizd a tényleges
akkumulátor/BMS-határokat, valamint a pontos TMC5160 v1.5 modul és motor
feszültség-/áramhatárát a dokumentációjukból; ne kösd a nyers
akkufeszültséget a szabályozott 12 V-os sínre, és ne növeld találomra a
biztosítékot. Biztosíts külön szabályozott **5 V / 5 A-képes CM5 I/O-
bemeneti táputat** az akkumulátorról, ha ezt fagyasztja be a hivatalos
panel; a szabályozó folyamatos/csúcsértéke, hőhatára, kimeneti védelme,
biztosíték/vezeték/csatlakozó névleges értéke, valamint a panel bemenetén
mért feszültség/polaritás legyen ellenőrzött legrosszabb terhelésnél.
Az USB-C táp/adat és PD-szerepeket csatlakozónként dokumentálni kell;
az USB-C adatkábel/port nem automatikusan tápbemenet. A 12 V-os
akkumulátort ne kösd közvetlenül 5 V-os panelbemenetre. Ne párhuzamosíts
próbapadi/USB-forrást külső akkumulátorral, és ne használd a CM5 USB-C
portját az akkumulátor/BMS töltésére külön megtervezett, jóváhagyott
töltőúttal és kompatibilis töltő nélkül. Mérd a szabályozó tartalékát,
hullámosságát, hőmérsékletét, indulási/bekapcsolási áramcsúcsát és
sínfeszültség-esését mindhárom tengely mozgása és a számítási/SDR-terhelés
közben. A kiadott tervben minden sínt/ágat védeni és biztosítani kell.

Az akkumulátor BOM-/költségnyilvántartás tartalmazza a kiválasztott külső
akkumulátort, a beépített vagy külső BMS-t/védelmet, a kompatibilis töltőt,
a szükséges kábeleket és rögzítőelemeket; ezek költsége szerepel a teljes
projektköltségben. A külső akkumulátorcsomag/BMS tömegét külön kell mérni
és jelenteni, de ki kell zárni az **5,000 kg-os állomástömeg-korlátból**.
Ha a töltőt üzemkész felszerelésként viszik, tömege beleszámít az állomásba;
egyébként külön kell megadni. Az ECO-WORTHY 30 Ah-s tétel felhasználói
referencia, nem jóváhagyott/minősített akkumulátorrendszer. A referenciaár
a [tájékoztató árak](REFERENCE-PRICES.md) között szerepel, de a végleges
ár/adó, leszállított tömeg, BMS-viselkedés, töltőkompatibilitás,
terhelőáram és autonómia még ellenőrzésre és próbára vár.

A feltételes RF-kimeneti cél 5 W FM vivő, 5 W PEP USB, 1 W AM vivő 100%-os szinuszos moduláció mellett. Ideális 100%-os AM-nél a burkolócsúcs a vivőfeszültség kétszerese, ezért a PEP a vivőteljesítmény négyszerese: 1 W vivőhöz 4 W PEP. Az 5 W PEP-lánc csak akkor kompatibilis, ha szűrő/interfész után is rendelkezésre áll a specifikált lineáris kimenet és a szükséges torzítás/headroom-tartalék; az aritmetikai 1 W különbség nem automatikusan használható tartalék. AM vivő/moduláció határát mért hullámforma/spektrum alapján állítsd, ne csak UI-értékből. Itt az FM 5 W vivő, USB 5 W PEP. AM/USB megfelelő lineáris PA-t igényel; E osztály nem alkalmas a burkolómegőrző módokhoz.

A LimeSDR Mini hozzávetőleges, frekvenciafüggő +10 dBm maximuma körülbelül 10 mW; 5 W 36,99 dBm: névlegesen körülbelül 27 dB erősítés kell a szűrő, koax, illesztetlenség és tervezési headroom előtt. Ez tervezési összehasonlítás, nem garantált gerjesztőszint vagy erősítő-specifikáció. `Pout` RF-kimenetű és `eta` drain-hatásfokú PA esetén az idealizált adási hő `Pout * (1/eta - 1)`. Feltételezett 50%-os hatásfoknál 5 W RF vivő alatt 5 W PA-hőterhelést jelent; a hatásfok, veszteségek, hullámforma-terhelés, egyidejű módok, környezeti hőmérséklet és hűtés nincs mérve. Ez nem számolja bele a két aktív vételi láncot, amelyek az engedélyezett egyetlen TX alatt bekapcsolva maradnak. A mért legrosszabb terhelés alapján méretezd az akkumulátort/DC-rendszert: `Pdc = Pout / eta` csak PA-ra, mindkét SDR, CM5, motorok, átalakítási veszteségek és csúcsok nélkül. Üzemidőt a kiválasztott akkumulátor használható kapacitása és mért terhelési profilja alapján állapítsd meg; névleges kapacitásból ne következtesd.

E példák egyetlen PA-t, akkumulátort, biztosítékot, vezetéket vagy hőtervet sem hagynak jóvá. Üzem előtt kibocsátást, hőmérsékletet, áramot és vevődeszenzitizációt névleges terhelés/csillapítás és ellenőrzött próbapadi teszt alapján állapíts meg.

A teljes üzemkész állomás megerősített szigorú tömegmaximuma 5,000 kg, beleértve állványt/fejet, szerelvényt, antennát, AZ/EL/POL rotort/motorokat, rádiókat, SBC-t, akkumulátort, kábeleket és burkolatokat. A javasolt tervezési cél legfeljebb 4,500 kg, 0,500 kg tartalékkal; ez tervezési cél, nem teszteredmény. A régi 3,130–3,200 kg becslésből kimaradt rádió és állvány, ezért nem megfelelési bizonyíték. Az új SBC, árnyékolás, SDR/PA, szűrők, hang, kábelköteg és hűtés a teljes tömeg része. A POL-motor, meghajtó/tápág, enkóder, végállások, tartó és torzióálló kábel további, nem számszerűsített tömeget ad, beleértve a mozgó szerelvényt is. Mérd le a teljes tényleges konfigurációt, vedd figyelembe a bizonytalanságot, számold újra az EL-terhet és külső súlypontot. Külön igazold a tényleges állvány/szerelvény besorolását tömegre, súlypontra, excentrikus, oldal- és csavaró terhelésre; megvásárolt állványtömeget/teherbírást nem feltételezünk.

## 6. Aláírási nyilvántartás

| Kapu | Szükséges bizonyíték | Állapot |
|---|---|---|
| G0 — hatókör/revízió | Jóváhagyott BOM, interfészdefiníciók, egyedi új panelrevízió | TARTÁS |
| G1 — mechanika | AZ/EL/POL végigjárás, külön POL NC-végállások, parkolórögzítés, backlash, kábelköteg, watchdog/tápmegszakítás, teljesállomás-leltár bizonytalansággal ≤5,000 kg, 4,500 kg célállapot, külső súlypont és állvány/szerelvény szerkezeti besorolásának bizonyítéka | TARTÁS: POL-út/hardver, tömeg/súlypont-leltár, állványbesorolás, fizikai build függőben |
| G1E — régi hordozó | Meglévő panel gyártási kiadási blokkolói és próbapadi biztonsági tesztjei lezártak | Fizikai szerelés TARTÁS |
| G2 — passzív RF | Kalibrált VNA-adat a sávfüggő 145/435 táplálásra, mindkét RHCP/LHCP-kapcsolóállapotra, axiális arányra, szűrőre, duplex/izolációra, harmonikusokra, végleges kábelkötegre | Nincs kiválasztott RF-lánc vagy kéziségkapcsoló |
| G3 — vétel/hang | RX-érzékenység/deszenzitizáció, CAT/Doppler, Bluetooth-hang folytonosság, SSTV/AX.25 vektorok; mindkét sáv mért RHCP/LHCP állapota | Szoftver/hardver-integráció függőben |
| G4 — adás | Engedély, névleges terhelés, teljesítmény/spektrum/hőmérés, háromtengelyes reteszek, RF-kapcsoló TX alatt zárva, teljes duplex deszenzitizáció bizonyítéka | TARTÁS; RF-kimeneti engedély nincs |

Minden kapunál rögzíts kezelőt, dátumot, állomásrevíziót, alkatrész-sorozat/revíziót, műszert/kalibrációs állapotot, környezetet, konfigurációt, mért adatot, megfelelt/nem felelt meg eredményt és javító lépést. „Nem mért” továbbra is függőben.
