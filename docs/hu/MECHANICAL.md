# Hordozható moduláris állomás — eredeti mechanikai prototípus

> **Olvasási sorrend:** a dokumentum elején álló, későbbi állapotfrissítések felülírják az alattuk található régebbi mechanikai méreteket és tömegterveket. Az alábbi régi planetáris hajtás és ESP32-hordozó történeti, opcionális terv; nem része a jelenlegi szíjas BASE-nek, és nem tekinthető a CM5-alapú új rádiórendszer gyártási tervének.

## VÉGLEGES: 22 mm-es valós kábelplenummal készült doboz — felülírja az alábbi történeti méreteket

A `cad\carrier_enclosure.scad` végleges doboza **224×174 mm belméretű, 228×178×43,6 mm külső méretű**, 2 mm-es fedéllel és 0,7 mm-rel kiemelkedő külső betűkkel. A **180×130 mm-es NYÁK** sarokpontja **(24,24), z=8**: oldalanként **22 mm szabad hely** marad, ami kezdeti burkolóként elegendő a jelentett 20 mm-es csatlakozókábelekhez; nem állítja tévesen, hogy a korábbi 2 mm-es hely elegendő volt. A NYÁK felett a tetőig 32 mm marad; a megerősített NYÁK-vastagság 1,6 mm, az NPTH furatok 3,2 mm-esek. Az oszlopok új helye: **(29,29), (199,29), (29,149), (199,149)**; középtávolságuk pontosan 170×120 mm. A tényleges kábel minimális hajlítási sugarát ellenőrizni kell: a 22 mm tervezett hely, nem minden dugóval végzett próba.

A kivehető vakpanelek megmaradnak, és csak a valós szerelvény szerint fúrhatók. Előlapi nyílási tartományok: x=20..60 és 168..208, z=15..37; oldalsó tartományok: y=25..55 és 123..153. Ezeket nem szabad USB/JST/sorkapocs furatközéppontjának tekinteni mérősablon nélkül. Minden kábelnek saját plénuma van a fal előtt. Az akkumulátor **külön** marad a rögzített tálcán; végleges méretei továbbra is blokkoltak, ezért nem modellezzük önkényesen a dobozban.

A jelenlegi külön tálca DXF-je **2 mm-es, 240×196 mm-es alumínium**, négy M5 rögzítő 180×30-as mintában, valamint két, a fülekhez igazodó M4. Névleges tömege furatok előtt 254 g. Ezt a tartó elvékonyításával vagy a parkolórögzítő eltávolításával nem szabad kompenzálni. A végső ASA-doboz térfogatai: alap 149 957,5; fedél 81 678,9; két panel 3 102,0 és két további panel 2 502,0 mm³; összesen kb. **242 844,5 mm³ / 259,84 g tömör ASA**. E méretű sima fedél kb. 81 095,6 mm³; az összekötött domború felirat további 583,3 mm³, kb. 0,624 g. A teljes BASE ASA tömege kb. **1,009 kg tömör anyagból**.

Frissített tág tömegkeret: **3,522–4,407 kg tömör anyaggal**, hipotetikus 75%-os ASA-anyaghányad mellett **3,270–4,155 kg**, a 254 g-os tálcát és akkumulátort is beleszámítva. A korábbi feltételes BuildLight 2,679 kg-hoz a doboz kb. 147,42 g-os növekménye, a 254 g-os tálca, valamint a korábbi 100 g helyett 150–220 g-os összeszerelt hordozó 50–120 g-os többlete összesen kb. **3,130–3,200 kg-ot** eredményez, még a további buck-átalakító, stop és kábelek előtt. A jelenlegi költség/tömegkeretben a **≤3 kg cél nem teljesül és fizikailag nincs igazolva**. Az alábbi 2,748/2,916 kg-os adatok, valamint az 184×134/188×138 mm-es dobozméretek történetiek, **felül vannak írva**. A kábelezési hely bővült, de ez nem bizonyít ≤3 kg-os állomást; a tömegcélhoz további tervezési döntés vagy tényleges alkatrészválasztás szükséges.

A négy végleges STL fájlonként, átmeneti fájlnéven exportálták, majd változatlanul átmentek az ellenőrzőn; a fedél 9 024 háromszögből és egyetlen összefüggő komponensből áll. A végső fedél SHA-256 értéke: `0C3E09D586A310A8FE5F26B071AE8EC72EA61FE250C590C94FEAFCA405B06B79`. A Liberation Sans Bold betűtípus mellékelve van, nincs platformfüggő helyettesítés. A tálca DXF és az összeállítási CSG frissült. A tesztek a dimenziónkénti további 44 mm helyet, az oszlopok relatív helyzetét, belmagasságot, hálókat és tömegnövekményt ellenőrzik; a fizikai illeszkedés továbbra sincs kipróbálva.

### A tényleges 180×130-as carrier NYÁK: a jelenlegi rögzített doboz

A hardverügynök jelentése szerint a vezetősávos NYÁK **180×130 mm**, furatai a NYÁK sarkától mérve: **(5,5), (175,5), (5,125), (175,125)**. A régi 124×64 mm-es belső doboz nem fér el benne, és nem szabad ezt a NYÁK-ot befogadó dobozként megrendelni vagy kinyomtatni; nem szabad egy képzeletbeli kisebb NYÁK-kal helyettesíteni.

A `cad\carrier_enclosure.scad` új rögzített dobozt modellez: külső méret 188×138×43,6 mm és külön 2 mm-es fedél; belső méret 184×134 mm; fal és fenék 2 mm. A NYÁK z=8 síkban áll (2 mm fenék felett 6 mm-es oszlopon), a feltételezett 1,6 mm-es NYÁK felett 32 mm szabad tér, a fedél alatt még 2 mm. A NYÁK (4,4) sarokpontról indul; házfuratok (9,9), (179,9), (9,129), (179,129), a jelentett mintával egyező 170×120 mm-es távolsággal. A hardverügynök megerősítette az **1,6 mm NYÁK-ot és a 3,2 mm-es M3 NPTH furatokat**; a CAD frissült. Szerelés előtt ellenőrizd a Gerber/drill fájlokat és a legyártott panelt. A NYÁK origója a bal felső sarok, mindkét koordinátája pozitív; a szimmetrikus téglalap minta egyezik. A CAD-be átvitelkor ne fordítsd meg a jelöléseket/csatlakozókat. M3 átmenőcsavar, alátét és anya kell, ASA-menet nem; az oszlopokra ne kerüljön alkatrész.

Két kivehető panel szolgál két 40×22 mm-es előlapi és két 30×22 mm-es oldalsó nyílásnak. Ezek **vakfedelek**, nem kitalált csatlakozónyílások; a tényleges csatlakozó és pozíció szerint kell fúrni vagy újragenerálni, a dugók és koax/kábel sugara számára helyet hagyva. A hardverjelentés kb. 10 mm-es ESP-magasságot és 15–20 mm-es meghajtó/hűtőborda-magasságot ad; ezek a 32 mm-es fejmagasságon belül vannak. A meghajtó/táp bal alsó, a GNSS/érzékelők jobb oldali elrendezése jelentett tájolás, nem következtetett furatpozíció. A GNSS/IMU és két AS5600 moduláris csatlakozású; maguk az AS5600 érzékelők a tengelyeik közelében maradnak. A 32 mm-es átlátszó tér csak a magassági keretet mutatja, nem beültetett alkatrészeket. A doboz és akkumulátor **álló** tálcán/állványon vagy a rotortól független modulban legyen, védett és tehermentesített kábellel; a nagy dobozt ne terheld az antennára/AZ karimára.

A `cad\carrier-metal-mount.dxf` rögzített 2 mm-es, 200×156 mm-es alumíniumlap: két M4 a dobozfülekhez, négy M5 az állvány-/tálcabilincsekhez 140×30 mm-es mintában. Átmenő csavarok, alátétek, anyák és szigetelő távtartók kellenek; nincs kitalált rotorba illesztés. Vágás/sorjázás után ellenőrizd a tartó teherbírását; a lap furatok előtt kb. 168,5 g és **beszámít a tömegbe**. A tálcát önmagában ne használd fogantyúként vagy antennatartóként; a hátlap, merevítések, tényleges bilincs és vezetékezés további tömegtartalékot igényel.

A `cad\carrier-stl` mappában négy selector exportálható: `base`, `lid`, `port40`, `port30` (mindkét panelből kettő nyomtatandó). CSG: `cad\carrier-assembly.csg`; exportáló szkript: `cad\export-carrier.ps1`. A négy STL CGAL- és két Node-tesztje sikeres. A négy panellel együtt a tömör térfogat 170 138,6 mm³, kb. **182,05 g ASA**; a régi 112,0 cm³-es / 113,04 g-os dobozfedélhez képest **69,01 g növekedés**. A BASE ASA tömege 0,862-ről **0,931 kg tömörre** változik; a NYÁK tömege nem lett kitalált módon csökkentve.

