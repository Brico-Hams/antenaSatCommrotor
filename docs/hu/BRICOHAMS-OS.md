# BricoHams PortableSatStation OS

## Mi ez a lemezkép?

Ez egy **64 bites Raspberry Pi OS Lite-származék** összeállítási receptje,
neve **BricoHams PortableSatStation OS**. A kiválasztott Compute Module 5
(CM5) és a hivatalos, 2. revíziós CM5 IO Board, valamint a projekt csak-GPIO
segédpanelje számára készül. Nem helyettesíti a Raspberry Pi OS kiadását,
nem hivatalos Raspberry Pi termék, és hardveresen nem validált lemezkép.

A build a hivatalos Raspberry Pi `pi-gen` `arm64` ágát használja, az
[`os/pi-gen.commit`](../../os/pi-gen.commit) fájlban rögzített teljes, állandó
committal, valamint a Trixie `stage2` Lite exporttal. A rögzített upstream
szakasz `-lite` jelölésű. A `pi-gen` az ARM64 buildeket az `arm64` ágán
dokumentálja, és jelenleg alapértelmezésben Trixie-t használ. A Debian
csomagtárolók továbbra is változhatnak biztonsági javítások telepítéséhez;
ezért ez reprodukálható *recept*, nem bitről bitre reprodukálható bináris
lemezkép. Minden build létrejött SHA-256 értékét rögzítsd.

A lemezkép szándékosan megtartja a Raspberry Pi OS `/etc/os-release` fájlját,
az upstream csomagdokumentációt és az első indításkori fióklétrehozást.
A BricoHams külön konzol-/bejelentkezési banner és képnèv. A Raspberry Pi OS
név az upstream alapot azonosítja; nem jelent Raspberry Pi-támogatást.
A projekt aktuális szerzői és upstream közleményei a
`/usr/share/doc/bricohams-os/` könyvtárba kerülnek.

## Build Linuxon

A Windows fejlesztői környezet nem állítja össze a Linux lemezképet. Natív
Linux-gép vagy Linux virtuális gép szükséges Docker Engine-nel, Git-tel,
rsync-kel, coreutils-szal és legalább 60 GiB szabad hellyel natív Linux
fájlrendszeren (például ext4, XFS vagy Btrfs). A build internetet igényel a
rögzített Raspberry Pi tárolóhoz, Debian Trixie tárolókhoz és a rögzített
Python-csomagfüggőségek indexéhez. A `pi-gen` munkakönyvtárat ne helyezd
NTFS-re, `/mnt/c` alá, megosztott Windows-fájlrendszerre vagy szóközt
tartalmazó elérési útra.

A projekt tiszta Linux-klónjából:

```bash
BUILD_ROOT=/var/tmp/bricohams-os-build \
  bash os/build-image.sh
```

A `BUILD_ROOT` nem tartalmazhat már `pi-gen` klónt. A képarchívum és a
mellé írt `.sha256` fájl a `BUILD_ROOT/artifacts/` könyvtárba kerül.
Ha máshová kell írni, állítsd az `OUTPUT_DIR` értékét. A szkript megtagadja
létező képfájl vagy ellenőrzőösszeg felülírását, a pontos `pi-gen` commitot
checkoutolja, a pi-gen Docker-útját használja, ellenőrzi a staging root
fájlrendszerben a hitelesítő adatokat/gazdagép-kulcsokat, majd kiírja az
archívum hash-ét. **Nem** ír SD-kártyát vagy eMMC-t, nem módosít csatlakoztatott
eszközt, nem engedélyezi a rádiószolgáltatást, és nem tesz közzé GitHub-kiadást.

Az opcionális, kézzel indított GitHub Actions képfeladat ugyanazt a receptet
használja. Elkülönül az automatikus push/PR-ellenőrzéstől, és csak az
ellenőrzött képarchívumot és ellenőrzőösszeget tölti fel rövid élettartamú
Actions-artifactként. A repository láthatósága meghatározza, ki töltheti le
az Actions-artifactet; csak akkor indítsd ezt a feladatot, ha ez a terjesztés
elfogadható.

