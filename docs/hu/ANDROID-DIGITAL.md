# Androidos digitális vétel és előkészített APRS-hang

Az Android-alkalmazás tényleges PD120/PD180 SSTV-kép- és Bell 202
AFSK1200 AX.25/APRS-keretdekódolást tartalmaz, továbbá hívójeltől
hívójelig küldhető APRS-rövid üzenetek összeállítását és helyi Bell 202
hangexportot. Ez opcionális tevékenység, elkülönül a régi rotor
navigációjától és vezetékes protokolljától. A meglévő rotor-BLE-szolgáltatás
kizárólag a rotoré, nem használjuk rádióhangra. A digitális DSP
átvitelfüggetlen. Külön rádiógazdagép-tevékenység valósítja meg a dokumentált
`radio-host/1.0.0` BlueZ GATT-protokollt; nem használja újra a régi rotor
GATT-szolgáltatását, parserét, MTU-ját vagy parancsmodelljét.

Az SSTV-, AFSK/AX.25/APRS-dekóderek, valamint az APRS-üzenet- és
hangkódoló Kotlin DSP-/protokollkomponensek átvitelfüggetlenek; JVM
tesztfixture-okkal, offline importtal és gazdagépről érkező adatfolyam
fogadásával egyaránt használhatók. A fizikai Bluetooth-együttműködési
mérések továbbra is szükségesek, és még nem készültek el.

A tervezett állomásarchitektúra CM5-gazdagép két cserélhető LimeSDR
Minivel, egyidejű VHF/UHF-vétellel és egyszerre legfeljebb egy adóval.
ESP32-es audiohíd nem része a tervnek. A tároló most már tartalmazza a
mérvadó Linux/BlueZ `radio-host/1.0.0` szerződést; a dedikált Android
rádiótevékenységnek a Linux-forrás a mérvadó. Az alkalmazás megvalósítja a
párosított eszköz kiválasztását, tokenes hitelesítést, verzió-/állapot-
feldolgozást, explicit VHF/UHF RX/TX-csatorna-hozzárendelést, tényleges
MTU-egyeztetést, kétirányú 8 kHz-es PCM-et, folytonosság-ellenőrzést,
abszolút TX-jóváírásokat, FM/AM/USB-hangolást, explicit önálló kézi módú
megerősítést, host-polarizációs képességválasztást, hang-lejátszást,
élő mikrofonos adást és APRS-hangküldést. A TX-gomb tiltva marad, amíg a
hang nem kész, nincs kiválasztva az alkalmazás helyi élesítési megerősítése,
és a legfeljebb két másodperces hostállapot nem jelzi a kiválasztott TX-
csatornát és a szükséges host-reteszeket. Az elavult állapot letiltja a TX-et,
amíg a felhasználó friss állapotot nem kér. A kiválasztott profil VHF/UHF
sávjain kívüli profil-visszaolvasást az alkalmazás elutasítja.

A megvalósítás **nem** igazolja a fizikai BlueZ-kapcsolatot, a kísérő
számítógépet, a LimeSDR-t, az RF-utat, az antennát, a jogszerűséget vagy
engedélyt, a meghajtási szinteket, illetve a rádiós vételt/adást. Ezt a
szolgáltatást tartsd külön az opcionális régi rotorvezérléstől. A befagyasztott
rotorállapot-parser és protokoll változatlan marad. Nem kerül ide helyi
SGP4-előrejelzés vagy kitalált rádió-/rotor-API.

A külön rádiógazdagép-tevékenység orbitális panelje csak hitelesített host
v1-kéréseket és tényleges `cm5-rotor/v1` válaszokat használ. Elérhető:
GET `/rotor/status`, GET `/rotor/sensorsstatus`, GET `/satellites/catalog`,
GET `/satellites/passes` (`noradId`, opcionális `limit`), SET `/rotor/track`
(`noradId`), SET `/rotor/target` (mindhárom véges `azDeg`, `elDeg`, `polDeg`),
valamint SET `/rotor/stop`. A sikeres válaszban `schema`, `ok:true` és
objektum típusú `data` szükséges; a hiba válaszában explicit `ok:false` és
nem üres `error` kell, amelyet a kezelőfelület megjelenít. A nem támogatott
vagy eltérő útvonalak, műveletek, payloadok és sémák hibával zárulnak,
nem jelennek meg sikeresnek. Távoli `/rotor/home` és `/rotor/calibrate`
nincs kitéve: a CM5-vezérlő ezekhez megbízható helyi konzolos megerősítést
igényel.

