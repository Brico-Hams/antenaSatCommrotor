# Carrier modular original — PortableSatStation, revisión A

Autoría actual: **Anatol EA5KAO, Diego EA5JEF y Pedro Roca Molina**.
Consultar `AUTHORS.md`, `ACKNOWLEDGEMENTS.md` y `DISCLAIMER.md`: esta autoría
corresponde al trabajo original del proyecto, no a los módulos, herramientas
ni publicaciones citados. La referencia educativa a
[Bricohams](https://bricohams.org) no implica respaldo comercial de fabricantes.
La actividad con niños/adolescentes exige supervisión adulta competente;
el prototipo no es un juguete. No transmitir sin autorización/licencia aplicable.

## Estado y límites de esta entrega

Diseño original de **placa portadora**, no copia de un controlador comercial.
Fuentes editables: `hardware/PortableSatCarrier.kicad_sch`, `.kicad_pcb`,
`.kicad_pro`, biblioteca local `.kicad_sym` y `.pretty`; generador auditable
`hardware/generate-carrier.cjs`. No se sustituyen las capas de cobre por dibujos.
Los Gerber proceden de KiCad CLI y los taladros de su exportador Excellon.
`fabrication/PortableSatCarrier-Gerbers-CAD-VERIFIED-NOT-RELEASED.zip`
contiene únicamente las siete capas Gerber, dos Excellon y el job Gerber
reales; no incluye dibujos decorativos ni sustituye las notas de fabricación.
El nombre **NOT-RELEASED** es intencionado: no enviar el ZIP a producción
hasta completar los bloqueantes formales de esta revisión.
Consultar **`fabrication/release-status.json`**, informes ERC/DRC y sus hashes:
que un archivo exista no significa que esté autorizado para producción.

**Prototipo no montado ni ensayado. HOLD de montaje/uso hasta cerrar los puntos
de verificación física y de potencia indicados al final.** ERC/DRC sólo comprueban
las reglas CAD; no certifican seguridad, inmunidad RF, temperatura ni el ajuste
físico de módulos de terceros. Los símbolos representan terminales de módulos
reemplazables con pines pasivos: ERC no valida internamente sus reguladores,
sus límites de tensión ni su programa.

## Arquitectura eléctrica real

```text
Fuente comercial protegida 12 V (NO batería desnuda / NO cargador integrado)
  + -- interruptor general DC externo -- J1.1 RAW12
                                            |
                                D1 SB560 (ánodo->cátodo)
                                            |
                                      PROTECTED12
                                            |
                           F1 SPT T3,15 A -- FUSED12 -- D2 SMBJ15A -- GND
                               |                 |
                      F2 T2,5 A              F4 T1 A
                               |                 |
                         J2.1 STOP_SEND      J4.1 BUCK12 -> VIN buck externo
                               |                 J4.2 GND -> GND buck
               contacto NC POTENCIA externo             |
               pulsador mantenido/enclavado         Pololu D24V22F5
               >=5 A DE CORTE a 12 V DC                  |
                               |                 VOUT -> J5.1 BUCK5
                         J2.2 VMOT               GND -> J5.2 GND
                               |                         |
                    C1/C2 220u/35 V                 F3 T1 A
                               |                         |
                   U2/U3 VM -> motores             JP1 puente extraíble
                               |                         |
                            GND                    U1 5V (ESP5)
                                                        |
                                              U1 regulador -> 3V3
                                                  sensores + VIO/MS1/MS2

Segundo contacto NC AISLADO del mismo pulsador: J3.1 STOP_N -- NC -- J3.2 GND
R2: 10k de STOP_N a 3V3. Abierto=HIGH=falla; normal=LOW.
```

J2 **no es entrada GPIO**: ambos bornes son positivos de la rama de potencia.
La corriente completa de ambos drivers atraviesa F2, J2 y el cable/contacto
externo; usar cable de cobre >=0,75 mm², corto y con alivio de tracción, y
bornas/contactos con capacidad DC documentada. No usar JST de señal, Dupont,
protoboard ni un contacto auxiliar de baja corriente en este circuito.
No puentear J2 para uso operativo. El pulsador exterior enclavado abre
físicamente VMOT, aunque MCU, Wi-Fi o firmware se bloqueen; lógica/web siguen
alimentadas antes del corte. La apertura permanece mientras el pulsador esté
enclavado. El retorno J2.2 alimenta efectivamente ambos drivers; la ruta no
depende de un relé controlado por software.

No se vende como parada de emergencia certificada. Los condensadores conservan
energía después de abrir: verificar caída de VMOT y tiempo de parada real.
Al desenclavar vuelve VMOT: **reset manual y rearme deliberado del controlador**
antes de mover. Si el requisito fuera un rearme eléctrico separado que siga
enclavado aun desenclavando el pulsador, esta revisión NO lo proporciona:
se necesita un contactor/control de rearme homologado externo, no un GPIO.

**D2 está después de F1**: F1 limita la rama de una TVS averiada en corto;
exigir además protección de cortocircuito/fusible en la fuente y en el cable
positivo, junto a la fuente. No conectar una batería sin ese fusible externo.
D1 bloquea polaridad inversa, pero no una sobretensión sostenida. Usar 12 V
regulados, máximo normal 13,8 V; **no usar 24 V**, aunque el driver lo admita.
SMBJ15A: standoff 15 V, clamp nominal máximo 24,4 V al pulso de ensayo;
Watterott especifica VM 5,5–28 V. Picos de cable y regeneración requieren
medición: una TVS no convierte cualquier fuente en compatible.

F1/F2/F3/F4 son Schurter SPT 5×20 cerámicos temporizados, números
0001.2509 (3,15 A), 0001.2508 (2,5 A), 0001.2504 (1 A, dos unidades).
Ficha SPT: 250 VAC / 300 VDC para estos valores, capacidad de corte DC
indicada por el fabricante; no sustituir por fusible sólo especificado AC.
Portafusible OGN 0031.8201: paso 22,5 mm, apoyo central NPTH 2,7 mm incluido.
Los valores son de arranque de prototipo, no prueba de selectividad.

## Módulos EXACTOS, orientación y conexiones

### U1: Espressif ESP32-DevKitC V4, ESP32-WROOM-32E, 38 pines

No sirve un DevKit genérico de 30 pines, C3, S3 ni una placa con otra separación.
Dos filas hembra de 19, paso **2,54 mm**, separación de centros **25,40 mm**.
Verificar con el módulo real antes de pedir placas; USB hacia y creciente,
antena hacia borde superior. Vista desde componentes:

```text
             ANTENA / sin metal ni cobre debajo de la antena
 izquierda x=77 mm                     derecha x=102,4 mm
  1 3V3        20 GND
  2 EN NC      21 IO23 NC
  3 VP/IO36    22 IO22
  4 VN/IO39    23 TX0 NC
  5 IO34       24 RX0 NC
  6 IO35       25 IO21
  7 IO32       26 GND
  8 IO33 NC    27 IO19
  9 IO25       28 IO18
 10 IO26       29 IO5 NC
 11 IO27       30 IO17
 12 IO14       31 IO16
 13 IO12 NC    32 IO4 NC
 14 GND        33 IO0 NC
 15 IO13       34 IO2 NC
 16 SD2 NC     35 IO15 NC
 17 SD3 NC     36 SD1 NC
 18 CMD NC     37 SD0 NC
 19 5V         38 CLK NC
                   USB
```

NC significa deliberadamente sin conexión al carrier, con marcador NC en
esquema; los pines flash/strap no se emplean. Las redes CAD NC no se unen entre sí.

| Función | GPIO | Polaridad / tensión |
|---|---:|---|
| AZ STEP / DIR | 26 / 27 | lógica 3,3 V |
| EL STEP / DIR | 14 / 13 | lógica 3,3 V |
| Enable común | 25 | activo LOW; R1 10k a 3V3 deshabilita al arranque |
| Monitor parada | 34 | NC a GND, abierto HIGH; pull-up externo |
| AZ mínimo / máximo | 35 / 36 | NC a GND, abierto HIGH; pull-up externo |
| EL mínimo / máximo | 39 / 32 | NC a GND, abierto HIGH; pull-up externo |
| RX ESP desde GNSS / TX ESP a GNSS | 16 / 17 | UART 3,3 V, NO RS232 ni TTL 5 V |
| AZ SDA / SCL | 21 / 22 | bus I2C0 3,3 V |
| EL SDA / SCL | 18 / 19 | bus I2C1 separado 3,3 V |

GPIO34–39 no disponen de pull-up interno: R2–R6 están realmente en la placa.
No están incorporados drivers de entradas industriales 12/24 V.
JP1 retirado **antes** de conectar USB alimentado: Espressif declara mutuamente
excluyentes USB, 5V externo y 3V3 externo. Nunca alimentar por dos métodos.
El carrier toma su 3V3 exclusivamente del regulador del DevKit; no hay segundo
regulador conectado en paralelo. Reservar presupuesto máximo inicial **100 mA
externos** (sensores+GNSS+VIO), medir caída/temperatura con Wi-Fi transmitiendo;
la capacidad real depende del DevKit y GNSS seleccionados.

El buck NO tiene footprint de módulo ni pinout geométrico supuesto en esta
placa: se instala separado y se cablean únicamente los puntos **rotulados**
VIN, GND y VOUT del **Pololu D24V22F5**. J4.1=VIN, J4.2=GND,
J5.1=VOUT 5V, J5.2=GND; EN y PG del módulo quedan sin conectar conforme a
su documentación. No sustituir por D24V25Fx: el fabricante advierte que su
pinout es diferente. La posición física de sus pads no define la del carrier.
La protección inversa/corto/térmica del buck es propia del módulo seleccionado;
la salida se comprueba a 5 V antes de conectar J5/ESP. Ningún conector GPIO
o sensor del carrier lleva BUCK5/FUSED5/ESP5.

### U2/U3: Watterott SilentStepStick TMC2209 **v2.x**

No presumir intercambiabilidad con A4988 ni clones BTT. Sockets hembra,
2 filas de 8, paso 2,54 mm, separación 15,24 mm. Vista superior, pines de
izquierda/derecha empezando por la parte superior del dibujo del fabricante:

| Pad carrier | Izquierda | Pad carrier | Derecha |
|---:|---|---:|---|
| 1 | EN=ENABLE_N | 9 | VM=VMOT |
| 2 | MS1=3V3 | 10 | GND |
| 3 | MS2=3V3 | 11 | M2B |
| 4 | SPREAD=GND | 12 | M2A |
| 5 | PDN_UART NC | 13 | M1A |
| 6 | PDN_UART NC | 14 | M1B |
| 7 | STEP | 15 | VIO=3V3 |
| 8 | DIR | 16 | GND |

MS1=MS2=HIGH, SPREAD=LOW: **1/16**, interpolación 1/256, stealthChop.
El módulo tiene pull-down interno de PDN_UART; conservar jumper de fábrica,
no convertirlo a UART ni cortar SPREAD. DIAG/INDEX auxiliares de la placa del
driver no están conectados: no se implementa StallGuard/sensorless homing.
La reducción mecánica de referencia es 25:1; confirmar la variante mecánica
final y el microstepping real antes de calibrar pasos/grado.

JM1/JM2, de izquierda a derecha: M2B, M2A, M1A, M1B.
M2B/M2A pertenecen a una bobina; M1A/M1B a la otra. Medir con óhmetro sin
alimentación. No enchufar/desenchufar motor con VMOT presente. Regular VREF
según versión/resistencia sense y ficha Watterott, empezando con corriente baja.
**1 A por fase es objetivo provisional**, no ajuste universal de potenciómetro
ni corriente de batería. Disipador y ventilación necesarios; probar temperatura.

## Sensores, GNSS y finales de carrera

Todos los JST son XH verticales **2,50 mm**, no 2,54 mm; crimp compatible y
alivio mecánico. Pad cuadrado + “1” identifica pin 1 en cada footprint.

| Conector | Pines 1,2,3,4 |
|---|---|
| J6 GNSS externo | 3V3, GND, GNSS_TX (hacia RX16), GNSS_RX (desde TX17) |
| J7 AS5600 AZ | 3V3, GND, AZ_SDA, AZ_SCL |
| J8 AS5600 EL | 3V3, GND, EL_SDA, EL_SCL |
| J9 opcional IMU/magnetómetro | 3V3, GND, AZ_SDA, AZ_SCL |

AS5600 usa **0x36**, ambos sensores deben ir en buses distintos. Breakout
alimentado a 3,3 V, no pull-ups a 5 V. R7–R10 4k7 en placa; si el breakout
ya monta pull-ups, calcular resistencia equivalente o retirar uno de los
juegos. Mantener I2C corto (objetivo <30 cm), separado de cables de motor.
No asumir funcionamiento fiable en cables largos sin prueba o transceptores.
Opción MPU6050 0x68/0x69 y LIS3MDL 0x1C/0x1E no colisiona con AS5600;
usar breakouts explícitamente compatibles con **VIN y lógica 3,3 V**.
J9 no implica que el firmware integre esos dispositivos.

GNSS sugerido: Adafruit Ultimate GPS breakout 746, comprobar revisión,
entrada VIN 3,3 V y UART 3,3 V antes de cablear; antena GNSS exterior separada
del ESP y radio. La PCB sólo proporciona UART/alimentación, no antena GNSS,
PPS ni interfaz RF. GNSS de una antena NO mide rumbo estático verdadero.
AS5600 mide ángulo relativo del eje; calibrar cero, dirección y eje físico.
La referencia Norte/elevación se calibra manualmente; magnetómetro junto
a motores, acero, imanes AS5600 y cables puede estar gravemente distorsionado.
No prometer heading absoluto automático ni confundir rumbo de movimiento
GNSS con orientación de antena.

| NC auxiliar, dos pines: señal / GND | GPIO |
|---|---:|
| J3 parada, contacto auxiliar aislado | 34 |
| J10 AZ mínimo/home | 35 |
| J11 AZ máximo/travel | 36 |
| J12 EL mínimo/home | 39 |
| J13 EL máximo/travel | 32 |

Ruptura del cable/accionamiento=HIGH. Son entradas de monitor, no corte
certificado. Los límites de carrera no cortan VMOT por sí mismos.
No compartir el contacto de potencia 12 V con un GPIO. Cablear todos los NC
antes de armar; no poner puentes permanentes para ocultar fallos.

## Fabricación y montaje, paso a paso

1. Abrir el proyecto con KiCad 10.0.7 o posterior compatible. Comparar
   `connectivity.json` con `firmware/include/board_config.h` y `docs/CONTROL.md`;
   cualquier diferencia exige regenerar y validar, no corregir sólo un dibujo.
2. Ejecutar `hardware/validate-export.ps1 -KiCadCli <ruta-local>\kicad-cli.exe`.
   Este script **bloquea exportación nueva** si ERC, DRC, paridad o conectividad
   fallan; crea hashes, Gerber, Excellon, netlist y posiciones de montaje.
3. Pedir FR4, dos capas, **cobre terminado 70 µm (2 oz) en ambas caras**,
   1,6 mm espesor, máscara ambas caras, serigrafía frontal/blanca, sin vías
   ciegas, sin impedancia controlada. HASL sin plomo o ENIG. Rectángulo
   180×130 mm; cuatro NPTH 3,2 mm. Consultar notas de `fabrication/STACKUP.txt`.
   No aceptar 1 oz como sustitución automática. Pedir prueba eléctrica por netlist.
4. Revisar Gerber en visor independiente: dos cobres con miles de segmentos
   y pads, masks, silk, contorno cerrado y PTH/NPTH separados. Verificar unidad
   mm y mismo origen en capas/taladros. No fabricar sólo `Edge.Cuts`.
   El CSV de posiciones de KiCad usa Y cartesiano hacia arriba: `PosY=-y`
   respecto a las coordenadas de PCB indicadas aquí. No invertir sólo una
   capa ni sólo el taladro; enviar siempre el juego completo exportado.
5. Comprobar con calibre ESP 19×2/25,40 mm, TMC 8×2/15,24 mm,
   JST 2,50 mm, bornas 5,08 mm, portafusibles 22,50 mm + apoyo central.
   Bloqueante: comprobar cuerpo, orientación de enclavamiento y acceso de
   tornillos; las envolventes originales son conservadoras, no STEP del proveedor.
6. Montar resistencias, D2 (cátodo marcado K al positivo), condensadores
   cerámicos, D1 (banda/cátodo K hacia PROTECTED12), sockets, bornas y
   portafusibles. C1/C2: positivo VMOT, negativo GND. No insertar módulos.
7. Óhmetro: no corto RAW12-GND, VMOT-GND ni ESP5-GND; verificar continuidad
   J2.2->U2/U3.VM y ausencia J2.1->J2.2 con parada abierta. Verificar que el
   NC auxiliar nunca recibe 12 V. Inspeccionar soldadura y polaridad.
8. Fuente de laboratorio 12 V limitada inicialmente a 100 mA, parada
   enclavada; medir buck aislado 5 V antes de conectar J5; incrementar límite
   sólo tras pruebas. Insertar ESP sin USB y JP1 apropiado, medir 3V3.
9. Insertar drivers sin motores, confirmar VIO y MS1/MS2=3V3 y EN HIGH.
   Parada enclavada: VMOT debe caer aunque Wi-Fi siga activo. Ensayar pulsador,
   cable roto, reset, pérdida de GNSS/encoder y desconexión de límite.
10. Conectar motores sin potencia, bajar VREF, hacer movimientos cortos sin
    antena cargada. Confirmar dirección, escalado 25:1, recorrido y feedback.
    Ensayar consumo/temperatura al menos 30 min antes de objetivo 1 A/fase.
    Medir transitorios VMOT en apertura y frenado, incluyendo cable largo.
11. Montar en caja de electrónica exterior con separadores aislantes M3.
    Origen PCB esquina superior izquierda; agujeros (5,5), (175,5),
    (5,125), (175,125) mm. Reservar altura total >=30 mm desde cara superior
    de PCB hasta techo de caja, no 30 mm adicionales sobre los drivers,
    acceso al USB/tornillos y aire. NO se afirma que quepa en cavidad del rotor.
    La coordinación mecánica debe usar esas coordenadas y este tamaño real.

La caja previa de 130×70 mm NO admite esta placa de 180×130 mm: se requiere
caja independiente mayor o soporte específico, no un escalado silencioso de
huellas. Reservar inicialmente >=20 mm alrededor para entradas de cable y
>=30 mm desde superficie superior PCB hasta techo; verificar radios de
curvatura/acceso real y altura efectiva de conectores/disipadores.
Mecánica ha creado `cad/carrier_enclosure.scad`: **revisión final ampliada**
exterior nominal 228×178×43,6 mm + tapa 2 mm + relieve 0,7 mm,
interior 224×174 mm; esquina PCB (24,24),
centros de soporte (29,29), (199,29), (29,149), (199,149) mm en la caja.
PCB a z=8 mm y 32 mm de altura libre sobre espesor nominal 1,6 mm;
esa altura total deja nominalmente 12 mm sobre un conjunto de driver de
20 mm de altura, no 32 mm libres por encima de él.
La revisión mecánica final declara pasos M3 de caja 3,2 mm, coincidentes
con taladros PCB reales 3,2 mm: comprobar holgura de impresión y no forzar
los tornillos ni usar la PCB como plantilla de taladrado con componentes.
Esta compatibilidad **de coordenadas** no demuestra encaje físico:
el margen lateral final es 22 mm por borde y los paneles están sin perforar;
definir puertos/alivio de tracción y acceso de cable/tornillos con la PCB
montada antes de cerrar la caja. La caja se monta estacionaria, no sobre el
eje móvil. Su masa CAD sólida estimada ≈260 g ASA tampoco es masa medida.
El soporte estacionario adicional `cad/carrier-metal-mount.dxf` es bandeja
de aluminio **240×196×2 mm**, masa presupuestada ≈254 g, no medida. Considerar
esa masa y las fijaciones además del carrier/caja en el balance de estación.
Estas dimensiones sustituyen la caja anterior 188×138 y la bandeja 200×156;
no fabricar esas revisiones antiguas para este conjunto final. El presupuesto
BuildLight comunicado de 3,130–3,200 kg antes de extras pendientes supera
el objetivo 3 kg: **objetivo de masa incumplido en el presupuesto actual**,
no ocultar el incremento ni afirmar que el conjunto cumple.
AS5600 va en los dos ejes de salida externos: el carrier no impone patrón de
agujeros para un breakout de encoder aún no seleccionado.

Estimación de masa, **no medición**: FR4 completo
`0,180 × 0,130 × 0,0016 × 1850 ≈ 69 g`; cobre completo hipotético en dos
caras 70 µm suma hasta ≈29 g antes de descontar grabado. Reservar ≈100 g para
placa desnuda y **150–220 g para el conjunto PCB+módulos** como provisión,
sin caja, fuente/batería, buck exterior, stop ni cables. La cifra no demuestra
el objetivo de masa total de la estación; pesar ensamblaje y revisar margen.

Separar RF 145/435 MHz, coaxiales, motores y buck de GNSS/ESP/sensores.
Caja metálica RF requiere sacar antenas y no cubrir antena ESP integrada.
Esta PCB no es duplexor, filtro RF, amplificador ni interfaz de transmisor.

## Bloqueantes de liberación de montaje / utilización

- Módulos reales y dimensiones comprobados; no sustituir pinouts por semejanza.
- Fuente comercial protegida, fusible de cable y desconexión general verificados.
- Referencia **exacta** de pulsador exterior, contactos NC aislados, corriente
  y **poder de corte DC >=5 A a 12 V** documentados. No basta marcado “10 A AC”.
  El BOM no inventa una pieza homologada; hasta seleccionar esa pieza no se
  autoriza operación con motores. Su enclavamiento es mecánico, no relé software.
- Selectividad fusibles, cortocircuito, TVS, regeneración, caída de tensión
  y temperatura de D1/pistas/terminales/driver ensayados al peor caso real.
- 3V3 del DevKit ensayado con Wi-Fi y todos los periféricos; presupuesto real.
- Firmware con este pinout y microstepping, calibración/recorrido mecánico
  y stop/rearme verificados en banco. Ninguna simulación sustituye estas pruebas.

## Trazabilidad y licencias

Esquema, PCB, reglas/footprints y documentación técnica de hardware originales:
**CERN-OHL-S-2.0**, copyright © 2026 Anatol EA5KAO, Diego EA5JEF y Pedro Roca
Molina; ver `LICENSES/CERN-OHL-S-2.0.txt` y `hardware/LICENSE.txt`.
El generador, script de validación y tests originales son software **MIT**,
con el mismo aviso de copyright; ver `LICENSES/MIT.txt`.
No se importó una PCB de terceros. Las publicaciones del fabricante se
consultaron en sus URLs oficiales y no se redistribuyen dentro del proyecto;
sus autores conservan sus derechos y no se les atribuye respaldo del prototipo.
KiCad oficial 10.0.7 extraído localmente de
`https://s3.cern.ch/kicad-downloads/windows/stable/kicad-10.0.7-x86_64.exe`;
no instalación global. KiCad software GPL; librerías oficiales de KiCad
CC-BY-SA 4.0 con excepción de uso en diseño. Se consultó la geometría
`Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open` para confirmar
paso/apoyo; las figuras del módulo no se incorporan a Gerber.

Fuentes consultadas (10-10-2026):
- Espressif DevKitC V4: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- Esquema oficial: https://dl.espressif.com/dl/schematics/esp32_devkitc_v4-sch.pdf
- TMC2209 v2: https://learn.watterott.com/silentstepstick/pinconfig/tmc2209/
- Esquema Watterott: https://github.com/watterott/SilentStepStick/tree/master/hardware
- Fusible SPT: https://www.schurter.com/en/datasheet/typ_SPT_5x20.pdf
- Buck D24V22Fx: https://www.pololu.com/product/2858
- AS5600: https://ams-osram.com/products/sensor-solutions/position-sensors/ams-as5600-position-sensor

Los precios de `bom/pcb.csv` son estimaciones unitarias orientativas, no ofertas;
añadir crimp, cable, disipadores, stop DC, fuente, caja y transporte. No hay
cargador de litio en placa ni declaración de seguridad funcional.
