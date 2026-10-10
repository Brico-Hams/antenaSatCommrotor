# Prototípus-webflasher (előkészítve, nincs közzétéve)

**A PCB/hardver nincs kiadva. Flash-elés közben ne csatlakoztasson motort.**
A CI a szoftvert és flash-adatokat ellenőrzi; a paneleket, kábelezést,
mozgást, vészleállítót, homingot, kalibrálást, pályapontosságot vagy RF-et
nem validálja. A Git előkészítése nem közzététel: itt nem történt push,
Pages-engedélyezés vagy GitHub Actions-futtatás.

## Mit fordít le

A `.github/workflows/webflash.yml` a mérnöki workflow-tól elkülönülten fut.
`v*` tag, `main`-re push vagy `workflow_dispatch` a valódi
`firmware/platformio.ini` **esp32** környezetét fordítja. Az érintett PR-ek
telepítési jogosultság, titok és `pull_request_target` nélkül építik/validálják
az artefaktumokat.

Rögzítések: PlatformIO Core 6.1.18; espressif32 6.10.0;
Arduino-ESP32 3.20017.241212 (Arduino 2.0.17); Xtensa 8.4.0+2021r2-patch5;
ArduinoJson 6.21.5; TinyGPSPlus 1.1.0; Sgp4-Library commit
`7c82d31f9d9a286acde5ef55da8308fc93d2ba96`. A NimBLE-Arduino 1.4.3
csak helyben opcionálisan konfigurált BLE-hez fordul. A LittleFS-felület
tartalmazza a fizikai kalibrációs varázslót. A BLE a vezérlő handlereit és
privátan konfigurált hitelesítést használja; közzététel/flash nem kapcsolja
be. HTTPS TLE-letöltés BLE-n 409-et ad; a TLE-t a kliens tölti le, majd a
vezérlő/alkalmazás dokumentált protokollján továbbítja. A nagy TLE-átvitel
`/api/tle/begin`, `/api/tle/chunk`, `/api/tle/commit` útvonalat, SHA256-
ellenőrzést, atomikus cache-cserét és lapozott katalógust használ. A telefon
tölti le az adatot, az SGP4-propagáció a rotoron marad. A fordítás nem
validálja a heapet, rádiós együttélést vagy fizikai kalibrálást.
CI ezenfelül `PLATFORMIO_PLATFORM_PACKAGES` segítségével rögzíti a
tool-esptoolpy 1.40501.0-t (esptool 4.5.1) és tool-mklittlefs 1.203.210628-at
(2.3); a vezérlő framework/toolchain rögzítése nem változik.
Node 22 és Python 3.11 rögzített kompatibilis majorverzió. Az Actions is
major szerint van rögzítve.

ESP Web Tools **10.1.0**, az npm metaadata és a csomag LICENSE fájlja alapján
ellenőrzött **Apache-2.0** licenccel. A `webflash/package-lock.json` az
integritással együtt a tranzitív függőségeket is rögzíti. A CI
`npm ci --ignore-scripts` parancsot futtat, a **teljes `dist/` könyvtárat**
a `vendor/esp-web-tools/` alá másolja könyvtárszerkezetének megtartásával,
és megőrzi a chunkokat/dinamikus importokat/licenceket. Nincs
`unpkg latest`, távoli CDN vagy csendes fallback. Böngészőbelépési pont:
**`dist/web/install-button.js`**, nem a kiterjesztés nélküli importokat
tartalmazó `dist/install-button.js` modul. A validátor a böngészős
disztribúció minden chunkjának relatív importjait ellenőrzi.
Az Arduino 2.0.17/ESP-IDF v4.4.7 upstream forrásokat és licencszövegeket
nyilvános tag-ekből tölti le, rögzített SHA256-hash alapján validálja;
az azonos tag alatti csendes változás nem elfogadható.
Az oldal kezdetben npm/GitHub függőséget igényel az eszközök előállításához/
kiszolgálásához; a forrásfájlokról önmagukban ne állítsa, hogy offline
flasherként működnek.

## Flash-adatok: találomra választott offset tilos

A `scripts/build-webflash-proof.py` PlatformIO utáni extra-script.
`webflash-proof` célja lefordítja a firmware-t, és rögzíti a valódi
`$UPLOADCMD`, `FLASH_EXTRA_IMAGES`, `ESP32_APP_OFFSET`, kártya/MCU és
csomagadatokat. **Nem futtat uploadot, nem nyit soros portot és nem töröl
eszközt.** A `scripts/build-webflash.cjs` ellenőrzi a receptet és a lefordított
binárisokat:

