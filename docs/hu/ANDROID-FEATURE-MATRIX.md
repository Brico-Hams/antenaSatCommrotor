# Android FIRSTVERSION funkciómátrix

Ez egy eredeti, korlátozott hatókörű natív megvalósítás, amely kiválasztott
képességekből merít ihletet; **nem teljes Look4Sat-funkcióparitás**. Nem
állít élő követést, igazolt RF-kimenetet, dekóder-paritást vagy fizikai
antennaműködést. A pályanézet kezdetben ezt mutatja: „NOT LIVE — host
integration pending”; bemutató pályaadat nem helyettesíti a valósat.

| Kért funkció | Ebben a kiadásban megvalósítva | Függő integráció / fizikai ellenőrzés |
| --- | --- | --- |
| Katalógus, szűrők, kedvencek | Natív katalógussorok; név/NORAD-szűrők; csak kedvencek nézet; valódi NORAD-azonosítóval kulcsolt, eszközön privát SharedPreferences | A hostnak valódi NORAD-ID-ket kell adnia, és a választást a saját slotazonosítóira kell fordítania. A rotor meglévő katalógus-slotjának `id` mezője **nem** NORAD-azonosító. Itt nem készült katalógusletöltő. |
| Átvonulások | Host által megadott, korlátozott AOS/csúcs/LOS Unix-másodperces UTC-lista; maximális eleváció és részleges átvonulás jelölése | Az SGP4/átvonulás-előrejelzés a rotor feladata. Az Activity-nek érvényes, megfigyelőhely-specifikus előrejelzést kell átadnia. A terepi validálás nem igazolja a pályapontosságot. |
| Térkép | Eredeti, offline equirektanguláris földrajzi rács, megfigyelőpont, megadott valódi műhold-alpont és időbélyeges földnyom; a dátumvonal ugrásait nem rajzolja át a világon | Vázlatos globális koordinátarajz, **nem országtérkép/utcatérkép**. Nincs letöltött térképcsempe, csempeszerver, helyadat-feltöltés vagy telefonos pályapropagáció. Pontok nélkül nem jelenít meg pályát. |
| AZ/EL radar | Északra tájolt, látható égbolt-ábra a ténylegesen átadott pálya-/követési mintákkal; horizont alatti pontok kizárva; középpont=zenit, külső kör=horizont | Megfigyelőhely-specifikus hostmintákat kell adni; terepi igazítás, műhold-beszerzés és antennacélzás fizikailag nincs tesztelve. |
| AOS-riasztások | Műholdankénti, kifejezett feliratkozás; privát vevő; immutable PendingIntent; értesítési csatorna; látható Android 13+ engedélykérő gomb/állapot; **pontatlan** AlarmManager-ütemezés | Az alábbi manifest-bejegyzéseket kell alkalmazni; az Activity csak kifejezett érintésre kér futásidejű engedélyt. A host frissítési/kapcsolatbontási callbackjeit be kell kötni. Nincs pontos riasztási engedély, WorkManager-függőség, garantált riasztás/Doze-állítás, háttérhálózat vagy újraindításkori visszaállítás. Újraindítás vagy kényszerített bezárás után újracsatlakozás/folytatás kell az újraszámításhoz/ütemezéshez. |
| Frekvenciák / Doppler | Kifejezetten átadott névleges UL/DL Hz, kért korrigált Hz, adapter által visszaigazolt Hz, mód/támogatottság-jelző; ismeretlen érték ismeretlen marad | Itt nem találunk ki rádiómodellt vagy frekvenciát; Doppler-számítás itt nincs. A rádió gazdájának kell megadnia a valódi profilt/támogatást és az RF-visszaigazolás jelentését. A szoftveres ACK nem mért RF. Hardveres/éteren át történő ellenőrzés függőben. |
| Három tengely | Külön kijelzett mért és hosttól kért AZ/EL/POL-érték; korlátozott numerikus kérőűrlap, opcionális host-callback, mért POL-radarjelölő | A mechanikai POL-szög **nem** RHCP/LHCP-kapcsoló. A jelölő sematikus tájolási referencia, nem mért elektromágneses polarizációs mező. A callbacket a meglévő hitelesített/kalibrált/biztonsági kapuzott vezérlési munkamenethez kell kötni; itt nem adunk hozzá közvetlen működtető-végpontot. A hardveres mozgás/kalibrálás nincs tesztelve. |
| PD120/PD180 SSTV | A pályaréteg szándékosan nem birtokolja és nem duplikálja a dekóder megvalósítását | A DSP-gazda kezeli a meglévő natív dekódert, vételi UI-t és bizonyítékokat. Az integrációt/valós audio-tesztet annak a gazdának kell rögzítenie; nincs Robot36-paritásra vonatkozó állítás. |
| APRS | A pályaréteg szándékosan nem birtokolja és nem duplikálja az AX.25/APRS-vételi implementációt | A DSP-gazda kezeli a meglévő vételi dekódert és teszteket. A rádió/éteren át történő és audio-interfész ellenőrzése függőben. |

