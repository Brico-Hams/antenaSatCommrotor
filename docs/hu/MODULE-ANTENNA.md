# Önálló modul: hordozható 145/435 MHz-es antenna

## Hatókör és függőségek

Az antenna rotor, CM5, SDR, akkumulátor és alkalmazás nélkül is megépíthető.
Kézi tartó/állvány és kompatibilis interfészű külső rádió használható vele.
Nem állítunk kereskedelmi SATCOM-teljesítményt vagy mért nyereséget/
polarizációt.

| Szükséges | Opcionális |
|---|---|
| ASA-darabok, mindkét sáv vezetői, gémek/tartók, fém rögzítők és 50 Ω SMA koax | AZ/EL/POL rotor |
| Tehermentesített kábelek, ellenőrzött csatlakozók és kézi tartó | Integrált SDR-rádió |
| RF-hangoláshoz és teszthez műszerek/lezárások | Diplexer, körpolarizációs hálózatok és RHCP/LHCP-kapcsolás, minősítés után |

Geometria és anyagok: [MECHANICAL.md](MECHANICAL.md),
[RF-AND-RADIO.md](RF-AND-RADIO.md), [CAD](../../cad/) és
[mechanikai BOM](../../bom/mechanical.csv). Az antenna költségéhez ne add
hozzá a teljes rotor BOM-ját; csak e modul tételeit válaszd ki. A dátummal
ellátott árak és a függő kategóriák a
[REFERENCE-PRICES.md](REFERENCE-PRICES.md) és a
[reference-prices.csv](../../bom/reference-prices.csv) fájlban szerepelnek.
Csak az ASA, az RF-INTERCONNECT, szükség esetén az RF-FILTER, a HARDWARE
rögzítőelemei és a fogyóanyagok tételeit vedd figyelembe; e modul alapján ne
vásárolj CM5-öt, SDR-t vagy motorokat. Az ASA tényleges felhasznált
mennyisége, valamint a vezetők és koaxok ára a konkrét alkatrészekkel való
egyeztetésre vár; végleges összeg nincs.

## Önálló összeszerelés lépésenként

1. Ellenőrizd az engedélyezett sávokat/frekvenciákat, CAD-revíziókat és a
   vezetők méreteit. A számított hosszok kezdeti hangolási értékek.
2. Nyomtasd az ASA-darabokat és vizsgáld repedést, fészket, illeszkedést;
   vezetők/tengelyek/teherhordó rögzítések legyenek fémből.
3. Szereld a gémet, tartókat és levehető VHF/UHF elemeket a
   [mechanikai útmutató](MECHANICAL.md) szerint. Ne vágj minden elemet
   minimális méretre a példány próbája előtt.
4. Készíts sávonkénti táplálást, hagyományos 50 Ω SMA kábeleket, rögzítést és
   tehermentesítést. Ellenőrizd a középérintkező típusát és csatlakozóanyát,
   ne RP-SMA-t válassz.
5. Próbáld a kézi kihajtást/összecsukást úgy, hogy ne húzd a koaxot, és a
   csatlakozó ne legyen teherhordó. Jegyezd fel az összeszerelt antenna tömegét
   és súlypontját.
6. VNA-val állítsd/be mérd előbb sávonként, majd a teljes szerelvényt; a nem
   használt portokat megfelelően zárd le. Rögzítsd az SWR-t és csatolást.
7. Körpolarizáció esetén szereld be a sávonkénti hálózatokat; mérd a fázist,
   amplitúdót, kéziséget és axiális arányt. Mechanikai elfordítás nem választ
   RHCP/LHCP-t.
8. Külső rádiót csak teszt után csatlakoztass; minimális teljesítménnyel kezdd,
   és ellenőrizd a hőmérsékletet/SWR-t. Terhelés nélkül TX-tesztelni tilos.

## Beállítás és elfogadás

Az antenna önmagában szoftvert nem igényel. Adás előtt dokumentáld a
frekvenciát, módot, adott esetben körkéziséget, kábelezést és mért korlátokat.
Az [ACCEPTANCE.md](ACCEPTANCE.md) RF-/mechanikai kapui az irányadók; helyes STL
nem bizonyít nyereséget, SWR-t vagy szélállóságot. A rotor interfésze levehető,
nem feltétele az antenna működésének.
