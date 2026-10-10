# Harmadik tengely: POL mechanikai koncepció

## Hatókör és állapot

Ez az eredeti, korlátozott úton mozgó gördülő fokozat a meglévő két tengelyes
BASE-hez. A meglévő antennanyerget az antenna iránytengelye körül forgatja.
Nem cseréli le vagy módosítja egyik meglévő AZ/EL-áttételt, firmware-t,
PCB-t vagy azok exportját sem. A harmadik fokozat egy GT2-szíj-áttételt
használ; nem a kétfokozatú, 25:1 AZ/EL-hajtás másolata.

**Csak koncepció; nincs kiadva vagy terhelésre minősítve.** A CAD/STL-
ellenőrzés a geometriát és a háló zártságát validálja, nem a feszültséget,
holtjátékot, RF-teljesítményt, terhelés alatti ütközéseket, kapcsoló-
időzítést, pontosságot vagy biztonságos működést. A motort, szíjat,
csapágyakat, fém tengelyt, ütköző hardvert, kapcsolót, RF-hálózatot és
kábelt pontosan be kell szerezni, illeszkedésüket ellenőrizni és tesztelni.
A rajz alapján ne adj és ne szereld fel kültérre.

## Mechanikai rétegrend és csatlakozások

A `cad/polarization_station.scad` a POL-fokozatot az eredeti BASE
`output_flange()` elemére illeszti, és az eredeti `saddle(20)` elemet
csatlakoztatja úgy, hogy egyik segédfüggvényt sem módosítja. Az alaplap a
meglévő 60 mm-es kimeneti karimához csatlakozik: négy 4,5 mm-es
átmenőfurat 44 mm-es osztókörön (31,11 mm-es négyzet), valamint középen
22 mm-es nyereghézag. A levehető boombilincs ugyanaz a 20 mm furatú
alkatrész marad; a négy nyeregrögzítő csavar hozzáférhető.

A nyereg origója a POL-hordozó csavarmintájához igazodik; az eredeti nyeregfurat eltolását (+35 mm Y, +24 mm Z) kifejezetten a POL csapágy-/tengelytengelyéhez kell illeszteni ugyanott (+35,+24 mm). Így az eredeti boom/antenna középvonala marad meg, nem a nyereg CAD-origóját tekintjük a bilincs furatának.

Két 608-as csapágy (8 × 22 × 7 mm), 48 mm-es tengelytávval, 8 mm külső
átmérőjű üreges fém tengelyt tart az antenna tengelyében. A kezdeti
tengelyburkoló méret: 8 mm külső átmérő, 5 mm belső átmérő, 96 mm hossz.
A furat csak egy kis hajlékony koaxnak való; csatlakozó nem haladhat át
rajta. A tényleges tengely anyagát, falvastagságát, koncentrikusságát,
csapágyüléseit, axiális rögzítését és merevségét válaszd ki és vizsgáld
meg. A teherviselő tengelyt ne nyomtasd ASA-ból. A csapágyülés hézaga és
rögzítő illeszkedése előzetes; a teljes keret gyártása előtt nyomtass
próbadarabot.

A NEMA14/tárcsa burkolómérete a meglévő motorhomlok- és 26 mm-es
rögzítőfurat-feltételezéseket használja. A 3 mm-es motorlap-DXF sablon,
nem ellenőrzött vágófájl: a kiválasztott motor központosító vállát,
csavarmintáját, tengelyét, homlokát, kábelkivezetését és tárcsaagyát
ellenőrizd a gyártói rajz alapján. A páros oldallap-DXF 90 × 64 mm-es
sablon, csapágy-, rögzítő-, összekötőrúd-, kapcsoló/ütköző- és motorlap-
furatokkal. Az összeállítás négy, 3 mm-es távtartó helyét mutatja az
oldallap-merevítés és a motorlap között. Két radiális hernyócsavar rögzíti
a forgó hordozót az üreges tengelyhez; a csavar hosszát és meghúzási
nyomatékát úgy állítsd be, hogy a csőbe kapaszkodjon, de ne üssön át a
koaxfuratba. A külön hasított bilincsbütyök M3-as rögzítőt használ; annak
zárását és rezgésállóságát is igazolni kell. A rajz méretei és anyaga nincs
megmunkálva vagy szerkezetileg ellenőrizve. Beépítés előtt sorjátlanítsd
és ellenőrizd az első fizikai darabot.