## Beépített futtatókörnyezet

A lemezkép alapja a helyi, első indításkor használt profilválasztó és a
build-előfeltételek; egyik alkalmazás-verem sincs benne előre telepítve. Az
upstream első felhasználó beállítása után a `tty1` helyi promptján kötelező
kifejezetten választani a `rotor-only`, `radio-only` vagy `integrated` profil
közül. A telepítő csak a választott profil Debian-futtatókörnyezeti és
projektcsomagjait teszi a `/opt/bricohams/venv` környezetbe. Rádióprogram,
rádiókonfiguráció és rádió systemd-egység csak rádiót tartalmazó profilba
kerül. A nem kiválasztott projektforrás a profil telepítése után törlődik;
profilt nem következtet ki automatikusan. A `rotor-only` nem telepíti a
BlueZ-t, SoapySDR-t, LimeSuite-t vagy az LMS7 bővítményt. Az `integrated`
mindkét függőségkészletet telepíti, de a rotor-szolgáltató függőben léte
miatt még nem üzemképes integrált profil.

| Első indítási választás | Telepített verem | Üzemi határ |
|---|---|---|
| `rotor-only` | Rotorfüggőségek; SDR-verem nélkül | Nincs mozgásszolgáltatás, amíg a gyártási CM5 BSP/adapter nem áll rendelkezésre |
| `radio-only` | Csak rádió-/SDR-függőségek | Kézi frekvenciás RX; a TX a fizikai kapu leképezéséig tiltva marad |
| `integrated` | Mindkét függőségkészlet | Nincs integrált szolgáltatás; követés hiányában nincs visszaállás kézi módra |
| Antenna-only | Nincs szükség gazdagép-profilra | A mechanikai/RF-modul önállóan szerelhető és minősíthető |

A profilválasztó a tényleges projektcsomag-belépési pontokat `--help`
kapcsolóval ellenőrzi, és a SoapySDR Python-kötést csak rádiós profilon
importálja; fizikai eszközöket nem sorol fel és nem inicializál. A rádió
systemd-egysége csak `radio-only` és `integrated` esetén kerül
`/etc/systemd/system` alá, a választó pedig soha nem engedélyezi. A
csomag-/API-azonosság tekintetében a projekt csomagmanifesztjei az irányadók.
Az [`os/runtime-requirements.txt`](../../os/runtime-requirements.txt) rögzíti
a rotor futásidejű Python-függőségeit; az
[`os/build-requirements.txt`](../../os/build-requirements.txt) rögzíti a
PEP 517 build-hátteret. Lásd a különálló
[rotor](../../os/install/rotor-only.md), [rádió](../../os/install/radio-only.md),
[antenna](../../os/install/antenna-only.md) és
[teljes állomás](../../os/install/full-station.md) telepítési útmutatókat.

A rendszerindítási konfiguráció kizárólag a befagyasztott CM5IO-segédpanel
busztérképét tartalmazza:

```ini
dtparam=i2c_arm=on
enable_uart=1
dtoverlay=spi1-3cs,cs0_pin=18,cs1_pin=17,cs2_pin=16
```

Ez bekapcsolja az I2C1-et BCM 2/3 lábakon, az SPI1-et CS0/CS1/CS2-vel BCM
18/17/16-on, valamint a GNSS UART-ot BCM 14/15-ön. A rögzített pi-gen
stage1 parancssor `console=serial0,115200` paramétert ad meg; a lemezkép
szakasza ellenőrzi és eltávolítja pontosan ezt a konzolparamétert, mielőtt a
tűket GNSS-re használná, miközben a helyi `tty1` konzolt megtartja.
Szándékosan nem engedélyezi és nem képezi át az SPI0-at. A hivatalos
Raspberry Pi SPI1 overlay dokumentálja ezeket a chip select alapértékeket
és paramétereket. Csatlakoztatás vagy feszültség alá helyezés előtt ellenőrizd
az összeszerelt CM5IO-panel ténylegesen létrejött eszközcsomópontjait,
UART-aliasát, GPIO-jogosultságait és minden periféria-visszaolvasást.