A host válaszait az Android visszakapott JSON-ként mutatja; nem talál ki
orbitális pillanatképet, nem értelmezi át az ismeretlen katalógus-/átvonulási
mezőket, nem terjeszt TLE-t, és a parancs elfogadásából nem állítja, hogy a
célállás létrejött. Az `OrbitSnapshotJson` csak javasolt modell, nem host-
válaszséma. A térkép, radar, részletes átvonulás-megjelenítés,
rádióprofilok és mért/kért tengely-pillanatkép nem érhető el, amíg a host
nem tesz közzé ellenőrzött válaszmodellt és az alkalmazás nem kapcsolódik
hozzá. A rotorútvonalak különállnak a rádióhost `/status` útvonalától; a
csak helyi `integration_snapshot()` nem Android-végpont.

**A hostnak küldött PCM nem igazolt rádióadás.** Az összeállított csomagok
továbbra is exportálhatók offline WAV-ként. A külön rádióképernyő csak friss
állapot, helyi megerősítés, host által jelzett fizikai ARM/PTT-bemenet és
RF-reteszek, audio-jóváírások, valamint rövid PTT-bérlet sikeres ellenőrzése
után küld PCM-et a hitelesített hostnak. A bérletet befejezéskor, leállításkor,
hibánál, háttérbe lépéskor, időtúllépéskor vagy kapcsolatvesztéskor elengedi.
A host PCM- vagy PTT-kérésének elfogadása nem bizonyít RF-kimenetet,
rádiós vételt, APRS-kézbesítést vagy ACK-t. Nincs automatikus
hangszóró-lejátszású PTT, A2DP/HFP digitálisrádió-átvitel,
APRS-IS-/mobil-SMS-átjáró, titkosítás vagy beégetett digipeater-útvonal.

A host `physicalArm` és `physicalPtt` mezői fizikai bemeneti jelzéseket
írnak le; a `physicalPtt` **nem** erősíti meg a független GPIO-s PTT-kimenet
visszajelzését. A Linux-host a magas aktív PTT-kéréseket független,
alacsony aktív MCP23017 GPA4/GPA5 visszajelző bemenetekkel és GPA6/GPA7
hibabemenetekkel ellenőrzi, mielőtt bérletet ad vagy tart fenn. Az Android
ezeket a GPIO-visszajelző lábakat nem kapja meg külön `/status` mezőként:
PCM-adatfolyam csak host-bérlet elfogadása után indul, az elutasítás pedig
biztonságosan leáll. Ez sem bizonyíték RF-kimenetre vagy rádiós adásra.

## Külön rádiógazdagép-hang

A főképernyőről nyisd meg a **Separate radio host** nézetet. Kizárólag
kifejezetten kiválasztott, már párosított BLE-hosthoz csatlakozz. A
felhasználó kapcsolatkor adja meg a titkos, 64 hexadecimális karakteres
tokent; az alkalmazás nem tárolja és nem naplózza. A BlueZ-nek hitelesített,
védett jellemzőket használó biztonságos párosítást kell megkövetelnie;
az Androidon párosított állapot önmagában nem bizonyít MITM-védelmet. A
hostoldali hitelesítés, protokollverzió és biztonsági szabályzat az irányadó.

A rádiószolgáltatás elkülönül a rotorszolgáltatástól; a
`docs/RADIO-HOST.md` befagyasztott szerződését használja: UUID
`c8201001-4e53-4253-9000-000000000001`; host→Android vezérlési notify/read
`c8201002-4e53-4253-9000-000000000001`; Android→host vezérlési
write-with-response `c8201003-4e53-4253-9000-000000000001`; host→Android
PCM notify `c8201004-4e53-4253-9000-000000000001`; Android→host PCM
write-with-response `c8201005-4e53-4253-9000-000000000001`. Az Android
feliratkozik/hitelesít, feldolgozza az aktuális állapotot, feliratkozik a
hangra, majd csak felhasználó által indított adatfolyam előtt egyeztet
tényleges, legalább 247-es ATT MTU-t.

