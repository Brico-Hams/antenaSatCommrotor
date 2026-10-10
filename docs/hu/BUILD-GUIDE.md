# Építési és beszerzési sorrend

## Vásárlás vagy nyomtatás előtt

1. Olvasd el az ARCHITECTURE, MECHANICAL, CONTROL és RF-AND-RADIO
   dokumentumokat.
2. Válaszd ki a konkrét motort; jegyezd fel a tömegét, tengelyét, hosszát,
   áramát és nyomatékgörbéjét.
3. Mérd meg a rádiót, állványt, diplexert és alternatív antennát.
   Nyomtatás előtt frissítsd a CAD-paramétereket. A névleges kompatibilitás
   nem bizonyítja a megfelelő illeszkedést.
4. Kérj ajánlatot a három BOM-listára. A tájékoztató összegek nem jelentenek
   ár- vagy elérhetőségi garanciát.
5. Határozd meg az üzemi frekvenciákat, majd szimuláld/mérd az RF-architektúrát.
   Ne vásárolj hibrideket hirdetett teljesítmény alapján a sávjuk ellenőrzése
   nélkül.
6. Ellenőrizd az eszközöket: OpenSCAD a CAD-hez, PlatformIO-környezet a
   vezérléshez, Node.js a számításokhoz. Ebben a kiadásban a hordozható
   validációs programokat a tárolón kívül helyezték el; ezek nem terepi
   függőségek.

## Fokozatos gyártás

### A iteráció: fogkapcsolódás és szerelés

Nyomtass próbadarabokat és egy bolygómű-fokozatot. Szereld össze és forgasd
kézzel. Ellenőrizd a fázist, hézagot, excentricitást és a nyomaték útját.
Az első fokozat beállítása előtt ne nyomtasd ki az egész szerkezetet.

### B iteráció: vezérlő-próbapad

Szereld fel az ESP32-t, GNSS-t, érzékelőket, határolókat és leállítót,
motorok terhelése nélkül. A pontos revíziót fordítsd/fel és teszteld az
összes hibát. Indításkor az eszköz maradjon hatástalanítva; ellenőrizd azt
is, hogy a meghajtók és kábelezés nem engedélyezik a motorokat lebegő GPIO
miatt.

### C iteráció: második tengely és rögzítés

Szereld össze mindkét áttételt, a fém tengelyeket és az állványrögzítést.
Helyezz fel kiegyensúlyozott próbatömeget; validálás nélkül ne használj
hosszú antennát. Mérd meg a pontosságot/holtjátékot, áramot és
hőmérsékleteket. Alkalmazd a G1 kaput.

### D iteráció: antenna és diplexer

Az állíthatóság érdekében tartalékkal vágd a fémet. A közzétett értékek
kezdeti méretek; a szigetelő, koax, átmérő, vasalat és más sávok módosítják
az elektromos hosszt. A végleges összeállításon, VNA-val hangold be.
A reflektornál is megbízható, vezető toldásokra van szükség. Korábbi
diplexert csak revízió, méretek és S-paraméterek ellenőrzése után építs be.

### E iteráció: terepi próba

Először vétellel kezdj, és hasonlítsd össze a független követést.
Csak a G1–G3 után végezz engedélyezett, minimális teljesítményű adást.
Ne hagyd felügyelet nélkül a rendszert, és ne üzemeltesd nem validált szélben.

## Változtatások és revíziók

Rögzíts minden modul-, motor-, microstep-, vezetékátmérő-, koax- vagy
szerelésváltozást. RF-változtatás RF-újraellenőrzést igényel; fogaskerék,
tengely, terhelés vagy állvány módosítása mechanikai újraellenőrzést.
Kerüld, hogy a firmware és a CAD különböző áttételi paramétereket tartalmazzon.

GitHub-közzététel előtt ellenőrizd a kiválasztott MIT/CERN-OHL-S-2.0
hatókört, a függőségeket és közleményeiket, a hitelesítő adatok és privát
mellékletek hiányát, valamint a hardverforrások átadására vonatkozó
kötelezettségeket.
