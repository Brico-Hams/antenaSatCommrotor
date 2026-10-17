# Tesztelés: komponensek, viselkedés és tesztpad

**Laboratóriumi frissítés, 2026-10-17 (spanyolul):**
[aktuális eljárások és üres adatlapok](../../testing/09-laboratorio.md),
[NanoVNA](../../testing/10-nanovna.md), [aktív RF](../../testing/11-rf-potencia.md)
és [kalibrálás](../../testing/12-calibraciones.md).
A 24 kiegészítő LAB-teszt és a nyomtatható munkafüzet itt még nincs lefordítva.
Az aktuális eljárások biztonsági javításai elsőbbséget élveznek a régi
lépésekkel szemben (I2C-azonosítás, meghajtótiltás és árammérés).
Ez a történeti fordítás önmagában nem használható laborutasításként.
A fizikai eredmények továbbra is FÜGGŐ állapotúak; a PCB/TX tiltás érvényes.

Ez a szakasz azt írja le, HOGYAN kell tesztelni a PortableSatStation minden komponensét **a PCB-k gyártása előtt** és az állomás integrálása előtt: tesztpad, ellenőrzőlisták, várt viselkedés és elfogadási kritériumok. Kiegészíti az [ACCEPTANCE.md](../ACCEPTANCE.md) G0-G4 kapuit és a [VALIDATION.md](../VALIDATION.md) nyilvántartását.

> **Állapot:** digitális prototípus, **fizikailag nem validált**. Az alábbiak közül még semmit sem mértek meg: minden teszt FÜGGŐ, amíg az eredmény, a dátum és a műszer nincs feljegyezve. A `Gn-m` hivatkozású kritériumok az ACCEPTANCE.md-ből származnak; a többi ennek a felülvizsgálatnak a **javasolt** mérnöki értéke, amelyet az első prototípussal meg kell erősíteni vagy módosítani. A szoftverfordítás vagy az átmenő szoftvertesztek nem validálják a kábelezést, a mechanikát vagy az RF-et.

## Hogyan használd ezt a szakaszt
1. Építsd fel a padot a [01-banco-de-pruebas.md](01-banco-de-pruebas.md) szerint szintenként (B0 → B4).
2. Futtasd az ellenőrzőlistákat sorrendben: elektronika → PCB-kapu → mechanika → RF/rádió → szoftver/OS → Android-alkalmazás → rendszer.
3. Minden eredményt jegyezz a [registro-pruebas.csv](registro-pruebas.csv) fájlba (tesztenként egy sor) dátummal, Git-revízióval, műszerekkel és kezelővel.
4. **Állj meg:** ha egy biztonsági teszt elbukik (PWR, DRV-02/05, SNS-04, MEC-05), ne lépj tovább terhelt motorokra vagy RF-re.
5. Egyetlen PCB-t se rendelj meg, amíg a [gyártás előtti kapu](03-puerta-pcb.md) nincs lezárva.

## Biztonság
Felnőtt felügyelet, elérhető vészleállító, áramkorlátos táp, a korai tesztekben terheletlen motorok, védőszemüveg fúráskor/csiszoláskor, engedély nélkül nem adunk, minden TX-tesztnél 50 Ω-os lezárás (nem antenna), a 12 V soha nem kerül a CM5 tüskesorára.

## Tesztek térképe
| Dokumentum | Szakaszok | Kapu |
|---|---|---|
| [01-banco-de-pruebas.md](01-banco-de-pruebas.md) | A tesztpad kialakítása | — |
| [02-electronica.md](02-electronica.md) | Elektronika: táplálás, meghajtók és érzékelők (PWR, DRV, SNS) | G1E |
| [03-puerta-pcb.md](03-puerta-pcb.md) | Gyártás előtti kapu a PCB-khez (PCB) | G1E |
| [04-mecanica.md](04-mecanica.md) | A forgató mechanikája (MEC) | G1 |
| [05-rf-y-radio.md](05-rf-y-radio.md) | Antenna, RF és SDR rádió (ANT, RAD) | G2 / G4 |
| [06-software-y-os.md](06-software-y-os.md) | Szoftver, CM5 hostok és OS-kép (SW) | G0 |
| [07-app-android.md](07-app-android.md) | Android-alkalmazás (APP) | G3 |
| [08-sistema.md](08-sistema.md) | Rendszerintegráció (G3 / G4) (SYS) | G3 / G4 |

A BricoHams-logóval és a szerzőkkel ellátott ábrák: T1 (pad), T2 (GPIO-tesztelő), T3 (mechanikai rögzítő) a `fig/` mappában.

Nyilvántartás: [registro-pruebas.csv](registro-pruebas.csv). Összeszerelés: [összeszerelési útmutató](../assembly/README.md). Az alkalmazás súgója: `android/app/src/main/res/raw*/`.
