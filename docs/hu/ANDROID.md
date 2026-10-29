# Natív Android-alkalmazás: helyi BLE-vezérlés

Alkalmazáscsomag: `org.bricohams.portablesatstation`; natív Kotlin;
minimum Android 8/API 26, cél-/fordítási SDK 35. Alapértelmezett
spanyol erőforrások, az eszköz nyelvéhez igazodó angol fordítással.
Nincs React, WebView, telefonon végzett pályaszámítás, felhőalapú
vezérlőszolgáltatás, analitika, telefonos geolokáció, CAT vagy PTT.
**INTERNET-kapcsolat kizárólag az alább rögzített három szolgáltatótól,
HTTPS-en letöltött nyilvános TLE-khez engedélyezett**; a vezérlés/adatátvitel
továbbra is helyi BLE-n zajlik.

**Terepen nem validált prototípus.** A fordítás nem validálja a
kábelezést, mechanikát, RF-et, funkcionális biztonságot vagy a rotor
pontosságát. Használjon fizikai vészleállítót, védett tápellátást,
ellenőrzött határolókat és felnőtt felügyeletet.

Jelenlegi szerzők: **Anatol EA5KAO, Diego EA5JEF és Pedro Roca Molina**.
A [Bricohams](https://bricohams.org) oktatási ismeretterjesztő hivatkozás,
nem tanúsítás és nem jelent harmadik féltől származó támogatást.
Lásd még: [szerzők](../../AUTHORS.md) és [nyilatkozat](../../DISCLAIMER.md).

## Fordítás és tesztelés

Windows alatt, az `android` könyvtárból:

```powershell
$env:JAVA_HOME = 'a\jdk-17\útvonala'
$env:ANDROID_HOME = 'az\android-sdk\útvonala'
$env:ANDROID_USER_HOME = Join-Path $PWD '.tools\android-user'
.\gradlew.bat --no-daemon testDebugUnitTest lintDebug assembleDebug
Get-FileHash .\app\build\outputs\apk\debug\app-debug.apk -Algorithm SHA256
```

Linux/macOS: `chmod +x gradlew`, majd
`./gradlew --no-daemon testDebugUnitTest lintDebug assembleDebug`.

Rögzített eszközök: **AGP 8.7.3 / Kotlin 2.0.21 / Gradle 8.9 / JDK 17 /
platforms;android-35 / build-tools;35.0.0**.
A Gradle-disztribúció SHA-256-ellenőrzése:
`d725d707bfabd4dfdc958c624003b3c80accc03f7037b5122c4b1d0ef15cecab`.
A `gradle-wrapper.jar` a hivatalos Gradle 8.9 bináris, SHA-256:
`498495120a03b9a6ab5d155f5de3c8f0d986a449153702fb80fc80e134484f17`.
Ellenőrzési források: [disztribúció](https://services.gradle.org/distributions/gradle-8.9-bin.zip.sha256),
[wrapper](https://downloads.gradle.org/distributions/gradle-8.9-wrapper.jar.sha256).

Az elkülönített helyi eszközök az ignorált `android\.tools` könyvtárba
kerültek: Microsoft JDK 17.0.16+8 az `aka.ms/download-jdk` címről,
ZIP SHA-256 `53f0c9ec64811a9ab968747076653e5500115db7230d244e4ec53577ca5ec8fc`;
Android parancssori eszközök 19.0,
`commandlinetools-win-13114758_latest.zip`, SHA-256
`98b565cb657b012dae6794cefc0f66ae1efb4690c699b78a614b4a6a3505b003`.
SHA-1 értékét (`54a582f3bf73e04253602f2d1c80bd5868aac115`) összevetettük a
`https://dl.google.com/android/repository/repository2-1.xml` tartalmával.
A globális Java/SDK nem módosul, és a privát kódot nem töltjük fel fordításra.
Az `ANDROID_USER_HOME` az `android\.tools\android-user` alatt tartja a
beállításokat és az AGP által generált debugkulcsot; a debugkulcs nincs
verziókezelésben, és nem tüntetjük fel szerzői kiadási kulcsként/
tanúsítványként.

A `.github/workflows/android.yml` JVM-teszteket, lintet és buildet futtat,
majd a **debug** APK-t és hashét letölthető GitHub-artefaktumként közzéteszi.
A debug APK a fejlesztői eszközök által generált debugkulccsal van aláírva;
**nem hivatalos terjesztési aláírás**, és nincs automatikus áruházi
közzététel. A release-terjesztés a szerző valódi privát kulcsát igényli a
tárolón kívüli, külön védett folyamatban.

### Helyi bizonyíték (2026. október 10.)

`testDebugUnitTest lintDebug assembleDebug`: **BUILD SUCCESSFUL**.
**29 JVM-teszt, 0 hiba/kivétel; a lint eredménye: „No issues found”.**
A valós vezérlőkóddal egyeztetett UUID/verzió/korlát ellenőrzését, pontos
MTU 23/185 keretezést, UTF-8-at, méret-/sorrendkorlátot, nem numerikus/
nem véges bemenetet, sikertelen hitelesítést, hibás állapotot,
inkompatibilis verziót, hívássorrendet, lapozott katalógust,
TLE-checksumot/epochot, 100-nál több elemű, kifejezetten kiválasztott
szolgáltatói részhalmazt, atomikus cache-t, HTTPS-allowlistet
átirányítás nélkül, valamint pontos offsetes begin/chunk/commit/abort
folyamatot is tartalmazza. Alkalmazás: **0.3.0-prototype**, versionCode **3**.

APK: `android\app\build\outputs\apk\debug\app-debug.apk`.
SHA-256:
`47997a78abd87b3aa4e26a33106f9b122a817121dd02c2abc7d6b72717ca399b`.
Az `apksigner verify` lefutott; az `aapt dump permissions` BLE-t, Android
30-ig helyengedélyt és a HTTPS-letöltésekhez INTERNET-jogot mutat. Ez debug,
nem release-terjesztésre aláírt APK. A hash nem tanúsít hardvert vagy BLE-t.
Jelentések: `android\app\build\reports\tests\testDebugUnitTest` és
`android\app\build\reports\lint-results-debug.html`.

A JDK 17-es helyi futtatókörnyezetben az alkalmazás **valódi HTTPS-letöltőjét
és parserét** futtattuk az AMSAT végponttal: HTTP 200, **97 műhold,
14434 bájt**, SHA-256
`ec291294636090d712fc901e4a7e3fa15bbeb8366fb771d7aad131b5c8db1ce9`.
Ez nem tesztben szimulált válasz; privát adatot nem töltöttünk fel.
A CelesTrak és PE0SAT ezen a hálózaton túllépte a csatlakozási időkorlátot:
nem állítjuk, hogy letöltött, és nem helyettesítettük TLS nélküli vagy más
URL-lel. A szolgáltatói hibák megtartják a cache-t. Ez a próba **nem**
validálja a TLS-t/rádiót valódi Android-eszközön vagy fizikai BLE-átvitelt.
A szolgáltatói adatok naponta változnak.

## Használat és biztonság

1. Fizikailag állítsa be a rotor BLE-jét a helyi passkey-jel és API-tokennel.
2. Írja a tokent a jelszómezőbe. A „Mentés” kifejezett művelet; az Android
   Keystore nem exportálható AES-GCM-kulcsot tárol, a SharedPreferences
   pedig kizárólag az IV-t és titkosított szöveget. Az alkalmazás backupja tiltott.
3. Olvassa el az engedélyek magyarázatát, majd keressen. Android 12+-on
   BLUETOOTH_SCAN/CONNECT kell; régebbi verziók BLE-hez helyengedélyt
   igényelnek, de az app nem hív hely-API-t, és nem szerzi meg/tölti fel a
   földrajzi helyet.
4. Kifejezetten válassza ki a fizikai eszközt. Az Android megjeleníti a
   párosítási párbeszédet. A bonding és a tokenes hitelesítés külön követelmény.
5. A csatlakozás és hitelesítés soha nem indít homingot, mozgást vagy
   motorengedélyezést.
6. Motorhasználat előtt kérdezze le az állapotot. Rehome/indítás ismételt
   fizikai kalibrálást igényel: műszeres szintezés, EL=0 kimenet és mért
   valódi irány (földrajzi észak/nap vagy deklinációval korrigált iránytű,
   fémtől távol). Az álló GNSS nem mér irányt. A beállítási útmutató mentett
   előrehaladása **nem** kalibráció; a firmware hitelesített állapota mérvadó.

A keresés 15 másodperc után és a képernyő elhagyásakor leáll. Kifejezett
leválasztás lehetséges. Háttérbe helyezéskor a munkamenet bezárul; nincs
automatikus újracsatlakozás és visszatéréskor motorparancs-küldés.
A Bluetooth megszakadása **nem helyettesíti a fizikai leállítást**.
Tokent nem naplózunk; tetszőleges hitelesítési kivétel/JSON nem jelenik meg.
A beállítások/fájlok kimaradnak a backupból és eszközök közti átvitelből;
az ablak letiltja a token képernyőképes/előnézeti megjelenítését. Ezek a
kontrollok nem védenek kompromittált telefon/keyboard/OS vagy root hozzáférés
ellen, és nem igazolják, hogy minden telefonon hardveres a Keystore.

## TLE: telefonos letöltés és atomikus BLE-átvitel

BLE-csatlakozás **előtt is letölthető**. Válassza ki az alkalmazásban a
CelesTrak, AMSAT vagy PE0SAT szolgáltatót, majd érintse meg a Letöltés gombot.
Csak az alábbi URL-ek engedélyezettek:

- `https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle`
- `https://www.amsat.org/tle/current/dailytle.txt`
- `https://tle.pe0sat.nl/kepler/mykepler.txt`

GET-kérés token, cookie, hely, privát fájl vagy adatfeltöltés nélkül.
Nincs analitika. A szolgáltató látja a forrás-IP-t és a szokásos nyilvános
kérést. Megmarad a rendszer TLS-/hostname-/CA-ellenőrzése; nincs `TrustAll`,
HTTP, felhasználói URL, átirányítás vagy nem biztonságos fallback.
Az átirányítás vagy nem 200-as HTTP-válasz hibaként jelenik meg, a legutóbbi
katalógus megőrzésével. Tanúsítványt nem javítunk, új célra nem követünk
átirányítást. Csatlakozási/olvasási időkorlát 15 s; az olvasást méretkorlát
és két olvasás közti 45 s-os határ védi. Mégse/háttérbe helyezés megszakítja
a feladatot, újracsatlakozás vagy közzététel nélkül. Hálózat nélkül Android-
fájlválasztóval (`ACTION_OPEN_DOCUMENT`) importálható fájl, általános
tárhelyengedély nélkül.

Tárolás/átvitel felső határa **48000 bájt, 100 műhold, 64 ASCII-karakteres
név, egyedi ötjegyű numerikus NORAD-azonosító**; két 69 karakteres sor,
NORAD-checksummal, egyező azonosítóval és érvényes epochhel. A vezérlő
numerikus mezőit/tartományait ellenőrzi, de a telefon nem futtat SGP4-et.
A CRLF LF-re normalizálódik, a validált, kanonikus katalógust őrizzük meg.
Ha a legfeljebb 48000 bájtos szolgáltatói/fájl-katalógusban több mint
100 érvényes bejegyzés van, kifejezett választó nyílik (RAM-ban legfeljebb
300 jelölt): válasszon **1–100-at**, előválasztás és csendes csonkítás nélkül.
A megszakítás nem változtatja meg a korábbi cache-t. Csak a kiválasztott
részhalmaz kerül újra validálásra, mentésre és átvitelre. A 48000 bájtnál
nagyobb fájl a katalógus újjáépítése előtt elutasítandó; importáljon kisebbet.
Commitkor a firmware validációja mérvadó. Az AMSAT-ban (QO-100-zal együtt)
előforduló üres pozitív exponenselőjelet a `control_logic.h` szerint
elfogadjuk; a sorokat/checksumokat nem írjuk át, orbitális elemet nem találunk ki.

A cache csak az alkalmazás privát fájljaiban él, és kimarad a backupból.
Csak teljes validálás, staged fájl írása/szinkronizálása után, ugyanabban a
könyvtárban végrehajtott `Files.move(ATOMIC_MOVE, REPLACE_EXISTING)` cseréli.
Ha az atomikus csere nem lehetséges, a régi fájl megmarad; nincs előbb törlő,
majd utólag másoló fallback. A sikertelen frissítés nem törli az utolsó
érvényes cache-t.

Átvihető a teljes katalógus vagy **csak a kiválasztott TLE**. Mindkét esetben
lecseréli a rotor teljes katalógusát, nem összeolvasztja/hozzáfűzi; a
megerősítő párbeszéd figyelmeztet a kiválasztás és a pass-cache
érvénytelenítésére. Az alkalmazás közvetlenül a begin előtt friss,
hitelesített állapotot kér, és nyugalmi (`READY`/`DISARMED`), érvényes
GNSS UTC- és TLE-életkor-feltételeket követel: a rotor UTC-je szerint
legfeljebb 14 napos és legfeljebb 1 nap jövőbeli epoch. Nem a telefon óráját
használja. Nem engedélyez motort, követést automatikusan nem indít.
Ellenőrizze a GNSS-t, töltse fel a rotor katalógusát, majd válasszon újra.

A tényleges handlerrel összevetett v1 szerződés:

| POST útvonal | Törzs | Elvárt ACK |
|---|---|---|
| `/api/tle/begin` | `length` egész 1..48000, `sha256` 64 kisbetűs hex | pozitív uint32 `uploadId` |
| `/api/tle/chunk` | `uploadId`, szekvenciális bájtoffset `offset`, 1..512 ASCII-bájtos `text` | a pontos akkumulált értékű `received` |
| `/api/tle/commit` | `uploadId` | HTTP 2xx hiba nélkül, `message` karakterlánccal |
| `/api/tle/abort` | `uploadId` | HTTP 2xx hiba nélkül, `message` karakterlánccal |

Minden chunk a 2048 bájtos JSON-maximumot és a GATT v1 keretezését is
betartja. A következő blokk előtt END/ACK szükséges. A hash, hossz, offset,
tulajdonos és TLE ismételt ellenőrzése ESP32-n történik; az előző cache
ellenőrzött commitig megmarad. A firmware RAM-ban stagingel és atomikusan
cserél LittleFS-ben. Alkalmazásoldali teljes timeout 5 perc, kérésenként
15 s; a firmware az inaktív átvitelt 60 s után érvényteleníti. Végrehajtása
bizonytalan parancsra nincs automatikus újrapróbálás. Ha a commit ACK-ja
elveszik, az alkalmazás **nem feltételezi sem a sikeres, sem a sikertelen
perzisztálást**: kifejezetten csatlakozzon újra és kérdezze le a rotor
katalógusát.

Átvitel alatt az app tiltja a párhuzamos módosítást. A megszakítás megvárja
az aktuális ACK-t, majd abortot küld. Átvitel alatt kért STOP előbb megvárja
az abortot, aztán küldi a stopot; a fizikai vészleállítót nem helyettesíti.
Ha a commitot már elküldte, nem ígér abortot/visszaállítást: megvárja a valódi
ACK-t, bizonytalan állapotban pedig lekérdezi a rotort. Ezt az app kifejezetten
jelzi. Mozgás/követés közben nem indítható átviteli folyamat. Az app nem küld
második, párhuzamos parancsot, és a végső ACK előtt nem állítja, hogy a commit
megerősített.

## Átvonulások és autonóm működés

Az SGP4-et és a következő 24 órát az ESP32 számítja; a telefon csak a rotor
katalógusából választ műholdat és lekérdezi a `/api/passes` útvonalat.
`calculating:true` válasz esetén korlátozott, legfeljebb 60 lekérdezést
kezdeményez, 1,5 másodperces közökkel, sorosítva és hitelesítve.
Az alkalmazás az AOS/LOS értékeket kifejezett Z jelű **UTC-ben**, valamint
maximális elevációval jeleníti meg; nem váltja helyi időre az UTC-t, és nem
számol pályát. A korlát elérése megjelenik, következő lekérdezés csak
kifejezett felhasználói műveletre indul. GNSS UTC, hely és friss TLE kell;
a firmware dönt a követés biztonságáról. A TLE nem tartalmaz frekvenciát,
ilyet nem találunk ki. A megerősített követés elindítása után a telefon
bezárható: az ESP32 a firmware-szerződésnek megfelelően autonóm módon folytatja.
Nincs CAT vagy PTT.

## Firmware-rel összevetett szerződés

Az UUID-k és a keretezés forrása a `firmware/src/main.cpp`
(`setupBLE`, `serviceBLE`) és `firmware/include/ble_protocol.h`, nem külső
szolgáltatás.

| GATT | UUID |
|---|---|
| Szolgáltatás | `c8200001-4e53-4253-9000-000000000001` |
| RX, válasszal írás és hitelesítés/titkosítás | `c8200002-4e53-4253-9000-000000000001` |
| TX, értesítések | `c8200003-4e53-4253-9000-000000000001` |
| Szabványos CCCD | `00002902-0000-1000-8000-00805f9b34fb` |

BLE JSON-verzió **1**. Minden keret 5–20 bájt:
`0x53, flags, sequenceLo, sequenceHi, payload(1–16 bájt)`.
START=1, END=2; little-endian sorszám nullától. Egyetlen töredéknél
START|END=3. MTU 185 tárgyalása (visszaesés 23-ra); **a v1 nagyobb MTU
esetén is 20 bájtot használ keretenként**, ahogy a firmware. Nincs newline,
NUL vagy részleges karakterlánc-összefűzés: UTF-8 dekódolás csak END után.
Kérés maximum 2048, válasz 8192 bájt. Elutasítandó a sorrendhiba, ismételt
START, ismeretlen flag, hibás UTF-8, idegen azonosító és túl nagy üzenet.

A teljes `status` válasz kötelező értékei:
**`apiVersion:2`, `protocolVersion:1`,
`firmwareVersion:"0.3.0-prototype"`**, a
`firmware/include/ble_protocol.h` fájllal összevetve. Más verzió, hiányzó
mező vagy szöveg típusú verzió letiltja a vezérlést és bontja a kapcsolatot.
A firmware-verzió összehasonlítása szándékosan pontos: új, akár kompatibilis
verzió is megköveteli az alkalmazás áttekintését/frissítését és a tesztek
futtatását.

Kérés:

```json
{"v":1,"id":1,"path":"/api/status","method":"GET","token":"<helyben megadva>","body":{}}
```

Válasz:

```json
{"v":1,"id":1,"code":200,"data":{"mode":"READY","fault":"","homed":true,"calibrated":false}}
```

Ez a részlet **szemléltető**, nem elfogadott teljes állapot: a firmware-ből
származó, tipizált pozíció-, UTC-, hely- és biztonsági mezők is szükségesek.
A `code=401/403` akkor sem fogadható el, ha a `data` sikerre utal.
Azonosítók pozitív uint32 értékek, kapcsolatonként szigorúan növekvők;
számláló csak kapcsolat bezárásakor indul újra. Első csere:
`GET /api/status` tokennel, bonding, szolgáltatásfelderítés, MTU és CCCD-
visszaigazolás után. `/auth` útvonalat nem találunk ki.

Egyszerre egy GATT-művelet és egy repülő JSON-kérés lehet. Minden írás
megvárja az `onCharacteristicWrite` eseményt; az elutasított indításnak
legfeljebb két korlátozott újrapróbálása van.

A ténylegesen támogatott útvonalak: GET `status`, `tle`, `passes`; POST
`stop`, `clear`, `home`, `move`, `calibrate`, `site`, `select`, `track`,
`catalog`, `tle/begin`, `tle/chunk`, `tle/commit`, `tle/abort`.
A képernyő a valódi, lapozott `POST /api/catalog` katalógust használja
egész `offset` és `limit:10` értékekkel, és a kiválasztás engedélyezése
előtt ellenőrzi a `total`, folytonos ID-k és `nextOffset` értékeket.
A „Következő oldal” kifejezett művelet, nincs kérésciklus. Mechanikus AZ
[-180,180]°, EL [0,90]°; valódi irány [0,360)°; hely lat [-90,90]°,
lon [-180,180]°, magasság [-500,9000] m. Csak véges numerikus érték
fogadható el; numerikus karakterlánc és boolean nem szám. A rotor számolja
az SGP4-et és az átvonulásokat; telefonos internet csak szolgáltatói
letöltéshez kell; helyi fájl importálható vagy internet nélkül használható
előzetesen betöltött TLE. A 8192 bájtnál nagyobb teljes GET `tle` elutasított;
a felület lapozott katalógussal kerüli meg a korlátot, és a rotor 100
műholdját is kezeli.

A vezérlő ugyanazokat a handlereket használja HTTP-n és BLE-n. Ha az egyik
átvitel birtokolja a mozgást, a másik nem indíthat vezérlőparancsot: 409-et
kap; a hitelesített STOP és állapotlekérdezés elérhető. Az app nem veszi át
csendben a vezérlést. Az ellenőrzött firmware-ben mozgás közbeni kézi
vezérlés/homing BLE-vesztése FAULT-ot okoz; a már elindított autonóm követés
nem függ a képernyő vagy app nyitva tartásától. STOP nem töröl hibát;
`clear` új homingot és kalibrálást követel.

## Hardveres validálás hátravan

A JVM-tesztek a logikát/protokollt ellenőrzik, nem a telefon rádióját.
Valódi Android-eszközön még ellenőrizendő: passkey párbeszéd, bonding
nélküli elutasítás, a firmware által megkövetelt MITM-titkosítás,
MTU 23 és tárgyalt MTU, 26/30/31/35 engedélyek, timeout, rádióvesztés,
második kliens és fizikai leállítás. Nem állítjuk, hogy a motorok, BLE-kapcsolat
vagy kalibrálás terepen validált.

## Felülvizsgálat 2026-10-11: TLE-letöltés, BLE-szinkron, arculat és súgó

A változtatásokat a felülvizsgálati környezetben **nem fordítottuk Gradle-lel** (nincs hálózat a Maven/SDK felé). A `TleCatalogue` és a
`TleDownload` logikáját `kotlinc`-kel JVM-en lefordítottuk, és ellenőrzést futtattunk; a JVM-tesztek (`./gradlew testDebugUnitTest`) még függőben vannak.

| Megállapítás | Valószínű ok | Javítás |
| --- | --- | --- |
| Hasznos magyarázat nélküli letöltési hibák | bármely HTTP-kód vagy időtúllépés „TLE érvénytelen: tle_http_…” vagy általános hibaként jelent meg | konkrét üzenetek: használati korlát (403/429), átirányítás (301/302/303/307/308), nem található, szerver és időtúllépés; az érvényes gyorsítótár megmarad |
| A sorvégi szóközös letöltés elbukott | az elemző pontosan 69 karakteres, záró szóköz nélküli sorokat követelt | a `TleCatalogue.parse` figyelmen kívül hagyja a záró szóközöket/CR-t/tabulátort (az érvényesített tartalom és az ellenőrzőösszeg változatlan) |
| A Raspberry felé az átvitel 300 mp-nél megszakadt | rögzített teljes időzítő, 512 karakteres blokkokkal 20 bájtos BLE-kereteken | elakadásészlelés: minden ACK-nál újraindul (60 mp); 60 mp előrehaladás nélkül megszakít és bont |
| BLE kapcsolódási hiba `133` | gyakori átmeneti Android-állapot újrapróbálás nélkül | legfeljebb 2 automatikus újrapróbálás a `BleTransport`-ban (a `RadioHostBleTransport`-ban még nincs) |
| Nincs logó és súgó | — | logó és szerzők mindhárom képernyőn (`Branding.kt`), BricoHams indítóikon, Súgó gomb (`HelpActivity`; offline szövegek a `res/raw`, `res/raw-en`, `res/raw-hu` mappában) |

**Megjegyzés a szolgáltatókról:** a korábbi ellenőrzés (fent) 97 műholdat töltött le az AMSAT-tól, de a CelesTrak és a PE0SAT időtúllépett arról a hálózatról.
Ebben a felülvizsgálatban egy webolvasó eszköz `302`-t kapott az AMSAT-tól `http://`-re, amit az alkalmazás elutasítana (nincs átirányítás, nincs titkosítatlan
forgalom), de az alkalmazással ez nem volt reprodukálható, ezért **egyetlen** szolgáltatót sem tiltottunk le. Ha egy szolgáltató nem működik a hálózatodról, az
alkalmazás elmagyarázza és másikat javasol; jegyezd fel a tesztnyilvántartásba, melyik működik (APP-03). A szolgáltató látja a kapcsolat IP-címét.

Valós telefonon még ellenőrzendő: a három szolgáltató a felhasználó hálózatáról, egy nagy katalógus teljes BLE-átvitele és a 133-as hiba újrapróbálása.
Tesztek: [testing/07-app-android.md](testing/07-app-android.md).
