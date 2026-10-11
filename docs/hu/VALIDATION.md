# Szállítási validációs napló

Dátum: 2026-10-10. Állapot: a korábbi ESP32-alap digitális validálása
megtörtént; a CM5-bővítés hiányos, a fizikai elfogadás hátravan.

## CM5-bővítés: aktuális kapuk

Az alábbi, ESP32-alapra vonatkozó PCB/firmware/Android-eredmények nem
validálják az új CM5-segédpanelt vagy annak független biztonsági felügyeletét.

| Új felület | Bizonyíték | Korlát |
|---|---|---|
| Moduláris dokumentáció és árak | Három, dokumentációs hivatkozásokat és árak következetességét ellenőrző Node-teszt sikeres | Nem teljes költségvetés és nem fizikai próba |
| CM5-segédpanel és biztonsági felügyelet | Interfésztérkép; 11 jelentett szerződésteszt | Nincs új bekötési rajz/vezetett NYÁK, ERC/DRC, Gerber, BOM vagy CPL |
| Rádió és rotor | Kapcsolódás a meglévő adapterhez és kilenc jelentett útvonal; 57, kifejezetten tesztvezérlőt használó offline teszt jelentve | A valódi CM5-szolgáltató/BSP és a biztonsági felügyelet függőben; nem bizonyít fizikai követést vagy TX-engedélyt |
| CM5-rotorvezérlő | 29 offline teszt jelentve, köztük az `open_adapter` összekapcsolása és a szolgáltató hiányának elutasítása | Nincs üzembe helyezett CM5-szolgáltató; éles üzemben nem helyettesíthető szimulációval |
| BricoHams OS-recept | Helyi ismétlés: kilenc OS-teszt sikeres, egy Linux/Python-teszt kihagyva; a dokumentációval/árakkal együtt futó összesítés 12 sikeres, nulla hibás, egy kihagyott | Nincs pi-gen build vagy CM5-indítás; az integrált OS-szolgáltatás szándékosan nincs engedélyezve |
| POL-mechanika | Hét teszt jelentve; hét nyomtatható alkatrész és három DXF-sablon jelen van; a húzásmentesítő exportja zárt hálóként jelentve | Az 5:1 és a 16 000 lépés/fordulat felbontás nem pontosság; lágy határok +/-80 fok, NC cél +/-85, jelölt keményütköző +/-90 fok; a névleges nulla hézag miatt tűrésellenőrzés szükséges |
| Android CM5 | 58 JVM-teszt; lint/assemble és v2-aláírás jelentve; 33 lint-figyelmeztetés, nulla hiba. A helyi APK 1 208 309 bájt, SHA-256-ellenőrzése sikeres | Nincs fizikai BLE/RF-teszt; a térkép/radar továbbra is offline, ellenőrzött OrbitSnapshot-leképezés nélkül |
| Android-orbitális funkciók | A snapshotmodell különbözik a rotor válaszától | A host/alkalmazás szerződése és integrációja függőben; kompatibilitás nem feltételezhető |
| Tömeg és autonómia | ≤5 kg-os cél kizárólag a külső akkumulátor nélkül, valamint kétórás cél | A CM5-ös teljes egységet állvánnyal és kábelekkel még le kell mérni | 

**CM5-TARTÁS:** ne gyártsd le az új segédpanelt, és ne aktiváld a motorokat
vagy a TX-et a GPIO-térkép, illetve a szerződéstesztek alapján. Hiányzik a
biztonsági áramkör, a minősített elektromos interfész és a tényleges
gyártási állomány.

Az Android CM5 debug APK a buildkimenetektől elkülönítve megőrzött példánya:
[PortableSatStation-CM5-debug.apk](../../releases/android/PortableSatStation-CM5-debug.apk).
SHA-256:
`ed52e0881353d7542dda1fac5062b372e2ea4bb8489710edc98386ecf5a77dd7`.
Az Android-panel hét valódi útvonalat kérdez le és a válaszokat jeleníti
meg; nem alakítja a JSON-adatokat térképpé/radarrá, és ACK fogadásából nem
igazolja az elért pozíciót. A távoli CM5-homing/kalibrálás nincs kitéve,
mert megbízható helyi megerősítést igényel.