A befagyasztott A revíziós szoftvertérkép a
[`hardware/cm5/interface.json`](../../hardware/cm5/interface.json) fájlból a
lemezképen a `/usr/share/bricohams-os/cm5-interface.json` helyre másolódik.
A BCM-leképezés befagyasztott; a segédpanel még nincs megtervezve/gyártva/
kiadva. Az első indítási helyi választó megjeleníti a `gpiodetect` eredményét,
majd a kezelőtől kéri a megfelelő `/dev/gpiochipN` kiválasztását, miután a
`gpioinfo` segítségével összevetette a tényleges vonalakat a CM5IO-térképpel.
Az operációs rendszer szándékosan nem feltételezi, hogy a BCM-vezérlő
`gpiochip0`.

A helyi választó által kiválasztott GPIO-chip után egy systemd biztonságos
állapotot fenntartó szolgáltatás BCM11 watchdog-jelet ALACSONY, BCM12
motor-engedélykérést ALACSONY, BCM13 TCA9548A-resetet MAGAS, a BCM22/23 PTT-
kéréseket pedig ALACSONY szinten tartja. A profil telepítésének befejezése
előtt elindul, és későbbi rendszerindításokkor is fenntartja ezeket a
szinteket. A rádiószolgáltatás csak akkor indulhat, ha ez a szolgáltatás aktív.
Hibánál a szolgáltatás újraindul; a gazda-időnként megismétli az inaktív
kimeneti értékeket. A hibás vagy helyreálló szolgáltató nem bizonyítja a
biztonságot: a független hardveres felhúzásoknak/kapuknak kikapcsolt
állapotba kell hibázniuk. A GPIO-tulajdonlás/helyreállítás vagy
tápvesztés továbbra is külső, alapértelmezetten kikapcsolt felhúzásoktól és
független hardvertől függ; a szoftveres GPIO-inicializálás nem biztonsági
kapu. Az operációs rendszer nem írja az MCP23017 GPA0..GPA2 engedélykimeneteit.
Az MCP23017 resetkor ezek maradjanak bemenetek a megadott külső felhúzásokkal.

Az operációs rendszer GPIO-térképe: I2C1 BCM2/3; AZ/EL/POL NC-végálláspárok
BCM4/5, 6/7, 8/9; vészleállító kiegészítő monitor BCM10; watchdog-kimenet
BCM11; motor-engedélykérés BCM12; TCA-reset BCM13; UART0 TX/RX BCM14/15;
SPI1 CS2/1/0 BCM16/17/18 és MISO/MOSI/SCLK BCM19/20/21; VHF/UHF PTT-kérés
BCM22/23; meghajtóhibák BCM24/25/26; opcionális GNSS PPS BCM27. A GPIO0/1
(fizikai ID_SD/ID_SC) fenntartott. Az MCP23017 GPA0/1/2 az AZ/EL/POL
engedélykérése, GPA3 a motorengedély visszajelzése, GPA4/5 a PTT
visszajelzése, GPA6/7 a PA-hibáké. Az I2C1 `0x70` című TCA9548A 0/1/2
csatornája az AS5600 enkódereket, a 3. az iránytűt, a 4. az IMU-t szolgálja;
az MCP23017 az I2C1 `0x20` címén található.

Csak a befagyasztott térkép I2C1/SPI1/UART0 interfészei vannak konfigurálva;
a build elutasítja az ütköző SPI/I2C/UART overlayeket vagy paramétereket,
nem próbálja találgatással javítani az elavult beállításokat. Megtartja a
pi-gen hivatalos CM5 `nospi10` overlayét, amely letiltja az SPI0 aliasokat,
nem pedig másik buszt rendel hozzájuk. A GPIO4..10 és 24..27 csak
szoftveresen figyelt bemenet marad; **nem** valósít meg közvetlen hardveres
végállás-leállítást vagy biztonsági besorolású vészleállító/watchdog/EN/PTT
áramkört.