A korábbi 2,679 kg-os feltételes BuildLight névlegesen **2,748 kg**, ha a teljes doboznövekményt tartalékoljuk és minden más korlát teljesül. A korábbi 75%-os ASA-forgatókönyvben ugyanezen teljes növekmény fenntartásával kb. **2,934 kg**, mindössze 66 g tartalék. A 180×130-as NYÁK feltételezett 100 g-os beültetett tömege még nincs lemérve; egy 1,6 mm-es, 1,85 g/cm³ FR4 panel önmagában kb. 69 g lehet, rézzel, ESP32-vel, meghajtókkal, csatlakozókkal és GNSS-szel együtt pedig jóval 100 g fölé kerülhet. Az új doboz és lemez szűkíti a célt; a ≤3 kg állítása előtt mérd le az elektronikát és akkumulátort. A 21 mm-es motorjelölt továbbra sem kompatibilis a jelenlegi alappal. Egyetlen feltételes tömegtáblázat sem mechanikai/elektromos jóváhagyás vagy mérés.

**A felhasználó által választott jelölés:** a 180×130-as carrier fedelén domború `BRICOHAMS` és `bricohams.org` felirat, hivatalos logó kitalálása nélkül. Paraméterek: `brand_name`, `brand_url`, `brand_raise=0.7`, `brand_font="Liberation Sans:style=Bold"`; a LiberationSans-Bold.ttf az OpenSCAD 2021.01 hordozható csomag része. Nem függ a rendszer Arial-helyettesítésétől. Más OpenSCAD esetén telepítsd/válaszd ezt a családot, vagy vizuálisan ellenőrizd és rendereld újra. A két középre zárt sor 12/8 mm-es, távol van a csavaroktól, sarkoktól és portoktól; z=1,95-től 2,7-ig ér, 0,05 mm-rel átfed a 2 mm-es fedéllel, tehát egyetlen összefüggő test. A 0,03 mm-es eltolás stabilizálja a nyomtatási kontúrt; nem fordított gravírozás és nem lebegő tábla. A fedelet sík oldalával lefelé, betűkkel felfelé nyomtasd; ez nem változtatja a 32 mm-es belső helyet és nem ad hozzá RF-fémet.

A feliratos fedél 52 398,9 mm³, a sima 51 815,6 mm³; növekmény 583,3 mm³, névlegesen kb. **0,624 g ASA**. A valódi bináris STL 9 024 háromszögből áll, zárt és irányított élekkel, degenerált elemek nélkül; teszt ellenőrzi a CAD-feliratot és a renderelt térfogatnövekedést. Az első ASCII kimenet degenerált elemeket tartalmazott, ezért elutasították; a végleges bináris export stabilizált kontúrral megfelelt. Mind a négy carrier STL újrarenderelve, CSG és tálca DXF újragenerálva. A jelöletlen korábbi doboztömeghez 0,624 g adandó; ez nem változtat azon, hogy nincs valós mérés/jóváhagyás. Az exportáló most `*.pending.stl` fájlba ír, ellenőriz, és csak utána cseréli a végleges STL-t, így a párhuzamos tesztek nem olvasnak félkész rendert. Az ellenőrző megtartja a degenerált-háromszög feltételt és összefüggő komponenseket is számlál: a feliratos fedél **egyetlen komponens**, nincsenek lebegő betűk. A végső újrarender és 11 mechanikai teszt sikeres. A végleges fedél SHA-256: `EC5806AA9FF4EB068FBC695D6CEEF794CD9DDE1DB68270D784114A5068320E34`.

Az új 2 mm-es fémtálca további kb. 0,168 kg, ezért a feltételes BuildLight **kb. 2,916 kg**, kb. 84 g maradékkal. A korábbi 75%-os ASA-eset a tálcával **kb. 3,102 kg**, tehát meghaladja a 3 kg-ot. Akkumulátor/NYÁK/vezérlés nincs lemérve; ≤3 kg nem igazolt, és szűkebb kiválasztás/tervezés kell.

**Végső hardverfrissítés:** carrier 180×130, FR4 1,6 mm, mindkét oldalon 2 oz réz, 3,2 mm-es NPTH megerősítve. A NYÁK-gyártó nem mérte meg a panelt; üres panelre konzervatív kb. 100 g tartalékot, ESP/TMC/hűtőbordák/sorkapcsok/biztosítékok szerelve **150–220 g-ot**, plusz még függő buck/stop/kábeleket kell fenntartani. A korábbi 100 g-os beültetett-elektronika cél már **nem védhető**. A 150–220 g-ra váltás 50–120 g-mal emel: a feltételes BuildLight **kb. 2,966–3,036 kg**, a további függő tételek és 21 mm-es motor-összeférhetetlenség ellenőrzése előtt. A kedvező végén is csak kb. 34 g marad, a magasabb vég meghaladja a 3 kg-ot. **Nincs jelenleg igazolt ≤3 kg-os jelölt**; feltételes összeget ne mutass elfogadásként.

A hardver legalább 30 mm-t kér a NYÁK **felett**; az itt megadott 32 mm névlegesen ezt teljesíti 20 mm-es komponensekkel, de nem hagy 30 mm-t az alkatrészek felett. Jelentett komponenskoordináták a NYÁK bal felső origójától: USB-modul jobbra; JST I/O x≈157; motorok y≈120 szélen; DC x≈12/y≈18 bal oldalon. Ezek alkatrészhelyek, nem ház-nyílásközéppontok: a panelek addig vakok, amíg a tényleges kábel/dugó és beültetett NYÁK nem mérhető. Hagyj helyet a jelentett 20 mm-es oldalsó csatlakozóknak; a 2 mm-es belső rés **nem biztosít 20 mm oldalsó helyet**, ezért a fal felé néző USB/sorkapocs nyitott panelt vagy helyi/külső bővítést kíván. Ne állíts zárt fedelű kábelkompatibilitást próba nélkül.

A jelentett Pololu D24V22F5 buck (17,8×17,8×8 mm) külön, szigetelt rögzítést igényel a rögzített tálcán/dobozon, igazolt méretű tartóval és csavarokkal; ne lebegjen a NYÁK fölött. Ne találj ki modulfuratokat; ne építsd be rajz nélkül. A védett akkumulátor végleges mérete és AS5600 breakout nincs kiválasztva; ezek gyártási/összeszerelési blokkolók. A korábbi 16×16-os érzékelőfurat továbbra is ideiglenes, nem kötelező a carrier NYÁK-ra.

## Jelenlegi BASE: szíjhajtás, tömegelsőbbség

A felhasználó kifejezett döntése szerint a hajtás módosítható a ≤3 kg célért, amelybe az akkumulátor beletartozik, a rádió/állvány nem. **Jelenlegi BASE: `cad\belt_station.scad`.** A `cad\station.scad` változatlanul megtartja a korábbi bolygóművet **LEGACY opcionális** tervként; a két BOM nem összeadandó és a két hajtás nem építendő együtt. A dokumentum planetáris részei csak a LEGACY változatra vonatkoznak. Megmarad az AZ ±180°, EL 0..90°, levehető antenna, álló rádió, AS5600, NC végállás, fém UNC állvány és még nem validált RF-geometria.

A BASE két GT2, 2 mm osztású 20:100 fokozatot használ: pontosan 5:1 × 5:1 = **25:1**. 200 teljes lépés × 16 mikrolépés × 25 = **80 000 parancsolt lépés/kimeneti fordulat**; ez az áttételi szám, nem igazolt felbontás/pontosság (névlegesen 0,0045°/lépés). Minden fogazott tárcsa **vásárolt fémtárcsa**, nem profil nélküli ASA GT2 fog. A CSG beszerzési befoglaló méretet jelöl, nem gyártható tárcsamodellt vagy garantált SKU-t. Négy folyamatos, vásárolt GT2 szíj: **126 fog / 252 mm / 6 mm széles**.

### Középtáv, feszítés, támaszok és valós erőátvitel

A 20 és 100 fogú tárcsa osztóköreinek sugara 6,3662, illetve 31,8310 mm. A nyitott szíj pontos hossza:

`2 sqrt(C²−(R−r)²)+π(R+r)+2 asin((R−r)/C)(R−r)`.

A megoldott középtáv **C=60,56301755 mm**; a burkolók nem fedik egymást. A 20 fogú tárcsa körülfogása **130,2718° / 7,237 fog**. Ebből önmagában nem következik nyomatékképesség; a szíj gyártói görbéjét a fordulatszám és feszítés alapján kell ellenőrizni. Egy reduktor középpontjai: motor x=−C, közbenső x=0, kimenet x=+C, mind y=0. Két szíjsík lokális z=15..21 és 28..34.

A 6082 alumíniumlemez névleges vastagsága **3 mm**, 187,126×86 mm; első lap z=0..3, hátsó z=54..57. Vágási DXF-ek: `cad\belt-front-plate.dxf`, `cad\belt-rear-plate.dxf`; AZ-tálca `cad\belt-tray.dxf`. A lemezek **nem ASA STL-ek**. A 48 mm külső átmérőjű ASA csészék a 608 (8×22×7) és 6000 (10×26×8) csapágyakat tartják, tengelyenként kettőt-kettőt. Első csészék z=3..13, hátsó z=44..54; a csapágyak a fémlemeznek és a csésze külső peremének támaszkodnak. Meghúzás előtt erőltetés nélkül igazítsd őket. A csapágyak belső felületei kb. 40 mm-re támasztják a **8×60 mm-es acél közbenső** és **10×89 mm-es acél kimeneti tengelyt**, tengelyenként kettőt; nem nyomtatott motor-tengelyt. A két csésze eltérő eltolása meggörbítheti a tengelyt: együtt állítsd a támaszokat, ellenőrizd koaxiálisságukat.