## Activity-integrációs szerződés

Minden hook az `org.bricohams.portablesatstation.orbit` csomagban van. A
MainActivity, erőforrások, Gradle vagy manifest módosítása nem e munka, hanem
a szülő/DSP-gazda feladata.

```kotlin
val overview = SatelliteOverviewView(activity)
overview.onSatelliteSelected = { noradId: Int -> /* valódi NORAD-ID átalakítása host-választássá */ }
overview.onAxesRequested = { target: ThreeAxisState -> /* meglévő biztonsági kapuzott vezérlőmunkamenet */ }
overview.onNotificationPermissionRequested = {
    // API >= 33: Activity.requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS), requestCode)
}
// UI-szál; csak hitelesített/validált, tényleges hostállapotot használj:
overview.submitSnapshot(snapshot: OrbitSnapshot?)
// Kapcsolatbontás, hosthiba, hiányzó identitás vagy inkompatibilis modell:
overview.submitSnapshot(null)
// onResume és az értesítési engedély eredménye után:
overview.refreshAlertPermission()
```

A fenti megjegyzések integrációs helykitöltők, **nem működő átviteli kódok**.
Az űrlap megjelenítése előtt kérd le a valódi hostállapotot. Ne tölts be
minta-frekvenciát, és ne másold a helyi űrlapértéket a mért tengelyekre vagy
az RF-visszaigazolásba. A profil támogatása kifejezett host-/adapterállítás,
nem a mód nevéből következik.

Az `OrbitSnapshot` lemásolja/korlátozza a kollekciókat, és csak olvasható
listákat tesz elérhetővé: 100 katalóguselem, 720 földnyom-pont, 100
átvonulás, 360 radarpont, 32 profil. A beágyazott skalármodellek
változtathatatlanok. Ellenőrzi a véges szög-/Hz-tartományokat, a pozitív
Unix-másodperc UTC-t (2100-ig), a földnyom időrendi sorrendjét, az egyedi
NORAD-ID-ket és a kiválasztott identitást. Az átvonulás-/radarmintákhoz
megfigyelő szükséges. A frissesség feltétele a csatlakoztatott adatforrás,
valamint az aktuális UTC a `generatedUtc` és `validUntilUtc` között.
A régi átadott adat elavult/offline címkével marad, soha nem „élő”.

### Javasolt adapter-JSON (NEM befagyasztott host-API vagy végpont)

Az `OrbitSnapshotJson.parse(JSONObject)` az alábbi összes kulcsot megköveteli;
a nem elérhető objektumok és frekvenciák explicit JSON `null` értékek,
a tömbök explicit tömbök legyenek. Nincs `optDouble` alapérték, kitalált
alpont, becsült Kepler-elem, sikeresnek látszó végpont, vagy rotor-slot-ID
NORAD-ID-vé alakítás.

- Gyökér: `schemaVersion: 1`, egész `generatedUtc`, `validUntilUtc`,
  logikai `sourceConnected`, nullable egész `selectedNoradId`.
- `catalogue`: `{noradId, name}`.
- Nullable `observer`: `{name, latitude, longitude, altitudeMeters}`.
- Nullable `subpoint` és `groundTrack` bejegyzések:
  `{utc, latitude, longitude}`.
- `passes`: `{aosUtc, peakUtc, losUtc, maxElevation, partial}`.
- Nullable `tracking` és `radarTrack` bejegyzések:
  `{utc, azimuth, elevation}`.
- Nullable `measuredAxes` / `requestedAxes`: `{azimuth, elevation, pol}`
  fokban.
- `radioProfiles`: `{name, mode, supported, uplinkHz, downlinkHz,
  requestedUplinkHz, requestedDownlinkHz, acknowledgedUplinkHz,
  acknowledgedDownlinkHz}`; mind a hat frekvenciamező nullable egész Hz.