A PCM mono S16LE, 8000 minta/másodperc, 16 bájtos little-endian
verzió/flag/stream/sorozatszám/mintaindex-fejléccel; MTU 247 mellett
csomagonként legfeljebb 114 mintával. Az alkalmazás megköveteli a rendezett
sorozat-/mintaszámlálókat és a kiválasztott streamazonosítót; hibás,
elavult vagy folytonossághiányos keret leállítja a hangot és érvényteleníti
a felvételt. Hiányzó mintákat soha nem pótol. Minden hangindítás explicit
RX/TX-csatornamezőket igényel. A jelenlegi két-Lime-összeállításnál ez
ellentétes sávú VHF/UHF-választást jelent, soha nem azonos csatornát vagy
kevert folyamot. Az egy rádiót használó önálló konfiguráció ugyanazt az
egyetlen csatornát fogadja RX-re és TX-re.

A hostállapot-kijelző profilként mutatja a sorozatszámot, tényleges
RX/TX-frekvenciát és mintavételi sebesség-visszaolvasást, RX-olvasásszámot,
sormélységet és hibát. A host 1 MSPS SDR-hardversebessége/visszaolvasása
elkülönül a 96 kSPS belső komplex DSP-alapsávtól és a 8 kSPS BLE-hangfolyamtól.
Ezek közölt/konfigurációs értékek, nem bizonyítják a LimeSDR fizikai
alkalmazását vagy RF-működését. Explicit indítás előtt nincs hangátvitel;
az üzemeltetési profil, tényleges csatorna és sáv ellenőrzése továbbra is
a host feladata.

A vételi felvétel legfeljebb 240 másodperc és 1 920 000 S16-minta
(körülbelül 3,7 MiB), utána leáll és dekódol. A leállítás/dekódolás előbb
a host hangját és minden aktív TX-bérletet is megszüntet. A digitális
dekóderhez a felhasználónak ki kell választania a PD120, PD180 vagy
AX.25/APRS módot. Az opcionális hangmonitor kifejezett Android-lejátszás
a host dekódolt PCM-jéből; 16 csomagos sora van, sorvesztéskor leáll,
nem próbálja elfedni a veszteséget, és nem engedélyezhet PTT-t. Az Android
lejátszása nem jelenik meg átlátszó A2DP/HFP hangkapcsolatként.

Hangadáskor a felhasználó választ a beépített/USB/vezetékes bemenetekből,
és explicit `RECORD_AUDIO` engedély szükséges; a Bluetooth rendszer-
mikrofonbemenetek ki vannak zárva. A beépített mikrofon hangszóró/
környezeti hangot vesz, **nem RF-et**. A PCM a rögzítés szerint (nem
felvételként tárolva vagy hangszórón lejátszva) a hostnak streamelődik,
legfeljebb 240 másodpercig, és leáll, ha sor/jóváírás/írás/állapot/retesz/
bérlet-ellenőrzés hibázik. Az élő APRS-adás az alkalmazás AX.25 UI/FCS/
HDLC bit stuffing/NRZI/Bell 202 kódolóját és ugyanezt a reteszelt PCM-
folyamot használja. A felhasználó beállítja a hívójelet, címzettet,
opcionális explicit digipeater-útvonalat és üzenetazonosítót, megerősíti
a titkosítatlan, jogszerű tartalmat, majd kifejezetten elfogadja a host
bérlet-/küldés párbeszédablakát. APRS-hez a host által jelzett FM szükséges.
A felület csak azt állítja, hogy a **host elfogadta a PCM-et**; a vett
ACK/rej-t nem párosítja helyi üzenettel és nem állít kézbesítést.

Az SAF WAV-export külön, offline előkészített hullámforma, nem hostnak
küldés. Ne játszd rádiómikrofonba, ne használj hangvezérelt PTT-t, és ne
feltételezd, hogy az exportált vagy host által elfogadott PCM adásra került.
Biztonságos RF-próbapadi ellenőrzéshez az engedélyezett helyi amatőrrádiós
szabályokat, host-hardverdokumentációt, valamint minősített műterhelési/
leválasztási eljárásokat kell külön követni.

## Audioforrás kiválasztása és csatlakoztatása

Nyisd meg a meglévő alkalmazás képernyőjéről a **Digital receive · SSTV /
APRS** nézetet. Az Activity felsorolja az Android által jelzett
audio-bemeneteket, és USB-audio-bemenetet választ elsőként, ha van; egyébként
a beépített mikrofont, vagy az elsőként jelentett bemenetet választja. A
felhasználó módosíthatja a választást és frissítheti a listát. A kiválasztott
Android-bemenet útvonalát kifejezetten az `AudioRecord.setPreferredDevice`
állítja be; ha az útvonal ténylegesen nem aktív, a rögzítés látható hibával
áll le ahelyett, hogy csendben mikrofonra váltana.

