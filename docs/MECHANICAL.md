# Estación portátil modular — prototipo mecánico original

## FINAL: caja con plenums reales22 mm, sustituye cotas históricas siguientes

La caja final en `cad\carrier_enclosure.scad` es **interior224×174 mm,
exterior228×178×43.6 mm**, tapa2 y letras0.7 exteriores. PCB180×130 se sitúa
en esquina **(24,24), z8**: **22 mm libres por cada borde**, suficiente como
envolvente inicial para conectores/cables20 mm reportados, sin fingir que
2 mm anteriores los admitían. Mantiene32 mm desdePCB al techo y las cotas
confirmadas1.6mmPCB y3.2mmNPTH. Postes ahora en **(29,29),(199,29),
(29,149),(199,149)**, exactamente170×120 entre centros. Validar radio mínimo
de cable real;22 mm es espacio diseñado, no ensayo de todos los enchufes.

Paneles ciegos removibles se conservan para perforar según el conjunto
real; frente aperturas x20..60 y168..208, z15..37; lateral y25..55 y123..153.
No se atribuyen esos paneles a centrosUSB/JST/bornas sin plantilla medida.
Todos los cables tienen plenum antes de pared. Batería permanece **separada**
en bandeja fija y sus dimensiones definitivas siguen bloqueadas: no se la
modela arbitrariamente dentro de la caja.

