# Architektúra és döntési napló

## Rendszerhatárok

A cél 145/435 MHz-es FM amatőr rádióállomás, nem kereskedelmi SATCOM-
terminál és nem katonai műholdrendszerek elérése. A kereskedelmi
hivatkozások nevei nem jelentik, hogy azok teljesítménye a miénkre is igaz.

```text
                         helyi böngésző
                              |
                        Wi-Fi AP / HTTP
                              |
Internet -- STA/TLS --> ESP32 -- SGP4 -- AZ/EL célértékek
kézi TLE -----------> cache       ^             |
GNSS UTC/hely -------------------+        biztonságos vezérlés
valódi észak + szint ------------+             |
NC leállító / határolók / encoderek -------- AZ/EL motorok

RT3S -- közös koax -- fém RF-diplexer -- VHF-port -- VHF-hálózat -- VHF antenna
                                      -- UHF-port -- UHF-hálózat -- UHF antenna
```

A körpolarizációs hálózat külön funkció: kvadratúra-hibrid, két
merőleges dipólus, kiegyensúlyozott táplálás és kézirány-vezérlés. Nem
helyettesíti a diplexert. Egyetlen fél-duplex adó-vevőből két antenna
összekapcsolása sem csinál teljes duplex rendszert.

## ADR-001: külön tároló

**Döntés:** új helyi Git-tároló a Documents alatt, `main` ággal.
**Indok:** a megnyitott könyvtár az Intune-hoz tartozik; nincs funkcionális
kapcsolat, ezért nem szabad összekeverni őket.
**Elvetett alternatíva:** az IDE-ben kijelölt script újrahasználata.
**Következmény:** távoli közzétételhez későbbi felhasználói lépés kell.
A felhasználó az eredeti szoftverhez MIT, a hardverhez CERN-OHL-S-2.0
licencet választott.

## ADR-002: két elektromosan különböző sáv

**Döntés:** két külön radiátor és illesztőhálózat.
**Indok:** a hullámhosszak aránya 3:1. Egy 449,55 MHz-es UHF-terv egyszeri
skálázása nem fedi le mindkét sávot ismert SWR-rel és mintázattal.
**Alternatíva:** elektromágneses modellezéssel optimalizált kétsávos Yagi.
**Következmény:** több csatlakozás; kölcsönös csatolás miatt minden portot
először külön, majd a teljes összeállításban kell mérni.

## ADR-003: kiindulásként keresztezett dipólus reflektorral

**Döntés:** eredeti paraméteres geometria, mechanikusan összecsukható,
levehető vezető alkatrészekkel. Az empirikus méretek kezdetiek.
**Indok:** olcsóbb és kisebb térfogatú, mint egy hosszú, nagy nyereségű Yagi.
**Elvetett alternatíva:** a képernyőképen látható kereskedelmi antenna
újrahasználata.
**Következmény:** STL-fájlokat nem másolunk és nyereséget nem állítunk;
a körpolarizációt és mintázatot szimulálni/tesztelni kell. Ha nem felelnek
meg, könnyű külső Yagi használható a rotorral kompatibilis interfésszel.

## ADR-004: független interfészek

**Döntés:** levehető nyerges antenna; adapterrel és fémrögzítéssel
különböző boomokat fogadó rotor; fix alapon lévő rádió; külön diplexer.
**Indok:** kézi antennahasználat, Yagi/SpaceQuad-csere vagy a rádió levétele.
**Következmény:** a MECHANIKAI univerzalitás nem jelent terhelési vagy
RF-kompatibilitást. Minden külső antennának meg kell felelnie a tömeg,
CG, szél és mozgástartomány feltételeinek.

## ADR-005: NEMA 14, nem NEMA 17/23

**Felhasználói döntés:** hordozhatóság előnyben NEMA 14-gyel.
**Indok:** kisebb tömeg, fogyasztás és térfogat.
**Következmény:** a NEMA-méret a karimát, nem a nyomatékot határozza meg.
A motort/meghajtót a valós sebességen érvényes nyomatékgörbe szerint kell
kiválasztani. A terhelést validálás korlátozza; nem ígérjük bármely
SpaceQuad antenna mozgatását.