Közvetlen vételi audióhoz használj leválasztott, megfelelően csillapított
USB-audio interfészt a rádió/vevő audio-kimenetéhez csatlakoztatva.
Csatlakoztatás előtt ellenőrizd a rádió és az interfész specifikációját, és
alakíts ki biztonságos, leválasztott kapcsolatot. Hangszórószintű kimenetet
ne csatlakoztass közvetlenül telefonbemenetre, hacsak az adott interfész erre
nincs méretezve. A telefon beépített mikrofonja a vevő hangszóróját vagy a
környezeti hangot hallja: **nem RF-vevő**, és szobazaj, AGC és visszhang
befolyásolja. Egyik audio-bemenet sem vesz vagy hangol RF-et. Külön vevő/
rádió és antenna szükséges.

Az élő rögzítés explicit gombbal indul, majd tájékoztató és az Android
`RECORD_AUDIO` engedélykérése következik. A felvétel csak az előtérben
látható Activity-ben történik, és leáll, ha a felhasználó a **Stop and
decode** lehetőséget választja, elnavigál, az audio-bemenet hibázik, vagy
eléri a szigorú 240 másodperces korlátot. 48 kHz-en a 16 bites mono audió
fenntartott memóriája legfeljebb kb. 23 MiB; a feldolgozást ugyanaz a
háttérmunkás végzi. A képernyő elhagyásakor a befejezetlen felvétel leáll és
eldobódik. Nem kerül be háttérszolgáltatás, felhőfeltöltés, audio-telemetria,
PTT, rádió-CAT-művelet vagy telefon-helyadat-hozzáférés.

Az Android Bluetooth SCO/headset rendszer-audio-végpontot is felsorolhat.
Ez hagyományos Android-profilú hang; az alkalmazás nem állítja, hogy az
A2DP/HFP átlátszó, kis késleltetésű, kétirányú PCM-kapcsolatot ad hanghoz és
AFSK/SSTV-hez. **A digitális rádióhoz készült, dedikált Bluetooth-hang még
nincs megvalósítva.** Ehhez mérvadó, külön befagyasztott GATT-hangszolgáltatási
vezetékspecifikáció és azzal egyező kísérő firmware kell, még bármilyen
Bluetooth-kapcsolati felület vagy átvitel megvalósítása előtt. A meglévő
rotor BLE-szolgáltatás/MTU-viselkedés érintetlen marad. A belső PCM
forrás-/nyelő interfészek átviteli módtól független illesztési pontot adnak
egy későbbi adapter számára.

## Helyi fájlbemenet és export

Az **Import PCM WAV** az Android Storage Access Framework dokumentumválasztóját
használja. A dekóder kizárólag RIFF/WAVE lineáris PCM-et (1-es formátumjelölő),
8/16/24/32 bites little-endian mintákat, 1 vagy 2 összefűzött csatornát és
8000–48000 Hz mintavételt olvas. A sztereó csatornákat mono jellé átlagolja.
A WAV legfeljebb 50 MiB és 240 másodperc lehet, az újramintavételezés előtt
is; a nem támogatott/tömörített WAV, hibás chunkok, csonka adat és tartományon
kívüli audio kifejezett hibát ad. Az olvasó ablakolt szinc aluláteresztő
szűrővel 11025 Hz-re mintavételez újra, majd FM-demodulál. Az exportált AFSK
hang mono, előjeles, 16 bites little-endian PCM, 8000 minta/s; megőrzi az
1200/2200 Hz-es Bell 202 hangokat, importkor ugyanazon vételi útvonalon
mintavételeződik újra. Float WAV,
IEEE-float WAV, tömörített WAV, WAVE extensible formátum és nem WAV-bemenet
nem támogatott.

A `PcmSource`/`PcmSink` interfészek korlátozott méretű blokkokban adnak át
mono, előjeles 16 bites mintákat. Minden blokk monoton növekvő sorszámot és
elsőmintaszámlálót tartalmaz; a gyűjtés és a WAV-írás hézag észlelésekor
elutasít, nem tölt ki vagy rejt el hiányzó audio-adatot. Jelenlegi adapterek
az Android `AudioRecord` rögzítése, valamint a korlátozott helyi PCM/WAV
import/export. Ezek a metaadatok belső folytonossági szerződést jelentenek,
**nem** javasolt Bluetooth GATT-vezetékformátumot; a Bluetooth-keretezés,
sorszámszélesség és mintaszámláló szemantikája a szülői projekt mérvadó
átviteli specifikációjára vár.

