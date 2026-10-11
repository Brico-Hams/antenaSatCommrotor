# Szoftver, CM5 hostok és OS-kép

Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.

## SW — Szoftver, CM5 hostok és az operációs rendszer képe

**A komponens várt viselkedése.** A teljes szoftvert fejlesztői számítógépen tesztelik, mielőtt hardverhez nyúlnának. A fordítás vagy az átmenő teszt NEM validálja a kábelezést, a mechanikát vagy az RF-et.

### SW-01
- [ ] **Művelet:** A tároló gyökerében futtasd: node --test "tests/*.test.cjs"
- **Várt viselkedés:** Minden teszt átmegy (66 a 2026-10-11-i felülvizsgálatban).
- **Elfogadási kritérium:** 0 hiba; bármilyen hiba blokkolja a további kapukat.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SW-02
- [ ] **Művelet:** Futtasd: PYTHONPATH=.:radio:rotor python3 -m pytest -q tests/rotor tests/radio_host
- **Várt viselkedés:** A forgatóvezérlő és a rádió host tesztjei.
- **Elfogadási kritérium:** 0 hiba (86 sikeres a felülvizsgálatban).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SW-03
- [ ] **Művelet:** Fordítsd és futtasd a natív vezérlési logikát (tests/control_logic/test_native) g++-szal és Unityvel; futtasd a node scripts/engineering-report.cjs parancsot.
- **Várt viselkedés:** Határ/idő/állapot logika és mérnöki számítások.
- **Elfogadási kritérium:** 6/6 natív teszt; a mérnöki jelentés nem jelez hibát.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SW-04
- [ ] **Művelet:** Hasonlítsd az SGP4-et egy független implementációhoz (azonos TLE, UTC és hely) egy átvonulás 10 időpontjában.
- **Várt viselkedés:** AZ/EL különbség.
- **Elfogadási kritérium:** ≤ 0,1° a zenittől távol (G0-3); azonos konvenciók és geodézia.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SW-05
- [ ] **Művelet:** Adj hibás adatot: csonka TLE, rossz ellenőrzőösszeg, régi epoch, HTML nevek, elérhetetlen forrás, túl nagy katalógus.
- **Várt viselkedés:** Minden esetben egyértelmű hiba.
- **Elfogadási kritérium:** Nincs mozgás és az érvényes gyorsítótár nem sérül (G0-7).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SW-06
- [ ] **Művelet:** Rendereld az összes alkatrészt OpenSCAD-del, és ellenőrizd a zárt hálót, a térfogatot és a váratlan komponensek hiányát (a domború logós fedeleket is).
- **Várt viselkedés:** Vízzáró hálók.
- **Elfogadási kritérium:** Minden alkatrész vízzáró; a render nem helyettesíti a fogaskapcsolat, hézagok és szerelési hozzáférés felülvizsgálatát (G0-5/6).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SW-07
- [ ] **Művelet:** Írd fel a BricoHams OS képet (os/build-image.sh Linuxon Dockerrel, vagy a build-os.yml munkafolyamat) a kártyára/eMMC-re, és indítsd a CM5-öt.
- **Várt viselkedés:** A BricoHams-banner megjelenik a konzolon és az /etc/issue fájlban; helyi bejelentkezés bricohams / Brico123 adatokkal.
- **Elfogadási kritérium:** Az első belépéskor változtasd meg a jelszót a passwd paranccsal; az SSH tiltva (a 22-es port zárva: nmap/ss); nincs titok, kulcs vagy Wi-Fi a képben. A képet eddig NEM építették meg és nem indították el.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SW-08
- [ ] **Művelet:** A CM5-ön futtasd a gpiodetect/gpioinfo parancsot, és válaszd ki azt a /dev/gpiochipN eszközt, amely a befagyasztott BCM-eltolásokat adja; indítsd a profilválasztót (rotor-only, radio-only, integrated).
- **Várt viselkedés:** A profil telepítve, és az /etc/bricohams/profile csak siker után jön létre.
- **Elfogadási kritérium:** Egyetlen modulszolgáltatás sem indul el magától; a biztonságos állapotot tartó szolgáltatás a GPIO-térkép ellenőrzése után indul; sikertelen telepítés függő jelölőt hagy.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

[Vissza a tartalomjegyzékhez](README.md)
