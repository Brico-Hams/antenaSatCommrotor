# Banco RF activo: previos, TX protegido y 25 W

Procedimientos LAB-14 a 21. Operador RF autorizado; componentes exactos,
manuales y ratings aprobados antes de conectar. [Arquitectura](../ANTENNA-PREAMPS.md)
no es un circuito ya cualificado. Prohibido TX al NanoVNA.

## 1. Calibrar la cadena de medida, no solo el instrumento

1. Registrar analizador/generador/vatimetro/acoplador, sensores, cargas,
   atenuadores y cables con serie, rango, certificados y vencimiento.
   Autocal interna segun manual no sustituye calibracion externa.
2. Verificar referencia de frecuencia con patron conocido (10 MHz/GNSSDO
   solo si disponible, estable y dentro de especificacion). Registrar
   error Hz/ppm y estado de lock. No forzar referencia externa incompatible.
3. Verificar generador a nivel seguro con sensor calibrado o receptor
   de medida; caracterizar atenuacion/cables a cada frecuencia.
   Generador sin nivel calibrado permite comparacion relativa, no MDS absoluto.
4. Poner a cero sensor de potencia sin RF y corregir por frecuencia;
   medir insercion/directividad del acoplador y perdida de camino.
   Una buena ROE de la carga no prueba que disipe 25 W.
5. Medir/confirmar atenuacion a las frecuencias de fundamental **y armonicos**.
   Presupuestar entrada del analizador, DC maximo, compresion y transitorios.
   Definir limite de parada y margen antes de habilitar PA.

Ejemplo, no seleccion de piezas: 25 W = 43,98 dBm, atenuador total
de 50 dB -> -6,02 dBm nominales. Con primer escalon de 30 dB,
ese atenuador disipa aproximadamente 24,975 W; uno de «2 W» se destruye
aunque el analizador este protegido nominalmente. Usar rating continuo,
temperatura/disipador, ROE y margen documentados. Si se mide por puerto
acoplado, incluir acoplamiento, directividad y carga del puerto principal:
no mezclar formulas de montaje en linea y acoplado.

```text
PA -> filtro -> acoplador/vatimetro -> carga 50 ohm dimensionada
                       |
             puerto acoplado -> atenuacion/proteccion -> analizador
```

Todos los puertos inutilizados terminados como indique el fabricante.
No mantener un receptor humano expuesto a audio intenso; tampoco
acercar manos/metal a conductores RF energizados.

## 2. LNA y receptor: LAB-16

Montaje de pequena senal: generador -> atenuacion calibrada -> filtro/LNA
-> proteccion/atenuacion de salida -> receptor/medidor. PA desconectado.

1. Verificar polaridad, tension, corriente limite y bias-tee si existe;
   no enviar DC al generador/receptor. Medir consumo, temperatura,
   oscilacion y retorno en condiciones admitidas por el equipo.
2. Comenzar por debajo del nivel lineal seguro del DUT y del equipo.
   Medir ganancia por canales a nivel conocido; restar perdida de caminos.
3. Subir nivel en pasos pequenos dentro del rating aprobado, registrando
   Pin/Pout para evaluar compresion si hay generador/analizador adecuados.
   No buscar punto de dano ni superarlo para «comprobar proteccion».
4. Medir sensibilidad con senal modulada, ancho de banda y criterio fijados
   antes (SINAD FM, SNR/BER segun modo); repetir con LNA en bypass/activo,
   mismo nivel en plano ANT, motores/DC-DC apagados/encendidos.
5. NF absoluta solo con fuente de ruido calibrada y ENR por frecuencia
   o analizador NF/metodo trazable. En Y-factor, usar potencias lineales
   de ruido integradas con igual ancho de banda, no restar dBm como Kelvin.
   Si no hay equipo adecuado, NF = NO_MEDIDA; ganancia no equivale a NF.

No se asigna NF, ganancia o sensibilidad aceptable sin requisito aprobado.
Registrar interferencia por alimentacion, bloqueo y recuperacion.

## 3. Conmutacion fail-safe sin RF: LAB-17

Usar carga simulada de control y PA desconectado/inhibido. Osciloscopio/
analizador logico sobre peticion PTT, permiso real PA, retorno de S1/S2,
alimentacion LNA y, cuando exista, detector de RF.

- Arranque, reset, PTT retenido, watchdog ausente, retorno abierto/pegado,
  alimentacion perdida y restablecida; inyectar fallos por interfaz de
  prueba segura, sin cortar cables vivos ni puentear protecciones.
- Medir tiempos y orden en RX->TX y TX->RX. Confirmar break-before-make,
  asentamiento/contact bounce y PA inhibido durante movimiento.
- Fijar tiempos desde ficha y medida del componente exacto; si no hay
  retorno real ni umbral/tiempo aprovado, BLOQUEADO.
- Ningun reset/reconexion restaura TX automaticamente; registrar todos
  los casos en filas separadas con captura temporal.

Repetir despues con detector/acoplador y potencia minima admitida,
solo si la fase sin RF fue aprobada. Nunca demostrar hot-switch dañando
un rele que no tiene ese rating.

## 4. Potencia, adaptacion y temperatura: LAB-18