Az Activity közvetlenül is létrehozhat változtathatatlan modelleket e javasolt
JSON helyett. Mezőt csak akkor használj, ha a tényleges host-szerződés
megfelelő identitással, idővel, megfigyelővel és mértékegységgel szolgáltatja.
A régi `PassData.aos/peak/los` mező Unix-másodpercként átalakítható, de önmagában
nem ad megfigyelőt/NORAD-azonosítót/alpontot/földnyomot/RF-állapotot. Az üres/
ismeretlen érték jobb, mint a kitalált állapot.

## Pontos manifest-kérés a felelős agent számára

A meglévő engedélyek mellé a `<manifest>` elem alá:

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

Az `<application>` elemen belül:

```xml
<receiver
    android:name=".orbit.PassAlertReceiver"
    android:enabled="true"
    android:exported="false" />
```

Nincs szükség Gradle-módosításra/függőségre, pontos riasztási engedélyre,
intent filterre vagy boot receiverre. A vevő regisztrációját ellenőrizni kell,
mielőtt az ütemezést sikeresnek jelentené. Engedély/csatorna megtagadásakor a
tervezett értesítést láthatóan törölni kell. AOS-változás a megfelelő
NORAD-riasztást törli/cseréli. Múltbeli/részleges/nem elérhető átvonulást nem
ütemezünk. Hostválasztás és kifejezett bontás törli az elavult ütemezett
riasztásokat, de megtartja a feliratkozásokat. A fogadáskori ellenőrzés
elnyomja a visszavont feliratkozású, lecserélt AOS-előrejelzésű, illetve
15 percnél többet késett riasztást.

## Eredeti implementáció és upstream licencek határai

Funkció-ötletként ellenőrzött hivatalos források; forráskódot nem töltöttünk
le vagy másoltunk:

- Look4Sat: <https://github.com/rt-bishop/Look4Sat>;
  a [licence](https://github.com/rt-bishop/Look4Sat/blob/main/LICENSE)
  **GPL-3.0**. Forrása/erőforrásai/térképcsempéi nem kerültek ebbe az
  eredeti rétegbe. Az eredeti projektkód MIT-licence nem licenceli újra a
  GPL-es upstream munkát: GPL-kód importálása külön terjesztési/licenc-
  felülvizsgálatot igényel.
- Robot36: <https://github.com/xdsopl/robot36>;
  a <https://github.com/xdsopl/robot36/blob/2af2390954aa248725042ba6b1332bbcca68c357/LICENSE>
  Ahmet Inan megengedő használati/másolási/módosítási/terjesztési
  engedélyét és garanciakizárását tartalmazza (2024). Ez a LICENCE nincs
  **MIT-nek vagy GPL-nek címkézve**. Dekóderkódot/eszközt nem másoltunk.
  A tényleges szövegre hivatkozz, ne a tároló nevéből vagy korábbi
  verzióból következtess licencre.

A pályaimplementáció nem csomagol térképcsempét, országhatárt, logót,
képernyőképet, hullámformát vagy más, szerzői jogvédelem alatt álló
térkép-/UI-eszközt. A koordinátarács és a natív vezérlők saját fejlesztések.

## Validálás és korlátok

Az összes pályaforrás önálló Kotlin 2.0.21-fordítása a meglévő Android SDK 35
és JUnit 4.13.2 használatával sikeres volt; **10 pályateszt** futott le.
Ez elkerülte az egyidejű Gradle/build-output írást. A tesztek az
`tests/android/orbit` alatt vannak, és a meglévő Android-tesztforrás-
leképezés már tartalmazza őket. A felelős build runner ezt futtathatja:

```text
:app:testDebugUnitTest --tests "*.OrbitModelsTest" --tests "*.OrbitSnapshotJsonTest"
```

A tesztek a másolt, változtathatatlan listákat, korlátokat, időrendet,
szigorú sémát/null/típus/ID-ellenőrzést, valós koordináta-vetítést,
észak/kelet radar-geometriát, frissességet, múltbeli/részleges/
ezredmásodperces AOS-elutasítást, NORAD-szűrőket, ismeretlen RF-mezőket és
POL-határokat fedik le. Az Android futásidejű engedélykérő párbeszédei,
SharedPreferences-tartósság, AlarmManager/értesítések kézbesítése,
rajzolás/akadálymentesség/eszköz-elrendezések, hostintegráció, SGP4-
pontosság és fizikai RF-/rotorüzem eszközön még nincs validálva.
Engedélyekre/riasztásra vonatkozó állításokat eszközön kell tesztelni;
JVM-bizonyíték nem elegendő.
