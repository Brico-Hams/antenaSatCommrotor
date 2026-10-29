# Autonóm vezérlés — ESP32-prototípus

Az eredeti projekt szerzői Anatol (EA5KAO), Diego (EA5JEF) és Pedro Roca Molina, a Bricohams oktatási környezetében (`https://bricohams.org`). A szerzői attribúcióért és korlátozásokért lásd a projekt AUTHORS, ACKNOWLEDGEMENTS és DISCLAIMER fájljait. A hivatkozások és függőségek saját szerzőiket megtartják; támogatás nem következik belőlük. Gyermekek/serdülők csak felnőtt felügyelete mellett tevékenykedhetnek, és nem adhatnak engedély/licenc nélkül.

## Hatókör és állapot

Az ESP32 **valódi SGP4-et** számít, nem Kepler-közelítést, a LittleFS-ben tárolt TLE-kből. Az NMEA GNSS adja az UTC-t és a helyet; a böngésző csak megjelenít és parancsot küld. Terepen nincs szükség Node-szerverre, felhőre vagy számítógépre. A 145/435 MHz-es kétsávos antenna közös rámutatást használ. A PTT/CAT **letiltott**: nem feltételezzük, hogy az RT3S teljes duplex módú vagy CAT-képes. Az OpenGD77-et és annak csatornáit/Dopplerét külön kell konfigurálni; a kijelzett eltolások névleges 145 és 435 MHz-et használnak, és nem helyettesítik a frekvenciatervet.

Ez szoftveresen lefordított és tesztelt prototípus, **terepen nem validált**. A motorokat, GNSS-t, RF-et, mindhárom szerverrel a TLS-t, enkódereket, ellenséges forgalom melletti késést és tanúsított biztonsági eljárást nem tesztelték. Ez nem funkcionálisan tanúsított vészleállító.

A vezérlő nem engedélyez semmilyen terepi terhet vagy szélállapotot. A 8 m/s, 0,06 m²-es felület és 0,25 m-es kar mechanikai példája **nem teljesíti** a közölt tervezési számítás biztonsági tartalékát; üzemi határként kezelni tilos. A 80 000 mikrolépés/fordulat konfiguráció 25:1 tényleges áttételt feltételez: a próbapadon ellenőrizd mindkét fokozatot, reteszelt illesztéseket és tényleges áttételt. Az antenna tömege/egyensúlya és az ASA-alkatrészek merevsége mérést igényel; az érvényes STL-háló vagy sikeres fordítás nem bizonyít mechanikai teherbírást.

A projekt saját fájljai:

* `firmware/platformio.ini`, `firmware/include/board_config.h`
* `firmware/include/control_logic.h`, `firmware/src/main.cpp`
* `firmware/include/ble_protocol.h` (megosztott keretezés és hitelesítés)
* `firmware/.gitignore` (kizárja a helyi eszközöket/buildet)
* `web/index.html` (teljesen offline spanyol felület)
* `tests/control_logic/test_native/test_main.cpp`
* `tests/control_sgp4.cpp`, `tests/control_web.test.cjs`
* ez a dokumentum

## Ellenőrzött függőségek és build

PlatformIO Core 6.1.18; `espressif32@6.10.0`, `esp32dev` (klasszikus ESP32, WROOM, 4 MB flash), Arduino ESP32 **2.0.17**, `framework-arduinoespressif32@3.20017.241212`, Xtensa `8.4.0+2021r2-patch5`; ArduinoJson 6.21.5; TinyGPSPlus 1.1.0. Bluetooth: **h2zero/NimBLE-Arduino 1.4.3**, a gyökér Apache-2.0 licenc ellenőrizve: `https://github.com/h2zero/NimBLE-Arduino/blob/1.4.3/LICENSE`. Binárisok terjesztésekor őrizd meg a licencet/értesítéseket és az Apache NimBLE stack értesítéseit. Klasszikus Bluetooth és Bluedroid nincs használatban; legfeljebb egy BLE-kapcsolat.

