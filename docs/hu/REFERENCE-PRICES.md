# Tájékoztató árak és nyitott költségvetés

## Hatókör és módszer

A tartós árjegyzék a [reference-prices.csv](../../bom/reference-prices.csv).
Az adatgyűjtés dátuma: **2026-10-10**. Az értékek tájékoztató jellegű,
nyilvánosan elérhető ármegfigyelések; nem kötelező érvényű ajánlatok és nem
garantálják az elérhetőséget. Árajánlatkérés céljából nem küldtük el a projekt
fájljait gyártónak.

A `unit_reference_eur` az egységár-referencia. A `mean_eur` csak akkor van
kitöltve, ha ugyanarról az alkatrészről két összehasonlítható megfigyelés áll
rendelkezésre. Egyetlen megfigyelés nem piaci átlag. A kifogyott termékek
árai fel vannak tüntetve, de ezekből nem állítható össze megvásárolható
termékkosár. Az üres mező jelentése **függőben**, nem nulla. Jóváhagyott
mennyiség nélkül az ismert ár sem ad tételsort a költségvetésben.

A kutatásban rögzített átváltás: 1 EUR = 1,1206 USD és 0,84763 GBP,
a [EKB 2026-10-09-i referenciaárfolyama](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml),
2026-10-10-én lekérdezve. A napi hivatkozás változhat: vásárlás előtt
ellenőrizd újra az árfolyam dátumát és értékét. Az átváltási díjat, importáfát,
vámot és szállítást nem tartalmazza. Az ismert áfát tartalmazó német árakat
1,19-cel, a spanyol árakat 1,21-gyel osztottuk. Ahol az áfa beszámítása nem
megerősített, ott nem vontuk le.

## Fő referenciák

| Azonosító | Referenciamennyiség | EUR/egység | Alap |
| --- | ---: | ---: | --- |
| CM5 | 1 | 115,67 | Két áfa nélküli ajánlat átlaga; az egyik nem elérhető |
| CM5IO | 1 | 18,40 | Egy áfa nélküli megfigyelés |
| SDR | 2 | 535,43 | 600 USD LimeSDR Mini egységenként; importadók előtt |
| DRV | 3 | 15,97 | TMC5160 v1.5; áfa nélkül |
| ENC | 3 | 5,31 | AS5600; importadók előtt |
| COMPASS | 1 | 8,88 | LIS3MDL; importadók előtt |
| IMU | 1 | 10,33 | Normalizált átlag; egy üzletben nincs készleten |
| GPS | 1 | 25,93 | Normalizált átlag |
| ASA | 1 referencia-orsó | 23,46 | Átlag áfa nélkül; a tényleges felhasználás függőben |
| BAT | 1 külső | 99,99 | Feltüntetett ár; az áfa beszámítása nem megerősített |
| PP-PACK | 1 referenciacsomag | 15,16 | Tíz teljes piros/fekete véglezárás (20 érintkező = öt összekapcsolt pár); importadók előtt |
| PP-TOOL | 1 opcionális szerszám | 35,69 | Újrahasználható krimpelőfogó; külön költségkeret |

A CM5, CM5IO, két SDR, három meghajtó, három enkóder, iránytű, IMU és GPS
részösszege **1313,90 EUR**, áfa nélkül normalizálva. Egy referencia-orsó
ASA-val **1337,35 EUR**. Ezek alternatív részösszegek, nem összeadandó tételek.
**Nem a teljes állomás ára.** A 99,99 EUR-os akkumulátor külön szerepel, mert
az adózási alapja nincs megerősítve. A CSV számítási célból megőrzi a
tizedesjegyeket; csak a végén kerekíts.

Még nincs teljes árajánlat a következőkre: lineáris PA-k, szűrők/diplexer és
RF-kapcsolás, koaxiális kábelek/SMA, motorok és mechanikus hajtás,
állvány, kötőelemek, kiegészítő NYÁK/PCBA, átalakítók, kiválasztott
kábelkötegek és biztosítékok, töltő, USB3-összeköttetések, hang/K1,
fogyóeszközök és mérőeszközök. A táblázat ezekhez függőben lévő sorokat
tartalmaz: ne rejtsd el ezeket úgy, hogy csak az árral rendelkező sorokat
összegzed.

## Külső energiaellátás, Powerpole és biztosítékok