- 1. fokozat: tárcsák z=14..26, a perem/agyrész is beleértve.
- 2. fokozat: z=27..39. Az első és második fokozat agya között **1 mm**.
- Hátsó csészék z=44-től: az agyhoz képest **5 mm**.
- A hátsó lemez z=57-nél ér véget; a terhelőkarima z=60-nál indul: 3 mm távolság.
- Karima z=60..78, mágnes z=81..93, érzékelő z=95..98; a tengely z=89-nél végződik.
- Vásárolt 100T tárcsa: karima külső átmérője ≤66,662; teljes axiális szélesség ≤12; agy külső átmérője ≤30 mm. A 20T tárcsa szélessége ≤12; agy OD ≤18 mm. **Vásárlás előtt mérd/ellenőrizd a rajzot**; sok kereskedelmi agy túl hosszú és áttervezés nélkül nem fér el.
- A motor kinyúló tengelye a homloklaptól **legalább 26 mm** legyen az első tárcsa eléréséhez; egy NEMA14 rövid tengelye nem megfelelő automatikusan. A 26 mm-es furattáv és 35 mm-es homloklap még előzetes.
- A közbenső tengely fém retesz/gyűrű vagy helyesen méretezett csap útján köti össze az első fokozat 100T tárcsáját a második 20T-jével. A kimeneti 100T tárcsa és karima fémtengelyen 10 legyen fém retesz/csap révén összekötve; ragasztó/ASA ne vigye át a nyomatékot. A csapfurat/reteszhornyok gyengítik a szelvényt; megmunkálni és vizsgálni kell.

**Valós feszítő:** 3 mm-es vízszintes hosszlyuk a motor és mindkét közbenső támasz rögzítésében, nem dísz feszítőgörgő. A kimenet rögzített; a közbenső negatív x irányba mozgatása növeli C2-t. A motort még tovább negatív irányba kell mozgatni, hogy C1 helyreálljon. Alkatrészenként ±1,5 mm állítás csak kis előfeszítésre való, hibás hosszú szíj kompenzálására nem. Csészénként négy M3 csavar nagy alátéttel; a motor négy M3-mal rögzül. A gyártó maximális feszítési adata szerint, a beállítás után húzd meg. Használj M4 állítócsavart és ellenanyát fém füleken, vagy távtartó-sablont; feszítőként ne hivatkozz rugalmas ASA-ra. Túl nagy feszítés csapágyat és tengelyt terhel. A valós tárcsaagyak mellett a szíjsík legyen szabad a csavarfejektől/gyűrűktől.

AZ esetén a reduktor homloklapja 45 mm-rel az alap fölött; a motor z=11..45 között szabad. Négy 36 mm-es fém távtartó támasztja az első lemezt a rögzített tálca z=6..9 síkja felett; a motort ne műanyag lógassa. EL a 3 mm-es, hajlított alumínium tartón legyen, merevítéssel/szegeccsel vagy csavarral; közös M4 karimainterfész. EL-tengely 60 mm-rel a tartó alapja fölött; a 86 mm magas lemezek 17 mm-rel nyúlnak fölé. A 38×38-as ablak engedi el az EL motort; négy M4 házrögzítő. A csészék és lemezek teherutat alkotnak; a hajlított fémtartó és merevítése valós fémgyártást és merevségpróbát igényel, a nyomtatott befoglaló modellje nem teherbírási igazolás.

Az AS5600 két 20 mm-es fém távtartóval és nyomtatott konzollal a hátsó lemezhez rögzül, **nem a kimenettel együtt forog**. A 6×2 mm-es mágnesek átmérő mentén vannak a kimenőtengelyen. Rádió/dobozok az állványhoz rögzített tálcán maradnak (BASE-nézetben nem renderelődnek újra); antenna/nyereg/NC-rögzítés újrahasznált. Hiányoznak a konkrét bütykök, szíjvédők, valós kábelezés, valamint a csavarfejek/agyrészek/reteszek ellenőrzése: **integrációs terv, nem összeszerelésben tesztelt vagy üzemkész szerelvény**. A CSG valós burkolókat mutat; a vásárolt fém alkatrészeket nem exportálja nyomtatható STL-ként. Energizálás előtt ellenőrizd az AZ/EL teljes mozgási burkolóját, szenzor/nyereg hézagot, koaxiálisságot, tartókat és teljes akkumulátort.

### Visszahajthatóság, teher és szállítás

A szíjhajtás **visszahajtható**; kikapcsolt motornál ne tulajdoníts neki planetáris önzárást vagy féket. Az antennát egyensúlyozd ki, majd alacsony helyzetben rögzítsd **fém parkolócsappal vagy a vázhoz külön rögzített hevederrel**; motorozás előtt vedd ki. Tápvesztéskor az EL leeshet: lekapcsolás előtt támaszd meg/vedd le az antennát; senki ne tartózkodjon alatta. Tartóáramot csak hő- és biztonsági próba után csökkents. Az ideiglenes 500 g-os és CG≤30 mm-es terhelési cél, valamint a korábbi szélpróbák előzetesek; nem vihetők át az ASA-nyomaték-/hatásfokadatok a szíjhajtásra. A szíj hatásfoka nincs mérve.

### Kezdeti tömeg-összehasonlítás és döntési feltétel (a 180×130 carrier előtt)

A BASE nyomtatott modell közös kiegészítőket tartalmaz, a 34 nehéz planetáris darabot nem. Négy új STL (`base`, `cup608`, `cup6000`, `encoder_support`) a `cad\belt-stl` könyvtárba kerül; a többi közös darab `cad\stl`. Tömör ASA-egyenérték **0,862 kg**, szemben a LEGACY 2,521 kg-jával. A CSV Bxx mennyiségek felváltják a Pxx/Mxx sorokat; közös B08..B10 csoportok selectorokat részleteznek, nem további komponensek.

Később kiválasztandó motor/akku/kábelezés tömegkerete: fém motor 0,24–0,36; nyolc tárcsa 0,16–0,24; szíjak 0,020–0,035; nyolc csapágy 0,130–0,150; acéltengelyek 0,169; négy lemez + EL-támasz + tálca 0,680–0,780; távtartók/hardver 0,150–0,250; antenna/RF/koax 0,360–0,580; vezérlés/akku 0,350–0,580 kg. A négy 187×86×3-as lemez furat előtt akár 0,521 kg; az EL-támasz/tálca teszi ki a tartalékot.

**Tömör összesen: 3,121–4,006 kg.** Hipotetikus 75%-os ASA-anyaghányad: **2,905–3,790 kg** (nem 75%-os slicer infill és nem slicereredmény). A kedvező szélsőérték névlegesen 3 kg alá kerül, de mindössze 95 g tartalékkal és mérés nélkül: **a cél nincs igazolva**; a nehezebb választás meghaladja. Elfogadáshoz minden csoportot ténylegesen meg kell mérni, valódi slicerjelentés kell, és az összeszerelt teljes tömeg ≤3,000 kg legyen az akkumulátorral, rádió/állvány nélkül. Teherhordó fészket, fogat, tengelyt ne vékonyíts tömeg kozmetikázására. Ha a tényleges beszerzés meghaladja a keretet, gyártás előtt állj meg és vizsgálj megmunkált fémszerkezetet vagy más architektúrát; ne közölj ≤3 kg-os eredményt.

BASE-ellenőrzés: négy STL CGAL figyelmeztetés nélkül, zárt/irányított élekkel; lemez DXF-ek, teljes szerelvény CSG. Node-tesztek ellenőrzik a középtávot, pontos szíjhosszt, áttételt, körülfogást, apilást és hálókat. Két változat összesen hat Node-tesztje sikeres. Szilárdsági elemzés, beszállítói rajz, teljes ütközési burkoló és fizikai teszt nem készült. Export/audit: `cad\export-belt.ps1`, `tests\mechanical-belt.test.cjs`, `tests\mechanical-belt-mass.cjs`.

### Kezdeti BuildLight: jelöltválasztás (a fenti carrier-frissítés az elsődleges)

Gyártói termékoldalak dokumentációs áttekintése 2026. október 10-én; nem történt vásárlás, mérés vagy új szerkezeti módosítás:

