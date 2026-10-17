# Modulo independiente: antena portable 145/435 MHz

Requisito actualizado: [comunicaciones AMSAT y techo de 25 W](SATELLITE-COMMS.md).
Aplica a PF-01, Eggbeater y QFH TX/RX con previo solo en RX y bypass
protegido. Es un techo de diseno pendiente de cualificacion, no potencia
autorizada del hardware ni consigna habitual de operacion.

Elegir entre las [tres alternativas](ANTENNA-OPTIONS.md):
[PF-01](ANTENNA-PORTABLE.md), [Eggbeater](ANTENNA-EGGBEATER.md) y
[QFH](ANTENNA-QFH.md). Guia comun de
[previos RX y proteccion TX](ANTENNA-PREAMPS.md).

## Candidata de rediseno PF-01

El [diseno PF-01](ANTENNA-PORTABLE.md) desarrolla la nueva alternativa
portable con un solo boom, cassettes plegables y puntas VHF desmontables.
Ver [BOM independiente](../bom/antenna-portable.csv) y
[vista de transporte](assembly/portable/PF-folded.svg).
Las instrucciones siguientes describen la antena anterior de dos booms;
no mezclar cortes, articulaciones ni puente de esa variante con PF-01.
Ninguna de las dos tiene aceptacion RF/fisica implicita.

## Alcance y dependencias

Se puede construir la antena sin rotor, CM5, SDR, bateria ni app.
Un soporte manual/tripode y radio externa con interfaces compatibles
permiten operarla por separado. No se anuncian prestaciones SATCOM
comerciales ni ganancia/polarizacion medidas.

| Necesario | Opcional |
| --- | --- |
| Piezas ASA, conductores de ambas bandas, boom/soportes, fijaciones metalicas y coaxial SMA 50 ohm | Rotor AZ/EL/POL |
| Cables con alivio de tension, conectores y montura manual comprobada | Radio SDR integrada |
| Instrumentos/cargas para ajuste y ensayo RF | Diplexor, redes circular y conmutacion RHCP/LHCP tras cualificacion |

Geometria y materiales: [MECHANICAL.md](MECHANICAL.md),
[RF-AND-RADIO.md](RF-AND-RADIO.md), [CAD](../cad/) y
[BOM mecanica](../bom/mechanical.csv). No sumar la BOM completa del
rotor para obtener el coste de antena: seleccionar solo piezas de este modulo.
Los precios fechados y las categorias pendientes estan en
[REFERENCE-PRICES.md](REFERENCE-PRICES.md) y
[reference-prices.csv](../bom/reference-prices.csv). Para antena sola usar
ASA, RF-INTERCONNECT, RF-FILTER si procede, fijaciones de HARDWARE y
consumibles: no comprar CM5/SDR/motores por seguir este recorrido.
La cantidad consumida de ASA y los conductores/coaxiales necesitan
cotizacion y reconciliacion con las piezas concretas; no hay total cerrado.

## Montaje independiente paso a paso

1. Revisar bandas/frecuencias autorizadas, versiones CAD y cotas de
   conductores. Las longitudes calculadas son iniciales para ajuste.
2. Imprimir piezas ASA y comprobar fisuras, alojamientos y ajuste;
   conductores/ejes/fijaciones y roscas de carga deben ser metalicos.
3. Montar boom, soportes y elementos VHF/UHF desmontables siguiendo
   [manual mecanico](MECHANICAL.md). No cortar todos los elementos al
   minimo antes de ensayar el ejemplar.
4. Preparar alimentacion de cada banda, cables SMA convencional 50 ohm,
   fijacion y alivio de tension. Verificar contacto central/genero, no RP-SMA.
5. Probar plegado y montaje manual sin tirar de coaxiales ni usar los
   conectores como soportes. Registrar masa y CG de la antena ensamblada.
6. Ajustar/medir cada banda con VNA y luego el conjunto, con puertos
   no usados correctamente terminados. Registrar ROE y acoplamiento.
7. Si se incorpora circular, montar redes por banda, medir fase/amplitud,
   mano y relacion axial. Giro mecanico no selecciona RHCP/LHCP.
8. Conectar radio externa solo despues de ensayos, comenzar a minima
   potencia y comprobar temperatura/ROE; no probar TX sin carga adecuada.

## Configuracion y aceptacion

La antena sola no requiere software. Documentar frecuencia, modo, mano
circular si procede, cableado y limites medidos antes de transmitir.
[ACCEPTANCE.md](ACCEPTANCE.md) define puertas RF/mecanicas; ninguna STL
correcta demuestra ganancia, ROE o resistencia al viento.
El interfaz del rotor es desmontable, no requisito de funcionamiento.
