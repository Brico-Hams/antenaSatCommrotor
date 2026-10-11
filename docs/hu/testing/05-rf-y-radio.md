# Antenna, RF és SDR rádió

Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.

## ANT — Antenna és passzív RF (VNA, hibrid, diplexer)

**A komponens várt viselkedése.** A forgatóval és a koaxokkal valós helyzetben az ÁHF ≤ 1,5 a középfrekvencián és ≤ 2 az üzemi csatornákon. A jó ÁHF NEM bizonyítja a cirkuláris polarizációt vagy a nyereséget: az együttest mérni vagy szimulálni kell.

### ANT-01
- [ ] **Művelet:** Kalibráld a VNA-t (OPEN, SHORT, LOAD, THRU) a csatlakozó síkjában, rádió nélkül.
- **Várt viselkedés:** Ellenőrzés 50 Ω-os lezárással: ÁHF ≈ 1,0.
- **Elfogadási kritérium:** Érvényes kalibráció minden mérési sorozat előtt (G2-1).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### ANT-02
- [ ] **Művelet:** Mérd sávonként a dipólusokat/reflektorokat (VHF 145 MHz, UHF 435 MHz) kihajtott együttessel, valós koax- és forgatóhelyzetben.
- **Várt viselkedés:** ÁHF-görbe és minimumfrekvencia.
- **Elfogadási kritérium:** ÁHF ≤ 1,5 a középen és ≤ 2 a csatornákon; dokumentáld a sávszélességet extrapoláció nélkül (G2-3).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### ANT-03
- [ ] **Művelet:** Mérd a hibridet sávonként: a kimenetek közötti amplitúdót és fázist a másik kapu 50 Ω-os lezárásával.
- **Várt viselkedés:** Aszimmetria és fázis.
- **Elfogadási kritérium:** Aszimmetria ≤ 0,5 dB és fázis 90° ± 5° a választott frekvenciákon (G2-4); megfelelő leválasztott lezárás.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### ANT-04
- [ ] **Művelet:** Mérd a 2 m/70 cm diplexert: beiktatási csillapítást ágonként, visszaverődési csillapítást és az ágak közötti leválasztást.
- **Várt viselkedés:** S21, S11 és keresztirányú S21.
- **Elfogadási kritérium:** Csillapítás ≤ 1 dB ágonként, visszaverődés ≥ 14 dB és leválasztás ≥ 40 dB szűrésként (G2-5); a 40 dB nem garantálja a deszenzibilizáció hiányát TX mellett.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### ANT-05
- [ ] **Művelet:** Ismételd az ÁHF-mérést 50 összecsukás/kinyitás után, és ellenőrizd az RF érintkezők folytonosságát.
- **Várt viselkedés:** ÁHF és folytonosság eltolódás nélkül.
- **Elfogadási kritérium:** ÁHF-változás < 0,1 és stabil folytonosság; a műanyag zsanérok nem az egyetlen RF érintkezők (G2-7).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### ANT-06
- [ ] **Művelet:** Mérd vagy szimuláld a sugárzási képet, az RHCP/LHCP értelmet és a tengelyarányt a teljes együttessel (antenna + koax + forgató).
- **Várt viselkedés:** Tengelyarány a műhold felé.
- **Elfogadási kritérium:** Tengelyarány ≤ 3 dB a cirkuláris polarizáció állításához (G2-6); e nélkül csak lineáris/kereszt polarizáció állítható.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### ANT-07
- [ ] **Művelet:** Vevővel és jelgenerátorral (vagy SDR-rel forrásként) mérd a minimálisan észlelhető szintet kikapcsolt és bekapcsolt forgatóval és átalakítókkal.
- **Várt viselkedés:** Zajszint motorokkal és anélkül.
- **Elfogadási kritérium:** Az eltérés dokumentált; az aktív motorok okozta zajnövekedés elfogadható legyen a célzott jelhez (G3-6).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

## RAD — SDR rádió (2 × LimeSDR Mini + CM5) és hang

**A komponens várt viselkedése.** A rádió forgató nélkül is működik vételben, két sorozatszámmal azonosított SDR-rel (VHF és UHF). A TX tiltva marad: csak fizikai engedéllyel, watchdoggal és lease-szel, terheléssel való minősítés után engedélyezhető.

### RAD-01
- [ ] **Művelet:** Csatlakoztasd mindkét LimeSDR-t USB-n és ellenőrizd a felismerést; jegyezd fel a két sorozatszámot és a VHF/UHF kiosztást.
- **Várt viselkedés:** Két különböző eszköz felismerve.
- **Elfogadási kritérium:** Soha nem „az első talált USB”: kifejezett kiválasztás sorozatszám szerint.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### RAD-02
- [ ] **Művelet:** Kérj mintavételi sebességet és frekvenciát, és olvasd vissza a hardverből; nyiss két egyidejű RX adatfolyamot (VHF és UHF).
- **Várt viselkedés:** A hardverből visszaolvasott értékek.
- **Elfogadási kritérium:** A kért sebesség nem ellenőrzött sebesség: jegyezd fel a visszaolvasottat; 10 perc alatt nincs mintaesés.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### RAD-03
- [ ] **Művelet:** Adj be referenciahangot/FM-et és ellenőrizd a demodulációt VHF-en és UHF-en; a DSP-t előbb WAV/vektorokkal, majd valós vétellel próbáld.
- **Várt viselkedés:** Helyes demodulált hang.
- **Elfogadási kritérium:** SNR és torzítás feljegyezve; a két vevő SSTV/APRS hangjait nem keverjük.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### RAD-04
- [ ] **Művelet:** Próbáld a Bluetooth PCM hangátvitelt (S16LE, mono, 8000 minta/s): kreditek, kiesések és újracsatlakozás.
- **Várt viselkedés:** Folyamatos adatfolyam szünet nélkül.
- **Elfogadási kritérium:** Nincs underrun 10 perc alatt; az aktív VHF/UHF csatornát kifejezetten kell választani; az átvitel nem jelent HFP/A2DP-t.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### RAD-05
- [ ] **Művelet:** Fizikai TX-engedély nélkül próbálj PTT-t a hostról/alkalmazásból és GPIO-ról (PTT_VHF_REQUEST BCM22, PTT_UHF_REQUEST BCM23).
- **Várt viselkedés:** A PTT elutasítva; a leválasztott kimenetek nyitottak (tiltottak); a PTT-visszajelzés konzisztens.
- **Elfogadási kritérium:** Engedély, watchdog és lease nélkül TX nem lehetséges; 50 Ω-os lezárással próbáld, soha antennával.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### RAD-06
- [ ] **Művelet:** Csak engedéllyel és jogosultsággal: minősítsd a TX-et minimális teljesítménnyel terhelésre: spektrum, felharmonikusok (145×3 = 435 MHz), blokkolás és hőmérséklet.
- **Várt viselkedés:** Tiszta spektrum és stabil hőmérséklet.
- **Elfogadási kritérium:** A felharmonikusok és mellékjelek a határokon belül; egyszerre csak egy TX aktív; G4 csak a G1-G3 jóváhagyása után.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

[Vissza a tartalomjegyzékhez](README.md)
