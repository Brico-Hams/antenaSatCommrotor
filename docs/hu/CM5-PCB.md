# CM5IO kiegészítő vezérlő-NYÁK

## Hatókör és kiadási állapot

Ez az eredeti kiegészítő vezérlőpanel a hivatalos Raspberry Pi Compute Module 5 IO Board 2. revíziójához (CM5IO rev 2) készül. A CM5 a CM5IO panelen marad; ez a NYÁK kizárólag annak 40 tűs GPIO-fejléchez csatlakozik. Nem önálló CM5-hordozópanel, nem másolja le, és nem függ a CM5 nagysebességű panelközi csatlakozójának tűkiosztásától.

A kiválasztott CM5-jelölt **CM5104016** (vezeték nélküli, 4 GB RAM, 16 GB eMMC). A pontos CM5 SKU beszerzési megerősítése még hátravan; ez nem módosítja a kizárólag GPIO-t használó interfészt. A panel csatlakoztatása előtt állítsd a CM5IO 40 tűs fejlécének VIO jumperét **3,3 V-ra**. 1,8 V-os fejléc-konfigurációt ne csatlakoztass.

A két LimeSDR Mini eszköz a CM5IO rev 2 két natív USB 3 portját foglalja el. Az USB 3 jelek közül egy sem halad át a kiegészítőpanelen. A CM5IO külön USB-C tápbemenettel és külön USB-adat/gazdacsatlakozókkal rendelkezik; ezek nem egyetlen, közös táp- és adatkapcsolatot jelentenek, és egyik csatlakoztatása sem garantálja a másik elérhetőségét vagy gazdaképességét. Az 5 V / 5 A csak tápellátási cél: a forrásnak egyeztetnie kell a szükséges USB-C PD-szerződést, a CM5IO bemeneti útjának támogatnia kell azt, és meg kell mérni a teljes egyidejű terhelést. Az 5 V / 3 A forrás nem elfogadható ehhez a tervhez: a két LimeSDR Mini periféria a megadott, egyenként 600 mA-es terhelésével már 1,2 A-t igényel, így csúcsok előtt legfeljebb 1,8 A marad a CM5-re, a CM5IO veszteségeire és az összes többi fogyasztóra. Az 5 A felirat önmagában nem elegendő: ellenőrizd az egyeztetett szerződést, és ahol az áramigény megköveteli, használj megfelelő névleges értékű, 5 A-es e-markerrel ellátott USB-C kábelt. Ne feltételezd, hogy egy tetszőleges USB-C csatlakozó vagy kábel 5 A-t támogat.

A kiegészítőpanel táp-, USB-adat- és RF-interfészeit tartsd elkülönítve. A két LimeSDR Mini tápját ne a panel 40 tűs fejlécének 5 V-os sínjéről vedd, és USB-adatukat ne vezesd át a kiegészítőpanelen. A hang célkonfigurációja a beépített hangszóró- és mikrofonhang USB-kodeken keresztül, továbbá egy különálló, még nem minősített, Kenwood-stílusú K1 kettős 3,5 mm / 2,5 mm tartozékinterfész UV-5R/UV-82-kompatibilis kiegészítőkhöz. Ez kompatibilitási cél, nem ellenőrzött rádió-/tartozéktű-kiosztás. A hangcsatlakozó külön, DNP-ként kezelt leánykártyára kerüljön; annak összekötő fejléce, tűkiosztása és kábelkötege maradjon befagyasztatlan, amíg a tényleges rádióval és tartozékkal nincs ellenőrizve. A BTL (busy-tone lamp, foglaltságjelző lámpa) érintkezőt soha ne tekintsd automatikusan földnek, és ne kösd hangföldre. A hang-visszavezetés kizárólag az igazolt, földreferenciás hangmeghajtó visszavezetésére csatlakozhat; a BTL-érintkezőtől külön kell tartani, hacsak a pontos tartozékáramkört nem ellenőrizték. Ezen a NYÁK-on a hangot ne csatlakoztasd RF-, PTT-, motor- vagy végállás-hálózatra.

Ha léteznek digitális tervfájlok, azok önmagukban nem jelentenek gyártási kiadást. A Gerber-, Excellon-, BOM- és CPL-exportot ugyanazon ellenőrzött panelrevízióból kell előállítani. A PCBA kiadásához a KiCad ERC/DRC/összeköttetési/paritásvizsgálatokban nulla hiba, ellenőrzött beültetési cikkszámok és footprintök, valamint az alábbi felülvizsgálati tételek lezárása szükséges. Ez a terv nem engedélyez megrendelést, feltöltést vagy fizikai tesztet. Nem állít semmilyen tömeget, követési pontosságot, RF-teljesítményt, motornyomatékot, hőtartalékot vagy 5 kg-os teljesállomás-eredményt.

## Külső akkumulátor, Powerpole és tápátalakítási szerződés

