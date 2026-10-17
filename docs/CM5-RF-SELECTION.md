# Seleccion CM5/RF: evidencia, interfaces y exclusiones

Fecha de recopilacion: 2026-10-10. Este registro distingue capacidad
documentada de componente, eleccion de arquitectura y prestaciones del
conjunto que necesitan banco. No es una liberacion de fabricacion.

## Arquitectura vigente

CM5 con CM5IO oficial adquirida, auxiliar original AZ/EL/POL y dos
LimeSDR Mini reemplazables. Dos receptores VHF/UHF concurrentes; ambas
cadenas tienen capacidad TX, pero politica inicial de un solo TX activo.
Sin ESP32 en la variante nueva; conservar la entrega anterior como historica.

| Elemento | Evidencia primaria | Limite |
| --- | --- | --- |
| CM5 | [Ficha oficial](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008180-DS-7-cm5-datasheet.pdf) | Revisar variante RAM/eMMC/wireless, temperatura, consumo y montaje exactos |
| CM5IO | [Documentacion oficial fijada](https://github.com/raspberrypi/documentation/blob/62ba0a0c2dd5030fe9b19458fa9bd174a451f79b/documentation/asciidoc/computers/compute-module/introduction.adoc) | Dos USB3 nativos; perifericos, corriente y rol USB2 se cualifican en el conjunto |
| LimeSDR Mini 2.x | [Documentacion hardware fijada](https://github.com/myriadrf/LimeSDR-Mini-v2/blob/bcab0b65506c7c9dbee2a79a76a951aa8f1cd48d/docs/v2.4/index.rst) | 10 MHz-3,5 GHz; un RX/un TX por modulo, SMA hembra, 69 x 31,4 mm; peso de revision a verificar |
| Full-duplex Lime | [Pagina del fabricante](https://www.crowdsupply.com/lime-micro/limesdr-mini-2) y [ejemplo RX/TX concurrente](https://github.com/myriadrf/LimeSuite/blob/699d05b7212aa612a9802c219dd6621be88c77db/src/examples/dualRXTX.cpp) | Capacidad de modulo, no inmunidad del receptor a su PA/antena |
| Tasas Lime | [API fijada](https://github.com/myriadrf/LimeSuite/blob/699d05b7212aa612a9802c219dd6621be88c77db/src/API/LimeSDR_mini.cpp) | Rango anunciado por esta API clasica inicia en 100 ksample/s; consultar dispositivo real, no asumir 96 ksample/s RF |
| TMC5160 v1.5 | [Watterott pinout](https://learn.watterott.com/silentstepstick/pinconfig/tmc5160/) y [esquema fijado](https://github.com/watterott/SilentStepStick/blob/098b7518b0de31e6a12fda78c68ae2666b81fbb6/hardware/SilentStepStick-TMC5160_v15.pdf) | Strap/configuracion/clock/corriente/refrigeracion de modulo exacto, no cualquier StepStick |

La variante CM5 wireless 4 GB/16 GB eMMC es un candidato de compra, no
una medicion de rendimiento ni cambio necesario en el resto de modelos.
No asignar peso al CM5, SDR, disipador o portadora desde sus dimensiones.

## Movimiento determinista y GPIO

Tres drivers con generador de rampas autonomo permiten que Linux solicite
posiciones sin sintetizar STEP mediante un bucle no determinista.
La reserva propuesta SPI1 usa GPIO16/17/18 como selects y
GPIO19/20/21 como MISO/MOSI/SCLK. I2C GPIO2/3 y UART GPIO14/15 quedan
reservados para sensores y GNSS. **La reserva no es un netlist aprovado**:
prevalece el mapa de interfaces de la auxiliar y su revision de pruebas.
Congelar un mapa no implica que haya sido ensayado fisicamente.

En Watterott TMC5160 v1.5: abrir jumper SD_MODE para modo de controlador
de movimiento segun su documentacion, SPI_MODE=VIO, SD_MODE=GND,
VIO=3,3 V; EN alto deshabilita salidas; CLK=GND selecciona reloj interno.
CS necesita pull-up externo. DCO es salida, no nSLEEP. Verificar frecuencia
y tolerancia del reloj para conversiones de velocidad/aceleracion.
No aplicar estos detalles a una revision distinta sin comprobar su esquema.

CM5IO puede seleccionar logica 1,8/3,3 V: la auxiliar de 3,3 V exige
configuracion compatible. Los drivers no reemplazan finales NC,
encoders, homing ni corte/watchdog independientes de Linux.

## USB, audio y energia

Los dos Lime ocupan los dos USB3 nativos. Un codec de audio USB adicional
necesita una conexion host/hub alimentado y cualificado, no un tercer
puerto supuesto. Una alternativa I2S obliga a revisar conflictos con SPI1.
Las velocidades de enlace no son caudal garantizado de aplicacion.

CM5IO documenta alimentacion 5 V/5 A; el funcionamiento a 5 V/3 A limita
perifericos a 600 mA segun la documentacion citada. Revisar fuente,
negociacion USB-C y cable reales. Bateria LiFePO4 externa de 12 V requiere
convertidor apropiado; no conectar 12 V a USB-C/rail CM5 de 5 V.

Audio Bluetooth transparente S16LE mono a 8 ksample/s implica
128 kbit/s por sentido, 256 kbit/s duplex antes de cabeceras/reintentos.
No usar el BLE de control ESP32 de tramas de 20 bytes como prueba de audio.
La nueva interfaz, perdidas y creditos se describen en
[RADIO-HOST.md](RADIO-HOST.md); un ensayo fisico Android/CM5 sigue pendiente.

## Por que se descartan referencias como cadena RF directa

- [(tr)uSDX](https://dl2man.de/) y
  [uSDX SOTA](https://antrak.org.tr/blog/usdx-sota-modular-all-mode-sdr-hf-transceiver-for-qrp-operations/)
  son referencias HF; su formato/CAT no acredita 145/435 MHz.
- SA8x8 y equivalentes FM no tienen una implementacion AM/USB verificada
  por esta seleccion. No declarar SSB por añadir un selector en la app.
- RTL-SDR Blog V4 solo recibe: no satisface envio APRS/voz por si solo.
- Pluto nominal desde 325 MHz no cubre 145 MHz sin modificaciones:
  no usar un ajuste no soportado como capacidad garantizada.
- ATU-100 es un acoplador, no duplexor, PA o transceptor VHF/UHF.

Las licencias originales de referencias no se sustituyen por MIT/CERN
del trabajo nuevo. No se redistribuyen ni adaptan los archivos CM5IO
oficiales suponiendo una licencia abierta no identificada; CM5IO se compra
y sus fuentes se citan para estudio.

## RF de potencia: bloqueo independiente

Actualizacion 2026-10-17: [AMSAT y techo de 25 W](SATELLITE-COMMS.md).
El nuevo requisito es <=25 W FM/CW o <=25 W PEP SSB a la salida de la
cadena, un solo TX activo, previa cualificacion fisica. Para los
transpondedores inversores listados se requiere LSB TX/USB RX, no solo
USB. No se habilita potencia por este cambio documental.

Referencias anteriores: 5 W FM, 5 W PEP USB y 1 W portadora AM. Lime entrega baja
potencia, aproximadamente +10 dBm maximo dependiente de revision/frecuencia;
no potencia de varios vatios. PA lineales y filtros por banda siguen
condicionados a seleccion y ensayos.

5 W equivalen a unos 37 dBm; pasar de 10 dBm a 37 dBm implica 27 dB
de ganancia ideal antes de perdidas. Esto no determina la ganancia segura:
considerar maxima ganancia, compresion, IMD, transitorios y limitacion
independiente del drive. AM a 1 W de portadora y modulacion 100% llega
idealmente a 4 W PEP; la cadena requiere margen y verificacion espectral.
No reutilizar un PA clase E HF como amplificador USB lineal.

A 25 W se requieren unos 44 dBm de salida, 34 dB de ganancia ideal
desde +10 dBm antes de perdidas. Es presupuesto, no ajuste seguro de
ganancia ni especificacion del PA. Recalificar linealidad, refrigeracion,
proteccion LNA, filtros, potencia DC y autonomia; AM a 100% no debe
superar 6,25 W de portadora para mantener 25 W PEP ideales.

145 MHz x 3 = 435 MHz: un armonico del TX VHF puede caer dentro del
receptor UHF. Dos SDR, diplexor y seleccion RHCP/LHCP no prueban aislamiento.
Medir desensibilizacion, bloqueo, armonicos, ROE, temperatura e IMD con
carga y equipo apropiados, inicialmente a minima potencia.
No conmutar una red RF bajo TX salvo rating especificamente comprobado.

La recepcion, el permiso PTT, la seleccion mecanica POL y la mano circular
son funciones independientes. Girar axialmente no cambia RHCP/LHCP.
No habilitar TX por una respuesta software exitosa sin permiso fisico,
camino RF confirmado y retorno verificado de la cadena real.
