"""Bench design content (equipment list, levels, GPIO tester, stop chain) in es/en/hu."""
LEVELS = [
 ('B0', dict(es='Mesa digital', en='Digital desk', hu='Digitális asztal'),
  dict(es='Ordenador de desarrollo, 2 teléfonos Android (8-11 y 12+), opcional CM5/Raspberry. Sin energía de potencia.', en='Development computer, 2 Android phones (8-11 and 12+), optional CM5/Raspberry. No power stage.', hu='Fejlesztői számítógép, 2 Android telefon (8-11 és 12+), opcionálisan CM5/Raspberry. Teljesítményfokozat nélkül.'),
  'SW, APP-01…06, PCB-01…03'),
 ('B1', dict(es='Electrónica sin PCB fabricada', en='Electronics without a fabricated PCB', hu='Elektronika gyártott PCB nélkül'),
  dict(es='Fuente de banco, cadena de parada, emulador de guarda en placa de prototipos, comprobador GPIO, 3 drivers TMC5160 en adaptador, motores NEMA14, AS5600 + TCA9548A + MCP23017 en módulos, finales NC, GNSS, CM5 + CM5IO.', en='Bench supply, stop chain, guard emulator on prototype board, GPIO tester, 3 TMC5160 drivers on breakouts, NEMA14 motors, AS5600 + TCA9548A + MCP23017 modules, NC limit switches, GNSS, CM5 + CM5IO.', hu='Labortáp, leállítási lánc, védelmi emulátor próbapanelen, GPIO-tesztelő, 3 TMC5160 meghajtó adapteren, NEMA14 motorok, AS5600 + TCA9548A + MCP23017 modulok, NC végállások, GNSS, CM5 + CM5IO.'),
  'PWR, DRV, SNS, PCB-04…07, APP-07…10'),
 ('B2', dict(es='Mecánica', en='Mechanics', hu='Mechanika'),
  dict(es='Rotor montado en un banco rígido con carga de 0,5 kg, goniómetro, indicador de dial, báscula, cámara térmica/termopar.', en='Rotor mounted on a rigid bench with a 0.5 kg load, protractor, dial indicator, scale, thermal camera/thermocouple.', hu='Merev padon rögzített forgató 0,5 kg-os terheléssel, szögmérő, mérőóra, mérleg, hőkamera/hőelem.'),
  'MEC'),
 ('B3', dict(es='RF', en='RF', hu='RF'),
  dict(es='VNA con kit de calibración, carga de 50 Ω ≥ 25 W, atenuadores, vatímetro, SDR como fuente/monitor, antena en exterior.', en='VNA with calibration kit, 50 Ω load ≥ 25 W, attenuators, wattmeter, SDR as source/monitor, antenna outdoors.', hu='VNA kalibráló készlettel, 50 Ω-os lezárás ≥ 25 W, csillapítók, wattmérő, SDR forrásként/monitorként, antenna kültéren.'),
  'ANT, RAD'),
 ('B4', dict(es='Sistema en campo', en='System in the field', hu='Rendszer a terepen'),
  dict(es='Trípode, batería elegida, estación completa, referencia de rumbo/horario, satélite real.', en='Tripod, chosen battery, complete station, heading/time reference, real satellite.', hu='Állvány, választott akkumulátor, teljes állomás, irány-/időreferencia, valódi műhold.'),
  'SYS'),
]
# (ref, qty, es, en, hu, used in)
EQUIP = [
 ('EQ-01', '1', 'Fuente de banco 0–30 V / 0–5 A con límite de corriente', 'Bench supply 0–30 V / 0–5 A with current limit', 'Labortáp 0–30 V / 0–5 A áramkorláttal', 'PWR, DRV'),
 ('EQ-02', '1', 'Cadena de parada: seta de emergencia con enclavamiento NC (contacto DC) o contactor DC + contacto auxiliar NC', 'Stop chain: latching NC emergency stop (DC-rated contact) or DC contactor + NC auxiliary contact', 'Leállítási lánc: reteszelt NC vészleállító (DC-névleges érintkező) vagy DC kontaktor + NC segédérintkező', 'PWR'),
 ('EQ-03', '1', 'Fusible y portafusibles dimensionados por cable y consumo; conectores Powerpole', 'Fuse and holder sized for wire and load; Powerpole connectors', 'Vezetékre és fogyasztásra méretezett biztosíték és tartó; Powerpole csatlakozók', 'PWR'),
 ('EQ-04', '1', 'Osciloscopio ≥ 100 MHz, 2-4 canales, con muelle de masa', 'Oscilloscope ≥ 100 MHz, 2-4 channels, with ground spring', 'Oszcilloszkóp ≥ 100 MHz, 2-4 csatorna, földrugóval', 'PWR, DRV, SNS'),
 ('EQ-05', '1', 'Analizador lógico de 8 canales o más (≥ 24 MS/s) con decodificador SPI/I2C/UART', 'Logic analyser, 8+ channels (≥ 24 MS/s) with SPI/I2C/UART decoding', 'Logikai analizátor 8+ csatornával (≥ 24 MS/s), SPI/I2C/UART dekódolással', 'DRV, SNS, PCB'),
 ('EQ-06', '1', 'Multímetro de 4½ dígitos o mejor, pinza amperimétrica DC', '4½-digit multimeter or better, DC clamp ammeter', '4½ jegyű multiméter vagy jobb, DC lakatfogó', 'PWR, DRV'),
 ('EQ-07', '1', 'Cámara térmica o termopar K de 2 canales', 'Thermal camera or 2-channel K thermocouple', 'Hőkamera vagy 2 csatornás K hőelem', 'PWR, DRV, MEC'),
 ('EQ-08', '1', 'Comprobador del contrato GPIO (placa de prototipos propia, ver abajo)', 'GPIO-contract tester (own prototype board, see below)', 'GPIO-szerződés tesztelő (saját próbapanel, lásd alább)', 'PCB-05'),
 ('EQ-09', '3', 'Driver TMC5160 v1.5 (SilentStepStick) en adaptador / placa de prototipos', 'TMC5160 v1.5 driver (SilentStepStick) on breakout / prototype board', 'TMC5160 v1.5 meghajtó (SilentStepStick) adapteren / próbapanelen', 'DRV'),
 ('EQ-10', '3', 'Motor NEMA14 bipolar de 200 pasos (el mismo modelo previsto)', 'NEMA14 bipolar 200-step motor (the intended model)', 'NEMA14 bipoláris 200 lépéses motor (a tervezett típus)', 'DRV, MEC'),
 ('EQ-11', '3+1', 'Módulo AS5600 + imanes diametrales (uno de repuesto)', 'AS5600 module + diametric magnets (one spare)', 'AS5600 modul + átmérős mágnesek (egy tartalék)', 'SNS'),
 ('EQ-12', '1+1', 'Módulos TCA9548A (0x70) y MCP23017 (0x20)', 'TCA9548A (0x70) and MCP23017 (0x20) modules', 'TCA9548A (0x70) és MCP23017 (0x20) modulok', 'SNS, PCB'),
 ('EQ-13', '6', 'Finales de carrera NC con cable y conector', 'NC limit switches with cable and connector', 'NC végálláskapcsolók kábellel és csatlakozóval', 'SNS'),
 ('EQ-14', '1', 'Módulo GNSS UART 3,3 V con antena y PPS', '3.3 V UART GNSS module with antenna and PPS', '3,3 V-os UART GNSS modul antennával és PPS-sel', 'SNS'),
 ('EQ-15', '1', 'Brújula/IMU remoto y referencia de norte verdadero (nivel de burbuja)', 'Remote compass/IMU and true-north reference (bubble level)', 'Távoli iránytű/IMU és valódi észak referencia (libella)', 'SNS, SYS'),
 ('EQ-16', '1', 'CM5 + placa oficial CM5IO + almacenamiento + disipador', 'CM5 + official CM5IO board + storage + heatsink', 'CM5 + hivatalos CM5IO panel + tároló + hűtőborda', 'SW, PCB, APP'),
 ('EQ-17', '2', 'LimeSDR Mini con cable USB y SMA', 'LimeSDR Mini with USB and SMA cables', 'LimeSDR Mini USB és SMA kábelekkel', 'RAD'),
 ('EQ-18', '1', 'Banco rígido (tablero de 18 mm) y fixture del rotor con carga de 0,5 kg', 'Rigid bench (18 mm board) and rotor fixture with 0.5 kg load', 'Merev pad (18 mm-es lap) és forgatórögzítő 0,5 kg-os terheléssel', 'MEC'),
 ('EQ-19', '1', 'Goniómetro, indicador de dial, calibre, báscula de 0,1 g / 5 kg', 'Protractor, dial indicator, calipers, 0.1 g / 5 kg scale', 'Szögmérő, mérőóra, tolómérő, 0,1 g / 5 kg-os mérleg', 'MEC'),
 ('EQ-20', '1', 'VNA (p. ej. NanoVNA o LibreVNA) con kit SOL + THRU', 'VNA (e.g. NanoVNA or LibreVNA) with SOL + THRU kit', 'VNA (pl. NanoVNA vagy LibreVNA) SOL + THRU készlettel', 'ANT'),
 ('EQ-21', '1', 'Carga ficticia de 50 Ω ≥ 25 W, atenuadores 10/20 dB, vatímetro RF', '50 Ω dummy load ≥ 25 W, 10/20 dB attenuators, RF wattmeter', '50 Ω-os műterhelés ≥ 25 W, 10/20 dB csillapítók, RF wattmérő', 'ANT, RAD'),
 ('EQ-22', '2', 'Teléfonos Android 8-11 y 12+ con el APK debug', 'Android phones 8-11 and 12+ with the debug APK', 'Android telefonok 8-11 és 12+ a debug APK-val', 'APP'),
 ('EQ-23', '1', 'Cable de audio aislado (aislador de masa) y WAV de prueba SSTV/APRS', 'Isolated audio cable (ground isolator) and SSTV/APRS test WAVs', 'Leválasztott audiokábel (földleválasztó) és SSTV/APRS teszt-WAV-ok', 'RAD, APP'),
]
STOP = dict(
 es='''Cadena de parada del banco (replica la del diseño, sin PCB):
`fuente + → fusible → interruptor general → contacto DC de la seta NC enclavada (o contactor DC) → bus VMOT → drivers`.
El contacto auxiliar NC de la misma seta va a `ESTOP_AUX_N` (BCM10, nivel sano = BAJO). La lógica (CM5, 5 V, 3,3 V) cuelga ANTES de la parada, para seguir viva y señalar el fallo. El contacto de la parada debe soportar la corriente de los tres motores con margen (el modelo exacto del diseño está sin seleccionar).''',
 en='''Bench stop chain (mirrors the design, without a PCB):
`supply + → fuse → main switch → DC contact of the latching NC stop (or DC contactor) → VMOT bus → drivers`.
The NC auxiliary contact of the same stop goes to `ESTOP_AUX_N` (BCM10, healthy level = LOW). The logic (CM5, 5 V, 3.3 V) is connected BEFORE the stop, so it stays alive and reports the fault. The stop contact must carry the three motors\' current with margin (the exact part of the design is unselected).''',
 hu='''A pad leállítási lánca (a tervet másolja, PCB nélkül):
`táp + → biztosíték → főkapcsoló → a reteszelt NC vészleállító DC érintkezője (vagy DC kontaktor) → VMOT sín → meghajtók`.
Ugyanennek a vészleállítónak az NC segédérintkezője az `ESTOP_AUX_N`-re megy (BCM10, egészséges szint = ALACSONY). A logika (CM5, 5 V, 3,3 V) a leállító ELŐTT csatlakozik, így él és jelzi a hibát. A leállító érintkezőjének tartalékkal kell viselnie a három motor áramát (a terv pontos alkatrésze nincs kiválasztva).''')
TESTER = dict(
 es='''Comprobador del contrato GPIO (placa de prototipos, NO es producción): se enchufa a la cabecera de 40 pines de la CM5IO y solo usa 3,3 V.
- Cada **salida** del CM5 (WATCHDOG_HEARTBEAT, MOTOR_ARM_REQUEST, TCA9548A_RESET_N, CS SPI, PTT_*_REQUEST…) alimenta un LED con resistencia de 2,2 kΩ a GND, para ver su nivel seguro tras reiniciar.
- Cada **entrada** (6 finales NC, ESTOP_AUX_N, FAULT_*_N, GNSS_PPS) lleva pull-up de 10 kΩ a 3,3 V, resistencia serie de 330 Ω y un interruptor a GND: cerrado = BAJO = sano; abierto/cable roto = ALTO = fallo.
- Los buses (I2C1, SPI1, UART GNSS) salen a pines de sonda para el analizador lógico.
- Nunca se conecta 5 V ni 12 V a esta placa.
La figura T2 lista las 26 señales de `hardware/cm5/interface.json` con su elemento de prueba.''',
 en='''GPIO-contract tester (prototype board, NOT production): it plugs into the CM5IO 40-pin header and uses 3.3 V only.
- Each CM5 **output** (WATCHDOG_HEARTBEAT, MOTOR_ARM_REQUEST, TCA9548A_RESET_N, SPI CS, PTT_*_REQUEST…) drives an LED with a 2.2 kΩ resistor to GND, to see its safe level after reboot.
- Each **input** (6 NC limits, ESTOP_AUX_N, FAULT_*_N, GNSS_PPS) has a 10 kΩ pull-up to 3.3 V, a 330 Ω series resistor and a switch to GND: closed = LOW = healthy; open/cut wire = HIGH = fault.
- The buses (I2C1, SPI1, GNSS UART) break out to probe pins for the logic analyser.
- 5 V or 12 V is never connected to this board.
Figure T2 lists the 26 signals of `hardware/cm5/interface.json` with their test element.''',
 hu='''GPIO-szerződés tesztelő (próbapanel, NEM gyártási): a CM5IO 40 tűs tüskesorára dugható, és csak 3,3 V-ot használ.
- A CM5 minden **kimenete** (WATCHDOG_HEARTBEAT, MOTOR_ARM_REQUEST, TCA9548A_RESET_N, SPI CS, PTT_*_REQUEST…) egy LED-et hajt 2,2 kΩ-os ellenálláson át a GND-re, hogy újraindítás után látható legyen a biztonságos szint.
- Minden **bemenet** (6 NC végállás, ESTOP_AUX_N, FAULT_*_N, GNSS_PPS) 10 kΩ felhúzót kap 3,3 V-ra, 330 Ω soros ellenállást és kapcsolót a GND-re: zárt = ALACSONY = egészséges; nyitott/szakadt vezeték = MAGAS = hiba.
- A buszok (I2C1, SPI1, GNSS UART) mérőtűkre vannak kivezetve a logikai analizátorhoz.
- Erre a panelre soha nem kötünk 5 V-ot vagy 12 V-ot.
A T2 ábra felsorolja az `hardware/cm5/interface.json` 26 jelét a hozzájuk tartozó tesztelemmel.''')