## Hajtás és elfordulás

A POL-áttétel egy megvásárolt 20 fogú:100 fogú GT2 fokozat (5:1), 2 mm
osztással, 252 mm osztáshosszú szíjjal. A pontos nyitott szíjhajtás
geometriája kb. 60,56 mm tengelytávot ad, a kis tárcsán több mint hat
kapcsolódó foggal. A CAD beszerzési burkolómérete nem egyedi, nyomtatott
fogazott tárcsa. A feszítést, szíjszélességet, fogprofilt, tárcsafuratot/
agyat, rögzítést és igazítást a kiválasztott alkatrészeken kell ellenőrizni.

A szemléltető 200 lépéses motorral és 16 microsteppel az 5:1 áttétel
16 000 parancsolt microstepet ad kimeneti fordulatonként, vagyis
0,0225 fokot parancs-inkrementumonként. Ez felbontási aritmetika, **nem**
pontosság, ismételhetőség, holtjáték vagy mért polarizációs szögpontosság.

Kezdeti határok:

| Határ | POL-szög |
| --- | ---: |
| Parancsolt szoftveres határ | -80…+80 fok |
| NC-kapcsoló célkioldása | -85 és +85 fok |
| Fizikai keményütköző célja | -90 és +90 fok |

Két független NC-kapcsolót használj. Nyitott érintkező, szakadt vezeték
vagy kapcsolótáp-vesztés határnak/hibának számítson. A keményütközést
fém ütközőcsap vegye fel, ne nyomtatott ASA-fül. A kapcsoló és ütköző közti
5 fok csak kezdeti elrendezési cél; a tényleges működtetési és ütközési
szögeket szögmérővel/sablonnal állapítsd meg, majd a mozgás engedélyezése
előtt ellenőrizd a lassítást és hibareakciót. A lépésszám nem helyettesíti
egyik kapcsolót vagy ütközőt sem. Folyamatos forgás és csúszógyűrű nem cél.
A CAD minden 4 mm-es ütközőcsap középpontját a forgásközépponttól 36 mm-re
helyezi, a bütyök hatótávolsága 34 mm, ezért a névleges csap-sugár éppen
érinti a bütyök csúcsát +/-90 foknál. Ez az ideális érintőhelyzet nem hagy
tűrési tartalékot; az első darabot ellenőrizd és igazítsd úgy, hogy ne
szorulhasson, ne kerülhesse meg a csapokat, és ne terhelje a koaxot. A
konzol és oldallap furatai csak kiinduló szerelési sablonok: válassz valódi
kapcsolót, ellenőrizd a kar/érintkező helyzetét, és mindkét végállásban
függetlenül igazold a csapok és az első darab hézagát.
A +/-90 fokos szögek nem validált célértékek, és nem tesztelt elfordulási
határok; a mozgás engedélyezése előtt az első darabon igazolni kell a
kapcsoló időzítését, a hézagokat, a keményütköző szilárdságát és a kábel
szervizhurkos viselkedését.

A hajlékony koaxot lehetőség szerint a tengely középvonalán vezesd, a
csatlakozókat tartsd az 5 mm-es furaton kívül, adj húzásmentesítést, és
alakíts ki a teljes -90…+90 fokos úthoz illő szervizhurkot. A koaxot az
előírt hajlítási sugár és RF-veszteség alapján válaszd ki; ismételt teljes
útciklusok során vizsgáld. A kábel ne legyen keményütköző, és ne viselje az
antenna terhét.

## Terhelések, tehetetlenség és kiegyensúlyozás