A tápforrás **12 V névleges** interfészű külső akkumulátor; az akkumulátorcsomag nem része az 5 kg-os berendezéstömeg-célnak. Referenciaként az ECO-WORTHY 12 V 30 Ah LiFePO4 termékváltozat szerepel: `40308275183822` ([gyártói/forgalmazói lista](https://es.eco-worthy.com/products/bateria-litio-lifepo4-12v-30ah?currency=EUR&country=ES&variant=40308275183822)). Ez jelölt, nem beszerzési vagy akkumulátor-elektromos befagyasztás: felhasználás előtt ellenőrizd a ténylegesen szállított modellt, a 30 Ah kapacitást, a belső BMS-határokat, a folyamatos/csúcsáramot, a csatlakozót és az adatlapot. Ne feltételezd, hogy a terméklista megadja a töltőfeszültséget, a lekapcsolási értéket vagy a maximális terhelést. A LiFePO4 teljes töltési feszültségeként megadott **14,6 V csak előzetes érték**; alkatrész-terhelési szűrésre is csak az adott csomag megerősítése után használható. Addig a kémiához tartozó felső/alsó feszültség és minden névleges érték nyitott; a „12 V névleges” nem jelent 12 V-os maximális feszültséget. A 30 Ah címke csak a pontos modell és névleges kapacitás megerősítése esetén felel meg 360 Wh-nak; ez sem bizonyít üzemidőt. Az akkumulátort külsőleg hordozzák, nem szerelik az állomásba, és az 5 kg-os célba nem számít bele. Nyers akkumulátorfeszültséget ne csatlakoztass a CM5IO 5 V-os USB-C tápbemenetére vagy a 40 tűs fejléc 5 V-os érintkezőjére.

Az akkumulátor különálló, moduláris **Anderson Powerpole 15/30/45 családú** piros/fekete kábelköteg-interfészt használ; a krimpérintkezőt ebből a családból kell kiválasztani az igazolt vezetékmérethez és terheléshez. Ne válassz 15 A, 30 A vagy 45 A érintkezőt pusztán a névleges címkéje alapján: a BOM/footprint befagyasztása előtt a pontos érintkező cikkszámát, vezetéktartományát, krimpelőszerszámát, házát, hőmérsékleti/derating feltételeit, feszültségét, valamint folyamatos/csúcsáram-alkalmasságát a gyártó elsődleges adatlapja és a mért rendszerterhelés alapján igazold. A piros/fekete házakat helyes polaritással/kulcsolással kell párosítani; a tényleges akkumulátorköteghez illeszkedést és polaritást mechanikailag is ellenőrizd.

Az akkumulátorkábel/pigtail a hozzá illő Powerpole-párt használja, és egy **pontos cikkszám szerint kiválasztott, áramterhelhetőségre méretezett NYÁK-sorkapocsba** végződjön. Ne tervezz Powerpole-ház-footprintet vagy azonosítatlan, szabad Powerpole-érintkezőt közvetlenül a NYÁK-ra. A paneloldali csatlakozót az igazolt gyártói cikkszám/adatlap alapján kell kiválasztani a tényleges vezetőmérethez, footprinthez, áramhoz, hőmérséklet-emelkedéshez és illeszkedéshez. A kiválasztásig sem a panelcsatlakozó footprintje, sem a Powerpole-érintkező, vezetékméret vagy áramérték nincs befagyasztva.

A szükséges tápellátási sorrend: akkumulátor pozitív pólusa → a csomaghoz közeli fő DC-biztosíték → fő leválasztó/szervizkapcsoló → védett elosztás; külön DC-minősítésű ág-biztosíték kell (1) a CM5IO 5 V-os USB-C átalakítójához, (2) a motor tápjához/átalakítójához, valamint (3) adott esetben minden PA/RF tápághoz. A biztosíték és foglalat feszültség-, áram- és megszakítóképessége feleljen meg a kiválasztott csomagnak és terhelésnek. Ne válassz találomra biztosítóáramot: mérd meg a folyamatos, indítási, megszorulási és adási csúcsokat; ellenőrizd a biztosíték idő–áram/gazdagítási viselkedését és hőmérsékleti deratingjét; és biztosítsd, hogy egyik biztosíték névleges értéke se haladja meg az általa védett vezeték, csatlakozó/érintkező, panelkapocs és biztosítéktartó biztonságos áramát. A csomag BMS-e nem helyettesíti a csomag melletti főbiztosítékot vagy az ág-biztosítékokat. A reteszelődő, DC-re minősített vészleállító a motor tápjának független megszakítási útja marad; az akkumulátor szervizleválasztója és biztosítéka nem helyettesíti.

Az autonómia célja legalább **2 óra** meghatározott, reprezentatív teljesrendszer-terhelési ciklus mellett. A csomag kapacitása 12 V névleges feszültségen szigorúan legyen **1 Ah-nál nagyobb** (>12 Wh), de a 12 Wh csak alsó korlát, és **nem igazolja a kétórás üzemidőt**. A méretezés alapja a mért akkumulátoroldali átlagteljesítmény legyen, beleértve a CM5/CM5IO-t, mindkét LimeSDR-t, hangot, vezérlőelektronikát, átalakítási veszteségeket, valamint a jóváhagyott rádióadási és motor-mozgási munkaciklust. Használd a `szükséges névleges Wh >= mért akkumulátoroldali átlagos W * 2 h / használhatóenergia-hányad` összefüggést; a használhatóenergia-hányadot a kiválasztott csomag, hőmérséklet, öregedés, lekapcsolási feszültség és tartalék alapján kell meghatározni. A védelmet, vezetékeket, csatlakozókat és szabályzókat külön méretezd a mért indítási és csúcsáramokra.

A CM5IO tápútja különálló a kiegészítőpanel akkumulátorbemenetétől: az akkumulátor feszültségét megfelelően megvalósított, egyeztetett USB-C 5 V-os táppá kell alakítani a CM5IO számára; az 5 V / 5 A csak a CM5IO tényleges bemeneti specifikációjának ellenőrzése és a teljes terhelés mérése után lehet célérték. Nyers 12 V-ot ne vezess USB-C tápérintkezőre, 40 tűs fejléc 5 V-os érintkezőjére vagy a CM5-re. A forrás/kábel terhelhetőségét, PD-egyeztetést és az esetleg szükséges 5 A-es e-markert együtt kell igazolni.

A kiegészítőpanel 12 V névleges akkumulátorbemenetéhez kémia-kompatibilis csomagvédelem/BMS, csomag melletti biztosíték, fordított polaritás elleni védelem, rövidzárlat-/túláramvédelem és a kiválasztott sínhez méretezett, védett átalakító fokozatok kellenek. Tartalmazzon tranzienselnyomást (TVS vagy az igazolt csomaghoz/átalakítóhoz választott egyenértékű megoldás) és szabályozott bekapcsolási áramot; a tranzienselnyomónak normál maximális csomagfeszültségen inaktívnak kell maradnia, a lefogási/energiaértékének pedig össze kell hangolódnia a védelemmel és az átalakító abszolút maximális értékeivel. Önmagában egy TVS nem bizonyít túlfeszültség-immunitást. A bemeneti alkatrészek konzervatív, előzetes terhelési vizsgálatára legalább **30 V** névleges alkatrészeket célozz; ez tervezési tartalék, nem bizonyíték arra, hogy az akkumulátor 30 V-on működhet vagy működnie kell. A tényleges csomagfeszültség-tartományhoz, tranziensekhez, védelmi koordinációhoz és kiválasztott alkatrészekhez a kiadás előtt újra ellenőrizd. Az 5 V-os logikai sínt a bemeneti akkumulátortól **galvanikusan leválasztott szabályzóval** kell táplálni; ellenőrizd a bemeneti tartományt, kimeneti/terhelési névleges értéket, leválasztást, EMI-t, hőviselkedést és hibakezelést. A motor tápátalakítása különálló, és nem feltételezhetően leválasztott; tápját a DC-re minősített reteszelődő vészleállító útjának külön meg kell szakítania. A tényleges akkumulátor-felső/alsó feszültség, motorfeszültség/-áram, biztosítékértékek, csatlakozó és szabályzóalkatrészek még nincsenek befagyasztva; a jelölt értékek nem engedélyeznek NYÁK-tervezést vagy kiadást. A LimeSDR-ek terhelőáramát ne vezesd át a 40 tűs 5 V-os sínen. A motor-táp, logika, CM5IO USB-C táp és USB-adat útja maradjon elkülönítve; kiadás előtt ellenőrizd a visszavezetéseket, bekapcsolási áramot, zajt és hibaviselkedést. Ez a tápellátási pontosítás nem helyettesíti a meglévő SMA RF-útvonalakat vagy a külön külső K1 hangcsatlakozási célt; sem az RF, sem a hang nem halad át az USB-C tápon.

### Akkumulátor-bemeneti EMI- és tápminőségi tervezési kapu

Az akkumulátor-bemenet terve nem általános, ideális LC-szűrő; nincs
kiválasztva alkatrészérték vagy nagyáramú fojtó. A vizsgálandó, elrendezés
előtti topológia:

1. Powerpole akkumulátorköteg és igazolt névleges értékű NYÁK-sorkapocs;
   az akkumulátorcsomag melletti biztosíték és fő szervizleválasztó.
2. Az igazolt akkumulátoráramhoz és hibaenergiához méretezett
   polaritásfordítás elleni védelem; a normál, ellenőrzött akkumulátortartományban
   inaktív, összehangolt TVS/tranzienskorlátozó; szabályozott bekapcsolási áram.
3. Opcionális közös módusú fojtó esetén **mind a pozitív, mind a visszatérő
   DC-vezetéket a tervezett, csatolt tekercseken kell átvezetni**; a
   legnagyobb folyamatos és tranziens áramra, tekercs-egyenáramú ellenállásra,
   telítődésre, hőmérséklet-emelkedésre, szigetelésre és hiba-viselkedésre
   kiválasztva/deratingelve. Soha ne tegyél kisjelű ferritet vagy 300 mA-es
   gyöngyöt sorba az 5 A-es CM5IO táppal. A beiktatási impedanciát a vizsgált
   vezetett zajfrekvenciákon kell ellenőrizni; önmagában nem RF-kibocsátási
   vagy vevő-deszenzitizációs megoldás.
4. Az opcionális csatlakozó-/fejlécszűrő modul még TBD: nincs beültetve és
   nincs kitalált footprintje. Bármely modul/fejléc pontos interfészt,
   érintkező-/rézterhelhetőséget, polaritást, elhelyezést, jóváhagyott
   alkatrészt, beültetési állapotot, valamint dokumentált impedancia-/áramadatot
   igényel. Ha a mérés külső szűrőt követel, külön minősített, dokumentált
   modulinterfészt kell hozzáadni, majd az új panelrevízió exportja előtt
   ismét elvégezni a kapcsolási rajz/footprint egyezőség-, ERC-, DRC-,
   összeköttetési, hő- és gyártási ellenőrzést.
5. Differenciális bemeneti szűrő csak akkor alkalmazható, ha azt a
   szabályozó gyártói útmutatója és a mért impedancia indokolja; a tényleges
   átalakító-bemeneti impedanciával, kábel/forrás impedanciával,
   kapacitással és ESR-rel, minden üzemállapotban szándékosan csillapítva
   kell ellenőrizni. Ne kapcsolj sorba vakon nagy Q-jú LC-fokozatokat:
   a kapcsolóüzemű átalakító negatív inkrementális bemeneti impedanciája
   instabillá tehet egy csillapítatlan bemeneti szűrőt. Valós
   forrásimpedanciával és mindkét CM5IO-/motorággal működés közben igazold
   az indulás, terheléslépcső, bemeneti feszültséglépcső, alulfeszültség,
   áramkorlátozás és helyreállás stabilitását.
6. Külön biztosított ágak a CM5IO 5 V-os USB-C átalakítóhoz, a motortáphoz
   és minden PA/RF táphoz, ha alkalmazható; helyi leválasztókondenzátor
   minden átalakítónál/terhelésnél. A nagy `di/dt` motor-/PA-hurkokat
   fizikailag tartsd távol a CM5 5 V-os logikától, GNSS-től, iránytűtől,
   enkóderektől és hangtól. Határozz meg tudatos visszatérő-/árnyékolás-/
   alvázkoncepciót; ne használj felülvizsgálat nélküli árnyékbekötést vagy
   motor-visszavezetést az érzékelő-/hangföldön keresztül.

Ne válassz közös módusú fojtót, differenciális induktort/kondenzátort,
gyöngyöt, ferritet, TVS-t vagy biztosítóáramot addig, amíg nincs meg a
pontos alkatrész-adatlap, mért ágterhelés, indítási/megszorulási/adási
áram, vezetékezés és szabályozó-stabilitási útmutató. Minden ferrit feleljen
meg az adott ág valós áramán a DC-előfeszítési/telítődési és DCR-esési
követelményeknek. Számszerűsítsd a szabályozó bemeneti/kimeneti
hullámosságát, tranziensválaszát, hőmérséklet-emelkedését, vezetett zaját,
a CM5IO 5 V-os feszültségesését/alulfeszültség-viselkedését és helyreállását;
vizsgáld a Linux stabilitását két LimeSDR egyidejű adatfolyama, motorindítás/
mozgás és rádióadás együttes terhelése alatt.

A vezetett tápoldali szűrést ne azonosítsd az antenna-port szűrésével vagy
az RF-deszenzitizáció kezelésével. Tartsd meg az SMA RF-útvonalakat; az
integráció után, 145/435 MHz-es esetekben mérd meg a vevőérzékenységet/
deszenzitizációt és az SMA-portoknál az adási melléktermékeket/
harmonikusokat. Különösen a 145 MHz harmadik harmonikusa esik 435 MHz
közelébe, ezért valódi kibocsátásmérés kell; sem egy DC-bemeneti fojtó,
sem a méretlen beiktatási veszteség nem bizonyít megfelelést vagy RF-
együttélést.

## Befagyasztott 40 tűs GPIO-szerződés (A revízió)

Az alábbi BCM GPIO-számok Linux GPIO-számok, nem a fizikai fejléc tűszámai. Az irány a CM5IO/CM5 felől értendő. Ez a térkép a rot vezérlőhöz és rádióhardver-adapterhez befagyasztott interfész. Bármely BCM- vagy fejléc-tű megváltoztatásához verziózott interfészrevízió és összehangolt szoftverfrissítés szükséges. Az alább felsorolt felhúzások és hardveres kapuk tervezési követelmények, nem bizonyítékai annak, hogy a hardver elkészült vagy igazolt.

| BCM GPIO | Fejléc tű | Hálózat / cél | Irány / polaritás / reset-szerződés |
|---:|---:|---|---|
| 2 | 3 | I2C1 SDA, multiplexer/biztonsági bővítő busz | Kétirányú, 3,3 V |
| 3 | 5 | I2C1 SCL, multiplexer/biztonsági bővítő busz | Nyitott kollektor/leengedve HIGH, 3,3 V |
| 4 | 7 | AZ minimum NC-végállás | Bemenet; LOW = zárt/egészséges, HIGH = nyitott/hiba |
| 5 | 29 | AZ maximum NC-végállás | Bemenet; LOW = zárt/egészséges, HIGH = nyitott/hiba |
| 6 | 31 | EL minimum NC-végállás | Bemenet; LOW = zárt/egészséges, HIGH = nyitott/hiba |
| 7 | 26 | EL maximum NC-végállás | Bemenet; LOW = zárt/egészséges, HIGH = nyitott/hiba |
| 8 | 24 | POL minimum NC-végállás | Bemenet; LOW = zárt/egészséges, HIGH = nyitott/hiba |
| 9 | 21 | POL maximum NC-végállás | Bemenet; LOW = zárt/egészséges, HIGH = nyitott/hiba |
| 10 | 19 | Vészleállító segéd NC-monitor | Bemenet; LOW = zárt/egészséges, HIGH = nyitott/hiba |
| 11 | 23 | Külső watchdog-életjelet adó kimenet | A CM5 biztosítja az életjel-éleket |
| 12 | 32 | Motorfelfegyverzési kérés | Kimenet; HIGH = kérés, külső lehúzás miatt resetkor KI |
| 13 | 33 | TCA9548A RESET_N | Kimenet; LOW = reset, külső felhúzás miatt resetkor inaktív |
| 14 | 8 | GNSS UART TX | Kimenet; nyugalmi HIGH, CM5 TX → vevő RX |
| 15 | 10 | GNSS UART RX | Bemenet; vevő TX → CM5 RX, 3,3 V |
| 16 | 36 | SPI1 CS2, POL-meghajtó | Kimenet; aktív LOW, külső felhúzás |
| 17 | 11 | SPI1 CS1, EL-meghajtó | Kimenet; aktív LOW, külső felhúzás |
| 18 | 12 | SPI1 CS0, AZ-meghajtó | Kimenet; aktív LOW, külső felhúzás |
| 19 | 35 | SPI1 MISO | Bemenet; 3,3 V |
| 20 | 38 | SPI1 MOSI | Kimenet; nyugalmi LOW, 3,3 V |
| 21 | 40 | SPI1 SCLK | Kimenet; nyugalmi LOW, 3,3 V |
| 22 | 15 | VHF PA PTT-kérés | Kimenet; HIGH = kérés, külső lehúzás miatt resetkor KI |
| 23 | 16 | UHF PA PTT-kérés | Kimenet; HIGH = kérés, külső lehúzás miatt resetkor KI |
| 24 | 18 | AZ-meghajtó diagnosztika | Bemenet; LOW = hiba, puffer/szint 3,3 V-ra korlátozva |
| 25 | 22 | EL-meghajtó diagnosztika | Bemenet; LOW = hiba, puffer/szint 3,3 V-ra korlátozva |
| 26 | 37 | POL-meghajtó diagnosztika | Bemenet; LOW = hiba, puffer/szint 3,3 V-ra korlátozva |
| 27 | 13 | GNSS PPS | Bemenet; opcionális időzítő impulzus, nem fixérvényességi jel |

A 26 kivezetett BCM GPIO-t ez a táblázat teljesen kiosztja. Különösen a GPIO0/1 (fizikai ID_SD/ID_SC) fenntartott, és nincs használatban.

A befagyasztott SPI1-vezetékezés: MOSI GPIO20, MISO GPIO19, SCLK GPIO21, CS2/CS1/CS0 pedig rendre GPIO16/17/18. A Linux SPI-eszköz elnevezését és overlay-kiválasztását a CM5IO elindított rendszerképén kell megerősíteni; a BCM-vonal kiosztása önmagában nem konfigurál Linux overlayt. Az I2C1 a TCA9548A-t szolgálja ki az alapértelmezett 0x70 címen; a 0., 1. és 2. csatorna a három AS5600 enkóderé, a 3. az iránytűé, a 4. az IMU-é. Az 5–7. csatorna nincs bekötve, hacsak későbbi revízió ki nem osztja. A GNSS az UART0 GPIO14/15-öt használja; a PPS opcionális, és a GPIO27-re kerül. A GPIO0/1 (fizikai ID_SD/ID_SC) fenntartott.

A közös motorfelfegyverzési GPIO kérés, nem biztonsági minősítésű engedélyezés. A befagyasztott szoftveres kiosztás az I2C 0x20 címen MCP23017-et használ: a GPA0/1/2 az AZ/EL/POL tengelyenkénti engedélykérése (HIGH = kérés; külső lehúzás = resetkor KI); GPA3 a motorengedélyezés visszajelzése, GPA4/5 a VHF/UHF PTT-visszajelzése, GPA6/7 pedig a VHF/UHF PA-hibabemenet. Ezek a bővítővonalak szoftveres megfigyelési/kérési jelek, nem biztonsági funkciók; pontos áramköreik és csatlakozóinterfészeik még blokkoló tételek. A bővítő resetje, tápvesztése vagy nem konfigurált tűi soha nem aktiválhatják a meghajtóengedélyezést. Minden aktív alacsony EN-t külön hardverrel is reteszelni kell úgy, hogy az egészséges külső watchdog és a zárt vészleállító lánc egyaránt szükséges legyen. A bővítő kimenete nem biztonsági funkció.

Az operációsrendszer-integráció szerződése a fenti kiosztású SPI1, I2C1 és UART0. Ne engedélyezd az SPI0-t az SPI1 helyett, és ne hagyd, hogy elavult device-tree overlayek átrendezzék ezeket a BCM-tűket. Az adapterintegráció előtt a célrendszeren ellenőrizd a CM5IO rendszerképének tényleges overlayneveit, valamint a létrejövő `/dev/spidev*`, I2C-, UART- és GPIO-vonalazonosítókat. Minden hidegindításkor, újraindításkor, szolgáltatás-újraindításkor, GPIO-szolgáltató helyreállásakor és bővítő-resetkor a motorfelfegyverzést, a tengelyenkénti engedélyeket és mindkét PTT-kérést inaktívra kell inicializálni. Egyetlen operációsrendszer-szolgáltatás, overlay vagy alkalmazás sem felfegyverezheti automatikusan a motort, illetve nem kérhet adást induláskor. A szoftveres alapértékek nem helyettesítik a külső hardveres, hiba esetén kikapcsolt reteszeket.

A fizikai, reteszelődő vészleállítónak a kiválasztott táphoz és motorokhoz méretezett, DC-re minősített külső kontaktoron/érintkezőn keresztül, függetlenül meg kell szakítania a motor tápját. Szoftveres monitor vagy NYÁK GPIO nem helyettesíti ezt a tápmegszakítási útvonalat. A watchdog, vészleállító-lánc vagy logikai táp elvesztésének mindhárom motor-meghajtót és mindkét PTT-kimenetet tiltania kell. A PTT-kérés tűjein külön külső lehúzás van, és külön izolált, hiba esetén kikapcsolt kimeneteken kell átvezetni őket; azok külső névleges értékei, csatlakozótű-kiosztása és elérhető visszajelzése még nincs kiválasztva.

A hat NC-végállás külön áramkör, minden mozgásvéghez egy; minden nyitott kapcsoló vagy szakadt vezeték hibának számít. Ezek csak GPIO-monitor-bemenetként vannak befagyasztva. A kiválasztott meghajtó rámpabemenetéhez vezető közvetlen hardveres keményvégállás-út még nincs igazolva vagy kiosztva. **Ne mozgasd a motorokat**, amíg a kapcsolási rajz nem tartalmaz és nem validál közvetlen hardveres végállás/meghajtóleállítási útvonalat. 5 V-os vagy 12 V-os kapcsolóáramkört ne csatlakoztass CM5 GPIO-ra.

## Hardveres blokkoló tételek (nem tekinthetők panelkiadásnak)

- Építs be és külön igazolj alapállapotban kikapcsolt hardveres utat mind a hat kemény végálláshoz; a BCM-végállásfigyelés önmagában nem elég.
- Válassz ki és igazolj külső watchdog-áramkört, időtúllépést és indítási polaritást. A BCM11 életjel-**kimenet**; a watchdog lejáratának Linux-függetlenül fizikailag inaktiválnia kell mind a meghajtóengedélyezéseket, mindkét PTT-kimenetet.
- Fagyaszd be a DC-re minősített reteszelő vészleállítót/kontaktort, a tápáram-védelmet és a motor-táp megszakítási útját. A GPIO10 kizárólag egy izolált segéd NC-érintkezőt figyel.
- Fagyaszd be a tengelyenkénti EN-reteszelést, beleértve a CM5 GPIO12 felfegyverzési kérelmet, az MCP23017 GPA0..2 kimeneteit, a bővítő resetviselkedését és a külső, alaphelyzetben kikapcsolt felhúzásokat/lehúzásokat.
- Fagyaszd be a két PTT-izoláló/csatlakozóáramkört és a PA-visszajelzés elektromos határait. A GPIO22/23 logikai szintű kérések, nem PA-meghajtó kimenetek.
- Fagyaszd be és igazold a tényleges UV-5R/UV-82 rádió és K1 tartozék tűkiosztását, a külön hangaljzat-leánykártya fejlécét, földreferenciáját, valamint a hang/BTL elválasztását, mielőtt az interfészt beültetnéd vagy csatlakoztatnád.
- Fejezd be a beépített hangszóró-/mikrofonútvonalat: a nyilvános USB-kodek-jelölt TI PCM2902C, de gazdacsatlakozása, mikrofon-előerősítője, hangszóró-erősítője, analóg jelszintjei és RF-együttélése még nincs megtervezve vagy minősítve. A kodekjelöltet ne tekintsd kész hangáramkörnek.
- Minősítsd a CM5IO USB-gazdatopológiáját és a táplált hub/tápkeretet két LimeSDR Mini és hang együttes használatára. Hanghoz nincs befagyasztva USB-gazdaport vagy hub.
- Ellenőrizd a CM5IO külön USB-C tápbemeneti, illetve USB-adat/gazda csatlakozóinak szerepét, az adott panelrevízió által támogatott PD-bemeneti szerződést/áramot, a forrás-egyeztetést és a teljes egyidejű terhelés tartalékát. Az 5 V / 5 A cél nem panelnévleges érték, és nem bizonyítja a rendelkezésre álló teljesítményt. Mérd meg a teljes rendszert a két LimeSDR-rel, CM5/CM5IO-val, hanggal, veszteségekkel, indítási és adási csúcsokkal együtt.
- Ellenőrizd, hogy a forrás és az 5 A-es e-markerrel ellátott kábel ténylegesen egyezteti-e a szükséges Type-C/PD áramot; ne használj passzív vagy ellenőrizetlen USB-C breakoutot, csak ellenállásokra épülő helyettesítőt vagy feltételezett 5 A-es kábelt.
- Válaszd ki a külső, 12 V névleges akkumulátor kémiáját, tényleges felső/alsó feszültségtartományát, 1 Ah-nál nagyobb kapacitását, folyamatos/csúcsáramát, csomagvédelmét/BMS-ét, csomag melletti biztosítékát, Powerpole-érintkező/ház/vezeték összeállítását, paneloldali sorkapcsát és mért kétórás rendszerterhelési ciklusát. A jelenlegi akkumulátorhivatkozás ECO-WORTHY 12 V 30 Ah LiFePO4-jelölt; a pontos típust, kapacitást, BMS-t és áramhatárokat a leszállított akkumulátor dokumentációjából kell ellenőrizni. A terméklista önmagában nem igazolja a 14,6 V-os töltőfeszültséget, a minimális feszültséget, a kisütőáramot vagy az üzemidőt. A 14,6 V csak megerősítés után használható előzetes alkatrész-terhelési szűrésre; a 30 Ah címke csak ellenőrzés után jelentene névleges 360 Wh-t. Az akkumulátortömeg nem része az 5 kg-os célnak; az állvány, rádió és minden más állomásberendezés beleszámít. A >12 Wh kapacitás-alsó korlát önmagában nem teljesíti a kétórás célt.
  - Méretezd és minősítsd az akkumulátor–CM5IO 5 V USB-C átalakítót az igazolt CM5IO-bemenethez és egyeztetett tápellátási szerződéshez; nyers akkumulátorfeszültség soha nem juthat a CM5IO 5 V-os bemenetére vagy 40 tűs fejlécére. Ettől külön fagyaszd be és méretezd az **izolált 5 V-os logikai** átalakítót, valamint a külön motor-átalakítósíneket, védelmet, visszavezetéseket, bekapcsolási áramkezelést és hibaviselkedést. Fagyaszd be a csomag melletti főbiztosítékot/leválasztót, illetve a CM5IO-, motor- és PA/RF-ágak DC-biztosítékait. A biztosítékértéket csak a mért terhelés, kábel, csatlakozó, foglalat, bekapcsolási áram és idő–áram koordináció alapján határozd meg; a BMS-védelem nem helyettesíti a biztosítékokat. Az akkumulátor-front-end előzetes, konzervatív terhelési szűréséhez használj legalább 30 V-os alkatrészértéket, majd a pontos csomagtartomány és tranziensek alapján ellenőrizd újra a véglegesítés előtt.
- Ne vezesd át a kiegészítőpanel vagy a LimeSDR-ek terhelőáramát a CM5IO 40 tűs 5 V-os fejlécén. A szabályzók, áramkorlátok, biztosítékok, vezetékek vagy rézszélességek kiválasztása előtt ellenőrizd a teljes tápkeretet és az indítási/adási csúcsokat.
- Ellenőrizd a Watterott modul fizikai foglalatának kulcsolását és a pontos v1.5 kapcsolási rajz/tűsorrendet; a BCM24..26 előtt ellenőrizd a diagnosztikai jel feszültségét és pufferelését.
- Ellenőrizd az összes megnevezett érzékelő/GNSS breakout revízióját, kábelét és tűkiosztását, moduláram-keretét, SPI/I2C/UART overlayeit, valamint a CM5IO rev 2 gazdagép-/hangtopológiáját.
- Szerezd be a pontos JLCPCB/LCSC cikkszámokat és beültetési csomagokat. Addig ne készíts üres PCBA BOM/CPL helyőrzőket, és ne állítsd, hogy a panel beültetésre kész.
- Az alkatrészárakat csak a pontos, beszerezhető gyártói és LCSC cikkszámok igazolása után becsüld meg; a jelenlegi terv nem támaszt alá árbecslést.
- Terepi üzem előtt próbapadon minősítsd a motoráram/hőmérséklet-tartalékokat, rámpa-/végállás-viselkedést, watchdogot, vészleállítót, PTT alapállapotban nyitott működését, RF/hang együttélést, végleges burkolatot és a teljes állomás 5 kg-os tömegét.

## Cserélhető külső modulok

A befagyasztott szoftveres érzékelőszerződés az alábbi gyártóspecifikus külső breakoutokat használja; pontos panelrevíziójukat, fizikai csatlakozóikat és kábeleiket még meg kell erősíteni. Ezek nem a NYÁK-ra helyezett footprintök. A kiegészítőpanel érzékelőcsatlakozói kulcsolt, 4 tűs I2C-interfészre vannak kiosztva (GND, 3V3, SDA, SCL); ne nevezd JST-SH-nak vagy STEMMA QT-nek, amíg a pontos footprintet, tűsorrendet és kábelköteget nem validálták:

| Funkció | Kiválasztott modul | Interfész |
|---|---|---|
| AZ/EL/POL enkóder, 3 db | Adafruit AS5600 Magnetic Angle Sensor, PID 6357 | I2C, 0x36; külön TCA9548A 0/1/2 csatornák |
| Iránytű | Adafruit LIS3MDL 3 tengelyes magnetométer, PID 4479 | I2C; TCA9548A 3. csatorna |
| IMU | Adafruit LSM6DSOX 6 szabadságfokú breakout, PID 4438 | I2C; TCA9548A 4. csatorna |
| GNSS | Adafruit Ultimate GPS Breakout, PID 746 | UART0, 3,3 V logika; opcionális PPS |

Az érzékelők tápja és logikája 3,3 V legyen. Csatlakoztatás előtt ellenőrizd a választott breakout revízióját, beépített felhúzásait, a tényleges csatlakozó 1. tűjének irányát, a mágneses enkóder rögzítését/légrését és az érzékelőkábelek elvezetését. Az iránytűt motoroktól, acéltól, enkóder-mágnesektől, tápvezetékektől és RF-hardvertől távol kalibráld és validáld; a NYÁK nem határozza meg a valódi irányt. A külső breakoutok és kábelek nincsenek benne a PCBA BOM/CPL-ben.

## SilentStepStick TMC5160 v1.5

Csak a Watterott SilentStepStick TMC5160 v1.5 tartozik a hatókörbe; pusztán az alkatrésznév alapján ne helyettesítsd másik TMC5160 hordozópanellel. A panelinterfész SPI1-et használ, tengelyenként egyedi, felhúzott chip-selecttel. Tartsd be a modul v1.5 konfigurációját: az SD_MODE jumpert hagyd nyitva, így a dokumentált külső lehúzás választja a rámpavezérlőt; az SPI_MODE legyen VIO-ra állítva; a belső órajelhez a CLK csatlakozzon GND-re; a letiltott állapothoz az EN legyen VIO-n; minden CS-hez szerelj külső felhúzást. Foglalatba helyezés előtt ellenőrizd a tényleges modulrevíziót és jumperállapotot.

A Watterott v1.5 rajza az alkatrész felőli tűsorrendet határozza meg. A modult felfelé néző MOSFET-ekkel tartva a bal oszlop fentről lefelé: EN, SDI/CFG1, SCK/CFG2, CS/CFG3, SDO/CFG0, DCO, STEP, DIR; a jobb oszlop fentről lefelé: VM, GND, M2B, M2A, M1A, M1B, VIO, GND. A foglalat tűszámainak kiosztása előtt ellenőrizd a letöltött, rögzített v1.5 kapcsolási rajzot és a fizikai modul kulcsolását. Ne használj TMC2209 footprintet. A meghajtó órajeltűrése, programozott árama, hűtése, VMOT-tartománya, végállás-polaritása, leállító rámpája és fizikai végállás-válasza adatlap-ellenőrzést és próbapadi tesztet igényel.

## CM5IO USB és RF/hang szétválasztás

Ne foglald le hanghoz a CM5IO egyik natív USB 3 portját sem, ha mindkettőt LimeSDR Mini használja. A kiválasztott hangeszköz külön ellenőrzött CM5IO gazdainterfészt vagy olyan táplált hubot használjon, amelynek gazda szerepe, sávszélessége, tápja és egyidejű rádiós működése igazolt. A pontos CM5IO-revízió és konfiguráció ellenőrzése nélkül ne feltételezd, hogy az USB-C csatlakozó gazdaport.

A kiegészítőpanel nem tartalmaz SMA-csatlakozót, RF-nyomvonalat, hangaljzatot vagy LimeSDR USB-adatkapcsolatot. A két LimeSDR-láncot, azok PA-/szűrőútjait és a hang I/O-t tartsd egymástól függetlenül. A PA PTT-interfészei elektromosan különállnak a hangtól, és letiltva maradnak a kiválasztott PA tűkiosztásának, PTT-feszültségének/-áramának és hiba esetén kikapcsolt viselkedésének teszteléséig. Ez a panel nem bizonyítja az 5 W FM, az 5 W PEP USB, az 1 W AM, a teljes duplex RF vagy a hangteljesítmény elérését.

## Gyártási és ellenőrzési kapuk

1. Fagyaszd be a pontos CM5IO-revíziót, a 40 tűs VIO jumpert 3,3 V-on, a pontos CM5 SKU-t, a Watterott meghajtó revízióját, valamint a külső kábelek/modulok csatlakozóirientációját.
2. Ellenőrizd a kapcsolási rajz és NYÁK paritását, a 40 tűs kiosztást, minden TMC5160 v1.5 foglalattűt az elsődleges rajz alapján, a végállás-polaritást, watchdog igazságtáblát, vészleállító megszakítási utat és izolált PTT-kimeneteket.
3. Futtasd le a KiCad 10 ERC- és DRC-ellenőrzéseket minden súlyossági szinten, továbbá a kapcsolási rajz paritás- és összeköttetetlen-elem ellenőrzését. Minden hibát oldj fel; ne kapcsold ki az ellenőrzéseket azért, hogy zöld legyen a jelentés.
4. Azonos panelorigóval exportáld a Gerber réz/maszk/feliratkép/kerület rétegeit és a PTH/NPTH Excellon-fájlokat. A CAM-adatokat, panelkontúrt, fúrófájlokat, csatlakozóirányt, netlistát és beültetési kizárási területeket függetlenül vizsgáld át.
5. JLCPCB BOM-ot és CPL-t ugyanabból a validált NYÁK-ból készíts. A CPL `Designator` értékei pontosan a kapcsolási rajzban/NYÁK-ban kiosztott, egyedi referenciajelölések legyenek; a rádió „K1” tartozékinterfész-neve nem NYÁK-referenciajelölés. A JLCPCB pozícióoszlopai: `Designator,Mid X,Mid Y,Layer,Rotation`; a koordináták az alkatrész panelen elfoglalt középpontját adják meg milliméterben. Feltöltés előtt minden referenciajelölést, oldalt és tájolást ellenőrizz az összeszerelt panel nézetén. A DNP-alkatrészeket hagyd ki a beültetési pozíciókból, és a BOM-ban kifejezetten jelöld őket. Csak a pontos gyártói alkatrészhez és tokozáshoz ellenőrzött LCSC-számot használd. A kézzel beültetendő furatszerelt foglalatokat, fejléceket, modulokat és DNP-elemeket kifejezetten jelöld; ne készíts nekik hamis beültetési pozíciót. Még nincs kiadott CPL-sor vagy referenciajelölés, mert nincs validált CM5 kiegészítő NYÁK.
6. Bármilyen mozgás vagy adás engedélyezése előtt próbapadon teszteld az áramkorlátokat, bekapcsolási/resetállapotokat, valamennyi NC kábel-szakadás hibát, watchdog-időtúllépést, vészleállító tápmegszakítást, mindhárom meghajtó letiltási útját, tengelyenkénti végállás-választ, SPI-visszaolvasást, TCA9548A helyreállást, enkódermágnes-állapotot, GNSS-fixet/PPS-t, izolált PTT alapállapotban nyitott működését, valamint RF-/hanginterferenciát.

## Elsődleges hivatkozások

- [Raspberry Pi CM5 és CM5IO dokumentáció](https://www.raspberrypi.com/documentation/computers/compute-module.html)
- [Raspberry Pi CM5 adatlap](https://pip.raspberrypi.com/documents/RP-008180-DS)
- [Watterott TMC5160 SilentStepStick tűkonfiguráció](https://learn.watterott.com/silentstepstick/pinconfig/tmc5160/)
- [Watterott SilentStepStick TMC5160 v1.5 kapcsolási rajz (rögzített revízió)](https://github.com/watterott/SilentStepStick/blob/098b7518b0de31e6a12fda78c68ae2666b81fbb6/hardware/SilentStepStick-TMC5160_v15.pdf)
- [TI TCA9548A termékoldal](https://www.ti.com/product/TCA9548A)
- [TI PCM2902C USB-audiokodek](https://www.ti.com/product/PCM2902C)
- [Adafruit AS5600, PID 6357](https://www.adafruit.com/product/6357)
- [Adafruit LIS3MDL, PID 4479](https://www.adafruit.com/product/4479)
- [Adafruit LSM6DSOX, PID 4438](https://www.adafruit.com/product/4438)
- [Adafruit Ultimate GPS, PID 746](https://www.adafruit.com/product/746)
