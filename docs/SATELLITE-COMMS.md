# BricoHams: comunicaciones satelitales y techo de 25 W

Consulta de fuentes: **2026-10-17**. Requisito de diseno, no certificado
de potencia ni autorizacion de transmision. Aplica a PF-01 y a las
alternativas Eggbeater y QFH solicitadas, todas con alcance TX/RX.
Las alternativas no quedan construidas o validadas por figurar aqui.

## 1. Fuentes primarias comprobadas

- [AMSAT: repetidores FM](https://www.amsat.org/live-fm-satellites/),
  pagina fechada 2026-07-10.
- [AMSAT: transpondedores lineales](https://www.amsat.org/live-linear-satellites/),
  pagina fechada 2026-03-24.
- [AMSAT: estado comunicado por operadores](https://www.amsat.org/status/).
  No es una garantia de activacion en el siguiente pase.
- [AMSAT: buenas practicas FM](https://www.amsat.org/fm-satellites-good-operating-practices-for-beginning-and-experienced-operators/).

La antigua pagina de comunicaciones de AMSAT esta marcada como obsoleta
desde 2025-05-28. Usar los listados anteriores y comprobar estado, horarios
y restricciones del operador antes de cada pase. Esta consulta comprueba
frecuencias publicadas; **no confirma actividad actual de cada satelite**.
Para ISS, el listado AMSAT remite ademas al
[estado de estaciones ARISS](https://www.ariss.org/current-status-of-iss-stations.html).
No se ha recuperado contenido operativo legible de esa pagina en esta
consulta, por lo que no se afirma su modo activo.

## 2. Repetidores FM: ejemplos de referencia, no presets habilitados

Subida significa Tierra -> satelite; bajada, satelite -> Tierra.
Frecuencias nominales, sin correccion Doppler:

| Satelite | Subida MHz | Bajada MHz | Acceso/condicion publicada por AMSAT |
| --- | ---: | ---: | --- |
| SO-50 | 145.850 FM | 436.795 FM | CTCSS 67 Hz; temporizador de 10 minutos, armado con portadora de 2 s y CTCSS 74,4 Hz cuando proceda |
| ISS | 145.990 FM | 437.800 FM | CTCSS 67 Hz; verificar modo/estado AMSAT y ARISS |
| AO-91 | 435.250 FM | 145.960 FM | No intentar acceso en eclipse por el estado de bateria; la fila consultada no especifica tono |
| AO-123 | 145.850 FM | 435.400 FM | CTCSS 67 Hz |
| IO-86 | 145.880 FM | 435.880 FM | CTCSS 88,5 Hz; horario y orbita de baja inclinacion |
| PO-101 | 437.500 FM | 145.900 FM | CTCSS 141,3 Hz; por horario y con advertencia de deterioro en el listado |

No sustituir el tono desconocido por cero ni habilitar TX automaticamente
con esta tabla. Obtener la ficha operativa completa del satelite elegido.
La disponibilidad depende tambien del lugar, elevacion y pase.
APRS/packet, telemetria y SSTV son servicios distintos: no usar sus
frecuencias como repetidor de voz ni transmitir sobre balizas.

## 3. Transpondedores lineales

Son bandas compartidas de SSB/CW, no un unico canal FM. Ejemplos publicados:

| Satelite/modo | Subida MHz / modo | Bajada MHz / modo | Condicion publicada |
| --- | --- | --- | --- |
| AO-7 B | 432.125-432.175 LSB | 145.925-145.975 USB | Inversor; solo con luz solar y segun modo |
| AO-73 | 435.130-435.150 LSB | 145.950-145.970 USB | Inversor; activo en eclipse, comprobar horario |
| FO-29 | 145.900-146.000 LSB | 435.800-435.900 USB | Inversor; activacion por horario y tension disponible |
| JO-97 | 435.100-435.120 LSB | 145.855-145.875 USB | Inversor; el listado indica telemetria inoperativa |
| RS-44 | 145.935-145.995 LSB | 435.610-435.670 USB | Inversor; baliza CW separada en 435.605 MHz |

En un transpondedor inversor, al aumentar la subida disminuye la bajada:
en el marco del satelite, f_bajada = f_bajada_max -
(f_subida - f_subida_min). Aplicar despues el Doppler de cada enlace.
No emparejar ambos extremos inferiores. Para RS-44, los centros nominales
son 145.965/435.640 MHz. Elegir un punto libre y evitar bordes/balizas;
el centro es ejemplo aritmetico, no canal reservado de llamada.

**USB solamente en TX no cubre estos ejemplos**: hace falta LSB en subida
y USB en bajada, o conversion IQ equivalente validada. AM no se adopta
como modo habitual en estos transpondedores; no usar FM en una banda
lineal salvo autorizacion expresa del operador.

## 4. Bandas, seguimiento y polarizacion

- Los ejemplos seleccionados requieren VHF aproximadamente 145,850-146,000
  MHz y UHF 432,125-437,800 MHz, segun el sentido TX/RX de cada fila.
  Son extremos de la muestra, **no un permiso para transmitir en todo
  ese intervalo** ni una especificacion exhaustiva de todos los satelites.
- Para diseno y barridos, mantener la cobertura objetivo del proyecto
  **144-146 y 430-440 MHz**, midiendo los canales realmente elegidos y
  dejando margen para Doppler. Las longitudes iniciales 145/435 MHz no
  prueban ROE, relacion axial o adaptacion en todo ese rango.
- V/u indica subida VHF/bajada UHF; U/v, lo contrario.
  AO-7 A necesita bajada de 29 MHz; QO-100, 2,4/10 GHz: quedan fuera
  de estas antenas V/U aunque aparezcan en AMSAT.
- Como orden de magnitud calculado, a 7,5 km/s de velocidad radial
  el desplazamiento es unos 3,6 kHz a 145 MHz y 10,9 kHz a 435 MHz.
  No es el Doppler de un pase concreto: calcularlo con TLE, UTC y sitio.
  Corregir ambos enlaces; los saltos de canal FM no sirven como control
  fino de SSB.
- Favorecer escucha de la bajada durante TX, con aislamiento demostrado.
  Un diplexor o dos VFO no convierten por si solos un equipo en full-duplex.
- Medir mano circular, fase y relacion axial por banda. Ni la forma
  Eggbeater/QFH ni girar POL garantizan RHCP/LHCP. El reflector plegable
  PF-01 requiere medir patron y acoplamiento con ambas bandas instaladas.

## 5. Potencia: techo solicitado, no consigna de operacion

Se adopta **25 W maximos conducidos a la salida de la cadena TX**,
con una sola cadena transmitiendo a la vez. No son 25 W por dipolo ni
50 W agregados. Aplicar ademas el menor limite entre licencia/regulacion,
operador del satelite y cada componente realmente cualificado.
EIRP/ERP requiere anadir ganancia y restar perdidas: 25 W conducidos
no limitan por si solos la potencia radiada equivalente.

| Modo | Interpretacion del techo de diseno |
| --- | --- |
| FM/CW | <=25 W de portadora; dimensionar potencia continua y ciclo de trabajo |
| SSB | <=25 W PEP, con PA lineal, control de drive y ensayo de IMD |
| AM, solo donde este autorizado | <=6,25 W de portadora a 100% de modulacion para no superar 25 W PEP ideales; comprobar picos reales |

Los antiguos 5 W FM/5 W PEP SSB y 1 W de portadora AM quedan como
referencias conservadoras de diseno/ensayo, **tampoco capacidades medidas**.
No se eleva ningun limite del firmware ni se habilita un PA por editar
esta guia. El sistema permanece sin permiso TX hasta superar las puertas
fisicas de [aceptacion](ACCEPTANCE.md).

AMSAT recomienda la minima potencia necesaria y senala que, en general,
5 W de un portatil con antena direccional bastan para FM. Es orientacion,
no garantia de enlace ni potencia obligatoria. No compensar un fallo de
apuntamiento, polarizacion o recepcion subiendo directamente a 25 W.
No transmitir sin oir el satelite y compartir el pase.

## 6. Previo solo RX y cadena de potencia pendiente

Cada banda necesita su propio preselector/LNA RX. La rama TX debe
**puentear fisicamente el LNA** mediante conmutacion RF apropiada:

```text
SDR TX -> PA -> filtro de salida -> via TX del conmutador -> antena
SDR RX <- proteccion <- LNA <- preselector <- via RX del conmutador
```

Es un esquema funcional, no circuito fabricable. Inhibir el PA antes de
conmutar, usar break-before-make, desconectar/terminar el LNA en TX,
apagar su alimentacion y confirmar posicion real antes de permitir PTT.
Apagar el LNA **no protege por si solo** su entrada. Ante fallo de control,
alimentacion o retorno, mantener PA inhibido; no conmutar con RF presente.
Durante TX VHF/RX UHF simultaneo, proteger tambien el LNA de la otra banda:
no basta con desconectar solo el previo de la banda que transmite.

Numeros calculados para 25 W sobre 50 ohm adaptados:

- 43,98 dBm; 35,36 V RMS, 50 V pico, 0,707 A RMS y 1 A pico.
  No son tensiones maximas internas de una red reactiva ni bajo ROE.
- Con solo 35 dB de aislamiento quedarian +8,98 dBm, unos 7,9 mW,
  en el puerto protegido antes de otras perdidas: no se declara seguro.
- Ejemplo **hipotetico**, LNA que tolere -10 dBm y margen de 6 dB:
  aislamiento requerido >=43,98 - (-10) + 6 = **59,98 dB**.
  Reemplazar por los ratings reales y medir todos los caminos de fuga.
  La desensibilizacion puede exigir mucho mas que evitar danos.

No seleccionar un rele/LNA sin ficha que cubra frecuencia, potencia,
aislamiento, ROE, transitorios y ciclo de trabajo. Recalificar coaxiales,
conectores, baluns, redes de fase, empalmes plegables y carga del puerto
aislado para el peor caso. Los ratings de potencia continua y PEP no
son intercambiables.

El [diplexor QRP y los hibridos estudiados](RF-AND-RADIO.md) **no estan
aprobados para 25 W**. Los valores publicados de 5-10 W del diplexor y
la referencia de 15 W del QCN3 no sirven como permiso a 25 W; QCN-3+
tampoco cubre 145 MHz. No basta con aumentar el rating de una resistencia.
Tambien sigue pendiente demostrar rechazo del tercer armonico VHF
que puede entrar en UHF, bloqueo y recepcion simultanea.

La seleccion de PA, disipacion, bateria y autonomia requiere revision:
25 W de RF no equivalen a 25 W de consumo electrico. Mantener HOLD
de TX hasta seleccionar componentes y ensayar en carga, con escalones
de potencia dentro de los ratings confirmados y sin pruebas de potencia
sobre el satelite.