A tápellátás a befagyasztott architektúrát követi: külső, névlegesen 12 V-os
akkumulátor, amely kimarad a teljes állomás 5 kg-os tömegcéljából; a
CM5IO USB-C tápbemenete elkülönül az USB adat-/gazdakapcsolattól; a feltételes,
egyeztetett 5 V/5 A célhoz továbbra is ellenőrizni kell a CM5IO névleges
értékeit és a teljes egyidejű terhelést. Nyers 12 V-ot soha ne vezess a
CM5IO 5 V-os USB-C- vagy 40 tűs bemenetére. Ez a cél nem állítja, hogy
elkészült az átalakító, létrejött a PD-egyeztetés vagy minősített a tápforrás.

Csak a rádiós profilok telepítik a `bluez`, `python3-soapysdr`,
`soapysdr-tools`, `soapysdr-module-lms7` és Debian LimeSuite-eszközöket a
tényleges eszközfelderítéshez. A BricoHams rendszerindítási művelete nem
csomagolja be és nem flasheli/frissíti a Lime FPGA firmware-t; kézi
firmware-művelet előtt vizsgáld meg a telepített csomagközleményeket és a
támogatott hardvereljárást. GNSS-démon nincs úgy konfigurálva, hogy lefoglalja
a GNSS UART-ot. `radio-only` profilban a BCM22/23 PTT-kérés hozzárendelése
befagyasztott, de a démon nem kap GPIO-kéréskapcsolókat. A hozzá tartozó
leválasztott kimenetek, fizikai arm/PTT/független RF-kapuk, PA-visszajelzés és
ellenőrzött felügyeleti szolgáltató nincs megvalósítva/tesztelve. A gazdagép
kézi frekvenciás RX marad, és nem tekinthető üzembe helyezett TX-nek.

A lemezkép nem állít be állomási Wi-Fi hozzáférési pontot, és nem állítja,
hogy a projekt webes felülete offline vezérlőszolgáltatásként települ.
A kezelő az első indításkor helyben választ hálózati beállításokat;
`radio-only` profilban a kézzel indított gazdagép dokumentált titkosított
Bluetooth GATT interfészt és localhost CAT-végpontot tesz elérhetővé.
A rádió API hangátvitele előjeles S16LE, monó, 8000 minta/s PCM; ez nem
jelent HFP/A2DP-t vagy igazolt fizikai audiointerfészt.

## Első indítás és profilválasztás

1. **Alapértelmezett fiók (tulajdonosi döntés):** felhasználó `bricohams`,
   jelszó `Brico123`, a pi-gen hozza létre (`FIRST_USER_NAME`/`FIRST_USER_PASS`,
   az átnevezővarázsló letiltva). Ez **nyilvános, közismert hitelesítő adat**:
   az első bejelentkezéskor változtasd meg a `passwd` paranccsal (az MOTD is
   ezt írja). Az SSH **kikapcsolva** marad (`ENABLE_SSH=0`), amíg meg nem
   változtattad. Ebbe a képbe nincs beépítve Wi-Fi-profil, SSH-kulcs, BlueZ
   partner, rádiótoken, sorozatszám vagy követési adatforrás. A BricoHams
   bannerek (`/etc/motd`, `/etc/issue`, `/etc/issue.net`, SSH-banner) statikus
   fájlok az `os/pi-gen-stage/stage2/99-bricohams/files/etc/` könyvtárban. A
   Raspberry Pi Imager testreszabásával a fiók és a hálózat továbbra is
   lecserélhető.