| Fájl | Decimális offset (hex) |
|---|---:|
| `bootloader.bin` | 4096 (0x1000) |
| `partitions.bin` | 32768 (0x8000) |
| `boot_app0.bin` | 57344 (0xe000) |
| `firmware.bin` | 65536 (0x10000) |

ESP Web Tools manifest: `chipFamily: "ESP32"` (klasszikus WROOM, **nem C3**).
Nem készül kitalált bináris vagy 0-tól feltöltött, NVS-t megsemmisíthető
kombinált kép. Négy külön flash-rész használatos. Ha az adott firmware-
revízió továbbra is LittleFS-ből szolgálja ki az `/index.html` oldalt, a CI
`buildfs`-t futtat és ötödik `littlefs.bin` részt ad hozzá, a
**`partitions.bin` fájlból** vett offsettel/mérettel (jelenlegi default:
0x290000/0x160000). Ez lecseréli a felületet és a tárolt TLE-t; előbb
készítsen másolatot. Ha a vezérlő a programflash-ba építi a felületet,
csak négy rész kell: ne töltsön fel megszokásból fájlrendszerképet.
A generátor a tényleges forráskódot ellenőrzi.

Validáció: ESP32-headerek, részek darabszáma, valódi parancs-offsetek,
biztonságos relatív útvonalak, minden bináris SHA256-ja/hossza,
szektorfedések, alkalmazás-/fájlrendszer-partíció mérete és valós NVS-
partíciós tábla. A `SHA256SUMS`, manifest és teljes commit azonosítja a
letöltést. A `build-info.json` a releváns forrásfa SHA256-át is összeköti:
minden `firmware/src`, `firmware/include`, web és `platformio.ini` fájl
egyedi hashét. A generátor összeveti a PlatformIO által rögzített fákkal;
ha a próba óta fejléc, UI vagy konfiguráció változott, újrafordítás kell.
A feloldott csomagverziók és npm-lock hash azonosítják a függőségeket.
A binárishash a buildútvonal/toolchain/metaadatok miatt eltérhet: a valódi
artefaktum hashét nem helyettesítjük másik build értékével. Első commit nélküli
vagy nem commitolt helyi build `local-prototype+uncommitted` címkét kap;
`sourceSha` értéke null, nem kitalált SHA. A `tests/webflash.test.cjs`
szintetikus próbája nem példa-firmware: csak ignorált tesztkönyvtárban van.
A CI a valódi bundle-t is validálja.

## Hitelesítő adatok és frissítés

A nyilvános build `carrierVerified=false` értéket és üres
`apPassword`, `apiToken`, `staSsid`, `staPassword` mezőket követel a
`board_config.h` fájlban. Ha `firmware/include/secrets.h` vagy
`firmware/secrets.ini` létezik, a build még fordítás ELŐTT meghiúsul.
Nyilvánosan terjesztett firmware-be Wi-Fi-jelszót/tokent ne illesszen
GitHub Secrets segítségével. Üres értékű, szűz NVS esetén a vezérlő
USB-s helyi provisioningig kikapcsolja az AP/API-t, újrafordítás nélkül.
Kompatibilis korábbi NVS esetén megőrzi a hitelesítő adatokat és a hordozó
ellenőrzött állapotát; induláskor mindig DISARMED, a homing/kalibrálás
nem áll vissza.

Provisioning **helyben, privát módon** a `docs/CONTROL.md` szerint;
konfigurációt ne töltsön Pages-re, Gitbe vagy nyilvános artefaktumba.
Telepítés után zárja be az ESP Web Tools portját, majd nyisson helyi,
115200 baud-os USB-konzolt. A `{"cmd":"setup"}` SETUP-ba lép,
kikapcsolja a Wi-Fi-t/motorokat és érvényteleníti a kalibrálást;
`cmd config` elmenti az SSID-t, saját 12–63 karakteres AP-jelszót és
saját 24–128 ASCII-karakteres tokent NVS-be (pontos mezők/validálás:
`CONTROL.md`); a `{"cmd":"reboot"}` alkalmazza a változtatást, DISARMED
állapotban indul. Hitelesítő adatot tartalmazó terminált/képernyőképet ne
osszon meg. `cmd carrier` verified=true értékkel csak a panel fizikai
ellenőrzése után küldhető. BLE csak kifejezett helyi aktiválás és saját
passkey után engedélyezhető. A flasher nem talál ki protokollt, nem
engedélyez automatikusan Improv Wi-Fi-t, és nem tesz közzé tokent.
Az NVS nincs titkosítva: fizikai/USB-hozzáféréssel kiolvasható vagy
módosítható a konfiguráció; az ott tárolt hitelesítő adat nem véd a
fizikai kinyeréstől. A JSON-sorok maximuma 768 bájt. A nyilvános képen
`tlsRoots` üres, ezért a HTTPS-frissítés elutasított; AP-konfiguráció után
kézi TLE-feltöltés továbbra is lehetséges. Ne állítsa, hogy a jelenlegi
nyilvános bináris megbízhatósági gyökerek beállítása nélkül képes HTTPS
TLE-letöltésre.

