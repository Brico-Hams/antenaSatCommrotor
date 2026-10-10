# Android-vezérlés és TLE-átvitel elfogadási tesztjei

Ezek függőben lévő tesztkritériumok, nem megvalósítási állítások.
A végleges BLE-szerződésnek meg kell egyeznie a lefordított firmware-rel.

## Kapcsolat és jogosultság

1. Android 12 vagy újabb rendszeren a scan/connect engedély megtagadása
figyelmeztetést adjon, ne végtelen újracsatlakozást vagy elrejtett
kivételt. Régebbi verziókon ellenőrizd a BLE-kereséshez szükséges
rendszerszintű helyengedélyeket.
2. Eszköz kézi kiválasztása. Az UUID-nak és a protokoll verziójának
egyeznie kell; ne csatlakozzon az első hasonló nevű eszközhöz.
3. Ellenőrizd a firmware által előírt titkosítást/párosítást és a helyben
beállított vezérlőtokent; hibás token ne hajtson végre parancsokat.
4. A token ne kerüljön naplóba, titkosítatlan beállítások közé,
hiba-képernyőképre vagy buildfájlba. A kulcsot az Android Keystore védje.
5. Csatlakozás, bontás vagy az alkalmazás újraindítása ne élesítse a
motorokat és ne állítsa vissza a homingot.
6. Android és web egyidejű használata ne kerülhesse meg a busy állapotot
vagy a reteszeléseket.

## Protokoll és hibák

1. Tárgyald le az MTU-t, és teszteld a minimumot is: az üzeneteket a
szerződés szerint bontsd és állítsd össze újra; ne feltételezd, hogy egy
TLE belefér egy írásba.
2. A Request ID, hossz, sorszám, elveszett töredék és timeout világos
hibát eredményezzen, és ne alkalmazzon részleges üzenetet.
3. Ismeretlen válasz vagy eltérő verzió ne jelenjen meg sikeresként.
4. Értesítések és callbackek ne blokkolják a UI-t vagy a rotor biztonságos
vezérlését.
5. A rotor ne végezzen nehéz fájlrendszer-/SGP4-műveletet a BLE-callbackben;
használja a dokumentált biztonságos mechanizmusát.

## Kalibráció

1. Külön állapotként jelenjen meg a homing, UTC/helyzet, szintezés,
valódi északi irány és az encoder nullája, ha használjuk. Álló GNSS
nem ad irányt.
2. A firmware-rel egyező véges értékek, tartományok és mértékegységek.
3. Mozgás/követés közben és hiányos előfeltételekkel utasítsa el a
kalibrálást; ne korlátozza csendben érvényesnek tűnő értékre.
4. A felhasználó erősítse meg a fizikai ellenőrzést. Az alkalmazás ne
feltételezzen nem implementált dőlés-/irányérzékelő-méréseket.
5. Az állvány elmozdítása vagy a homing megismétlése a szabályzat szerint
érvénytelenítse a megfelelő adatokat.

## TLE a telefon internetkapcsolatán

1. Engedélyezett források HTTPS-en; nem biztonságos TLS vagy sima HTTP nélkül.
2. Hálózati hiba őrizze meg az utolsó érvényes katalógust és mutassa az
adat korát; újraletöltés ne jelölje újként az epochot.
3. Ellenőrizd a hosszt, ellenőrzőösszeget, epochot és katalógusméret-korlátot.
4. Átvitel atomikusan történjen: a BLE megszakadása ne hagyjon csonka cache-t.
5. TLE-frissítés csak a rotor megengedett állapotában történjen, a
leállítás felfüggesztése nélkül.
6. Frekvenciát ne következtess a TLE-ből; a rádiót külön kell konfigurálni.

## Átvonulások és önálló működés

1. Az alkalmazás az ESP32-ben SGP4-gyel számolt átvonulásokat kérdezze le;
az UTC-idő legyen egyértelmű.
2. Ugyanazt a műholdat válaszd a listában/átvonulásnál/követésnél;
katalógusfrissítéskor ne keveredjenek az indexek, a NORAD-azonosító
legyen a kulcs.
3. Horizont, kábelhatárok, beszerzés, zenit és sebesség: lehetetlen célokat
a rotor kifejezetten utasítsa el.
4. Az alkalmazás bezárása alatt a rotor csak akkor folytassa autonóm módon
az átvonulást, ha az adatok, érzékelők és biztonsági állapot továbbra is
érvényesek.
5. A fizikai leállító mobil, Bluetooth és böngésző nélkül is működjön.

## Android-kiadás

Az APK-t rögzített verziókkal kell fordítani, a hash-t/commitot meg kell
őrizni. Parser/UI-tesztek nem egyenértékűek a telefonnal és rotorral végzett
tesztekkel. A GitHub Actions előkészítése nem jelenti távoli futtatás vagy
áruházi terjesztés megtörténtét; a kiadási aláírást a tárolón kívül kell
védeni.
