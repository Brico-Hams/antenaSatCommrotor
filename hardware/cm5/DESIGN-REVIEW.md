# CM5 Guard A — segundo paso: diseño conectado y rutado de revisión

2026-10-10. **NO FABRICABLE / NO OPERAR / SIN VALIDACIÓN FÍSICA.**
Esta entrega sustituye el borrador sin rutear del primer paso. Mantiene el mapa
software `interface.json` revisión A sin modificarlo. No modifica README,
ARCHITECTURE ni REQUIREMENTS. No es una portadora CM5: usa CM5IO rev2 por GPIO.

## Resultado digital comprobado

KiCad aislado **10.0.7**, esquema de 160 componentes (158 huellas físicas),
PCB 2 capas, espesor nominal 1,6 mm, contorno **290 x 280 mm** provisional:

- **ERC 0** (todos los niveles de severidad habilitados).
- **DRC 0**, **0 conexiones pendientes**, **0 diferencias esquema/PCB**;
  `--all-track-errors --severity-all --schematic-parity --refill-zones --save-board`.
- **377 aserciones** de contrato, netlist, geometría, DNP y BOM/CPL.
- Modelo booleano exhaustivo: **8192 estados**, más secuencia fault/recovery/POR.
  Verifica lógica ideal ligada a nets reales, NO SPICE, temporización ni banco.
- **1952 segmentos, 178 vías y 2 zonas RF** (ver `routing-metrics.json`).
- **97 componentes SMT / 17 grupos BOM** en CSV JLCPCB de revisión.

No se excluyó ninguna infracción individual. Se mantuvieron checks opcionales
inactivos de la configuración inicial de KiCad; no se debe llamar esto
“absolutamente todos los checks habilitados”. ERC: single_global_label,
four_way_junction, simulation_model_issue, footprint_filter. DRC:
missing_courtyard, track_not_centered_on_via, tuning_profile_track_geometries,
footprint_filters_mismatch, footprint_type_mismatch. Los informes JSON enumeran
los checks activos/inactivos y severidades. No se obtiene aprobación física
mediante un ERC/DRC limpio.

## Archivos y reproducción

