# Calibraciones y verificaciones: DC, sensores, mecanica y sistema

Estas operaciones generan registros «antes/ajuste/despues» con patrones,
incertidumbre y limites acordados. Verificar con referencia independiente;
ajustar a una lectura y volver a leerla no demuestra exactitud.
No sustituye instrucciones de fabricantes ni autoriza una placa HOLD.

## Recepcion por familia: cada componente y cada unidad

Aplicar LAB-01 a todas las filas seleccionadas de `componentes.csv` y
expandir por unidad fisica. Esta tabla asigna los metodos para completar
la columna de ensayos bajo revision; **no permite aceptar un lote por
medir solo una unidad sin un plan de muestreo aprobado**.

| Familia | Conexion/metodo y lectura real | Referencia/ensayos y motivo de parada |
| --- | --- | --- |
| Resistencias y terminaciones DC | Sin energia, aislar una pata si circuito paralelo; DMM apropiado o cuatro hilos para shunt, valor/temperatura y tolerancia | BOM/ficha, LAB-01/06; una resistencia DC 50 ohm no es una carga RF caracterizada |
| Condensadores | Descargar y comprobar cero V; LCR en frecuencia/nivel de prueba de ficha, C/ESR/dispersion; polaridad y tension | LAB-01/06; no ensayar ruptura ni megohmetro sobre circuitos montados; C0G/NP0 y corriente RF segun ficha |
| Inductores/ferritas | LCR compensado open/short del fixture, L/Q/DCR a frecuencia indicada; caracterizacion RF/SRF con fixture apto si necesaria | LAB-01/04; no extrapolar un L medido a 1 kHz hasta 435 MHz ni rating termico por tamano |
| Diodos, LED, TVS, FET e IC discretos | Pinout/serie, prueba estatica de baja energia dentro de ratings y circuito funcional con fuente limitada | LAB-01/07/17; no activar avalancha de TVS ni buscar tension destructiva como ensayo de recepcion |
| Fusibles, seta, contactor, guard y arnes | Continuidad sin energia, calibre de cable, polaridad, fijacion y rating DC; caida por contacto a corriente autorizada y apertura por fixture | PWR/LAB-07/17; fusible no se quema como prueba ordinaria, contacto pegado se simula sin puentear seguridades |
| Conectores y cable RF | Inspeccion centro/genero, continuidad segun circuito, S11/S21 y estabilidad de conexion/flexion controlada | LAB-01/04/18; no asumir SMA nominal soporta el peor caso del montaje |
| Hibridos, baluns, diplexor, filtro | Matriz RF, cargas en puertos no medidos, fase/reparto y potencia posterior dentro de rating | LAB-04/05/18/19; nunca VNA durante TX |
| Rele/conmutador/limitador/LNA/PA | Ficha exacta y banco pasivo/control primero, luego activo con niveles protegidos | LAB-15 a 20; desconocido/no retornado -> PA inhibido |
| DC-DC, bateria, cargador | Bateria/cargador compatibles segun fabricante, inspeccion, fuente/carga protegidas, tensiones/consumo/ripple/temperatura/Wh | LAB-07/23; no cortocircuito, perforacion, descarga profunda o carga fuera de ficha; bateria dañada se segrega |
| Motor/driver/disipador | Modelo/Rsense, bobinas desconectadas para DCR, alimentacion y RMS fase con sonda apropiada, fallo simulado/temperatura | DRV/LAB-08; no extraer motor energizado ni tocar puente con masa de sonda comun |
| Encoder/mux/expansor/final/IMU/GNSS | Identidad y buses aislados, calibracion comparada, rangos y fallos inyectados en fixture | SNS/LAB-09 a 11; no programar OTP ni asumir ACK como identidad |
| PCB/modulo/CM5/ESP32/SDR/USB | Revision/huella/orientacion/continuidad sin energia y puerta PCB; luego rails/USB/config/funcion con logs | PCB/SW/RAD/LAB-07/22; placas HOLD no se energizan |
| Audio, microfono, altavoz, codec y Bluetooth | Identidad/impedancia/niveles compatibles; tono/loopback y nivel sin clipping; latencia/perdidas y aislamiento | RAD/APP/LAB-22; no conectar salida de altavoz a entrada microfono sin adaptacion |
| ASA/carcasa/engranaje/correa/eje/rodamiento/fijacion | Cotas y cupones, orientacion/capas, acceso, retencion, alineacion, holgura y esfuerzo autorizado por fixture | MEC/LAB-12/13; no homologar por STL ni inventar pares de apriete |
| Conductor, manguito, malla, soporte de antena | Diametro/longitud/radio/paso, continuidad/uniones y cada bloqueo; inspeccion antes/despues de ciclos, RF del conjunto | LAB-03/13/18/21; no inferir ganancia ni potencia de DC continua |
| Tripode/montura/retencion/funda | Rating/cotas/acceso, CG/masa y envolvente real con accesorios; estabilidad en zona restringida, sin provocar vuelco | MEC/LAB-13/23; sin viento/carga suspendida no autorizados |
| Herramienta/patron/consumible | Identidad, rango, certificado o lote/caducidad, compatibilidad material/adhesivo y uso prescrito | LAB-01/02/06/12/14; no es pieza a sumar al peso de estacion; no aprobar patron contra si mismo |
| Software/OS/app/archivos | Hash/config/variante y reproduccion del comportamiento con hardware real cuando aplique | SW/APP/SYS/LAB-22/24; logs sin secretos, simulacion no equivale a prueba fisica |

