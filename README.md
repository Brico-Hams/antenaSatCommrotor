# PortableSatStation - estacion portable 145/435 MHz

## Idiomas / Languages / Nyelvek

La documentacion se prepara en espanol, ingles y hungaro. Las ediciones
inglesa y hungara estan en traduccion/sincronizacion y no se consideran
completas hasta comprobar cobertura y correspondencia con la revision
tecnica vigente. El indice de idiomas se enlazara al finalizar esas pruebas.
Los textos originales de licencias de terceros se conservan sin alteracion.

## Costes y materiales de referencia

La ampliacion incorporara precios de referencia en EUR para componentes,
materiales de montaje y consumibles, con cantidad, modelo/revision, fecha,
fuentes, IVA y portes. El promedio se calculara solamente con cotizaciones
comparables; una sola observacion se identificara como tal. Componentes
todavia sin modelo aprobado tendran una provision orientativa claramente
separada o precio pendiente, nunca coste cero ni precio inventado.
Las herramientas reutilizables se presupuestaran aparte del coste de la
estacion. Los pasos ilustrados se relacionaran con los identificadores de
la BOM para distinguir piezas, cables, fijaciones y materiales externos.
Las observaciones y categorias pendientes se conservan en
[reference-prices.csv](bom/reference-prices.csv), con metodo y limites en
[REFERENCE-PRICES.md](docs/REFERENCE-PRICES.md). El subconjunto electronico
cotizado suma 1313.90 EUR sin IVA normalizado; no es el coste de la estacion
completa. La recopilacion sigue abierta y no constituye presupuesto cerrado.

Diseno original modular de una estacion de radioaficionado para satelites:
antena plegable de dos bandas, rotor AZ/EL de dos ejes, controlador ESP32
con AP web y seguimiento local, compartimento RF desmontable y soporte RT3S.

