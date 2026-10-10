# CM5/RF-választás: bizonyítékok, interfészek és kizárások

Adatgyűjtés dátuma: 2026-10-10. Ez a nyilvántartás különválasztja a komponens dokumentált képességét, az architektúra-választást és azokat az összeállítási teljesítményeket, amelyekhez próbapadi igazolás kell. Nem gyártási kiadás.

## Aktuális architektúra

CM5 a beszerzett hivatalos CM5IO-val, saját AZ/EL/POL segédpanellel és két cserélhető LimeSDR Minivel. Két párhuzamos VHF/UHF vevő; mindkét lánc TX-képes, de a kezdeti szabályzat csak egy aktív TX-et enged. Az új változatban nincs ESP32; a korábbi változat maradjon történeti.

| Elem | Elsődleges bizonyíték | Korlát |
|---|---|---|
| CM5 | [Hivatalos adatlap](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008180-DS-7-cm5-datasheet.pdf) | A pontos RAM/eMMC/wireless változatot, hőmérsékletet, fogyasztást és rögzítést vizsgáld |
| CM5IO | [Rögzített hivatalos dokumentáció](https://github.com/raspberrypi/documentation/blob/62ba0a0c2dd5030fe9b19458fa9bd174a451f79b/documentation/asciidoc/computers/compute-module/introduction.adoc) | Két natív USB3; perifériák, áram és USB2-szerep a teljes összeállításban minősítendő |
| LimeSDR Mini 2.x | [Rögzített hardverdokumentáció](https://github.com/myriadrf/LimeSDR-Mini-v2/blob/bcab0b65506c7c9dbee2a79a76a951aa8f1cd48d/docs/v2.4/index.rst) | 10 MHz–3,5 GHz; modulonként egy RX/egy TX, SMA aljzat, 69×31,4 mm; pontos revízió tömege ellenőrzendő |
| Lime teljes duplex | [Gyártói oldal](https://www.crowdsupply.com/lime-micro/limesdr-mini-2) és [egyidejű RX/TX példa](https://github.com/myriadrf/LimeSuite/blob/699d05b7212aa612a9802c219dd6621be88c77db/src/examples/dualRXTX.cpp) | Modulképesség, nem a vevő PA-/antennajellel szembeni immunitása |
| Lime mintavételi frekvenciák | [Rögzített API](https://github.com/myriadrf/LimeSuite/blob/699d05b7212aa612a9802c219dd6621be88c77db/src/API/LimeSDR_mini.cpp) | Ez a klasszikus API 100 ksample/s-től hirdet tartományt; ellenőrizd a valós eszközt, ne feltételezz 96 ksample/s RF-et |
| TMC5160 v1.5 | [Watterott tűkiosztás](https://learn.watterott.com/silentstepstick/pinconfig/tmc5160/) és [rögzített kapcsolási rajz](https://github.com/watterott/SilentStepStick/blob/098b7518b0de31e6a12fda78c68ae2666b81fbb6/hardware/SilentStepStick-TMC5160_v15.pdf) | A pontos modul strapjait/konfigurációját/óráját/áramát/hűtését ellenőrizd; nem tetszőleges StepStickre érvényes |

A 4 GB RAM/16 GB eMMC-s CM5 wireless változat beszerzési jelölt, nem teljesítménymérés, és a többi modellhez nem kötelező módosítás. CM5, SDR, hűtőborda vagy hordozópanel tömegét ne becsüld a méretekből.

## Determinisztikus mozgás és GPIO

Három, önálló rámpagenerátoros meghajtó lehetővé teszi, hogy a Linux pozíciót kérjen STEP-jelek nem determinisztikus ciklusban való előállítása nélkül. A javasolt SPI1-foglalás: GPIO16/17/18 chip select, GPIO19/20/21 MISO/MOSI/SCLK. I2C GPIO2/3 és UART GPIO14/15 érzékelő/GNSS számára lefoglalva. **A foglalás nem jóváhagyott netlist**; a fagyasztott és tesztelt segédpaneltérkép az irányadó.

Watterott TMC5160 v1.5 esetén: SD_MODE jumpert nyisd a dokumentált mozgásvezérlő-módhoz, SPI_MODE=VIO, SD_MODE=GND, VIO=3,3 V; EN magas szinten letiltja a kimeneteket; CLK=GND belső órát választ. CS-hez külső felhúzó kell. DCO kimenet, nem nSLEEP. Sebesség/gyorsulás konverzióhoz ellenőrizd az órafrekvenciát és tűrést. Ezeket a részleteket más revízióra ne alkalmazd a saját kapcsolási rajza ellenőrzése nélkül.

A CM5IO 1,8/3,3 V logikát választhat; a 3,3 V-os segédpanelnek megfelelő konfiguráció szükséges. A meghajtók nem helyettesítik az NC-végállásokat, enkódereket, homingot vagy a Linux-független tápmegszakítót/watchdogot.

## USB, hang és energia

A két Lime a két natív USB3 portot foglalja el. További USB-hangkodekhez minősített gazdacsatlakozás/táplált hub kell; harmadik portot nem szabad feltételezni. Az I2S alternatíva az SPI1-gyel való konfliktus felülvizsgálatát igényli. Linksebesség nem garantált alkalmazásszintű áteresztés.

A CM5IO dokumentált tápja 5 V/5 A; 5 V/3 A mellett perifériákra 600 mA marad a hivatkozott dokumentum szerint. Vizsgáld meg a valós tápegységet, USB-C egyeztetést és kábelt. A külső 12 V-os LiFePO4 akkumulátorhoz megfelelő átalakító szükséges; 12 V-ot ne köss USB-C-re/CM5 5 V-os sínre.

A transzparens Bluetooth-hang 8 ksample/s, S16LE mono esetén irányonként 128 kbit/s, duplexen 256 kbit/s, fejlécek/újraküldések előtt. Az ESP32 húszbájtos vezérlő BLE-keretei nem igazolják a hangot. Az új interfész, veszteség és credit modell a [RADIO-HOST.md](RADIO-HOST.md) dokumentumban szerepel; Android/CM5 fizikai teszt még hátravan.

## Miért nem megfelelőek a hivatkozott eszközök közvetlen RF-láncnak?

- A [(tr)uSDX](https://dl2man.de/) és [uSDX SOTA](https://antrak.org.tr/blog/usdx-sota-modular-all-mode-sdr-hf-transceiver-for-qrp-operations/) HF-referencia; formátuma/CAT-ja nem igazolja a 145/435 MHz-et.
- SA8x8 és hasonló FM-megoldásokhoz a kiválasztás nem talált igazolt AM/USB-megvalósítást. SSB-t ne állíts csak azért, mert az alkalmazásban módválasztó van.
- RTL-SDR Blog V4 csak vételre való; önmagában nem teljesíti az APRS/hang adását.
- A névleges 325 MHz-től induló Pluto 145 MHz-et nem fed le módosítás nélkül; nem támogatott hangolást ne tekints garantált képességnek.
- Az ATU-100 antennaillesztő, nem duplexer, PA vagy VHF/UHF adó-vevő.

A hivatkozások eredeti licenceit nem írjuk felül az új munka MIT/CERN licenceivel. Nem terjesztjük újra a hivatalos CM5IO forrásfájljait, és nem feltételezünk azonosítatlan nyílt licencet; a CM5IO-t megvásároljuk, dokumentációját tanulmányozásra hivatkozzuk.

## RF-teljesítmény: külön blokkoló

Célok: 5 W FM, 5 W PEP USB, 1 W AM vivő. A Lime kis teljesítményű, revízió/frekvenciafüggően kb. legfeljebb +10 dBm-et ad; ez nem több watt. Lineáris PA-k és sávonkénti szűrők kiválasztás és mérés függvényei.

5 W kb. 37 dBm; 10 dBm-ről 37 dBm-re ideálisan 27 dB erősítés kell veszteségek előtt. Ez nem határozza meg a biztonságos erősítést: a maximális erősítést, kompressziót, IMD-t, tranziens viselkedést és a meghajtás független korlátozását mérlegelni kell. 1 W AM vivő és 100% moduláció ideálisan 4 W PEP; a láncnak tartalék és spektrum-ellenőrzés kell. USB lineáris erősítőként HF E osztályú PA-t ne használj.

145 MHz × 3 = 435 MHz: egy VHF adó harmadik felharmonikusa az UHF vevősávba eshet. Két SDR, diplexer és RHCP/LHCP-választó nem bizonyít izolációt. Megfelelő terheléssel/műszerekkel mérd a vevő deszenzitizációját, blokkolását, felharmonikusokat, SWR-t, hőmérsékletet és IMD-t; kezdd minimális teljesítményen. RF-hálózatot TX alatt ne kapcsolj, kivéve ha a konkrét besorolás ezt igazolja.

A vétel, PTT-engedély, mechanikai POL-választás és körpolarizációs kéziség külön funkció. Tengelyirányú forgatás nem vált RHCP/LHCP-t. TX-et ne engedélyezz pusztán sikeres szoftverválaszra: fizikai engedély, igazolt RF-út és a valós lánc visszaolvasása is kell.
