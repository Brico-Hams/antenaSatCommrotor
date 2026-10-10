# Önálló modul: CM5 SDR-rádió

## Hatókör és függőségek

Rádió rotor és projektspecifikus antenna nélkül is építhető, kompatibilis
külső antennával vagy műterheléssel. CM5/CM5IO-t, két LimeSDR Minit, hangot és
védett tápot használ. A célzott teljesítményekhez további PA/szűrő kell; ezek
nem a csupasz SDR kimeneti teljesítményei.

| Szükséges | Opcionális vagy üzemmódfüggő |
|---|---|
| CM5/CM5IO, sorozatszám szerint azonosított két SDR, USB/hűtés és táp | Mechanikus rotor és három meghajtója |
| 50 Ω SMA RF-utak, vevővédelem és szűrés | Projekt hordozható antennája |
| Bluetooth PCM-hang, mikrofon/hangszóró, ha használt | GNSS/SGP4/rotor automatikus Dopplerhez |
| Fizikai TX-engedély, watchdog, biztosíték, minősített TX RF-út | Körpolarizációs RHCP/LHCP-hálózatok |
| Lineáris PA/szűrők/műterhelés az 5 W célhoz | Külső K1 hangkapcsolat az integrált hang helyett |

A [RADIO-HOST.md](RADIO-HOST.md) dokumentálja az interfészeket és teszteket;
a [CM5-RF-SELECTION.md](CM5-RF-SELECTION.md) rögzíti az alkatrészekre vonatkozó
bizonyítékot. Az [ANDROID-DIGITAL.md](ANDROID-DIGITAL.md) különbözteti meg a
DSP-t, létrehozott hangot, RF-adást és távoli ACK-t. Ne keverd össze őket.

## A modul alkatrészei és költsége

A [REFERENCE-PRICES.md](REFERENCE-PRICES.md) és a
[reference-prices.csv](../../bom/reference-prices.csv) tartalmazza az árakat
és a függő tételeket. A rádiómodulhoz CM5/CM5IO, két SDR, valamint a
szükséges RF, AUDIO, USB-DATA, COOLING és tápellátási kategóriák választandók
ki. A mozgásérzékelők, motorok és a rotor mechanikája nem kötelező beszerzés
az önálló rádióhoz. TX-hez a fizikai adásengedély és watchdog akkor is
kötelező; a motorok elhagyása nem ok a védelem eltávolítására. A korábbi RF
BOM nem tartalmaz automatikusan minősített, multimódusú lineáris PA-kat vagy
a bővítés teljes költségvetését.

## Önálló összeszerelés és konfigurálás

1. Válaszd ki a CM5/CM5IO/Lime revíziókat; jegyezd fel a két egyedi
   sorozatszámot és a VHF/UHF-hozzárendelést. Ne az első megtalált USB-eszközt
   válaszd.
2. Szereld az egységeket szellőző, rögzített alapra megfelelő rögzítéssel és
   árnyékolással; foglalt USB3 portok esetén határozd meg a hang csatlakozását.
3. Építs külső Powerpole/biztosíték-elosztást, CM5-szabályozást és RF-ágakat.
   Számítógép/SDR csatlakoztatása előtt mérd meg a feszültséget és polaritást.
4. Készíts SMA/kábeleket/lezárásokat, előválasztót és RX-védelmet. PA és
   ellenőrzött RF-út nélkül maradj vételi módban.
5. Telepítsd a radio-only profilt és a gazdagép közzétett függőségeit.
   Az USB-azonosítókat és privát hitelesítő adatokat helyben állítsd be.
6. Ellenőrizd a felderítést, hardverből visszaolvasott mintavételi
   frekvenciákat/frekvenciákat és a két egyidejű RX-folyamot. A kért
   mintavételi sebesség nem ellenőrzött tényleges sebesség.
7. Válaszd ki kifejezetten a VHF/UHF hangcsatornát, teszteld Bluetooth
   PCM-et/creditet/veszteséget; két vevő SSTV/APRS hangját ne keverd.
8. Állíts be engedélyezett kézi frekvenciát/módot. Önálló mód nem színlelhet
   orbitális helyzetet vagy Dopplert érvényes adatok nélkül.
9. Teszteld a DSP-t WAV-/tesztvektorokkal, majd valós vétellel. Mikrofon/
   hangszóró/K1 hangot csak ellenőrzött tűkiosztással, biasszal és szinttel
   konfigurálj.
10. TX-hez minősítsd a PA-t/szűrőket, terhelést, spektrumot, hőmérsékletet
    és fizikai engedély/watchdog/lease útját. Minimális teljesítménnyel kezdj;
    egyszerre csak egy TX legyen aktív.

## Módok elkülönítve

Vétel/kézi üzem nem függhet rotortól. Automatikus Doppler valós, friss és
ellenőrzött orbitális adatforrást, UTC-t és állomási helyet igényel; a forrás
elvesztése ne váltson csendben kézi adásra. A tényleges standalone támogatást
a gazdagép kódjával/tesztjeivel kell ellenőrizni; ez a dokumentum nem állítja,
hogy kész. Az 5 W FM, 5 W PEP USB és 1 W AM cél továbbra is mérésre vár.
