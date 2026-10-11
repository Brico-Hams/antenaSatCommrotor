# Gyártás előtti kapu a PCB-khez

Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.

## PCB — Gyártás előtti kapu a PCB-khez (ESP32 hordozó és cm5-guard-A)

**A komponens várt viselkedése.** Egyetlen panelt sem rendelnek meg és nem gyártanak le, amíg a kapu minden pontja nincs mérés és dátum mellett JÓVÁHAGYVA. Egy Gerber ZIP vagy render nem helyettesíti az ERC/DRC-t és a padot.

### PCB-01
- [ ] **Művelet:** Nyisd meg mindegyik projektet KiCadben, és futtasd az ERC-t, DRC-t, a „unconnected items”-t és a kapcsolási rajz/PCB paritást a dokumentált verzióval.
- **Várt viselkedés:** Nulla hiba és nulla indokolatlan figyelmeztetés.
- **Elfogadási kritérium:** A jelentés a reports/ alatt mentve; a szkripttel hozzáadott szitanyomat-logó miatt a DRC-t újra kell futtatni (ebben a változatban függőben).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PCB-02
- [ ] **Művelet:** Ellenőrizd, hogy minden gyártási fájl egyezik az SHA-256 értékével a reports/manifest-sha256.json és a fabrication/release-status.json fájlban (sha256sum).
- **Várt viselkedés:** Minden hash egyezik.
- **Elfogadási kritérium:** Bármilyen eltérés = ne gyártsd; generáld újra a manifestet a tároló szkriptjével.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PCB-03
- [ ] **Művelet:** Töltsd be a Gerbereket független nézegetőbe (KiCad Gerber Viewer, Tracespace vagy gerbv), és nézd át a rétegeket, furatokat, körvonalat és a BricoHams-logót a szitanyomaton.
- **Várt viselkedés:** Teljes rétegek, olvasható logó, pad vagy furat átfedése nélkül.
- **Elfogadási kritérium:** A logó távolsága ≥ 8 mm (carrier) és ≥ 21 mm (guard-A) a BRANDING.md szerint; nincs szitanyomat padokon.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PCB-04
- [ ] **Művelet:** Építsd meg a padon az egyenértékű áramkört (valódi modulok + prototípus-kábelezés) minden blokkra: táplálás, meghajtók, érzékelők, leállítás/watchdog.
- **Várt viselkedés:** Minden blokk teljesíti a PWR, DRV és SNS teszteket a padon.
- **Elfogadási kritérium:** E szakaszok minden tesztje JÓVÁHAGYVA a panel megrendelése előtt.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PCB-05
- [ ] **Művelet:** A GPIO-szerződés tesztelővel (pad, lásd PAD) járd végig az interface.json 26 jelét: minden kimenet a saját LED-jét hajtja, minden bemenet a saját kapcsolójára reagál.
- **Várt viselkedés:** A 26 jel egyezik a BCM-mel, a tüskesor lábával és az alapértelmezett biztonságos szinttel.
- **Elfogadási kritérium:** Nulla felcserélt vagy duplikált jel; újraindítás után minden kimenet a biztonságos szintjén.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PCB-06
- [ ] **Művelet:** Ellenőrizd a lábnyomokat az adatlapokhoz: DevKitC, SilentStepStick, MCP23017, TCA9548A, csatlakozók és biztosítékok 1. lába, tájolása és kiosztása; nyomtasd ki a PCB-t 1:1-ben papírra és tedd rá a valódi modulokat.
- **Várt viselkedés:** Minden lábnyom fizikailag illeszkedik.
- **Elfogadási kritérium:** Egyik modul sem ütközik másikkal, a doboz csavarjaival vagy a fedéllel (G1E-12).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PCB-07
- [ ] **Művelet:** Vizsgáld át a vezetősáv/teljesítménysáv áramkeretét (szélesség, réz, esés) a három motor áramával és a biztosítékkal.
- **Várt viselkedés:** A számított esés és hőmérséklet a határokon belül.
- **Elfogadási kritérium:** Számolt és a padon mérésekkel megerősített (PWR-02, PWR-08).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PCB-08
- [ ] **Művelet:** Készítsd elő a rendelést: BOM, CPL (hivatkozások, koordináták, oldal, forgatás), DNP/kézi modul lista, gyártói DFM és a pontos LCSC alkatrészek megerősítése.
- **Várt viselkedés:** A rendelésben nincs blokkoló DFM-figyelmeztetés; kifejezett jóváhagyás nélkül nem megy el rendelés.
- **Elfogadási kritérium:** Minden JÓVÁHAGYVA és egy második személy által ellenőrizve; ne fizess, amíg a PCB-01…07 nincs lezárva.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

[Vissza a tartalomjegyzékhez](README.md)
