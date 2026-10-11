# Tesztek és elfogadási kapuk


Részletes lépések, tesztpad és komponensenkénti ellenőrzőlisták: [testing/README.md](testing/README.md).

Rögzítsd a dátumot, Git-revíziót, műszereket, kezelőt, összeállítást és
eredményt. A nem mért kritérium **FÜGGŐBEN** marad; számítás alapján nem
jelölhető JÓVÁHAGYOTTNAK.

## G0: szoftver és digitális geometria

1. Fordítsd le a firmware-t a rögzített függőségekkel.
2. Futtasd a pályaszámítási, határérték-, idő- és hibásadat-teszteket.
3. Hasonlítsd össze az SGP4-et független implementációval ugyanarra a
   TLE/UTC/telephely kombinációra: a cél <=0,1 fok AZ/EL-ben, a zenittől
   távol, azonos konvenciók/geodézia mellett.
4. Ellenőrizd a mértékegységeket: a GNSS-magasság méterben legyen, a
   könyvtár az API-ja szerint működjön; szélesség/hosszúság fokban,
   UTC helyi idő korrekciója nélkül.
5. Rendereld az OpenSCAD-ben az ÖSSZES alkatrészt; ellenőrizd a zárt
   hálót, térfogatot, önmetszést és a váratlan komponensek hiányát.
6. Ellenőrizd mindkét fokozat fogkapcsolódását, a bolygók fázisát,
   csapágyakat, tengelyt, hézagokat, kötőelemeket és szerelési hozzáférést;
   a render nem helyettesíti ezt.
7. Csonka TLE, hibás ellenőrzőösszeg, régi epoch, HTML-nevek, kiesett
   forrás vagy túl nagy katalógus: egyértelmű hiba, mozgás nélkül.

## G1: mechanika RF nélkül

1. Nyomtass próbadarabokat: furat, tengely, betét, fog és persely.
   Mérd meg az ASA zsugorodását, és rögzítsd a kompenzációt; ne csiszolással
   tüntesd el a hibákat.
2. Szerelj össze egy fokozatot motor nélkül: teljes fordulat simán,
   szabadon mozgó bolygók, koncentrikusan alátámasztott kimenet.
   Ismételd meg két fokozattal.
3. Erősítsd meg a második fokozat napkerekének rögzítését az első
   bolygóhordozójához: a szabadon úszó fogaskerék nem visz át nyomatékot.
4. Ellenőrizd a motorok fizikai lekapcsolását a leállítóval és az NC
   határolókkal.
5. Indítás/újraindítás/watchdog nem okozhat forgást, és nem állíthatja
   vissza a homing állapotot.
6. Homing antenna nélkül: leválasztott vagy beragadt kapcsoló, illetve
   el nem ért kapcsoló -> timeouttal hibázzon, ne mozogjon korlátlanul.
7. Mérőórával/szögmérővel mérd meg a holtjátékot irányváltáskor, fokban
   rögzítsd.
8. Kiegyensúlyozás a célterheléssel: 0,5 kg, CG <=30 mm; használj
   másodlagos rögzítést és stabil próbapadot az állvány előtt.
9. Lassan, szél nélkül teszteld a <=2 fok RMS pontosságot és a <=5 fok
   maximális eltérést. A haladási irány és a tengely hibáját különítsd el.
10. 30 perces terheléspróba: ne legyen lépésvesztés, kilazulás vagy az
    alkatrész határértékét meghaladó hőmérséklet.
11. Validáld az AZ, EL és kábelek határait a kiszámított fékezési
    tartalékkal.
12. Mérj le mindent, a kábeleket és tápegységet is: cél <=3 kg
    rádió/állvány nélkül. Mérd meg a csomag méretét; tájékoztató cél a
    <=450 mm hossz leszerelt radiátorokkal. Ne csak a dobozt mérd.

A `calc/design.json` nyomatékköltségvetése szerint a 8 m/s PÉLDA 0,06 m2
felülettel és feltételezett 0,1 Nm-es motorral NEM teljesíti a 2-es
biztonsági tényezőt. Ezért a 8 m/s NEM engedélyezett szélhatár.
Menet közbeni nyomaték és tényleges terhelés mérése előtt kizárólag
szélmentes, ellenőrzött próbapadon üzemeltess. Minden alternatív antennát
újra kell validálni.

## G1E: hordozópanel és WebFlash, motorok táplálása előtt