## Jelenlegi végső összefoglaló

| Szállítandó | Eredmény | Korlát |
|---|---|---|
| Node-összesítés | 35/35 sikeres | Nem mér latenciát vagy hardvert |
| ESP32-firmware | Fordítás; Unity 6/6 és valódi SGP4-vektor | Fizikai párosítás/motorpróba nélkül |
| Android | Debug APK, 29 JVM, nulla lint-probléma, ellenőrzött aláírás | Fizikai BLE-telefon nélkül |
| WebFlash | Valódi bundle, 9 ellenőrzés, böngészős smoke teszt | Fizikai USB és távoli Pages nélkül |
| PCB | ERC/DRC/paritás/fel nem kötött net: nulla; valódi Gerberek | Gyártási/üzemeltetési HOLD |
| CAD | Hálók és matematika ellenőrizve; branding egyesítve | Szerelés/nyomaték/szél nem tesztelt |
| RF | Dokumentáció és kezdeti méretek | SWR/nyereség/leválasztás nem mérve |
| Tömeg | BuildLight 3,130–3,200 kg, további elemek előtt | NEM teljesíti a <=3 kg célt |

Az alábbi szakaszok az integráció történetét tartalmazzák. A fenti
összefoglaló a szállítás állapotáról irányadó; a hash-ek konkrét
revíziókat jelölnek, flasheléskor ne keverje őket.

**Legutóbbi összesítés: 35/35 teszt sikeres, nulla hiba.**
Javítva lett a fedélháló, a rézvastagság-mező és az NVS-átfedést vizsgáló
fixture. Az alábbi történeti hibanaplók nyomon követhetőség céljából
maradnak meg; nem a jelenlegi eredményt mutatják. A digitális szállítás
ekkor még várta a végső PCB/WebFlash-jelentéseket.
A végső PCB/WebFlash/Android-jelentés azóta megérkezett; fizikai elfogadás
van hátra, nem ezen artefaktumok fordítása. Antenna/rotor/PCB fizikai
tesztje és távoli Pages-futtatás nem történt. BLE-firmware, USB,
TLE-átvitel, megosztott verziók és nagyobb doboz beépítése után az
összesítést megismételték: 35/35 sikeres. Az Android JVM/build próbái
az alkalmazás befejezésekor külön szerepelnek.

Ez a napló megkülönbözteti a digitális próbákat a fizikai viselkedéstől.
A firmware/CAD végső eredményei az integráció befejezésekor kerültek be;
addig nem tekintettük őket elfogadottnak.

| Felület | Jelenlegi bizonyíték | Állapot |
|---|---|---|
| RF/fogaskerék/terhelés számítások | Node.js 22.16.0, 5/5 teszt | Aritmetika elfogadva |
| OBJ/STL-referencia ellenőrző | 2/2 teszt, nem módosítja a bemenetet és nem feltételez egységet | Metaadat elfogadva |
| Dokumentációs hivatkozások | Helyi linkek feloldva, CONTROL.md is | Elfogadva |
| Számoló és tesztek diagnosztikája | VS Code hibamentes | Diagnosztika elfogadva |
| Eredeti PDF-ek | SHA-256 az `input-hashes.json` fájlban, helyi Xpdf-kivonat | Rögzítve |
| ESP32-firmware | Vezérlő sikeresen fordult; WebFlash provisioning revízióban | Fordítás elfogadva, próbapad nem |
| Web AP | Szintaxis/DOM/API-próba és nyolc hitelesített művelet | Digitális elfogadva; hardver hátravan |
| CAD/STL | 34 STL exportálva; matematika/leltár próbái sikeresek | Részben digitális; tömeg ellenőrzés alatt |
| Mechanikai összeszerelés | Nincs megépített prototípus | G1 hátravan |
| Antenna/diplexer/hibrid RF | Nincs együttes VNA-mérés | G2 hátravan |
| Terepi követés | Fizikai berendezést nem üzemeltettek | G3/G4 hátravan |

