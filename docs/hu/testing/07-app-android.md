# Android-alkalmazás

Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.

## APP — Android-alkalmazás (arculat, súgó, TLE-letöltés és BLE-szinkron)

**A komponens várt viselkedése.** Az alkalmazás HTTPS-en tölt le TLE-t a CelesTrak, AMSAT vagy PE0SAT szolgáltatótól, és érvényesített privát gyorsítótárban tárolja; a pályákat csak a vezérlő számolja. A Raspberry/forgató felé az átvitel helyi BLE, 60 mp-es elakadásészleléssel, és az utolsó érvényes gyorsítótárat hiba esetén sosem írja felül.

### APP-01
- [ ] **Művelet:** Telepítsd a debug APK-t (GitHub Actions android.yml) egy Android 8-11 és egy Android 12+ telefonra; nyisd meg az alkalmazást.
- **Várt viselkedés:** Megjelenik a BricoHams-logó, a szerzők sora (Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina) és a bricohams.org; az indítóikon a BH-logó.
- **Elfogadási kritérium:** A logó mindhárom képernyőn (főoldal, digitális vevő, rádió host) és a Súgóban látható; nincs levágás sötét/világos módban.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-02
- [ ] **Művelet:** Koppints a Súgóra minden képernyőn, a telefon spanyol, angol és magyar nyelvével.
- **Várt viselkedés:** A képernyő súgószövege a telefon nyelvén (es, en vagy hu) megnyílik; hálózat nélkül.
- **Elfogadási kritérium:** A súgó olvasható és hibamentes; az idézett gombnevek egyeznek a felülettel (a felület es/en; a magyar mindkettőt idézi).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-03
- [ ] **Művelet:** Internettel próbáld ki egyenként a három szolgáltatót (CelesTrak, AMSAT, PE0SAT) a TLE letöltésével.
- **Várt viselkedés:** Előrehaladás bájtban és „letöltés kész” üzenet; a katalógus a helyi listában.
- **Elfogadási kritérium:** Bejegyzések > 0 friss epochhal legalább egy szolgáltatótól; jegyezd fel, hogy a három (CelesTrak, AMSAT, PE0SAT) közül melyik válaszol a hálózatodról és melyik nem.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-04
- [ ] **Művelet:** Ismételd meg a CelesTrak-letöltést többször egymás után, majd repülő üzemmódban.
- **Várt viselkedés:** Több egymást követő letöltés után a CelesTrak 403/429-et adhat; repülő üzemmódban hálózati hiba.
- **Elfogadási kritérium:** Konkrét használati korlát üzenet (várj pár órát/másik szolgáltató) vagy sikertelen letöltés üzenet; az utolsó érvényes gyorsítótár megmarad; nincs félrevezető „TLE érvénytelen: tle_http_…”.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-05
- [ ] **Művelet:** Importálj egy érvényes helyi TLE-fájlt, majd egyet rossz ellenőrzőösszeggel, egy csonkát és egyet, amelynek sorai végén szóközök vannak.
- **Várt viselkedés:** Az érvényes és a záró szóközös fájl importálódik; a rossz/csonka egyértelmű hibát ad.
- **Elfogadási kritérium:** A gyorsítótár csak érvényesítés és atomi csere után változik; a hibák megmutatják az okot.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-06
- [ ] **Művelet:** Tölts le 100-nál több műholdat tartalmazó katalógust.
- **Várt viselkedés:** Részhalmazt kell választani (legfeljebb 100).
- **Elfogadási kritérium:** 101 kijelölésnél a párbeszédablak elutasít; ≤ 100-nál mentés.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-07
- [ ] **Művelet:** Keress forgatókat (15 mp), válaszd ki kifejezetten a forgatót, erősítsd meg a passkeyt és mentsd a titkosított tokent.
- **Várt viselkedés:** Hitelesített kapcsolat ellenőrzött verziókkal.
- **Elfogadási kritérium:** „Hitelesítve, verziók ellenőrizve” üzenet; a csatlakozás NEM engedélyezi a motorokat. Ha 133-as hibával elbukik, az alkalmazás legfeljebb 2-szer újrapróbálja, mielőtt jelzi.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-08
- [ ] **Művelet:** Érvényes UTC mellett és READY/DISARMED módban koppints a katalógus átvitelére; kövesd az előrehaladást bájtban az „átvitel kész” üzenetig.
- **Várt viselkedés:** A TLE-k megérkeznek a vezérlőre (Raspberry/CM5); a host ugyanabban a sorrendben mutatja a frissített katalógust.
- **Elfogadási kritérium:** Teljes idő feljegyezve (≈ 512 karakter/blokk 20 bájtos kereteken); a katalógus hash egyezik az alkalmazásban és a hoston; nincs eltolási hiba.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-09
- [ ] **Művelet:** Az átvitel közben kapcsold ki a forgatót vagy vidd távolabb a telefont; várj 60 mp-et előrehaladás nélkül.
- **Várt viselkedés:** Az átvitel megszakad és a kapcsolat bomlik időtúllépés üzenettel; a vezérlőn a korábbi katalógus érintetlen.
- **Elfogadási kritérium:** A host korábbi katalógusa nem változik (atomi átvitel commit-tal); újracsatlakozás után az újrapróbálás működik.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-10
- [ ] **Művelet:** Válassz műholdat a vezérlő katalógusából és kérdezd le az átvonulásokat; hasonlítsd az AOS/LOS-t független referenciához (azonos állomás és TLE).
- **Várt viselkedés:** Konzisztens átvonulások; a vezérlő számol, nem a telefon.
- **Elfogadási kritérium:** AOS/LOS-eltérés < 30 mp; ha a számítás nem fejeződik be, a lekérdezési korlát jelezve a felhasználónak.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### APP-11
- [ ] **Művelet:** Digitális vevő: játssz le egy SSTV és egy APRS 1200 baud WAV-ot hangszóróval/kábellel a telefon hangbemenetére.
- **Várt viselkedés:** Az SSTV-kép és az AX.25 csomagok dekódolva; a napló menthető.
- **Elfogadási kritérium:** Helyes dekódolás ésszerű hangszinttel; az alkalmazásból nincs TX.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

[Vissza a tartalomjegyzékhez](README.md)
