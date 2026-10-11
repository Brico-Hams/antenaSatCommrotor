# A forgató mechanikája

Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.

## MEC — A forgató mechanikája (AZ / EL / POL)

**A komponens várt viselkedése.** A tengelyek motor nélkül simán forognak, a szíjak tartják a feszességet, a fizikai ütközők a kábelek sérülése előtt megállítanak, és a hajtás a célterhelés alatt nem veszít lépést. A 8 m/s szél NEM engedélyezett határ, amíg a valós nyomatékot nem mérték.

### MEC-01
- [ ] **Művelet:** Nyomtass próbadarabokat (furat, tengely, betét), és mérd az ASA zsugorodását tolómérővel; nyomtasd ki a csapágytartókat és rögzítőket.
- **Várt viselkedés:** Mért méretek a névlegesekkel szemben.
- **Elfogadási kritérium:** A kompenzáció feljegyezve; a 608/6000 erőltetés és látható játék nélkül illeszkedik; nincs csiszolás a hibák elfedésére.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-02
- [ ] **Művelet:** Szereld össze a szíjas hajtóművet motor NÉLKÜL (20T:100T ×2 = 25:1, 252 mm GT2 szíjak); forgasd kézzel a kimenetet egy teljes fordulatot.
- **Várt viselkedés:** Sima, egyenletes forgás, fogugrás és szíjsúrlódás nélkül.
- **Elfogadási kritérium:** Egyenletes kézi nyomaték; a szíj egyenesen fut, nem ér a lemezekhez; 1 mm hézag a fokozatok között.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-03
- [ ] **Művelet:** Mérd a szíjfeszességet (lehajlás terheléssel a szakasz közepén) a ±1,5 mm-es hosszlyukakkal; 30 perc után ismételd.
- **Várt viselkedés:** Befutás után stabil feszesség.
- **Elfogadási kritérium:** Nincs megcsúszás vagy >10 % feszességvesztés; a csavarok csavarrögzítővel/alátéttel, semelyik nem lazul.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-04
- [ ] **Művelet:** Ellenőrizd, hogy a 2. fokozat bemeneti tárcsája rögzített az 1. fokozat kimeneti tengelyén (nem lebeg), és a kimeneti tengelyt két csapágy tartja.
- **Várt viselkedés:** Lekötött motornál, kézzel a kimenetre adott nyomatékkal csúszás nélkül átadódik a nyomaték.
- **Elfogadási kritérium:** Nulla relatív elfordulás a tárcsa és a tengely között; koncentrikus kimenet.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-05
- [ ] **Művelet:** Homing antenna nélkül a végálláskapcsolóval: a) csatlakoztatva, b) lecsatlakoztatva, c) beragadva, d) el nem érve.
- **Várt viselkedés:** a) AZ=-180°, EL=0° beállítva; b,c,d) hiba időtúllépéssel.
- **Elfogadási kritérium:** Soha nem korlátlan mozgás; a hiba rehome-ot igényel (G1-6).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-06
- [ ] **Művelet:** Mérd a holtjátékot irányváltással mérőórával vagy szögmérővel minden tengelyen.
- **Várt viselkedés:** Érték fokban tengelyenként.
- **Elfogadási kritérium:** Feljegyezve és szoftveresen kompenzálva; tájékoztató cél ≤ 1°; összhangban az SNS-03-mal.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-07
- [ ] **Művelet:** Egyensúlyozd a célterhelést (0,5 kg-os antenna) és mérd a súlypontot a tengelyhez képest; másodlagos rögzítéssel, stabil padon próbáld a tripod előtt.
- **Várt viselkedés:** A súlypont 30 mm-en belül a tengelytől.
- **Elfogadási kritérium:** Súlypont ≤ 30 mm; az EL tengely nem esik le áramszünetben, vagy rögzített (nyugalmi nyomaték motor nélkül).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-08
- [ ] **Művelet:** Lassú követés szélcsendben: járd be mindegyik tengelyt, és hasonlítsd az enkóderpozíciót referencia-szögmérőhöz/mérőórához 10 pozícióban.
- **Várt viselkedés:** Hiba pozíciónként.
- **Elfogadási kritérium:** Pontosság ≤ 2° RMS és legnagyobb eltérés ≤ 5° (G1-9); különítsd el az irányhibát a tengelyhibától.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-09
- [ ] **Művelet:** Futtass 30 percig váltakozó mozgást a célterhelés alatt; ellenőrizd az elveszett lépéseket, a lazulást és a hőmérsékletet.
- **Várt viselkedés:** A visszatérési pozíció azonos a kezdetivel.
- **Elfogadási kritérium:** Nincs lépésvesztés (végső hiba < 1°), nincs laza csavar, a hőmérsékletek a határokon belül (G1-10).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### MEC-10
- [ ] **Művelet:** Mérd meg a teljes üzemkész együttest (tartalmazza az állványt, rádiót és kábeleket; az külső akkumulátort nem, azt külön mérd) és a összecsukott méretet.
- **Várt viselkedés:** Teljes tömeg és méretek.
- **Elfogadási kritérium:** Tömeg ≤ 5 kg a jelenlegi követelmény szerint (a korábbi ≤ 3 kg történeti); az akkumulátor tömegét külön jegyezd fel.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

[Vissza a tartalomjegyzékhez](README.md)