A sikeres SSTV-kimenet eredeti, 640 × 496 képpontos méretben jelenik meg, és
PNG-ként menthető az SAF dokumentumválasztójával. A sikeresen dekódolt
AX.25-keretek ugyanígy UTF-8 szövegként menthetők. A napló tartalmazza a
forrás/cél/útvonal, keretvezérlési információkat és az olvasható APRS-
értelmezést; kizárólag az AX.25 FCS-ellenőrzésen átment kereteket sorolja
fel. A naplók csak helyiek; tényleges célhelyüket és megőrzésüket a
felhasználó választja.

## Megvalósított jel- és keretformátumok

### PD120 és PD180 SSTV

A kiválasztott demodulátor 31 csapos ablakolt Hilbert-féle analitikus jelet és
mintáról mintára számított kvadratúra-fáziskülönbséget használ az audio
pillanatnyi frekvenciájának (FM) visszanyerésére. Felismeri az analóg SSTV-
fejlécet (két, egyenként 300 ms-os, 1900 Hz-es vezető, közöttük 10 ms
1200 Hz-en), majd dekódolja a 30 ms-os VIS kezdő/adat/paritás/leállító
szimbólumokat. A VIS adatbitjei alacsonytól magas felé olvasva: 1100 Hz = 1,
1300 Hz = 0; a paritást ellenőrzi, és csak a VIS `0x5f` PD120-at és `0x60`
PD180-at fogadja el. A kifejezetten kiválasztott módnak egyeznie kell a
dekódolt VIS-szel.

A képdekóder a két mód soridőit használja (PD120 komponens-szkennelés
121,6 ms; PD180 183,04 ms), soronként 20 ms 1200 Hz-es vízszintes
szinkronnal és 2,08 ms 1500 Hz-es porch-csal. Minden sor szinkronját és
porch-át ellenőrzi. Egy továbbított sorcsoport 640 mintát tartalmaz Y0,
Cr (R−Y), Cb (B−Y) és Y1 komponensekhez; a közös 4:2:0 színkülönbség-
információt a szomszédos Y-sorokra terjeszti ki, majd RGB-vé alakítja.
Az eredmény a teljes, 640 × 496 képpontos kép. Hiányzó sor/szinkron, hibás
VIS/paritás, rossz mód, rövid adat, csend vagy a támogatott komponens-
frekvenciatartományon kívüli jel esetén hiba keletkezik, nem részleges vagy
mesterségesen kitöltött kép. A fejléceknek a dekóder durva igazításához
képest 5 ms-on belül kell lenniük, az összetett soridő pedig a névleges
szabványt követi; nagy órajel-eltérés, az adó szinkronjának ingadozása,
szélsőséges zaj és súlyos fading elutasítást okozhat.

### Bell 202 AFSK1200 / AX.25 / APRS

Az AFSK-vevő ugyanazt a mért FM-audio-frekvenciát használja, 1200
szimbólum/másodperc sebességgel, a szimbólum közepén mintavételezve, és
felismeri a Bell 202 1200 Hz-es mark, illetve 2200 Hz-es space hangokat.
NRZI-t dekódol (nincs átmenet = egyes, átmenet = nulla), felismeri a `0x7e`
HDLC-flaget, öt egymást követő adat-1 után eltávolítja a beszúrt nullát,
LSB-első bájtokat állít össze, és 512 bájtra korlátozza a keretet. Feldolgozza
az AX.25 cél-, forrás- és legfeljebb nyolc digipeater-címet, SSID-ket és az
ismétlődő flag-eket; UI- és nem-UI vezérlő/PID-csomagokat is naplóz.
Keret csak akkor jelenik meg, ha little-endian AX.25 FCS-e átmegy a CRC-16/
X.25 ellenőrzésen (tükrözött polinom `0x8408`, kezdeti/végső XOR `0xffff`).
Ugyanazon felvétel ismétlődő, érvényes keretei csak egyszer jelennek meg.
Érvényes keret nélküli felvétel hibát jelent; hibás CRC-t soha nem címkéz
csomagnak.