Futtasd a `node scripts/polarization-report.cjs` parancsot a
`calc/polarization.json` megismételhető értékeihez. Szándékosan csak egy
példaantennát modellez: 0,5 kg, 30 mm CG-eltérés, 0,30 m tehetetlenségi
sugár, 0,06 m2 vetületi terület, valamint kizárólag számításhoz használt
8 m/s szél, feltételezett 1,225 kg/m3 levegősűrűséggel, 1,2 ellenállási
tényezővel és 2 biztonsági tényezővel. A 8 m/s **nem** üzemi határ.
Kiválasztott motor dinamikus nyomatékgörbéje nincs megadva; a jelentés nem
állítja, hogy a motor megfelel vagy nem felel meg.

Ebben a példában az antenna önmagában mért POL/EL tehetetlenségi nyomatéka
`m * (k^2 + e^2) = 0.04545 kg m2`; a szemléltető 0,5 rad/s2
0,022725 Nm tehetetlenségi nyomatékot ad a gravitáció, szél, súrlódás és
hardver előtt. A példa AZ-tehetetlensége kizárólag a ponttömeg-tag:
`m * r^2 = 0.03125 kg m2`, feltételezett 250 mm sugáron. Nem számol az
antenna elosztott tehetetlenségével és a mozgó AZ/EL/POL-hardware-rel.
E példákat nem szabad összeadni, majd teljes rotor minősítéseként megadni.

Azonos feltételek mellett a szél erőhatása 2,8224 N. A példában eltérő
nyomatéki karokat kell figyelembe venni: a nyomásközéppont 30 mm-es
excentricitása 0,084672 Nm nyomatékot ad POL körül; a célzási tengely
250 mm-es karja AZ/EL körül 0,7056 Nm-t. Az antenna 30 mm-es CG-eltolása
vízszintes POL/EL-tengely körül a legrosszabb példahelyzetben legfeljebb
0,14715 Nm gravitációs nyomatékot ad; a függőleges AZ ideális esetben
nem visel gravitációs nyomatékot. A szemléltető 2-es tényezővel az
antenna önálló POL-, EL- és AZ-nyomatéka rendre kb. 0,463644, 1,7055 és
1,4112 Nm. Ezekből hiányzik a rotor hardvere, kábelhúzás, súrlódás, a
példán kívüli gyorsulás és a valós antenna területének/CG-jének bizonytalansága.

Az ellensúly mind tömeget, mind tehetetlenséget módosít. Ponttömeg-példában
0,15 kg szükséges 100 mm-es sugáron 0,5 kg kiegyenlítéséhez 30 mm-en;
ez az ellensúly nincs a CAD-ben vagy tömegkeretben, és nem javasolt
alkatrész. Ellensúly választása előtt mérd le és határozd meg a teljesen
forgó antenna/nyereg/kábel szerelvény CG-jét. Mérd meg a teljes tengely
tehetetlenségét, vagy vezesd le lemért alkatrészekből és mért sugarakból;
számítsd újra az AZ- és EL-terhelést a mozgó keretekkel, motorokkal,
kábelköteggel és POL-motorral együtt. A fixen elevációs keretre szerelt
POL-motor akkor is növeli az EL/AZ-terhet, ha nem a POL-tengelyen forog.

Az antenna-only példát ne használd háromtengelyes szerelvény terhelési
minősítéseként. A feltételes két tengelyes tömegkeret 3,130–3,200 kg; az új
POL-keret, plusz motor, koax és forgó oldali RF-hálózat tömegét és
tömegközéppontját még nem mérték meg. Ezek hiányzó értékei kifejezetten
szerepelnek a `calc/polarization.json` fájlban. A tömeg és a
tömegközéppont felmérése után számítsd ki a hozzáadott EL-gravitációs
terhelést `m_POL * g * perpendicular_CG_offset_EL` szerint, minden tengely
hozzáadott ponttömeg-tehetetlenségét `m_POL * r_axis^2` és a fokozat
saját súlyponti tehetetlensége összegeként, a szélterhelési nyomatékot pedig
a mért vetületi terület, nyomásközéppont-eltolás és egyeztetett üzemi szél
alapján. Amíg ezek a bemenetek hiányoznak, a háromtengelyes teljes érték
ismeretlen; ne adj hozzá kitalált motornyomaték- vagy tömegtartalékot a
régi költségvetéshez.

## Tömeg, BOM és nyitott beszerzés

