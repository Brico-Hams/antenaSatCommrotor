# Elektronika: táplálás, meghajtók és érzékelők

Minden teszt egy jelölőnégyzet: csak akkor jelöld be, ha a mérés, a dátum és a műszer rögzítve van a nyilvántartásban.

## PWR — Táplálás, védelmek és leállítás

**A komponens várt viselkedése.** Lenyomott vészleállítónál egyetlen motor sem kaphat energiát, még ha a firmware vagy a host lefagy is; a CM5 és a logika tápot kap, hogy jelezze a hibát. A vészleállító elengedése NEM indítja újra a mozgást: újra kell élesíteni és ismételni a homingot.

### PWR-01
- [ ] **Művelet:** Motorok és rádió nélkül kösd be az áramkorlátos labortápot 0,2 A-re állítva, és emeld a névleges 12 V-ra.
- **Várt viselkedés:** Stabil üresjárati áram, nincs melegedés; 2 perc után semmi sem forró tapintásra.
- **Elfogadási kritérium:** Az áram a korlát alatt marad anélkül, hogy elérné; helyes polaritás (előbb ellenőrizd soros diódával/LED-del).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PWR-02
- [ ] **Művelet:** Mérd meg multiméterrel a 12 V-ot, 5 V-ot és 3,3 V-ot a csomópontjaikon (panel/CM5IO/kiegészítő) üresjáratban és terhelve.
- **Várt viselkedés:** A három sín ±5 %-on belül marad, és a motorok indulásakor nincs beesés.
- **Elfogadási kritérium:** Egyetlen GPIO sem lát 3,3 V-nál többet; a 12 V soha nem jut a CM5-re (CM5-PCB).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PWR-03
- [ ] **Művelet:** Csatlakoztatott motorokkal, 12 V-on nyomd le a vészleállítót, és mérd a VMOT-ot minden meghajtónál.
- **Várt viselkedés:** A VMOT minden tengelyen 0 V-ra esik; a logika/CM5 él és jelzi az ESTOP-ot.
- **Elfogadási kritérium:** VMOT < 1 V; az ESTOP_AUX_N (BCM10) aktív-magasra vált; nincs utómozgás.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PWR-04
- [ ] **Művelet:** Leállított rendszernél állítsd le és indítsd újra a hostot (a szolgáltatás kill -9-je és újraindítás) lenyomott vészleállítónál.
- **Várt viselkedés:** A fizikai megszakítás megmarad: újraindításkor egyetlen tengely sem mozdul.
- **Elfogadási kritérium:** Nulla mozgás; indítás után az állapot DISARMED, a homing nincs visszaállítva (G1-5).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PWR-05
- [ ] **Művelet:** Állítsd le a WATCHDOG_HEARTBEAT-et (BCM11) élesített motorokkal, mechanikai terhelés nélkül a padon.
- **Várt viselkedés:** A motorengedély megszűnik, a meghajtók letiltódnak (EN magas).
- **Elfogadási kritérium:** A lekapcsolási időt oszcilloszkóppal mérd és jegyezd fel; a watchdog pontos kialakítása nincs kiválasztva, ne találj ki értéket.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PWR-06
- [ ] **Művelet:** Idézz elő biztosítékhibát (vedd ki), és szakítsd meg minden NC érzékelő vezetékét.
- **Várt viselkedés:** Egyértelmű szoftverhiba és letiltott motorok.
- **Elfogadási kritérium:** Szakadt vezeték = MAGAS = hiba; sosem értelmezhető egészséges végállásként (LOW = egészséges).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PWR-07
- [ ] **Művelet:** Mérd a hullámosságot és tranzienseket a VMOT-on és az 5 V-on oszcilloszkóppal (rövid földrugó) a három motor gyorsítása és fékezése közben.
- **Várt viselkedés:** A tüskék és beesések a meghajtók és a CM5 által tűrt határokon belül vannak.
- **Elfogadási kritérium:** Nincs CM5-újraindulás, nincs meghajtóhiba; jegyezd fel a csúcstól csúcsig értéket (CM5-PCB EMI-kapu).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### PWR-08
- [ ] **Művelet:** Futtasd 30 percig a motorokat lassú váltakozó mozgással, és mérj hőkamerával/hőelemmel a meghajtókon, DC/DC-n, biztosítékon és Powerpole csatlakozókon.
- **Várt viselkedés:** Hőmérséklet-stabilizáció folyamatos eltolódás nélkül.
- **Elfogadási kritérium:** Egyetlen alkatrész sem lépi túl az adatlapi határt; a csatlakozók feszültségesése < 50 mV érintkezőnként üzemi áramnál.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