Az olvasható, `0xf0` PID-es APRS UI-csomagokat APRS-szövegként értelmezi.
A megvalósított megjelenítések: tömörítetlen `!`/`=` pozíciók, időbélyeges
`/`/`@` pozíciók, `:` üzenetek és `>` állapotok/lekérdezések, továbbá szükség
szerint az eredeti olvasható payload. A szabványos `DDMM.hhN`/`DDDMM.hhE`
koordinátákat ellenőrzi, és előjeles decimális fokban mutatja. Más olvasható
APRS-tartalom szöveg marad; a tömörített/base-91 pozíciók, Mic-E, telemetria,
objektum-/elem-specifikus szemantika, az alap AX.25-címreprezentáción túli
címzettek/útvonalak és a nem-UI/APRS alkalmazási payloadok nem kerülnek így
dekódolásra. Az olvashatatlan alkalmazási payload bájtjait a UI nem kódolja
base64-be; a szövegnapló jelzi, hogy e payload nem jelent meg.

### APRS rövid üzenetek és előkészített hang

Az üzenetűrlap hívójeltől hívójelig menő APRS-rádióüzenetet készít (nem
mobil-SMS-t és nem APRS-IS/internet-átjárót). Érvényes állomáshívójel és
SSID szükséges. A bejövő APRS-üzeneteket, `ack` és `rej` válaszokat az
APRS-címzettel és az opcionális, 1–5 karakteres üzenetazonosítóval elemzi.
A bejövő lista a helyes FCS-ű vételi keretek közül a pontosan konfigurált
hívójel–SSID pároshoz szűr, és csak az oda címzett üzeneteket mutatja. A
lista az aktuálisan dekódolt felvételre/fájlra korlátozódik, nem tartós
tároló. A vett `ack`/`rej` fogadott protokollszövegként jelenik meg; **soha
nem kapcsolódik össze egy helyben előkészített/exportált WAV-val**, és nem
módosít elküldött/kézbesített állapotot.

Üzenet összeállításakor add meg a forrás- és célhívójel–SSID-t, 1–67
nyomtatható ASCII üzenetkaraktert, opcionális 1–5 alfanumerikus
üzenetazonosítót, valamint opcionális, kifejezetten megadott, vesszővel
elválasztott digipeater-útvonalat (legfeljebb nyolc érvényes hívójel).
Üres útvonal megengedett; univerzális/alapértelmezett útvonalat nem illeszt
be automatikusan. A felhasználónak kifejezetten nyilatkoznia kell, hogy a
tartalom jogszerű, titkosítatlan amatőrrádiós szöveg. Ez nem tartalom-
ellenőrzés, titkosításfelismerés, engedélyellenőrzés vagy adási engedély.
Az alkalmazás nem titkosít szöveget, és nem ad mezőt titkosított RF-tartalom
létrehozására.

Az előkészítés AX.25 UI-keretet hoz létre `APRS` APRS-célazonosítóval,
`0xf0` PID-del, felhasználói APRS-címzettel/üzenettel/üzenetazonosítóval,
opcionális konfigurált digipeaterekkel, számított X.25 FCS-sel,
HDLC-flag-ekkel/bit stuffinggal és NRZI-kódolással. Ezután folyamatos fázisú
Bell 202, 1200/2200 Hz-es hangot és mono, 8000 Hz-es, előjeles, 16 bites
PCM RIFF/WAVE fájlt készít az SAF fájlválasztóján keresztül. A WAV elején és
végén csend van, továbbá rögzített flag-előtagot/-utótagot tartalmaz.
**Az exportált hang csak előkészített moduláció, nem elküldött csomag.**
Nem indul automatikusan lejátszás, nincs PTT-kapcsolata, nincs RF-nyugtaút,
és a hangot nem szabad rádiómikrofonra vagy hangvezérelt PTT kiváltására
lejátszani.