## Környezeti eszközök

Kezdetben Node, OpenSCAD, PlatformIO és pdftotext nem volt a PATH-ban.
A Python-környezet konfigurálásához sem adott a bővítmény implementációt.
Hordozható Node-ot és helyi Xpdf-et használtunk a munkamenet
artefaktumkönyvtárában, nem globális telepítést és nem az Intune-könyvtárat.

Node 22.16.0: hivatalos letöltés, ZIP ellenőrzése a hivatalos
SHASUMS256-hoz:

`21c2d9735c80b8f86dab19305aa6a9f6f59bbc808f68de3eef09d5832e3bfbbd`

Xpdf tools 4.06: `https://dl.xpdfreader.com/xpdf-tools-win-4.06.zip`.
A PDF-eket nem küldtük harmadik félnek. A két PartIIRotatorcontrol
SHA-256-a azonos; egyetlen duplikált forrásként kezeljük, nem két külön
tanulmányként.

## Lefuttatott számítási parancsok

```powershell
node --test tests\engineering.test.cjs
node scripts\engineering-report.cjs
```

Eredmény: 5 teszt, 5 sikeres, 0 hiba. A VS Code integrált tesztfelfedezője
nem találta meg a CJS-teszteket; a Node natív tesztfuttatója futott.

Az `scripts/validate.ps1` legutóbbi integrált futása: 12 teszt,
12 sikeres, 0 hiba. A CONTROL.md korábbi integrációs hibája a
vezérlő-dokumentáció átvétele után megoldódott. A webpróba ellenőrzi
a szintaxist, DOM-ot, API-sémát, nyolc hitelesített műveletet és a nevek
biztonságos megjelenítését; ez nem fizikai ESP32-teszt.
A metaadat-ellenőrző két saját tesztje sikerült; az eredeti OBJ/STL
fájlokat módosítás nélkül olvassa. A TDS_AV2040 hibás kódolású szövege
miatt helyi raszterizálást igényelt; a számadatokat vizuálisan ellenőrizték.

A kezdeti mechanikai szállítmány 34 STL-t exportált OpenSCAD-del,
és ellenőrizte a zárt/orientált éleket, illetve pozitív térfogatot.
A mechanikai tesztek involutát, 25:1 arányt, bolygófázist és 121 ideális
fogkapcsolódási metszeti pozíciót tartalmaztak. Nem teljes állomásütközés-
vizsgálat és nem szerelési próba.

A kezdeti, teljesen tömör ASA-egyenérték számítás 2,641 kg volt a
fémalkatrészek hozzáadása előtt. A <=3 kg tömegcél nincs igazolva;
geometriaoptimalizálást és teljes tömegbüdzsét kértek. A tömör értéket
ne tüntesse fel infill-es nyomtatás tömegeként, és ne hagyja ki az akkumulátort.

Korlátozott revízió: 2,521 kg tömör ASA-egyenérték, megtakarítás 120,45 g.
További büdzsé: 1,464–2,294 kg; hipotetikus, rádió/állvány nélküli nyomtatott
össztömeg: 3,208–4,038 kg. Nem teljesíti a <=3 kg-ot. A felhasználó engedélyezte
az áttétel cseréjét és a tömeg elsőbbségét. Az új, könnyű BASE-változat két
GT2 20:100 fokozattal elkészült; a régi eredmények bolygóműves változatra
vonatkoznak, és nem validálják automatikusan az újat.

A PCB/WebFlash befejezése előtti legutóbbi összesített futás: 16 teszt,
16 sikeres, 0 hiba. Szíjmatematika, új hálók, tömegaudit, dokumentáció és
webes biztonsági felületek is szerepelnek benne. A statikus interlock-
ellenőrzés nem latenciamérés.

BASE: 0,862 kg tömör ASA-egyenérték; büdzsé 3,121–4,006 kg, hipotetikus
könnyített forgatókönyv 2,905–3,790 kg. A <=3 kg továbbra sincs bizonyítva.
A visszahajtható szíjakhoz kiegyensúlyozás és független mechanikai megtartás kell.