A normál írás NVS-t NEM érint: alapértelmezés szerint 0x9000–0xdfff.
A manifest törlési megerősítést követel (`new_install_prompt_erase: true`);
az **Erase device** jelölő alapállapotban nincs bejelölve.
Az ESP Web Tools 10.1.0 tényleges kódjának ellenőrzése szerint a **false**
Improv Serial nélküli eszközön automatikus törlést okoz; ezért NVS
megőrzéséhez NE használjon false értéket. **Ne jelölje be az „Erase device”
opciót**, kivéve, ha teljes törlés a szándék, készült mentés, és a
párbeszédben ezt kifejezetten megerősítette. NVS csak azonos partíciós
tábla esetén tartható meg; layout-migrációhoz áttekintett stratégia/mentés
szükséges. A homingot/kalibrálást soha ne állítsa vissza automatikus
mozgásengedélyezésként.

## Pages engedélyezése – csak a tulajdonos döntésére

1. Hozza létre a távoli tárolót/URL-t a kiválasztott fiókkal. Ezek a fájlok
   nem találnak ki URL-t; a GitHub deployment által ténylegesen megadott
   URL-t kell lekérni.
2. GitHubon: **Settings → Pages → Source: GitHub Actions**.
3. Hozzon létre `webflash-pages` környezetet, állítson be kézi jóváhagyású
   **Required reviewers** szabályt, korlátozza az ágakat `main`-re, és ha
   lehetséges, tiltsa a megkerülést. Ellenőrizze, hogy a repo terve/
   láthatósága támogatja a védelmet.
4. Csak a prototípus áttekintése és a jóváhagyók beállítása után állítsa be
   a repository `WEBFLASH_PAGES_APPROVED=prototype-only` változóját.
   Enélkül nem fut a deploy. Ne állítsa be, ha nem követelhető meg reviewer:
   inkább kézzel töltse le az artefaktumot, közzététel nélkül.
5. Jóváhagyás esetén push `main`-re, vagy `main` ágról dispatch
   `deploy_pages=true` paraméterrel. A tag-ek verziózott artefaktumot
   készítenek, de nem deployolnak Pages-re; PR soha. Más ágról indított
   dispatch sem deployol.

Buildhez `contents: read`; `pages: write` és `id-token: write` kizárólag a
feltételes, védett környezetű deployhoz kell. PAT és titok bevitele nem
szükséges. A deployment jóváhagyása nem teszi kiadott termékké a hardvert:
a PROTOTÍPUS figyelmeztetések az oldalon maradnak.
Az Actions artefaktum neve `webflash-<commit SHA>`; az oldal, valódi binárisok,
hash-ek, metaadat, licenc-közlemények és relinkelhető forrás/objektumok
találhatók benne. A megfelelőségi/upstream-fájlok nagyok; flasheléskor nem
töltődnek le, csak a manifest részei. Terjesztéskor őrizze meg őket.
A workflow nem hoz létre GitHub Release-t és nem mozgat taget.

## Böngésző, jogosultságok és adatvédelem

A Pages-nek HTTPS-en kell kiszolgálnia. A Web Serial biztonságos
környezetben **asztali Chrome vagy Edge** böngészőt követel; Firefox,
Safari és mobil nem támogatott alternatíva. Nyissa meg közvetlenül, ne
iframe-ben; vállalati házirend blokkolhatja az USB-t. Portengedély csak
a Csatlakozás gomb megnyomásakor, opcionálisan jelenik meg.
Elutasítás/megszakítás nem flashel semmit: próbálja újra vagy használja a
helyi PlatformIO-t. Címke/port alapján válassza ki az **ESP32-DevKitC V4 38-pin WROOM-32E**
modult; megjelenés alapján ne következtessen a lábkiosztásra. A motorok és
aktuátorok tápját válassza le; csak USB-t csatlakoztasson.