Az élő rádiógazdagép-munkafolyamat a külön, hitelesített BLE-hangszolgáltatáson
át képes APRS PCM-et továbbítani, helyi megerősítéshez, friss hostállapothoz,
host ARM/PTT- és RF-reteszekhez, jóváírásokhoz, valamint rövid PTT-bérlethez
kötve. Ez szoftveres út a hosthoz, **nem igazolt RF-adás**; egyetlen
host-elfogadás sem jelenik meg továbbítottként, vettként vagy kézbesítettként.
Az SAF-exportált WAV továbbra is offline-only: nem indul el automatikusan,
és nem küldődik el. Külső próbapadi munkafolyamat nem jelent integrációt vagy
működő RF-utat: ha megfelelő engedéllyel rendelkező kezelő önállóan teszteli
az exportált hangot, a rádió dokumentált kiegészítő/adatbemenetét használja
megfelelően minősített galvanikus leválasztáson és csillapításon keresztül,
teljesítményre méretezett műterhelésre (nem antennára), engedélyezett
tesztfrekvencián/-módban, külön kezelt fizikai PTT-vel. Kezdd biztonságosan
alacsony szinten, független vételi/mérőberendezéssel ellenőrizd a
hullámformát és modulációt a műterhelésen, a PTT-t pedig kézzel engedd el.
Hangszórószintű kimenetet soha ne csatlakoztass közvetlenül; ne vezess
jelet a mikrofonon vagy hangvezérelt PTT-n át, és a WAV-exportot ne
tekintsd adási felhatalmazásnak.

### Korlátozott feldolgozás és látható hibák

Az élő és importált audio ugyanazon PCM-normalizálón és demodulátoron halad
át. A felvétel szigorú felső határa 240 másodperc; korlátozott a mintavételi
frekvencia, a PCM-formátum, a WAV/RIFF chunkméret, az AX.25-kerethossz és a
dekóder megszakítása. Minden művelethez ki kell választani a kívánt módot.
Nem támogatott bemenet, CRC-/paritáshiba, hiányzó keret/fejléc,
képszinkron-hiány, hibás mintaszint, elavult/megszakított UI-feladat vagy
SAF-hiba nem eredményez sikeresnek látszó alapértelmezett kimenetet. A
vételi képernyő bezárásakor az aktív rögzítő leáll/felszabadul, a dekódolás
és a dokumentum-I/O megszakad.

E korlátok a szokásos memória- és feldolgozási igényt határolják, de a
prototípus nem esett át ellenséges parser-bemeneteket vagy eszközöket
vizsgáló fuzz-teszten. Nem hitelesíti a vett rádióadat eredetét; a dekódolt
csomagot ne kezeld megbízható parancsként vagy biztonsági bizonyítékként.

## Reprodukálható JVM-ellenőrzés

Az összes Kotlin-szintetikus fixture végponttól végpontig teszteli a dekódert
SDR, rádió, RF-adás vagy külső dekóder nélkül:

- Hilbert-/fáziskülönbséges FM-demoduláció 1200, 1500, 1900 és 2300 Hz-en.
- Teljes hosszúságú szintetikus PD120 (`0x5f`) és PD180 (`0x60`) fejlécek,
  VIS-paritás, mind a 248 külön szinkronnal ellenőrzött összetett sor, Y/Cr/Cb/Y
  képpont-összeállítás.
- Véletlen PCM-adatnál jel hiányának elutasítása, hibás VIS-paritás és
  kiválasztott mód eltérésének elutasítása.
- WAV PCM-beolvasás és hibás/tömörített bemenet elutasítása.
- AX.25 `123456789` X.25 CRC-ellenőrzés `0x906e`; ellenőrzött, ismert APRS-
  pozíciókeret függetlenül számolt little-endian FCS-sel; AFSK-hangok,
  bit stuffing, NRZI, HDLC-flag-ek, elemzett címek, APRS-pozíció, valamint
  érvényes/hibás CRC és véletlen zaj elutasítása.
- APRS-üzenettörzs/címzett/azonosító és ACK/rej elemzése, hívójel-/útvonal-/
  üzenethatárok, konfigurált állomás szerinti bejövőszűrés, valamint
  végponttól végpontig tartó körút az összeállított UI-kerettől az FCS-en,
  HDLC-bit stuffingon/NRZI-n, Bell 202 8000 Hz S16LE PCM-en és WAV-exporton
  át a WAV-importon/újramintavételezésen keresztül AX.25/APRS-dekódolásig.
- PCM-forrás/-nyelő másolás, 8000 Hz-es mono S16LE WAV import/export,
  pontos mintamegőrzés, valamint a sorszám-/mintaszámláló-hézagok kifejezett
  elutasítása.
- CM5 `cm5-rotor/v1` keret- és kérésútvonal-ellenőrzés az Androidban
  kivezetett hét távoli művelethez, beleértve a szigorú target/track/passes
  payloadokat, explicit hosthibákat, valamint a kizárólag helyi konzolról
  elérhető homing/kalibrálási műveletek elutasítását.

