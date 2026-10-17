# NanoVNA: procedimiento de banco de pequena senal

Aplicable a LAB-02 a 05 y LAB-15, ANT-01 a 05. Registrar **modelo exacto,
serie, firmware y manual**: NanoVNA, H/H4, V2 y derivados no tienen el
mismo rango, nivel, dinamica ni menu. Se usan nombres funcionales, no
una secuencia de botones inventada. Consultar el manual del ejemplar.
Este protocolo no cambia sus ratings.

## 1. Seguridad y limites del instrumento

1. PA, transceptor y bias-tee desconectados fisicamente. Descargar
   condensadores mediante el procedimiento del DUT; comprobar con DMM
   ausencia de DC en todos los puertos antes de conectar. Apagar un
   transceptor sin desconectarlo no basta.
2. LNA activo no se conecta hasta tener ganancia, alimentacion y potencia
   maxima del receptor VNA verificadas; usar [banco RX](11-rf-potencia.md).
3. Confirmar conectores convencionales de 50 ohm y genero. No forzar
   SMA/RP-SMA; usar llave y par del fabricante, no un valor universal.
   Inspeccionar centros, kit, coax y adaptadores; evitar descargas ESD.
4. Habitualmente CH0/PORT1 es emision/reflexion y CH1/PORT2 recepcion.
   Identificar en el manual: no conectar suponiendo etiquetas iguales.
   Muchos NanoVNA miden solo **S11/S21 en sentido directo**, no S22/S12
   simultaneos ni todos los errores de un VNA de dos puertos completo.

## 2. Elegir barrido y plano de referencia

- Calentar/estabilizar segun manual y registrar tiempo, bateria/fuente
  y temperatura. Fijar nivel de excitacion si es configurable, puntos,
  promediado/ancho de banda si disponibles. Registrar todo.
- Barrido inicial separado 144-146 MHz y 430-440 MHz; hacer primero
  exploracion mas amplia si la resonancia esta fuera. Refinar en cada
  canal y su Doppler calculado. No ajustar solo a 145/435 MHz.
- Registrar f_inicio, f_fin, N y paso `Delta f=(f_fin-f_inicio)/(N-1)`.
  Un barrido UHF de 10 MHz/101 puntos tiene paso 100 kHz: no caracteriza
  por si solo un canal SSB ni localiza finamente un minimo.
  Elegir el paso segun ancho del detalle y repetir mas estrecho.
- Plano: extremos de los cables/adaptadores que tocaran el DUT.
  Dibujar y fotografiar. Todo adaptador añadido tras calibrar introduce
  error; recalibrar. Port extension no elimina perdida, mal matching
  o error de un adaptador desconocido.

## 3. Calibracion SOL y respuesta THRU

Anotar ID de calibracion en `calibraciones.csv`; guardar estado/memoria
y parametros. Se necesitan **OPEN, SHORT y LOAD conocidos** con modelo
apropiado del kit. Un tapon sin centro no es una carga.

1. Resetear/cancelar correccion anterior segun manual.
2. Conectar OPEN en el plano PORT1, adquirir; retirar sin mover cables.
3. Conectar SHORT, adquirir; retirar.
4. Conectar LOAD 50 ohm, adquirir. No tocar los contactos ni dejar
   un adaptador suelto en el plano.
5. Si el modelo soporta aislamiento, seguir su manual con terminaciones
   independientes. No fabricar una correccion ISOLN conectando ambos
   puertos a una T. Registrar si se omitio/no soporta.
6. Para transmision, unir extremos PORT1/PORT2 con THRU conocido.
   Registrar su longitud, adaptadores y si se normaliza a 0 dB/fase cero
   o se usa un modelo de thru. Ejecutar THRU/DONE/SAVE segun manual.
7. Confirmar correccion activa y rango/puntos. Cambiar rango, cables,
   conexion, temperatura significativamente o condiciones de medida
   exige nueva verificacion y, si procede, recalibracion. No asumir que
   una interpolacion de memoria conserva precision.

En un NanoVNA simple esto es SOL de reflexion y normalizacion/correccion
de transmision segun su firmware: **no anunciar SOLT completo de dos
puertos** sin que el instrumento lo implemente.

## 4. Verificacion independiente antes y despues

Conservar «as found», ajustes y «as left». No basta con volver a medir
la misma LOAD usada para calibrar: es una comprobacion interna, no
validacion independiente. Utilizar carga/patron distinto caracterizado
y atenuador de referencia con incertidumbre conocida a ambas bandas.