1. Rögzítsd a kapcsolási rajz/PCB/Gerber revízióját, a modulok listáját
és a firmware lábkiosztását. Mind a 16 GPIO-jel egyezzen, ismétlődés nélkül.
2. Futtasd az ERC, DRC, unconnected és kapcsolási rajz/PCB paritás
ellenőrzést a dokumentált eszközzel; ne helyettesítsd azzal, hogy
létezik egy Gerber ZIP.
3. Kézzel ellenőrizd a lábnyomokat, az 1-es lábat és a DevKitC/driver
irányát, a vezetősávok áramterhelhetőségét, kapcsokat, biztosítékokat,
TVS-eket és hőelvezetést.
4. Modulok nélkül mérd meg a hálózatok folytonosságát és a zárlatmentességet;
az elektromos eljárás szerint, korlátozott tápegységgel tápláld.
5. Ellenőrizd a 12 V-ot, 5 V-ot és 3,3 V-ot a megfelelő csomópontokban;
GPIO ne kapjon 5 V-ot.
6. Ellenőrizd, hogy az ENABLE indításkor tiltott. Vizsgáld a VMOT fizikai
lekapcsolását az MCU-tól függetlenül, úgy, hogy a logika hiba jelzésére
feszültség alatt maradhat.
7. Ellenőrizd az összes érzékelő NC-nyitását és vezetékszakadását.
Vizsgáld meg a külső felhúzókat azokon a GPIO-bemeneteken, amelyeknek
nincs belső felhúzójuk.
8. Csak a kompatibilis ESP32-t flasheld, motor és rádió csatlakoztatása
nélkül. Ellenőrizd a hash-t, alkalmazás-eltolást, partíciókat és LittleFS-t.
9. A nyilvános képből hiányozzanak a titkok: USB-n történő beállításkor
ellenőrizd, hogy nem ír ki jelszót/tokent, és SETUP/újraindítás után sem
végez homingot.
10. Az NVS nincs titkosítva: védd a fizikai hozzáférést, tartalmát ne
másold Gitbe. A LittleFS frissítése felülírhatja a TLE/cache-t: dokumentáld
az előzetes mentést, és ne keverd össze az NVS megőrzését a fájlrendszer
megőrzésével.
11. A GitHub Actions/Pages külön távoli tesztet igényel; a helyben
jóváhagyott manifest nem bizonyítja a távoli engedélyt vagy a helyes
telepítést.
12. Ellenőrizd, hogy a beépített márkajelzés illeszkedik a fedélre, és
nem ütközik csatlakozókkal, csavarokkal, szellőzéssel vagy laza alkatrésszel.

## G2: passzív RF

1. Kalibráld a VNA-t a csatlakozó referencia-síkján, csatlakoztatott
rádió nélkül.
2. Mérj meg sávonként minden dipólust/reflektort és illesztőhálózatot.
3. A teljesen összeállított készletet, kábelt és rotort valós helyzetben
mérd: cél SWR <=1,5 a kiválasztott középfrekvencián és <=2 az üzemi
csatornákon. Dokumentáld a sávszélességet, ne extrapolálj.
4. Sávonként mérd a hibridet: cél eltérés <=0,5 dB és 90 +/-5 fok fázis
a kiválasztott frekvenciákon; az izolált port megfelelő lezárású legyen.
5. Mérd a diplexert: kezdeti szűrésként cél áganként <=1 dB beiktatási
veszteség, visszaverés >=14 dB és leválasztás >=40 dB. További egyidejű
vevőnél számítsd ki a szükséges leválasztást az adóteljesítményből és a
vevő maximális bemenőszintjéből, tartalékkal; a 40 dB nem garantálja
a deszenzitizáció hiányát.
6. A mintázatot, RHCP/LHCP irányt és tengelyarányt ne következtesd
kereskedelmi hibridből vagy jó SWR-ből; mérd/szimuláld az együttest.
Kezdeti cél a <=3 dB tengelyarány a műhold irányában a körpolarizáció
bejelentéséhez.
7. 50 összecsukás után ellenőrizd a folytonosságot és ismételhetőséget.
A műanyag csuklópánt nem lehet az egyetlen RF-érintkezés.

## G3: vétel és vezérlés

1. Hasonlíts össze egy átvonulást független referenciával, azonos
állomással és TLE-vel.
2. Internet nélküli AP: TLE importálása, kiválasztás, előrejelzés és
követés.
3. Zárd be a mobilt átvonulás közben: az ESP32 számítása és követése
folytatódjon.
4. GNSS-kiesés, érvénytelen UTC, régi cache, elveszett encoder esetén
ellenőrizd a dokumentált viselkedést, figyelmeztetést és biztonságos leállást.
5. Horizont alatti/nem megkezdett átvonulás, kábelcsavarodás, zenit és
elérhetetlen sebesség: a célpontot kifejezetten utasítsa el, ne irányítson
rossz célra.
6. Hasonlítsd össze a vételi zajt bekapcsolt/kikapcsolt konverterek és
motorok mellett.
7. Ismert referenciával ellenőrizd a valódi tájolást; az állvány
elmozdításakor ismételd meg, új helyen ne használd újra a kalibrációt.

## G4: engedélyezett adás

Csak ellenőrzött licenccel/engedéllyel, frekvencián és műholddal. Kezdd
minimális teljesítménnyel és megfelelő műterheléssel végzett próbapadi
tesztekkel; ellenőrizd a hálózatok és csatlakozók hőmérsékletét. Ne adj
illesztetlen hálózatra, illetve az ellenőrzött diplexer/hibrid tartományán
kívül.

Az RT3S nem hallja az adás alatti letöltési irányt, ha fél-duplex üzemben
van. Saját lesugárzott jel figyeléséhez használj második vevőt, és számítsd
ki az adó elleni védelmet. Passzív szűrővel ne hirdess teljes duplexet.

## Eredménylap

| Teszt | Revízió/műszerek | Mért eredmény | Állapot | Teendő |
| --- | --- | --- | --- | --- |
| G0 | Kitöltendő | Lásd VALIDATION | Részleges | A napló szerint |
| G1 | A prototípus nincs összeszerelve | Nincs mérés | Függőben | Nyomtatás és teszt |
| G2 | VNA szükséges | Nincs mérés | Függőben | RF-illesztés és mérés |
| G3 | Követési próbapad | Nincs mérés | Függőben | Autonómia ellenőrzése |
| G4 | Rádió/licenc | Nincs mérés | Függőben | Csak G1–G3 után |