## ADR-006: két 5:1 bolygómű

**Döntés:** mindkét fokozatban rögzített gyűrű, bemenő napkerék és kimenő
bolygóhordozó; összesen 25:1.
**Indok:** kompakt tengely és elosztott áttétel.
**Feltétel:** R=S+2P; (S+R)/bolygók száma egész. Az alapszámítás S=18,
P=27, R=72, modul=1,5; így 12 fogas napkerékhez képest elkerüli a
korrekció nélküli alámetszést.
**Következmény:** a gyűrű osztóköri átmérője 108 mm, ezért a külső
burkolóméret ennél nagyobb. Nem fér el tisztességesen 60 mm-es dobozban.

## ADR-007: valós pontosság és felbontás külön kezelése

**Döntés:** visszacsatolás/homing és kalibrálás; névleges microstep
0,0045 fok.
**Indok:** a microstepping nem szünteti meg a rugalmasságot, holtjátékot,
mágneses hibát, lépésvesztést vagy a kezdeti tájolási hibát.
**Következmény:** kezdeti végső pontossági kritérium <=2 fok RMS lassú,
szélmentes tesztben; nincs ultrapontossági ígéret.

## ADR-008: az ASA nem helyettesíti a fémet

**Döntés:** ASA vázhoz/fogaskerekekhez; tengely, csavar, persely, állványbetét
és RF-elemek fémből.
**Indok:** kedvező UV-állóság/tömeg, de anizotrop szilárdság és kúszás.
**Következmény:** a tűréseket próbadarabokkal kell beállítani; elsődleges
terhelést ne menetelj műanyagba, az ASA-t pedig ne tekintsd RF-árnyékolónak.

## ADR-009: egyenes fogak az első iterációban

**Döntés:** a kettős ferdefogazás előtt ellenőrizhető fogaskerekek.
**Indok:** könnyebb nyomtatni és beállítani; a halszálka nem garantál
nulla holtjátékot, és axiális szerelési korlátokat ad.
**Következmény:** kettős ferdefogazás későbbi változat lehet, ha mért
eredményei jobbak. A konkrét paramétereket a mechanikai kézikönyv adja.

## ADR-010: pályaszámítás az ESP32-n

**Felhasználói döntés:** helyi SGP4, tárolt TLE, érvényes óra és hely.
**Indok:** a böngésző a követés megkezdése után lekapcsolódhat.
**Elvetett alternatíva:** mobil/PC küldjön minden egyes pontot átvonulás alatt.
**Következmény:** valós pályakönyvtár, RAM-keret, katalóguskorlát és
számítási gyakoriság szükséges; az SGP4 nem helyettesíthető körpályával.

## ADR-011: az AP nem internet

**Döntés:** helyi AP mindig elérhető; opcionális STA internetkapcsolattal;
hálózat nélküli használathoz kézi TLE-import.
**Indok:** az internetkapcsolat nélküli ESP32 az AP-jén át nem tud adatot
letölteni a Celestraktól.
**Következmény:** tartós cache, látható hibák, ellenőrzött HTTPS és
TLE-nkénti adatkor. A HTML-ben kódolt ampersandokat az URL-ben `&`-re kell
normalizálni.

## ADR-012: helyzet, idő és tájolás külön állapot

**Döntés:** GNSS UTC/helyhez; kifejezetten kalibrált valódiészaki referencia
és szint; homing a mechanikai referenciához.
**Indok:** az álló GPS nem ad megbízható irányt. Motor, acél és koax melletti
magnetométer hibás irányt mutathat; a deklináció helyi és változó.
**Következmény:** kalibrálás ismert északhoz és alternatívaként vízmérték;
nincs kitalált önorientáció. Az állvány cseréje újrakalibrálást igényel.

## ADR-013: kábelhatárok és zenit

**Döntés:** nincs korlátlan AZ-forgás; fizikai és logikai határok vannak.
**Indok:** kábelvédelem és beszorulás megelőzése.
**Következmény:** a nagyobb sebességet vagy határt igénylő átvonulást
elutasítja/leállítja; tervezés nélkül nem követi a hosszabb úton. A zenit
közelében beállítható kizárási zóna van, amíg a stabil követés nem igazolt.

