# Követelmények és nyomon követhetőség

| ID | Követelmény | Megvalósítás / bizonyíték | Elfogadás |
| --- | --- | --- | --- |
| R01 | 145/435 antenna | CAD és RF-AND-RADIO | VNA mindkét sávon, összeszerelve |
| R02 | Összecsukható, hordozható | MECHANICAL, levehető alkatrészek | Teljes csomag méretének és tömegének mérése |
| R03 | AZ/EL-követés | CONTROL, SGP4 | Pályareferencia és két tengelyes próbapad |
| R04 | Mobil nélküli önállóság | ESP32-ben végzett számítás | Böngésző bezárása követés közben |
| R05 | AP webes felület | web és firmware | Internet nélküli elérés mobilról |
| R06 | TLE frissítése | STA/TLS/import | Látható hiba és konzisztens cache |
| R07 | UTC-helyzet | GNSS és érvényességi állapot | Újraindítás, fix hiánya, óra elvesztése |
| R08 | Tájolás/szintezés | Külön valódi kalibráció | Mért szöghiba |
| R09 | RT3S OpenGD77 | Tartó és önálló üzem | Valós verzió és csatornák ellenőrzése |
| R10 | Korábbi diplexer | Moduláris RF-integráció | Méretek és S-paraméterek megerősítése |
| R11 | Fényképezőgép-állvány | Fém betét | Terhelési és torziós próba |
| R12 | Cserélhető antennák | Boomadapterek | Tömeg/CG ellenőrzése antennánként |
| R13 | NEMA14/25:1/ASA | CAD, számítások | Kézi forgatás, nyomaték, melegedés |
| R14 | Mozgásbiztonság | NC, határolók, hibakezelés | Fizikai leállítás böngésző nélkül |
| R15 | Git és dokumentáció | Független tároló | Tartós fájlok és előzmények |
| R16 | Költségkeret alacsonyan tartása | Tájékoztató BOM | Helyi ajánlat, kitalált árak nélkül |
| R17 | Referenciaanyagok | SOURCES, REFERENCE-ANALYSIS | PDF-enkénti hivatkozások és licenckorlátok |
| R18 | Hordozó PCB és Gerber | hardware, fabrication, PCB | ERC/DRC és hálózatok, lábnyom/áram ellenőrizve |
| R19 | Csatlakoztatható érzékelők | Közös PCB/CONTROL térkép | Két AS5600 címütközés nélkül és GNSS |
| R20 | Tápvédelem | Biztosíték, polaritás, túlfeszültség, motorlekapcsolás | Elektromos tesztek motor/RF előtt |
| R21 | Vezetett webes kalibráció | UI és közös vezérlés | Homing/észak/szint és egyértelmű hibák |
| R22 | Android BLE-alkalmazás | android, firmware BLE | Párosítás/auth, engedélyek és telefonos teszt |
| R23 | TLE telefonon át | HTTPS-letöltés, atomikus BLE-átvitel | Érvényes katalógus, hibák és csonkításmentes cache |
| R24 | Rotor által számolt átvonulások az alkalmazásban | ESP32 SGP4 és BLE-lekérdezés | Nincs telefonfüggőség átvonulás közben |
| R25 | Integrált 145/435 teljes duplex FM, AM és SSB/USB rádió | Kért bővítés; multimódusú RF-architektúra ellenőrzendő | Vétel adás közben mindkét sávkombináción, mért spektrum és deszenzitizáció |
| R26 | CAT és Doppler ugyanabban az APK-ban | Integráció függőben; RT3S-nek ne tulajdoníts CAT-ot | Valós TX/RX-frekvencia, visszajelzés és hibák/reteszelések |
| R27 | SSTV PD120/PD180 Androidon | Helyi audio-dekóder fejlesztése | Ismert PCM-vektorok és kép, majd rádiós próba |
| R28 | AX.25 AFSK1200 és APRS | Dekódolás és állomásjel-hívójelek közti üzenetek fejlesztése | Valós CRC, NRZI, bit stuffing, címzett, ID és ACK |
| R29 | Kétirányú Bluetooth-audio | A rotor aktuális BLE-jétől független átlátszó kapcsolat | Mintafolytonosság, látható veszteség, késleltetés és együttélés |
| R30 | Beépített hangszóró/mikrofon, Baofeng-típusú tartozék | Audio-interfész és panel függőben | Pontos tartozék lábkiosztása, bias, PTT, leválasztás és visszacsatolásmentesség |
| R31 | APRS-üzenet rádiós küldése | Moduláció és RF-átvitel külön validálandó | Hanggenerálás nem jelent elküldést, távoli ACK nélkül nincs kézbesítés |
| R32 | Raspberry Pi Zero vagy hasonló értékelése rádióhoz/rotorhoz ESP32 nélkül | Megvalósíthatósági igény; nincs jóváhagyott SBC-választás vagy teszt | USB/CPU/RAM/Bluetooth mérése, determinisztikus mozgásgenerálás és az operációs rendszertől független leállítás |
| R33 | PCB/Gerber és teljes dokumentáció frissítése | Új revízió a modulok/SBC kiválasztásához kötve | ERC/DRC, lábnyom/lábkiosztás, áram, audio, RF, mechanika; a korábbi ESP32-panel jóváhagyása nem használható |
| R34 | Harmadik, korlátozott POL-tengely | Hárommotoros mechanikai/vezérlési terv fejlesztés alatt | Út, homing, NC-határok, encoder, kábelek, tömeg/CG és nyomaték validálva |
| R35 | RHCP/LHCP RF-kapcsolás | A POL-forgástól független, kompatibilis körpolarizált antennához kötött | Fázis/amplitúdó, tengelyarány, leválasztás és adás nélküli kapcsolás mindkét sávon |
| R36 | Teljes tömeg <=5 kg | Felváltja a korábbi, kizárásokat tartalmazó 3 kg-os korlátot | Antenna, három tengely, rádió/SBC, doboz, érzékelők, akku, kábelek és állvány együtt mérve |
| R37 | GNSS, iránytű és dőlés az új változatban | GNSS/UTC, magnetométer és IMU, valamint AZ/EL/POL encoderek | Kalibráció, deklináció/valódi észak, interferencia, látható érvényesség és biztonságos hibareakció |
| R38 | 50 ohmos SMA RF-csatlakozók | Antenna, rádió, diplexer és RHCP/LHCP-hálózatok; RP-SMA és BNC/N adapterlánc kizárva az új változatból | Nem, érintkező, lábnyom, teljesítmény, koax, húzásmentesítés és tömeg ellenőrizve; audio/táp nem SMA |
| R39 | CM5 + LimeSDR Mini, ESP32 nélkül | Később kiválasztott architektúra; cserélhető, teljes duplex RF-modul | Hordozópanel, USB, erőforrás, teljesítmény/akku, hűtés és független leállítás tesztelve |
| R40 | Look4Sat/Robot36 által inspirált Android-funkciók | Elsőként választott verzió: katalógus/átvonulások, térkép/radar, értesítések, frekvencia/Doppler, három tengely, PD120/180 és APRS | Funkciónkénti mátrix és tesztek; nincs teljes paritás vagy licenc nélküli felület-/kódmásolás |
| R41 | Két LimeSDR Mini VHF/UHF egyidejű vételéhez | Felváltja a köztes, egy SDR-es választást; mindkét lánc képes adásra | Sorozatszám szerinti egyértelmű azonosítás, két valós stream, audióválasztás, szűrés és deszenzitizáció; kezdetben csak egy aktív TX |
| R42 | Spanyol, angol és magyar dokumentáció | Teljes, szinkronizált kiadások; szójegyzék, ábrák/feliratok, szerelés, figyelmeztetések és indoklások | Dokumentumonkénti lefedettség, hivatkozások és forrásrevízió/hash; eredeti licencek módosítás nélkül |
| R43 | Minden alkatrész/anyag tájékoztató ára | Mennyiséget, modellt, dátumot, EUR-forrásokat, összehasonlítható átlagot, ÁFÁ-t/szállítást és külön szerszámokat tartalmazó BOM | Részösszegek és lefedettség ellenőrzése; függő ár/tartalék nem vásárlás és nem nulla költség |
| R44 | Ábrák a szerelési útmutatóban | Lépésekhez kapcsolt ábrák és BOM-azonosítós alkatrésztérkép | Alkatrész/anyag/lépés megfeleltetése, rajzrevízió és a koncepcionális rajz korlátai |
| R45 | JLCPCB Gerber + BOM + CPL csomag | Valós Gerber/fúrófájlok, pontos LCSC-azonosítós BOM, mm/oldal/elforgatás adatú CPL és kézi/DNP-lista | ERC/DRC/összeköttetések; referenciajelölők, origó, tájolás és beszállítói kódok egyezése; alapértelmezés szerint nincs megrendelés vagy fizikai kiadás |
| R46 | USB-C tápellátáshoz és adatkapcsolathoz | Megerősített preferencia; az RF SMA és a K1 hanginterfész megmarad | Portszerep/-sebesség és táp, PD/kábel/áramkorlát ellenőrizve; nem kerülhet inkompatibilis feszültség a CM5-re |
| R47 | Külső akkumulátor kizárása az 5 kg-os határból | Felváltja az akkumulátor korábbi beszámítását; a külső kapacitás méretezésével legalább 2 óra fenntartása | Külső tömeg és költség külön; hasznos energia/áram és szabályozás igazolva; 12 Wh nem bizonyít 2 órát |
| R48 | Egyedi BricoHams operációs rendszer | Hivatalos ARM64 Raspberry Pi OS, márkajelzés/banner, projektkomponensek és -szolgáltatások, biztonságos helyi konfiguráció | Reprodukálható forrás/verzió, a ténylegesen megépített image elkülönítve a recepttől, CM5-boot, függőségek és jogosultságok; megosztott hitelesítő adat és automatikus felfegyverzés nélkül |
| R49 | Powerpole és elosztó-biztosítékok | Külső 12 V-os Powerpole-bemenet, akkumulátor melletti főbiztosíték, valamint CM5/motor/RF ágak biztosítékai | Polaritás, krimp/vezeték-keresztmetszet, DC/megszakítóképesség, idő–áram görbe/áram/bekapcsolási csúcs, hőmérséklet és koordináció; a BMS nem helyettesíti a biztosítékot |
| R50 | Tápoldali EMI-szűrők értékelése | Csillapított közös/differenciális módú szűrés, leválasztókondenzátorok és az ágak elkülönítése | Mért áram, telítődés, egyenáramú ellenállás/feszültségesés, szabályozóstabilitás, bekapcsolási csúcs/tranziensek és vett zaj; a DC-szűrő nem azonos az RX/TX-leválasztással |
| R51 | Független modulok és általános útmutató | Saját anyag-/szerelési-/konfigurációs útmutató az antennához, rotorhoz és rádió-SDR-hez; külön ábrázolt integráció | Rotor telepítése SDR nélkül, kézi rádió rotor nélkül, antenna szoftver nélkül; közös BOM duplikált CM5/táp tételek nélkül |