A vezérlő ESP32-DevKitC V4/WROOM-32E-re, PSRAM nélkül fordult:
PlatformIO 6.1.18, espressif32 6.10.0, Arduino 2.0.17. A vezérlő
fejlesztője 4 Unity-tesztet és Vallado SGP4-vektorpróbát futtatott, sikerrel.
A befagyasztott PCB-lábkiosztással közölt firmware SHA-256-a:
`99B550AF144C31B5B7918F3A5E17D245F108D1C602CB234E8E79358E066045B3`.
A hozzárendelés utáni közölt LittleFS:
`EDBDB2F968F6CC0DA83A04061E3806A4C7C403735B9C8C3EA44B897F62E8D9C2`.
E hash-ek ezt a revíziót jelölik; későbbi provisioningváltozás újrafordítást
és új hash-ek rögzítését igényli.

Fejlesztés alatt álló carrier PCB: 180x130 mm, nem fér a régi 124x64 mm-es
belső méretű dobozba. Új dobozintegrációt kértek; közös GPIO-térkép alapján
ne állítsa, hogy illeszkedik. Gerber/ERC/DRC jelentés még nincs.

Integrációfrissítés: 28 új Node-teszt, 28 sikeres, 0 hiba; az új,
180x130-as carrierhez való dobozt, frissített tömegbüdzsét és
manifest/WebFlash-próbákat is beleértve. Ez nem tanúsít PCB-t, USB-flashelést
vagy távolról futtatott GitHub Actions-t.

A vezérlőbe 115200 baud-os helyi USB-provisioning került
(`setup`, `config`, `carrier`, `reboot` JSON-parancsokkal), hitelesítő
adatok fordítás nélküli beállítására. A SETUP letiltja a motorokat/Wi-Fi-t/API-t
és érvényteleníti a homingot/kalibrálást; az NVS nem titkosított, fizikailag
védendő. Közölt Unity-tesztek: 5/5. Az izolált buildben közölt legutóbbi bináris
SHA-256-a:
`C413748CDDF16C3AFF782FF3663F93D7B9BB613DB90DAF1FD73C067CEF0771CE`.
A WebFlash-telepítésnek ugyanabból a revízióból kell újraépítenie és saját
ellenőrizhető hash-eit kiadnia; a történeti hash-eket ne keverje.
CA nélküli nyilvános képen a HTTPS tiltott; kézi TLE-import rendelkezésre áll.
Fizikai USB-próba nem történt.

Későbbi, PCB/branding integrációs futás: 35 tesztből 31 sikeres, 4 hiba
az új dobozfedél degenerált háromszögei miatt. A geometria/export javítását
kérték a validátor lazítása nélkül. A fedél e hiba fennállásáig nincs
elfogadva. A PCB öt tesztje sikeres: SHA-256-manifest, 38 pines lábkiosztás
és ERC/DRC/paritás jelentés. A PCB-tulajdonos végső jelentése és fizikai
ellenőrzés hátravan; automatikus kiadás nincs.

Javított fedél: bináris export ellenőrzése a fájlcsere előtt; 9024 háromszög,
egy összefüggő komponens és 0,7 mm domborítás. Közölt SHA-256:
`EC5806AA9FF4EB068FBC695D6CEEF794CD9DDE1DB68270D784114A5068320E34`.
Legutóbbi összesítés: 35 tesztből 33 sikeres és két integrációs hiba:
PCB-teszt rézvastagság-mezője, valamint a WebFlash-fixture hibás fejléc miatt
az NVS-átfedési teszt előtt elbukott. A bizonyíték/fixture javítása az
elfogadási feltételek gyengítése nélkül szükséges. Végső összesített
jóváhagyás ekkor még hátravolt.

A végső doboz kábelezési térrel bővült: belső méret 224x174 mm,
külső 228x178 mm, a PCB felett 32 mm; élanként 22 mm. Négy STL és
240x196x2 mm-es tálca újragenerálva; 11 sikeres mechanikai tesztet közöltek.
A fedél egy összefüggő komponens, integrált brandinggel. Frissített
BuildLight-büdzsé 3,130–3,200 kg a MÉG HIÁNYZÓ kiegészítések előtt.
**Ebben a revízióban a <=3 kg követelmény nem teljesül.** Korábbi,
alacsonyabb forgatókönyvek nem tüntethetők fel végső, validált tömegként.