- [Pololu 1207 / SOYO SY35ST26-0284A](https://www.pololu.com/product/1207): motoronként közzétett **130 g**, NEMA14, 35×35×26 mm, 200 lépés/fordulat, 280 mA/fázis, 7,4 V névleges tekercsfeszültség, 650 g·cm ≈ 0,0637 Nm tartónyomaték. A **D5 tengely 21 mm-re nyúlik ki: NEM kompatibilis** a jelenlegi BASE 26 mm-es igényével. Ne hagyd jóvá és ne állítsd, hogy illeszkedik. Később az első 20T tárcsa agyának motor felé fordítását lehet vizsgálni beszállítói rajzzal és új axiális ellenőrzéssel, vagy meghatározott, megtámasztott fém tengelykapcsolóval; ASA tengelyhosszabbítót ne használj. Áram és dinamikus nyomatékgörbe próbát igényel; a tartónyomaték nem engedélyezi az 500 g-os terhet.
- [TalentCell YB1203000-USB](https://talentcell.com/lithium-ion-battery/12v/yb1203000-usb.html): közzétett „**kb. 190 g**”, 11,1 V, 3000 mAh ≈ 33,3 Wh névleges; kimenet **9–12,6 V / legfeljebb 3 A**, illetve 5 V / legfeljebb 2 A. A tényleges akkumulátor nem garantáltan 190 g; mérd meg. Nedvesség/eső kerülendő, csomagot felnyitni tilos, csak a megfelelő töltőt használd. Védelmi rendszerrel/carrierrel/szabályozóval való kompatibilitása a PCB-ügynök jóváhagyására vár; az 5 V-os kimenet nem motor-táp, a 12 V nem feltétlenül szabályozott. Az alulfeszültségi és egyidejű terhelési tartalékot biztosítsd.

Az egycellás, kis tömegű akkumulátor rögtönzött boost-átalakítóval elvetve: veszteség, áram és védelem miatt nem feltétlenül megfelelő. A 3 mm-es lemezeket, acél támaszokat, csapágyakat és mechanikus parkolórögzítést nem vékonyítjuk tömegcsökkentésként.

Az alábbi táblázat **feltételes BuildLight beszerzési/gyártási terv**. Csak a motor és akkumulátor terméktömege van publikálva; a többi csoport **tömegplafon**, nem beszállítói adat. Csoport csak rajz/kiválasztás/mérés után fogadható el, ha a határon belül van. Nem lezárt BOM és nem bizonyíték ≤3 kg-ra.

| Csoport | Határ/jelölt kg | Alap és feltétel |
|---|---:|---|
| Minden ASA-darab és doboz | 0,460 | Slicer-/mérési cél; jelenlegi tömör 0,862; infillből nem garantálható |
| Két Pololu 1207 motor | 0,260 | Gyártó szerint 130 g/db; a 21 mm-es tengely jelenleg nem illik |
| Nyolc fém tárcsa | 0,160 | Beszerzési határ; valódi rajz/tömeg függő |
| Négy szíj | 0,020 | Beszerzési határ; ellenőrizhető GT2 specifikáció függő |
| Nyolc csapágy | 0,130 | Beszerzési határ; 4×608 és 4×6000 megtartandó |
| 8×60 és 10×89 acéltengelyek | 0,169 | Geometriai számítás, támaszok nem változtathatók |
| 3 mm lemezek, EL-támasz és tálca | 0,680 | Geometria/sűrűség/tartalék; vastagság nem csökkenthető |
| Távtartók, csavarok, reteszek, U-bilincsek és parking | 0,150 | Csoportplafon; fék/parking vagy hardver nem hagyható el |
| Antennák, üvegszál, koax és RF-hálózatok | 0,360 | Alumínium csoportplafon; erősítés/tömeg nincs validálva |
| NYÁK, meghajtók, GNSS, kábel, biztosíték és védelem | 0,100 | PCB-hardver cél, függő; csatlakozók is benne |
| TalentCell YB1203000-USB | 0,190 | „Kb.” gyártói adat; az egység lemérendő |
| **Feltételes részösszeg** | **2,679** | Nem mért tömeg és nem jóváhagyott összeállítás |
| Tartalék 3,000-ig | **0,321** | Többletkábel, eltérés, motoradapter, dobozbővítés |

**A ≤3 kg prioritás fizikailag még nem teljesült.** A 0,460 kg ASA-keret a teljes tömör térfogat 53,4%-ának felel meg; csak a megfelelő falakkal/merevítésekkel végzett slicerjelentés mutatja meg, elérhető-e gyengítés nélkül. A korábbi 75%-os anyagbecslés 0,646 kg. Ha a slicer 0,646 kg-ot kíván, a részösszeg 2,865 kg-ra nő, tartaléka 0,135 kg. A 21 mm motor tengelye mechanikai módosítást igényel; a NYÁK alapterülete meghaladhatja a régi 124×64 mm-es belső teret és új dobozt igényelhet, fogyasztva a tartalékot. E függőségeket ne rejtsd el feltételes terv jóváhagyottként bemutatásához.

33,3 Wh-s akkumulátorra szemléltető, nem mért üzemidő: feltételezett 80%-os használható energia 26,6 Wh; 10/15/20 W teljes fogyasztás mellett 2,66/1,77/1,33 óra. Nem vizsgált üzemidő, és a rádiót sem tartalmazza. Valós aktív időt a motoráram, meghajtók, Wi-Fi/GNSS, fékezés és veszteségek befolyásolják; egész napos üzemet ne ígérj. Kisebb Wh-értékű másik akkumulátor csak elektromos/biztonsági követelmények, publikált tömeg és áramkorlátok után választható; az akkumulátort a tömegösszegből nem szabad kihagyni.

BuildLight elfogadás: kompatibilis rajzok, szerelési/terhelési próba, slicer ≤ plafon, csoportonkénti mérés, összesen ≤3,000 kg **a NYÁK-kal és akkumulátorral együtt**. Bármelyik kapu sikertelensége esetén vissza kell térni a tervezéshez/kiválasztáshoz; a feltételes költségvetés nem minősíthető kész terméknek.

Saját paraméteres terv, nem kereskedelmi termék rekonstrukciója, illetve harmadik fél fájljainak/képernyőképének másolata. **A prototípus nincs összeszerelve, terhelésen kipróbálva, antennái RF-ben validálva.** Helyes STL nem jelent működő mechanizmust, szilárdságot, minden mozgáshelyzet ütközésmentességét vagy jó állóhullám-arányt. A felhasználó az eredeti hardverhez **CERN-OHL-S-2.0**, saját szoftverhez **MIT** licencet választott; a hatókör és szövegek a `NOTICE.md`/`LICENSES` dokumentumokban vannak. A külső hivatkozások saját licencei változatlanok; ismeretlen licencű forrásokat itt nem terjesztünk tovább. Ez a helyi átadás nem jelent távoli közzétételt. Szerzőség és köszönet: a koordinátor által Anatol EA5KAO, Diego EA5JEF és Pedro Roca Molina számára készített `AUTHORS.md`, `ACKNOWLEDGEMENTS.md`, `DISCLAIMER.md` fájlokban. A [Bricohams](https://bricohams.org) oktatási kezdeményezés nem jelent gyártói vagy idézett projektbeli jóváhagyást. Kiskorúak felnőtt felügyeletét igénylik; engedély/licenc nélkül adni tilos. Firmware betöltése előtt válaszd le a motorokat és RF-et, használj védett tápot és ellenőrizd a tűkiosztást; prototípus flashelése nem igazolja a hardver jóváhagyását. Az irányadó cél **≤3 kg állvány és rádió nélkül**, nem mért tömeg. Az összeállítási geometria befoglalókat/fő darabokat mutat; csavarok, anyák, kábelek, fonatok, végállásbütykök, hibridek és fém burkolat a szerelési útmutató szerinti tényleges elemek, nem nyomtatható STL-ek.

## Fájlok és önálló használat

- `cad\station.scad`: OpenSCAD; `part="assembly"` mutatja az összeállítást.
- `cad\parameters.scad`: mm/fok paraméterek, ASA, hézagok és frekvenciák.
- `cad\gears.scad`: számított valódi evolvens fogazat, nem dekoratív fogak.
- `cad\mechanical.scad`: reduktorok, tartók és interfészek.
- `cad\antenna.scad`: külön antenna 145 és 435 MHz-re.
- `cad\export.ps1`: CGAL-render alkatrészenként és STL-ellenőrzés.
- `tests\mechanical-math.cjs`: számítások/fogoldal-mintavételezés; Node-csomag nélkül.
- `tests\mechanical-stl.cjs`: véges háromszögek, zárt és irányított élek, degenerált háromszögek hiánya és pozitív orientált térfogat.
- `bom\mechanical.csv`: alapmennyiségek, anyagok és irányadó tömegkeret.

Exportálható selectorok: `sun1`, `sun2`, `planet`, `ring`, `carrier1`, `carrier2`, `motor_plate`, `intermediate_plate`, `output_plate`, `keeper608`, `keeper6000`, `spacer15`, `spacer9`, `spacer38`, `spacer6` (segéd), `tripod_base`, `output_flange`, `elevation_bracket`, `saddle20`, `saddle25`, `saddle32`, `flat_adapter`, `limit_bracket`, `magnet_holder`, `sensor_bracket`, `radio_cradle`, `enclosure`, `enclosure_lid`, `diplexor_box`, `diplexor_lid`, `antenna_hub`, `band_bridge`, `arm_socket`, `coupon`. A `gearbox`, `antenna145`, `antenna435`, `assembly` összeszerelési nézet, az egyesült modellt ne nyomtasd egyetlen alkatrészként. Az `assembly.csg` megőrzi az összeállítást. Mozgó darabokat összeolvasztó összeszerelt STL nem készül.

A hivatalos **OpenSCAD 2021.01 Windows x64 ZIP** innen lett letöltve: <https://files.openscad.org/OpenSCAD-2021.01-x86-64.zip>, a `cad\tools` alatt elkülönítve, globális telepítés nélkül. Ismétlés:

```powershell
Set-Location 'C:\Users\anatol.lopez\Documents\PortableSatStation'
& '.\cad\export.ps1' -Node 'HELYI_ÚTVONAL\node.exe'
& 'HELYI_ÚTVONAL\node.exe' '.\tests\mechanical-math.cjs'
```

Más hivatalos futtatható fájl a `-OpenSCAD` opcióval adható meg. Az egyedi render naplók `cad\stl\*.render.log` alatt vannak. A létrehozás során használt Node a munkamenet elkülönített eszközkönyvtárában volt; nem a CAD függősége és nem települ rendszerre.

## Reduktor: tengelyenként két planetáris fokozat

A kezdeti választás **egyenes fogazat**, nem kettős ferde/herringbone: elkerüli a gyártási axiális erőket, könnyebb a fogkapcsolat mérése, kisebb idő/költség. A herringbone csökkentheti a nettó axiális erőt, de **a holtjátékot**, hajlást vagy nyomtatási hibát nem szünteti meg. Nem kínálunk ellenőrizetlen ferde fogazást kész opcióként.

Modul 1,5; nyomásszög 20°; napkerék **18**, bolygó **27**, belső gyűrű **72**, három bolygó 120°-onként. Osztósugarak 13,5 / 20,25 / 54 mm; bolygóközépponti sugár **33,75 mm**. Gyűrű külső átmérő **124 mm**, hogy a foggyök mögötti fal 6,125 mm legyen; ez szándékosan nagyobb a vékony fal kb. 114 mm-es befoglalójánál. Hasznos fogszélesség 12 mm; a gyűrű fizikai szélessége 17 mm.

- `R=S+2P=72`: a külső és belső fogkapcsolat helyes.
- `(S+R)/3=30`: három bolygó egész fogosztású összeszerelési feltétele.
- Rögzített gyűrű: `i=1+R/S=5`; két fokozat **25:1**.
- Profilkorrekció nélküli elméleti minimális fogszám `ceil(2/sin²20°)=18`; profilkorrekció nélküli 12 fogú napkereket nem alkalmazunk. Rejtett profilkorrekció nincs.
- Külső fogfej `rp+m`, fogláb `rp-m-0.25m`; gyűrű fogfej `rp-m`, fogláb `rp+m+0.25m`. Névleges radiális hézag **0,375 mm**.
- Fogvastagság-csökkentés foganként `backlash/2=0.125 mm` az osztókörön; névleges teljes érintőirányú ráhagyás **0,25 mm fogpáronként**, nem garantált kimeneti holtjáték. A próbadarabnál 0,20/0,25/0,30 értéket vizsgáld. ASA-kopással nő a holtjáték.
- A gyűrű **belső** evolvens; a fog a külső gyök felé szélesedik. A gyűrű rögzített tájolása csak a fogaknál tartalmaz 2,5° fázist; rögzítőfuratok a 30+60k fokos helyzetben maradnak. Napfázis 0°, bolygó `középszög+180−180/27`. A fázisokat önkényesen ne változtasd.

### Tengelyirányú apilás reduktoronként

A lokális koordináták a motor homloklapjától értendők, `z=0`. A távtartók és támaszok valódi hézagot adnak; STL-eket mérés nélkül ne helyezz egymásra a lista sorrendjében.

| Elem | z-tartomány mm | Részlet |
|---|---:|---|
| Előzetes motor | −34..0 | 35 mm-es homloklap; végleges motorrajz az irányadó |
| Motorlap | 0..8 | Előzetes 26-os furattáv, M3, 23 központi nyílás |
| Nap1 agy / fogak1 | 4..12 / 12..24 | Motor tengelye 5; M3 radiális betét/csavar |
| Rögzített gyűrű1 | 9..26 | Hat M3 összekötő rúd |
| Bolygók1 / vállak | 12..24 / 10..33 | OD6 ID4 L12 fém persely |
| Bolygótartó1 / agy | 26..32 / 32..40 | 2 mm fogfelületi hézag |
| Közbenső 8-as tengely | 26..62 | Acél; csapok z=36 és 58 |
| 608 lap / csapágy | 41..50 / 42..49 | Rögzítő 50..53; axiális játék kalibrálandó |
| Nap2 agy / fogak2 | 54..62 / 62..74 | 1 mm szabad tér a rögzítőhöz |
| Rögzített gyűrű2 | 59..76 | 9-es távtartók z=50-től |
| Bolygók2 / vállak | 62..74 / 60..83 | Alátét és anya a tartó mögött |
| Bolygótartó2 / agy | 76..82 / 82..90 | Kimenő acél10, csap z=86 |
| Kimenő támasz1 | Lap 91..101, 6000: 92..100 | Rögzítő 101..104 |
| Kimenő támasz2 | Lap 110..120, 6000: 111..119 | Rögzítő 120..123; középtáv 19 |
| 10-es tengely | 76..153 | L77; csapok z=86/136/149 |
| Terhelőkarima | 124..142 | Tárcsa 124..130, agy 130..142 |
| Mágneshordozó | 145..157 | Az utolsó 8 mm-es tengelyrészen ül; csap z=149 |
| NYÁK-tartó | 159..162 | Névleges mágnes-táv 2 mm; valós NYÁK-hoz igazítandó |

Kimenetenként két **6000 10×26×8**, közbensőn **608 8×22×7** csapágy. A 10-es tengelycsapágyat ne nevezd 608-nak. A csapágyak külső gyűrűje 1 mm-es vállra támaszkodik. A rögzítő központi nyílása az ID+1; állítóalátét csak a külső gyűrűre kerüljön, hogy a belső gyűrű szabadon fusson. Ne ASA-sajtolt illesztésre bízd a megtartást. A 12 bolygó **6×4×12-es bronzperselyt** és 4 mm-es acélvállat kap; nem modellezünk lehetetlen átmérőjű kereskedelmi csapágyat.

Az első bolygótartó fizikailag a 8-as tengelyen, két M3 csappal hajtja a 2. napkereket. A második tartó és karima fémcsapokkal csatlakozik a 10-es tengelyhez. Tengelyt merőleges sablonnal fúrj, sorjázd és fárasztópróbázd: a lyukak csökkentik a keresztmetszetet és repedésindító helyek. M3 átmenőcsavar önzáró anyával; nyomtatott menet vagy ragasztó önmagában nem nyomatékátvivő. Jelentős terhelést ne csak hernyócsavarra bízz.

### Szerelési és illesztési ellenőrzés

1. Ellenőrizd a kiválasztott NEMA14 gyártói rajzát: a 35 mm névleges osztály nem igazolja a 35 mm-es házat, 26 furattávot, 34 mm hosszúságot, 5-ös tengelyt vagy nyomatékot. Nyomtatás előtt igazítsd a CAD-t.
2. Nyomtass illesztési próbadarabot: 8,0/8,1/8,2/8,3 mm furatok. Valós acélon vizsgáld; kezdeti `fit` átmérőirányú értéke 0,25. Próbáld a 22/26-os fészket, betéteket, 4-es rudat és M4-et is.
3. Tisztítsd ki a gyököket, sorját és áthidalásokat. Először egy nap/bolygó/gyűrű fogpárt szerelj. Kézzel, teljes fordulaton ellenőrizd a sima mozgást, festékkel jelöld az érintkezést. ASA-kompatibilis kenőanyag ne jusson RF-csatlakozókra.
4. Szereld be az 1. napkereket/motort, majd a három bolygót a fenti fázissal, persellyel, vállas csavarral, alátéttel és 1. tartóval. Mért axiális játék legyen **0,2–0,4 mm**. A váll szorítsa a tartót, ne fogja be a bolygót. A kereskedelmi vállhossz alátétet/vágást igényelhet; ne feltételezd, hogy egy szokásos csavar megfelel.
5. Szereld be a 8-as tengelyt, 608-as lapot, 15-ös távtartókat, csapágyat és rögzítőt. A tartó/agyrész z=40-nél véget ér, a lap z=41-nél kezdődik; ne érjenek össze.
6. Szereld a 2. napkereket z=54-től, csap z=58; a 2. gyűrű z=59-től, majd a második három bolygót és tartót.
7. Szereld a 15-ös távtartókat, első támaszt, 9-es távtartókat és második támaszt. A két 6000-est meghúzás előtt ideiglenes tengellyel igazítsd, csavarokkal ne kényszerítsd helyre.
8. Szereld a 10-es tengelyt, karimát és z=136-os csapot, mágneshordozót és z=149-es csapot. Az AS5600-at a kiválasztott NYÁK-on koaxiálisan szereld. A 16×16-os furatminta előzetes. A tartóláb a második rögzített lemez z=120 síkjára kerül, két M3-mal x=−55/y=±10 helyen; torony x=−66..−62. Rögzítés az **adott tengely saját álló házához**, ne a mágneshordozóhoz; antenna terhe ne menjen a NYÁK-on/mágnesen át. Ellenőrizd a valódi NYÁK-vastagságot/forrasztásokat: a nyomtatott lap nem elektronika. Az érzékelő **nem foroghat együtt** a karimával, bölcsővel, EL-tartóval AZ körül; a talp csak a saját tengelyházán legyen rögzítve.
9. EL-en ismételd meg. A motor homloklapja hat M3-mal kerül a tartó oldalára; 38×38-as nyílás kell az előzetes 35 mm-es motorhoz. Belépő kábeleket tehermentesítsd.
10. AZ-alap z=0..12; a 38-as távtartók a reduktor homloklapját z=50-re emelik, így a motor z=16..50. Emelés nélkül a motor az alaphoz/állványhoz ütődne. AZ rudak kb. 180, EL rudak 130 mm; csak a valós apilás lemérése után vágd őket.
11. Az AZ karima z=174..192 helyen hordja az EL-t. Az EL-nyereg saját tengelyén lokális z=130-tól szerelhető, 22-es szenzorkivágással, 35 mm-rel oldalra eltolt és 24 mm magasan álló gémmel. Szenzor a z=159 síkban, szabadon a műanyag felett (nyereg z=154-ig); még a 32-es gém is elkerüli a szenzorhidat (lap x=12/y=±12) az EL 0..90° tartományában. Az EL tengely 84 mm-rel van a saját alaplap fölött: a reduktor alsó éle szabad az alap és az AZ-szenzorhíd felett. Négy, ±15,556 mm-es pozícióban csavarozz (31,112-es négyzet); fizikailag ellenőrizd a csavarok és érzékelő hézagát.
12. Szerelj négy NC kapcsolót, állítható fém bütyköt és egymástól független mechanikus ütközőt. A konzol 18 mm-es furattávja előzetes; mérd meg a mikrokapcsolót. Csavarral rögzíts az alaphoz/lemezhez, ragasztóval ne. A CAD tartókat exportál, univerzális bütyököt nem; a kapcsolóhoz és fékezési tartalékhoz egyedit kell készíteni. Működést AZ ±180° és EL 0/90° előtt mérd; kezdeti szoftverhatár ±170° és 5..85°. AZ folyamatos forgását tiltsd, mert a koax/kábelek felcsavarodnak.

## Interfészek, hordozhatóság és rádió

A teljes antenna négy M4 csavarral oldható le a karimáról/nyeregről; felemelés előtt a koaxot a hibridekről bontsd. RF-gémek 20 mm-es üvegszálból, kiválasztott 20/25/32 szerkezeti gém-/bilincsmérettel. A nyergek két **M5 fém U-bilincset** használnak, x=±22 helyzetben; lábak y=35±(átmérő/2+5), lábköz 30/35/42 mm. Olyan valódi bilincset válassz, amely illik e távolsághoz és legalább 45 mm hasznos menethosszhoz; használj fém teherelosztó lemezt, nagy alátétet és önzáró anyát. Ne lapítsd össze a csövet. Sík felülethez `flat_adapter`, közös M4 minta és négy M5 54×36-on, mind átmenő fémszerelvénnyel. Terhelt bilincset ne nyomtass menettel.

Állvány: befogott **1/4-20 UNC fém anya** (kezdeti 11,1 mm lapméret, 5,6 magas), amely a talp bontásával hozzáférhető; ezenkívül kereskedelmi **3/8-16 → 1/4-20 fémadapter**. Nyomtatott UNC-menet nincs. Ellenőrizd a csavar hosszát: ne érjen fenékre, nyomást ossz el, legyen az anyának fém megtartása és biztonsági kötél az állványhoz. Ez a talp nem igazolja az állvány/fej stabilitását vagy oldalirányú teherbírását. Szélben/egyenetlen talajon biztosítsd a lábakat, ballasztot és a területet; senki ne álljon alatta.

Az RT3S az **állványhoz rögzített, álló alapon/tálcán** marad, ne az AZ karimán/antennán. Kezdeti burkoló 61×39×131 mm oldalanként 2 mm hézaggal: **előzetes, a felhasználó tényleges készülékén mérendő**, kapcsokkal, PTT-gombbal, csatlakozókkal/akkumulátorral. A bölcső nem igazol vízzárást vagy illeszkedést; használat előtt kézzel próbáld ki, két heveder a hornyokban és harmadik biztonsági kötél. Ne takard a hűtést, hangszórót, kezelőszerveket. A rádió az antenna bontása nélkül kivehető.

A base mellett megjelenő dobozokhoz **az állványra rögzített fém tálca** kell; nem lóghatnak a levegőben vagy az antennán. A diplexer külön doboza 80×70×35 mm, M3-mal levehető fedéllel. A választott diplexer/csatlakozók alapján változtasd a méretet és nyílásokat. Az ASA **nem RF-árnyékoló**: a 74×64×32 mm-es belső falat/feneket/fedelet 0,3 mm alumíniumlemezzel, vezető illesztéssel, fém-fém csavarozással és a berendezéshez illeszkedő RF-földeléssel béleld. Sorja/zárlat ellen szigetelő távtartókat alkalmazz. Műanyagfestés nem bizonyít EMC-t, tömítettséget vagy árnyékolást. A 130×70×45-ös elektronikai doboznak fedél, kábelátvezető és csepphurok kell; esőben ne energizáld.

Opcionális befoglaló referencia a `DuplexorSpaceQuad` nyilvános projekt `f5c7dc375ed7b9882f52bd7757deaf44cd422b81` commitja. Közzétett SMA-nyák 37×23 mm, doboz 45,2×27,6×14,1 mm (Amphenol 132289, két M2×10); BNC NYÁK 55,5×33 mm, doboz 59,9×37,6×23,5 mm (Amphenol B6252HB-NPP3G-50, két M2×12). Ezek **publikált méretek, nem a mi egységünk mérései**. Mindkét befoglaló névlegesen elfér a 74×64×32 mm rekeszben, de ez nem igazolja három csatlakozó, dugók, anyák, koaxok és hajlítási sugarak helyét. A CAD általános 10 mm-es nyílásai **nem SMA/BNC sablonok**; a valós csatlakozó mérése után módosíts, vagy a kábelt átvezetőn vezesd ki.

A külső projekt becsült footprint-csatlakozóméretei: SMA fül 9,6×1,9, NYÁK feletti tengely 0,4; nyílás 6,8 mm. BNC test a NYÁK fölött 14,8, tengely 7,5; nyílás 14,9 mm. Rögzítés/fúrás előtt tolómérővel ellenőrizd; becsült csatlakozó ne tartsa a panelt. Az idézett 2/2/1,6 mm fal/fenék/tető és 0,15 mm tolerancia nem helyettesíti a saját ASA kalibrálását. Ez **háromportos diplexer**, nem kvadratúrahibrid; két külön 90°-os hálózat továbbra is kell a keresztezett dipólusokhoz. Az ideális szimuláció és a 0805-ös elemek 5–10 W jelzése nem igazol valós teljesítményt, veszteséget, kompatibilitást vagy hőmérsékletet. CAD-fájlokat/áramkört nem használunk fel.

Külső referenciák sem helyettesítik az állomás tesztjét. A LibreSat v1.0 saját nyilatkozata szerint együtt nem építették/mérték; NEMA17-et és 25:1 cikloidot használ, nem a mi NEMA14/planetáris hajtásunkat. Terhelés-, szél- és hatásfokfeltételezései nem átvihető minősítések. A LibreDMR/OpenGD77 hivatalos útmutatója igazolja az RT3S műholdképernyő Doppler TX/RX, AZ/EL, kézi hely/UTC és CPS Kepler-elemek funkcióját; ez nem bizonyít CAT-ot vagy teljes duplexet. A mi bölcsénk fizikai mérése még függő.

## Eredeti antenna: két keresztezett, reflektoros szerelvény

Nem skálázunk 449 MHz-es tervet, hogy „kétsávosnak” nevezzük. Mindegyik sávnak saját, két ortogonális dipólból és két ortogonális reflektorból álló geometriája van; a kezdeti számítás:

```text
lambda_mm = 299792.458 / f_MHz
driven_tip_to_tip = lambda_mm / 2 * 0.92
reflector_tip_to_tip = driven_tip_to_tip * 1.05
separation = 0.225 * lambda_mm
```

| Sáv | λ (mm) | Dipól, vég–vég | Reflektor, vég–vég | Síkok távolsága |
|---|---:|---:|---:|---:|
| 145 MHz | 2067,53 | 951,07 | 998,62 | 465,20 |
| 435 MHz | 689,18 | 317,02 | 332,87 | 155,07 |

Ezek **kezdeti becslések**, nem nyereség-, iránykarakterisztika-, SWR-, polarizáció- vagy illesztési mérés/szimuláció. A zsanérok, fonatok, gémek, reflektor, doboz/radio és **VHF/UHF kölcsönös csatolás** hatása nincs validálva. A gémek közötti szemléltető 80 mm oldalirányú távolság nem igazolt RF-távolság. A gém eltolásával való mechanikai kiegyensúlyozás nem igazol RF-mintát. Három 20-as furatú nyomtatott híd köti össze mindkét RF-gémet és a 175 mm-es központi szerkezeti gémet. M4 átmenő csavar nagy alátéttel és fém gallérral; ASA menet ne legyen teherút. A híd a hosszirányú egyensúlyi síktól 50 mm-re kerüljön, hogy ne foglalja a nyereg helyét. A két sugárzóközép egybeesik hosszirányban, de az eltérő tömegeket ténylegesen ki kell egyensúlyozni. A 25/32 mm csak szerkezeti gém/nyereg alternatíva; az RF-gém és híd marad 20 mm; szerkezeti méretváltáskor fém/dielektromos adapterhüvely kell.

### Vágás, zsanérok és szállítható szakaszok

A 4 mm-es rúd előzetes. A vég–vég méretbe a 24 mm-es középső rés beletartozik: geometriai félkar `L/2−12`; kb. 463,53 mm a VHF gerjesztettnél, 487,31 mm a reflektornál. Az M4 zsanér 36-os sugáron van; fix vezető stub r=12..28 (**16 mm**), külső kar r=46-tól. A 18 mm-es zsanérhézagot **rugalmas rézfonat** hidalja át. Valós elektromos hosszát a képlet nem kezeli; minden fonat legyen azonos, VNA-val hangold, és ne tekintsd az ASA rést vezetőnek. M4 acéltengely és r=42 helyen M3 keresztcsavar pozitívan rögzíti a kihajtott kart. r=54-nél M3 csavar betéttel/fémhüvellyel fogja meg a rudat, ne ASA menetben. Súrlódás nem elég önmagában.

| Fémrész | Mennyiség | Névleges geometriai hossz (mm) | Javasolt kezdeti vágási hossz |
|---|---:|---:|---:|
| r=12..28 stub mindkét sávon | 16 | 16 | 16; hangolásra ne vágd |
| VHF gerjesztett külső rész | 4 kar, karonként 2 szakasz | 429,53 = 214,77+214,77 | 2×220 karonként |
| VHF reflektor külső rész | 4 kar, karonként 2 szakasz | 453,31 = 226,65+226,65 | 2×232 karonként |
| UHF gerjesztett külső rész | 4 | 112,51 | egyenként 118 |
| UHF reflektor külső rész | 4 | 120,44 | egyenként 126 |
| VHF összekötő hüvely | 8 | 50, OD8 ID4 | ID a tényleges fémhez igazítandó |
| VHF dielektromos gém | 2 szakasz | kb. 245/db | összeszerelve sík–sík 465,20 |
| UHF dielektromos gém | 1 | kb. 180 | sík–sík 155,07 |

**Vezető** sárgaréz-/alumíniumhüvely: a toldás **homlokillesztésű** (az 50 mm-t nem kell levonni), oldalanként 25 mm betolás, két merőleges, 2 mm-es pozitív fém csap/csavar. Alumínium legyen tiszta, kompatibilis oxidációgátló pasztával. 4 mm-es rudat M3-mal ne fúrj, amíg a szilárdságot nem vizsgáltad. A kis hüvelycsapok az RF rudakon vannak, különböznek a reduktorok M3 csapjaitól. A nézetben látható hüvely csak befoglaló; a két fél valós illesztésénél legyen. Külső szegmensek eltávolításával és VHF gém bontásával szállításkor egyik fém/gémdarab sem hosszabb 450 mm-nél. Topolt hosszra, orientációs jelre, elfordulás- és kihúzódásgátlóra szereld; a szabadon csúszó teleszkópos toldás nem tartja a rezonanciát/folytonosságot. Szállításkor hajtsd össze a zsanérokat és rögzítsd a karokat. Az `antenna_arm_angle=90` nézet csak szemléltető kinematika, nem vizsgálja minden fonat/hüvely ütközését.

A reflektorok elektromos folytonosságát **fémhidakkal, a gém körül** biztosítsd, a keresztezésen kívül; ha két tengely keresztezi egymást, eltérő magasságban fussanak. A gerjesztett dipól két kivezetését ne hidald át és ne kösd gémhez. Karok/reflektorok külön levehetők aggyal/zsanérral; jegyezd fel a bontási sorrendet, ne veszítsd el a rögzítőket.

A **50 Ω illesztést** nem nyomtatott agy biztosítja. Minden sávhoz megfelelő illesztő/balun kell, továbbá külső, az adott polarizációhoz beállított 90°-os hibrid azonos kábelhosszakkal. Ellentétes körpolarizáció fázisát csak ellenőrzés után fordítsd meg. Két külön hálózat után valódi, 145/435 MHz-re és teljesítményre/veszteségre megfelelő diplexer. Két dipól párhuzamos összekötése nem eredményez automatikusan 50 Ω-ot, és e geometria sem 50 Ω-os. Csak fém vezeti az RF-et, nyomtatott huzal nem. Kis teljesítményű VNA-val hangolj, előbb külön-külön, majd az állomás teljes valós elrendezésében. Apró, szimmetrikus lépésekben vágj. Tartsa be az engedélyezési és RF-expozíciós szabályokat; senki ne érjen rudakhoz, adás alatt álló antennához vagy mozgó alkatrészhez.

Az `docs\ACCEPTANCE.md` RF-számai szűrési célok, nem igazolt teljesítmények: SWR≤1,5 középen / ≤2 csatornákon, hibrid amplitúdó-egyensúly ≤0,5 dB és fázis 90°±5°, diplexer veszteség ≤1 dB, return loss ≥14 dB és izoláció ≥40 dB. E célok teljesítése sem bizonyítja a vétel biztonságát adás közben, és nem engedélyez teljes duplexet a vevő, teljesítmény és RF-lánc kiértékelése nélkül.

Komponensreferencia: a gyártó aktuális **Mini-Circuits QCN-3+** adatlapja 220–470 MHz tartományt jelez; a 435 benne van, a 145 **nincs**. Ne kezeld kétsávos hibridként, és ne extrapolálj a `QCN-3` utótag nélküli megnevezésre, amelynek azonossága nincs megerősítve. CMX/Anaren modell nincs kiválasztva ellenőrizhető adatlappal.

## Terhelés, nyomaték, szél és tömeg: célok, nem minősített kapacitás

Kezdeti antennatömeg-cél legfeljebb **500 g**, CG az EL-tengelytől **≤30 mm**, a teljes antenna/koax/gém összerakásával mérve. Gravitációs nyomaték: `0,5×9,81×0,03 = 0,147 Nm`. Az ábrán a gém nagyjából középen van, de ténylegesen egyensúlyozni kell; a nyereg áthelyezése, mérsékelt ellensúly vagy az antennán kívüli kiegészítők csökkenthetik a nyomatékot. Az EL-reduktor tömege AZ-inercia. Ne emelj nehéz antennát pusztán a motor tartónyomatéka alapján.

Példa, **nem a megvásárolt motor adata**: feltételezett NEMA14 dinamikus nyomatéka 0,08 Nm, fokozatonkénti hatásfok 0,65: `0,08×25×0,65²=0,845 Nm` elméleti kimenet. Ellenőrizd valódi motor görbéjét sebesség/áram, veszteség, hő és ASA-merevség mellett. A tartónyomaték nem dinamikus nyomaték. Próba előtt tengelyenkénti igényt **0,5 Nm alatt**, biztonsági tényezővel tarts; ez nem a mechanizmus/fog/csap igazolt értéke.

Konzervatív szélpélda: sűrűség 1,225 kg/m³, Cd=1,3, ekvivalens felület 0,12 m², kar 0,15 m, szél 8 m/s: `T = 0.5*rho*Cd*A*v²*kar = 0,917 Nm`; gravitációs 0,147-tel együtt **1,064 Nm**, amely meghaladja a 0,5 Nm-es sapkát és a példabeli 0,845 Nm-t. E lökés nem tekinthető megengedettnek. 5 m/s esetén 0,358+0,147≈**0,505 Nm**, már határeset. Először beltérben/szélcsendben tesztelj, erősödő szélben hajtsd össze és szereld le; az állvány/kábelek további nyomatékot adnak. 5 m/s-re vagy 3 kg-ra nincs garancia. Felügyelet nélkül ne hagyd aktív állapotban.

A CSV költségei csoportonkénti tervezési tartományok, nem bolti árak/árajánlatok. A Pxx külön költség nélkül, a filament M24-ben van. Ne számold duplán a nyereg/sík adapter alternatíváját vagy más BOM elektronikai elemét. A műanyag tömegét tömör STL térfogatból és kb. 1,07 g/cm³ ASA-sűrűségből becsüljük; infill változtat az eredményen, fém/merevítés/koax növeli. Minden kész darabot mérj; 3 kg fölött a cél nem teljesült.

### 2026. október 10-i validálás

- OpenSCAD 2021.01 CGAL-lal **34 egyedi selector STL-t** renderelt, mind a 34 napló ERROR/WARNING nélkül; az összeállítás CSG-ként készült.
- Mind a 34 STL zárt, következetesen irányított élekkel, nem degenerált háromszögekkel és pozitív térfogattal átment. Ez nem igazolja a fizikai illeszkedést/ütközésmentességet, és nem teljes önautómetszési elemzés.
- Node 22.16 ellenőrizte a 25:1 áttételt, 30-as zárást, 18-as minimális fogszámot, radiális hézagot és a napkerék egy fogfordulatának 121 mintáját: a bolygó kontúrja nem hatol a napba vagy gyűrűanyagba. Szimmetria miatt egy bolygóhármas egyenértékű. Ideális egyenes fogazatú kapcsolati tényező: külső 1,580, belső 1,944. Motor/alap méreteit, EL-tengely/alap és a 32-es gém/enkóderhíd viszonyát is ellenőrizték a megengedett negyedkörben. Teljes összeállítási ütközési söprés nem történt.
- Névleges leltár **131 nyomtatott darab**, az alternatív sík adapter nélkül. Optimalizálás utáni tömör térfogategyenérték **2,521 kg ASA**, 1,07 g/cm³ mellett. **Minden darabot tömören nyomtatva a fémek, motorok és koax előtt túllépnénk a 3 kg célon.** Infill/merevítés és valós tömeg további vizsgálatot kíván; infilltömeget nem számítottak.
- CSV mechanikai/RF tervezési tartománya **248–671 €**, nem árajánlat; a rádiót/állványt és más BOM-ban szereplő vezérlőelektronikát nem tartalmazza.

Sem nyomtatás, sem összeszerelés, szél-/nyomaték-/tömegmérés vagy RF-illesztési próba nem történt. A külső fogak gyökátmenete diszkretizált radiális ívet használ a talpkörig, nem fogmaróval generált trochoidát; az aktív fogoldalak valódi evolvensek. Ezekhez a fogakhoz ne rendelj ISO/AGMA fáradási minősítést.

### Korlátozott optimalizálás és tömegkeret

Az alap alsó mezőit kimarták, 3 mm felső héj, perem, központi anya-boss és a rudakhoz hat 14 mm-es borda megtartásával. Csak a fedelek belső felületét könnyítették, 1,6 mm-es tető, perem és középső borda megtartásával. Evolvens/gyök, tartók, tengelyek, csapágyfészkek, EL-oldallemez vagy motorrögzítés nem változott. A bordák megtartott geometriák, **nem számított vagy tesztelt szilárdság**; könnyítés után vizsgáld az alapot.

| STL | Korábbi térfogat mm³ | Új térfogat mm³ |
|---|---:|---:|
| tripod_base | 233270,3 | 130922,3 |
| enclosure_lid | 27191,2 | 20331,2 |
| diplexor_lid | 16691,2 | 13331,2 |

Névleges tömör ASA-megtakarítás **120,45 g**, műanyag össztömeg 2,641→2,521 kg. Három STL CGAL-lal újrarenderelve és ellenőrizve; mind a 34 végső hálót újra auditálni kell. `tests\mechanical.test.cjs`: három validáció sikeres (matematika, leltár, optimalizálás/tömeg), köztük két optimalizációs unit teszt. `export.ps1 -Only tripod_base,enclosure_lid,diplexor_lid` részkészletet generál, minden STL saját validálásával.

A fogaskerekek és tartók tömör ASA tömege névlegesen 0,579 kg; a többi 1,942 kg. **Érzékenységi példa**, nem slicereremény: a fogak/tartók 100%-át, a többi tömör térfogat 60%-át megőrizve 1,744 kg ASA adódna. A hipotetikus 60%-os anyaghányad **nem 60%-os slicer infill**; a falak/bordák/héjak nagyban befolyásolják. Ne garantáld e tömeget, és ne csökkents teherhordó támaszt csak a szám kedvéért. Használj valós slicerjelentést, a támasz/brim tömegével együtt.

| További csoport | Tervezési tömeg kg |
|---|---:|
| Két később kiválasztott NEMA14 | 0,24–0,40 |
| Két 608 és négy 6000 | 0,09–0,12 |
| Két-két 8×36 és 10×77 acéltengely | 0,1234 névleges geometriai |
| 12 M3 rúd: hat 180 és hat 130 mm | 0,1032 névleges geometriai |
| 12 acélváll 4×23, fej/anya nélkül | 0,0272 névleges geometriai |
| Perselyek/csapok/csavarok/U-bilincs/adapter | 0,12–0,22 |
| Alumínium RF rudak/hüvelyek, üvegszál gémszakaszok | 0,25–0,40 |
| Koax/90°-os hálózatok/diplexer/bélés | 0,18–0,30 |
| Vezérlő/meghajtók/kábelezés | 0,08–0,15 |
| Hordozható táp/akkumulátor | 0,25–0,45 |
| **Részösszeg ASA, rádió és állvány nélkül** | **1,464–2,294** |

A valós motor/csapágy/radio/akkumulátor beszállítói adatot és tömeget ellenőrizni kell. Acél számításához 7,85 g/cm³ sűrűséget használtak; a furatlevonás és fej nincs benne, csavarozási csoport tartalékolja. Alumínium helyett réz/sárgaréz RF-elem jelentősen növelheti a tömeget. Tálca/merevítések/hevederek tartalékot igényelnek; egyik tartomány sem kitalált beszállítói adat.

Még az 1,744 kg-os hipotetikus nyomtatási eset is **3,208–4,038 kg** össztömeget ad; tömör ASA-val **3,985–4,815 kg**. A robusztus 124 mm-es tervezés táppal együtt **nem éri el és nem igazolja a ≤3 kg célt**. Ne hirdesd 3 kg-os állomásnak. A célhoz új, fizikai döntés kell (optimalizált megmunkált/lemezes fém, nem szállított külső táp, kisebb architektúra vagy tesztelt szerkezeti módosítás); ne vékonyíts fogat/támaszt találomra. A teljes antennát is meg kell mérni; az 500 g cél fonattal/koaxszal/hardverrel túlléphető.

### Mechanikai integráció állapota

A nyomatéklánc, motor-/tengely-/csapágy-méretek definiáltak és rendereltek. A NEMA14 **26 mm furattáv előzetes**, az 5 mm-es tengely pedig csak megvásárolt motorrajz alapján fogadható el. Nincs általános NEMA14-kompatibilitási garancia. A teljes CSG nem végleges, igazolt összeszerelés: hiányoznak a konkrét végállásbütyök/ütköző geometriák, csavarfejek/anyák/alátétek, végleges diplexer/kábelrögzítés és mozgási söprés. Koaxiális illesztés, csapok, axiális játék, valódi NYÁK és kábelezés próbapadi szerelést kíván. Méretellenőrzés részleges, **nem bizonyítja az összes ütközés hiányát**. Végső minősítés: reprodukálható moduláris CAD-prototípus, nem üzemkész vagy assembly-tested állomás.

## ASA-nyomtatás, hibák és elfogadás

A fogaskerekeket Z tengellyel nyomtasd, 0,15–0,20 mm réteggel és legalább 5 peremmel; a fogak/agyrészek lokálisan 100%-os kitöltést kapjanak. A nagy darabokra kezdetben 30–45%, legalább 5 perem és borda javasolt. A koronák csavarjai körül ne csökkentsd a peremeket. Lemezek sík oldala legyen az ágyon, szükség szerint brim. EL-támasz és zsanér hajlításnak kitett; mérlegeld az élére állított nyomtatást/fém merevítést, anisotrópiát próbázd. Csak furatot dörzsárazd; félreigazítás elfedésére evolvenst ne reszelj. Csapágyat ne melegítve szerelj be. Toleranciát a valós nyomtatóval/filamenttel/lottal igazíts, ne globális méretezéssel.

Az ASA emissziót ad: a gyártó szerinti, megfelelő elszívást/szellőzést és zárt nyomtatóteret biztosítsd; a puszta zárt tér nem garantál védelmet belégzés ellen. Forró ágy/hotend, fémhez kesztyű, fúráshoz/vágáshoz szemvédelem. ASA időjárásállóbb lehet PLA-nál, de napsütés/terhelés alatt kúszhat, hőstabilitásra nincs minősítve.

Utasítsd el a repedt foggyököt, ASA-t összenyomó anyát, hajlott csapot, ovális perselyt, tengelyhez súrlódó rögzítőt, beszoruló bolygót, kitágult zsanérhornyot, elveszett csapot, feszes koaxot, növekvő holtjátékot vagy laza mágnest. A kimeneti oda-vissza holtjátékot mérőórával mérd, ne a motorlépésekből vezesd le. Igazold, hogy az AS5600 lépésvesztéskor is a kimeneti tengelyt érzékeli. A szakadt NC végállásnak le kell állítania: előbb motor nélkül próbáld a szakadt vezetéket és vészleállítást. A mechanikus ütköző nem váltja ki az elektromos tápmegszakítást.

Terepi elfogadás előtt még elvégzendő: kézi teljes ciklus; ütközés/kábel ellenőrzés AZ ±180° és EL 0..90° határon; 100 üres ciklus, 100 fokozatosan terhelt ciklus; nyomaték/áram/hő/holtjáték mérése; tápvesztés, NC végállások, állványstabilitás, antenna- és mágnesmegtartás, valós tömeg, SWR/minta/RF-expozíció, valamint ismételt összecsukás utáni folytonosság. E tesztek még nem történtek meg.
