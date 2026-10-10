# Felelősségi és oktatási célú felhasználási nyilatkozat

A PortableSatStation **kísérleti mérnöki prototípus**. Nem tanúsított
termék, nem játék, nem biztonsági eszköz, nem vészhelyzeti kommunikációs
berendezés és nem kereskedelmi SATCOM-terminál. A vonatkozó licencek
szerint, a törvény által megengedett mértékben garancia nélkül kerül
átadásra. Ez a nyilatkozat nem zár ki olyan jogokat vagy felelősséget,
amelyeket jogszerűen nem lehet kizárni.

## A validálás állapota

A számítások, szoftvertesztek, fordítás és hálóellenőrzések nem
bizonyítják az elektromos vagy mechanikai biztonságot, teherbírást,
vízállóságot, szélállóságot, állóhullámarányt (SWR), nyereséget,
RF-leválasztást vagy a tényleges követési pontosságot. Lásd a
[VALIDATION.md](VALIDATION.md) dokumentumot, és teljesítsd az
[ACCEPTANCE.md](ACCEPTANCE.md) kapuit.

Az elkészült Gerber nem egy felülvizsgált vagy bevizsgált áramköri lap.
Gyártásba küldés előtt ellenőrizni kell a lábnyomokat, csatlakozásokat,
tervezési szabályokat, áramterhelhetőséget, hőelvezetést, védelmeket és
a teljes összeállítást. A firmware feltöltése sem validálja a
csatlakoztatott hardvert.

## Rádiózás és szabályozás

Csak a vonatkozó engedélyek/licenc, frekvenciasávok, adóteljesítmény és
jogi feltételek betartásával, valamint a műholdüzemeltető előírásai
szerint szabad adni. Kereskedelmi vagy katonai berendezések említése nem
engedélyezi azok használatát vagy rendszereik elérését. Mérés nélkül ne
adj át RF-hálózatokra. Egy RT3S fél-duplex rádiót nem tesz teljes
duplexszé egy diplexer.

## Mozgatás, energia és gyártás

Összeszerelés, összecsukás, kábel- vagy meghajtócserék előtt válaszd le a
tápellátást. A böngészőtől/firmware-től független fizikai leállításnak
elérhetőnek kell maradnia, és mindenkit távol kell tartani a mozgási
tartománytól. Áramkimaradás után ne használd a motorokat nem biztonságos
teher megtartására. Validáld az állványt, a rögzítéseket, a kiegyensúlyozást
és a határolókat.

Csak ellenőrzött védelemmel ellátott, kereskedelmi tápegységet/akkumulátort
és megfelelő töltőt használj. Ne építs rögtönzött akkumulátorcsomagot, és
ne hidald át a biztosítékokat vagy védelmeket. Az első indításkor vagy
firmware-feltöltéskor ne csatlakoztass motorokat/RF-et. ASA nyomtatásához,
megmunkáláshoz és forrasztáshoz a gyártói előírások szerinti megfelelő
eszközök, szellőztetés és védelem szükséges.

## Gyermekek és serdülők

A [Bricohams](https://bricohams.org) oktatási célú használata hozzáértő
felnőtt felügyelete mellett történjen. A szimulációt és a vételt kell
előnyben részesíteni. Kiskorúak felügyelet nélkül ne férjenek hozzá
mozgó alkatrészekhez, szerszámokhoz, forrasztáshoz, akkumulátorokhoz,
feszültség alatt lévő áramkörökhöz vagy adókhoz. Ne tegyetek közzé
kiskorúak személyes helyadatait, hitelesítő adatait vagy azonosító
adatait a tárolóban, a flashelő webhelyen vagy megosztott naplókban.

## Harmadik felek, védjegyek és adatok

Az idézett védjegyek és szerzők megtartják jogaikat. Az eredeti szerzők
jóváhagyása, támogatása vagy együttműködése nem következik beleértve.
A TLE-adatok és külső szolgáltatások hibásak vagy elavultak lehetnek.
Ellenőrizd az epochot és az érvényességet; kritikus döntésekhez ne
használd őket.

A jelenlegi szerzők: **Anatol EA5KAO, Diego EA5JEF és Pedro Roca Molina**.
A korábbi munkák és függőségek külön attribúciót kapnak.