Az `android` mappából futtasd a teszteket, az összes Android JVM-tesztet,
a lintet és az alkalmazás buildjét a tároló elkülönített `.tools` JDK/SDK-
jával és Gradle-cache-ével:

```powershell
$env:JAVA_HOME = (Resolve-Path .tools\jdk\jdk-17.0.16+8).Path
$env:GRADLE_USER_HOME = (Resolve-Path .tools\gradle).Path
$env:ANDROID_HOME = (Resolve-Path .tools\sdk).Path
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat --no-daemon :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
```

A sikeres szintetikus teszt a determinisztikus DSP-/protokoll-fixture
viselkedést igazolja, **nem** RF-vevő kompatibilitást, alkalmazásindítási/
megjelenítési tesztet, adott telefonon működő élő audio-útvonalat, vagy
működő ISS/adó vételét. Terepi használat előtt mindezt a támogatott
Android-telefonokon, a pontosan bekötött vevővel és referenciarögzítésekkel
ellenőrizd.

## Igazolt hibakeresési buildtermék

Az ehhez a változtatáshoz ellenőrzött debug APK (a helyi Android debug
kulccsal aláírva; ez nem release/terjesztési aláírás):

- `android/app/build/outputs/apk/debug/app-debug.apk`
- Méret: 1 208 309 bájt.
- SHA-256: `ED52E0881353D7542DDA1FAC5062B372E2EA4BB8489710EDC98386ECF5A77DD7`
- Az APK Signature Scheme v2 ellenőrzése sikeres.
- Aláíró: helyi Android debug-kulcs, a tanúsítvány SHA-256-a
  `c7ca5c0533cd3db2d189c5e3402042c1d2e565bde2f49264501190e17154ed7b`.
- Ellenőrzési futás: mind az 58 Android JVM-teszt hiba és bukás nélkül
  sikeres; a `lintDebug` és az `assembleDebug` is sikeres. Az APK v2
  aláírás-ellenőrzése sikerült. A lint 33 figyelmeztetést és nulla hibát
  jelent, többek között orbitális UI-fordítási és rajzolás közbeni
  allokációs figyelmeztetéseket.

## Elsődleges specifikációk és hivatkozások

- Martin Emmerson, *Image Communication on Short Waves* (ingyenes angol
  fordítás, az SSTV szabványelméletével és mód-táblázataival):
  [SSTV Handbook](https://www.sstv-handbook.com/).
- Martin Emmerson, *Image Communication on Short Waves*, tartalom és
  letöltések (2019-es kiadás):
  [a szerző letöltési oldala](https://www.sstv-handbook.com/download/sstv-handbook.pdf).
- N7CXI módjából származtatott, látható forrású PD hullámforma-paraméterek
  és szkennelsor-elrendezés (reprodukálható, implementációk közti
  ellenőrzéshez; az alkalmazáskódba nem építettük be/másoltuk):
  [pdSSTV JS móddefiníciók](https://github.com/pefech/js-sstv/blob/3b2e296677420f6543021ca1a19e469174ab32de/src/sstv/modes.js).
- Független, nyílt SSTV-vevő mód-táblázata (PD VIS-kódok, komponens-idő,
  sorgeometria, 640 × 496 sor):
  [QSSTV módparaméter-táblázat](https://github.com/ON4QZ/QSSTV/blob/8c27d6d169d8c6c197eb47b2089870e39bc06a02/src/sstv/sstvparam.cpp).
- TAPR, *AX.25 Amateur Packet-Radio Link-Layer Protocol, Version 2.2*:
  HDLC-flag-ek, bit stuffing, cím/vezérlő/információs mezők és FCS.
  A TAPR kiadvány-végpont a feladat során 404-et adott; a nyomon
  követhetőség kedvéért a forrás itt marad:
  [TAPR AX.25-kiadványok](https://www.tapr.org/published.html).
- APRS Working Group, *APRS Protocol Reference, Version 1.0.1*. Az eredeti
  APRS.org PDF-végpont a feladat során megtagadta az automatikus letöltést;
  emberi ellenőrzéshez itt a hivatkozás:
  [APRS101 specifikáció](https://www.aprs.org/doc/APRS101.PDF).

Az eredeti dekóder Kotlinban, ehhez az alkalmazáshoz készült; a harmadik
féltől származó SSTV-hivatkozások kizárólag az interoperábilis formátum- és
időzítési tényekhez adtak hátteret. Külső dekódercsomag vagy korlátozott/
GPL-implementáció nincs beágyazva.