### Üzemi állomástömeg-kapu

A mérvadó maximum **5,000 kg a teljes, üzemi állomásra**: az antennára,
mindhárom rotortengelyre és motorra, rádióra, SBC-re, burkolatra, minden
üzemi kábelre/csatlakozóra, érzékelőre és az állványra együtt. Kizárólag a
külső akkumulátorcsomag/BMS van kizárva; tényleges tömegét külön, szállított
tömegként kell mérni és jelenteni, soha nem nulla tömegként.
A tervezési cél **4,500 kg**, vagyis a maximum alatti előnyben részesített
0,500 kg mért tartalék; ez cél, nem ígéret arra, hogy a terv eléri.
Számítsd bele továbbá a három AZ/EL/POL enkóderérzékelőt és azok három
rögzítőkonzolját, a távoli, rögzített talpra szerelt iránytű/IMU-t annak
tartójával, valamint az álló GPS-vevőt, antennát és tartót. Tömegük, valamint
minden kapcsolódó kábel és csatlakozó az üzemi össztömeg része.
A kijelölt számítógépes/radio-alapkonfiguráció: egy Raspberry Pi Compute
Module 5 (CM5), két cserélhető LimeSDR Mini és azok tartói, a kiválasztott
hivatalos CM5 hordozópanel és hőelvezető megoldás, végleges burkolat, valamint minden
beépített SDR teljesítményerősítő/szűrő és azok hő-/RF-hardvere. ESP32-t
ne számíts bele. A kiegészítő vezérlő-/interfész- és érzékelőelektronika,
tartói és rögzítőelemei is részei a tömegnek.

Az örökölt feltételes két tengelyes 3,130–3,200 kg-os becslés már tartalmazza
az AZ/EL-motorokat és az antennát, de egy nem ismert akkumulátortömeg-
keretet is tartalmaz, miközben a rádiót és az állványt kizárja. Az
akkumulátor/BMS tömegkerete csak akkor vonható le, ha visszakeresett vagy
lemért érték rendelkezésre áll. A korábbi 1,800–1,870 kg-os különbség az
5 kg-os határig nem felhasználható tömegkeret. A helyes össztömeg és
maradékkeret addig **ismeretlen**, amíg az alapot egyeztetjük és a teljes
jelenlegi állomást nem mérjük le.

`station_total = (historical_two_axis_budget - measured_historical_battery_allowance) + CM5_and_official_CM5IO_thermal_mounts + two_LimeSDR_Minis_and_mounts + enclosure_radio_PAs_filters_auxiliary_hardware + new_POL_subsystem + full_tripod + sensors_mounts + station_power_and_all_cables_connectors`

A teljes állványtömeget add hozzá, mert a történelmi alap kizárja az
állványt. A régi kábelek/csatlakozók elszámolását fizikai leltárral ellenőrizd;
csak a ténylegesen hiányzó részt add hozzá, pontosan egyszer. A Powerpole
mindkét illeszkedő fele és érintkezői, bemeneti vezetékek, pozitív főbiztosíték
és tartó, mindhárom külön biztosított ág vezetékei/csatlakozói,
biztosítékai/tartói és a beszerelt húzásmentesítés az 5 kg-os keret része.
A töltő is beleszámít, ha az üzemi készlettel együtt szállítják. A külső
akkumulátor/BMS az egyetlen kizárt tömegtétel; külön kell mérni.

A készletben szerepeljen a CM5 és CM5IO, **két** cserélhető LimeSDR Mini és
tartóik, végleges burkolat, PA/szűrő/árnyékolás és minden kiegészítő
vezérlő-/interfész-elektronika; a harmadik POL-motor és teljes mechanikája;
teljes állvány; három enkóder és külön tartóik; távoli, rögzített talpú
iránytű/IMU és tartó; álló GPS-vevő, antenna és tartó; minden érzékelővezeték,
RF-koax, SMA-csatlakozó és Powerpole-/tápvezeték. A 69 × 31,4 mm-es LimeSDR
burkolóméret csak tervezési referencia, nem tömeg- vagy illeszkedési garancia.
Minden kiválasztott alkatrész tényleges tömege jelenleg mérésre vár; ne
becsüld és ne hagyd ki.