## ADR-014: biztonságos hibaviselkedés

**Döntés:** indításkor hatástalanított állapot, fizikai NC-leállító,
fizikai határolók, timeoutos homing, reteszelt hiba és explicit újraélesítés.
**Indok:** újraindítás vagy referencia-vesztés nem okozhat mozgást.
**Következmény:** sérült adat, érvénytelen óra, régi TLE vagy elveszett
érzékelő nem kaphat sikeres választ és közelítő mozgást sem.

## ADR-015: az RT3S önálló

**Döntés:** a rádió firmware-ét nem módosítjuk, automatikus PTT-t nem
csatlakoztatunk, és nem állítunk általános USB CAT-ot.
**Indok:** rádiócsatlakozó/programozó nem feltétlenül CAT-API.
**Következmény:** kompatibilis adatokkal OpenGD77-et kell programozni;
a rádió Doppler-korrekciója és rotor-követése külön számítás, amelyeknek
egyezniük kell.

## ADR-016: levehető RF-rekesz

**Döntés:** a korábbi diplexert fizikailag integráljuk, teszt nélkül nem
tervezzük újra.
**Indok:** a felhasználó munkájának megőrzése és az antenna/radio önálló
használhatósága.
**Következmény:** a korábbi projekt tényleges méreteit, kapcsolását,
leválasztását és teljesítményét tartóvágás vagy TX előtt ellenőrizni kell.

## ADR-017: nem tanúsított tömegcél

**Döntés:** a teljes prototípust mérjük, ne csak a filament grammjait adjuk össze.
**Indok:** motor, csapágy, tengely, akkumulátor, koax és csatlakozó a fő
tömegforrás.
**Következmény:** a <=3 kg-os korábbi cél a rádiót és állványt kizárta,
az állomás értékelésekor a tápot beleszámította; túllépés esetén rögzítés
és újratervezés szükséges.

## ADR-018: kapuk szerinti validálás

**Döntés:** G0 szoftver/CAD, G1 mechanika RF nélkül, G2 passzív RF,
G3 vétel, G4 engedélyezett adás.
**Indok:** STL vagy unit teszt nem garantál működő berendezést.
**Következmény:** G1–G4 teljesítése előtt ne nevezd terepkésznek;
a blokkolókat tüntesd fel, ne rejtsd el.

## ADR-019: a tömeg előnyben az áttétel típusával szemben

**A felhasználó által jóváhagyott revízió:** <=3 kg előnyben; a bolygómű
könnyebb áttételre cserélhető AZ/EL-követés megtartásával.
**Bizonyíték:** korlátozott könnyítés után is 2,521 kg tömör ASA-egyenérték;
nyomtatott alkatrészekkel és akkumulátorral hipotetikusan 3,208–4,038 kg.
A régi cél nem teljesül.
**Döntés:** BASE két, sorba kapcsolt GT2 20:100 szíjfokozattal, összesen
25:1; a bolygómű LEGACY. A valós áttételt a firmware-rel össze kell hangolni.
**A felhasználó által elvetett alternatíva:** a jelenlegi bolygóműves tömeg
elfogadása.
**Következmény:** újra kell értékelni a merevséget, holtjátékot, feszítést,
határokat és a táp nélküli viselkedést. A szíj visszahajtható, nem EL-fék.
Mérés előtt ne állíts <=3 kg-ot, és ne helyettesítsd a teljes
költségkeretet néhány STL tömegével.

A kezdeti digitális BASE-eredmény: 0,862 kg tömör ASA-egyenérték.
A teljes keret 3,121–4,006 kg; könnyített hipotetikus forgatókönyv
2,905–3,790 kg. A <=3 kg cél nyitott: a kereten belüli komponensek
kiválasztása és a teljes egység lemérése kell, nem egy becslés alsó
szélének sikerként kijelentése.

## ADR-020: javítható hordozó-nyomtatott áramköri lap és ellenőrizhető Gerber

