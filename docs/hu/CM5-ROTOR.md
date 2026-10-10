# CM5 Linux-rotor és követő host

## Hatókör és validálási határ

Ez az új, önálló Linux-rotor alrendszer a Raspberry Pi Compute Module 5
(CM5) számára. A CM5 az állomás egyetlen számítógépe; a kiválasztott
LimeSDR Mini külön rádióeszköz, amelyet a rádiószolgáltatás kezel. Az
örökölt ESP32 firmware és BLE-protokoll változatlan marad. A rotor
szolgáltatása különálló modul, amelyet a hitelesített Linux Bluetooth-/
rádió-host hívhat; nem birtokolja a rádiót, Android-alkalmazást, firmware-t
vagy hordozópanel-tervet.

A szoftver nem biztonsági tanúsítás. CM5/Linux-folyamat, szoftveres
hiba-jelzőbit vagy sikeres SPI-írás nem helyettesíti a normálisan
kikapcsolt hardveres motor-tápmegszakítást, a hat független NC-tengely-
határolót, a külső vészleállítót vagy a független hardver-watchdogot.
Ezeket az áramköröket és kábelezést a kiválasztott hordozópanel
befagyasztása előtt kell rögzíteni és ellenőrizni, még bármilyen
motormozgás vagy RF-adás engedélyezése előtt.

Minden szükséges visszajelzés hiánya, érvénytelensége, elavultsága,
kalibrálatlansága vagy ellentmondása esetén a megvalósítás zárt biztonsági
állapotba lép. Produkciós szimulált-meghajtó tartalékút nincs. Szimuláció
csak kifejezetten megnevezett unit-test fixture-ökben használható.

## Telepítés és indítás

A rotor Python-csomagja független a rádiócsomagtól; nem importál SDR-, PA-,
Bluetooth- vagy hangkomponenst. Önálló csomagként telepítsd a `rotor/`
könyvtárból `python -m pip install .` paranccsal, elkülönített Python-
környezetben. Indítási példák:

```text
portable-sat-rotor --config /etc/bricohams/rotor.json
python -m rotor
```

A helyi JSON Lines interfész bemeneti soronként egy
`{"operation":"...","data":{}}` kérést fogad, és a vezérlő kifejezett
`{ok, data, error}` válaszát adja. A `--local-console` helyi folyamat-
jogosultsági választás, nem kérésmező; távoli BLE/API-adapter soha nem
engedélyezheti.

A CLI-nek és a rádió-hostnak egyaránt szüksége van CM5 platform-BSP-re, amely
a `portable_sat_rotor.hardware` entry-point csoportban `cm5` nevű Python
belépési pontot regisztrál. A szolgáltató megkapja a kifejezett
vezérlőkonfigurációs útvonalat, és valódi érzékelőkből, meghajtókból és
alaphelyzetben kikapcsolt tápengedélyező kapuból összeállított
`RotorController` példányt ad vissza. Az adapter elindítja a vezérlő 50 ms-os
szervizciklusát. Nincs beépített szimulált vagy találgatott hardver-
összeállítás. A revízió-A szoftveres tűkiosztás a
[hardware/cm5/interface.json](../../hardware/cm5/interface.json) fájlban
rögzített, de az AUX NC/E-stop/watchdog/
tápengedélyező biztonsági áramkörei még nincsenek megtervezve/kiadva, és az
iránytű/IMU BSP sincs kiválasztva. Ezek ellenőrzéséig és produkciós BSP
telepítéséig az indítás kifejezett hibával leáll. A csomag rádiószoftver
nélkül is telepíthető, de a fizikai működés még nincs üzembe helyezve.

## Nyilvános vezérlő-hook

A szállítási adapter felel a hitelesítésért, kérésazonosítókért és a külső
rádió-host válaszburkáért. Csak validált műveletet és JSON-objektumot ad
át a rotorvezérlőnek:

```python
RotorController.handle_control(
    operation: str,
    data: Mapping[str, object],
    *,
    local_console: bool = False,
) -> Mapping[str, object]
```

A `local_console` értékét a megbízható hostadapter állítja, soha nem egy
távoli JSON-mezőből másolja. A hook JSON-szerializálható műveleti adatot ad
vissza, a rádióadapter pedig ezt a szokásos kérésazonosító/útvonal-burokba
helyezi:

```json
{"ok": true, "data": null, "error": null}
```

Érvénytelen vagy jogosulatlan kérés kifejezett hibát ad, nem térhet vissza
sikeresnek látszó alapértékkel. A vezérlő BLE-ről nem élesíthet,
homingolhat vagy kalibrálhat. A rádió-host a
`status.data.verifiedHealthy` és `status.data.fault` értékeket kérdezze le;
ne fogadjon el kliens által beküldött rotor-egészségi állapotot.

Támogatott műveletek:

| Művelet | Kérés adatai | Biztonsági és válaszszerződés |
| --- | --- | --- |
| `status` | `{}` | Aktuális gépállapot, hiba, üzembe helyezési/ellenőrzési állapot, tengelypozíciók/célok/határok/encoder-adatkor és érzékelő-érvényesség/-adatkor. Hiányzó vagy érvénytelen adat `null`, hamis érvényességjelzővel; soha nem töltjük nullával. |
| `sensorsstatus` | `{}` | Validált nyers GNSS-, encoder-, iránytű- és IMU-visszajelzés időbélyeggel/adatkorral és kalibrálási eredettel. |
| `home` | `{"confirm":"HOME CM5 ROTOR"}` | Csak helyi konzolról. Korlátozott, tengelyenkénti háttérfeladat indul a konfigurált NC-kapcsoló felé; tengelyenként legfeljebb 120 másodperc. Kapcsolásnál, timeoutnál, visszajelzés-vesztésnél vagy bármely hibánál megáll. Nem ment egyélű alapot, és nem állítja, hogy valódi AZ-t állított be. |
| `calibrate` | Felmért `encoderZeroDeg`, `azBaseTrueDeg`, alapszintű roll/pitch, deklináció/forrás/dátum, iránytű hard-/soft-iron és orientációs mátrixok, POL-modell/forrás/offset, `carrierVerified:true`, valamint pontosan `CALIBRATE AND ARM CM5 ROTOR` megerősítés | Csak helyi konzolról, álló, fizikailag rögzített állapotban. Befagyasztott `mechanics_verified` konfiguráció, friss érzékelő-/encoder-visszajelzés és ellenőrzött élő iránytű/IMU BSP kell. A `headingMode:"manual"` elutasítandó; kézi iránykalibráció nem támogatott az adott BSP ellenőrzéséig. A `carrierVerified` csak helyi attesztáció, nem helyettesíti a kiadott biztonsági áramkört és validált fizikai visszajelzést. A kalibráció csak RAM-ban él, újraindítás után meg kell ismételni. |
| `goto` | Abszolút `{"azDeg":szám,"elDeg":szám,"polDeg":szám}` | Elutasítja a nem véges/tartományon kívüli értéket, elavult visszajelzést, homing nélküli tengelyt, aktív irányfüggő határolót vagy üzembe nem helyezett hordozót. Mindhárom tengelyhatár és kimeneti microstep-arány a befagyasztott mechanikai konfigurációból származzon. |
| `track` | `{"noradId":egész}` | Aktuális, validált TLE, friss GNSS UTC/hely, valódi irányra kalibrálás és minden mozgási reteszelés szükséges. Valós SGP4 alatti pontot/azimutot/elevációt/távolságot/távolságsebességet, parancsolt tengelyszögeket és időbélyegeket közöl. A helyben üzembe helyezett `apparent-track` vagy `cross-track` POL-geometria/eltolás kifejezett mechanikai konvenció; nem bizonyítja a műhold adóantennájának polarizációját. A műhold tényleges polarizációját külön kell ellenőrizni. |
| `stop` | `{}` | Azonnali szoftveres stop-kérés és meghajtó rámpás leállítás; megszakítja az aktív homingot és érvényteleníti a home-referenciákat. A hardveres E-stop/watchdog marad a független biztonsági út. |
| `catalog` | Opcionális, korlátozott lekérdezés | Csak valós, validált, cache-elt műholdrekordokat és TLE-epochokat ad vissza. |
| `passes` | Opcionális `noradId`, korlátozott intervallum/darabszám | Korlátozott előrejelzési feladat; valódi számított felkelési/culminációs/lenyugvási UTC-t és geometriát ad. Nem blokkolhatja a motor-szolgáltatási ciklust. |