## DRV — Motorvezérlők (TMC5160 v1.5 a CM5-ön; TMC2209 az ESP32 hordozón)

**A komponens várt viselkedése.** Minden meghajtó LETILTVA indul (EN magas); csak a közös hardverengedéllyel és tengelyenkénti kéréssel engedélyezhető. A STEP/rámpa jeleket a meghajtó állítja elő (TMC5160 rámpa mód SPI-n), soha nem egy Linux-ciklus.

### DRV-01
- [ ] **Művelet:** Motor nélkül tápold be és olvasd ki SPI-n minden TMC5160 verzió/IOIN regiszterét (CS0 AZ, CS1 EL, CS2 POL).
- **Várt viselkedés:** Mindhárom a várt chipverzióval válaszol.
- **Elfogadási kritérium:** Mindhárom CS-en érvényes válasz; különben ellenőrizd az SPI1 kábelezést (MOSI BCM20, MISO BCM19, SCLK BCM21).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### DRV-02
- [ ] **Művelet:** Csatlakoztatott motorokkal és magas EN mellett ellenőrizd, hogy a tengelyek kézzel szabadon forognak (nincs tartónyomaték).
- **Várt viselkedés:** Letiltott meghajtónál nincs tartónyomaték.
- **Elfogadási kritérium:** Szabad forgás = a meghajtó valóban le van tiltva.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### DRV-03
- [ ] **Művelet:** Számítsd ki a fázisáramot a panelod mérőellenállásából és a motor névleges áramából, állítsd be az IRUN/IHOLD-ot, és mérd az egyik fázist lakatfogóval/árammérővel.
- **Várt viselkedés:** A mért RMS áram ≈ a számított.
- **Elfogadási kritérium:** ±10 %-on belül és sosem a motor névleges árama felett; ne másold egy másik NEMA14 értékét.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### DRV-04
- [ ] **Művelet:** Forgass egy tengelyt pontosan 10 motorfordulatot a meghajtó rámpáján, és számold jelöléssel/enkóderrel.
- **Várt viselkedés:** Mechanikai fordulat = a várt lépésszám (200 lépés × 16 mikrolépés × áttétel).
- **Elfogadási kritérium:** A felhalmozott hiba < 1 motorlépés; ügyelj rá, hogy az interpolált 256 mikrolépést ne számold valódi lépésnek.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### DRV-05
- [ ] **Művelet:** Idézz elő meghajtóhibát (szimulált túlmelegedés, vagy kikapcsolt meghajtónál egy fázis lecsatlakoztatása), és figyeld a FAULT_AZ_N/EL_N/POL_N-t (BCM24/25/26).
- **Várt viselkedés:** A hiba jelzett, a motorok letiltottak; nincs automatikus újrapróbálkozás.
- **Elfogadási kritérium:** A hiba látható a host állapotában és az alkalmazásban; törléséhez rehome szükséges.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### DRV-06
- [ ] **Művelet:** Mérd a meghajtó hőmérsékletét 10 perc üzemi áram után zárt dobozban.
- **Várt viselkedés:** Stabil hőmérséklet.
- **Elfogadási kritérium:** Az adatlapi határ alatt, tartalékkal; különben adj hűtőbordát/szellőzést és ismételd.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