**Autores actuales:** Anatol EA5KAO, Diego EA5JEF y Pedro Roca Molina.
Referencia de divulgacion cientifica para ninos y adolescentes:
[Bricohams](https://bricohams.org).
Ver [autoria](AUTHORS.md), [agradecimientos](ACKNOWLEDGEMENTS.md) y
[aviso de responsabilidad](DISCLAIMER.md). Uso educativo siempre supervisado.

**Estado: prototipo de ingenieria, no equipo RF/mecanico certificado.**
Los resultados de compilacion, pruebas y exportacion se registran en
[VALIDATION.md](docs/VALIDATION.md). Una compilacion o un STL valido NO
demuestra ROE, ganancia, resistencia al viento ni seguridad de una
estructura montada. No fabricar en serie ni transmitir sin el protocolo
de puesta en servicio.

![Arquitectura modular original](docs/system-overview.svg)

## Base acordada

| Aspecto | Decision |
| --- | --- |
| Bandas | 145 y 435 MHz; canales concretos segun satelite y normativa |
| Motores | Dos NEMA 14; corriente/par segun ficha del motor elegido |
| Reduccion | BASE: dos etapas de correa GT2 20:100, total 25:1; planetarios como LEGACY |
| Material | ASA para piezas mecanicas; conductores y ejes metalicos |
| Seguimiento | SGP4 en ESP32; el movil no es el motor orbital |
| Red | AP sin Internet; STA con Internet o importacion manual de TLE |
| Radio | RT3S/OpenGD77 independiente; sin CAT/PTT automatico supuesto |
| Montaje | Tripode fotografico, inserto metalico y adaptadores de boom |
| Modularidad | Antena, rotor, radio y diplexor se separan |
| Masa | <=5 kg para conjunto operativo incluido tripode, radio y cables; bateria externa excluida por eleccion posterior; objetivo <=3 kg historico |
| Carga inicial | Objetivo a ensayar: antena <=0,5 kg, CG <=30 mm del eje EL |

**Cambio de prioridad aprobado:** la variante planetaria resulto demasiado
pesada en el presupuesto preliminar (3,208-4,038 kg con alimentacion).
El usuario autoriza una transmision mas ligera para priorizar <=3 kg.
La variante BASE conserva 25:1 y 80000 microsteps/vuelta, coordinados con
firmware. La geometria de montaje aun requiere verificacion fisica;
el calculo planetario original permanece
como comparativa, no como prueba de la variante ligera.

## Ampliacion en desarrollo: radio integrada multimodo

Esta seccion recoge las peticiones posteriores a la entrega inicial.
**No son prestaciones ya verificadas del hardware anterior ni de la APK
publicada localmente.** La tabla distingue alcance solicitado y estado;
las cifras medidas se registran en [VALIDATION.md](docs/VALIDATION.md).

| Funcion | Descripcion tecnica y limites | Estado de la ampliacion |
| --- | --- | --- |
| Radio de satelites VHF/UHF | 145/435 MHz nominales, frecuencias concretas segun satelite y normativa; cadenas RX/TX independientes para full-duplex | Arquitectura RF en verificacion; dos modulos seleccionados |
| Modos analogicos | FM, AM y SSB banda lateral superior (USB); USB aqui significa modo de modulacion, no conector | Solicitados; no se anuncian posibles en un modulo exclusivamente FM |
| CAT y Doppler | Control de frecuencia RX/TX y modo desde la misma APK; correccion dependiente de velocidad radial y plan de frecuencias | Integracion nueva pendiente; RT3S conserva operacion independiente sin CAT supuesto |
| Ordenador integrado | Raspberry Pi Compute Module 5 (CM5), CM5IO oficial, alimentacion y refrigeracion, para SDR, audio, SGP4 y rotor sin ESP32 | Arquitectura elegida; rendimiento conjunto, potencia y termica pendientes |
| Portadora y PCBA | CM5IO oficial adquirida mas placa auxiliar original para movimiento/sensores/protecciones | Eleccion confirmada; Gerbers/BOM/CPL de la auxiliar en desarrollo. No se fabrica una portadora CM5 unica personalizada en esta revision |
| Modulos RF | Dos LimeSDR Mini reemplazables, uno por banda para recepcion VHF/UHF simultanea; ambos capaces de TX; SMA convencional 50 ohm | Eleccion vigente; un solo TX activo inicialmente. Salida nativa de baja potencia, no 5 W: PA lineales y filtros requieren cualificacion fisica |
| Movimiento bajo Linux | Generador de movimiento dedicado en drivers, limites NC, corte fisico de potencia y watchdog independiente | Drivers y placa nueva pendientes; no generar STEP con un bucle no determinista y declarar precision |
| GNSS/GPS | Receptor y antena para sitio, altitud y UTC de SGP4; interfaz UART y PPS solo con niveles/protocolo documentados y verificados | GNSS NMEA implementado en variante ESP32; receptor/interfaz SBC y antena por seleccionar; PPS opcional y no verificado; GNSS estacionario no da rumbo |
| Brujula | Magnetometro remoto, calibracion del conjunto instalado, declinacion por sitio/fecha y referencia de norte verdadero | Compass/magnetometro nuevo no implementado ni calibrado; sensor, montaje, interfaz y PCB pendientes; conectores opcionales previos no implican brujula funcional |
| Inclinacion/nivel | IMU mide inclinacion de la base para compensacion de inclinacion de brujula; no es elevacion de antena | IMU, montaje, interfaz y calibracion nuevos pendientes; cableado/pines TBD hasta congelar PCB |
| Posicion de ejes | Tres encoders de salida independientes AZ/EL/POL y seis finales NC independientes (dos por eje); homing y limites conservadores | Tres canales de feedback y seis entradas por disenar. Tres AS5600 comparten direccion I2C 0x36: buses separados o multiplexor concreto y verificado; no asumir bus comun |
| Audio Bluetooth | Bidireccional: recepcion a Android y envio de voz/AFSK hacia radio; transporte PCM transparente separado del BLE del rotor | Protocolo y caudal en desarrollo; no atribuir audio a las tramas de control actuales |
| Audio local | Altavoz pequeno y microfono integrados; accesorio externo tipo Baofeng/K1 con jacks separados de 3,5/2,5 mm | No son conectores SMA ni de alimentacion; pinout, bias, PTT y compatibilidad exacta pendientes; no cablear por apariencia |
| SSTV en Android | Recepcion y reconstruccion de imagenes ISS PD120/PD180 desde audio | Decodificador y vectores de prueba en desarrollo |
| Funciones tipo Look4Sat/Robot36 | Primera version acordada: catalogo/pases, mapa/radar, avisos, frecuencias/Doppler, tres ejes, SSTV ISS y mensajeria APRS | Matriz funcional y desarrollo por etapas; no se promete paridad completa ni todos los modos Robot36 |
| Digitales en Android | Bell202 AFSK1200, AX.25 con NRZI, bit stuffing y CRC; interpretacion APRS | Desarrollo y pruebas PCM pendientes; no incluye automaticamente otros protocolos digitales |
| Mensajes APRS | Recepcion, redaccion y envio entre indicativos, destinatario, ID y ACK/rej | Codificacion de audio y transporte RF se verifican por separado; un WAV no demuestra transmision ni entrega |
| SMS celular | No solicitado en la seleccion final: APRS entre indicativos no es SMS a un numero de telefono | Sin pasarela movil ni promesa de entrega |
| PCB/Gerbers actualizados | Nueva portadora de ordenador, motores, audio y protecciones, con modulos RF desmontables | Revision separada pendiente de componentes/pinouts; no usar la aprobacion ERC/DRC anterior |
| Ensamblaje JLCPCB | Paquete de Gerbers/taladros, BOM PCBA y CPL pick-and-place con referencias, coordenadas, cara y rotacion; listado separado de modulos/manual/DNP | Solicitado; pendiente de placa rutada, LCSC exactos y verificacion. No se ha enviado una orden |
| Caja y energia | Branding Bricohams, acceso a conectores, blindaje RF metalico, ventilacion, bateria y protecciones | Reabrir cotas, consumo, temperatura y masa tras seleccionar hardware |
| Autonomia | Objetivo 2 horas con dos receptores activos y transmision intermitente; incluir CM5, Bluetooth, sensores y tres ejes | Consumo, porcentaje TX, capacidad util y eficiencia pendientes de medida; no duracion garantizada |
| Tercer eje POL | Motor para giro axial limitado de la antena, posicion calibrada, limites fisicos y paso protegido de coaxiales | Diseno y recalculo de masa, cargas, transmision y tres canales de motor en desarrollo |
| Seleccion RHCP/LHCP | Conmutacion RF de alimentacion/fase en antena circular compatible, distinta del giro mecanico POL | Redes por banda y conmutacion con TX inhibido pendientes de diseno y medida |
| Conectores RF | SMA convencional de 50 ohm en antena, diplexor VHF/UHF, hibrido/puertos CP, LimeSDR/radio y bulkheads | Eleccion vigente para aligerar; no RP-SMA, BNC de base ni cadenas de adaptadores. Verificar pin/socket central y genero de acoplamiento en cada pieza; masa, soporte, alivio y par del fabricante TBD. BNC solo opcion heredada |
| USB-C | Preferencia para alimentacion y datos; conservar SMA RF, K1 audio y Bluetooth bidireccional | Verificar rol host/provisionamiento, velocidad, tension y negociacion/cable de potencia por puerto; no asumir un unico puerto para todo |
| Alimentacion Powerpole y fusibles | Powerpole rojo/negro en enlace bateria externa/estacion, fusible principal cerca del positivo de bateria y fusibles por rama CM5/motores/RF | Seleccionar contactos/cable/portafusibles DC y calibres segun carga, inrush y proteccion del conductor; BMS no sustituye fusibles |
| EMI de alimentacion | Evaluar choque de modo comun, filtro diferencial amortiguado y desacoplos por rama; separar retorno/potencia de motores, conversores y RF | Corriente/saturacion/DCR, estabilidad del convertidor, transitorios y ruido recibido requieren medidas; no aislamiento RF garantizado |
| Sistema operativo BricoHams | Derivado de Raspberry Pi OS oficial ARM64 para CM5, banner/branding originales, dependencias y servicios del proyecto, aprovisionamiento privado local | Receta/CI en desarrollo; no imagen arrancada o flasheada verificada. Arranque sin movimiento/PTT y puesta en servicio explicita |

Las referencias [(tr)uSDX](https://dl2man.de/) y
[uSDX SOTA](https://antrak.org.tr/blog/usdx-sota-modular-all-mode-sdr-hf-transceiver-for-qrp-operations/)
orientan modularidad, formato y control CAT, pero son equipos **HF**:
no se escalan a 145/435 MHz cambiando solamente el firmware.
El [ATU-100](https://github.com/Dfinitski/N7DDC-ATU-100-mini-and-extended-boards)
es un acoplador, no un transceptor, filtro de aislamiento o diplexor VHF/UHF.
No se copian sus disenos ni se sustituyen sus licencias por las del proyecto.

Para full-duplex se deben medir aislamiento, bloqueo y desensibilizacion
del receptor durante TX en ambas combinaciones VHF/UHF, ademas de ROE,
armónicos y temperatura. Ningun valor de potencia, sensibilidad, autonomia,
latencia o precision de esta ampliacion se considera garantizado.
PTT debe quedar desactivado en arranque, fallo, perdida de enlace o expiracion
del permiso; transmision requiere autorizacion y puesta en servicio fisica.
La compresion de voz y la supresion de ruido pueden impedir SSTV/AFSK;
una conexion Bluetooth correcta no prueba que el audio digital sea util.
Girar una antena circular alrededor de su eje no invierte RHCP/LHCP:
la seleccion de mano necesita una red RF adecuada y ensayos de relacion
axial, fase y aislamiento. El tercer motor no existia en el rotor AZ/EL
anterior; sus drivers, limites y presupuesto no cubren el nuevo eje.

La primera entrega ESP32, su firmware/WebFlash, la APK y Gerbers anteriores
siguen siendo la variante documentada de referencia, no una implementacion
de la radio nueva. ### Matriz de variantes y evidencia (AUD-06)

| Generacion | Contenido | Pruebas que le aplican | Estado |
| --- | --- | --- | --- |
| ESP32 + RT3S (primera entrega) | ESP32 SGP4, WebFlash, APK ESP32 | 29 pruebas JVM, Node, firmware | Referencia historica; NO es aceptacion de CM5 |
| Intermedia (1-2 SDR) | Etapas del ADR-024 a ADR-026 | Pruebas de contrato de la etapa | Superada |
| CM5 + 2 LimeSDR Mini + AZ/EL/POL | Auxiliar CM5 rutada, Android CM5 | 58 pruebas JVM, 377 comprobaciones de contrato, ERC/DRC 0/0 | Prototipo DIGITAL; NO FABRICAR, NO ENERGIZAR, NO HABILITAR PTT |

Digital, fabricable y seguro operacionalmente son hitos distintos. Resultados
heredados de una generacion no se presentan como aceptacion de otra.

Si se adopta Raspberry Pi, su instalacion/aprovisionamiento
sera distinto de WebFlash ESP32. Consulte las decisiones
[ADR-024 a ADR-026](docs/ARCHITECTURE.md) y la trazabilidad
[R25 a R33](docs/REQUIREMENTS.md).

### Ubicacion, orientacion y sensores

El GNSS quieto **no mide el rumbo de la estacion**: proporciona sitio/UTC;
un rumbo deducido del movimiento no sustituye al norte verdadero del rotor.
El receptor GNSS usa UART unicamente cuando modulo, niveles logicos, protocolo,
conector y PCB esten verificados; usar PPS solo tras verificar su nivel,
polaridad y temporizacion en la documentacion del modulo exacto. La brujula
magnetometrica nueva **no esta implementada ni validada**. Debe instalarse
remota de motores, drivers, RF/potencia, cableado de alta corriente y piezas
ferromagneticas; su ubicacion, orientacion y pines siguen TBD hasta congelar
la PCB.

Calibrar hard/soft-iron y alineacion sensor-base con la estacion completa en
su configuracion final; registrar metodo, sitio/fecha y fuente/version de la
declinacion magnetica, y usar la inclinacion medida por IMU para compensar el
rumbo. Validar en campo contra una referencia manual independiente de norte
verdadero. Registrar variacion con motores apagados y encendidos bajo prueba
segura; comprobar efectos de RF/potencia solo en una prueba controlada y
autorizada, o dejarlos marcados pendientes. Si el campo es invalido, obsoleto
o discrepa de la referencia, mostrar error e inhibir el apuntado dependiente
del rumbo: nunca inferir rumbo de GNSS estacionario ni sustituirlo por cero.
El magnetometro no reemplaza los tres encoders ni los seis finales NC.
Ubicacion/UTC invalidas impiden seguimiento/Doppler; errores de posicion,
limites o parada deben inhibir movimiento y TX segun la politica verificada.

### Limite de masa actualizado

**Requisito vigente: <=5,000 kg del conjunto completo listo para operar**,
incluidos antena, rotor AZ/EL/POL, radio, ordenador, caja, sensores,
cables/conectores y tripode. **Bateria externa excluida por eleccion posterior**:
registrar aparte su masa como carga transportada adicional.
Pesar el inventario con esta unica exclusion explicita;
objetivo de trabajo propuesto <=4,500 kg para reservar 500 g de margen,
no resultado de medicion. La nueva variante aun no acredita cumplirlo.
Se mantiene el objetivo de 2 horas con bateria externa de 12 V de capacidad
a dimensionar. 12 V x 1 Ah = 12 Wh nominales: para 2 horas darian solo 6 W
medios antes de perdidas, no autonomia suficiente demostrada para CM5,
dos SDR y tres ejes. No confundir mAh (capacidad) con mA (corriente maxima).
El usuario autoriza dimensionar una bateria externa mayor; capacidad util,
corriente, tension extrema, convertidores y porcentaje TX requieren calculo
y ensayo. Su coste se incluye en el presupuesto aunque su masa se excluya.
**Referencia seleccionada posteriormente:**
[ECO-WORTHY LiFePO4 12 V / 30 Ah](https://es.eco-worthy.com/products/bateria-litio-lifepo4-12v-30ah?currency=EUR&country=ES&variant=40308275183822),
externa. 12 V x 30 Ah = 360 Wh es un calculo nominal, no energia util
medida ni autonomia garantizada. Verificar la ficha de la variante exacta:
tension nominal/maxima, limites BMS, carga/temperatura y peso. No trasladar
especificaciones de versiones 100 Ah a esta bateria. Su BMS no reemplaza
fusible externo ni convertidores; nunca conectar la bateria al rail CM5
de 5 V directamente.
La bateria alimenta la estacion mediante Powerpole y fusible principal
proximo al borne positivo, antes del cable largo. La distribucion tiene
ramas protegidas para convertidor CM5/USB-C 5 V, motores y RF; la parada
fisica/watchdog conservan su funcion independiente. Verificar polaridad
con multimetro, seccion/longitud de cable, crimps y fijacion. El valor y
curva del fusible se seleccionan con corriente de carga/inrush y capacidad
del conductor/conector/portafusibles, no por la corriente maxima del BMS.
No conectar o desconectar conectores bajo carga salvo rating verificado.
Los conectores SMA se limitan a RF: alimentacion y sensores conservan
conectores adecuados, y el micro/altavoz externo utiliza su interfaz de audio
verificada. Fijacion a panel y alivio de tension deben impedir que el peso
o la torsion del coaxial carguen una pista PCB o el contacto del conector.

El presupuesto BuildLight con PCB/caja final es **3,130-3,200 kg antes
de adicionales pendientes: el anterior <=3 kg NO se cumplia** y esa cifra
historica no incluye por si sola la nueva radio, POL ni el tripode.
La transmision por correa es reversible; se requiere equilibrio y
retencion mecanica independiente cuando motores quedan desenergizados.

La imagen comercial orienta el concepto de portabilidad, no se reproduce
su geometria ni sus archivos. El diseno a 449,55 MHz de una referencia
no se presume compatible con 145/435 MHz.

## Documentacion y archivos

- [Antena independiente: materiales, montaje y ajuste](docs/MODULE-ANTENNA.md).
- [Rotor independiente: montaje, sensores y configuracion](docs/MODULE-ROTOR.md).
- [Radio SDR independiente: montaje, audio y configuracion](docs/MODULE-RADIO.md).
- [Integracion general de los modulos paso a paso](docs/MODULE-INTEGRATED.md).
- [Arquitectura y decisiones justificadas](docs/ARCHITECTURE.md).
- [Evidencia de seleccion CM5, SDR, motores y limites RF](docs/CM5-RF-SELECTION.md).
- [Requisitos y trazabilidad](docs/REQUIREMENTS.md).
- [Analisis de los PDF](docs/REFERENCE-ANALYSIS.md).
- [Fuentes, licencias y procedencia](docs/SOURCES.md).
- [RF, diplexor y OpenGD77](docs/RF-AND-RADIO.md).
- [CAD, impresion y montaje](docs/MECHANICAL.md).
- [Control, cableado logico y API](docs/CONTROL.md).
- [PCB y archivos de fabricacion](docs/PCB.md).
- [WebFlash y compilacion en GitHub](docs/WEBFLASH.md).
- [App Android BLE y transferencia TLE](docs/ANDROID.md).
- [Ensayos de app y protocolo movil](docs/ANDROID-ACCEPTANCE.md).
- [Alimentacion y separacion electrica](docs/ELECTRICAL.md).
- [Calculos preliminares](calc/design.json).
- [Desarrollo numerico y margenes](docs/DESIGN-CALCULATIONS.md).
- [Orden de construccion](docs/BUILD-GUIDE.md).
- [Transporte y operacion de campo](docs/FIELD-MANUAL.md).
- [Riesgos y mitigacion](docs/RISKS.md).
- [Ensayos y criterios de aceptacion](docs/ACCEPTANCE.md).
- [Resultado verificable de esta entrega](docs/VALIDATION.md).
- [Placa auxiliar CM5 (KiCad rutada, ERC/DRC 0, NO fabricable)](hardware/cm5/DESIGN-REVIEW.md).
- [Precios de referencia](docs/REFERENCE-PRICES.md), [APK Android](releases/android/PortableSatStation-CM5-debug.apk).
- [pront.md](pront.md): prompt de auditoria independiente (ES/EN/HU).
- [CAD](cad/), [firmware](firmware/), [web](web/), [BOM](bom/).

## Validacion local

Requiere Node.js 22 o posterior para los calculos sin dependencias:

```powershell
node --test tests\engineering.test.cjs
node scripts\engineering-report.cjs
```

El manual de control describe la compilacion del firmware y su carga.
El manual mecanico describe la exportacion de cada pieza en OpenSCAD.
No hay un servicio cloud ni un PC obligatorio durante un pase.

## Uso de campo

1. Instalar un tripode estable; nivelar, equilibrar y verificar la fijacion.
2. Conectar los modulos con la alimentacion desconectada; comprobar parada.
3. Obtener posicion y UTC validas; confirmar norte verdadero y nivel.
4. Hacer homing y comprobar limites sin antena antes de cargarla.
5. Importar/actualizar TLE y verificar antiguedad y frecuencias.
6. Seleccionar un pase alcanzable y armar conscientemente el seguimiento.
7. Operar la radio de forma independiente: OpenGD77 y rotor deben usar
   el mismo satelite, posicion y tiempo. No esperar recibir mientras
   transmite una unica RT3S.
8. Parar, quitar alimentacion, desmontar y plegar; no plegar partes en movimiento.

Las instrucciones detalladas y los interbloqueos prevalecen sobre esta lista.
La caja ASA no proporciona blindaje RF; las redes pasivas se alojan en
un submodulo metalico y se verifican con VNA.

## Git

Repositorio local independiente, rama `main`. No se publica automaticamente.
No contiene los PDF adjuntos, credenciales Wi-Fi, ni modelos comerciales.
Licencias elegidas: software original MIT y hardware original
CERN-OHL-S-2.0; ver alcance y derechos de terceros en [NOTICE.md](NOTICE.md).

Flujo GitHub Actions / Pages preparado para compilar y ofrecer
WebFlash de la placa de control. Bundle local generado y comprobado;
no se ha publicado ni ejecutado Pages remotamente. El despliegue exige
las aprobaciones documentadas y no significa aprobacion del hardware.

El controlador implementa calibracion web guiada y protocolo BLE.
La app Android incorpora descarga TLE por HTTPS y transferencia al
rotor; los pases y el seguimiento se calculan en el ESP32, no en el
telefono. APK debug (generacion ESP32) compilada, 29 pruebas JVM, lint y firma verificados (no aplican a la variante CM5, que registra 58);
no se ha probado interoperabilidad con un telefono y rotor fisicos.