A kiválasztott akkumulátor az ECO-WORTHY **40308275183822** változata,
**DE-L13060202003-1** SKU-val; töltőt nem tartalmaz. A nyilvános adatlap
szerint: 12,8 V, 30 Ah, 360 Wh, 3,55 kg, 183 × 176 × 83 mm-es méret és
M5-ös kivezetések. 12,8 × 30 = **384 Wh**, ami eltér a feltüntetett
360 Wh-tól. Tervezéshez az alacsonyabb, 360 Wh-os értéket használjuk; egyik
érték sem igazolt mért, hasznos energiaként. A gyártó legfeljebb 30 A-es
töltő-/kisütőáramot és legfeljebb 14,6 V-os töltőfeszültséget ad meg; más
BMS-modellek küszöbértékeit vagy csúcsidőtartamait nem tulajdonítjuk ennek
a modellnek. A töltési hőmérséklet 0–55 °C, a kisütési -20–55 °C; hideg
esetén az automatikus lekapcsolás nincs igazolva.

Az állomás **5 kg-os** céljából kizárólag a külső akkumulátor marad ki.
Tömege továbbra is része a szállított tömegnek, költsége pedig a projekt
költségvetésének. Az állvány, kábelek, rádió, csatlakozók és beépített
szűrők beleszámítanak. A kétórás üzemidőt a tényleges RX/TX-ciklussal és
motorhasználattal kell megmérni.

A WP30-10 tíz teljes piros/fekete érintkezőt és húsz kontaktust tartalmaz:
öt összekapcsolt párt. Egy párhoz két érintkező kell; ne add össze a
csomag árát és ugyanazon érintkezőinek kiosztási költségét. Pontosan az
adott érintkezőkkel kompatibilis szerszámot és vezetéket használj. A fő
biztosítékot az akkumulátor pozitív kivezetése mellé, a számítási, motor- és
RF-ágak biztosítékait pedig az ágakhoz kell telepíteni. A BMS nem helyettesíti
ezeket. A kereskedelmi példákban szereplő 5 A vagy 15 A **nem határozza meg**
a jóváhagyott névleges áramokat: a vezetéket, üzemi áramot, indítási csúcsot,
hőmérsékletet és DC-megszakítóképességet figyelembe véve kell kiválasztani.

## USB-C és EMI-szűrés

A Raspberry Pi 27 W-os hálózati tápegysége csak próbapadi referencia; nem
oldja meg az akkumulátoros tápellátást. Az USB-C tápegységnek a kompatibilis
5 V/5 A profilt kell biztosítania, a kábelt pedig minősíteni kell. A PD-t
fogadó trigger nem USB-C tápegység, és nem jogosít fel 9–20 V CM5IO-ra
kapcsolására.

A 31-es típusú 2631801202 toroid referenciaára **2,56 EUR áfa nélkül**
magtagonként értendő, nem kész fojtótekercsenként. Négy–nyolc mag ára
10,24–20,48 EUR lenne adó és szállítás előtt, de ez nem teljes EMI-költségvetés
és nem jóváhagyott darabszám. A közös módusú fojtók, csíptetős ferritek és
csillapított differenciális LC-szűrő továbbra is opcionális/függő-DNP.
Minősíteni kell az egyenáramú ellenállást, áramot, kiegyensúlyozatlanságot/
telítődést, hőmérsékletet, frekvenciát, feszültségesést és az átalakító
stabilitását. A szűrővel és anélkül is össze kell hasonlítani az RX-zajt és
a TX hamis összetevőit; a beépített szűrő tömegét bele kell számítani az
5 kg-ba.

## Beszerzés modulonként

Használd az [antenna](MODULE-ANTENNA.md), [rotor](MODULE-ROTOR.md),
[rádió](MODULE-RADIO.md) és [integrált rendszer](MODULE-INTEGRATED.md)
útmutatóit. A helyi BOM-ok alkatrészlisták, nem önálló termékkosarak,
amelyeket felülvizsgálat nélkül össze kellene adni: az integrált változatban
a CM5/CM5IO csak egyszer szerepel, a megosztott elemeket pedig egyetlen
modulhoz kell rendelni. Az alternatívák, szerszámok és opcionális referenciák
nem adódnak automatikusan a kiválasztott részösszeghez.

A költségvetés lezárásához rögzíteni kell az MPN-t/revíziót, az egyes
szerelési lépésekhez jóváhagyott mennyiséget, a felhasznált darabszámot a
megvásárolt csomagmennyiségtől elkülönítve, az elérhetőséget, az áfát és
minden rendelés szállítási díját. A beszállítót és a dátumot is rögzítsd,
majd egyeztesd a helyi BOM-okat ezzel a táblázattal. Addig a teljes költség
**nyitott**.