Végső PCB: KiCad 10.0.7, ERC/DRC/paritás/fel nem kötött kapcsolatok:
nulla; 180x130 mm, két réteg, 2 oz, 40 alkatrész, 17349 szegmens,
55 via. Réz/maszk/szitaminta/kontúr valódi Gerberek, PTH/NPTH Excellon,
netlista és SHA-256-manifest exportálva. ZIP:
`fabrication/PortableSatCarrier-Gerbers-CAD-VERIFIED-NOT-RELEASED.zip`.
Gyártás/üzemeltetés HOLD a modulméretek, pontos DC-leállító, illetve
fizikai elektromos/termikus minősítés miatt.

BLE/Android-bővítés és vezetett kalibrálás fejlesztés alatt.
Az app HTTPS-en tölti le a TLE-t, BLE-n továbbítja; az ESP32 marad az
átvonulás/követés számítója. Új bináris és ugyanazon revízió bizonyítékával
új WebFlash-build szükséges.

Közölt végső BLE-firmware: NimBLE 1.4.3 (Apache-2.0), bonding,
MITM/titkosítás és token; USB-s passkey, kezdetben kikapcsolt BLE.
Közös HTTP/BLE handlerek; a callback összerak/queue-ba tesz, és nem futtat
nehéz filesystem/SGP4 feladatot. TLE begin/chunk/commit/abort hossz-, SHA-256-
és szekvenciális offset-ellenőrzéssel; lapozott műholdlista.
Befagyasztott verziók: `apiVersion=1`, `protocolVersion=1`,
`firmwareVersion=0.2.0-prototype`. Közölt vezérlőbuild: flash 1199509 bájt,
statikus RAM 59084 bájt. Firmware SHA-256:
`64194FB5A0FBDB16D5ECBB6233F56D88C587E91C998A8E8A4F621B9C6C185DD3`.
Unity 6/6 és Node control 3/3 közölt siker. Fizikai párosítás, BLE-latencia
és Wi-Fi/motor együttélés nincs tesztelve.

Végső átviteli revízió: BLE-szétkapcsolás azonnal megszakítja a RAM-ban
lévő feltöltést és felszabadítja a tulajdonjogot, a perzisztált cache
megtartásával. Újrafordított firmware közölt SHA-256-a:
`143A541D86F87922459371FB4F7E5C2B615AC8932382A9E2521BDFC0362EFF81`.
Ez a hash váltja fel az előzőt e revízióra; a WebFlash-t azonos változással
kell újraépíteni. TLE-importhoz nem kell GNSS-fix, de követésindításhoz
érvényes UTC/hely/TLE továbbra is szükséges.

Valós szolgáltatói validálás: az AMSAT HTTPS-katalógus üres pozitív
exponensjelet tartalmazott. A vezérlő és app parserét úgy javították,
hogy a sorok ne módosuljanak és a checksum-szigor ne lazuljon.
Unity 6/6 és valódi SGP4-ellenőrzés sikeresnek közölve. A javítás utáni
firmware-hash:
`549B1DAB4121E490E355D6259675483B8C752780CF0B7A52CDEB4CBC568BAD02`.
Az Android-kód által végrehajtott letöltés 14434 bájt, 97 érvényes
műhold; SHA-256:
`ec291294636090d712fc901e4a7e3fa15bbeb8366fb771d7aad131b5c8db1ce9`.
CelesTrak/PE0SAT asztali ellenőrzése timeoutot adott; a cache megmarad,
TLS-t nem tiltották le. A teszt nem garantálja a szolgáltatók jövőbeni
elérhetőségét.

