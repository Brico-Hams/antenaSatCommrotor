# BricoHams-arculat a PCB-ken és a nyomtatott alkatrészeken

Forrás: `branding/bricohams_horizontal.png` (BH-logó + „bricohams”). A
`scripts/make_logo_assets.py` egyszínű sokszögekké (`branding/bricohams_polys.json`) és az
`cad/bricohams_logo.scad` OpenSCAD-modullá alakítja (generált; kézzel ne szerkeszd). A szlogent és a
pontokat elhagyjuk (részletek < 0,3 mm).

## PCB (felső szitanyomat, `F.SilkS`)
Az `scripts/add_logo_pcb.py` rasztereli a Gerbereket, megkeresi a legszabadabb helyet (távol a
forrasztópaddaktól/maszknyílásoktól, furatoktól, meglévő szitanyomattól és a laperéltől), és a logót
Gerber-régióként (G36/G37, LPD/LPC) **és** `gr_poly` háromszögekként is hozzáadja a `.kicad_pcb`
fájlhoz, hogy egy új KiCad-kimenet is megőrizze.

| Panel | Pozíció (mm, Gerber-koordináták) | Méret | Távolság a legközelebbi elemtől |
| --- | --- | --- | --- |
| PortableSatCarrier (ESP32) | X 102,5 / Y −126,2 | 40 × 12,2 | 8,3 mm |
| cm5-guard-A | X 243,5 / Y −239,7 | 50 × 15,3 | 21,9 mm |

Frissültek az SHA-256 értékek (`fabrication/release-status.json`,
`hardware/cm5/reports/manifest-sha256.json`) és a carrier Gerber-ZIP. **Korlátok:** a KiCad nem volt
elérhető, ezért az **ERC/DRC nem futott újra, és a Gerbereket nem KiCadből generáltuk újra**; a
Gerbereket közvetlenül módosítottuk, és gerbonarával újraolvasva ellenőriztük. A szitanyomat nem
érinti a rézréteget, de a gyártónak át kell néznie az előnézetet. A panelek továbbra sem kaptak
gyártási engedélyt (lásd VALIDATION.md).

## Nyomtatott alkatrészek (0,6 mm dombormű)
Az `enclosure_lid` és `diplexor_lid` fedelek, a `radio_cradle` tartó (hátfal, külső oldal) és a
`carrier` fedele. 0,05 mm átfedés, hogy ne maradjon lebegő sziget; a vízzáró hálókat trimesh-sel
ellenőriztük. A fogaskerekeket és a szerkezeti alkatrészeket nem módosítottuk.

## Illusztrációk
Az összeszerelési ábrák tartalmazzák a logót, a címblokkot és a szerzők sorát
(Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina · bricohams.org); lásd az
[összeszerelési útmutatót](assembly/README.md). A régi diagramokat a `scripts/brand_svgs.py` látta
el arculattal.