A 4,500 kg a mérnöki cél, lehetőleg 0,500 kg lemért tartalékkal, nem
megfelelőségi ígéret. A 12 V, 1 Ah példa 12 Wh névleges energiája legfeljebb
6 W ideális átlagot ad két órára, veszteségek és tartalék előtt; ez nem
bizonyít kétórás üzemidőt. A nagyobb külső akkumulátort a valós CM5/SDR
terheléshez kell kiválasztani és tesztelni. A `bom/polarization.csv`
beszerzési és mérlegelési lista, nem árajánlattal ellátott vagy kiadott BOM.
Az 1 Ah-s példa korábbi, kizárólag szemléltető érték, nem a jelenlegi
akkumulátor-referencia: lásd az [ECO-WORTHY 12 V, 30 Ah-s referenciát és
annak korlátait](REFERENCE-PRICES.md). Az akkumulátorcsomag/BMS továbbra is
kívül esik az 5,000 kg-os állomástömegen, tényleges tömegét azonban külön
kell mérni és a szállított össztömeghez hozzáadni.

Az RF-összesítés külön tagként kezeli az SMA átvezető aljzatot, a fém
interfészlemezt, a POL-tengely koax/szervizhurok-szerelvényét, mind a négy
antennatápvonal-koax szerelvényt, valamint a további alkatrészre szerelt
RF-csatlakozókat/adaptereket. A négy ág: 145 MHz A és B, továbbá 435 MHz A
és B; mindegyikhez külön tömegérték szükséges, nem helyettesíthető egyetlen
közös jumper tömegével. A csatlakozótömeget vagy a nevesített kábelkötegben,
vagy a külön csatlakozótagban számold egyszer. A rádió/SBC/burkolat
többlettömege jelenleg ismeretlen.

A két LimeSDR Mini mindegyikének 69 × 31,4 mm-es körvonala csak elrendezési burkolóméret,
nem tömegadat, illeszkedési garancia vagy ellenőrzött panelrevíziós rajz;
a magasság, csatlakozó-kizárási területek, rögzítés és hűtési hézag még TBD.
A hivatalos CM5 hordozópanel és CM5 hőelvezetése mechanikai módosítást
igényelhet; ezeket a kiválasztott alkatrészekkel ellenőrizd. A régi
rádiódobozba illeszkedést nem állítjuk.

A GPS-antenna maradjon az állomáson rögzítve, akadálytalan égboltlátással;
ne szereld a forgó boomra. Az iránytű/IMU külön irányreferencia, nem
enkóder. A rögzített talpra szereld, motoroktól és RF-tápáramú hardvertől
távol; lehetőleg ne közös motor- vagy RF-tápburkolatba. Ellenőrizd a
mágneses torzítást az összeszerelt, bekapcsolt állomáson. E mechanikai
koncepcióból ne következtess irányra, iránypontosságra vagy GPS-
teljesítményre. Ne feltételezz pontos kész modult és ne találj ki
konzolillesztést: az iránytű/IMU modul és tartó mérete, a GPS-vevő/antenna
modulok és tartóik mérete, valamint elhelyezésük TBD. A hardverkiválasztás
5 kg-os határhoz történő kiadása előtt válaszd ki az alkatrészeket és
rögzítsd lemért tömegüket.

A POL-motor egy harmadik, hozzáadott motor; tömege, ára, árama, tengelye és
dinamikus nyomatéka TBD. A POL-keretet, tengelyt, csapágyakat, tárcsát,
merevítést, kapcsolókat, koax/RF-többletet és esetleges ellensúlyt is le kell
mérni. A POL-motor, mechanika, rádió, két SDR, kiegészítő hardver és állvány
tömege a többi hozzáadással együtt ismeretlen. Az üzemi össztömeg
nem számítható ki, amíg a hozzáadott hardvert, állványkülönbözetet és még
be nem számított üzemi kábeleket/csatlakozókat le nem mérik. A
hardverkiválasztás feltétele a tömegösszesítés lezárása; megfelelőséget csak
akkor állíts, ha a teljes konfigurációjú állomást ténylegesen 5,000 kg-nak
vagy kevesebbnek mérted. A `bom/polarization.csv` beszerzési és mérlegelési
ellenőrzőlista, nem beszállítói árajánlattal ellátott vagy kiadott BOM.