**A felhasználó által kért bővítés:** saját vezérlőpanel GNSS-, tengely-/
tájolásérzékelő-, motor-, táp- és védelmi csatlakozókkal, valamint
gyártási Gerber-fájlokkal.
**Kifejezett választás:** cserélhető modulokat hordozó panel; nem
diszkrét IC-ként beforrasztott ESP32/meghajtó/GNSS.
**Indok:** helyszíni javíthatóság, kisebb kockázat és költség az első
iterációban.
**Döntés:** szerkeszthető kapcsolási rajz/PCB, firmware-rel egyező GPIO-
térkép, tervezési szabályok, Gerber/Excellon-kimenet és konkrét
hivatkozásokat tartalmazó BOM.
**Következmény:** a modulok PONTOS típusát és méreteit kell ellenőrizni.
Egy általános DevKit vagy StepStick név nem igazolja az elektromos
kompatibilitást. A motor-táp szoftvertől függetlenül legyen megszakítható;
a logika hibajelzéshez feszültség alatt maradhat.
**Korlát:** a fájlok puszta létezése nem jelent gyártási kiadást; ERC/DRC,
lábnyom, áram, leválasztás, folytonosság és próbapadi teszt külön kapuk.
Opcionális tájolásérzékelőről ne állítsd, hogy firmware-ben megvalósult,
csak mert van csatlakozó. Az álló GNSS továbbra sem ad valódi északot.

## ADR-021: Bricohams-jelölés nyomtatása

**A felhasználó kifejezett választása:** a `BRICOHAMS` szöveg és
`bricohams.org` domború, a vezérlődoboz fedelébe integrált megjelenítése.
**Döntés:** a fedél geometriájához kapcsolt, paraméteres mélységű és
pozíciójú felirat, csavaroktól, szellőzőtől és csatlakozóktól távol.
A módosítás után újra kell generálni az STL-t és ellenőrizni a hálót.
**Indok:** tartós azonosítás matrica vagy külön alkatrész nélkül.
**Korlát:** nem reprodukálunk be nem nyújtott hivatalos logót; a szöveges
védjegy nem jelent tanúsítást vagy harmadik fél jóváhagyását.

## ADR-022: vezetett kalibráció és Android BLE

**Kifejezett bővítés:** webes felületű kalibráció és natív Android-
alkalmazás Bluetooth-vezérléshez; a felhasználó BLE-t választott.
**Döntés:** közös vezérlési, hitelesítési és állapotprotokoll; ne legyenek
olyan duplikált parancsok, amelyek más átvitelen megkerülhetik a
reteszeléseket. A kalibrálás külön kezeli a homingot, hely/UTC-t, szintet és
valódi északot, állapotvalidálással és kifejezett fizikai jóváhagyással.
**Következmény:** ki kell értékelni az ESP32-WROOM-32E memóriáját és
Wi-Fi/BLE-együttélését; a BLE hozzáadása után újra kell fordítani és
validálni a WebFlash-t. Az alkalmazás csatlakozáskor nem élesít motort,
és nem helyettesíti a fizikai leállítót.

## ADR-023: a telefon TLE-híd, a rotor a számító

**Kifejezett választás:** az alkalmazás HTTPS-en TLE-t tölt le, BLE-n
továbbítja; az ESP32 önállóan számítja az SGP4-átvonulást/követést.
Az alkalmazás lekérdezi és megjeleníti az eredményt. Telefonon számolt
pályát nem küldünk át.
**Indok:** terepen frissíthető adat a mobilinternet segítségével anélkül,
hogy feltételeznénk, hogy a rotor AP-ja internetet ad.
**Következmény:** korlátozott, töredékes és atomikus átvitel; TLE-validálás
mindkét oldalon; látható hibák; mozgás alatt cache-frissítés tiltása.
A TLE-lista nem ad műholdfrekvenciát vagy valódi állványirányt.
A telefon kapcsolatvesztése nem alakítja az autonóm követést kézi vezérléssé,
és önmagában nem érvényteleníti az átvonulást; a rotor biztonsági szabályzata
és az UTC/hely/érzékelők érvényessége az irányadó.

## ADR-024: moduláris, multimódusú műholdas rádióbővítés