Az adapter a host meglévő `path`/`op` burkában többek között az alábbi
útvonalakon teheti elérhetővé ezeket: `/rotor/status`,
`/rotor/sensorsstatus`, `/rotor/home`, `/rotor/calibrate`, `/rotor/goto`,
`/rotor/track`, `/rotor/stop`, `/satellites/catalog` és
`/satellites/passes`. Ne hozz létre második, nem hitelesített BLE-
szolgáltatást, és ne engedd távoli hívónak helyi konzol-felhasználó
szerepének állítását.

Az ugyanazon hoston futó Bluetooth-/rádió-kezelő frontend kizárólag helyi
adapterinterfészt használhat:
`rotor.radio_adapter.open_adapter(controller_config_path)`. Az eredmény
`snapshot()`, `dispatch(path, operation, data, peer)`, `disconnect(peer)` és
`close()` metódusú objektum. A `snapshot()` a rotor-host
`cm5-rotor/v1` biztonsági/követési objektumát adja vissza: `sampledMonotonic`,
`hardwareCommissioned`, `gnssValid`, `gnssSampledMonotonic`, `sgp4Valid`,
`trackingSampledMonotonic`, `fault`, `utc` (a tényleges GNSS-alapú
propagált állapot Unix-másodperce), `site`
(`[latitudeDeg, longitudeDeg, altitudeM]`), `rangeRateMps` és a teljes
`status` objektum. Az érvénytelen adat `null`/hamis, és hibát tartalmaz;
soha nem gyártott, érvényes nullérték.

A rádió-host legalább 200 ms-onként kérdezze le a `snapshot()`-ot, hogy
teljesüljön a jelenlegi snapshot-korhatár. A követési bemenet érkezési
idejeként a `trackingSampledMonotonic` értéket használja, ne a későbbi
lekérdezés idejét. A rotor GNSS-forrása 10 másodperc után lejár; az SGP4
500 ms-onként frissül, a híd pedig az 1 másodpercnél régebbi mintát
elutasítja. A host ettől külön legalább 500 ms-onként frissítse a rotor
biztonsági állapotát. Hiányzó, elavult, üzembe nem helyezett vagy hibás
adat esetén a host nem jelezhet ellenőrzötten egészséges állapotot vagy
érvényes Doppler/követést. Az önálló helyi CLI független ettől a frontendtől,
valamint a rádió/SDR/PA-függőségektől; a telefon vagy rádiófolyamat
elvesztése nem állítja le a futó rotoros követési munkamenetet.

Az állapot legalább a `state`, `fault`, `verifiedHealthy`, `commissioned`,
`calibrated`, `updatedMonotonic`, `axes`, `sensors` és `satellite` mezőket
tartalmazza. Minden tengely mezői: `positionDeg`, `targetDeg`, `homed`,
`encoderValid`, `encoderAgeMs`, `minimumLimitClosed` és
`maximumLimitClosed`. A műholdadatok mezői: `noradId`, `name`, `utc`,
`latitudeDeg`, `longitudeDeg`, `altitudeKm`, `azimuthDeg`, `elevationDeg`,
`rangeM`, `rangeRateMps`, `apparentTrackAngleDeg`, `siteUtc` és `gnssAgeMs`.
Az érvénytelen/nem elérhető érték `null` marad hamis érvényességjelzővel;
soha nem helyettesíthető nullával.

Az érzékelőállapot ezenkívül `motorPermitHealthy`, `driverFaultsClear`,
`interlockAgeMs` és `interlocksValid` mezőket is közöl. Üzembe helyezéshez
és mozgáshoz friss, validált motorengedély-visszajelzés, E-stop/watchdog
visszajelzés és mindhárom revízió-A aktív alacsony meghajtóhiba-bemenet
(BCM24–26) szükséges. A hibabemenet csak azután jelenthető töröltnek, hogy
a BSP validálta a fizikai bemeneti áramköröket és megfigyelte az inaktív
HIGH szintet. Hiányzó, elavult, hibás vagy nem validált visszajelzés mindkettőt
blokkolja. Az MCP23017 visszajelzési polaritása a fizikai áramkör pontos
definíciójától függ; GPIO-kérés vagy szoftveres átalakítás nem bizonyítja a
független engedélylánc oldott állapotát.