## Az RF-polarizáció külön funkció

Ebben a koncepcióban minden koaxiális RF-csatlakozás szabványos polaritású
**50 ohmos SMA**; az RF-koaxláncban RP-SMA, BNC és N-típus nem megengedett.
Ez csak az RF-/koaxcsatlakozásokra vonatkozik: a Baofeng kézibeszélő-,
hangszóró-, mikrofon- és más hang-/tartozékcsatlakozóit **ne** cseréld le,
és ne alakítsd át SMA-ra. Meglévő hanginterfészeik változatlanok.

A rögzített talpi koaxbelépés méretezett interfész, nem kiválasztott vagy
lemért csatlakozó. A `cad/polarization-coax-interface.dxf` egy előzetes
30 × 22 × 3 mm-es fém fület határoz meg, névleges 1/4-36 UNS SMA
csatlakozómenethez 6,5 mm-es átvezető furattal, két 3,4 mm-es
húzásmentesítő furattal 10 mm középtávolságon, 6 mm-es eltolással, valamint
két 3,4 mm-es rögzítőfurattal 24 mm középtávolságon. Kiadás előtt mérd le a
ténylegesen beszerzett SMA-aljzatot, menetet, anyát, panelvastagság-
tűrést és tömeget; ellenőrizd, hogy elfér-e a 3 mm-es fülben. A kábelkötöző
furatok jelentik itt az egyetlen meghatározott húzásmentesítő kialakítást;
a tényleges kötözőt/grommetet és koaxútvonalat válaszd ki és teszteld.
A csatlakozók maradjanak a tengely 5 mm-es furatán kívül.

Könnyű 50 ohmos koaxot csak az adott kábel és teljes útvonal veszteség-,
teljesítmény-/frekvencia-besorolásának és minimális hajlítási sugarának
ellenőrzése után válassz. Rögzítsd a tengely szervizhurok-törzsének és a
négy egyedi antennatápvonal-jumpernek a tömegét a csatlakozóvégekkel együtt.
A koax típusa, hossza, hajlítási sugara és összeszerelt tömege még TBD; a
könnyű kialakítás nem bizonyítja az RF- vagy mechanikai követelmények
teljesülését.

Az antenna iránytengely körüli mechanikai forgatása **nem** alakítja át az
RHCP-t LHCP-vé. A kéz kiválasztásához sávonként, egymástól független,
ortogonális táplálási portokkal rendelkező, kompatibilis körpolarizált
antenna kell. Koncepcionális elrendezésként minden sávhoz külön
90 fokos kvadratúra-hibrid tartozik: az antenna ortogonális betáplálásai a
hibrid két kimeneti portjára csatlakoznak; RF-re méretezett DPDT
átkapcsoló keresztezi a rádióforrást az egyik hibridbemenetre, az 50 ohmos,
méretezett lezárást pedig a másikra. A forrás és lezárás felcserélése a
hibrid bemenetei között megfordítja a betáplálások relatív fázisát, és így
az ellenkező kéziséget választja ki, ha az antenna kompatibilis, és a
tényleges hibrid port-/fáziskonvenciója ezt alátámasztja. Ez nem
validált hálózatkoncepció; nem kiválasztott kapcsolási rajz vagy RF-terv.

