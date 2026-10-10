# Szállítási és terepi üzemeltetési kézikönyv

## Szállított modulok

- Antenna: boom, levehető radiátorok és reflektorok, RF-hálózatok és koax.
- Rotor: AZ/EL és nyeregrész rádió és antenna nélkül.
- Vezérlés: ESP32, GNSS, táp, leállító és eltávolítható RF-modul.
- RT3S saját akkumulátorral és levehető tartóval.
- Fényképezőgép-állvány és fém adapter.

Ne a kábeleknél fogva emeld. Védd az RF-toldások meneteit és érintkezőit.
A <=450 mm-es célzott csomagméret a hosszú részek szétszerelését igényli:
egy 475,5 mm-es VHF-kar nem fér össze varázsütésre, ha nincs kettéválasztva.

## Összeszerelés

Leválasztott táppal nyisd szét az állványt stabil talajon, ellenőrizd a
fémrögzítést és a másodlagos biztosítást. Ne feltételezd, hogy a
fényképezőgéphez megadott függőleges terhelhetőség oldalirányú nyomatékot is
engedélyez. Szereld fel a rotort, csatlakoztasd a határolókat, motorokat és
érzékelőket; alkalmazz húzásmentesítést.

Nyisd szét az antennát pozitív reteszekkel és fémes érintkezőkkel; az
utolsó koaxszal együtt egyensúlyozd ki az EL tengelyt. Ne akaszd az RT3S-t
vagy az akkumulátordobozt a boom végére. Mindenki maradjon a forgási
tartományon kívül.

## Pozíció, UTC, szint és észak

A GNSS-fix helyzetet ad, nem a mozdulatlan állvány irányát. Szintezd az
alapot, és ismert referenciával állapítsd meg a valódi északi irányt. Ha
iránytűt használsz, a naprakész forrásból származó deklinációt kompenzáld,
és tartsd távol a motortól/tengelytől/mágnestől; a teljes összeszerelés
után ellenőrizd az eltérést.

Helyi időt ne adj meg UTC-ként. Jegyezd fel a magasságot és mértékegységét;
hegyen a megfigyelő magassága és a horizont akadályai két külön dolog.
A homing csak a mechanikai tengelyt kalibrálja.

## TLE hegyi használathoz

Indulás előtt frissítsd; őrizd meg a cache-t és egy kézi másolatot.
Helyszínen:

- Az AP lehetővé teszi a helyi böngészést, de nem ad internetet.
- Elérhető STA/hotspot esetén az engedélyezett szolgáltatótól tölts le.
- Internet nélkül importálj friss epochú TLE-t, majd ellenőrizd a műholdat.
- A tényleges epoch korát vizsgáld, ne csupán a letöltés idejét.

A TLE-t ne kezeld frekvencialistaként. Ellenőrizd az aktív transzpondert,
módot és frekvenciákat a műhold üzemeltetőjének aktuális forrásaiból.

## Átvonulás közben

Ellenőrizd, hogy a rádió a megfelelő műholdon van, az UTC/helyszín
összhangban áll, a követés pedig élesítve van. Győződj meg róla, hogy az
átvonulás a vezérlő AZ/EL-határai, sebessége és zenitkizárása mellett
elérhető.

Az OpenGD77 a modell/verzió szerint kezelheti saját műholdas üzemét;
kövesd a telepített verzió kézikönyvét. CAT-kapcsolatot nem ígérünk.
Egy fél-duplex RT3S adás közben nem teszi lehetővé a letöltési irány
egyidejű hallgatását.

A webes felület nem fizikai vészleállító: a hardveres leállító maradjon
elérhető. Szél, rendellenes mozgás, új vételi zaj vagy laza csatlakozó
esetén állítsd le és keresd meg a hibát; ne erőltesd a követést.

## Szétszerelés

Állítsd le, ellenőrizd, hogy a motorok mozdulatlanok, válaszd le a tápot,
tehermentesítsd az EL tengelyt, majd szereld le az antennát. Független
használathoz vedd le a rádiót/RF-modult. Ne hajtsd össze a dipólusokat és
ne bontsd meg a bolygóművet engedélyezett motorok mellett. Szárazon tárold
az elemeket; az ASA-doboz nem bizonyít vízállóságot.

## Önálló felhasználás

Az antenna rotor nélkül, kézi állvánnyal és saját RF-hálózatával is
használható. A rotor a validált terhelési tartományon belül más antennával
is használható. A diplexert vezérlődoboz nélkül, külsőleg lehet
csatlakoztatni. Az RT3S saját akkumulátorral, a tartón kívül is működik.
