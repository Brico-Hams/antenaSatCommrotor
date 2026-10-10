# Önálló modul: AZ/EL/POL rotor

## Hatókör és függőségek

LimeSDR, PA, RF-szűrők, projektenantennák és hangrendszer nélkül is
összeállítható. Más antenna csak akkor használható, ha tömege, súlypontja és
terhelése minősített. Az új változat CM5/CM5IO-t és segédpanelt használ;
a két tengelyes ESP32-változat külön történeti kivitel, önmagában nem
teljesíti a harmadik, POL tengelyt.

| Szükséges | Nem szükséges a csak rotorhoz |
|---|---|
| Három tengely, motorok/hajtások, tartók és rögzítés/állvány | Két LimeSDR és nagy teljesítményű rádió |
| CM5/CM5IO, segédpanel, három rámpagenerátoros meghajtó és védett táp | Bluetooth-hang/kodek/mikrofon/hangszóró |
| GNSS, iránytájolás/kalibráció, enkóderek/NC végállások, stop/watchdog | Körantenna vagy RHCP/LHCP RF-hálózatok |
| Kábelek, biztosítékok, Powerpole és kompatibilis szabályozás | TX/APRS/SSTV |

Saját referenciák: [CM5-ROTOR.md](CM5-ROTOR.md),
[POLARIZATION-MECHANICAL.md](POLARIZATION-MECHANICAL.md),
[MECHANICAL.md](MECHANICAL.md), [CM5-PCB.md](CM5-PCB.md). Ezek mutatják,
mi valósult meg és mi igényel próbapadi tesztet; még be nem fagyasztott
revízióhoz ne vásárolj úgy, mintha a termék kiadott lenne.

## A modul alkatrészei és költsége

Lásd a [REFERENCE-PRICES.md](REFERENCE-PRICES.md) és a
[reference-prices.csv](../../bom/reference-prices.csv) fájlt: a CM5, CM5IO,
DRV ×3, ENC ×3, COMPASS, IMU és GPS a rotor tájékoztató referenciaárai.
A MOTION, HARDWARE, STRUCTURE, PCB-FAB/PCB-PCBA és POWER-RAILS/HARNESS
továbbra is teljes árajánlatra/kiválasztásra vár. Csak a ténylegesen
beépített fogyóeszközöket és megosztott alkatrészeket válaszd ki. Az
önálló rotor beszerzésébe ne vedd bele az SDR-t, PA-t, hangrendszert vagy
RF-szűrőket. A rádió hiánya nem szünteti meg a stopot, watchdogot és a
mozgásvédelmet.

## Önálló szerelés és konfigurálás

1. Válassz kompatibilis rotor- és segédpanel-revíziót. CM5-háromtengelyes
   konfigurációhoz ne használj két TMC2209-es/ESP32-es hordozót.
2. Táp nélkül szereld a szerkezetet, fém csapágyakat/tengelyeket és hajtást;
   ellenőrizd az utat és egyensúlyt. A POL korlátozott forgású tengely.
3. Szereld be a kimeneti enkódereket és hat NC végállást; vizsgáld a
   véghelyzeteket és a használandó antenna koaxának mozgási terét.
4. A fagyasztott paneltérkép szerint szereld a CM5/CM5IO-t és segédpanelt,
   rámpamódú meghajtókat és kompatibilis logikát; Linux ciklusból STEP-et
   ne generálj.
5. Az égboltot látó GNSS-t és a mágneses zavaróktól távoli iránytű/IMU-t
   telepítsd. Álló GPS nem méri az északot.
6. Kösd a külső tápot, Powerpole/biztosítékot és szabályozást; a motorok
   leválasztásával folytonosságot/polaritást ellenőrizz. CM5-re 12 V-ot ne adj.
7. Ha rendelkezésre áll, konfiguráld a rotor-only profilt a telepítőben:
   SDR-eszközök ne legyenek előfeltételek és ne induljanak el. A
   [CM5-ROTOR.md](CM5-ROTOR.md) közzétett parancsait ellenőrizd, ne kitalált
   szolgáltatásokat.
8. Mozgás engedélyezése előtt, biztonságos terheléssel és kifejezett helyi
   üzembe helyezéssel próbáld a stopot, watchdogot, nyitott kábelt és újraindítást.
9. Végez homingot, szintezést, valódi északi tájolást és EL/POL nullázást.
   Kalibráld az érzékelőket; dokumentáld a deklinációt és a motor ki/be
   állapotában mért eltérést.
10. Tölts be TLE-t, ellenőrizd az UTC-t/helyet, majd jósolj áthaladást;
    antennamentesen vagy minősített próbateherrel kövesd, mielőtt az antennát
    felszereled.

## Függetlenség és biztonság

Kikapcsolt/hiányzó RF nem akadályozhatja a minősített mozgásvezérlést.
Érvénytelen érzékelőt ne helyettesíts nullával. A határokat, követésvesztést,
pozícióvesztést és stopot próbapadon kell tesztelni. A körpolarizációs kéziség
nem változik POL-lal; a csak rotor nem tartalmaz RHCP/LHCP RF-hálózatot.
Alkalmazás vagy SBC nem helyettesíti a fizikai stopot.