Para LCR, registrar modelo/serie/fixture, compensacion open/short, frecuencia,
nivel, modo serie/paralelo y patrones de verificacion en el inventario de
equipos (añadir fila). Sin LCR o fixture apto dejar C/L/Q no medidos.
Pruebas de aislamiento de red o de seguridad electrica de un equipo
comercial alimentado por red pertenecen a personal competente y normativa
especifica; no abrir fuentes de red ni introducir pruebas de alta tension
en este banco de baja tension.

## LAB-06: DMM, fuente, osciloscopio, corriente y temperatura

- **DMM/fuente/carga:** serie y certificado; comprobar cero, puntas y
  fusible del DMM. Comparar 3,3/5/12 V en vacio y carga con referencia
  calibrada adecuada; registrar caida en cables y corriente limite
  verificada con carga electronica. 0,2 A es solo exploracion de un
  bloque sin CM5/SDR/motores, no corriente de arranque suficiente de todo.
  No usar modo A en paralelo a la fuente ni modo ohm sobre circuito vivo.
- **Corriente:** cero de pinza DC o sonda; corriente RMS de fase de motor
  PWM/chopper necesita sonda/ancho de banda/metodo apropiados. Corriente
  DC de entrada no es corriente de fase y DMM ordinario puede engañar.
  Comparar con patron/shunt caracterizado sin cambiar la puesta a masa.
- **Osciloscopio:** autocal, compensacion de sonda y factor x1/x10 en
  ambos extremos; verificar amplitud/tiempo con referencia. Para ripple
  registrar ancho de banda, acoplamiento, muestreo y masa corta.
  La pinza de masa de una sonda normal puede cortocircuitar un puente:
  usar diferencial/aislada con ratings adecuados; no levantar tierra
  de proteccion del osciloscopio.
- **Termopar/termica:** comparar con referencia en puntos que abarquen
  el uso; fijar contacto y emisividad/reflejos. IR sobre aluminio brillante
  no equivale a temperatura interna. Registrar T_ambiente, T_pieza,
  incremento y tiempo. No tocar para juzgar «caliente».
- **Logica:** umbrales 3,3 V y masa comun segura; verificar timebase y
  frecuencia de muestreo contra reloj conocido. Un analizador de 24 MS/s
  no prueba tiempos de cualquier SPI rapido.

Sin patron/certificado suficiente, etiquetar verificacion funcional limitada
y no emitir conformidad cuantitativa fuera de la incertidumbre conocida.

## LAB-07/08: energia, protecciones, drivers y guard

1. Con circuito sin energia verificar polaridad, continuidad, fusibles,
   pinout y ausencia de cortos; cableado contra esquema aprobado y
   seccion/ratings reales. No usar diodo/LED como sustituto de comprobar
   polaridad ni como proteccion de un CM5 completo.
2. Cargar cada rail desde vacio a uso autorizado; medir en bornes del DUT
   reposo/arranque/parada, corriente y transitorios. Tolerancia +/-5%
   es criterio propuesto, prevalece el intervalo mas estricto del fabricante.
3. ESTOP/watchdog: carga retenida, primero indicadores/cargas ficticias,
   despues motores sin antena. Medir EN, bus, tiempo de corte y estado.
   <1 V en VMOT no demuestra inmovilidad: EL debe retenerse mecanicamente.
4. Retirar fusible/conectar simulador de cable abierto **sin energia**,
   nunca sacar portafusibles de potencia vivos. Simular fallo sin provocar
   sobretemperatura real ni desconectar fases energizadas.
5. Driver: obtener Rsense/modelo exactos, calcular RMS segun ficha y
   documentar IRUN/IHOLD, microsteps y modo. Medir corriente de fase
   con sonda adecuada, comparar +/-10% propuesto sin exceder rating.
   EN alto se confirma por nivel/corriente/estado: el cogging mecanico
   puede existir sin corriente y giro manual no prueba inhibicion.
6. Registrar firmware/config y restauracion segura tras fallo. Ejecutar
   por cada AZ/EL/POL montado; ESP32 y CM5 usan drivers/interfaces
   distintos. No aplicar un pin BCM a un ESP32 por copiar formulario.

## LAB-09: encoders, imanes, finales NC y bus

- Calibrar goniómetro/comparador de referencia antes de ajustar encoder.
  Marcar cero mecanico retenido y comprobar sentido; no cargar offset
  anterior de otro montaje.
- AS5600: MD/ML/MH y AGC en giro completo; registrar gap, centrado, serie,
  canal del mux y alimentacion. Evitar programacion OTP irreversible:
  offsets de trabajo en configuracion reversible.
