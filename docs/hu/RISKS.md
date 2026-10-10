# Műszaki kockázatok és enyhítés

| Kockázat | Ok | Enyhítés | Szükséges bizonyíték |
| --- | --- | --- | --- |
| A szél meghaladja a nyomatékot | A felület/kar dominál, kicsi a NEMA14 | Korlátozd az üzemet, egyensúlyozz, állítsd le | Menet közbeni nyomaték és terhelési próba |
| Az állvány elfordul | A fényképezőgép terhelhetősége nem AZ-nyomaték | Fém, másodlagos rögzítés, teszt | Kilazulás nélküli torzió |
| Bolygómű-holtjáték | Játék, nyomtatási pontatlanság, hajlékony hordozó | Tűrések és visszacsatolás | Kimeneten mért holtjáték |
| Alámetszett napkerék | Kevés fog | 18 fogas, 1,5-ös modulú alap | Profil és érintkezés vizsgálata |
| Nem szerelhető fogazás | Helytelen fázis/hézag/tartó | Először egy fokozat összeszerelése | Teljes kézi körbeforgatás |
| Referencia elvesztése | Újraindítás, kapcsoló, szakadt vezeték | Hatástalanítás és újra-homing | Hibabeviteli teszt |
| Hibás irány | Mágnesek/motorok, deklináció | Valódi észak ellenőrzése | Mért irányhiba |
| Hibás UTC/helyzet | GNSS-fix nélkül, régi óra | Érvényességi állapot és reteszelés | GNSS nélküli és újraindítási teszt |
| Régi TLE | Cache vagy régi szolgáltatóadat | Műholdanként epoch, reteszelés | Adatkor-tesztek |
| V/U kölcsönhatás | Közös radiátorok és reflektor | Szimuláció és összeszerelt VNA-mérés | Végleges SWR/mintázat |
| Sávon kívüli hibrid | A SATCOM nem 145/435 | Gyártói adatlap és mérés | S-paraméterek sávonként |
| Nem kompatibilis diplexer | Projektcímke, nem mérés alapján nevezve | Pontos revízió és próba | Méretek, teljesítmény, leválasztás |
| Rossz RF-érintkezés az összecsukható résznél | Műanyag zsanér, oxidáció | Pozitív fémes toldás | 50 ciklus és ismételt VNA |
| Rotor EMI-je | Közeli meghajtó/DC-DC és koax | Fém al-doboz és szűrés | Vétel motor ki/be |
| Feltételezett teljes duplex | Egyetlen fél-duplex RT3S | Kifejezett üzemmód vagy külön vevő | Valós rádióteszt |
| Zenit/kábelcsavarodás | Szinguláris sebesség és határok | Nem elérhető átvonulások kizárása | Szimuláció és próbapad |
| ASA túlmelegedése | Napon álló doboz és meghajtóáram | Helyes áram és szellőzés | Mért hőmérséklet |
| Tömeg a cél fölött | Elfelejtett akkumulátor, acél és koax | Valós összeállítás lemérése | Dokumentált mérlegelés |
| Harmadik felek jogai | Nyilvános URL nem licenc | Eredeti munka, idézés STL-másolás nélkül | Eredetnyilvántartás |

A mechanikai és RF-kockázatokat szoftvertesztekkel nem lehet lezárni.
A „függőben” állapot szándékos, és láthatónak kell maradnia.