### A rotor állapotának továbbítása a közös PTT-biztonságnak

A megbízható helyi adapter legalább 500 ms-onként frissítse a rádió-host
`Safety.rotor_update(fault, verified=True)` állapotát. `verified=True`
csak akkor megengedett, ha a teljes, üzembe helyezett hardverlánc jelen
van és friss: vezérlő/meghajtó visszajelzései, mindhárom encoder-csatorna,
mind a hat NC-határoló, külső vészleállító/watchdog állapota, a szükséges
GNSS- és attitűd-bemenetek, érvényes kalibráció, valamint aktív vagy
követési hibából eredő hiba hiánya. Egyébként nem ellenőrzött/hibás
rotorállapotot jelentsen. Ismeretlen, elavult, nem ellenőrzött vagy hibás
rotorállapot tiltja a közös fizikai PTT-t. BLE-kliensek nem jelenthetik a
rotor egészségét, és nem törölhetik a rotorhibát.

A hibák reteszelődnek. A helyreállításhoz a hibaokot meg kell szüntetni,
érvényes, friss visszajelzések szükségesek, el kell végezni az előírt helyi
ellenőrzést/visszaállítást, majd új, kifejezett helyi élesítés kell. A Linux-
szál takarítása és az SPI-leállítási parancs legfeljebb szoftveres
best-effort; nem helyettesíti a független elektromos lekapcsolást.

## Tengelyek, visszajelzés és mozgási követelmények

A mechanikai áttételek konfigurációs bemenetek maradnak, amíg a
mechanikáért felelős fél be nem fagyasztja őket. A jelenlegi munkaszámok
kifejezetten előzetesek: AZ és EL 25:1, 200 teljes lépés/fordulatú motorral
és 16 microsteppel (80 000 motor-microstep a kimeneti fordulaton); POL 5:1
(16 000 microstep/fordulat), javasolt +/-90 fokos mechanikai végütközőkkel.
A POL javasolt egyfokozatú szíjhajtása 20:100; kezdeti szoftveres határa:
-80 és +80 fok, két NC-kapcsolójának célkioldása +/-85 fok, a jelölt ütközők előtt.
A szemléltető 200 lépéses motor és 16 microstep 16 000 parancsolt
microstepet jelent kimeneti fordulatonként (0,0225 fok/parancs-inkrementum,
nem pontosság). Ezek dokumentációs egyeztető értékek, nem rögzített vagy
validált mozgáskonfigurációk. Tengelyt ne engedélyezz a mért áttétel, a
kapcsolóműködés, ütközőhézag/-szilárdság, teljes kábel-szervizhurok,
hasznos teher kiegyensúlyozása és enkóder-visszajelzés elsődarabos
ellenőrzéséig.

A mechanikai jelentés példabeli, csak antennára vonatkozó CG- és
tehetetlenségi értékei nem teljes tengelyminősítések. Mérd le újra a POL
fokozatot és a terhet, mérd meg az összeállított súlypontot és tengely-
tehetetlenséget, majd számítsd újra a hozzáadott EL/AZ gravitációs és
tehetetlenségi terhelést a POL-motorral/kerettel, kábelköteggel és mozgó
szerkezettel együtt. A példából ne következtess motornyomaték-megfelelőségre
vagy kültéri terhelhetőségre; a kiválasztott motor dinamikus nyomatékgörbéje
és fizikai terhelésvizsgálatok továbbra is szükségesek.

Linux GPIO soha nem generálhat lépésimpulzust. Egy lehetséges TMC5160 a
rámpát belsőleg hajthatja végre pozíciómódban, a `RAMPMODE`, `XTARGET`,
`VMAX`, `AMAX` és `DMAX` regiszterekkel. Sebességátváltás vagy rámparegiszter
csak a kiválasztott chip adatlapja, órajele, microstep- és panelkonfigurációja
ellenőrzése után tekinthető validáltnak. Az SPI-adapter a chip 5 bájtos
kereteit és dokumentált, csővezetékes olvasási szemantikáját használja,
ellenőrzi a visszaadott regiszter-/állapotértékeket, helyesen deaktiválja a
chip selectet, és láthatóvá teszi a buszhibákat. A sikeres syscall/írás
önmagában nem bizonyítja, hogy a meghajtó készen áll. A konkrét hordozópanel,
lábkiosztás, SPI-mód/órajel, engedélyezési polaritás, power-good és
meghajtóhiba-kábelezés továbbra is hardverkiválasztási/próbapadi ellenőrzési
feladat.

