# Tápellátás, kábelezés és elektromos elkülönítés

Ez a dokumentum az elektromos architektúrát határozza meg, nem egy
legyártott PCB-t, és nem állítja, hogy minden beszerezhető modul kompatibilis.
A felhasználó emellett cserélhető modulokat tartalmazó hordozó PCB-t kért
kapcsolási rajzzal, Gerberrel, érzékelő- és védelmi csatlakozásokkal.
Ennek fejlesztése külön nyomon követett; nem feltételezhető, hogy minden
DevKit vagy StepStick azonos lábnyomú. Lásd ADR-020.
A végleges GPIO-kiosztás és a vezérlő csatlakozásai a CONTROL.md-ben és
a firmware-ben találhatók.

## Tápellátási fa

```text
kereskedelmi, védett 12 V névleges tápegység, a meghajtókkal ellenőrzött tartomány
  |
  +-- a kábel/fogyasztás szerint méretezett biztosíték -- főkapcsoló
        |
        +-- a motorok tápellátásának fizikai megszakítása hozzáférhető vészleállítóval
        |     +-- AZ meghajtó -- AZ motor
        |     +-- EL meghajtó -- EL motor
        |
        +-- DC/DC 5 V -- ESP32-panel
                    +-- 3,3 V szabályozás kompatibilis érzékelőkhöz

RT3S: saját, független akkumulátor
RF: passzív, fém dobozban; nincs automatikus PTT
```

Használj ellenőrzött védelmű kereskedelmi tápegységet/akkumulátort és
hozzá való töltőt. Ne készíts rögtönzött lítiumcsomagot. A leállítónak
firmware- vagy böngészőfagyás esetén is tiltania kell a mozgást. A
szoftver által figyelt NC-kontaktus kiegészíti a hardveres lekapcsolást;
nem tanúsított biztonsági relé.

## Meghajtók és áram

A TMC2209 vagy egyenértékű meghajtó korlátozza a fázisáramot. A beállítást
a meghajtópanel, az érzékelőellenállás és a motor névleges RMS-árama alapján
kell kiszámítani; ne másolj át értéket egy másik NEMA14-ről. Ellenőrizd a
tényleges 16 microstep módot: a 80000 lépés/fordulat feltételezi a motor
200 lépés/fordulatát, 16 microstepet és 25:1 áttételt, nem a 256 belső,
interpolált lépést.

A gyártó előírása szerint helyezz leválasztó kondenzátort a VMOT közelébe,
védd a polaritást, gondoskodj szellőzésről, és ellenőrizd a hőmérsékletet
zárt, napon álló dobozban. Táp alatt ne csatlakoztass/le motorvezetéket.
Ellenőrizd a logika/meghajtó közös földjét, valamint a teljesítmény,
koax és GNSS elkülönítését.

## Érzékelők és kábelezés

- Az ESP32 nem tűri az 5 V-os bemenetet, kivéve ha dokumentált
  szintillesztés van.
- Az AS5600 címe közös I2C-cím; használj külön buszokat vagy multiplexert.
  Két, azonos buszra kötött, eltérő cím nélküli érzékelő nem működik.
- A mágnes mechanikai iránya, távolsága és tengelye számít. Ellenőrizd a
  tartományon kívüli mezőt és az elfordulást, mielőtt a visszacsatolásra
  támaszkodsz.
- A soros GNSS logikai szintje legyen kompatibilis; a GNSS-antennának
  szabad égbolt kell, és az álló antenna nem ad azimut-referenciát.
- Az NC-t úgy kösd be, hogy a vezetékszakadás hibát okozzon. A motorok
  leválasztásával ellenőrizd az elektromos és logikai polaritást.
- A mozgási határolóknak fizikai hely és fékezési tartalék kell; a
  rajzolásuk vagy változók korlátozása nem elég.

## Moduláris, minden-egyben RF

A diplexer és RF-hálózatok fém doboza legyen külön a meghajtóktól és
konverterektől. Az ASA mechanikai burkolat, nem árnyékolás. Rögzített
csatlakozókat és húzásmentesítést használj; a koax súlya ne terhelje az
RT3S SMA-csatlakozóját. A rádiótartó tegye hozzáférhetővé a PTT-t,
hangerőt, kijelzőt, akkumulátort és antennacsatlakozást. SMA-adaptert csak
a tényleges készülék menet- és csatlakozó-nemének ellenőrzése után válassz.

Hasonlítsd össze a vett zajt bekapcsolt/kikapcsolt motorok és DC/DC-k
mellett; ha nő, adás előtt javítsd a szűrést, elhelyezést, árnyékolást és
visszavezetéseket. Az RF-csatlakozások és diplexer nem keverendők össze a
rádió állítólagos USB-vezérlő interfészével.

## Energia-önállóság: módszer, nem ígért szám

Mérd meg a követés, készenlét, homing és Wi-Fi teljesítményét. A hasznos
energia a tápegység kimenetén mért érték, nem a cella kapacitása szorozva
12 V-tal, ha a gyártó más feszültségen adja meg az mAh-t.

`óra = hasznos Wh / átlagos W`

Pusztán számtani példa: 30 Wh hasznos energia és 8 W átlag esetén 3,75 h.
Az árammérés nélkül ez nem becslés erre az állomásra. Rögzíts tartalékot
hidegre, öregedésre és a konverter veszteségére.