A harmadik féltől származó könyvtárat Pages szolgálja ki, de a soros port
minden adata helyben marad. A modul script `crossorigin="anonymous"`
beállítású; az eszközök azonos eredetűek, nincs szükség CDN-re és CORS-on
át nem kap harmadik fél hozzáférést a porthoz. Privát kód/firmware,
jelszó/token vagy saját telemetria nem kerül feltöltésre. A GitHub csak
nyilvános eszközök szokásos webes kéréseit látja. A függőségekhez CI-ben
npm/upstream tárolók érhetők el; a felhasználó privát kódja nem kerül
flashelési szolgáltatásba.

## Helyi validálás (panel nélkül)

A projekt gyökeréből, Node 22/Python 3.11/PlatformIO rendelkezésre állásakor:

```powershell
Push-Location webflash
npm ci --ignore-scripts --registry=https://registry.npmjs.org
Pop-Location
$env:PLATFORMIO_EXTRA_SCRIPTS = 'post:../scripts/build-webflash-proof.py'
python -m platformio run -d firmware -e esp32
python -m platformio run -d firmware -e esp32 -t webflash-proof
python -m platformio run -d firmware -e esp32 -t buildfs
node scripts\build-webflash.cjs
node --test tests\webflash.test.cjs
node scripts\build-webflash.cjs --validate build\webflash
```

Ha a generátor hiányzó upstream közleményt/licencet jelez, csomagolás előtt
a workflow „Preserve upstream source and license” lépését is futtassa.
A binárisok, eszközök és kimenetek ignorált `build/` és `.pio/` könyvtárba
kerülnek; a `webflash/node_modules` szintén ignorált. Binárist ne tegyen Gitbe.
Mindig a `webflash` könyvtárból telepítsen: ne futtasson csomag nélkül,
gyökérből `--prefix`-szel `npm install`-t, és ne adjon hozzá `file:..`
függőséget vagy helyi linket. A generátor elutasítja a nem registry-s
függőségeket, valamint az értesítések bejárásakor a junction/symlink útvonalat,
hogy elkerülje a projekt/Android SDK véletlen rekurzív bejárását.
Kézi másolathoz a **`build\webflash`** könyvtárat szolgálja ki HTTPS-en
vagy localhoston: ne nyissa meg `file:` protokollal a
`webflash/index.html`-t, és ne feltételezze, hogy az eszközök ott vannak.
Fordítási vagy ellenőrzési hiba megállítja a generálást/deploymentet.

## Licencek és oktatás

Szerzők: **Anatol EA5KAO**, **Diego EA5JEF**, **Pedro Roca Molina**;
köszönet a [Bricohams](https://bricohams.org/) szervezetnek.
Lásd `AUTHORS.md`, `ACKNOWLEDGEMENTS.md`, `DISCLAIMER.md`, `NOTICE.md`.
A Bricohamsra gyermekek és fiatalok tudományos ismeretterjesztő szervezeteként
hivatkozunk. A jelenlegi szerzőség nem helyettesíti a könyvtárak vagy
felhasznált források szerzőit; a hivatkozás nem jelent együttműködést,
szponzorációt vagy jóváhagyást. Az eredeti szoftver MIT; az SGP4 telepített
könyvtár MIT-licence ellenőrzött; az ESP Web Tools/NimBLE-Arduino Apache-2.0;
ArduinoJson MIT; TinyGPSPlus/Arduino-ESP32 LGPL-2.1, az SDK saját eredeti
közleményeivel. Ne állítsa, hogy a teljes bináris kizárólag MIT-licencű.
A bundle megőrzi a licencszövegeket, pontos függőségforrásokat, relinkelhető
objektumokat és upstream linkeket/verziókat; újraterjesztéskor ezeket is
őrizze meg. Kereskedelmi forgalomba hozatal előtt vizsgálja felül az SDK/
komponensek kötelezettségeit. A hardver külön, CERN-OHL-S-2.0 licencű.

Kiskorúak oktatási célú használatához felnőtt felügyelete szükséges;
gyermekek ne végezzenek veszélyes szerelést, és engedély/licenc nélkül
soha ne használjanak RF-adást. A CI egyik próbája sem bizonyít fizikai
elfogadást, elektromos vagy RF-kompatibilitást.