Végső WebFlash: valódi build és bundle az aktuális forrásfából,
AMSAT-javítást tartalmazó fejléccel. Kilenc valódi artefaktum-ellenőrzés
és helyi böngészős smoke teszt sikeres (HTTP 200, figyelmeztetési kapu,
helyi dialog-importok), USB megnyitása nélkül. A bundle firmware-hash-e
`549B1D...BAD02`. LittleFS SHA-256:
`866C1AF7C5B1FFE96C5DCC4DCF8C692383DDDE28FEF7C772581148DC37D12256`.
A bundle metaadata forrás/config/UI fákat, csomagverziókat és npm-lockot köt
össze. Flash-használat 1199553 bájt, statikus RAM 59084 bájt. A LittleFS
metaadatok miatt buildenként változhat; mindig a tényleges hash validálandó,
bináris reprodukálhatóságot nem feltételezünk.

Az ESP Web Tools a `new_install_prompt_erase=true` beállítást igényli, hogy
a törlési lehetőség kezdetben ne legyen kijelölve; false automatikusan törölhet
Improv nélküli eszközön. A figyelmeztetés és megerősítés megmarad.
Pages-hez prototype-only jóváhagyási változó és reviewerrel védett környezet
kell; nem történt közzététel vagy GitHub CI-futtatás.

## Végső Android-eredmény

APK: `android/app/build/outputs/apk/debug/app-debug.apk`, 980724 bájt.
SHA-256:
`47997a78abd87b3aa4e26a33106f9b122a817121dd02c2abc7d6b72717ca399b`.
Sikeres build, 29 hibamentes JVM-teszt, nulla lint-probléma és sikeresen
ellenőrzött debug-aláírás. Nem release-aláírás vagy áruházi terjesztés.
Az előkészített CI újragenerálhatja az artefaktumokat; a buildkönyvtár nem
része a verziókezelt kódnak.

A HTTPS-letöltés a három szolgáltatóra korlátozott; fájlimport, privát
atomikus cache, teljes/kiválasztott BLE-átvitel, rotorállapot-előellenőrzés,
legfeljebb 60 pass-lekérdezés és UTC-idő. A hitelesítő adatok Android
Keystore-szal titkosítva; az INTERNET-engedély kizárólag jóváhagyott
letöltéshez használatos, token vagy privát adat nem kerül feltöltésre.
A rotor számolja az SGP4-et, a telefon nem küld pályát. Valós AMSAT-próba
sikeres; CelesTrak/PE0SAT timeout dokumentálva. Android/BLE/motor közös
fizikai összeállítása nincs tesztelve.

A 8 m/s-os szélpélda a 2-es biztonsági tényezővel **NEM teljesítette**
a nyomatéki keretet. A teszt éppen azért sikeres, mert kimutatja ezt a
korlátot; nem igazolja az ilyen szélben történő működést.

## Ellenőrzés 2026-10-11 (felülvizsgálati környezet, hardver nélkül)

| Tesztcsomag | Eredmény | Megjegyzés |
| --- | --- | --- |
| `node --test "tests/*.test.cjs"` | 66/66 | az `npm test` javítva Node 22-höz |
| `pytest tests/rotor tests/radio_host` | 86 sikeres | a `test_controller` segédfüggvény átnevezve (a pytest tesztként gyűjtötte be); `PYTHONPATH=.:radio:rotor` |
| Natív vezérlőlogika (Unity, g++) | 6/6 | `tests/control_logic/test_native` |
| OpenSCAD 2021.01 render a logós alkatrészekről | vízzáró | 4 alkatrész |
| Android JVM, KiCad ERC/DRC, `control_sgp4.cpp`, OS-lemezkép | **nem futott** | nincs hálózat a Gradle-hez, nincs KiCad, nincs rögzített SGP4 könyvtár, nincs Docker/Debian tükör |

## Értelmezés

Egy lefordított orbitális könyvtár nem igazolja a kábelezést, az érzékelők
pontosságát vagy a teljes követést próbapadi vizsgálat nélkül.
Az exportált háló nem igazolja az illeszkedést, szerelhetőséget,
szilárdságot vagy fogkapcsolatot. A kezdeti méretek nem garantálják az RF-
illeszkedést/nyereséget. A nyitott korlátozásokat az ACCEPTANCE.md és
RISKS.md írja le.