SGP4: [Hopperpop/Sgp4-Library](https://github.com/Hopperpop/Sgp4-Library) 1.0.3, commit **7c82d31f9d9a286acde5ef55da8308fc93d2ba96**. Ellenőriztük az `Sgp4::init`, `site`, `findsat`, `satrec.error` tényleges aláírásait és a rögzített forrás TEME→megfigyelő számítását. Az upstream burkoló WGS84-et választ; belső pufferei kifejezetten inicializálódnak, és a sorok módosítható másolatait adja át. A független teszt WGS72-tel hasonlít a Vallado 00005 ellenőrző vektorához: R=(7022.46529266,-1400.08296755,0.03995155) km, V=(1.893841015,6.405893759,4.534807250) km/s. Hivatkozás: [CelesTrak SGP4 szoftver](https://celestrak.org/software/vallado-sw.php). A függőségkezelő megőrzi a könyvtár saját értesítéseit/licenceit; a forrás nincs vendorizálva vagy módosítva.

Ennek az alrendszernek az **eredeti szoftvere** a felhasználó választása és a projekt NOTICE szerint MIT licencű; az eredeti hardver CERN-OHL-S-2.0 licencű. Ez nem rendeli hozzá a MIT licencet a teljes belinkelt firmware-hez. E licencek nem licencelik át a könyvtárakat, eszközöket vagy külső hivatkozásokat: minden függőség megtartja saját licencét. Ismeretlen licencű forrásokat nem terjesztünk újra, távoli publikálás nem történt.

A rögzített SGP4 commit `LICENSE` fájlját ellenőriztük: **The MIT License (MIT), Copyright (c) 2016**; a szerzői jogi és engedélyezési értesítéseket meg kell őrizni másolatban vagy lényeges részekben, beleértve az azt tartalmazó terjesztett binárist is. Nyilvános bizonyíték: `https://github.com/Hopperpop/Sgp4-Library/blob/7c82d31f9d9a286acde5ef55da8308fc93d2ba96/LICENSE`. A README Grady Hillhouse koordináta-transzformációját is MIT-licencűnek jelöli. Ebben a függőségben GPL-t nem találtunk; ez nem licenceli át a többi könyvtárat, Arduino ESP32-t vagy eszközöket. Bináris terjesztése előtt őrizd meg **minden** belinkelt függőség értesítéseit, és vizsgáld meg a pontos framework-verzió kötelezettségeit.

PlatformIO-val rendelkező fejlesztői környezetben:

```powershell
Set-Location .\firmware
pio run -e esp32
pio run -e esp32 -t buildfs
pio run -e esp32 -t upload
pio run -e esp32 -t uploadfs
pio device monitor -b 115200
pio test -e control_native
```

A natív teszthez GCC/G++ kell a PATH-on. Ezen a gépen nem volt használható Python, PlatformIO vagy GCC; beágyazott Python 3.11.9-et, PlatformIO 6.1.18-at és Zig 0.13.0-t töltöttünk le **kizárólag a `firmware/.tools` alá**, globális telepítés nélkül. A VS Code Python-környezet-konfigurációs szolgáltatásoknak nem volt megvalósításuk. A beágyazott Pythonnak helyi esptool 4.5.1 kellett, mert az izoláció miatt nem tudta importálni a PlatformIO külső szkriptcsomagját.

Ténylegesen lefuttatott tesztek:

* ESP32 fordítás/linkelés és `firmware.bin` generálása: **SIKERES**.
* `index.html`-t tartalmazó LittleFS build: **SIKERES**.
* Ziggel fordított/futtatott hat Unity teszt: **6 SIKERES, 0 hiba**: határok/koordináták, UTC/szökőévek/lejárat, TLE-checksum/epoch, sebesség-/gyorsulás-/leállítási/pozitív és negatív mozgáshatárok, USB-hitelesítőadat-ellenőrzés, BLE-keretek/hitelesítés (valódi titok nélkül).
* Futtatható program a rögzített SGP4 ellen: Vallado epoch vektor **SIKERES**, tűrés: pozíció 1 m, sebesség 1 mm/s.
* `node --test tests/control_web.test.cjs`: **SIKERES** (szintaxis, DOM-azonosítók, nyolc hitelesített művelet, HTML-ként nem megjelenített műholdnevek és statikus firmware-retesz-ellenőrzések; nem szimulál időzítést vagy hardvert).
* A `pio test -e control_native` kezdetben GCC-hiány miatt elbukott; ugyanazt a Unity-kódot alternatívaként Ziggel futtattuk. Ezt a parancsot nem tüntetjük fel sikeresként.

A `.pio/build/esp32` binárisai fejlesztési artefaktumok, nem bizonyítják a flashelést vagy fizikai működést. A LittleFS feltöltése felülírja tartalmát: fájlrendszer-frissítés előtt exportáld a TLE-ket.

### WebFlash/CI csomag (csak klasszikus ESP32)

A CI `secrets.h` nélkül is fordíthat: a `board_config.h` üres hitelesítő adatokat és `carrierVerified=false` értéket tartalmaz. Ez a biztonságos kép hatástalanítottan indul, **helyi USB-provisionálásig nem üzemelő AP-val**; az AP konfigurálásához nem kell újrafordítani. Privát jelszót/tokent ne tegyél nyilvános GitHub Pages-képbe.

### Helyi USB-provisionálás (nyilvános kép)

Válaszd le a motorokat/RF-et. Nyiss helyi 115200-as soros konzolt (ESP Web Tools konzol vagy naplózás/telemetria nélküli helyi terminál), és küldj minden JSON-t LF-fel záruló sorban:

1. `{"cmd":"setup"}`: lekapcsolja a Wi-Fit, ENABLE OFF és provisioning-hiba állapotot kényszerít ki, érvényteleníti a homingot/kalibrálást, és blokkolja az API-t.
2. `{"cmd":"config","ssid":"Valasztott nev","password":"SAJAT_PRIVAT_JELSZO","token":"SAJAT_VELETlen_PRIVAT_TOKEN"}`. Helyettesítsd az értékeket: SSID 1..32, jelszó 12..63, véletlen token 24..128 nyomtatható ASCII karakter. Opcionális `staSsid` és `staPassword` (≥8); elhagyásuk törli a mentett STA-adatokat. Ne küldj titkot távoli szolgáltatásba, és ne publikáld a konzolelőzményt.
3. Csak a panel/meghajtó/polaritások fizikai validálása után: `{"cmd":"carrier","verified":true}`. Nem indítja és nem élesíti a motorokat. A `verified:false` a következő indításkor visszavonja a hardverengedélyt.
4. `{"cmd":"reboot"}`. Hatástalanítva indul; csatlakozz a beállított biztonságos AP-hoz, nyisd meg a `http://192.168.4.1` címet, és add meg a tokent az oldalon.

A parser maximuma 768 bájt/sor; a válaszok nem ismétlik meg a titkokat. A hitelesítő adatok privát, **nem titkosított** NVS-ben maradnak: a flash fizikai hozzáféréssel kiolvasható; ez a prototípus nem állít be flash encryptiont/secure bootot. Az NVS-konfiguráció nem teljes tranzakció: írási hiba esetén maradj SETUP állapotban és próbáld újra. A konzolon nem állítható be CA PEM; a HTTPS-hez érvényes, befordított gyökértanúsítványok kellenek, míg a kézi TLE-import a nyilvános képpel működik. USB-hozzáférésű kezelő módosíthatja a konfigurációt; védd a fizikai hozzáférést. A homing/kalibrálás soha nem tárolódik, a hordozó ellenőrzésének mentése mellett sem.

### Biztonságos Bluetooth LE és Android

A kép lehetővé teszi a Wi-Fi AP és BLE egyidejű működését; együttélésük és fizikai késésük nincs mérve. A BLE gyárilag letiltott. Helyi USB SETUP-ban add hozzá: `{"cmd":"ble","enabled":true,"passkey":SAJAT_PRIVAT_HATJEGYU_SZAM}`. Helyben válassz 100000..999999 közötti számot, ne e dokumentum globális passkey-jét használd; az érték nem íródik ki. `enabled:false` újraindítás után letiltja a BLE-t. A BLE-konfiguráció módosítása a következő induláskor törli a tárolt bondokat. A konzol továbbra is OFF állapotban kényszeríti a motorokat; ezután `{"cmd":"reboot"}`.

Androidot a rendszer párbeszédablakával és a privát passkey-jel párosítsd; **Secure Connections, bonding és MITM kötelező**, bizonytalan alternatív módot soha ne fogadj el. Az alkalmazásba a helyi API-tokent is írd be; az nem kerül felhőbe. Minden parancshoz, még a STOP/status művelethez is, titkosított/hitelesített/bonded kapcsolat és helyes token kell. A rádió/NVS nem egyenlő a secure boottal: védd a fizikai hozzáférést.

GATT **v1** protokoll, hirdetett név: `PortableSatStation`:

* Szolgáltatás: `c8200001-4e53-4253-9000-000000000001`
* RX írás **ATT-nyugtával**, titkosítva/hitelesítve: `c8200002-4e53-4253-9000-000000000001`
* TX-értesítések: `c8200003-4e53-4253-9000-000000000001`

Küldés előtt iratkozz fel a TX-re. A minimum MTU 23 működik, nagyobb MTU egyeztetésétől függetlenül. Minden keret ≤20 bájt: byte0=0x53; byte1 START=1, END=2 flag (egyetlen keretnél 3); byte2/3 little-endian uint16 szekvencia, kezdőérték 0, lépésköz 1; byte4..19 1..16 bájt UTF-8 JSON-t tartalmaz. NUL és ismeretlen flagek nincsenek. Parancs csak érvényes END, séma és hitelesítés után hajtható végre. Kérés ≤2048 bájt, összeállítási időtúllépés 3 s, egyszerre egy kérés/válasz. Sorrenden kívüli/interleaving/túlcsordulási hiba esetén nincs részleges végrehajtás.

Teljes kérés:
`{"v":1,"id":1,"method":"POST","path":"/api/calibrate","token":"PRIVAT_TOKEN","body":{"trueAz":0,"levelConfirmed":true}}`.
Az ID pozitív egész, **kapcsolatonként növekvő**. GET esetén `body:{}`.
Teljes válasz: `{"v":1,"id":1,"code":200,"data":{"message":"..."}}`.
A `data` pontosan a HTTP JSON objektumát használja; visszanyerhető ID nélküli keretezési hibánál id0. Válasz ≤8192 bájt; a nagyobb katalógus 413-at ad, HTTP-n kell lekérni/importálni. Foglalt sornál 429, időtúllépésnél 408. A következő kérés előtt várd meg az előző válasz END-jét, kivéve hitelesített STOP előre sorolását, amely megszakíthatja az előző választ.

Azonos handlerek/reteszek: `/api/status`, site, home, move, stop, clear, calibrate, select, track, passes, tle GET/POST. BLE-n az `/api/update` 409-et ad: HTTPS csak HTTP-n, nyugalmi állapotban. TLE BLE-n csak 2048 bájtba férő részhalmazzal; csendes csonkolás nincs. A firmware nem másol második mozgáslogikát. A STATUS hozzáadja a `controlOwner` (HTTP/BLE/none), `bleConfigured`, `bleConnected`, `bleSecure`, `encoderZeroVerified` értékeket. A STATUS kompatibilitást jelez `apiVersion=2`, `protocolVersion=1` és `firmwareVersion="0.3.0-prototype"` mezőkkel; ezt hitelesített kézfogásra használd, külön auth-útvonal nincs. Az API 2 (Bricohams Android-integráció) hozzáadja a hitelesített `POST /api/time` (`{"utcMs":...}`) útvonalat: GNSS nélkül egy megbízható alkalmazás 10 percre beállítja az UTC-t; a GNSS UTC mindig elsőbbséget élvez (409), járó motorok mellett a 2 s-nál nagyobb ugrás elutasítva. A STATUS új mezői: `timeSource` (`none`/`gnss`/`app`), `microsteps`, `transmissionRatio`, `stepsPerDegree`, `maxDegPerSecond`. Az `esp32_nema17` PlatformIO-környezet az olcsó profilt fordítja: újrahasznosított NEMA17, TMC2209 1/8 mikrolépéssel, azonos 25:1 szíjak, 40000 mikrolépés/fordulat, legfeljebb 6,0 °/s. Lefordítva; panelen és rotoron nem tesztelve. Mozgás közben a másik átviteli módból érkező módosítások 409-cel elutasítva; hitelesített STOP mindig elérhető. HOME/MOVE kézi művelet közbeni BLE-szétkapcsolás hibát okoz és érvényteleníti a homingot; az autonóm TRACK GNSS/TLE/reteszek mellett folytatódik, a telefonkapcsolat nem szükséges hozzá.

Az értesítések kézbesítése nem garantált: az alkalmazás észlelje a szekvencia-/időtúllépést, majd kérdezze le újra a státuszt; ATT-írásból soha ne feltételezze a végrehajtást. A fizikai vészleállító és a biztonsági feladat nem függ a telefontól vagy átviteli módtól. Ha a motorhatáridő túllépi a 20 ms-ot, hiba; a Wi-Fi/BLE együttélés nincs tanúsítva.

### Nagy TLE-átvitel Androidról (ugyanaz a v1 protokoll)

A telefon a megengedett szolgáltatóktól HTTPS-en tölti le, majd **TLE-t**, nem pályát továbbít: az SGP4, a passzok és a követés továbbra is a rotorban számítódnak. A katalógus legfeljebb 100 műholdat/48 kB-ot támogat; ha túllépi, válassz részhalmazt. Csendes csonkolás nincs. Új, megosztott HTTP/BLE POST-útvonalak:

| Útvonal | Body / eredmény |
|---|---|
| `/api/tle/begin` | `{length:1..48000,sha256:"64 hex lowercase"}` → `{message,uploadId}` |
| `/api/tle/chunk` | `{uploadId,offset,text}`; text 1..512 UTF-8 bájt, az offset pontosan szekvenciális → `{message,received}` |
| `/api/tle/commit` | `{uploadId}` → pontos SHA256 és hossz, TLE-validálás és atomi rename; 200 vagy 400, hiba esetén korábbi gyorsítótár marad |
| `/api/tle/abort` | `{uploadId}` → 200, gyorsítótár megmarad |
| `/api/catalog` | `{offset:0,limit:10}`; limit 1..10 → `{total,nextOffset,satellites:[{id,name,epoch,fresh}]}`; végén nextOffset=-1 |

A hash és offset az átvitt szöveg pontos bájtjain számolandó (SHA256 előtt normalizálj). A begin nem cseréli le a gyorsítótárat; commit csak minden chunk és egyező hash után történik. Az átvitelt HTTP/BLE tulajdonolja, egyéb módosítás 409-cel blokkolt; aktív átvitel alatt motor nem indulhat. 60 s inaktivitás RAM-beli megszakítást okoz, a gyorsítótár érintése nélkül. BLE-szétkapcsolás azonnal megszakítja saját RAM-átvitelét és felszabadítja a tulajdonost, a perzisztált gyorsítótár módosítása nélkül.

A hash/validálás/flash műveletek a loopban/handlerekben futnak, **soha nem BLE callbackben**; a szétkapcsolási callback csak felszabadítja a RAM-átvitelt, az RX callback pedig csak összeállít és sorba tesz egy ellenőrzött, korlátozott méretű kérést. A `/api/passes` lekérdezései inkrementálisak/idle-only maradnak; az Android addig kérdezi a `calculating` értéket, amíg false nem lesz. Az alkalmazásnak nem kell és nem szabad SGP4-et megvalósítania ahhoz, hogy pályát adjon át a rotornak.

### Webes/alkalmazásbeli kalibrációs segéd (eljárás)

A webes felület lépéseket és HOME/motorok/szintezés/észak/enkóderek/hely/UTC állapotot mutat. Fizikai kezelővel hajts végre HOME-ot; várd meg a READY-t, mozgasd EL=0-ra, műszerrel szintezd, és figyeld a **valódi észak** megbízható referenciáját, ne az álló GNSS-t. Engedélyezett AS5600 esetén HOME-kor kimeneti nullákat vesz fel és megköveteli az `encoderZeroVerified` állapotot. A POST calibrate homed, nyugalmi/ENABLE OFF, EL=0 és megerősített szint feltételű; offset=aktuális irány−AZmechanikai. Automatikusan megvalósított IMU-/magnetométer-érzékelő nincs. Reset, új homing vagy szerelésváltozás után kalibrálj újra.

```powershell
pio run -d firmware -e esp32
pio run -d firmware -e esp32 -t buildfs
```

A layoutot a rögzített framework `default.csv` fájljával ellenőrizték; klasszikus ESP32 DevKitC V4 WROOM-32E, 4 MB flash, PSRAM nélkül. S3/C3/WROVER esetén ne használd újra.

| Rész | Build-útvonal | Hex / decimális offset |
|---|---|---|
| bootloader | `firmware/.pio/build/esp32/bootloader.bin` | 0x1000 / 4096 |
| partíciós tábla | `firmware/.pio/build/esp32/partitions.bin` | 0x8000 / 32768 |
| kezdeti OTA | `$PLATFORMIO_CORE_DIR/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin` | 0xe000 / 57344 |
| alkalmazás | `firmware/.pio/build/esp32/firmware.bin` | 0x10000 / 65536 |
| LittleFS web | `firmware/.pio/build/esp32/littlefs.bin` | 0x290000 / 2686976 |

A fájlrendszerpartíció neve `spiffs`, de LittleFS formátumú, mérete 0x160000 (1 441 792 bájt). **A LittleFS-t is írd fel**, különben a `/` 503-at ad. Az ESP Web Tools manifest a fenti öt részt/offsetet használhatja; egyesített binárishoz esptool 4.5.1 kell:

Flash-elés előtt válaszd le a motorokat és RF-et, és használj védett tápot. A prototípus-kép nem tanúsítja vagy hagyja jóvá a csatlakoztatott panelt.

```powershell
esptool.py --chip esp32 merge_bin -o combined.bin --flash_mode dio --flash_freq 40m --flash_size 4MB `
  0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin `
  0x10000 firmware.bin 0x290000 littlefs.bin
```

Futtasd az öt bináris részt tartalmazó könyvtárban; az egyesített kép **0x0** offsetre írandó. A csomag megtartja a belinkelt függőségek értesítéseit, és nem licenceli át MIT-ként az egészet. A fájlrendszer flashelése vagy a chip törlése megsemmisíti a helyi TLE/NVS adatokat: WebFlash-felületnek ezt egyértelműen jeleznie kell.

## Kötelező vezetékezés és provisionálás

A `board_config.h` a **38 tűs ESP32-DevKitC V4 WROOM-32E, PSRAM nélkül** rögzített térképét adja. A `carrierVerified=false` motorokat/GNSS-t letiltva tartja a hordozópanel fizikai ellenőrzéséig és a `cmd carrier` USB-konzolos megerősítéséig (vagy egy privát buildben true értékre állításáig). WROVER, S3/C3 vagy más fejléc-elrendezésű modul esetén nem használható. Flashelés előtt elektromosan ellenőrizd a tényleges térképet. Az ellenőrzés elutasítja a duplikált, flash/fenntartott/strapping/konzol tűket, a 34-es vagy nagyobb kimeneti GPIO-t, valamint busz/UART-átfedéseket. A GPIO34–39 nem rendelkezik belső felhúzással: minden biztonsági bemenetre külső ellenállást szerelj.

A NYÁK-tervvel befagyasztott net→GPIO térkép:

| Interfész | GPIO |
|---|---|
| AZ STEP / DIR | 26 / 27 |
| EL STEP / DIR | 14 / 13 |
| közös ENABLE | 25, aktív LOW |
| E-stop NC | 34 |
| AZ minimum/maximum NC | 35 / 36 |
| EL minimum/maximum NC | 39 / 32 |
| GNSS RX / ESP32 TX | 16 / 17 |
| AS5600 AZ SDA / SCL | 21 / 22 |
| AS5600 EL SDA / SCL | 18 / 19 |

A GPIO16/17 kizárólag WROOM-32E-hez jóváhagyott, ahol rendelkezésre áll; WROVER/PSRAM modult ne használj. Külső 10 kΩ felhúzás kell az ENABLE-re és mind az öt NC-bemenetre. Egyezményes meghajtó: **Watterott TMC2209 SilentStepStick standalone módban**, MS1=MS2=3,3 V a modul hivatkozása szerint 1/16-hoz; motor UART/DIAG nincs bekötve/vezérelve e firmware-ből. Behelyezés előtt ellenőrizd a revíziót és fejlécirányt a panel- és gyártói dokumentációval.

* Tengelyenként külső STEP/DIR-meghajtó, NEMA14-hez beállított áram és megfelelő táp. A motort ne az ESP32-ről tápláld. Fizikailag állítsd be a **16 mikrolépést**, 200 lépés/fordulat motort és 25:1 bolygóművet: **80 000 mikrolépés/kimeneti fordulat**, 222,222… mikrolépés/fok. A jelenlegi könnyű alapkivitel a bolygóművet **két, vásárolt 20:100 fogú GT2 fokozatra** cseréli: 5×5=25:1, a parancs/fordulat érték változatlan. A bolygómű korábbi opcionális változat, nem az alap hajtás. Ellenőrizd a fogszámot, mikrolépést és szerelt áttételt; nyomtatott GT2 profilokat és rajz nélküli tárcsákat ne feltételezz.
* Közös ENABLE aktív LOW, **külső felhúzással, amely reset közben is OFF állapotban tartja**. Más meghajtó-polaritás esetén előbb alakítsd át az áramkört/kódot.
* Az E-stop **normál esetben földre zárt**; szakadt kábel/HIGH hibát vált ki. A driver tápját/engedélyezését firmware-től függetlenül fizikailag meg kell szakítania. A bemenet csak ezt az áramkört figyeli.
* Négy fizikai **NC–GND** végállás: AZ minimum/maximum és EL minimum/maximum. HIGH/nyitott állapot elért végállást vagy vezetékszakadást jelent. Homing közbeni nyitás nem különbözteti meg a hibás érintkezőt a valódi határtól: az eljárás felengedést és új megközelítést igényel, de továbbra is fizikai ellenőrzés szükséges. Végleges telepítéshez használj felügyelt hardvert.
* AZ minimum **−180°**, maximum **+180°** mechanikai; EL minimum 0°, maximum 90°. A tényleges végállásokat, fizikai tartalékot és referenciákat sablonokkal állítsd be; a szoftver nem tudja, hová kerültek.
* UART GNSS NMEA 9600, konfigurálható; 3,3 V-os szint, RX/TX kiosztással.
* Lehetőleg két AS5600 legyen **a kimeneten**, ne a motoron a reduktor előtt. I2C-cím 0x36 külön buszon, 3,3 V-os felhúzások, `encoders=true`, konfigurált tűk és enkóder-polaritás. Jelenlét-/tartományellenőrzés; referencia homingkor, három, >3° eltérést jelző olvasás/vesztés után hiba; 100 ms mintavétel, 5 ms I2C-időtúllépés. Szögfelbontás ≈0,088°, backlash/merevség mérése nélkül. Az abszolút enkóder nem különböztet meg teljes fordulatokat; a végállások és vezetékezés továbbra is szükségesek.

AP-jelszó legyen legalább 12 és legfeljebb 63 karakter, token véletlen, legalább 24 karakter és egyedi (lehetőleg 32 véletlen bájt kódolva). Üres érték esetén AP/API letiltott. Valódi titkot tartalmazó firmware-t/konfigurációt ne publikálj. Opcionális: STA SSID/jelszó és **aktuális CA PEM** a szolgáltatókhoz `tlsRoots` mezőben; kitalált CA nincs, `setInsecure()` nem használható. A STA csak kimenő hozzáférés: a 80-as portot ne tedd ki nem megbízható hálózatra. A helyi HTTP védett Wi-Fi-n tokent használ, helyi TLS nincs; hozzáférést korlátozd engedélyezett kezelőkre.

## Folyamat és biztonság

1. Indítás mindig **DISARMED, ENABLE OFF**. A homing nem perzisztál.
2. Ellenőrizd az E-stopot/vezetékezést, parancsolj HOME-ot. AZ a minimum felé keres, 700 mikrolépésnyit visszahúzódik a felengedésig, majd újra megközelíti; ezután ugyanígy EL. Debounce 30 ms, **tengelyenként 240 s** időtúllépés; hiba, ha a tervezett út nem talál/felenged érintkezőt. A minimum helyett ne használj másik végállást.
3. Mozgasd ismert helyzetbe EL=0-val. Szintezd az alapot szintezővel/dőlésmérővel; megbízható referenciával határozd meg az aktuális **valódi** irányt. `/api/calibrate` számítja: offset=aktuális irány−mechanikai AZ. Az álló GNSS **nem ad headinget**, és szintezést sem.
4. UTC-hez <3 s-os GNSS-üzenetek kellenek, érvényes 2024–2099 évvel. Automatikus helyhez <5 s-os fix és magasság szükséges; a perzisztált kézi hely fix helyet adhat, **a GNSS UTC-t nem helyettesíti**. Mozgás közbeni >2 s UTC-ugrás hibát okoz.
5. Importálj TLE-t, válassz műholdat és kérdezd le a passzokat. Elutasítja a checksumhibát, eltérő NORAD-számot, érvénytelen orbitális mezőket és nem támogatott formátumot. Csak numerikus NORAD használható (Alpha-5/OMM nincs), maximum **100 műhold/48 kB**.
6. Mozgasd az AZ/EL-t a várt érték közelébe; a TRACK csak horizont fölött indulhat, és kalibrálást, homingot, UTC-t, helyet és friss TLE-t igényel. >15° megszerzési/eltérési hiba leállít, hogy elkerülje a váratlan keresőforgást.
7. A STOP megszakítja a mozgást és letiltja a meghajtókat, de nem törli a hibát. Homing alatti STOP érvényteleníti a referenciát. Kemény hiba érvényteleníti a homingot/kalibrálást; törléshez (CLEAR) zárt E-stop, HOME és új kalibrálás kell. Áram nélküli kézi mozgatás vagy szerelésváltozás után ismét CLEAR/HOME/kalibrálás szükséges.

Az AZ mechanikai koordináta ±180°-ra korlátozott; valódi irányt kalibrációs offsettel alakít át. Korlátlan unwrap nincs. A kábelvágáson átmenő >180° ugrás hibát/újrapozicionálást vált ki. EL 0..90°. Maximális sebesség 500 mikrolépés/s (=2,25°/s), gyorsulás 300 mikrolépés/s². Külön motorfeladat, iterációnként legfeljebb egy impulzus, visszanyerő sorozat nélkül; mozgáskor dt>20 ms hibát vált ki. Impulzus-/irányjelhez 3 µs tartalék kell.

A feladat-előrejelző ciklusonként négy pozíciót dolgoz fel, nem blokkol teljes passzra. Mozgás alatt passzlekérdezés/-indítás elutasított; a függő számítás szünetel. TLE-letöltés is elutasított aktív motorok mellett. A fizikai felügyelet a HTTP-szervertől független feladatban fut, a kötelező fizikai tápmegszakítás mellett; a legrosszabb hardveres válaszidőt még mérni kell. Nem garantál elegendő sebességet zenit közelében: próbapadon teszteld a követést/backlash-t; mechanikailag lehetetlen passzok előzetes, tanúsított tervezése nincs. A TRACK EL≥89°-ot elutasít, és e zónába lépéskor hibát vált ki. Az 1 s-mal előre propagált SGP4 ellenőrzi az AZ/EL sebességet: 2,25°/s fölött hiba/leállítás; ez nem garantál gyorsulási tartalékot, és nem váltja ki a fizikai próbát.

A nyugalomban letiltott motorok elveszíthetik pozíciójukat; enkóderrel ez felügyelhető, nélküle minden elmozdulás után a kezelőnek újra home-olnia kell. A könnyű szíjas kivitel visszahajtható: STOP, hiba, reset és nyugalom esetén a meghajtó letilt, és **elektromos nyomatékkal nem tartja meg az antennát**. Egyensúlyozd ki a terhet, és használj független mechanikai féket/rögzítést a tápvesztéskor bekövetkező zuhanás vagy veszélyes elfordulás ellen. Az AS5600 eltérést érzékelhet, de terhet nem tart meg. A ≤3 kg célból kimarad a rádió/állvány, a tápellátás viszont beleszámít; ez nem mért tömeg és nem terhelési engedély.

## Helyi HTTP API

Minden `/api/*` útvonal, GET is, `X-Control-Token: <beállított token>` fejlécet igényel. Nincs CORS, GET-oldali állapotmódosítás, wildcard vagy cookie; a token csak az oldal memóriájában van, localStorage-ban nem. POST `Content-Type: application/json`; a válasz JSON. 200 siker, 202 elindított parancs, 400 hibás séma, 401 tokenhiba, 409 előfeltétel, 502 letöltési hiba. `{"message":"..."}` vagy `{"error":"..."}`. A webes leállítás nem helyettesíti a fizikai E-stopot.

| Módszer/útvonal | Törzs / eredmény |
|---|---|
| GET `/api/status` | mode/fault, hardwareConfigured, enabled, homed, calibrated, level, utc/utcValid, siteValid/manualSite/lat/lon/alt, northOffset, azMechanical/el, skyAz/skyEl/rangeKm/rangeRateKmS, doppler145Hz/doppler435Hz, trackingBlocker, selected, download, staConnected, encoders, pttCat=false |
| POST `/api/site` | `{"manual":true,"lat":40.4,"lon":-3.7,"alt":650}`; minden kötelező; false visszaáll GNSS-re. Álló helyzet szükséges; érvényteleníti az orbitális számítást/passzlistát |
| POST `/api/home` | `{}`; fizikai, aszinkron homing, csak mechanikai pozíciót kalibrál |
| POST `/api/move` | `{"az":0,"el":0}`; AZ **mechanikai**, nem valódi irány; szereléshez nem kell kalibrálás/UTC |
| POST `/api/stop` | `{}`; letilt, FAULT-ot nem töröl |
| POST `/api/clear` | `{}`; zárt E-stop mellett törli a hibát, homingot/kalibrálást érvénytelenít |
| POST `/api/calibrate` | `{"trueAz":0,"levelConfirmed":true}`; aktuális valódi irány, EL=0 és nyugalom kötelező |
| GET `/api/tle` | `{"satellites":[{"id":0,"name":"...","epoch":unix,"fresh":true,"line1":"...","line2":"..."}]}` |
| POST `/api/tle` | `{"text":"név\n1 ...\n2 ...\n"}`; teljes, validált, perzisztens csere, részleges keverés nélkül |
| POST `/api/select` | `{"id":0}`; az aktuális lista indexe, nem NORAD; importkor visszaáll |
| GET `/api/passes` | Számítást indít/lekérdez: `calculating`, `stepSeconds=10`, `passes:[{aos,los,peak,maxEl,partial}]`; idők Unix UTC. 24 órás ablak, 0° geometriai horizont, 10 s időfelbontás; nagyon rövid passz kimaradhat. 60 s cache; partial jelzi a csonkolt ablakot |
| POST `/api/track` | `{}`; a jelenleg kiválasztott követése (jövőbeli ütemezés nincs); horizont alá kerüléskor befejeződik |
| POST `/api/update` | `{"provider":"celestrak"}` vagy `amsat` / `pe0sat`; nyugalom, STA-kapcsolat, GNSS UTC és CA PEM kell |

Pontos szolgáltatók, tetszőleges URL nincs:

* CelesTrak amateur: `https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle`
* AMSAT: `https://www.amsat.org/tle/current/dailytle.txt`
* PE0SAT: `https://tle.pe0sat.nl/kepler/mykepler.txt`

A HTTPS ellenőrzi a hostnevet, tanúsítványláncot és GNSS-időt. Átirányítás kikapcsolva; pozitív, ≤48 kB `Content-Length` szükséges (chunked elutasítva), kapcsolódás 5 s, olvasás 8 s. Formátumváltozás, TLS, DNS, lista-limit vagy válaszhiba **kifejezett**; ha a szolgáltató túllépi a 100 műholdat, tartsd meg, illetve kézzel importálj részhalmazt. Nem állítjuk, hogy ESP32-vel mindhárom aktuális választ letöltöttük. Az izolált AP nem ér el internetet.

A LittleFS validálás után `/tle.new` fájlt ír és atomikusan `/tle.txt`-re nevezi át; hiba esetén a korábbi RAM-/fájlrendszer-cache megmarad. Csatolási hiba esetén nem formáz automatikusan. A hely/offset NVS-ben van; szint-/homing-/kalibráció-megerősítés **nem** áll vissza. A régi/jövőbeli TLE tiltja a követést (>14 napos vagy >1 nap jövőbeli epoch), és a friss letöltés sem módosítja az orbitális epochot.

## Valódi antenna előtt még szükséges próbák

Leválasztott motorokkal: ellenőrizd az ENABLE polaritását, az E-stop fizikai működését reset és processzorlefagyás esetén, a kábelnyitást, minden végállást és időtúllépést; az irányt, mikrolépést/áttételt és AS5600-szerelést. Mérd a legnagyobb késést HTTPS/SGP4/Wi-Fi mellett. Teszteld a GNSS-vesztést, UTC-ugrást, sérült/régi TLE-t, íráshibát és tápmegszakadást, mágnes/buszvesztést, elakadást, backlash-t, kábelhatárt és zenitet. Ezután terhelőpad és független szögreferencia; csak ezután felügyelt, kis teljesítményű RF-próba. Nincs perzisztens autohoming, kettős GNSS-heading, IMU, dinamikus szélprofil, automatikus passzsor, teljes duplex vezérlés vagy adásautomatizálás.