2. Az upstream elsőfelhasználó-beállítás után a BricoHams-választó elindul
   a helyi `tty1` konzolon. Válassz kifejezett modulprofilt, és jelentkezz be
   a már létrehozott helyi kezelői fiókkal. A profil telepítéséhez internet
   szükséges a Debian- és a rögzített Python-csomagindexhez. Vizsgáld meg a
   `gpiodetect`/`gpioinfo` kimenetét, majd válaszd ki azt a pontos
   `/dev/gpiochipN` eszközt, amely a befagyasztott BCM-vonalakat biztosítja.
   Sikertelen telepítéskor a választó függő jelölőként megőrzi a profilt,
   így az újrapróbálkozás nem kever függőségkészleteket. A
   `/etc/bricohams/profile` csak sikeres telepítés után jön létre. Modul-
   szolgáltatás nem lesz engedélyezve vagy elindítva; a GPIO-térkép
   ellenőrzése után külön biztonságosállapot-fenntartó indul. Sikertelenség
   esetén olvasd el a konzolhibát, állítsd helyre a hálózatot, és indítsd
   újra a rendszert ugyanazzal a választással.
3. A helyi konzolon ellenőrizd az operációs rendszert, a kiválasztott profilt
   és interfészeket:

   ```bash
   cat /etc/os-release
   cat /etc/bricohams/profile
   grep -A8 'BEGIN BRICOHAMS' /boot/firmware/config.txt
   grep -o 'console=[^ ]*' /boot/firmware/cmdline.txt
   ls -l /dev/spidev1.* /dev/i2c-1
   ```

   Az eszközcsomópont-nevek ellenőrzendő elvárások, nem működő busz bizonyítékai.
   Indításkor a lemezkép nem homingolja a motorokat, nem mozgat tengelyt,
   nem billenti a PTT-t, nem kezd adást, és nem flashel firmware-t.
4. `radio-only` profilban helyi BlueZ-eszközökkel párosítsd és bízd meg a
   kívánt vezérlőeszközt. A tényleges `Device1` útvonalat a
   `busctl tree org.bluez /org/bluez` kimenetéből olvasd ki. A két valódi
   Lime-eszközt `portable-sat-radio --discover` vagy `SoapySDRUtil --find`
   paranccsal keresd meg. A felderítés nem igazolja az áteresztést,
   antennacsatlakozást vagy RF-biztonságot.
5. `radio-only` profilban csak nem titkos azonosítókat írj a rádiószolgáltatás
   csoportja által olvasható, root tulajdonú konfigurációba. A konfiguráló
   eszköz ellenőrzi a partner útvonalát, a sorozatszámokat és a támogatott
   hardveres mintavételi tartományt; nem párosít eszközt, nem állít üzembe,
   és nem engedélyez egységet:

   ```bash
   sudo bricohams-radio-config \
     --peer /org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF \
     --vhf-serial ACTUAL_VHF_MINI_SERIAL \
     --uhf-serial ACTUAL_UHF_MINI_SERIAL \
     --hardware-rate 1000000
   ```

   Minden példát helyben felderített értékre cserélj. A szolgáltatás
   rendszerindításkor nincs engedélyezve; a konfiguráló eszköz nem indítja
   el és nem engedélyezi. Véletlenszerűen létrehozott hitelesítési tokenje
   privát jogosultságokkal a `/var/lib/bricohams/radio/token` útvonalon
   tárolódik; csak megbízható kliensnek add át, kezelő által felügyelt helyi
   csatornán. Soha ne tedd ezt a tokent a repositoryba, Wi-Fi-fájlba vagy
   build-artifactbe. Az azonosítók későbbi módosításához állítsd le az
   egységet, a nem titkos JSON-fájlt helyben, `sudoedit` paranccsal módosítsd:

   ```bash
   sudoedit /etc/bricohams/radio-host.json
   sudo chown root:bricohams-radio /etc/bricohams/radio-host.json
   sudo chmod 0640 /etc/bricohams/radio-host.json
   ```

   A szolgáltatás minden indítás előtt ismét ellenőrzi a teljes sémát.
   `STANDALONE_MANUAL` módot használ: nem feltételez GNSS/rotor Dopplert,
   és követésvesztéskor nincs visszaállás. Párosítás és RX-próbapadi
   ellenőrzés után a kezelő kifejezetten indíthatja:
   `sudo systemctl start bricohams-radio.service`; ellenőrizd a naplót és
   az állapotot. Külön jóváhagyott eljárás nélkül rendszerindításkor ne
   engedélyezd. A kézi TX tiltva marad. A BCM22/23 kérőtűk és MCP23017
   visszajelzések kiosztása befagyasztott, de a leválasztott PTT-kimenetek,
   a fizikai arm/PTT és független RF-kapuk, a PA-visszajelző áramkörök, valamint
   az ellenőrzött felügyeleti szolgáltató továbbra is hardveres/kiadási
   blokkolók. A biztonságosállapot-fenntartó mindkét PTT-kérést ALACSONYAN
   tartja.