Bandeja independiente actualDXF **aluminio2mm240×196**, cuatroM5 en patrón
180×30 y dosM4 coincidentes con orejas; peso nominal254g antes de agujeros.
No adelgazar soporte ni eliminar parking para compensarlo. ASA final caja:
base149957.5, tapa81678.9, dospaneles3102.0 y dos2502.0mm³,
total≈242844.5mm³/**259.84g ASA sólido**. Tapa lisa de este tamaño≈81095.6mm³;
relieve conectado añade583.3mm³≈0.624g. ASA totalBASE≈**1.009kg sólido**.

Presupuesto amplio actualizado: **3.522–4.407kg macizo**, escenario hipotético
75%materialASA **3.270–4.155kg**, incluyendo bandeja254g y batería. El antiguo
BuildLight2.679 condicionado, incrementos caja≈147.42g, bandeja254g y
carrierensamblado150–220g en vez100g dan **≈3.130–3.200kg**, ANTES de
buck/stop/cables adicionales. **Objetivo≤3kg incumplido en presupuesto actual
y no demostrado físicamente.** Las cifras2.748/2.916 y cajas184×134/188×138
en secciones históricas de abajo están **SUPERADAS**, no son montaje vigente.
Se requiere otra decisión de diseño/selección física para cumplir masa;
esta ampliación resuelve espacio de cableado, no demuestra estación≤3kg.

Los4STL finales se exportaron por archivo staged y pasaron el validador intacto;
tapa9024triángulos y un único componente conectado. SHA256tapa final:
`0C3E09D586A310A8FE5F26B071AE8EC72EA61FE250C590C94FEAFCA405B06B79`.
FontLiberationSansBold incluida; no sustitución de plataforma. DXF bandeja y
CSG actualizados. Los tests comprueban espacio44mm adicional por dimensión,
postes relativos, headroom, mallas y masa adicional; ajuste físico aún pendiente.

### Carrier PCB real180×130: caja modular estacionaria vigente

El agente hardware reporta placa ruteada **180×130 mm**, agujeros
**(5,5),(175,5),(5,125),(175,125)** desde esquinaPCB. **La caja antigua
interior124×64 no cabe y no se debe comprar/imprimir para esa placa.**
No se sustituye por una futuraPCB pequeña ficticia.

`cad\carrier_enclosure.scad` modela nueva caja original:
exterior188×138×43.6 mm más tapa2 mm, interior184×134, paredes/fondo2 mm,
PCB a z8 (postes6 sobre fondo2), **32 mm libres encima de PCB1.6 provisional**,
2 mm adicionales bajo tapa. PCB esquina(4,4), agujeros de carcasa
(9,9),(179,9),(9,129),(179,129), distancias170×120 idénticas al reporte.
El agentehardware confirma **PCB1.6 y taladros3.2mmM3**; CAD actualizado.
Verificar Gerber/drill y PCB fabricada antes de montar. OrigenPCB superior
izquierdo con coordenadas positivas, patrón rectangular simétrico coincide;
no invertir etiqueta/conectores al trasladar al CAD. M3 pasantes con arandelas y tuerca,
sin roscaASA; no montar componentes sobre esos postes.

Dos paneles extraíbles para aperturas40×22 en frente y dos30×22 en lateral.
Son tapas **ciegas**, no holes de conectores inventados: perforar/regenerar
según conectores y posición real, reservar enchufes y radio de coax/cable.
Hardware informa ESP≈10mm y drivers/disipadores15–20mm, dentro de headroom32;
driver/potencia abajo-izquierda, GNSS/sensores derecha. Es orientación reportada,
no agujeros de conectores inferidos. GNSS/IMU y dosAS5600 siguen conexiones
modulares; AS5600 físicos permanecen junto a sus ejes.
Envolvente transparente32mm muestra headroom, no componentes ruteados.
Caja y batería permanecen **estacionarias en bandeja/trípode** o como módulo
independiente junto al rotor; cable protegido y alivio de tensión.
No cargar caja grande sobre antena/bridaAZ.

`cad\carrier-metal-mount.dxf`: placa estacionaria aluminio2mm200×156,
dosM4 coincidentes con orejas de caja y cuatroM5 para abrazaderas de trípode/
bandeja en patrón140×30mm. Tornillos pasantes, arandelas, tuercas y separadores
aislantes; no hay encaje ficticio dentro rotor. Cortar/desbarbar y comprobar
capacidad del soporte; placa nominal≈168.5g antes de agujeros **se cuenta**.
No usar bandeja aislada como asa ni como apoyo de antena; respaldo/refuerzos/
abrazadera real y cableado aumentan reserva.

Cuatro nuevos selectores exportados en `cad\carrier-stl`: `base`, `lid`,
`port40`, `port30` (imprimir dos de cada panel). CSG en `cad\carrier-assembly.csg`,
script `cad\export-carrier.ps1`. CuatroSTL CGAL y dos pruebasNode aprobados.
Volumen sólido total con4paneles170138.6mm³≈**182.05g ASA**, sustituyendo
caja/tapa antigua112.0cm³≈113.04g: incremento **69.01g**.
ASA BASE vigente0.862→**0.931kg sólido**; no reducción ficticia de masaPCB.

BuildLight anterior2.679 se convierte nominalmente **2.748kg**, reserva252g,
si se reserva el incremento completo y todos los restantes límites cumplen.
Con escenarioASA previo75%, incremento también reservado completo da
≈2.934kg, solo66g de margen. **PCB180×130 poblada100g objetivo sigue sin pesaje**;
una PCBFR4 nominal1.6mm sola ronda69g usando1.85g/cm³, más cobre,ESP32,
drivers/conectores/GNSS puede superar ampliamente100g. Caja/placa nueva hace
más estrecho el objetivo; pesar electrónica+batería antes de afirmar≤3kg.
Motor candidato21mm sigue incompatible con base actual. Ninguna tabla de masa
condicionada equivale a aprobación mecánica/elétrica o medición.

**Marca elegida por usuario:** tapa de carrier180×130 integra texto en relieve
`BRICOHAMS` y `bricohams.org`, sin inventar logotipo oficial. Parámetros
`brand_name`, `brand_url`, `brand_raise=0.7`, `brand_font="Liberation Sans:style=Bold"`;
fontLiberationSans-Bold.ttf está incluido en OpenSCAD2021.01 portátil.
No se depende de sustituciónArial del sistema. Al usar otro OpenSCAD, instalar/
seleccionar esa familia o verificar visualmente y volver a renderizar.
Texto centrado en dos líneas12/8mm, lejos de tornillos/esquinas/puertos,
arranca z1.95 y acaba2.7: solapa0.05 con tapa2 y forma sólido conectado.
Offset0.03mm estabiliza contornos para impresión; no grabado inverso ni placa
flotante. Imprimir tapa cara plana hacia cama, letras hacia arriba; no afecta
headroom interior32mm ni incorpora metalRF.

Tapa marcada **52398.9mm³** frente51815.6 lisa: delta583.3mm³,
≈**0.624g ASA** nominal. BinSTL real9024triángulos, aristas cerradas/orientadas,
sin degenerados; prueba comprueba textos en CAD y aumento de volumen renderizado.
La primera salidaASCII produjo degenerados y fue rechazada; exportación final
binaria más contorno estabilizado sí pasó. CuatroSTLcarrier re-renderizados,
CSG/placaDXF regenerados. Masas previas de caja sin marca necesitan añadir0.624g,
irrelevante para aceptar3kg: no existe pesaje real ni aprobación.
Exportador escribe ahora `*.pending.stl`, valida y solo entonces reemplaza
STL final; evita que pruebas paralelas lean un render incompleto. Validador
conserva criterio de degenerados y añade conteo de componentes conectados:
tapa marcada **un único componente**, no letras flotantes. Re-render final y
11 pruebas mecánicas aprobadas. SHA256 tapa final:
`EC5806AA9FF4EB068FBC695D6CEEF794CD9DDE1DB68270D784114A5068320E34`.
Con la nueva bandeja metal2mm se añaden≈0.168kg: BuildLight condicionado
**≈2.916kg**, margen≈84g. El escenarioASA75% más bandeja supera3kg
(**≈3.102kg**). Batería/PCB/control aún no medidos: ≤3kg no probado,
su cumplimiento exige selección/diseño más ajustado, no omitir bandeja.

**Actualización final hardware:** carrier180×130, FR41.6 y cobre2oz en ambas
caras, NPTH3.2 confirmado. Fabricante de PCB no ha pesado unidad: reserva
placa desnuda≈100g conservadora y **ensambladaESP/TMC/disipadores/bornas/fusibles
150–220g**, más buck externo/stop/cables pendientes. El objetivo anterior
100g de electrónica poblada ya **no es defendible**. Sustituirlo por150–220g
añade50–120g: BuildLight condicionado≈**2.966–3.036kg**, antes de adicionales
pendientes y de comprobar incompatibilidad de motor21mm. Incluso rango favorable
deja≈34g de margen; extremo alto excede3kg. **No hay candidato listo que cumpla
≤3kg**; no presentar una suma provisional como aceptación.

Hardware pide≥30mm **sobrePCB**, confirmado ahora; espacio32 cumple nominalmente
esa interpretación con componentes20mm, no30 libres sobre componentes.
Conectores reportados: USB módulo a derecha y≥68, JST I/O cerca x157,
motores en borde y120, DC cerca x12/y18 izquierda (origenPCB superiorizquierdo).
Estas coordenadas son de componentes, no centros de aberturas de caja:
los paneles siguen ciegos hasta medir cable/enchufe y la placa montada.
Mantener libres los20mm para conectores/cable laterales reportados; interior
2mm de margen **no proporciona20mm lateral**, por lo que USB/bornas hacia
pared requieren panel abierto o aumento local/externo del compartimento.
No afirmar compatibilidad de cableado con tapa cerrada sin esa comprobación.

Buck comercialPololuD24V22F5 reportado17.8×17.8×8mm necesita **montaje separado
aislado** en bandeja fija/caja, fijado mediante soporte de dimensiones verificadas
y tornillos, no flotando sobrePCB. No se inventan agujeros del módulo ni se
integra fuera de límite sin dibujo. Dimensiones finales batería protegida y
AS5600breakout aún sin elección: bloqueos de fabricación/ensamblaje. Patrón
sensor16×16 anterior sigue provisional, no impuesto por carrierPCB.

## BASE vigente: reducción por correas, prioridad de masa

Por decisión explícita del usuario se permite cambiar transmisión para
perseguir≤3 kg incluyendo batería, excluyendo radio/trípode. **BASE vigente:
`cad\belt_station.scad`**. `cad\station.scad` conserva íntegro el planetario
anterior como **LEGACY opcional**, no se suman ambos BOM ni se construyen juntos.
Las secciones planetarias de este documento describen exclusivamente LEGACY.
Se mantiene AZ±180, EL0..90, antena desmontable, radio estacionario, AS5600,
finalesNC, trípode metal UNC y geometría RF sin validar.

BASE utiliza dos etapas **GT2 paso2 mm 20:100**, exactas5:1×5:1=**25:1**.
200 pasos completos×16 microsteps×25 conserva **80000 pasos/vuelta salida**;
comunicado al controlador. No implica resolución/precisión real de0.0045°.
Todas las poleas dentadas son **compradas de metal**, no dientes GT2 ASA
sin perfil probado. En CSG son envolventes declaradas de compra, no modelos
fabricables de polea ni promesa de SKU disponible. Correas compradas continuas
GT2 **126 dientes /252 mm, ancho6 mm**, cuatro en total.

### Centros, tensión, apoyos y transmisión físicos

Radios primitivos20t=6.3662 y100t=31.8310 mm. Longitud exacta de correa abierta:
`2 sqrt(C²−(R−r)²)+π(R+r)+2 asin((R−r)/C)(R−r)`.
Se resuelve **C=60.56301755 mm**; envolventes no se solapan. Contacto polea20:
**130.2718° /7.237 dientes**. No asumir capacidad de par de esa cifra;
consultar fabricante de correa con velocidad/tensión y curva motor.
Centros en una reductora: motor x−C, intermedio x0, salida x+C, todos y0.
Dos planos de correa a z15..21 y28..34 (coordenadas locales).

Placas de aluminio6082 **3 mm** nominal187.126×86, frente z0..3,
trasera54..57. DXF de corte:
`cad\belt-front-plate.dxf`, `cad\belt-rear-plate.dxf`; bandejaAZ
`cad\belt-tray.dxf`. Las placas **no son STL
ASA**. Copas ASA48 mm exterior sostienen608 (8×22×7) y6000(10×26×8),
dos de cada por eje. Frente3..13, trasera44..54; rodamientos se apoyan contra
placa metal y labio externo de copa. Alinear sin forzar antes de apretar.
Las caras interiores de rodamientos separados≈40 mm apoyan ejes acero
**8×60 intermedio y10×89 salida**, dos de cada, no eje motor impreso.
Los desplazamientos diferenciales de ambas copas deforman ejes: ajustar
ambos apoyos conjuntamente y comprobar coaxialidad.

* Etapa1: poleas z14..26 incluyendo bridas/hub.
* Etapa2: z27..39. Separación hub1/hub2 **1 mm**.
* Copas traseras empiezan44: **5 mm** respecto hub2.
* Placa trasera acaba57; brida de carga empieza60, espacio3.
* Brida60..78, imán81..93, sensor95..98; eje acaba89.
* Poleas100 compradas: bridaOD≤66.662, ancho axial total≤12, hubOD≤30.
  Poleas20: ancho≤12, hubOD≤18. **Medir dibujo real antes de compra**;
  muchas poleas comerciales tienen hubs más largos, no cabrán sin rediseño.
* Eje motor saliente **≥26 mm desde cara** para llegar a primera polea;
  NEMA14 corto no sirve automáticamente. Paso agujeros26 y cara35 provisionales.
* Shaft intermedio une polea100 de primera etapa a20 de segunda por llave
  metálica/collarines o pasadores correctamente dimensionados. Salida100 y brida
  unen acero10 mediante llave/pasador; no transmisión por adhesivo/ASA.
  Agujeros de pasadores y keyways debilitan sección: mecanizar/ensayar.

**Tensor real:** ranuras horizontales3 mm en montaje de motor y ambos soportes
intermedios, no una rueda tensora decorativa. Salida fija; mover intermedio a
x negativo aumenta C2. Mover motor aún más negativo para restablecer C1.
Rango±1.5 por pieza permite pequeño pretensado, no compensar correa errónea.
Cuatro tornillosM3 por copa y arandelas grandes, motor cuatroM3, apretar tras
ajuste según tensión máxima de fabricante. Añadir tornillos de ajuste M4 y
contratuerca sobre pestañas metálicas o usar calibre de distancias;
no tensar con ASA flexible como referencia. Un exceso carga rodamientos y eje.
Hubs reales deben dejar plano de correa libre de cabezas/collarines.

AZ: cara reductora a45 mm sobre base; motor z11..45 queda libre. Cuatro
separadores metálicos36 soportan placa delantera sobre bandeja fija z6..9,
no motor suspendido de plástico. EL sobre soporte de aluminio plegado3 mm
con refuerzos/remaches o tornillos: interfaz bridaM4 compartida. EjeEL60 mm
sobre base del soporte; placas86 mm altas quedan17 mm sobre ella. Ventana
38×38 libera motorEL; cuatro fijacionesM4 de carcasa. Copas y placas
constituyen camino estructural; perfil plegado/refuerzos requiere fabricación
metal real y prueba de rigidez, no imprimir su envolvente.

AS5600 fijado a placa trasera mediante dos espaciadoresmetal20 mm y soporte
impreso, **no girando con salida**. Imanes6×2 diametrales a eje de salida.
Radio/cajas permanecen en bandeja fija al trípode (no renderizadas de nuevo
en vistaBASE), antena/silla/montajeNC se reutilizan. Faltan levas específicas,
guardas de correas, cableado real y comprobación de cabezas/hubs/llaves:
**conjunto es diseño de integración, no assembly-tested ni listo para operar**.
CSG muestra envolventes honestas; no se exportan compras metálicas como STL
imprimible. Verificar barridosAZ/EL, sensor frente a silla, coaxial, soportes
y batería completa antes de energizar.

### Backdrive, carga y transporte

Correas son **reversibles/backdrivable**; no atribuir bloqueo de reductora
planetaria ni freno al motor apagado. Balancear antena y aparcar baja/inmovilizada
con **pasador metálico de parking o correa independiente al bastidor**,
retirado antes de motorizar. Pérdida de energía puede dejar caerEL: sujetar/
desmontar antena antes de cortar; no personas debajo. Reducir hold-current
solo tras prueba térmica y control de seguridad. Mantener límites de carga
provisionales500 g/CG≤30 mm y pruebas de viento previas, no transferir el
torque/eficiencia ASA a correa. Eficiencia de correas no medida.

### Masa comparativa inicial y criterio de decisión (antes de carrier180×130)

Impresión BASE comparte accesorios pero no las34 piezas pesadas de reductora.
Cuatro nuevos STL (`base`, `cup608`, `cup6000`, `encoder_support`) se exportan
en `cad\belt-stl`; resto común en `cad\stl`. **ASA sólido equivalente0.862 kg**,
frente2.521 kg del LEGACY. CantidadesBxx del CSV reemplazan Pxx/Mxx; grupos
compartidosB08..B10 detallan selectores, no componentes adicionales.

Presupuesto de masa con motor/batería/cableado seleccionados posteriormente:
metal motores0.24–0.36, ocho poleas0.16–0.24, correas0.020–0.035,
ocho rodamientos0.130–0.150, ejes acero0.169, cuatro placas+soporteEL+bandeja
0.680–0.780, separadores/herrajes0.150–0.250, antena/RF/coax0.360–0.580,
control/batería0.350–0.580 kg. Placas cuatro187×86×3 aportan hasta0.521 kg
antes de agujeros; soporte plegado/bandeja completan reserva.

**Macizo:3.121–4.006 kg**. Ejemplo hipotético de fracción material75% de ASA
(NO infill75% ni resultado slicer): **2.905–3.790 kg**. Extremo favorable
entra nominalmente≤3, pero solo95 g de margen y ningún pesaje: **objetivo no
probado**. Selección pesada incumple. Aceptación requiere pesar cada grupo,
informe real de slicer y **masa total ensamblada≤3.000 kg**, incluyendo batería,
sin radio/trípode. No rebajar asientos/dientes/ejes para maquillarlo.
Si compras reales superan presupuesto, detener y revisar estructura metal
mecanizada o arquitectura antes de fabricar; no publicar estación≤3 kg.

ValidaciónBASE: cuatro STL CGAL sin warnings, aristas cerradas/orientadas;
DXF placas, CSG de conjunto. PruebaNode confirma centros, longitud exacta,
ratio, wrap, stack y mallas. Dos variantes: seis pruebasNode aprobadas.
Ningún análisis de resistencia, dibujo proveedor, full collision sweep ni
ensayo físico realizado. `cad\export-belt.ps1`, `tests\mechanical-belt.test.cjs`,
`tests\mechanical-belt-mass.cjs` reproducen exportación/auditoría.

### BuildLight inicial: selección candidata (actualización carrier arriba prevalece)

Revisión documental de productos de fabricante (10 octubre2026), sin compra
ni medición y sin nuevas modificaciones estructurales:

* [Pololu1207 /SOYO SY35ST26-0284A](https://www.pololu.com/product/1207):
  **130 g publicados por motor**, NEMA14 35×35×26 mm,200 pasos/vuelta,
  280 mA/fase,7.4 V nominal de bobina, holding torque650 g·cm≈0.0637 Nm.
  **EjeD5 saliente21 mm: NO compatible con montajeBASE actual que exige26**.
  No aprobarlo ni afirmar que encaja. Posible revisión posterior de orientación
  de hub de polea20 hacia motor, con dibujo comercial y nueva verificación
  axial, o acople metálico especificado y apoyo; no extender eje con piezaASA.
  Corriente y curva dinámica requieren ensayo; holding torque no autoriza500g.
* [TalentCell YB1203000-USB](https://talentcell.com/lithium-ion-battery/12v/yb1203000-usb.html):
  **“About190g” publicado**,11.1 V3000mAh≈33.3 Wh nominal, salida
  **9–12.6 V /3 A máximo** y5 V/2 A máximo. No pesa190g garantizados:
  pesar unidad. Evitar lluvia/humedad, no abrir pack y usar cargador correcto.
  Compatibilidad con protección/carrier/regulador pendiente del agentePCB;
  no alimentar motores desde salida5 V ni asumir12 V regulados. Reservar
  margen al undervoltage y simultaneidad de cargas.

Se descarta batería1S de pequeño peso con boost improvisado: pérdidas/corriente
y protección podrían incumplir. No se reducen espesores3 mm, apoyos de acero,
rodamientos ni retención mecánica de parking para bajar una cifra.

La tabla siguiente es **plan de compra/fabricación BuildLight condicionado**:
solo motor y batería tienen masas de producto publicadas; restantes son
**límites de masa por grupo**, no cifras de proveedor. Se acepta grupo únicamente
tras plano/selección/pesaje ≤límite. No es BOM ya cerrado ni demostración≤3kg.

|Grupo|Límite/candidato kg|Base de cifra y condición|
|---|---:|---|
|ASA todas las piezas y cajas|0.460|Objetivo slicer/pesaje; actual sólido0.862; no garantizado por infill|
|Dos motoresPololu1207|0.260|Publicado130g cada; montaje21mm actualmente incompatible|
|Ocho poleas metal|0.160|Límite compra; dibujo y masa reales pendientes|
|Cuatro correas|0.020|Límite compra; especificación GT2 verificable pendiente|
|Ocho rodamientos|0.130|Límite compra; conservar4x608/4x6000|
|Ejes acero8×60 y10×89|0.169|Cálculo geométrico, sin cambiar apoyos|
|Placas3mm, soporteEL y bandeja|0.680|Geometría/densidad y reserva, no reducción de espesor|
|Separadores, tornillos, llaves, Ubolts y parking|0.150|Límite conjunto; no omitir freno/parking ni herrajes|
|Antenas, fibra, coax y redesRF|0.360|Límite conjunto aluminio, no ganancia/peso validado|
|PCB, drivers, GNSS, cables, fusible y protección|0.100|Objetivo pendiente de hardwarePCB, incluye conectores|
|TalentCell YB1203000-USB|0.190|Fabricante “about”, pesar unidad|
|**Subtotal condicionado**|**2.679**|No masa medida ni montaje aprobado|
|Reserva hasta3.000|**0.321**|Cables extra, desvíos, eventual adaptación motor y ampliación caja|

**Prioridad≤3kg aún no satisfecha físicamente**: el requisitoASA0.460 equivale
a53.4% del volumen sólido total y solo un informe de slicer con paredes/
refuerzos correctos dirá si es alcanzable sin debilitar; la estimación previa
75% daba0.646 kg. Si el slicer requiere0.646, subtotal sube2.865 y reserva
baja0.135. Motor21mm exige revisión mecánica; PCB footprint puede exceder
interior124×64 y exigir caja nueva, consumiendo reserva. No esconder estas
dependencias para presentar una opción ficticiamente aprobada.

Autonomía ilustrativa pack33.3Wh: con80% energía utilizable supuesta26.6Wh y
consumo total medido después de10/15/20W daría2.66/1.77/1.33h. No es duración
probada ni incluye radio. El tiempo activo real depende corriente motor,
drivers, WiFi/GNSS, frenado y pérdidas; no prometer jornada completa.
Alternativa de menosWh solo después de requisitoseléctricos y de seguridad,
con sus masas y límites de corriente publicados; no quitar batería del cómputo.

Regla de aceptación BuildLight: planos compatibles, ensayo de montaje/carga,
slicer≤límite, cada grupo pesado y total≤3.000kg **incluyendoPCB y batería**.
Si una puerta falla, volver a selección/diseño: no reclasificar este presupuesto
condicional como producto listo. No se han comprado motores/batería citados.

Diseño propio paramétrico, no reconstrucción de un producto comercial ni copia
de archivos/screenshot de terceros. **Prototipo no montado, no ensayado en carga
y antenas sin validación RF.** STL correcto no implica mecanismo funcional,
resistencia, ausencia de colisiones en todos los movimientos ni buen ROE.
El usuario eligió **CERN-OHL-S-2.0 para hardware original** y **MIT para software
original**, con alcance y textos en `NOTICE.md`/`LICENSES`. Las referencias
externas conservan sus propias licencias; no se redistribuyen aquí fuentes de
licencia desconocida. Esta entrega local no implica publicación remota.
Autoría y reconocimientos: consultar `AUTHORS.md`, `ACKNOWLEDGEMENTS.md` y `DISCLAIMER.md`
creados por el coordinador para AnatolEA5KAO, DiegoEA5JEF y PedroRocaMolina.
La iniciativa educativa [Bricohams](https://bricohams.org) no implica aval de
fabricantes ni de proyectos citados. Menores y adolescentes requieren
supervisión adulta; no transmitir sin autorización/licencia aplicable.
Antes de cargar firmware desconectar motores y RF, usar alimentación protegida
y verificar pinout; flashear un prototipo no certifica hardware aprobado.
Objetivo orientativo: **≤3 kg sin trípode ni radio**; no es masa medida.
La geometría completa muestra envolventes y piezas principales. Tornillos,
tuercas, cableado, trenzas, levas de finales, híbridos y revestimiento metálico
se instalan según esta guía, no son STL imprimibles.

## Archivos y uso independiente

* `cad\station.scad`: abrir en OpenSCAD; `part="assembly"` muestra conjunto.
* `cad\parameters.scad`: parámetros en mm/grados, ASA, holguras y frecuencias.
* `cad\gears.scad`: involutas reales calculadas, no dientes decorativos.
* `cad\mechanical.scad`: reductoras, soportes e interfaces.
* `cad\antenna.scad`: antenas diferentes para 145 y 435 MHz.
* `cad\export.ps1`: render CGAL de cada pieza y comprobación del STL.
* `tests\mechanical-math.cjs`: cálculos y muestreo de flancos; Node sin paquetes.
* `tests\mechanical-stl.cjs`: triángulos finitos, aristas cerradas orientadas,
  ausencia de triángulos degenerados y volumen orientado positivo.
* `bom\mechanical.csv`: cantidades base, materiales y presupuesto orientativo.

Selectores exportables: `sun1`, `sun2`, `planet`, `ring`, `carrier1`, `carrier2`,
`motor_plate`, `intermediate_plate`, `output_plate`, `keeper608`, `keeper6000`,
`spacer15`, `spacer9`, `spacer38`, `spacer6` (auxiliar), `tripod_base`,
`output_flange`, `elevation_bracket`, `saddle20`, `saddle25`, `saddle32`,
`flat_adapter`, `limit_bracket`, `magnet_holder`, `sensor_bracket`,
`radio_cradle`, `enclosure`, `enclosure_lid`, `diplexor_box`, `diplexor_lid`,
`antenna_hub`, `band_bridge`, `arm_socket`, `coupon`.
`gearbox`, `antenna145`, `antenna435`, `assembly` son vistas de montaje:
no imprimir su unión como una pieza. `assembly.csg` conserva el conjunto.
No se exporta un STL de conjunto que fusione piezas móviles en un sólido.

Se descargó OpenSCAD oficial **2021.01 Windows x64 ZIP** desde
<https://files.openscad.org/OpenSCAD-2021.01-x86-64.zip>, aislado en
`cad\tools`, sin instalación global. Para repetir:

```powershell
Set-Location 'C:\Users\anatol.lopez\Documents\PortableSatStation'
& '.\cad\export.ps1' -Node 'RUTA_LOCAL\node.exe'
& 'RUTA_LOCAL\node.exe' '.\tests\mechanical-math.cjs'
```

Puede proporcionar otro ejecutable oficial con `-OpenSCAD`. Los registros
individuales están en `cad\stl\*.render.log`. El Node usado durante creación
está en el directorio aislado de herramientas de la sesión; no es dependencia
del CAD ni se instala en el sistema.

## Reductora: dos etapas planetarias por eje

Elección inicial **recta**, no doble hélice: evita fuerzas axiales de fabricación,
facilita medir contacto y reduce tiempo/coste. Una herringbone puede reducir
empuje axial neto, pero **no elimina backlash**, flexión ni errores de impresión.
No se ofrece hélice sin verificar como opción supuestamente lista.

Módulo 1.5, presión 20°, sol **18**, planeta **27**, corona interna **72**,
tres planetas a 120°. Radio primitivo 13.5 / 20.25 / 54 mm; centros de planetas
a **33.75 mm**. Corona OD **124 mm** para pared de 6.125 mm detrás de raíces,
deliberadamente mayor que la envolvente aproximada de 114 mm de una pared fina.
Ancho útil engranes 12 mm; corona física 17 mm.

* `R=S+2P=72`, correcto engrane interno y externo.
* `(S+R)/3=30`, condición integral de montaje de tres planetas.
* Corona fija: `i=1+R/S=5`; dos etapas dan **25:1**.
* Mínimo teórico sin corrección de perfil `ceil(2/sin²20°)=18`;
  no se usa sol12 sin desplazamiento de perfil. No hay desplazamiento oculto.
* Cabeza externa `rp+m`, raíz `rp-m-0.25m`; corona cabeza `rp-m`,
  raíz `rp+m+0.25m`. Holgura radial nominal **0.375 mm**.
* Reducción de espesor por rueda `backlash/2=0.125 mm` en círculo primitivo:
  allowance tangencial total nominal **0.25 mm por pareja**, no juego de salida
  garantizado. Ensayar 0.20/0.25/0.30 tras cupón. Desgaste ASA aumenta juego.
* Corona: involuta **interna**, ensanchando diente hacia raíz exterior.
  Orientación fija de corona incluye fase 2.5° únicamente en dientes; taladros
  de atado permanecen a 30+60k grados. Sol fase0°, planetas
  `ángulo centro+180−180/27`. No cambiar fases de manera arbitraria.

### Apilado axial por reductora

Coordenadas locales referidas a cara del motor `z=0`. Separadores y apoyos
mantienen huecos reales; no apilar STL en el orden de la lista sin medir.

|Elemento|Intervalo z mm|Detalle|
|---|---:|---|
|Motor provisional|−34..0|Cara35 mm; dibujo del modelo definitivo manda|
|Placa motor|0..8|Paso26 provisional, M3, hueco central23|
|Cubo sol1 / dientes1|4..12 / 12..24|Eje motor5, inserto/tornillo M3 radial|
|Corona1 fija|9..26|Seis varillas M3|
|Planetas1 / hombros|12..24 / 10..33|OD6 ID4 L12 casquillos metálicos|
|Portaplanetas1 / cubo|26..32 / 32..40|2 mm a caras de dientes|
|Eje intermedio8|26..62|Acero; pasadores a z36 y58|
|Placa608 / rodamiento|41..50 / 42..49|Retenedor50..53; juego axial por calibrar|
|Cubo sol2 / dientes2|54..62 / 62..74|1 mm libre respecto retenedor|
|Corona2 fija|59..76|Separadores9 desde z50|
|Planetas2 / hombros|62..74 / 60..83|Arandelas y tuercas tras carrier|
|Portaplanetas2 / cubo|76..82 / 82..90|Salida acero10, pasador z86|
|Salida apoyo1|Placa91..101, 6000:92..100|Retenedor101..104|
|Salida apoyo2|Placa110..120, 6000:111..119|Retenedor120..123; centros separados19|
|Eje10|76..153|L77, pasadores z86/136/149|
|Brida de carga|124..142|Disco124..130, cubo130..142|
|Portaimán|145..157|Encaja sobre últimos8 mm de eje; pin z149|
|Soporte PCB|159..162|Distancia nominal imán2 mm; ajustar al PCB real|

Dos **6000 10×26×8** en salida por eje; **608 8×22×7** intermedio.
No llamar 608 a un rodamiento de eje10. Rodamientos apoyan aro exterior sobre
escalón de1 mm. Retenedores con ventana central id+1; usar arandelas de ajuste
solo sobre aro exterior para no frenar aro interior. No dependen de encaje
a presión en ASA. Los 12 planetas llevan **bronce 6×4×12**, hombro de acero4;
no se modela un ficticio rodamiento comercial de diámetro imposible.

El portaplanetas1 **arrastra físicamente sol2** por eje8 con dos pasadores M3.
Carrier2 y brida están unidos a eje10 mediante pasadores metálicos. Taladrar
ejes con plantilla perpendicular, desbarbar y ensayar fatiga: los agujeros
reducen sección, son puntos de inicio de grieta. Tornillos de paso M3 con
tuerca autoblocante, no rosca impresa ni adhesivo como única transmisión.
No transmitir carga importante solo mediante tornillo prisionero.

### Montaje y control de ajuste

1. Verificar plano NEMA14 seleccionado: 35 mm es clase nominal, no certificación
   de carcasa35, paso26, longitud34, eje5 ni par. Ajustar CAD antes de imprimir.
2. Imprimir cupón: agujeros8.0/8.1/8.2/8.3. Probar acero real; ajustar `fit`
   diametral0.25 inicial. Probar también asientos22/26, insertos, rod4 y M4.
3. Limpiar raíces, rebabas y puentes. Montar una sola pareja sol/planeta/corona.
   Verificar giro completo suave a mano, marcando contacto con tinta.
   Mantener lubricante compatible ASA fuera de conectores RF.
4. Instalar sol1 y motor. Montar 3 planetas con orientación anterior, casquillos,
   hombros, arandelas y carrier1. Ajustar juego axial **0.2–0.4 mm** medido.
   Los hombros deben apretar carrier, no bloquear planetas; longitudes de hombro
   comerciales pueden requerir arandelas/corte, no asumir tornillo normal.
5. Instalar eje8, placa608, separadores15, rodamiento y retenedor.
   Carrier/cubo acaba40; placa empieza41, no contacto de cubo con placa.
6. Montar sol2 desde54 y pin z58; corona2 desde59, segunda terna y carrier2.
7. Instalar separadores15, apoyo1, separadores9 y apoyo2. Alinear ambos6000 con
   eje provisional antes de apretar varillas, sin forzarlos con tornillos.
8. Instalar eje10, brida y pin z136, portaimán y pin z149. Montar AS5600
   coaxial en PCB elegido. Patrón16×16 es provisional. Pie del soporte sobre
   la segunda placa fija z120, dos M3 en x−55/y±10, torre a x−66..−62.
   Sujetar al **soporte estacionario del
   eje**, no al portaimán; ninguna carga de antena pasa por PCB/iman.
   Comprobar el grosor del PCB y soldaduras reales: la placa impresa no es
   electrónica. El sensor NO debe girar con brida/cuna/soporteEL sobre AZ:
   fijar su pie exclusivamente a carcasa de su propio eje.
9. Repetir para EL. Cara motor EL se atornilla a mejilla del soporte con seis
   M3; apertura38×38 libera motor real provisional35. Aliviar cables al entrar.
10. Base AZ queda z0..12; separadores38 elevan cara de reductora a50,
    dejando motor z16..50. Sin esta elevación motor chocaría con base/trípode.
    Varillas AZ aproximadamente180, EL130, cortar solo con apilado medido.
11. Brida AZ z174..192 soporta EL. SillaEL monta desde z130 local del ejeEL,
    hueco22 para encoder, boom desplazado lateralmente35 y a altura24. Sensor
    queda en plano159 libre sobre plástico (silla acaba154); incluso boom32
    queda fuera del puente sensor (placa acaba x12/y±12) durante EL0..90.
    EjeEL está84 mm por encima de su placa base: borde inferior de reductora
    libre sobre base y sobre puente sensorAZ. Atornillar cuatro posiciones
    ±15.556 mm (cuadrado31.112); comprobar luz de tornillos y sensor físicamente.
12. Montar cuatro NC, levas regulables metálicas y topes mecánicos independientes.
    Patrón bracket18 mm provisional; medir microinterruptor. Fijar a placas/base
    con tornillos, no pegamento. El CAD exporta soportes pero no una leva
    universal ficticia: fabricar leva según interruptor y margen de frenada.
    Medir accionamiento antes de **AZ±180 y EL0/90**; empezar con límites software
    ±170 y5..85. No permitir vuelta continua de AZ: coaxiales y cables se enrollan.

## Interfaces, portabilidad y radio

Antena completa desprendible por cuatro tornillos M4 a brida/silla; desconectar
coaxial de los híbridos antes de levantar. Booms RF20 de fibra vidrio y adaptador
estructural elegido20/25/32. Las sillas usan dos **U-bolts M5 metálicos**,
posiciones x±22, patas y=35±(diámetro/2+5), luz entre patas30/35/42 mm.
Elegir U-bolt real con esa luz y longitud útil ≥45 mm, placa metal de reparto,
arandelas grandes y tuercas autoblocantes; no apretar hasta aplastar tubo.
Para cara plana usar `flat_adapter`, M4 en patrón común y cuatro M5
en54×36, siempre pasantes metal. No imprimir abrazaderas roscadas para carga.

Trípode: tuerca **1/4-20 UNC metálica capturada** (AF11.1 alto5.6 inicial),
accesible desmontando base, más adaptador **3/8-16 a1/4-20 metálico comercial**.
No hay roscas UNC impresas. Comprobar longitud de tornillo: no hacer fondo,
repartir presión, añadir retenedor metal a tuerca y cuerda de seguridad al
trípode. Esta base no certifica estabilidad/cabezal ni su capacidad lateral.
En viento/terreno irregular asegurar patas, lastre y zona sin personas debajo.

RT3S permanece en **base/bandeja FIJA al trípode**, no en brida AZ/antena.
Envolvente inicial61×39×131 mm más2 mm de holgura por lado: **provisional, medir
unidad del usuario** incluyendo clips, botón PTT, conectores y batería.
La cuna no valida estanqueidad ni ajuste; probar manualmente antes de usar,
dos correas por ranuras y tercera cuerda de seguridad. No bloquear disipación,
altavoz ni mandos. Radio extraíble sin desmontar antena.

Las cajas mostradas junto a base necesitan **bandeja metálica fija** al trípode;
no se propone dejarlas suspendidas en el aire ni colgarlas de antena.
Caja diplexor independiente80×70×35 y tapa desmontables con M3.
Cambiar medidas y aperturas al diplexor/conectores elegidos. ASA **no apantalla
RF**: revestir paredes/fondo interior74×64×32 y tapa con chapa aluminio
0.3 mm, juntas conductoras, tornillos/puntos metal-metal y conexión de masas
RF según equipo. Evitar rebabas/cortos con separadores aislantes. No se promete
EMC, hermeticidad ni blindaje con pintura plástica. Electrónica130×70×45 con
tapa, pasacables y bucles antigoteo; no energizar bajo lluvia.

Referencia opcional de envolvente: proyecto público `DuplexorSpaceQuad`,
commit `f5c7dc375ed7b9882f52bd7757deaf44cd422b81`, publica PCB SMA37×23 mm,
caja45.2×27.6×14.1 mm (Amphenol132289, dos M2×10), o PCB BNC55.5×33 mm,
caja59.9×37.6×23.5 mm (AmphenolB6252HB-NPP3G-50, dos M2×12). Son datos
publicados, **no mediciones de nuestra unidad**. Ambas envolventes caben
nominalmente dentro74×64×32 de nuestro compartimento, pero no prueban espacio
para los tres conectores, enchufes, tuercas, coaxiales ni radio de curvatura.
Las aperturas genéricas10 mm del CAD **no son plantillas SMA/BNC**: modificar
tras medir conectores reales o llevar cable a pasacables.

Ese proyecto declara dimensiones de conectores estimadas de footprints:
SMA pestaña9.6×1.9, eje PCB+0.4, abertura6.8 mm; BNC cuerpo14.8 sobre PCB,
eje PCB+7.5, abertura14.9 mm. Verificar con calibre antes de taladrar/fijar;
no cargar la placa mediante conectores aproximados. Sus paredes/fondo/techo
2/2/1.6 mm y tolerancia0.15 no sustituyen calibración de nuestro ASA.
Es un **diplexor de tres puertos**, no híbrido de cuadratura; seguir necesitando
dos redes90° separadas para dipolos cruzados. Simulaciones ideales y una
indicación5–10 W para0805 no certifican potencia, pérdidas, compatibilidad
o temperatura reales. No se reutilizan aquí sus archivos CAD ni circuito.

## Antena original: dos conjuntos cruzados con reflector

No se escala un diseño449 MHz para anunciar dual banda. Cada banda tiene dos
dipolos ortogonales con dos elementos reflectores ortogonales, geometría propia
calculada inicialmente por:

```
lambda_mm = 299792.458 / f_MHz
driven_tip_to_tip = lambda_mm / 2 * 0.92
reflector_tip_to_tip = driven_tip_to_tip * 1.05
separation = 0.225 * lambda_mm
```

|Banda|λ mm|Dipolo extremo-extremo|Reflector extremo-extremo|Distancia planos|
|---|---:|---:|---:|---:|
|145 MHz|2067.53|951.07|998.62|465.20|
|435 MHz|689.18|317.02|332.87|155.07|

Estas medidas son **estimaciones de inicio**, no simulación o medida de ganancia,
patrón, ROE, polarización ni adaptación. Influencia de bisagras, trenzas, booms,
reflector, caja/radio y **acoplamiento mutuo VHF/UHF** sin validar. Distancia
lateral ilustrativa80 mm entre booms no es separación RF comprobada.
Balance mecánico por desplazamiento de booms no certifica patrón RF.
Un puente impreso con tres agujeros20 une ambos booms RF y un boom estructural
central175 mm. Pernos M4 pasantes con arandelas grandes y collarines metálicos;
no depender de rosca ASA. Puente a50 mm del plano de balance longitudinal para
no ocupar la misma sección que silla; centros de ambos conjuntos coinciden
longitudinalmente, pero masas desiguales requieren balance real. Diámetros25/32
son alternativas de boom estructural/silla; booms RF y puente siguen20, usar
casquillo adaptador metálico/dieléctrico al cambiar estructura.

### Corte, bisagras y secciones transportables

Diámetro rod4 mm provisional. Hueco central24 mm incluido en extremo-extremo:
cada brazo geométrico es `L/2−12`, ≈463.53 mm VHF excitado y487.31 reflector.
La bisagra M4 está a radio36: stub conductor fijo r12..28 (**16 mm**),
brazo conductor distal desde r46; hueco de articulación18 mm se salva mediante
**trenza cobre flexible**. Su longitud eléctrica real modifica fórmula:
mantener todas las trenzas idénticas y ajustar en VNA; no afirmar que el
hueco ASA es conductor. Pivote de acero M4 y M3 transversal a radio42 bloquean
positivamente desplegado. Tornillo M3 en r54 retiene varilla mediante insertos
y manguito metal, no rosca ASA. No usar fricción como único seguro.

|Pieza metal|Cantidad|Longitud geométrica nominal mm|Corte inicial largo sugerido|
|---|---:|---:|---:|
|Stubs r12..28, ambas bandas|16|16|16, no recortar para sintonía|
|VHF distal excitado|4 brazos, cada uno dos segmentos|429.53 =214.77+214.77|2×220 por brazo|
|VHF distal reflector|4 brazos, cada uno dos segmentos|453.31 =226.65+226.65|2×232 por brazo|
|UHF distal excitado|4|112.51|118 cada uno|
|UHF distal reflector|4|120.44|126 cada uno|
|Manguito unión VHF|8|50, OD8 ID4|Ajustar ID al metal real|
|Boom VHF dieléctrico|2 segmentos|~245 cada uno|Mide plano a plano465.20 al ensamblar|
|Boom UHF dieléctrico|1|~180|Plano a plano155.07|

Manguitos **conductores** de latón/aluminio: empalme **a tope** (no restar50 de
longitudes), inserción25 por lado, dos pasadores/tornillos metálicos positivos
de2 mm perpendiculares, aluminio limpio y compuesto antioxidante compatible.
No perforar rod4 con M3 sin revisar resistencia. Se usan pasadores pequeños
para los manguitos RF, distintos de pasadores M3 en los ejes reductores.
La ubicación de manguito en vista es envolvente ilustrativa; colocarlo en
la junta real de las dos mitades. Retirar segmentos exteriores y separar boom
VHF; ninguna sección de metal/boom supera450 mm. Ensamblar con topes de longitud,
marcas de orientación, antirotación y seguro; una unión telescópica libre no
mantiene resonancia ni continuidad. En transporte plegar bisagras y atar brazos;
la vista `antenna_arm_angle=90` es cinemática ilustrativa, no validación de
interferencia de todas las trenzas/manguitos.

Elementos reflectores deben ser continuos eléctricamente: unir sus mitades
opuestas mediante **puentes metálicos alrededor del boom**, fuera del cruce,
manteniendo dos ejes a alturas distintas si se cruzan. No puentear los dos
terminales del dipolo excitado ni unirlos al boom. Brazos y reflector desmontan
independientemente por cubos/bisagras; anotar secuencia y no perder bloqueo.

La alimentación **50 Ω adaptada** no sale de imprimir un cubo. Instalar por
banda match/balun apropiado para cada dipolo y un híbrido externo90° con cables
iguales para polarización elegida; invertir fase para circular opuesta solo
tras comprobación. Dos redes **separadas**, luego diplexor real145/435 compatible
con potencia/pérdidas. No conectar directamente dos dipolos en paralelo creyendo
obtener50 Ω ni atribuir50 Ω a esta geometría. RF metal únicamente, sin hilos
impresos. Afinar con VNA a baja potencia, primero cada banda aislada y luego
combinada sobre estación real. Recortar simétricamente por pequeños incrementos.
Respetar licencias y exposición RF; mantener personas alejadas de varillas,
antena energizada y partes móviles.

Los criterios RF numéricos del proyecto en `docs\ACCEPTANCE.md` son objetivos
de cribado, no prestaciones demostradas: ROE≤1.5 al centro/≤2 en canales,
desbalance de híbrido≤0.5 dB y fase90°±5°, diplexor pérdida≤1 dB,
return loss≥14 dB y aislamiento≥40 dB. Incluso cumplirlos no demuestra
seguridad de recepción durante transmisión ni autoriza operación full-duplex
sin evaluación del receptor, potencia y cadena RF completa.

Referencia de componente: la ficha de fabricante actual **Mini-Circuits QCN-3+**
indica220–470 MHz:435 está dentro,145 **fuera**. No tratarlo como híbrido
dual banda ni extrapolar a la referencia sin sufijo `QCN-3`, cuya identidad
no queda confirmada. No se seleccionan modelos CMX/Anaren sin ficha verificable.

Las referencias externas tampoco sustituyen ensayos de esta estación:
LibreSat declara su v1.0 no construido/medido como conjunto y utiliza
NEMA17/cicloidal25:1, no nuestro NEMA14/planetario. Sus hipótesis de carga,
viento y eficiencia no son ratings transferibles. La guía oficial mantenida
LibreDMR/OpenGD77 confirma pantalla satélite RT3S con Doppler TX/RX,
azimut/elevación, ubicación/UTC manual y Keplerianos desde CPS; eso no demuestra
CAT ni full-duplex. Nuestra cuna sigue pendiente de medición física.

## Carga, par, viento y masa: objetivos, no capacidad certificada

Objetivo inicial antena **500 g máximo**, CG a **≤30 mm** de ejeEL medido con
antena completa/coaxiales y booms ajustados. Torque gravitatorio:
`0.5×9.81×0.03 = 0.147 Nm`. La ilustración coloca boom aproximadamente al
centro, pero hay que balancear físicamente; reducir momento moviendo silla,
contrapeso moderado o accesorios fuera de antena. La masa de toda reductoraEL
añade inercia AZ. No elevar antena pesada porque el motor tenga holding torque.

Ejemplo, **no dato de motor vendido**: NEMA14 torque dinámico asumido0.08 Nm,
eficiencia0.65 por etapa: `0.08×25×0.65²=0.845 Nm` salida teórica.
Comprobar curva real versus velocidad/corriente, pérdidas, temperatura y
rigidez ASA. No presupone que holding torque sea torque dinámico.
Hasta ensayos limitar demanda a **0.5 Nm por eje** y con factor de margen;
no es rating probado del mecanismo ni de los dientes/pines.

Viento conservador de ejemplo: densidad1.225 kg/m³, Cd1.3, área equivalente
0.12 m², brazo0.15 m, viento8 m/s:
`T = 0.5*rho*Cd*A*v²*brazo = 0.917 Nm`, más gravedad0.147 = **1.064 Nm**:
**excede** tanto cap0.5 como ejemplo0.845. No usar esa ráfaga como admisible.
A5 m/s da0.358+0.147≈0.505 Nm, ya marginal. Probar inicialmente en interior/
calma, plegar y desmontar al crecer viento; tripode/cables añaden torque.
No garantizar uso a5 m/s ni3 kg. Nunca dejar activo sin vigilancia.

Presupuesto CSV son rangos de planificación **por línea total**, no precios de
tienda/cotizaciones. Pxx sin coste separado porque filamento se cuenta M24.
No duplicar alternativas de silla/plano ni contar componentes electrónicos que
estén en otro BOM. Masa de plástico se estima por volumen STL sólido y densidad
ASA~1.07 g/cm³; infill cambia resultado, metal/refuerzos/coaxial aumentan masa.
Medir cada pieza ensamblada; si supera3 kg, el objetivo ha fallado.

### Validación realizada, 10 octubre 2026

* OpenSCAD2021.01 renderizó **34 selectores STL individuales** por CGAL,
  sin ERROR/WARNING en sus34 registros; conjunto generado como CSG.
* Los34 STL pasaron prueba de aristas cerradas con orientación consistente,
  triángulos no degenerados y volumen positivo. Esto no es certificación de
  contacto/colisión física ni un análisis exhaustivo de autointersección.
* Node22.16 validó relación25:1, cierre30, mínimo18 dientes, holguras radiales
  y121 posiciones de una vuelta de diente del sol: muestras de contorno del
  planeta no invaden sol ni material de corona. Una terna es equivalente por
  simetría. Contact ratio ideal recto: externo1.580 e interno1.944.
  Se comprobaron también cotas motor/base, ejeEL/base y puente de encoder
  versus boom32 en el cuadrante permitido. No es barrido completo ensamblado.
* Inventario nominal **131 piezas impresas**, sin sumar adaptador plano
  alternativo. Volumen sólido equivalente tras optimización: **2.521 kg de ASA**
  a1.07 g/cm³. **Imprimir todo macizo superaría objetivo3 kg al añadir metal,
  motores y coaxiales.** Infill/refuerzos y masa real necesitan revisión
  antes de afirmar que el conjunto es ligero; no se calculó masa de infill.
* Rango de planificación mecánica/RF del CSV: **248–671 €**, no cotizaciones,
  excluye radio/trípode y electrónica de control de otro BOM.

No se ha impreso, montado, medido viento/par/masa ni probado adaptación RF.
Las raíces externas usan transición radial discretizada hasta círculo base,
no una trocoide generada por herramienta de tallado; flancos activos son
involutas reales. No atribuir a esos dientes un rating ISO/AGMA de fatiga.

### Optimización acotada y presupuesto de masa

Se vaciaron campos inferiores de base manteniendo piel superior3 mm, perímetro,
boss central de tuerca y seis nervios14 mm hacia varillas. Se aligeraron
únicamente caras interiores de tapas manteniendo techo1.6 mm, bordes y nervio
central. No se tocaron involutas/raíces, carriers, ejes, asientos de rodamientos,
mejillaEL ni fijaciones de motor. Estos nervios son geometría conservada,
**no resistencia calculada o ensayada**; verificar base tras aligeramiento.

|STL|Volumen previo mm³|Volumen nuevo mm³|
|---|---:|---:|
|tripod_base|233270.3|130922.3|
|enclosure_lid|27191.2|20331.2|
|diplexor_lid|16691.2|13331.2|

Ahorro nominal sólido ASA **120.45 g**, conjunto plástico2.641→2.521 kg.
Tres STL re-renderizados CGAL y comprobados; los34 mallas finales se validan
de nuevo por inventario. Runner `tests\mechanical.test.cjs`: tres validaciones
aprobadas (matemática, inventario y optimización/masas), incluidas dos pruebas
unitarias de optimización. `export.ps1 -Only tripod_base,enclosure_lid,diplexor_lid`
permite regenerar un subconjunto sin omitir la validación de cada STL.

El subconjunto engranes+carriers sólido pesa0.579 kg nominal; resto1.942 kg.
**Ejemplo de sensibilidad**, NO resultado de slicer: conservar100% de engranes/
carriers y60% del volumen sólido del resto daría1.744 kg ASA. Ese60% es fracción
material global hipotética, **no ajuste de infill60%**: paredes/nervios/skins
alteran mucho el resultado. No garantizar esa masa ni reducir soportes de carga
para cumplir una cifra. Usar informe real del slicer, incluidos soportes/brim.

|Grupo adicional|Masa de planificación kg|
|---|---:|
|Dos NEMA14 seleccionados posteriormente|0.24–0.40|
|Dos608 y cuatro6000|0.09–0.12|
|Ejes acero8×36 y10×77, dos de cada|0.1234 nominal geométrico|
|12 varillasM3, seis180 y seis130|0.1032 nominal geométrico|
|12 hombros acero4×23, sin cabezas/tuercas|0.0272 nominal geométrico|
|Casquillos/pasadores/tornillería/U-bolts/adaptador|0.12–0.22|
|Varillas RF y manguitos **aluminio**, booms fibra|0.25–0.40|
|Coaxial/redes90°/diplexor/liner|0.18–0.30|
|Controlador/drivers/cableado|0.08–0.15|
|Alimentación portátil/batería|0.25–0.45|
|Subtotal sin ASA, radio ni trípode|**1.464–2.294**|

Motor/rodamiento/radio/batería reales necesitan ficha/pesaje. Valores de acero
calculados con densidad7.85 g/cm³; no incluyen corte de agujeros y cabezas,
que se reservan en tornillería. Usar cobre/latón en vez de aluminio puede
aumentar considerablemente masa RF. Bandeja/refuerzos/correas pueden aumentar
reserva; ningún rango es peso de proveedor inventado.

Incluso el escenario de impresión hipotético1.744 kg produce **3.208–4.038 kg**
total; macizo daría **3.985–4.815 kg**. **Objetivo ≤3 kg NO logrado ni demostrado
por este diseño robusto124 mm** con alimentación incluida. No anunciarlo como
estación de3 kg. Para perseguirlo hace falta una nueva decisión física
(mecanizado/placas metálicas optimizadas, alimentación externa no transportada,
arquitectura más pequeña o revisión estructural ensayada); no adelgazar dientes
o apoyos especulativamente. Las antenas completas también deben pesarse:
target500 g puede incumplirse con trenzas/coaxial/herrajes pesados.

### Estado de integración mecánica

La cadena de par y cotas de motor/shafts/bearings están definidas y renderizadas.
Paso NEMA14 **26 mm provisional** y eje5 solo se aceptan tras plano del motor
comprado. No hay garantía universal de montaje NEMA14. CSG completo no es
ensamblaje final verificado: faltan geometrías específicas de levas/topes,
cabezas/tuercas/arandelas, sujeción definitiva del diplexor/cables y sus barridos.
La alineación coaxial, pasadores, juegos axiales, PCB real y cableado exigen
montaje de banco. Las pruebas de cotas son comprobaciones parciales explícitas,
**no ausencia de todas las colisiones**. Clasificación final: prototipo CAD
modular reproducible, no estación lista para operar ni assembly-tested.

## Impresión ASA, fallos y aceptación

Orientar engranes ejeZ, capas0.15–0.20 mm, ≥5 perímetros, dientes/cubos100%
relleno local; piezas grandes30–45% y nervios con ≥5 perímetros inicialmente.
No rebajar perímetros de coronas alrededor de tornillos. Placas planas en cama,
brim si hace falta. Soporte EL y bisagras soportan flexión: considerar imprimir
de canto o refuerzo metálico y ensayar anisotropía. Escariar solo taladros,
no limar involutas para esconder desalineación. Rodamientos no montan calientes.
Ajustar tolerancias con material/lote/impresora reales, no una escala global.

ASA genera emisiones: recinto y extracción/ventilación adecuada según fabricante,
evitar inhalación y espacios habitados; no prometer que un recinto sellado
sin extracción protege. Cama/hotend calientes, guantes al manipular metal,
protección ocular al taladrar/cortar. ASA resiste intemperie mejor que PLA,
pero puede sufrir creep al sol/carga y no certifica estabilidad térmica.

Rechazar: grietas en raíces, tuercas que aplastan ASA, pines doblados,
casquillos ovalados, retenedor rozando eje, bloqueo de planetas, ranuras de
bisagra agrandadas, pasador perdido, coaxial tenso, juego creciente o imán flojo.
Medir backlash ida/vuelta en salida con comparador, no extrapolar pasos de
motor. Confirmar AS5600 sobre eje de salida durante pérdida de pasos.
Un final NC desconectado debe detener; probar cable abierto y emergencia con
motor desconectado primero. Topes mecánicos no sustituyen corte eléctrico.

Aceptación pendiente antes de campo: ciclo manual completo, comprobación
colisiones/cables ±180 y0..90, 100 ciclos sin carga, 100 con carga creciente,
medición par/corriente/temperatura/backlash, caída de alimentación, finales NC,
estabilidad trípode, retención de antena e imanes, masa real, ROE/patrón/exposición
RF y continuidad tras repetidos plegados. No se han realizado estas pruebas.