Az R25–R31 bővítés felváltja az új rádió korábbi, csak FM-es köztes
választását, de megőrzi az első kiadás önálló RT3S/rotor működését. Nem
teszi az FM-modulokat SSB-képessé, és az alkalmazásvezérlők jelenléte nem
jelenti RF-lánc megvalósítását. Új PCB/doboz kiadása előtt újra kell
nyitni a tömeg, fogyasztás, hűtés és költség kérdését. Az egységes SBC-re
vonatkozó későbbi kérés újranyitja az ESP32 megtartásáról szóló döntést:
ez értékelés, nem már igazolt csere.

## Az első iteráció nem céljai

- Katonai SATCOM-lefedettség vagy kompatibilitás a fényképen látható
  kereskedelmi antennával.
- Teljes duplex RT3S-sel; SSB FM/DMR-rádióval.
- Bármely SpaceQuad antenna mozgatása terhelés-ellenőrzés nélkül vagy
  kalibrálás nélküli telepítése.
- Nyomtatott alkatrészekkel, tesztek nélkül garantált, egy fok alatti pontosság.
- Korlátlan tápellátás, tanúsított IP-vízállóság vagy bármilyen széllel
  szembeni ellenállás.
- CAT/PTT automatizálása ellenőrizetlen protokollal.

## Valós készülékről szükséges adatok

A konkrét motor és nyomatékgörbéje, RT3S méretei akkumulátorral/tokkal,
csatlakozók és koax mérése, állvány típusa és megengedett terhelése,
a diplexer VNA-mérése, kiválasztott tápegység, nyomtató tűrései, valós
tömeg/CG, és az új iránytű beépítése esetén a helyi mágneses tér.