145 MHz-re és 435 MHz-re külön, függetlenül minősített hálózatot/kapcsolót
kell megvalósítani. Ha egyetlen koax halad át az üreges forgótengelyen, a
forgó szerelvényen a sávonkénti hálózatok előtt kompatibilis 145/435 MHz-es
diplexer szükséges, és a rádió végén ennek reciprok párja; ez a forgó
tömeget is növeli, ami TBD. A meglévő lineáris polarizációjú prototípus-
antenna nem kompatibilis: sávonként megfelelő, független ortogonális
betáplálású antennát használj. Üzem előtt VNA-val/ismert jellel ellenőrizd
minden hibrid fázisegyensúlyát, sávszélességét, beiktatási veszteségét,
leválasztását, RF-teljesítményét, lezárásait, csatlakozóit és az antenna
konvencióját. A kapcsolók, csatolóhálózatok, 50 ohmos lezárások, vezérlés
és adásretesz kiválasztatlanok és méretlenek. Az RF-vezérlés legyen
elektromosan független a POL-motortól; kapcsolás alatt, illetve bizonytalan
vagy hibás kapcsolóállapotban tiltsd az RF-adást. A kapcsoló feszültségét,
áramát, hibaállapotát, megszakítás előtti/utáni viselkedését, reteszét és
visszavertteljesítmény-kezelését külön meg kell tervezni és tesztelni.
Itt nincs állítás kereskedelmi alkatrészről, teljesítménybesorolásról vagy
mért RF-eredményről.

Az opcionális `pol_part=10` kábelkötöző STL-fájlt,
`cad/polarization-power-strain-relief.stl`, OpenSCAD 2021.01-gyel
rendereltük, és egyetlen zárt, helyesen orientált, 3132 háromszögű
(11 769,7 mm3) szilárd hálóként ellenőriztük. Ez csak a háló topológiáját
igazolja, nem a panelilleszkedést, kábelrögzítést, nyomtatási szilárdságot
vagy Powerpole-csatlakozó illeszkedését.

## Powerpole-kábelköteg rögzítése és panelcsatlakozás

A három védett egyenáramú ág külön tömegkeretet kap: a szabályozott CM5IO
5 V-os átalakítást, a felülvizsgált NC vészleállító megszakítási útján
átvezetett motor-tápot, valamint az RF PA tápját. Külön mérd meg a pozitív
főbiztosítékot és tartóját, minden ág biztosítékát/tartóját, az ágak
pozitív/visszavezető vezetékeit és végcsatlakozóit, az akkumulátor–állomás
vezetékpárt, valamint az állomáshoz rendelt piros/fekete Powerpole-
csatlakozópárt és érintkezőit. A névleges értékek, pontos érintkező-/
burkolattípusok, csatlakozó-kódolás, vezeték-keresztmetszet/hossz,
biztosítéktartó minősítése és minden biztosítékérték TBD. A Powerpole
családneve vagy a burkolat színe nem igazolja a csatlakozó tájolását vagy
polaritását; táp csatlakoztatása előtt ellenőrizd a konkrét szerelvényeket
feszültségmentesen, DMM-mel. A külső akkumulátor/BMS az egyetlen, a
állomástömeg-határból kizárt tápbemeneti tétel.

Opcionális, általános kábelrögzítő lemez a `cad/polarization_station.scad`
fájlban `pol_part=10` értékkel választható; additív STL-exportját,
`cad/polarization-power-strain-relief.stl` fájlt OpenSCAD 2021.01-gyel
renderelték, majd egyetlen zárt, orientált, 3132 háromszögű szilárd
hálóként (11 769,7 mm3) ellenőrizték. Névleges méretburka 48 × 84 × 3 mm;
négy 3,4 mm-es panelrögzítő-furat és négy pár, 12 mm-es osztású,
3,4 mm-es kábelkötegelő-furat található rajta. A párok a bemenő vezetéket
és a három kimenő ágat rögzíthetik. Ez általános kábelrögzítő, **nem
Powerpole-csatlakozó-tartó**: a panelosztást, a kábel/kötegelő illeszkedését,
a nyomtatott szilárdságot, húzásmentesítést és kihúzással szembeni ellenállást
az első darabon kell illesztéssel és próbával ellenőrizni. Ha beépíted, a
lemezt, kötegelőket és rögzítőelemeket is számítsd bele az állomástömegbe.

