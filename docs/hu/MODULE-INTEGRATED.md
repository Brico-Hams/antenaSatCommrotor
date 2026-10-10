# Általános összeszerelés: önálló modulok összekapcsolása

## Csak a szükséges modulokat válaszd ki

| Cél | Belépési pont |
|---|---|
| Csak antenna, külső/kézi rádióval | [MODULE-ANTENNA.md](MODULE-ANTENNA.md) |
| Csak rotor, a felhasználó kompatibilis antennájával | [MODULE-ROTOR.md](MODULE-ROTOR.md) |
| Csak SDR-rádió, külső antennákkal/terhelésekkel | [MODULE-RADIO.md](MODULE-RADIO.md) |
| Teljes állomás | Ez és az [ASSEMBLY-MULTIMODE.md](ASSEMBLY-MULTIMODE.md) |

Az integrált összeállításban a CM5 közös a rádióval/rotorral: az önálló
BOM-ok összeillesztésekor ne számolj kétszer CM5-öt, CM5IO-t vagy tápellátást.
Modul elhagyása nem jogosítja fel a hozzá függő reteszek áthidalását.

## Integrációs sorrend

1. Külön fejezd be és fogadd el az antenna mechanikáját/RF-jét, a rotor
   mozgását/érzékelőit és a rádió vételét/hangját.
2. Állítsd fel az állványt és rögzített alapot. A CM5, rádió, hűtőbordák és
   külső akkumulátor nem forog az antennával. Ellenőrizd a stabilitást és CG-t.
3. A levehető interfészen rögzítsd az antennát a rotorhoz; ellenőrizd a
   háromtengelyes terhelést/utat, koaxot és tehermentesítést.
4. Sávonként kösd össze az RF SMA-t, ha minősített, körpolarizációs hálózatot,
   és a POL-forgástól független kéziségválasztót. TX maradjon tiltva.
5. A fagyasztott kapcsolási rajz szerint építsd be a Powerpole-elosztást,
   biztosítékokat, átalakítókat és EMI-szűrést; ellenőrizd esést/hőt/tranzienseket.
6. Ha megvalósult, válaszd az `integrated` szoftverprofilt, az SDR-azonosítókat
   és helyi hitelesítő adatokat. Indításkor ne legyen automatikus élesítés.
7. Kalibráld az UTC-t/helyet, szintet/északot, AZ/EL/POL nullpontokat; vizsgáld
   az érzékelő-, határ-, óra-, Bluetooth-, folyamat- és stop/watchdog-hibákat.
8. Valós orbitális adatokkal validáld az áthaladást/térképet/radart és
   Dopplert; TX előtt ellenőrizd a hangot, SSTV/APRS-t és látható hibajelzést.
9. Műszerekkel/terheléssel minősítsd a TX-et/teljes duplexet: mindkét
   VHF/UHF-irány, felharmonikusok (145×3=435 MHz), blokkolás és melegedés.
10. Mérd le az üzemi együttest az állvánnyal/kábelekkel; csak az aktuális
    döntés szerinti külső akkumulátort hagyd külön, és azt külön jegyezd fel.
    Ellenőrizd a ≤5 kg-ot és 2 órás üzemidőcélt méréssel.

## Ábrák, alkatrészek és hibák

Az [illusztrált útmutató](ASSEMBLY-MULTIMODE.md) összerendeli az ábrákat,
alkatrészazonosítókat, külső anyagokat és lépéseket. A koncepcionális rajz
nem megmunkálási sablon vagy gyártási tűkiosztás.
A [TROUBLESHOOTING-MULTIMODE.md](TROUBLESHOOTING-MULTIMODE.md) tartalmazza a
számított problémákat, ellenőrzéseket és leállási kapukat. Az árlistákat
konkrét hivatkozással/dátummal kell lezárni, megkülönböztetve az újrahasználható
eszközöket, fogyóanyagokat, megosztott és még nyitott tételeket. Az aktuális
ármegfigyeléseket a [REFERENCE-PRICES.md](REFERENCE-PRICES.md) és a
[reference-prices.csv](../../bom/reference-prices.csv) tartalmazza.
Az elektronikai részösszeget és az elektronikai részösszeg + ASA változatot
ne add össze: ezek alternatívák. A külső akkumulátor költsége szerepel a
költségvetésben, noha az 5 kg-os állomástömegből kizárt; a töltő nincs benne
az akkumulátor árreferenciájában. Ne állítsd, hogy teljes a költség, amíg
függő kategória vagy jóvá nem hagyott mennyiség van.

Ez a tartalomjegyzék nem igazolja a fizikai integráció tesztelését.
A [VALIDATION.md](VALIDATION.md), [ACCEPTANCE.md](ACCEPTANCE.md) és a pontos
NYÁK/Gerber/BOM/CPL-revízió az irányadó.