No comenzar si filtros, redes de fase, conmutadores, cable, carga o
empalmes tienen rating inferior/desconocido. QRP historico no autoriza 25 W.

1. Revisar carga/enfriamiento, recinto RF, exposicion, fuente/fusible,
   permiso local y parada. Separar NanoVNA y receptores no protegidos.
2. Secuencia propuesta 1 -> 5 -> 10 -> 25 W, **solo escalones menores o
   iguales al limite confirmado**. Si el rating es 5 W, detenerse ahi:
   no completar las otras filas como aprobadas.
3. A cada escalon medir P directa/reflejada, tension/corriente DC,
   tiempo, duty cycle, temperatura ambiente y puntos calientes.
   La duracion se fija con rating y objetivo termico aprobados; no
   declarar «continuo» por 10 s. Mantener hasta condicion de estabilidad
   predefinida sin sobrepasar ningun rating.
4. Calcular `|Gamma|=sqrt(Pr/Pf)` y ROE si vatimetro/directividad permiten.
   Con Pr cerca del suelo del equipo, informar limite/incertidumbre.
5. Parar ante deriva, arco, olor, aumento de reflejada, limite termico,
   corriente anomala, perdida de retorno o refrigeracion. Desenergizar
   antes de tocar/inspeccionar uniones.
6. Repetir mediciones pasivas despues de enfriar; cambios dejan HOLD.
   Una carga resistiva verifica cadena TX, no radiacion ni potencia
   admisible de la antena; probar antena requiere plan posterior autorizado.

## 5. Espectro, SSB y modos: LAB-19

Conectar analizador solo a camino protegido calibrado. Registrar span,
RBW/VBW, detector, promediado, atenuacion, preamp, referencia y niveles.
Elegirlos conforme al metodo normativo y ancho de modulacion.

- Fundamental, armonicos y espurios; corregir perdida de camino a cada
  frecuencia. `P_DUT=P_leida+perdidas`; dBc respecto a fundamental
  igualmente corregida, no respecto a una portadora de otro ajuste.
- Cambiar atenuacion externa y compensarla: un armonico que cambia
  de forma no esperada puede ser generado por sobrecarga del analizador.
  Su filtro o rango insuficiente no prueba ausencia de emisiones.
- SSB: prueba de dos tonos/audio y ganancia lineal, medir IMD y PEP con
  equipo apropiado. No aplicar 25 W de portadora como sustituto de 25 W PEP.
  Comprobar **LSB subida/USB bajada** con senal conocida.
- AM si procede y esta autorizada: portadora <=6,25 W al 100% ideal
  para techo 25 W PEP, medir envolvente/picos reales. FM: desviacion y
  ancho ocupado con modulacion y preenfasis configuradas.

No hay limite universal de armonicos/IMD/desviacion en esta hoja: copiar
normativa de licencia/servicio y requisitos del satelite, con fuente.
Sin limite aplicable o equipo capaz -> BLOQUEADO/INDETERMINADO.

## 6. Aislamiento y desensibilizacion: LAB-20

Primero medir fuga con fuente debil, RX/LNA sustituidos por terminacion
y detector protegido; despues subir en escalones aprobados en recinto/
carga. No usar un LNA como detector de su propia supervivencia.

Registrar fundamental y armonicos en plano RX. Presupuesto:
`A_requerida=P_TX_dBm-P_admisible_dBm+margen_dB`, donde P_admisible
incluye dano, compresion y requisito de recepcion, el menor de ellos.
A 25 W, -10 dBm hipoteticos y margen 6 dB dan 59,98 dB, **no un limite
universal del LNA**. Si el suelo de medida no demuestra el margen,
INDETERMINADO; no sumar ciegamente aislamientos de catalogo.

Para sensibilidad simultanea, usar montaje de inyeccion RF calibrado,
combinador/aisladores/filtros que protejan generador y receptor. Medir
sensibilidad/SNR con PA apagado y encendido, misma senal deseada.
Tercer armonico de VHF puede entrar UHF; medir ambas direcciones y
configuraciones de conmutacion. Si no hay aislamiento demostrado no
se conecta el receptor ni se anuncia full-duplex.

## 7. Patron, mano y relacion axial: LAB-21

No se obtienen del NanoVNA en mesa por una ROE baja. Se requiere campo
de ensayo o camara, antena de referencia y posicionador. Registrar
distancia, alturas, polarizaciones, potencia minima autorizada y entorno.
Condicion geometrica orientativa de campo lejano `R>=2D²/lambda`,
con D del conjunto mayor; no garantiza ausencia de reflexiones.

Con referencia lineal giratoria, medir potencia recibida corregida en
pasos angulares y repetir en elevaciones/azimuts de interes. En montaje
valido, diferencia max/min en dB aproxima relacion axial dB; no confundir
desvanecimiento/multipath con elipse. Esa medida sola **no identifica
RHCP/LHCP**: comparar con referencias de mano conocida, convención de
observacion y orientacion registradas. Ganancia absoluta requiere metodo
de sustitucion calibrado y presupuesto de perdidas/incertidumbre.

Aplicar a PF con/sin malla y a cada EB/QFH con alimentacion/soportes reales.
Objetivo G2: relacion axial <=3 dB hacia el satelite para anunciar circular,
no «en todas direcciones» por medir un solo eje.