Kifejezetten Powerpole-paneltartó szándékosan nincs még megtervezve: nem
választottak ki és nem ellenőriztek pontos csatlakozóburkolatot,
érintkezőt, panelrögzítést vagy gyártói méretrajzot. Ne méretezd át ezt az
általános rögzítőlemezt, az SMA-interfészt vagy egy családnév szerinti
méretburkot úgy, mintha azok igazolt csatlakozó-illesztést jelentenének.
Külön paneltartót csak a kiválasztott burkolat pontos rajzának,
rögzítőelemeinek, illeszkedésének és előírt panelvastagságának egyeztetése
után adj ki.

Az örökölt alapból az állvány hiányzik; a teljes kiválasztott üzemi
állványt pontosan egyszer mérd le és add hozzá az aktuális össztömeghez.
A régi elszámolás a kábeleket/csatlakozókat tartalmazottnak tekinti, de ezt
fizikai leltárral ellenőrizd, és csak a hiányzó részt add hozzá, egyszer.
Az új enkódereket, három tartójukat, GPS-vevőt/antennát, iránytűt/IMU-t,
tartóikat és érzékelőkábeleiket a leltárig és mérésig hozzáadandóként kezeld.
Az érzékelők tömegét egyenként rögzítsd, majd pontosan egyszer számold el az
érzékelők/tartók tagban; kábeleik és csatlakozóik a külön
`sensor_cables_and_connectors` tagba kerüljenek. Az
`other_additional...` tagból hagyd ki ezeket és a külön elszámolt RF-koax-/
csatlakozótételeket. Külön mérd és számold el a CM5-modult, a hivatalos
CM5IO-t, a kiválasztott hűtést, tartókat, **két** cserélhető LimeSDR Mini
egységet, végleges burkolatot, PA-kat, szűrőket, árnyékolásokat és a
fennmaradó rádióhardvert; ne számolj kétszer olyan alkatrészt, amely egy
már mért szerelvény része. A történeti akkumulátor-tömegkeretet csak akkor
vond le az alapból, ha visszakeresett vagy lemért adat áll rendelkezésre.
Az állomástömeg és a szabad tömegkeret a leltár egyeztetéséig ismeretlen.

Az RF-csatlakozó-/kábelösszesítés külön tagként kezeli az SMA
panelátvezető aljzatot, a fém interfészlemezt, a POL-tengely
koax/szervizhurok-szerelvényét, mind a négy antennatápvonal-koax
szerelvényt és a további, alkatrészre szerelt RF-csatlakozókat/adaptereket.
A négy ág 145 MHz A/B és 435 MHz A/B; mindegyiknek saját tömegértéke kell,
nem lehet egy közös jumper-tömeggel helyettesíteni. A csatlakozótömeget a
nevesített kábelkötegben vagy külön csatlakozótagban számold el, egyszer.
A rádió/SBC/burkolat hozzáadott tömege, valamint a két LimeSDR és tartóik,
a segédelektronika és minden új tétel tömege ismeretlen; ezek nélkül ne
adj meg állomástömeget.

## Reprodukció és elfogadás

Helyi OpenSCAD CLI-vel rendereld az STL- és DXF-kimeneteket a
`cad/polarization_station.scad` fájl 1–9 numerikus `pol_part` értékeivel:
keret, rotorhordozó, csapágyrögzítő, határolóbütyök, határolókonzol,
eredeti BASE-nyereg, motorlap-DXF, oldallap-DXF. A `pol_part=0` az
összeszerelést mutatja, ez vizualizáció, nem nyomtatható STL. Fizikailag
ellenőrizd a 20 mm-es nyerget, meglévő karimát, valós tárcsákat/motort,
csapágyakat, kábelt, ütközőket és NC-kapcsolókat. Motor-táp nélkül vizsgáld
meg először a kapcsoló–ütköző sorrendet és a kábel teljes útját; ezután
felügyelt, kis sebességű próbapadi teszt következhet, leválasztott RF-fel
és független vészhelyzeti tápmegszakítással. A 7-es a motorlap-DXF, a 8-as
az oldallap-DXF, a 9-es a koaxinterfész-DXF; a 10-es az opcionális,
általános kábelkötegelős húzásmentesítő lemezt választja, amely nem
Powerpole-csatlakozó-tartó. A `pol_part=10` elemet külön, új STL-ként
exportáld; ne írd felül egyik meglévő kimenetet sem.
