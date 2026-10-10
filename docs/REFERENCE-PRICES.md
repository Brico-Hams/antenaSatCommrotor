# Precios de referencia y presupuesto abierto

## Alcance y metodo

La tabla persistente es [reference-prices.csv](../bom/reference-prices.csv).
Fecha de recopilacion: **2026-10-10**. Son observaciones publicas orientativas,
no ofertas vinculantes ni garantia de disponibilidad. No se han enviado
archivos del proyecto a un fabricante para obtener una cotizacion.

`unit_reference_eur` es la referencia unitaria. `mean_eur` solo se rellena
cuando hay dos observaciones comparables del mismo componente. Una observacion
no es un promedio de mercado. Las cotizaciones agotadas se indican y no
constituyen una cesta comprable. Campos vacios significan **pendiente**, no
cero. Un precio conocido sin cantidad aprobada tampoco da un coste de linea.

Conversion registrada por la investigacion: EUR1 = USD1.1206 y GBP0.84763,
[referencia BCE](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml)
de 2026-10-09, consultada el 2026-10-10. El enlace diario es mutable: comprobar
fecha y tasa nuevamente antes de comprar. No incluye comision de cambio,
IVA de importacion, aduanas ni portes. Las referencias alemanas con IVA
conocido se dividen por 1.19; las espanolas por 1.21. No se descuenta un IVA
cuya inclusion no se ha confirmado.

## Referencias principales

| ID | Cantidad de referencia | EUR/unidad | Base |
| --- | ---: | ---: | --- |
| CM5 | 1 | 115.67 | Media de dos cotizaciones sin IVA; una no disponible |
| CM5IO | 1 | 18.40 | Una observacion sin IVA |
| SDR | 2 | 535.43 | USD600 por LimeSDR Mini; antes de impuestos de importacion |
| DRV | 3 | 15.97 | TMC5160 v1.5; sin IVA |
| ENC | 3 | 5.31 | AS5600; antes de impuestos de importacion |
| COMPASS | 1 | 8.88 | LIS3MDL; antes de impuestos de importacion |
| IMU | 1 | 10.33 | Media normalizada; una tienda agotada |
| GPS | 1 | 25.93 | Media normalizada |
| ASA | 1 bobina de referencia | 23.46 | Media sin IVA; consumo real pendiente |
| BAT | 1 externa | 99.99 | Precio mostrado; inclusion de IVA no confirmada |
| PP-PACK | 1 paquete de referencia | 15.16 | Diez extremos completos rojo/negro; antes de importacion |
| PP-TOOL | 1 herramienta opcional | 35.69 | Crimpadora reutilizable; presupuesto separado |

El subconjunto CM5, CM5IO, dos SDR, tres drivers, tres encoders, brujula,
IMU y GPS suma **1313.90 EUR**, normalizado sin IVA. Con una bobina ASA
de referencia suma **1337.35 EUR**. Estos son subtotales alternativos, no
sumandos. **No son el precio de la estacion completa.** La bateria de
99.99 EUR se mantiene separada por tener base fiscal no confirmada.
Las cifras CSV conservan decimales para el calculo; redondear al final.

Quedan sin cotizacion completa: PA lineales, filtros/diplexor y conmutacion
RF, coaxiales/SMA, motores y transmision mecanica, tripode, tornilleria,
auxiliar PCB/PCBA, convertidores, arneses y fusibles seleccionados, cargador,
interconexiones USB3, audio/K1, consumibles y herramientas de medida.
La tabla incluye filas pendientes para estas categorias: no ocultarlas
sumando solo las filas con precio.

## Energia externa, Powerpole y fusibles

La bateria elegida es ECO-WORTHY variante **40308275183822**, SKU
**DE-L13060202003-1**, un paquete sin cargador. La ficha publica indica
12.8 V, 30 Ah, 360 Wh, 3.55 kg, dimensiones 183 x 176 x 83 mm y bornes M5.
12.8 x 30 = **384 Wh**, distinto de los 360 Wh publicados. Para planificacion
se conserva el valor menor, 360 Wh; ninguno demuestra energia util medida.
Publica carga/descarga maxima de 30 A y tension maxima de carga 14.6 V;
no se atribuyen umbrales ni duraciones de pico de otros modelos de BMS.
Carga 0 a 55 C y descarga -20 a 55 C; no se ha demostrado corte automatico
por frio.

Solo la bateria externa se excluye del objetivo de **5 kg** de la estacion.
Su masa sigue formando parte del peso transportado y su coste del presupuesto.
Tripode, cables, radio, conectores y filtros instalados siguen incluidos.
La autonomia de dos horas debe medirse con el ciclo RX/TX y motores reales.

WP30-10 contiene diez extremos rojo/negro completos y veinte contactos:
cinco parejas acopladas. Una pareja requiere dos extremos; no sumar paquete
y asignaciones de sus mismos contactos. Usar herramienta y cable compatibles
con los contactos exactos. Instalar fusible maestro cerca del positivo de
bateria y fusibles de ramas de computo, motores y RF. El BMS no sustituye
estos fusibles. Los ejemplos comerciales de 5 A o 15 A **no fijan**
las intensidades aprobadas: seleccionar por cable, corriente normal,
arranque, temperatura y capacidad de interrupcion DC.

## USB-C y filtrado EMI

El alimentador de red Raspberry Pi 27 W es solo una referencia de banco;
no resuelve la alimentacion desde bateria. La fuente USB-C debe proporcionar
el perfil compatible 5 V/5 A y su cable debe calificarse. Un trigger PD
receptor no es una fuente USB-C y no autoriza aplicar 9-20 V a CM5IO.

El toroide tipo31 2631801202 cuesta como referencia **2.56 EUR sin IVA**
por nucleo, no por choque terminado. Cuatro a ocho nucleos costarian
10.24-20.48 EUR antes de impuestos/portes, pero no constituyen un presupuesto
EMI completo ni una seleccion de cantidad. Choques de modo comun, ferritas
de abrazadera y LC diferencial amortiguado siguen opcionales/pending-DNP.
Calificar DCR, corriente, desequilibrio/saturacion, temperatura, frecuencia,
caida de tension y estabilidad del convertidor. Comparar ruido RX y espurias
TX con y sin filtro; incluir el peso instalado en los 5 kg.

## Compras por modulo

Usar los recorridos [antena](MODULE-ANTENNA.md), [rotor](MODULE-ROTOR.md),
[radio](MODULE-RADIO.md) e [integrado](MODULE-INTEGRATED.md). Sus BOM locales
son listas de componentes, no cestas independientes que deban sumarse sin
revision: en el integrado se cuenta CM5/CM5IO una vez y se asignan las piezas
compartidas a un unico modulo. Las alternativas, herramientas y referencias
opcionales no se agregan automaticamente al subtotal seleccionado.

Para cerrar presupuesto, fijar MPN/revision, cantidad por paso de montaje,
unidades consumidas frente a paquetes comprados, disponibilidad, IVA y
portes de cada pedido. Registrar proveedor y fecha y reconciliar las BOM
locales con esta tabla. Hasta entonces el coste total permanece **abierto**.