- `cm5-guard-A.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, `sym-lib-table`,
  `fp-lib-table`, `Guard.kicad_sym`, `Guard.pretty\WE744824622.kicad_mod`.
- `design\component-register.csv`: cada referencia/valor/MPN/huella/DNP.
- `reports\erc.json`, `drc.json`, `contract-tests.json`, `routing-metrics.json`,
  `validation-summary.json`, `commands.json`, `manifest-sha256.json`, PDF.
- `fabrication\NOT_FOR_MANUFACTURE\gerber`: cobre realmente rutado, máscaras,
  pasta, serigrafías, contorno y taladros Excellon PTH/NPTH/mapas.
- `JLCPCB-BOM-REVIEW.csv`, `JLCPCB-CPL-REVIEW.csv`, posiciones KiCad originales.

Ejecutar `design\validate-export.ps1 -KiCadRoot <ruta KiCad10.0.7>` vuelve a
validar/exportar **la PCB rutada existente**, sin destruir sus rutas.
`-RebuildAndRoute` regenera y usa Freerouting1.9.0/JRE17 **locales**, `-da`
deshabilita analytics; nunca se envía netlist a un servicio de ruteo remoto.
La regeneración completa se ejecutó de nuevo y pasó ERC/DRC/paridad y exportación.
design\finish_missing.py aplica un fallback local acotado de rutas de señal
a rejilla0,15mm (no rutas de potencia/RF), siempre sometido a DRC estricto.
El número de segmentos puede variar entre ejecuciones del autorouter.
Freerouting consulta disponibilidad de nueva versión (no se presenta como
software offline estricto). La ruta regenerada requiere de nuevo DRC0; cualquier
exitCode no cero detiene el procedimiento. Los archivos DSN/SES se conservan
en `design\routing` como evidencia local; no tienen autoridad sobre KiCad DRC.

## Decisiones y pendientes por bloque

### Host, sensores y GNSS

J1 conecta los 26 GPIO exactamente al JSON A. VIO **3,3 V**, no 1,8 V; pines
1/2/4/17 de potencia NC. El host NO alimenta dos LimeSDR por esta placa. Su
consumo, USB3/audio, fonte PD y refrigeración son externos. J2 toma **5 V de
un convertidor aislado externo**, AP2112K-3.3TRG1 regula 3,3 V; no convierte
12 V ni aporta aislamiento. J2 DNP hasta cualificar arnés/convertidor.
MCP23017-E/SO 0x20 (A0/A1/A2 GND), GPA0..7 conforme contrato, GPB reservado NC.
TCA9548APWR 0x70: canales0/1/2 a AS5600 externos PID6357 0x36; canal3 LIS3MDL,
canal4 LSM6DSOX (SD4/SC4 pines13/14; pin12 GND). Conectores JST-PH candidatos
NO equivalen a STEMMA/QT: necesitan arnés de pinout comprobado. Pullups4,7k
por canal/bus deben ajustarse con pullups breakout y capacitancia de cable.
GNSS PID746 J8: GND,3V3,RX_CM5<-TX_GNSS,TX_CM5->RX_GNSS,PPS27. Alimentación,
UART/PPS, orientaciones, ESD, overlays y secuencias de alimentación pendientes.
No afirmar inmunidad al backpower del GPIO con host/guard apagados parcialmente.

### Seis NC, watchdog, E-stop y rearme manual

Cada final NC a GND usa pullup10k y 100nF, Schmitt SN74HC14. Abierto/cable roto
= fault; corto a GND **no detectado**. NAND8 SN74HC30 produce SAFE_OK con seis
healthy, auxiliar E-stop y WATCHDOG_OK. Un fallo inhibe **todos** los EN y PTT:
política global conservadora, no parada direccional. Símbolos LS30/LS08 son
sólo dibujo/pinout de biblioteca; MPN son **HC CMOS3,3V**, NO montar TTL LS.

Watchdog SN74HC123DR: A=GND,B=BCM11,CLR=POR,Q pin13,Cext14/RCext15,
R1M/C1u. Timeout ~450ms **estimación no cualificada**, requiere factor real,
fugas/capacitancia DC-bias/temperatura y pruebas. Segundo canal inhibido.
POR RC/Schmitt es candidato, **no supervisor brownout certificado**.

**Nuevo U12/U13/U14**: botón NO local J40, pulldown10k,100nF y doble Schmitt;
D flip-flop SN74HC74 con clear asíncrono `SAFE_OK AND LOGIC_RESET_N`.
D=`NOT(arm OR PTT_VHF OR PTT_UHF)`; clock=flanco del botón; PRE=3V3.
Q=`REARMED`; permiso=`SAFE_OK AND REARMED`. Para rearmar: todo sano,
arm/PTT bajos, **nuevo flanco manual**. Recuperar NC/heartbeat o POR no pone Q
alto por sí solo; botón mantenido antes del fallo no crea otro flanco ideal.
Arm baja bloquea los tres motores aunque expander conserve solicitudes altas.
Pérdida de lógica, rebotes, pulsos mínimos, metastabilidad/races y botón
averiado necesitan prueba física. No SIL/PL ni redundancia/certificación.

Q1..3 2N7002 tiran EN a GND únicamente con permiso y request correspondiente;
pullup EN10k y pulldowns solicitudes/gates. EN inhibe bobinas, **no frena ni
retiene eje cargado**. Añadir/verificar retención/freno de gravedad, inercia y
stop distance. E-stop **principal DC-rated externo** debe cortar VMOT entre
salida J42 y retorno J28. Auxiliar NC J15 no conduce potencia. Corte/contactor
normalmente abierto y fail-off en falta de VIO siguen sin seleccionar/probar.

### Geometría y conexiones de tres TMC5160

Watterott v1.5 fuente fijada commit098b7518…: placa15,24x20,32mm,
columnas **12,70mm**, pitch2,54mm. Pares J16/J17,J19/J20,J22/J23 tienen esa
separación y pin1 alineado; no componentes debajo. Contornos Dwgs.User
orientativos. Datos extraídos en `source-evidence\module-geometry.json`.
Original Eagle numera pads top-to-bottom8..1; guard sockets numera1..8.
**No confundir números: comparar net y vista superior**.
Izquierda EN,SDI,SCK,CS,SDO,DCO,STEP,DIR; derecha VM,GND,M2B,M2A,M1A,M1B,VIO,GND.
DCO NC, no FAULT/nSLEEP. FAULT BCM24/25/26 sigue sólo a entrada externa
contacto/OD aislado J25..27, diagnóstico TMC real no está diseñado.
SPI1 tres CS pullup10k; STEP/DIR GND. CLK GND, SPI_MODE VIO y SD_MODE jumper
abierto necesitan straps en módulo **no implementados por esos sockets**.
Reloj/rampas/corriente/torque/calor/fit/socket y VMOT adecuados sin comprobar.

GND de ambos pads módulo se declara GND_MOTOR; **NT1 net-tie 2mm** lo referencia
a GND_LOGIC en punto explícito. Módulos no aíslan SPI/retorno. Verificar caminos
reales, unión paralela interna del módulo, corrientes/sensor/audio y unión
externa del convertidor; no atribuir aislamiento de estación a un convertidor.

### Potencia: implementación CAD, NO etapa cualificada

Powerpole PP15/30/45 se conserva como **pigtail externo**, como exige CM5-PCB;
no footprint ficticio de housing/contacto. J41 candidato terminal Phoenix
MKDS3/2/5,08 1711725, tras fusible próximo al pack y desconexión externa.
**F1 + F2..F6** portafusibles ATO candidatos Littelfuse178.6165.0001:
principal y ramas lógica/motor/CM5IO/VHF-PA/UHF-PA. **Sin inserts**: amperajes,
DC interrupt, time-current e inrush NO elegidos. Todos DNP, no puentes/jumpers
que eludan protección. Exactitud suffix/holder/DC/contact/cable por validar.

Q7 AOD4185 PMOS-40V candidato, drain BAT_FUSED/source BAT_PROTECTED, zener12V
BZT52C12 gate-source, gate RC100k/100n DNP. D2 SMBJ18A DNP tras fusible.
No demostrar rating/battery normal range/clamp/protección de carga/SOA con
esto: **inrush control de RC no es limitador de corriente cualificado**,
MOSFET/TVS/transitorios/inversión/arranque pendientes. Pack nominal12V no
establece máximo14,6V; ninguna corriente de estación inferida.

Rama lógica F2: **L1 WE744824622**2,2mH,6A a70°C,20mΩ max, fabricante rev008:
dos devanados1-4 y2-3. Positivo F2->1->4 y retorno GND_MOTOR->2->3;
**ambos conductores** cruzan CMC. No bead300mA en rama5A. Huella original
`Guard.pretty` derivada del datasheet: agujeros1,3mm, patrón10x12mm; library
WE-CMB-L genérica tenía numbering/pitch incompatibles y **no se usa**.
Candidato damping serie R80=1Ω2W + C80=47u50V, no LC diferencial ideal.
J46 salida primaria EMI al **convertidor aislado5V externo aún sin elegir**,
salida secundaria por J2. Pendiente estabilidad/impedancia real/cables/ESR/
inrush/noise/DC-bias/saturación y temperatura. CMC/DC input no prueba desense.

J42 motor hacia corte E-stop externo, J43 convertidor CM5IO PD externo,
J44/45 PA externos. Todos DNP. Ruteo DC trunks2mm, motor coils1mm,
supply0,4mm y señal0,2mm; hay **neckdowns** BAT_PROTECTED por RC/semiconductores
y **vías0,6/0,3mm no cualificadas para corriente**. Widths exactos en metrics;
**2mm no establece amperaje seguro**. Sin presupuesto de corriente/temp/cobre
ni contactos/pistas/vías/inrush medidos, no energizar. Falta optimización real
loops alta-di/dt, decoupling a pie de pin y separación por criterio EMI,
aunque CAD sea conectado. El floorplan sigue grande/provisional.

R52 y C16 son el RC de puerta de potencia y quedan DNP. C21 es bypass de
lógica3,3V y sigue poblado: pruebas netlist/DNP comprueban ambas identidades.

### SMA físicos y USB-C/PTT

J36/J37 Amphenol132134 VHF y J38/J39 UHF: cuatro **SMA hembra convencionales**,
pasivos feed-through **dos circuitos separados**, nunca unir SDR TX y RX.
Traza central2,9mm y launches1mm; retornos shield B.Cu y dos planos locales
independientes de motor/lógica. FR4 nominal1,6mm no congela stackup/epsilon/
impedancia: **50Ω no validado**; launch discontinuities, conector/body/
retorno, VNA/insertion-loss/ROE/PA-power/desense y145x3=435MHz pendientes.
No PA/filter/diplexor/RHCP-LHCP diseñado ni dirección RF funcional atribuida.
Los dos feed-throughs NO proporcionan por sí solos cuatro rutas TX/RX SDR.

USB-C J34 USB4105-GF-A y J35 **DNP device USB2**, CC5,1k; VBUS/return/shield
separados de batería/lógica. **No PD source5A**, no USB3 ni codec/hub/audio.
No USB2 diferencial90Ω/ESD/host topology cualificado; ruteo digital de nets
no certifica enlace. CM5IO utiliza su fuente PD externa y USB3 nativos.

PTT VHF/UHF gate rearme+SAFE_OK+request,2N7002+LTV-817S con1k LED;
colector/emisor flotante, nominal~2mA estimado. CTR/carga/tensión/fugas/
transitorios/polaridad/creepage no cualificados. Feedback PTT externos
J32/J33, fallos PA J29, motor feedback lógico invertidoQ6: **no confirman RF,
contactores ni corriente motor**. Aislamiento de opto no certifica creepage
ni separación física del ruteo. No PA, no TX antes de pruebas independientes.

## Reglas DRC y PCBA

Se cambiaron reglas generales0,25mm a **0,18mm copper**, hole-to-hole0,15mm,
track mínimo0,15mm,edge0,5mm para geometría fina USB/TSSOP. No se redujo
clearance a0/no se excluyeron shorts. Autorouter tuvo clearanceSMD0,18mm
explícito; clases localDSN DC0,35mm/motor0,25mm. No estos mínimos para alta
energía/aislamiento: revisar con fabricante/cobre/voltaje/ensamblaje real.

BOM/CPL SMT extraídos de PCB/netlist final; Comment/Designator/Footprint/
Quantity/Manufacturer Part, MidX/MidY(mm)/Top/Rotation. DNP/THT/net-tie fuera
de CSV SMT; todos registrados individualmente, montaje manual de terminal/
sockets/SMA **aún no cualificado**. Sin códigos LCSC inventados ni precios.
PreviewJLC, orientación/centro/pin1/stock/revisión de huella/cotización
pendientes. **No upload/pedido autorizado**, aunque Gerber sea conectado.

## Fuentes y gate de cierre

`docs\CM5-PCB.md`, `CM5-RF-SELECTION.md`, `REQUIREMENTS.md` y contrato JSON A.
Geometría módulo de fuente oficial fijada y facts JSON; pinout
https://learn.watterott.com/silentstepstick/pinconfig/tmc5160/.
CMC datasheet leído/renderizado conservado:
https://www.we-online.com/components/products/datasheet/744824622.pdf.
Símbolos/huellas KiCad10.0.7 verifican pinout CAD, NO hoja de datos eléctrica
completa de cada MPN. Phoenix página oficial403, no declarar primary part
qualification. Datasheet TRACO tec3wi inaccesible403; **no converter elegido**.

Antes de fabricar: obtener pack voltage/current/BMS, contacts/crimp/wires,
fuse insert selection/time-current/interrupt, reverse/TVS/inrush/DC converters/
PD/contactors, revisar copper/vías/thermal/EMI y floorplan, módulos/straps,
rearme/brownout/fault recovery real, retención motor, opto/PA, USB y SMA RF,
ensamble BOM/CPL/LCSC. Ensayar bancada controlada power-on/off/brownout,
Linux/GPIO crash, heartbeat fijo/perdido, NC/E-stop/rearme/MCP reset y
recuperación, picos/stall, estabilidad/ripple, RF/desense/ROE/armónicos y masa.
**Ninguno de esos ensayos físicos se ha efectuado.** ERC/DRC0 no los sustituye.