**Kifejezett választás:** cserélhető RF-modulos, integrált 145/435 MHz-es
teljes duplex rádió, CAT/Doppler és vezérlés ugyanabból az APK-ból. A
későbbi kérés AM-et és SSB/USB-t is hozzáad, felváltva a köztes, kizárólag
FM-es választást.
**Döntés:** modulválasztás vagy Gerbergyártás előtt igazolni kell a valódi
multimódusú architektúrát. A rádió maradjon levehető, a rotor/antenna
független. A már validált rotorpanel ettől még nem validált RF-/audio-
panel, és nem kap automatikusan más lábkiosztást.
**Indok:** (tr)uSDX és uSDX SOTA HF-modularitás/CAT-hivatkozás, nem
145/435 MHz-es RF-lánc. Az ATU-100 nem adó-vevő vagy diplexer.
**Következmény:** újra kell vizsgálni költséget, tömeget, fogyasztást,
árnyékolást és RX/TX-leválasztást; két beállított frekvencia nem bizonyít
teljes duplexet.

## ADR-025: audio, SSTV és APRS-üzenetek

**Kifejezett választások:** kétirányú Bluetooth-audio, beépített hangszóró
és mikrofon, külső Baofeng-típusú csatlakozó, ISS PD120/PD180 SSTV,
AX.25 Bell202 AFSK1200 és hívójelek közti APRS-üzenetek.
**Döntés:** az audio átlátszó, a jelenlegi vezérlő-BLE-től különálló
kapcsolat; az audio nem tulajdonítható a rotor 20 bájtos keretprotokolljának.
A tartozék pontos modelljét és lábkiosztását ellenőrizni kell, mielőtt
Baofeng-kompatibilisnek nevezzük. BTL-hangszórókimenetet ne köss közvetlenül
jack-földre.
**Indok:** a hangkompresszió, AGC és zajelnyomás megváltoztathatja a
dekódoláshoz szükséges hangokat. A hangfolytonosság és az adatátviteli
sebesség/együttélés tesztje a vezérlés hitelesítése mellett szükséges.
**Következmény:** a PCM-dekódolást/-kódolást RF-től függetlenül lehet
ellenőrizni; WAV létrehozása nem jelent adást. A távoli APRS-ACK nem azonos
a helyi átviteli ACK-val. Nincs mobilhálózati SMS-átjáró vagy műholdas
kézbesítési garancia. Hiba, lejárat vagy kapcsolatbontás esetén a PTT-nek
vételi állapotba kell esnie.

## ADR-026: egységes SBC és új hordozópanel értékelése

**Későbbi kérés:** Raspberry Pi Zero vagy hasonló a rádióhoz, audióhoz,
követéshez és rotorhoz, az ESP32 elhagyásával, ha megvalósítható.
**Ideiglenes döntés:** erőforrások/portok és a Linux nem determinisztikus
ütemezésétől független mozgásgenerálás felmérése. Python/Linux ciklusból
ne adj STEP-impulzust, majd nevezd pontosnak. Vizsgálj beépített
rámpagenerátoros meghajtót, független fizikai tápmegszakítást és watchdogot;
kapcsolási rajz előtt az eszközöket/regisztereket ellenőrizd.
**Következmény:** az ESP32 elhagyását teszt nem hagyta jóvá; az új
PCB/Gerber identitása/revíziója legyen külön az eredeti hordozótól.
Linux-indítás, Bluetooth-hiba vagy blokkolt folyamat nem tarthat fenn PTT-t
vagy veszélyes mozgást. A korábbi ESP32 WebFlash nem telepít Raspberry Pi
rendszert; választás esetén külön beállítási eljárást kell dokumentálni.

## ADR-027: harmadik POL-tengely és külön körpolarizáció-kapcsolás

**Kifejezett választás:** korlátozott tengely körüli forgás és külön
RHCP/LHCP RF-kapcsolás kompatibilis körpolarizált antennához.
**Döntés:** új AZ/EL/POL-változat harmadik motorral, határolókkal, hominggal
és kalibrált pozícióval. A többlet forgó tömeg, CG, kábelcsavarás, energia
és szerkezet miatt újra kell számítani az EL/AZ-terhet; a POL út és áttétel
saját specifikációt igényel, nem szabad automatikusan átvenni a 25:1-et.
**Indok:** a POL lineáris polarizációt orientálhat; a tengely körüli
forgatás nem fordítja meg a körpolarizáció kézirányát. RHCP/LHCP-t sávonként
ellenőrzött fázis-/táplálóhálózattal, adás közben tiltva kell választani.
**Következmény:** ne engedélyezz alapértelmezetten folyamatos forgást,
RF-forgócsatlakozást vagy harmadik meghajtót. A kétmotoros régi hordozó
nem teljesíti az új igényt. A korábbi keret már meghaladta a 3 kg-ot; az új
tengely más újratervezés és mérés nélkül nem állítja helyre ezt a célt.