Három független kimeneti encoder és hat NC-határoló van (AZ, EL, POL
tengelyenként minimum és maximum). Bármely hiányzó, elavult, mágneshibás,
hihető tartományon kívüli vagy meghajtópozícióval ellentmondó encoder
megtiltja a mozgást. A határolóbemenet csak igazoltan zárt NC-áramkör esetén
egészséges; szakadás, bemenetvesztés vagy ellentmondás hiba. Az irányfüggő
határellenőrzés a keményütköző előtt leállítja a mozgást; hiba után egyetlen
tengelyt sem szabad pusztán helyreállítási kísérletként megmozgatni.

A javasolt encoder-megvalósítás tengelyenként egy AS5600-at használ
`0x36` I2C-címmel, TCA9548A-csatornán (javasolt csatornák: 0, 1, 2).
A TCA9548A csatornaválasztási viselkedését és az AS5600 mágnesállapot-/nyers
szög-regisztereinek értelmezését az elsődleges adatlapokkal és a
kiválasztott panellel kell ellenőrizni. Minden mintánál rögzíteni kell a
kiválasztott csatornát, monotón olvasási időt, nyers szöget és MD/MH/ML
állapotot. Követelmény: mágnes észlelve (MD=1), sem túl erős, sem túl
gyenge mező (MH=0, ML=0); az elavult/érvénytelen minta elutasítandó.
Encoderhiányból vagy szenzorbusz-hibából nem származhat hihetőnek látszó szög.

Az iránytű és IMU hardverkiválasztása még nincs befagyasztva. A pontos
elsődleges adatlapok, panelkábelezés, tengelyorientáció, mintaérvényességi
ellenőrzés és kalibrációs eljárás rögzítéséig csak validált, időbélyeges
visszajelzéseket átadó, injektált `SensorInputs` határ használható; ez nem
produkciós hardvermeghajtó. A dőléskompenzáció a mért gyorsulásmérő-dőlést
használja. Valódi irányhoz a teljes összeszerelt rendszeren hard-/soft-iron
kalibrálás és explicit, korlátozott, forrással/dátummal igazolt deklináció,
vagy explicit módon megadott és függetlenül ellenőrzött kézi valódiészaki
referencia kell. A hiányzó deklináció nem nulla, és pusztán GNSS-
koordinátákból nem következik irány.

A kért AZ/EL elfordulási sebességkorlát 2,25 fok/másodperc. A POL javasolt
1 fok/másodperces korlátja előzetes marad a mechanikai konfiguráció
befagyasztásáig. A mozgást monotón idejű szolgáltatás hajtja; minden
hardverbusz/meghajtónak egy tulajdonosa van, a parancssor korlátozott,
a határidők felügyeltek, és a követési hiba ellenőrzött. Bármely Python-
munkás kivétele, elmulasztott szolgáltatási határidő, meghajtóhiba vagy
érzékelő-timeout hibáztatja a rendszert, és `finally` blokkban megkísérli
a tiltást/leállítást; ha a szoftver nem fut, az elektromos védelemnek
függetlenül kell megszakítania a tápot.

A homing véges (tengelyenként legfeljebb két perc), csak az üzembe helyezett
helyi eljárással végezhető, és kizárólag az adott tengely NC minimum
bemenetét használja. Azonnal meg kell állnia timeout, sikertelen
kapcsolóátmenet, encoder-vesztés, váratlan maximumkapcsoló-állapot,
meghajtóhiba, vészleállító vagy watchdog-hiba esetén. A homing csak
munkamenet-érvényű mechanikai referenciát állít be; nem ment egyélű alapot,
nem következtet földrajzi északra, és nem helyettesíti a kalibrációt.

## GNSS, SGP4 és műholdkimenetek