| Comprobacion | Conexion y lectura | Decision |
| --- | --- | --- |
| Carga independiente | S11 complejo, retorno y ROE por frecuencia | Comparar con certificado/caracterizacion + incertidumbre y tolerancia aprobada |
| Atenuador independiente | PORT1 -> atenuador -> PORT2; S21 magnitud/fase si conocida | Comparar perdida a 145 y 435 y canales extremos; no solo DC |
| THRU de comprobacion | S21 y fase, sin modificar correccion | Residual frente a modelo; no «exactamente cero» por definicion |
| Repetibilidad | Tres desconexiones/conexiones del patron | Registrar dispersion; no flexionar cables despues de calibrar |
| Suelo de fuga/ruido | Puertos separados y terminados, mismo barrido | Registrar por banda y repetir con disposicion real de cables |

Si faltan patrones independientes, registrar **verificacion limitada**,
no trazabilidad acreditada. Definir tolerancias antes del ensayo. Si
falla verificacion posterior, poner en cuarentena las medidas desde
la ultima verificacion valida y repetirlas tras resolver la causa.

## 5. Medidas pasivas

### Antena, redes y coax (LAB-03/04)

`PORT1 -> cable calibrado -> DUT`; para S21, DUT entre ambos puertos.
Terminar a 50 ohm todos los otros puertos con cargas caracterizadas.
Radio y LNA desconectados. Montar la antena en configuracion real,
lejos de personas/metal no representativos, con separacion registrada,
coax inmovil y motor parado; repetir si cambia soporte/rotor.

1. Medir cada puerto equilibrado mediante su balun/matching real;
   no conectar un brazo suelto y declarar impedancia de la antena.
   Un reflector pasivo sin alimentacion no tiene «S11 de puerto»
   medible directamente: medir continuidad/geometria y efecto instalado.
2. Exportar barrido complejo `.s1p`; anotar ROE/retorno en canales,
   centro, minimo y bordes. Una foto del minimo no prueba cobertura.
3. Para coax, insertar cable entre puertos calibrados: medir S21 con
   referencia adecuada y retorno, repetir en posiciones de giro seguras.
   Invertir fisicamente el DUT y recalibrar/verificar el nuevo plano si
   se necesita reflexion del otro extremo. Etiquetar sentido.
4. Comparar antena antes/despues de 50 ciclos de plegado/rearmado;
   inspeccion, continuidad y posicion de minimo. El criterio propuesto
   de variacion de ROE <0,1 requiere incertidumbre compatible.

### Diplexor y filtros (LAB-04)

En tres puertos medir: comun -> VHF (UHF terminada), comun -> UHF
(VHF terminada), VHF -> UHF (comun terminado), y S11 de cada puerto
con los otros terminados. Registrar matriz/etiquetas, f y sentidos;
un `.s2p` en un par no describe los tres puertos.

Usar criterios G2: insercion <=1 dB, retorno >=14 dB y aislamiento
>=40 dB como cribado; no garantizan RX simultaneo ni 25 W.
Si fuga/ruido y rango dinamico no permiten medir 40/60 dB con margen
evaluado, resultado **INDETERMINADO o limite de medida**, nunca un
valor preciso debajo del suelo del equipo.

### Hibrido/red de fase (LAB-05)

Hibrido de cuatro puertos: identificar entrada, A, B y aislado mediante
ficha; terminar los dos no conectados en cada medida. Medir S21 hacia A
y hacia B con **mismo cable de recepcion/plano** sin cambiar el otro
camino. Registrar fase compleja y perdida en cada canal.

Cada medida del camino se refiere al mismo THRU/estado de calibracion.
Desenrollar fase para continuidad y calcular diferencia modulo 360°,
seleccionando signo/convenio. No restar valores de fase envuelta a
ciegas cerca de +/-180°. Diferencia de perdida A/B <=0,5 dB y fase
90° +/-5° son objetivos G2, **no prueba de mano ni relacion axial**.
Verificar carga aislada y peor disipacion en otro ensayo de potencia.
Un hibrido ideal reparte -3,01 dB a cada salida: no confundir reparto
con perdida excedente.

## 6. Formulas, exportacion y limitaciones

`RL=-20 log10(|S11|)`, `ROE=(1+|S11|)/(1-|S11|)`,
`IL=-20 log10(|S21|)` en dB. Si |S11|>=1 o IL negativa en un DUT
pasivo, revisar calibracion/ruido antes de declarar ganancia.
ROE 1,5 equivale a retorno 13,98 dB; ROE 2 a 9,54 dB.
Un corto DC puede ser normal en ciertas antenas/baluns: usar el circuito,
no rechazar por regla universal «antena = circuito abierto».

Guardar barridos con modelo, plano, calibracion y puertos en nombre/metadata.
No presentar como medido un S12/S22 que el software haya copiado suponiendo
reciprocidad. Guardar datos realmente disponibles y reconectar para otros
sentidos. Ningun barrido de pequena senal valida calentamiento, 25 W,
ganancia radiada, figura de ruido, circular o espurios.