## ADR-028: teljes tömeg és új változat érzékelői

**Kifejezett választás:** 5 kg korlát az állvánnyal és valamennyi üzemkész
elemmel együtt; ez felváltja a korábbi, kizárásokat tartalmazó 3 kg-ot.
**Döntés:** teljes, lemért leltár és javasolt 500 g tartalék (belső cél
4,5 kg); ismeretlen alkatrészekre nincs kitalált költségvetés. GNSS a
helyhez/UTC-hez, kalibrált magnetométer deklinációval az irányhoz, IMU a
dőléshez, független encoder az AZ/EL/POL tengelyhez.
**Indok:** az álló GPS nem ad északot, az iránytű nem ad tengelypozíciót;
a motorok/áramok megváltoztatják a mágneses teret.
**Következmény:** az új PCB/dokumentáció foglalja magában az érzékelők
tömegét, tápját, csatlakozását, szerelését és tesztjét; három AS5600
közös I2C-címét meg kell oldani. Rajz alapján ne állítsd, hogy PPS,
iránytű vagy encoder működik. Az érvényességi hiba legyen látható és tiltsa
a rá épülő funkciót; a kézi kalibráció kifejezett, ellenőrzött eljárás, nem
csendes helyettesítő.

## ADR-029: SMA RF-interfészek

**Kifejezett választás:** hagyományos, 50 ohmos SMA a rádió, antenna,
diplexer és polarizációs hálózat tömegének/térfogatának csökkentésére.
**Döntés:** nincs RP-SMA, BNC/N adapter és húzásmentesítés nélküli koax-
rögzítés a PCB-n; alkatrészenként ellenőrizni kell a középérintkezőt és
csatlakozási nemet.
**Következmény:** a lábnyom/méret és besorolás a tényleges csatlakozótól
függ; a tömegcsökkenést mérni kell. SMA nem alkalmazható tápra,
érzékelőre vagy mikrofon/hangszóró tartozékra. A régi BNC-változatok
történeti referenciák, nem az új bővítés RF-interfészei.

## ADR-030: CM5 és cserélhető, teljes duplex SDR

**Kifejezett választás:** Raspberry Pi Compute Module 5 és LimeSDR Mini.
A felhasználó megerősítette a teljes duplex/adás igényét, miután tisztáztuk,
hogy az RTL-SDR Blog V4 kizárólag vevő.
**Döntés:** CM5 számításhoz/vezérléshez/audióhoz és egy független RX/TX-
láncú SDR; ez váltja fel a köztes Zero/Pi4 és két modul javaslatokat.
**Következmény:** CM5-hordozópanel vagy több wattos RF-teljesítmény még
nincs validálva. A revíziót, hűtést, nagysebességű USB-t, tápot, lineáris
PA-kat és szűrőket teszteléssel kell kiválasztani. A korábbi ESP32-rotor
csak külön történeti változatként marad meg.

## ADR-031: más alkalmazások által inspirált Android-hatókör

**Kifejezett választás:** első változat katalógussal/átvonulásokkal,
térképpel/radarral, riasztásokkal, frekvenciával/Dopplerrel, AZ/EL/POL-
vezérléssel, ISS PD120/PD180 SSTV-vel és APRS-üzenetekkel; nincs teljes
Look4Sat/Robot36-egyezés.
**Döntés:** funkció/állapot/tesztmátrix, eredeti implementáció és licenc-
felülvizsgálat könyvtár/eszköz újrahasználata előtt.
**Következmény:** valós pályaadat nélküli térkép nem bizonyít követést;
szintetikus kép DSP-teszt, nem RF-vétel. Android-riasztás engedélyektől,
órától és rendszerkorlátoktól függ.

