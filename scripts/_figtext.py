"""Trilingual figure text: id -> {lang: (title, subtitle, [steps])}; legends and labels."""
LEG = {
 'part': {'es': 'Placa Al 3 mm', 'en': 'Al plate 3 mm', 'hu': 'Al lemez 3 mm'},
 'cup': {'es': 'Copa de rodamiento (ASA)', 'en': 'Bearing cup (ASA)', 'hu': 'Csapágytartó (ASA)'},
 'belt': {'es': 'Correa GT2', 'en': 'GT2 belt', 'hu': 'GT2 szíj'},
 'asa': {'es': 'Pieza ASA impresa', 'en': 'Printed ASA part', 'hu': 'Nyomtatott ASA alkatrész'},
 'base': {'es': 'Base ligera', 'en': 'Light base', 'hu': 'Könnyű alap'},
 'mast': {'es': 'Mastil', 'en': 'Mast', 'hu': 'Árboc'},
 'elem': {'es': 'Elementos', 'en': 'Elements', 'hu': 'Elemek'},
 'box': {'es': 'Caja', 'en': 'Enclosure', 'hu': 'Doboz'},
 'cradle': {'es': 'Soporte radio', 'en': 'Radio cradle', 'hu': 'Rádiótartó'},
 'cu': {'es': 'Cobre', 'en': 'Copper', 'hu': 'Réz'},
 'board': {'es': 'Placa / mascara', 'en': 'Board / mask', 'hu': 'Panel / maszk'},
 'silk': {'es': 'Serigrafia (logo BricoHams)', 'en': 'Silkscreen (BricoHams logo)', 'hu': 'Szitanyomat (BricoHams-logó)'},
 'safety': {'es': 'Seguridad / finales', 'en': 'Safety / limits', 'hu': 'Biztonság / végállások'},
 'other': {'es': 'Otras senales', 'en': 'Other signals', 'hu': 'Egyéb jelek'},
 'step': {'es': 'Paso', 'en': 'Step', 'hu': 'Lépés'},
}
X = {
'R1': dict(es=('Rotor BASE: piezas del reductor','Reduccion por correa GT2 25:1 (20T:100T x2)',[
  'Comprobar: 2 placas Al 3 mm (DXF), 8 separadores Al Ø8, 2 correas GT2 252 mm.','Poleas compradas: 2 x 20T y 2 x 100T; ejes acero Ø8x60 y Ø10x89.','Rodamientos 608 y 6000 con sus copas ASA y retenedores.','Motor NEMA14 provisional (cara 35 mm, agujeros a 26 mm).','Imprimir copas y retenedores en ASA; no imprimir poleas ni correas.']),
  en=('Rotor BASE: gearbox parts','GT2 belt reduction 25:1 (20T:100T x2)',[
  'Check: 2 Al plates 3 mm (DXF), 8 Al spacers Ø8, 2 GT2 belts 252 mm.','Purchased pulleys: 2 x 20T and 2 x 100T; steel shafts Ø8x60 and Ø10x89.','608 and 6000 bearings with their ASA cups and keepers.','NEMA14 motor is provisional (35 mm face, holes at 26 mm).','Print cups and keepers in ASA; do not print pulleys or belts.']),
  hu=('BASE forgató: a hajtómű alkatrészei','GT2 szíjhajtás 25:1 (20T:100T x2)',[
  'Ellenőrizd: 2 db 3 mm-es Al lemez (DXF), 8 db Ø8 Al távtartó, 2 db 252 mm-es GT2 szíj.','Vásárolt szíjtárcsák: 2 x 20T és 2 x 100T; acéltengelyek Ø8x60 és Ø10x89.','608-as és 6000-es csapágyak ASA tartókkal és rögzítőkkel.','A NEMA14 motor ideiglenes (35 mm-es homlok, 26 mm-es furatkiosztás).','A tartókat és rögzítőket ASA-ból nyomtasd; szíjtárcsát és szíjat ne.'])),
'R2': dict(es=('Rotor BASE: despiece del reductor','Orden de montaje de las dos etapas',[
  'Atornillar copas de rodamiento a la placa trasera (lado interior).','Insertar rodamientos 608 (eje Ø8) y 6000 (eje Ø10) en las copas.','Montar polea 20T en el eje del motor y polea 100T en el eje intermedio.','Colocar la primera correa; dejar 1 mm de holgura entre etapas.','Montar polea 20T intermedia y 100T de salida; segunda correa.','Cerrar con la placa frontal y los separadores; tensar con las ranuras ±1.5 mm.']),
  en=('Rotor BASE: gearbox exploded view','Assembly order of the two stages',[
  'Bolt the bearing cups to the rear plate (inner side).','Press the 608 (Ø8 shaft) and 6000 (Ø10 shaft) bearings into the cups.','Fit the 20T pulley on the motor shaft and the 100T on the intermediate shaft.','Fit the first belt; keep a 1 mm gap between stages.','Fit the intermediate 20T and the output 100T pulleys; second belt.','Close with the front plate and spacers; tension using the ±1.5 mm slots.']),
  hu=('BASE forgató: a hajtómű robbantott ábrája','A két fokozat összeszerelési sorrendje',[
  'Csavarozd a csapágytartókat a hátsó lemezre (belső oldal).','Nyomd be a 608-as (Ø8 tengely) és 6000-es (Ø10 tengely) csapágyakat a tartókba.','Szereld a 20T tárcsát a motortengelyre, a 100T tárcsát a köztes tengelyre.','Tedd fel az első szíjat; a fokozatok között hagyj 1 mm hézagot.','Szereld fel a köztes 20T és a kimeneti 100T tárcsát; második szíj.','Zárd le az elülső lemezzel és a távtartókkal; feszítsd a ±1,5 mm-es hosszlyukakkal.'])),
'R3': dict(es=('Rotor BASE: eje de azimut','Reductor, brida de salida e iman del encoder',[
  'Fijar la base ligera al tripode con los 4 tornillos.','Montar bandeja metalica y separadores sobre la base.','Colocar el reductor sobre los separadores; alinear eje de salida con el eje AZ.','Montar brida de salida y portaiman; sensor sobre el soporte del encoder.']),
  en=('Rotor BASE: azimuth axis','Gearbox, output flange and encoder magnet',[
  'Fix the light base to the tripod with the 4 screws.','Mount the metal tray and spacers on the base.','Place the gearbox on the spacers; align the output shaft with the AZ axis.','Mount the output flange and magnet holder; sensor on the encoder support.']),
  hu=('BASE forgató: azimut tengely','Hajtómű, kimeneti karima és enkóder-mágnes',[
  'Rögzítsd a könnyű alapot az állványhoz a 4 csavarral.','Szereld az alapra a fém tálcát és a távtartókat.','Tedd a hajtóművet a távtartókra; a kimeneti tengelyt told az AZ tengelybe.','Szereld fel a kimeneti karimát és a mágnestartót; az érzékelő az enkódertartóra kerül.'])),
'R4': dict(es=('Rotor BASE completo (AZ + EL)','Reductor AZ, soporte EL y segundo reductor en elevacion',[
  'Montar soporte metalico EL sobre la brida AZ.','Fijar segundo reductor con el eje EL horizontal.','Instalar silla de antena en el eje de salida EL.','Comprobar giro libre a mano y topes antes de energizar.']),
  en=('Complete rotor BASE (AZ + EL)','AZ gearbox, EL support and second gearbox in elevation',[
  'Mount the metal EL support on the AZ flange.','Fix the second gearbox with the EL axis horizontal.','Install the antenna saddle on the EL output shaft.','Check free rotation by hand and the end stops before powering up.']),
  hu=('Teljes BASE forgató (AZ + EL)','AZ hajtómű, EL tartó és második hajtómű az elevációs tengelyen',[
  'Szereld az EL fémtartót az AZ karimára.','Rögzítsd a második hajtóművet vízszintes EL tengellyel.','Tedd fel az antennanyerget az EL kimeneti tengelyre.','Áramra kapcsolás előtt kézzel ellenőrizd a szabad forgást és a végállásokat.'])),
'R5': dict(es=('Eje POL: despiece','Etapa GT2 5:1, eje hueco, 2 rodamientos 608',[
  'Insertar los 2 rodamientos 608 en el soporte.','Pasar el eje hueco y fijar la polea de salida.','Montar motor y polea pequena; colocar y tensar la correa.','Instalar topes de ±90°.']),
  en=('POL axis: exploded view','GT2 5:1 stage, hollow shaft, 2 x 608 bearings',[
  'Press the 2 x 608 bearings into the support.','Pass the hollow shaft through and fix the output pulley.','Mount the motor and small pulley; fit and tension the belt.','Install the ±90° stops.']),
  hu=('POL tengely: robbantott ábra','GT2 5:1 fokozat, üreges tengely, 2 db 608-as csapágy',[
  'Nyomd be a 2 db 608-as csapágyat a tartóba.','Vezesd át az üreges tengelyt és rögzítsd a kimeneti tárcsát.','Szereld fel a motort és a kis tárcsát; tedd fel és feszítsd a szíjat.','Szereld fel a ±90°-os ütközőket.'])),
'R6': dict(es=('Eje POL montado','Conjunto de polarizacion sobre la silla',[
  'Verificar giro libre ±90° sin tocar cables.','Unir al brazo de antena con la abrazadera.','Dejar lazo de cable para el recorrido completo.']),
  en=('POL axis assembled','Polarisation assembly on the saddle',[
  'Verify free ±90° rotation without cables binding.','Join to the antenna boom with the clamp.','Leave a cable loop for the full travel.']),
  hu=('Összeszerelt POL tengely','Polarizációs egység a nyergen',[
  'Ellenőrizd a szabad ±90°-os forgást a kábelek akadása nélkül.','Kösd az antennatartóhoz a bilincsel.','Hagyj kábelhurkot a teljes elfordulási úthoz.'])),
'A1': dict(es=('Antena: piezas impresas','Nucleo, brazos y bloques de fijacion',[
  'Imprimir en ASA las piezas del nucleo y bloques.','Retirar soportes y comprobar orificios.','Presentar en seco antes de pegar o atornillar.']),
  en=('Antenna: printed parts','Core, arms and fixing blocks',[
  'Print the core and blocks in ASA.','Remove supports and check the holes.','Dry-fit before gluing or screwing.']),
  hu=('Antenna: nyomtatott alkatrészek','Mag, karok és rögzítőblokkok',[
  'A magot és a blokkokat ASA-ból nyomtasd.','Távolítsd el a támaszokat és ellenőrizd a furatokat.','Ragasztás vagy csavarozás előtt próbáld össze szárazon.'])),
'A2': dict(es=('Antena V/U montada','Mastil con elementos radiales',[
  'Fijar el nucleo al mastil.','Montar los elementos con la longitud de la tabla de diseno.','Medir ROE en cada banda antes de conectar al sistema.']),
  en=('V/U antenna assembled','Mast with radial elements',[
  'Fix the core to the mast.','Fit the elements at the lengths in the design table.','Measure SWR on each band before connecting to the system.']),
  hu=('Összeszerelt V/U antenna','Árboc sugárirányú elemekkel',[
  'Rögzítsd a magot az árbochoz.','Szereld fel az elemeket a tervezési táblázat hosszaival.','Mérd meg az állóhullámarányt (SWR) minden sávon, mielőtt a rendszerhez kötöd.'])),
'C1': dict(es=('Cajas electronicas y soporte de radio','Tapas con logo BricoHams en relieve',[
  'Imprimir cajas en ASA (logo en la cara exterior de la tapa).','Insertar insertos roscados.','Montar PCB sobre separadores y cerrar con la tapa.']),
  en=('Electronics enclosures and radio cradle','Lids with embossed BricoHams logo',[
  'Print the enclosures in ASA (logo on the outer face of the lid).','Install threaded inserts.','Mount the PCB on spacers and close with the lid.']),
  hu=('Elektronikai dobozok és rádiótartó','Fedelek domború BricoHams-logóval',[
  'A dobozokat ASA-ból nyomtasd (a logó a fedél külső oldalán van).','Szereld be a menetes betéteket.','Szereld a PCB-t távtartókra és zárd le a fedéllel.'])),
'I1': dict(es=('Estacion completa','Rotor + antena montados',['Rotor sobre el tripode.','Antena sobre la silla EL.','Electronica fija en la base, no gira.']),
  en=('Complete station','Rotor + antenna assembled',['Rotor on the tripod.','Antenna on the EL saddle.','Electronics stay on the fixed base and do not rotate.']),
  hu=('Teljes állomás','Forgató + antenna összeszerelve',['Forgató az állványon.','Antenna az EL nyergen.','Az elektronika a fix alapon marad, nem forog.'])),
'E1': dict(es=('PCB portadora PortableSat','Capa superior (Gerber)',['Revisar el logo y la serigrafia sobre la placa.','Soldar primero SMD, luego conectores y pasantes.','Medir continuidad y cortos antes de energizar.','Primer arranque con fuente limitada en corriente.']),
  en=('PortableSat carrier PCB','Top layer (Gerber)',['Check the logo and silkscreen on the board.','Solder SMD first, then connectors and through-hole parts.','Check continuity and shorts before powering up.','First power-up with a current-limited supply.']),
  hu=('PortableSat hordozó PCB','Felső réteg (Gerber)',['Ellenőrizd a logót és a szitanyomatot a panelen.','Előbb az SMD alkatrészeket forraszd, aztán a csatlakozókat és a furatos alkatrészeket.','Bekapcsolás előtt mérd a folytonosságot és a zárlatokat.','Az első indítás áramkorlátos tápról történjen.'])),
'E2': dict(es=('PCB cm5-guard-A','Capa superior (Gerber, NO fabricar: prototipo)',['Solo revision: placa en estado de diseno, no apta para fabricacion.','Comprobar el logo y la serigrafia en KiCad.','Ejecutar DRC/ERC en KiCad antes de cualquier pedido (pendiente).']),
  en=('cm5-guard-A PCB','Top layer (Gerber, DO NOT manufacture: prototype)',['Review only: board is at design stage, not fit for manufacture.','Check the logo and silkscreen in KiCad.','Run DRC/ERC in KiCad before any order (pending).']),
  hu=('cm5-guard-A PCB','Felső réteg (Gerber, NEM gyártható: prototípus)',['Csak felülvizsgálatra: a panel tervezési állapotú, gyártásra nem alkalmas.','Ellenőrizd a logót és a szitanyomatot a KiCadben.','Bármilyen rendelés előtt futtass DRC/ERC-t a KiCadben (függőben).'])),
'E3': dict(es=('Cableado GPIO CM5','Contrato de senales (hardware/cm5/interface.json)',['Cablear segun la tabla; no inventar pines.','Finales de carrera y paro NC: nivel sano = bajo.','MOTOR_ARM_REQUEST arranca en bajo (seguro).','Pasos solo desde el controlador dedicado, nunca GPIO Linux.']),
  en=('CM5 GPIO wiring','Signal contract (hardware/cm5/interface.json)',['Wire according to the table; do not invent pins.','Limit switches and stop are NC: healthy level = low.','MOTOR_ARM_REQUEST idles low (safe).','Step pulses only from the dedicated controller, never Linux GPIO.']),
  hu=('CM5 GPIO-kábelezés','Jelszerződés (hardware/cm5/interface.json)',['A táblázat szerint kábelezz; ne találj ki érintkezőket.','A végálláskapcsolók és a vészleállító NC: egészséges szint = alacsony.','A MOTOR_ARM_REQUEST alaphelyzetben alacsony (biztonságos).','Léptetőimpulzus csak a dedikált vezérlőből jöhet, soha Linux GPIO-ról.'])),
'I2': dict(es=('Integracion colectiva','Secuencia de MODULE-INTEGRATED.md',['Cada modulo se acepta solo antes de unir.','No sumar dos CM5 ni dos sistemas de energia.','No puentear interbloqueos al quitar un modulo.']),
  en=('Collective integration','Sequence from MODULE-INTEGRATED.md',['Accept each module on its own before joining.','Do not add a second CM5 or second power system.','Do not bypass interlocks when removing a module.']),
  hu=('Közös integráció','A MODULE-INTEGRATED.md lépéssora',['Összekapcsolás előtt minden modult külön fogadj el.','Ne adj hozzá második CM5-öt vagy második tápellátó rendszert.','Modul eltávolításakor ne hidald át a reteszeléseket.'])),
}
FLOW = {
 'es': ['Aceptar por separado antena, rotor y radio','Montar tripode y base fija','Acoplar antena al rotor','RF SMA por banda, TX inhibido','Distribucion Powerpole/fusibles','Perfil integrated + identidades SDR','Calibrar UTC, norte y ceros AZ/EL/POL','Validar pases, Doppler, audio, SSTV/APRS (sin TX)','Cualificar TX/full-duplex con carga e instrumentos','Pesar conjunto (<=5 kg) y ensayar autonomia 2 h'],
 'en': ['Accept antenna, rotor and radio separately','Mount tripod and fixed base','Couple the antenna to the rotor','SMA RF per band, TX inhibited','Powerpole/fuse distribution','Integrated profile + SDR identities','Calibrate UTC, north and AZ/EL/POL zeros','Validate passes, Doppler, audio, SSTV/APRS (no TX)','Qualify TX/full-duplex with load and instruments','Weigh assembly (<=5 kg) and test 2 h endurance'],
 'hu': ['Antenna, forgató és rádió külön elfogadása','Állvány és fix alap felszerelése','Az antenna csatlakoztatása a forgatóhoz','SMA RF sávonként, TX tiltva','Powerpole/biztosíték elosztás','Integrated profil + SDR-azonosítók','UTC, észak és AZ/EL/POL nullpontok kalibrálása','Átvonulások, Doppler, hang, SSTV/APRS (TX nélkül)','TX/full-duplex minősítése terheléssel és műszerekkel','Az együttes mérése (<=5 kg) és 2 órás üzemidő-próba'],
}