6. `rotor-only` profilban a szoftvercsomag SDR-függőségek nélkül települ,
   de a gyártási CM5 BSP/`open_adapter` még függőben van: mozgásszolgáltatás
   nem települ és nem indul. `integrated` esetén mindkét csomag települ,
   de a rádió wrapper elutasítja az indítást, és hiányzó követés/rotor-
   integráció esetén nem áll vissza kézi működésre. Az antenna-only építéshez
   nincs OS-profil. Kövesd a fent hivatkozott, külön profilútmutatókat.

## Biztonsági és validálási határ

A banner és busz-overlay nem validálja a panelt. A saját panel dokumentációja
továbbra is megköveteli a független motor-tápmegszakítót, normálisan zárt
végállásokat, vészleállító/watchdog ellenőrzését, a kiválasztott TMC5160
panelbeállításokat, enkóder-/érzékelőkalibrálást, GNSS-validálást,
RF-szűrést/izolációt és mért RF-teszteket. A szoftveres start/stop/status vagy
sikeres SPI-visszaolvasás nem helyettesíti a független hardverbiztonságot.
A projekt nem állítja, hogy az állomás elérte az 5 W tervezési célt, hogy a
CM5 mindkét Lime USB-folyamát tartósan kiszolgálja, vagy hogy a teljes állomás
teljesíti tömegkorlátját.

A rootfs-szakasz hibával leáll, ha mentett Wi-Fi-hitelesítőt, engedélyezett
SSH-kulcsot, SSH-gazdagépkulcsot, rádiókonfigurációt/tokent vagy bootkor
engedélyezett rádióegységet talál. Az upstream `/usr/share/doc` közlemények
megmaradnak; a pi-gen BSD 3-Clause licence is települ a projektközleményekkel.
Harmadik fél firmware-blobot vagy logót nem másolunk a lemezképbe.

## Upstream hivatkozások

- [Raspberry Pi OS- és számítógép-dokumentáció](https://www.raspberrypi.com/documentation/)
- [Raspberry Pi Compute Module dokumentáció](https://www.raspberrypi.com/documentation/computers/compute-module.html)
- [Hivatalos Raspberry Pi pi-gen ARM64/Trixie forrás a rögzített commitnál](https://github.com/RPi-Distro/pi-gen/tree/d346cd53562b3c6b4f94c9155175f814258c456d)
- [Hivatalos Raspberry Pi Linux SPI1 overlay dokumentáció](https://github.com/raspberrypi/linux/blob/4103a989a46196239b830bd07693277e42b8f992/arch/arm/boot/dts/overlays/README)
- [Raspberry Pi CM5IO és segédpanel tűszerződése](CM5-PCB.md)

## Build állapota (olvasd el, mielőtt megbízol egy lemezképben)

A recept, a bannerek és az alapértelmezett fiók csak statikusan ellenőrzöttek
(szintaxis és tárolóteszt). Ebből a receptből a készítési környezetben **nem
készült és nem indult el lemezkép**: nincs Docker-démon, nincs ARM chroot/binfmt,
és a Debian/Raspberry Pi tükrök elérhetetlenek voltak. Építsd az
`os/build-image.sh` szkripttel Linuxon Dockerrel (60 GiB szabad hely), vagy
indítsd a `.github/workflows/build-os.yml` GitHub Actions munkafolyamatot
(kézi indítás). Amíg a lemezkép nem indult el CM5-ön és az itt leírt ellenőrzések
nem futottak le, az operációs rendszer NEM elfogadott.
