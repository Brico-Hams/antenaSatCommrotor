# Eredeti moduláris hordozópanel — PortableSatStation, A revízió

Jelenlegi szerzők: **Anatol EA5KAO, Diego EA5JEF és Pedro Roca Molina**. Lásd az `AUTHORS.md`, `ACKNOWLEDGEMENTS.md` és `DISCLAIMER.md` fájlokat: ez a szerzőség a projekt eredeti munkájára vonatkozik, nem az idézett modulokra, eszközökre vagy kiadványokra. A [Bricohams](https://bricohams.org) oktatási hivatkozása nem jelent gyártói kereskedelmi támogatást. Gyermekekkel/serdülőkkel végzett tevékenység hozzáértő felnőtt felügyeletét igényli; a prototípus nem játék. Alkalmazandó engedély/licenc nélkül adni tilos.

## A kiadás állapota és korlátai

Eredeti **hordozópanel-terv**, nem kereskedelmi vezérlő másolata. Szerkeszthető források: `hardware/PortableSatCarrier.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, helyi `.kicad_sym` könyvtár és `.pretty` footprintök; auditálható generátor: `hardware/generate-carrier.cjs`. A rézrétegeket nem helyettesítik rajzok. A Gerbereket a KiCad CLI, a furatokat az Excellon-exportáló állítja elő. A `fabrication/PortableSatCarrier-Gerbers-CAD-VERIFIED-NOT-RELEASED.zip` kizárólag a hét tényleges Gerber-réteget, két Excellon-fájlt és Gerber-jobot tartalmazza; díszítő rajzokat nem tartalmaz, és nem helyettesíti a gyártási megjegyzéseket. A **NOT-RELEASED** elnevezés szándékos: a ZIP-et ne küldd gyártásba a revízió formális blokkoló tételeinek lezárásáig. Lásd a **`fabrication/release-status.json`** fájlt, az ERC/DRC-jelentéseket és hash-eiket: egy fájl megléte nem jelenti, hogy gyártásra engedélyezett.

**A prototípus nincs összeszerelve és tesztelve. A fizikai és tápellátási ellenőrzési pontok lezárásáig az összeszerelés/használat TARTÁS alatt.** Az ERC/DRC kizárólag a CAD-szabályokat ellenőrzi; nem tanúsítja a biztonságot, RF-immunitást, hőmérsékletet vagy a harmadik féltől származó modulok fizikai illeszkedését. A szimbólumok cserélhető, passzív tűkkel megadott modulokat jelölnek: az ERC nem validálja a belső szabályozóikat, feszültséghatáraikat vagy firmware-üket.

## Tényleges elektromos architektúra

```text
Védett, kereskedelmi 12 V-os táp (NEM csupasz akkumulátor / beépített töltő NÉLKÜL)
  + -- külső fő DC-kapcsoló -- J1.1 RAW12
                                            |
                                D1 SB560 (anód->katód)
                                            |
                                      PROTECTED12
                                            |
                           F1 SPT T3,15 A -- FUSED12 -- D2 SMBJ15A -- GND
                               |                 |
                      F2 T2,5 A              F4 T1 A
                               |                 |
                         J2.1 STOP_SEND      J4.1 BUCK12 -> külső buck VIN
                               |                 J4.2 GND -> buck GND
               külső NC TÁPÉRINTKEZŐ                    |
               reteszelhető kapcsológomb          Pololu D24V22F5
               >=5 A MEGSZAKÍTÁS 12 V DC-n              |
                               |                 VOUT -> J5.1 BUCK5
                         J2.2 VMOT               GND -> J5.2 GND
                               |                         |
                    C1/C2 220u/35 V                 F3 T1 A
                               |                         |
                   U2/U3 VM -> motorok             JP1 kivehető átkötés
                               |                         |
                            GND                    U1 5V (ESP5)
                                                        |
                                              U1 szabályozó -> 3V3
                                                  érzékelők + VIO/MS1/MS2

Ugyanazon gomb második, izolált NC érintkezője: J3.1 STOP_N -- NC -- J3.2 GND
R2: 10k a STOP_N és 3V3 között. Nyitott=HIGH=hiba; normál=LOW.
```

A J2 **nem GPIO-bemenet**: mindkét kapcsa a tápág pozitív vezetője. Mindkét meghajtó teljes árama az F2-n, J2-n és a külső vezetéken/érintkezőn halad át; használj rövid, legalább 0,75 mm²-es rézvezetéket, húzásmentesítést, valamint dokumentált DC-névleges kapcsokat/érintkezőket. Ebben az áramkörben ne használj jelátviteli JST-t, Dupont-vezetéket, próbapanelt vagy kisáramú segédérintkezőt. Működéshez ne hidald át a J2-t. A külső reteszelhető gomb fizikailag megszakítja a VMOT-ot akkor is, ha az MCU, Wi-Fi vagy firmware lefagy; a logika/web a megszakítás előtt továbbra is tápot kap. A reteszelés feloldásáig az áramkör nyitva marad. A J2.2 ténylegesen mindkét meghajtót táplálja; az útvonal nem szoftvervezérelt relőtől függ.

Ezt nem áruljuk tanúsított vészleállítóként. A kondenzátorok a megszakítás után energiát tárolnak: ellenőrizd a VMOT-lecsengést és a tényleges leállási időt. A retesz feloldásakor visszatér a VMOT: mozgás előtt **kézzel reseteld és szándékosan élesítsd újra a vezérlőt**. Ha külön elektromos resetre lenne szükség, amely a gomb reteszének feloldása után is reteszelt marad, ezt a revízió NEM biztosítja: erre külső, jóváhagyott kontaktor/resetvezérlés kell, nem GPIO.

**A D2 az F1 után van**: az F1 korlátozza a zárlatos TVS leágazását; emellett rövidzárvédelmet/biztosítékot követelj meg a tápnál és a pozitív kábelben, közvetlenül a táp közelében. Külső biztosíték nélkül akkumulátort ne csatlakoztass. A D1 fordított polaritás ellen véd, tartós túlfeszültség ellen nem. Szabályozott 12 V-ot használj, normál maximum 13,8 V; **24 V-ot ne használj**, még akkor sem, ha a meghajtó elviselné. SMBJ15A: 15 V standoff, a tesztimpulzus névleges maximum clampje 24,4 V; a Watterott 5,5–28 V VM-et specifikál. Kábeltranziensek és regeneráció mérést igényelnek: a TVS nem tesz minden tápot kompatibilissé.

Az F1/F2/F3/F4 Schurter SPT 5×20 kerámia, lomha biztosíték: 0001.2509 (3,15 A), 0001.2508 (2,5 A), 0001.2504 (1 A, két darab). Az SPT-adatlap ezekre az értékekre 250 VAC / 300 VDC-t és gyártó által megadott DC-megszakítóképességet ír; ne helyettesítsd csak AC-re specifikált biztosítékkal. OGN 0031.8201 biztosítéktartó: 22,5 mm-es osztás, a központi NPTH 2,7 mm-es támaszlyukkal. Ezek prototípus-induló értékek, nem szelektivitási bizonyítékok.

## PONTOS modulok, tájolás és csatlakozások

### U1: Espressif ESP32-DevKitC V4, ESP32-WROOM-32E, 38 tű

Általános 30 tűs DevKit, C3, S3 vagy más tűtávolságú panel nem megfelelő. Két sorban 19 hüvelyes érintkező, **2,54 mm** osztás, **25,40 mm** középtávolság. Panelrendelés előtt ellenőrizd a tényleges modullal; USB lefelé, antenna a felső él felé. Alkatrészoldali nézet:

```text
             ANTENNA / alatta ne legyen fém vagy réz
 bal x=77 mm                              jobb x=102,4 mm
  1 3V3        20 GND
  2 EN NC      21 IO23 NC
  3 VP/IO36    22 IO22
  4 VN/IO39    23 TX0 NC
  5 IO34       24 RX0 NC
  6 IO35       25 IO21
  7 IO32       26 GND
  8 IO33 NC    27 IO19
  9 IO25       28 IO18
 10 IO26       29 IO5 NC
 11 IO27       30 IO17
 12 IO14       31 IO16
 13 IO12 NC    32 IO4 NC
 14 GND        33 IO0 NC
 15 IO13       34 IO2 NC
 16 SD2 NC     35 IO15 NC
 17 SD3 NC     36 SD1 NC
 18 CMD NC     37 SD0 NC
 19 5V         38 CLK NC
                   USB
```

Az NC szándékosan nincs a hordozóra kötve, a rajzon NC jelölést kapott; a flash/strap-tűket nem használjuk. A CAD NC-hálózatai nem csatlakoznak egymáshoz.

| Funkció | GPIO | Polaritás / feszültség |
|---|---:|---|
| AZ STEP / DIR | 26 / 27 | 3,3 V logika |
| EL STEP / DIR | 14 / 13 | 3,3 V logika |
| Közös enable | 25 | aktív LOW; R1 10k a 3V3-ra, induláskor tilt |
| Leállítás monitor | 34 | NC GND-re, nyitott HIGH; külső felhúzás |
| AZ minimum / maximum | 35 / 36 | NC GND-re, nyitott HIGH; külső felhúzás |
| EL minimum / maximum | 39 / 32 | NC GND-re, nyitott HIGH; külső felhúzás |
| ESP RX GNSS-ről / ESP TX GNSS-hez | 16 / 17 | 3,3 V UART, NEM RS232 és NEM 5 V TTL |
| AZ SDA / SCL | 21 / 22 | I2C0 busz, 3,3 V |
| EL SDA / SCL | 18 / 19 | külön I2C1 busz, 3,3 V |

A GPIO34–39-en nincs belső felhúzás: az R2–R6 ténylegesen a panelen van. Ipari 12/24 V bemeneti meghajtó nincs beépítve. JP1-et a táp alatt lévő USB csatlakoztatása **ELŐTT** távolítsd el: az Espressif kizárólagosnak mondja az USB-, külső 5 V- és külső 3V3-táplálást. Két módszerrel egyszerre soha ne táplálj. A hordozó kizárólag a DevKit szabályozójáról veszi a 3V3-at; nincs párhuzamos második szabályozó. Kezdetben legfeljebb **100 mA külső keretet** tartalékolj (érzékelők+GNSS+VIO), és Wi-Fi-adás közben mérd a feszültségesést/hőmérsékletet; a tényleges kapacitás a kiválasztott DevKit/GNSS függvénye.

A buck szabályozónak ezen a panelen nincs modul-footprintje vagy feltételezett geometriai tűkiosztása: külön szerelendő, és csak a **Pololu D24V22F5** címkézett VIN, GND és VOUT pontjaihoz vezetékezhető. J4.1=VIN, J4.2=GND, J5.1=VOUT 5V, J5.2=GND; az EN és PG a modul dokumentációja szerint bekötetlen. Ne helyettesítsd D24V25Fx-szel: a gyártó eltérő tűkiosztásra figyelmeztet. A padok fizikai helyzete nem határozza meg a hordozópanel csatlakozását. A fordított polaritás/rövidzár/hő elleni védelem a kiválasztott modul sajátja; J5/ESP csatlakoztatása előtt ellenőrizd az 5 V kimenetet. A hordozópanel egyetlen GPIO- vagy érzékelőcsatlakozója sem visz BUCK5/FUSED5/ESP5 hálózatot.

### U2/U3: Watterott SilentStepStick TMC2209 **v2.x**

Ne feltételezz A4988-cal vagy BTT-klónnal való felcserélhetőséget. Hüvelyes foglalatok, 2 sor × 8, 2,54 mm osztás, 15,24 mm sorköz. Felülnézet, bal/jobb tűk a gyártói rajz felső végétől:

| Hordozó pad | Bal oldal | Hordozó pad | Jobb oldal |
|---:|---|---:|---|
| 1 | EN=ENABLE_N | 9 | VM=VMOT |
| 2 | MS1=3V3 | 10 | GND |
| 3 | MS2=3V3 | 11 | M2B |
| 4 | SPREAD=GND | 12 | M2A |
| 5 | PDN_UART NC | 13 | M1A |
| 6 | PDN_UART NC | 14 | M1B |
| 7 | STEP | 15 | VIO=3V3 |
| 8 | DIR | 16 | GND |

MS1=MS2=HIGH, SPREAD=LOW: **1/16**, 1/256 interpoláció, stealthChop. A modulnak belső PDN_UART-lehúzása van; őrizd meg a gyári jumpert, ne alakítsd UART-ra, és ne vágd el a SPREAD-et. A meghajtópanel DIAG/INDEX segédje nincs bekötve: StallGuard/szenzor nélküli homing nincs megvalósítva. A referencia mechanikai áttétel 25:1; kalibrálás előtt ellenőrizd a végleges mechanikai változatot és a tényleges mikrolépést.

A JM1/JM2 kivezetések balról jobbra: M2B, M2A, M1A, M1B. Az M2B/M2A egy tekercs, az M1A/M1B a másik tekercs. Áramtalanítva, ohmmérővel mérd meg. VMOT jelenlétében motort csatlakoztatni/leválasztani tilos. A VREF-et a Watterott modulverziója/sense-ellenállása és adatlapja szerint állítsd be, alacsony áramról indulva. **A fázisonkénti 1 A ideiglenes cél**, nem általános potméter-beállítás vagy akkumulátoráram. Hűtőborda és szellőzés szükséges; mérd a hőmérsékletet.

## Érzékelők, GNSS és végállások

Minden JST XH függőleges, **2,50 mm** osztású, nem 2,54 mm; kompatibilis krimpelést és mechanikai tehermentesítést használj. A négyzet alakú pad és „1” felirat jelöli az 1. tűt minden footprintön.

| Csatlakozó | 1., 2., 3., 4. tű |
|---|---|
| J6 külső GNSS | 3V3, GND, GNSS_TX (RX16 felé), GNSS_RX (TX17 felől) |
| J7 AS5600 AZ | 3V3, GND, AZ_SDA, AZ_SCL |
| J8 AS5600 EL | 3V3, GND, EL_SDA, EL_SCL |
| J9 opcionális IMU/magnetométer | 3V3, GND, AZ_SDA, AZ_SCL |

Az AS5600 **0x36** című; a két érzékelőnek külön buszon kell lennie. A breakout tápja 3,3 V, nem lehet 5 V-ra húzott felhúzás. A panelen R7–R10 4k7 van; ha a breakouten is van felhúzás, számítsd ki az eredő ellenállást vagy távolítsd el az egyik készletet. Az I2C legyen rövid (cél <30 cm), a motorvezetékektől elkülönítve. Hosszú kábelnél ne feltételezz megbízható működést próba vagy adó-vevő nélkül. Opcionális MPU6050 0x68/0x69 és LIS3MDL 0x1C/0x1E nem ütközik az AS5600-zal; csak kifejezetten **VIN- és 3,3 V-os logikakompatibilis** breakoutot használj. A J9 nem jelenti, hogy a firmware integrálja ezeket az eszközöket.

Javasolt GNSS: Adafruit Ultimate GPS breakout 746; vezetékezés előtt ellenőrizd a revíziót, 3,3 V VIN-t és UART-ot; a GNSS-antenna az ESP-től és rádiótól legyen külön. A NYÁK csak UART-ot/tápot biztosít, GNSS-antennát, PPS-t vagy RF-interfészt nem. Egyantennás GNSS **nem mér statikus valódi irányt**. Az AS5600 a tengely relatív szögét méri; kalibráld a nullát, irányt és fizikai tengelyt. Az északi/elevációs referenciát kézzel kell kalibrálni; motorok, acél, AS5600-mágnesek és kábelek mellett az iránytű erősen torzulhat. Ne ígérj automatikus abszolút headinget, és ne téveszd össze a mozgó GNSS irányát az antenna tájolásával.

| NC segéd, két tű: jel / GND | GPIO |
|---|---:|
| J3 leállítás, izolált segédérintkező | 34 |
| J10 AZ minimum/home | 35 |
| J11 AZ maximum/útvég | 36 |
| J12 EL minimum/home | 39 |
| J13 EL maximum/útvég | 32 |

Kábelszakadás/működtetés = HIGH. Ezek monitorbemenetek, nem tanúsított lekapcsolás. A végállások önmagukban nem kapcsolják le a VMOT-ot. 12 V-os tápkontaktust GPIO-val megosztani tilos. Élesítés előtt minden NC vezetékezés szükséges; hibák elrejtéséhez tartós jumpert ne használj.

## Gyártás és szerelés, lépésről lépésre

1. Nyisd meg a projektet KiCad 10.0.7 vagy kompatibilis újabb verzióval. Hasonlítsd össze a `connectivity.json` fájlt a `firmware/include/board_config.h` és `docs/CONTROL.md` tartalmával; bármely eltérés újragenerálást és validálást igényel, ne csak egy rajzot javíts.
2. Futtasd a `hardware/validate-export.ps1 -KiCadCli <helyi_elérési_út>\kicad-cli.exe` parancsot. A szkript **blokkolja az új exportot**, ha ERC, DRC, paritás vagy összeköttetés hibás; hasheket, Gerber, Excellon, netlist és beültetési pozíciókat állít elő.
3. FR4-et rendelj, két réteggel, mindkét oldalon **70 µm kész réz (2 oz)**, 1,6 mm vastagság, kétoldali maszk, fehér előlapi szitázás, vakvia nélkül, szabályozott impedancia nélkül. HASL ólommentes vagy ENIG. Téglalap 180×130 mm; négy NPTH 3,2 mm. Lásd `fabrication/STACKUP.txt`. Az 1 oz-ot ne fogadd el automatikus helyettesítőként. Kérj netlist szerinti elektromos tesztet.
4. Független Gerber-nézőben vizsgáld meg: mindkét rézrétegen több ezer szegmens/pad, maszk, szitázás, zárt kontúr, PTH/NPTH külön. Ellenőrizd a mm mértékegységet és a közös réteg/furateredetet. Ne csak `Edge.Cuts` réteget gyártass. A KiCad pozíció-CSV-je Y-t felfelé növekvő kartéziánus koordinátaként kezeli: `PosY=-y` az itt megadott NYÁK-koordinátákhoz képest. Ne fordíts meg csak egy réteget vagy a furatfájlt; mindig a teljes exportált csomagot küldd.
5. Tolómérővel ellenőrizd ESP 19×2/25,40 mm, TMC 8×2/15,24 mm, JST 2,50 mm, kapocsléc 5,08 mm, biztosítéktartó 22,50 mm + középtámasz méretét. Blokkoló: ellenőrizd a házat, polarizált retesz irányát és csavarhozzáférést; az eredeti burkolatok konzervatívak, nem a beszállító STEP-modelljei.
6. Szereld be az ellenállásokat, D2-t (jelölt K katód a pozitívra), kerámiakondenzátorokat, D1-et (sáv/K katód a PROTECTED12 felé), foglalatokat, kapocsléceket és biztosítéktartókat. C1/C2: pozitív a VMOT-ra, negatív GND-re. Még ne helyezz be modulokat.
7. Ohmmérővel ellenőrizd, hogy nincs RAW12–GND, VMOT–GND vagy ESP5–GND zárlat; vizsgáld meg a J2.2→U2/U3.VM folytonosságot, és hogy nyitott leállítónál nincs J2.1→J2.2. Ellenőrizd, hogy az NC segédre soha nem kerül 12 V. Vizsgáld át a forrasztást és polaritást.
8. Kezdetben 100 mA-re korlátozott 12 V-os labor táppal, reteszelt leállítóval mérd meg az izolált buck 5 V kimenetét J5 csatlakoztatása előtt; csak a próbák után emeld a korlátot. USB nélkül helyezd be az ESP-t és a megfelelő JP1-et, mérd a 3V3-at.
9. Motor nélkül helyezd be a meghajtókat; ellenőrizd a VIO és MS1/MS2=3V3 értéket, valamint EN HIGH állapotot. Reteszelt leállítónál a VMOT-nak esnie kell akkor is, ha a Wi-Fi aktív. Teszteld a gombot, kábelszakadást, resetet, GNSS/enkóder-vesztést és végállás-leválasztást.
10. Táp nélkül csatlakoztasd a motorokat, csökkentsd a VREF-et, terhelt antenna nélkül rövid mozgásokat végezz. Erősítsd meg az irányt, 25:1 skálát, mozgástartományt és visszajelzést. Az 1 A/fázis cél előtt legalább 30 percig vizsgáld az áramfelvételt/hőmérsékletet. Mérd a VMOT-tranzienseket megszakításkor és fékezéskor, hosszú kábellel is.
11. Szigetelő M3 távtartókkal szereld kültéri elektronikai dobozba. NYÁK origója bal felső sarok; furatok (5,5), (175,5), (5,125), (175,125) mm. A NYÁK felső felülete és dobozfedél között legalább 30 mm teljes magasságot hagyj — nem 30 mm-t a meghajtó fölött —, biztosíts USB-/csavarhozzáférést és légáramlást. Nem állítjuk, hogy a rotor üregébe befér. A mechanikai koordináció használja e koordinátákat és valós méretet.

A korábbi 130×70 mm-es dobozba a 180×130 mm-es panel NEM fér: külön nagyobb doboz vagy tartó kell, footprint-csendes átméretezés nem megengedett. Kezdetben legalább 20 mm helyet hagyj a kábelbemenetek körül és legalább 30 mm-t a NYÁK felső síkja és a fedél között; ellenőrizd ténylegesen a hajlítási sugarakat, hozzáférést, csatlakozók/hűtőbordák magasságát.

A mechanika létrehozta a `cad/carrier_enclosure.scad` fájlt: **végleges kibővített revízió**, névleges külső méret 228×178×43,6 mm + 2 mm fedél + 0,7 mm domborulat, belső méret 224×174 mm; NYÁK-sarok a dobozban (24,24), tartóközéppontok (29,29), (199,29), (29,149), (199,149) mm. NYÁK z=8 mm, névleges 1,6 mm vastagság fölött 32 mm szabad magasság; ez névlegesen 12 mm-t hagy egy 20 mm magas meghajtó felett, nem 32 mm-t. A végleges mechanikai revízió 3,2 mm-es M3 dobozfuratot határoz meg, ami megegyezik a NYÁK tényleges 3,2 mm-es furataival: ellenőrizd a nyomtatási hézagot, ne erőltesd a csavarokat, és alkatrészes NYÁK-ot ne használj fúró sablonjaként.

Ez a koordináta-kompatibilitás **nem bizonyít fizikai illeszkedést**: a végső oldalhézag szélenként 22 mm, a panelek még nincsenek kifúrva; a doboz lezárása előtt a beszerelt NYÁK-kal határozd meg a portokat/kábeltehermentesítést és kábel-/csavarhozzáférést. A doboz álló szerelésű, nem a mozgó tengelyre kerül. CAD-ből becsült tömör ASA-tömege ≈260 g, nem mért érték. A külön álló `cad/carrier-metal-mount.dxf` alumínium tálca **240×196×2 mm**, költségvetési tömege ≈254 g, nem mért. Ezt a tömeget és a rögzítőelemeket is vedd figyelembe a carrier/doboz mellett az állomástömegben. Ezek a méretek a korábbi 188×138-as dobozt és 200×156-os tálcát váltják fel; a régi változatokat ehhez a végleges egységhez ne gyártsd le. A közölt BuildLight 3,130–3,200 kg-os keret a még függő extrák előtt meghaladja a 3 kg-os célt: **a jelenlegi keretben a tömegcél nem teljesült**; a növekedést ne rejtsd el, és ne állítsd, hogy a szerelvény megfelel.

Az AS5600 a két külső kimeneti tengelyre szerelendő: a hordozópanel nem határoz meg még ki nem választott enkóder-breakout furatkiosztást.

Tömegbecslés, **nem mérés**: teljes FR4 `0,180 × 0,130 × 0,0016 × 1850 ≈ 69 g`; a két teljes, hipotetikus 70 µm-es rézréteg legfeljebb ≈29 g-ot ad hozzá a maratás levonása előtt. Hagyj ≈100 g-ot csupasz panelre és **150–220 g-ot NYÁK+modul-együttesre** tervezési tartalékként, doboz, táp/akkumulátor, külső buck, stop és kábelek nélkül. Ez nem bizonyítja a teljes állomás tömegcélját; mérd le a szerelvényt és ellenőrizd a tartalékot.

A 145/435 MHz RF-et, koaxokat, motorokat és buckot válaszd el a GNSS/ESP/érzékelőktől. RF-fémház esetén az antennákat ki kell vezetni, és a beépített ESP-antennát nem szabad letakarni. Ez a NYÁK nem duplexer, RF-szűrő, erősítő vagy adóinterfész.

## Összeszerelési/használati kiadás blokkoló tételei

- A tényleges modulok és méretek ellenőrzöttek; hasonlóság alapján ne helyettesíts tűkiosztást.
- Védett kereskedelmi táp, kábelbiztosíték és fő leválasztás ellenőrzött.
- A külső gomb pontos cikkszáma, izolált NC-érintkezők, áram és dokumentált **legalább 5 A megszakítóképesség 12 V DC-n** igazolt. A „10 A AC” jelölés nem elég. A BOM nem talál ki minősített alkatrészt; annak kiválasztásáig motoros működés nem engedélyezett. A reteszelés mechanikus, nem szoftverrel vezérelt relé.
- A biztosítékok szelektivitását, zárlatot, TVS-t, regenerációt, feszültségesést, D1/pálya/kapcsok/meghajtó hőmérsékletét a tényleges legrosszabb esetben tesztelték.
- A DevKit 3V3 tápját Wi-Fi és valamennyi periféria mellett tesztelték; a tényleges keret ismert.
- Az e tűkiosztású firmware, mikrolépés, mechanikai kalibrálás/mozgástartomány és stop/újraélesítés próbapadon ellenőrzött. Szimuláció nem helyettesíti ezeket a teszteket.

## Nyomon követhetőség és licencek

Az eredeti hardver kapcsolási rajza, NYÁK-ja, szabályai/footprintjei és műszaki dokumentációja **CERN-OHL-S-2.0** licencű, copyright © 2026 Anatol EA5KAO, Diego EA5JEF és Pedro Roca Molina; lásd `LICENSES/CERN-OHL-S-2.0.txt` és `hardware/LICENSE.txt`. Az eredeti generátor, validálószkript és tesztek **MIT** szoftverek, ugyanazzal a szerzői jogi értesítéssel; lásd `LICENSES/MIT.txt`. Harmadik féltől származó NYÁK-ot nem importáltunk. A gyártói kiadványokat hivatalos URL-eken használtuk fel, nem terjesztjük újra a projektben; szerzőik megtartják jogaikat, és nem tulajdonítunk nekik prototípus-támogatást.

A hivatalos KiCad 10.0.7-et helyben kicsomagoltuk innen: `https://s3.cern.ch/kicad-downloads/windows/stable/kicad-10.0.7-x86_64.exe`; globális telepítés nincs. A KiCad szoftvere GPL-es; a hivatalos KiCad-könyvtárak CC-BY-SA 4.0 licencűek a tervben történő használatra vonatkozó kivétellel. A `Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open` geometriáját az osztás/támasz ellenőrzésére használtuk; a modul ábrái nem kerültek a Gerberbe.

Felhasznált források (2026-10-10):
- Espressif DevKitC V4: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- Hivatalos kapcsolási rajz: https://dl.espressif.com/dl/schematics/esp32_devkitc_v4-sch.pdf
- TMC2209 v2: https://learn.watterott.com/silentstepstick/pinconfig/tmc2209/
- Watterott kapcsolási rajz: https://github.com/watterott/SilentStepStick/tree/master/hardware
- SPT biztosíték: https://www.schurter.com/en/datasheet/typ_SPT_5x20.pdf
- D24V22Fx buck: https://www.pololu.com/product/2858
- AS5600: https://ams-osram.com/products/sensor-solutions/position-sensors/ams-as5600-position-sensor

A `bom/pcb.csv` fájlban szereplő árak tájékoztató, egységár-becslések, nem ajánlatok; add hozzá a krimpelést, kábeleket, hűtőbordákat, DC-stopot, tápot, dobozt és szállítást. A panelen nincs lítiumakkumulátor-töltő és nincs funkcionális biztonsági nyilatkozat.
