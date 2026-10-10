# Reprodukálható számítások és az értelmezés korlátai

E példák egyetlen bemenete a [design.json](../../calc/design.json).
Futtasd a [engineering-report.cjs](../../scripts/engineering-report.cjs)
fájlt az újraszámításhoz, a kapcsolatokat pedig a projekt tesztjeivel
ellenőrizd. Ezek a számítások függetlenek az RF- és terheléspróbáktól.

## Kezdeti hosszak sávonként

Kiinduló empirikus modell Tomas Brincil hivatkozásából:

```text
lambda = c / f
L_dipolo_total = lambda / 2 * 0,92
L_reflector_total = 1,05 * L_dipolo_total
distancia_reflector = 0,225 * lambda
```

| Mennyiség | 145 MHz | 435 MHz |
| --- | ---: | ---: |
| Hullámhossz, mm | 2067,534 | 689,178 |
| Dipólus TELJES hossza, mm | 951,066 | 317,022 |
| Dipóluskarok hossza, mm | 475,533 | 158,511 |
| Kezdeti vágás karonként (+10 mm), mm | 485,533 | 168,511 |
| Reflektor TELJES hossza, mm | 998,619 | 332,873 |
| Reflektor távolsága, mm | 465,195 | 155,065 |

Ne keverd össze a teljes hosszt az egyes karok hosszával. Egy keresztezett
dipólus sávonként két, egymásra merőleges dipólusból áll; egy keresztezett
reflektor is két, egymásra merőleges elemből áll. A vezető átmérője, a
táplálási rés, toldások, műanyagok, boom és más sávok hatnak a rezonanciára
és impedanciára. Ezek a számok nem jelentenek optimalizált Yagi-antennát,
és a körpolarizációt sem bizonyítják.

A VHF-távolság mutatja, miért nem elég ehhez a geometriához egy merev
300 mm-es boom; az eredeti szerelésnél szétszedhető szakaszok szükségesek.
A vezető összecsukásnál a folytonosságot fém és mechanikus reteszek őrzik,
nem a zsanér véletlenszerű érintkezése.

### Negyedhullámú koax: példa, nem teljes hibrid

`L_coax = lambda / 4 * VF`

Feltételezett VF=0,66 mellett 145 MHz-en 341,143 mm, 435 MHz-en
113,714 mm. Mérd meg a kábel tényleges VF-értékét. Két ilyen hosszúságú
50 ohmos átkötő önmagában nem alkot illesztett, 50 ohmos osztót/hibридet.
Az RF-kézikönyvben leírt topológia, impedanciák, lezárás, egyensúly és mérés
szükséges.

## Bolygómű

Rögzített gyűrű, bemenő napkerék és kimenő bolygóhordozó esetén:

`i = 1 + N_korona / N_nap = 1 + 72/18 = 5`

Két sorba kapcsolt fokozat: `i_összes = 5*5 = 25`.

| Paraméter | Érték |
| --- | ---: |
| Modul | 1,5 mm |
| Nyomásszög | 20 fok |
| Nap / bolygó / gyűrű fogszám | 18 / 27 / 72 |
| Osztóköri átmérő | 27 / 40,5 / 108 mm |
| Bolygó keringési sugara | 33,75 mm |
| Bolygók száma | 3 |
| Fázisfeltétel | (18+72)/3 = 30, egész szám |

`N_korona = N_nap + 2*N_bolygó = 18+54 = 72`.
A szomszédos bolygók középtávolsága:
`2*33,75*sin(60 fok) = 58,46 mm`.
A bolygó közelítő külső átmérője egy modulnyi fogmagassággal:
`1,5*(27+2) = 43,5 mm`. Ebben az ideális keresztmetszetben a bolygók
nem metszik egymást; ez nem ellenőrzi a tartókat, csavarokat vagy az
axiális rétegezést.

Szabványos, korrekció nélküli, 20 fokos evolvens fog esetén:
`N_min ~= 2/sin(20 fok)^2 = 17,10`.
A 12 fogú napkerék profilkorrekciót/más feltételt igényel. A 18 fogas
alapválasztás elkerüli, hogy egy kis fogaskereket alámetszés-vizsgálat
nélkül elfogadjunk.

## Felbontás, nem pontosság

```text
200 lépés/fordulat * 16 microstep * 25 = 80000 parancs/fordulat
360 / 80000 = 0,0045 fok/parancs
```

A driver belső interpolációja nem növeli a parancsfelbontást. A végső
pontosság érzékelőktől, iránytól, dőléstől, játéktól, deformációtól,
excentricitástól és a rendelkezésre álló nyomatéktól függ. A kimeneten
kell mérni.

## Terhelőnyomaték: példa, amely NEM teljesíti a 8 m/s-os szélcélt

A példa feltételezései — nem egy megvásárolt motor specifikációi:

- Antenna tömege 0,5 kg, kiegyensúlyozatlansága 0,03 m.
- Motornyomaték 0,1 Nm, fokozatonként 0,7 hatásfok.
- Vetületi felület 0,06 m2, Cd=1,2, levegősűrűség 1,225 kg/m3.
- Szél 8 m/s, aerodinamikai kar 0,25 m.
- Előírt biztonsági tényező 2.

```text
T_gravitáció = m*g*d = 0,14715 Nm
F_szél = 0,5*rho*Cd*A*v^2 = 2,8224 N
T_szél = F*kar = 0,7056 Nm
T_szükséges_tartalékkal = 2*(0,14715+0,7056) = 1,7055 Nm
T_feltételezett_kimenet = 0,1*25*0,7^2 = 1,225 Nm
```

**A biztonsági tartalék nem teljesül. E számítás alapján ne üzemeltesd
8 m/s-os szélben.** A léptetőmotor hirdetett tartónyomatéka nem a menet
közbeni nyomatéka. Széllökés, súrlódás, gyorsulás és dőlés további
tartalékot követel. A kiegyensúlyozás segít a gravitáció ellen, de a
szélterhelést nem szünteti meg.

Ne próbáld ezt a hibát a specifikáción túli áram növelésével vagy azzal
orvosolni, hogy a nyomtatott fogaskerék biztosan elviseli a csökkentett
nyomatékot. Mérj, csökkents terhelést/szelet, módosíts aerodinamikát vagy
válts architektúrát.

## Állvány

A fényképezőgép-állvány 1/4-20 menete névlegesen 6,35 mm átmérőjű és
25,4/20 = 1,27 mm menetemelkedésű. A 3/8-16 menet névleges átmérője
9,525 mm, emelkedése 1,5875 mm. ASA menetes tartó helyett fém betétet/anyát
használj. Ezek a méretek nem bizonyítják az állvány torziós merevségét vagy
teherbírását.