## ADR-032: két SDR egyidejű kétsávos vételhez

**Későbbi kifejezett választás:** két LimeSDR Mini, nem Lime + RTL-SDR;
ez felváltja az ADR-030 egy SDR-es köztes választását.
**Döntés:** sorszámmal azonosított VHF-lánc és UHF-lánc, két egyidejű vevő,
mindkét láncon adási képességgel. Kezdeti konzervatív szabályzat: egyszerre
csak egy TX aktív, két egyidejű adásra nincs feltételezett engedély.
Kifejezetten válaszd ki, hogy a VHF/UHF audio melyik dekóderhez menjen;
két hangcsatornát ne keverj össze.
**Következmény:** újra kell számolni az USB-t, fogyasztást, hőt, tömeget,
szűrést és mindkét vevő védelmét. Két csatlakozó/szoftverpéldány nem
bizonyítja, hogy adás közben is egyidejű a vétel.

## ADR-033: hivatalos CM5IO és saját kiegészítő PCBA

**Kifejezett választás:** megvásárolt hivatalos CM5IO és saját
JLCPCB-gerber/BOM/CPL kiegészítőpanel. E revízióhoz elvetjük az egyedi,
nagysebességű, egységes CM5-hordozópanelt.
**Döntés:** a CM5IO adja a CM5-rögzítést és két natív USB3-portot; a saját
kiegészítő három meghajtót, érzékelőket és reteszeléseket kezel, ellenőrzött
interfészekkel. Hivatalos fájlokat ne terjessz a projekt licence alatt.
**Következmény:** a CM5IO-t, hűtést, kábelezést és kiegészítőpanelt a
tömeg-/árkeretbe bele kell venni. Harmadik USB-audioeszközhöz meghatározott
host/hub kell; két foglalt USB-port nem hagy képzelt harmadik portot.
Ha a kiegészítő 3,3 V-os logikát használ, a CM5IO VIO-t 3,3 V-ra kell
állítani; az 1,8 V-os választás nem csereszabatos interfész-felülvizsgálat
nélkül.

## ADR-034: USB-C és külső akkumulátor

**Kifejezett választások:** USB-C előnyben részesítése tápra és adatra az
SMA RF és a K1 hang megtartása mellett; a külső akkumulátor kizárása az
5 kg-os határból. A kétórás cél megmarad, és 12 V/1 Ah-nál nagyobb külső
akkumulátor megengedett.
**Döntés:** az akkumulátor szállított tömegét külön kell rögzíteni,
költségét bele kell venni a projekt költségvetésébe, áramát/energiáját/
szabályozását pedig a tényleges fogyasztás alapján kell méretezni.
12 Wh névleges energia veszteség előtt csak 6 W átlagteljesítményt enged
két órán át; ezt nem szabad elegendőnek nyilvánítani. Az egyetlen tömeg-
kizárás az akkumulátor; az állvány, rádió és kábelek nem zárhatók ki.
Ellenőrizni kell az USB-C/PD portonkénti feszültségét és szerepét; 12 V
nem köthető közvetlenül az 5 V-os CM5-sínre.

## ADR-035: modulonkénti építés és szoftver

**Kifejezett kérés:** az antenna, rotor és rádió dokumentációja és
összeszerelése legyen önálló, továbbá készüljön általános, ábrákkal
kiegészített kézikönyv.
**Döntés:** négy belépési pont: MODULE-ANTENNA, MODULE-ROTOR,
MODULE-RADIO és MODULE-INTEGRATED; rotor-only, radio-only és integrated
profilok nem támaszkodhatnak nem létező hardverfüggőségekre.
**Következmény:** az önálló, kézi rádióüzem nem igényel rotort/SGP4-et,
de megköveteli a valódi TX-engedélyt és RF-utat; az integrált Doppler nem
eshet át csendben kézi módba. A rotor önállóan nem indít SDR-t és nem
függ hangtól. Az antenna önállóan nem igényel számítógépet. Az integrált
BOM megszünteti a CM5/hordozó/táp duplikálását, miközben a megosztott
alkatrészek nyomon követhetők maradnak.