A GNSS-parser tényleges NMEA-mondatokat dolgoz fel ellenőrzött
ellenőrzőösszeggel és érvényes vevő-fixállapottal. UTC-t és helyet csak
összefüggő fixből fogad el, és tíz másodperc érvényes frissítés nélkül
érvénytelenít. Hiányzó, hibás vagy elavult fix soha nem esik vissza
`(0, 0)`-ra, host-fali órára vagy mesterséges epochra.

A műholdpozíciót pontosan rögzített `sgp4` Python-disztribúció számítja,
Vallado SGP4/SDP4 implementáció alapján; a unit tesztek ismert Vallado
tesztvektort használnak. Ellenőrzendők a TLE-sorszámok, fix szélességű
mezők, ellenőrzőösszegek, NORAD-identitás, epoch és a propagált állapot
hibája. A TLE-csere atomikus; a cache korlátozott (48 KiB és 100 NORAD-ID).
Nem támogatott vagy lejárt elemkészlet nem frissíthető észrevétlenül és
nem helyettesíthető kitalált adattal.

Az SGP4 TEME-helyzetet és -sebességet konzisztensen kell átalakítani
Földhöz rögzített/helyi topocentrikus rendszerbe. A távolságsebesség a
relatív helyzetből és relatív sebességből számítandó (beleértve a
megfigyelőhely Földforgási sebességét), nem két külön mintavételű pozíció
véges differenciájából. A véges, validált eredményt a pontosan felhasznált
GNSS-UTC időbélyegével kell ellátni. 15 fokos eleváció alatt nem kérünk
ráállást. A 89 fokos zenitőr elkerüli az azimut szingularitását; átlépése
vagy elérhetetlen/kábelcsavarodást okozó cél esetén korlátozott biztonságos
leállítást/újratervezést kell végezni, soha nem utasítást a tengelyhatár
átforgatására.

Az átvonulás-előrejelzés korlátozott háttérfeladat: csak üresjáratban vagy
igazolt szolgáltatási tartalékkal futhat, és át kell adnia a vezérlést
motor-kiszolgáláskor. A normál motor- és hibafelügyeleti ciklus nem várhat
hálózati/TLE-letöltésre vagy átvonulásszámításra. A `catalog`, `passes`,
`track` és állapotkimenetek kizárólag valós, validált műhold-ID-t, nevet,
UTC-t, koordinátát, szöget, távolságsebességet és frissességet mutathatnak.
Az Android kijelezheti ezeket a valós értékeket; helykitöltő célt nem
jeleníthet meg élő követésként.

## Függőségek és validálás

A rotor Python-függőségi jegyzéke maradjon külön a `radio/` könyvtártól.
Az SGP4-csomag verzióját pontosan rögzíteni kell, upstream licencét/
közleményét fel kell jegyezni; a könyvtárat ne másold a tárolóba.
Hardverelérési könyvtárat csak a Linux-hordozópanel befagyasztása után
válassz, és szükség szerint projektlokális környezetbe vagy a Linux-
disztribúció csomagkezelőjével telepíts. Python-csomagot globálisan ne telepíts.

A unit tesztek kifejezetten elnevezett szimulált meghajtó-/érzékelő-fixture-
eket használnak, és fizikai mozgás nélkül vizsgálják a vezérlőt és a
hibameneteket. Kötelező tesztek: NMEA-ellenőrzőösszeg és frissesség;
Vallado SGP4-helyzet/sebesség és topocentrikus távolságsebesség vektorok;
TLE-validálás/cache-határok; encoder mágnesállapot/adatkor; minden NC/
vészleállító/watchdog/meghajtóhiba; határok és előzetes sebességkorlátok;
homing-timeout; kizárólag helyi, explicit üzembe helyezés; szálhiba és
leállítás; API siker/hiba-válasz alakja; valamint rádió-host rotorállapot
frissesség/tiltás integrációja.

A szoftvertesztek nem tudják igazolni a hordozópanelt, motoráram-/hőhatárokat,
mechanikai terhelést, leállító-kábelezést, watchdog-függetlenséget, encoder-
igazítást, iránytű mágneses zavarását, GNSS-telepítést, rádió/PTT-viselkedést
vagy a CM5 terhelés alatti időzítését. Ezek kifejezett üzembehelyezési és
terepi tesztblokkolók maradnak. A Linux nem kemény valós idejű operációs rendszer.
