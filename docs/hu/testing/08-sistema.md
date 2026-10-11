# Rendszerintegráció (G3 / G4)

Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.

## SYS — Rendszerintegráció és a G3 / G4 kapuk

**A komponens várt viselkedése.** Ha minden modul külön el van fogadva, ebben a sorrendben integrálj: mechanika RF nélkül, passzív RF, vétel és vezérlés, és csak legvégül az engedélyezett adás. Helyváltoztatás után semmi sem használható újra: újra kell kalibrálni.

### SYS-01
- [ ] **Művelet:** Kövess egy valódi műholdátvonulást, és hasonlítsd független referenciához, azonos állomással és TLE-vel.
- **Várt viselkedés:** Irányzás az egész átvonulás alatt.
- **Elfogadási kritérium:** Az irányzási hiba az antennanyaláb belsejében (G3-1); parancsolt és mért AZ/EL napló.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SYS-02
- [ ] **Művelet:** Internet nélkül (saját AP): importálj TLE-t, válassz, jósolj és kövess; zárd be az alkalmazást az átvonulás alatt.
- **Várt viselkedés:** A követés a vezérlőn folytatódik.
- **Elfogadási kritérium:** A számítás és követés nem függ a telefontól (G3-2/3).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SYS-03
- [ ] **Művelet:** Idézz elő: GNSS-vesztést, érvénytelen UTC-t, régi gyorsítótárat, elveszett enkódert, horizont alatti átvonulást, zenitet, kábelfeltekerést és elérhetetlen sebességet.
- **Várt viselkedés:** Dokumentált szabály, figyelmeztetés és biztonságos leállás minden esetben.
- **Elfogadási kritérium:** Egyértelműen elutasítva; soha nem irányít rossz célra (G3-4/5).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SYS-04
- [ ] **Művelet:** Erősítsd meg a valódi északot ismert referenciával; mozgasd az állványt és ismételd a kalibrációt.
- **Várt viselkedés:** A valódi tájolás minden helyszínen megerősítve.
- **Elfogadási kritérium:** A kalibráció új helyszínen nem használható újra (G3-7).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SYS-05
- [ ] **Művelet:** Mérd meg az üzemkész együttest és mérd az üzemidőt a választott akkumulátoron 2 órás folyamatos próbával.
- **Várt viselkedés:** Mért tömeg és üzemidő.
- **Elfogadási kritérium:** ≤ 5 kg a külső akkumulátor nélkül és a 2 órás cél üzemidő mérésekkel igazolva, nem számítással.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SYS-06
- [ ] **Művelet:** G4, csak engedéllyel: próbaadás terhelésre minimális teljesítménnyel, majd engedélyezett valódi átvonulás; figyeld a hálózatok és csatlakozók hőmérsékletét.
- **Várt viselkedés:** Tiszta adás; nincs TX illesztetlen hálózattal vagy a diplexer/hibrid tartományán kívül.
- **Elfogadási kritérium:** Egyszerre csak egy TX aktív; a saját lejövő jel figyeléséhez védett második vevő kell; passzív szűrővel nem állítható full-duplex.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

[Vissza a tartalomjegyzékhez](README.md)