## SNS — Érzékelők: AS5600, NC végálláskapcsolók, GNSS, iránytű/IMU

**A komponens várt viselkedése.** Hiányzó vagy tartományon kívüli érzékelő egyértelmű hibát okoz, soha nem kitalált értéket. Az álló GNSS NEM ad irányt.

### SNS-01
- [ ] **Művelet:** Pásztázd az I2C1-et a TCA9548A multiplexeren (0x70) át: válaszd ki minden csatornát és olvasd az AS5600-at (0x36).
- **Várt viselkedés:** Csatornánként egy AS5600; a multiplexer resetje (BCM13) helyreállítja a buszt.
- **Elfogadási kritérium:** Mindhárom AS5600 egyenként válaszol; kettő egy csatornán multiplexer nélkül hibás pásztázást ad (várt).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SNS-02
- [ ] **Művelet:** Olvasd az AS5600 STATUS (MD/ML/MH) és AGC értékét a beépítési mágnestávolságnál; forgass 360°-ot.
- **Várt viselkedés:** MD=1 (mágnes észlelve), ML=MH=0, AGC középtartományban; a szög monoton 0-tól 4095-ig.
- **Elfogadási kritérium:** Nincs MH/ML a teljes fordulaton; átmérős mágnes középen; fordítsd az irányt, ha fordítva forog.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SNS-03
- [ ] **Művelet:** Hasonlítsd az AS5600 szögét szögmérővel/mérőórával 8 pozícióban.
- **Várt viselkedés:** Az olvasat egyezik a referenciával.
- **Elfogadási kritérium:** Hiba ≤ 0,5° (12 bites felbontás ≈ 0,088°); jegyezd fel az eltérést és a mechanikai játékot.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SNS-04
- [ ] **Művelet:** Működtesd mindegyik végálláskapcsolót (AZ min/max, EL min/max, POL min/max) és figyeld a BCM4, 5, 6, 7, 8, 9-et.
- **Várt viselkedés:** Egészséges = ALACSONY; működtetett vagy szakadt vezeték = MAGAS.
- **Elfogadási kritérium:** Mind a hat reagál; a motor a végállás irányában tiltott; a szoftver NEM helyettesíti a fizikai ütközőt.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SNS-05
- [ ] **Művelet:** GNSS kültéren vagy ablaknál: várj a fixre és hasonlítsd az UTC-t és a pozíciót ismert referenciához; mérd a PPS-t (BCM27) oszcilloszkóppal.
- **Várt viselkedés:** Érvényes NMEA, 1 Hz-es PPS.
- **Elfogadási kritérium:** UTC-hiba < 1 s a referenciához képest; stabil PPS; koordináták és magasság a szoftver mértékegységeiben (magasság méterben).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SNS-06
- [ ] **Művelet:** Vedd le a GNSS antennát és figyeld az idő/hely állapotát a hoston.
- **Várt viselkedés:** Az UTC/hely érvénytelenné válik a türelmi idő után; a követés blokkolt.
- **Elfogadási kritérium:** Egyértelmű figyelmeztetés és biztonságos leállás (G3-4); sosem követ csendben elavult UTC-vel.
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

### SNS-07
- [ ] **Művelet:** Iránytű/IMU: irányítsd az antennát ismert valódi irányra (nap/referencia) kikapcsolt és bekapcsolt motorokkal; jegyezd fel a különbséget.
- **Várt viselkedés:** Stabil, ismételhető olvasat fémtől távol.
- **Elfogadási kritérium:** A deklinációval korrigált eltérés dokumentált; ha az aktív motorok megváltoztatják az olvasatot, vidd távolabb az érzékelőt (távoli iránytű).
- _Mért eredmény ____ · Dátum ____ · Műszer ____ · Állapot: FÜGGŐ_

[Vissza a tartalomjegyzékhez](README.md)