- Medir al menos 8 posiciones en ambos sentidos, tres repeticiones,
  evitar discontinuidad 359°/0° restando como angulo circular. Calcular
  error, histeresis, RMS y maximo; comparar <=0,5° propuesto para sensor,
  incertidumbre compatible, distinto de precision del rotor completo.
- I2C: seleccionar un canal a la vez y alimentar/aislar cada sensor para
  identificarlo. Dos dispositivos con la misma direccion **pueden
  responder al mismo ACK**: escaneo no demuestra unicidad ni fallo.
- NC: apertura, cable roto, corto simulado por fixture autorizado y
  contacto pegado. Confirmar nivel sano/fallo y respuesta segura por eje.
  NC solo no detecta todos los cortos; documentar cobertura y timeout.

## LAB-10: GNSS, UTC, PPS y referencia de frecuencia

Guardar coordenadas, datum, altura elipsoidal/ortometrica y unidades;
no intercambiar metros/kilometros. Cielo abierto, antena y alimentacion
segun ficha; registrar fix, satelites, precision reportada, arranque frio/
caliente y edad de dato. Comparar UTC/PPS con referencia independiente;
NMEA por UART tiene latencia y no es PPS. Registrar timebase, lock,
leap seconds segun receptor y edad del TLE. No exigir precision de tiempo
inferior a lo que permite el montaje. Sin UTC valida no liberar tracking.

## LAB-11: brujula/IMU y norte verdadero

En montaje completo, lejos de acero/corriente, nivelar y efectuar
calibracion hard/soft iron siguiendo fabricante. Registrar offsets/matriz,
version y orientacion de ejes. Comparar con norte verdadero independiente
(levantamiento/linea conocida), declinacion y fecha/fuente; no confundir
norte magnetico con verdadero. GNSS estacionario de una sola antena
no da rumbo. Repetir motores/DC-DC encendidos y posiciones del rotor:
documentar interferencia, no «calibrar fuera» un campo variable.

## LAB-12/13: metrologia y piezas mecanicas

- Calibre/micrometro: limpiar, comprobar cero y bloques/anillos conocidos
  en rango; no corregir escala total por un solo agujero.
- Bascula: cero/tara y masas de referencia en varios puntos incluyendo
  carga de uso; resolucion no es exactitud. Medir unidades repetidas.
- Comparador/goniómetro: verificar referencia en posiciones conocidas,
  perpendicularidad/radio efectivo. Para holgura por desplazamiento,
  `angulo=atan(desplazamiento/radio)` en radianes; registrar geometria,
  sentido y fuerza aplicada. No empujar un brazo sin retener carga.
- Llave dinamometrica: certificado/rango y par requerido de tornillo,
  inserto y material. No inventar un par para ASA; usar cupon y revision
  estructural. Tornillo/tuerca de potencia no se aprieta «hasta que ceda».
- Conductores/empalmes: calibre, plantilla por banda, radio/helice/paso,
  continuidad y resistencia de contacto (cuatro hilos si es necesaria
  baja resistencia). Ohmios DC no prueban baja perdida RF.
- PF: pivote/bloqueo separados, malla, 50 ciclos y repetibilidad; EB/QFH:
  sectores identificados y radios preservados; revisar tras rearmar.
  Pesar la antena completa/CG, no sumar solo tubos del CAD.
- Motor/transmision: relacion por conteo real, giro manual sin energia,
  alineacion, holgura, retencion y luego carga progresiva de hasta
  objetivo autorizado. No doblar antenas reales para simular viento.

## LAB-22/23/24: audio, SDR, software y conjunto

- Dos SDR: serie fija VHF/UHF y readback de reloj/tasa/frecuencia;
  usar senal independiente para error Hz/ppm tras warm-up, no el mismo
  oscilador como fuente y referencia. Registrar overruns/drops.
- Audio: tono/WAV conocido, nivel RMS/FS, clipping, sample rate y ruta;
  loopback calibrado con generador/analizador si se mide distorsion.
  Bluetooth introduce latencia: medir extremo a extremo con reloj
  comun o metodo sincronizado; repetir perdidas/reconexion por banda.
- Software/OS/app: hash exacto, modelo/OS telefono, versiones,
  permisos, errores y logs sin secretos; ACK no prueba movimiento/PTT.
  No confundir un test simulado con prueba real de hardware.
- Conjunto: referencia externa de AZ/EL en >=10 posiciones ambos sentidos,
  error circular AZ, RMS/max y tiempos. Homing primero sin antena.
  Limites se fijan por fixture y cableado seguros, no por maxima vuelta
  que deje la aplicacion. Objetivo <=2° RMS y <=5° maximo en G1.
- Autonomia: registrar bateria, tension, corriente, Wh, temperatura y
  duty cycle de RX/motores/TX medido; no extrapolar dos horas desde
  consumo en reposo. Masa <=5 kg excluyendo solo bateria externa.
  Repetir norte/UTC tras mover el tripode. TX en campo solo con
  aceptacion de emisiones/protecciones/licencia/exposicion y estado SAT.
