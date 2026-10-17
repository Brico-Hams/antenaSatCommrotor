# RF, polarización y RT-3S: arquitectura y límites verificables

Fecha2026-10-10. Fuentes/versiones en [SOURCES.md](SOURCES.md); análisis de PDF en [REFERENCE-ANALYSIS.md](REFERENCE-ANALYSIS.md). Objetivo nominal145/435MHz, no homologación del conjunto.

**Actualización 2026-10-17:** [contraste AMSAT y techo solicitado de
25 W](SATELLITE-COMMS.md). Los ratings y ensayos históricos siguientes
no se elevan automáticamente: este diplexor QRP y los híbridos citados
no están aprobados para 25 W. Revisar toda la cadena y el bypass del
previo RX antes de seleccionar componentes.

## Tres conceptos diferentes

| Elemento | Función | Lo que NO demuestra |
|---|---|---|
| **Diplexor**, tres puertos | Un puerto común de50Ω y dos ramas por banda: VHF y UHF; filtros paso bajo/paso alto | No genera polarización circular; no añade un segundo receptor al radio |
| **Operación full-duplex** | Recepción durante transmisión, con radio/radios y aislamiento suficientes | Dos frecuencias programadas o dual-watch no bastan |
| **Híbrido de90°**, cuatro puertos eléctricos | Alimenta dos dipolos/planos ortogonales con amplitud y fase adecuadas dentro de su banda; cuarto puerto aislado terminado | No separa145/435MHz y no da buena relación axial fuera de banda |

El repositorio se llama duplexor-spacequad, pero su README describe eléctricamente un **diplexor**. No inferir «full duplex» de su nombre.

## Topología propuesta, sin suponer circular ni recepción simultánea

```text
RT-3S: único puerto RF
           |
    diplexor 145/435 opcional, solo después de ensayar el ejemplar
       |                                      |
   rama VHF                              rama UHF
       |                                      |
   antena VHF                             antena UHF
   (lineal inicial)                       (lineal inicial)
```

Si se adopta circular: **cada** rama necesita dos planos ortogonales y su propia red de fase caracterizada, o desplazamiento físico/fase eléctrica diseñado y ensayado conjuntamente. Un solo híbrido SATCOM sin banda conocida no se pone antes del diplexor para «hacer circular ambas bandas».

La orientación de dipolos y los puertos determina mano RHCP/LHCP. Documentar convención de observación y verificar experimentalmente; no basta con el color del coaxial. Circular↔lineal ideal cuesta3dB; circular de mano opuesta ideal no tiene una pérdida universal de3dB.

## D — Red exacta del proyecto público del usuario

Revisión `f5c7dc375ed7b9882f52bd7757deaf44cd422b81`, README/BOM:

| Rama / referencia | Valores de la revisión recomendada |
|---|---|
| VHF paso bajo | L1/L3=68nH; L2=100nH; C1/C2=18pF |
| UHF paso alto | L4/L5=15nH; **C3/C5=8.2pF; C4=4.7pF** |
| UHF esquema histórico | C3/C5=4.7pF; C4=2.7pF: no confundir con optimizados |
| Componentes |0805; inductores altaQ (ejemplos0805CS-680XJL/101XJL/150XJL); condensadores C0G/NP0≥100V |
| PCB |2capas FR4 de1.6mm, cobre1oz; autor declara CPWG50Ω, pista1.4mm, hueco a masa0.25mm |
| Banda objetivo |144–146MHz y430–440MHz |

El autor indica ambigüedad10/18pF del esquema original para C1/C2 y elige18pF. No mezclar BOM histórica y optimizada. Tolerancias, Q, ESR, SRF, corriente y parásitos de la PCB no están verificados aquí contra fichas de componentes.

### Simulación NO es medición

README atribuye a simulación **ideal** optimizada S11≈−31dB a145/435MHz, inserción<0.05dB y aislamiento>49dB. No convertirlos en especificaciones garantizadas ni llamar compatible el diplexor con esta nueva antena/radio.

`docs/PRUEBAS.md` establece como objetivos físicos:

| Medición, otro puerto terminado50Ω | Criterio de la fuente |
|---|---|
| S11 puerto RADIO, ramas terminadas |<−15dB en144–146 y430–440MHz |
| RADIO→VHF |Inserción<0.5dB a145; rechazo>35dB a435MHz |
| RADIO→UHF |Inserción<0.7dB a435; rechazo>35dB a145MHz |
| VHF→UHF, RADIO terminado |Aislamiento>35dB en ambas bandas |
| Potencia con carga/vatímetro |Escalones1→5→10W, ROE estable, sin calentamiento apreciable |

Son **criterios pendientes**, no resultados. No se ejecuta10W sin confirmar primero ratings del ejemplar, conectores, inductores, condensadores, carga y disipación. «Sin calentamiento apreciable» es insuficiente como calificación: registrar temperatura, tiempo/ciclo de trabajo, potencia y ROE.

0805 no significa por sí solo potencia garantizada. El README afirma **unos5–10W** para portátiles/QRP y recomienda bobinas al aire/condensadores apropiados para mayor potencia. La aceptación del nuevo conjunto comienza a mínima potencia; el valor10W no es un límite certificado. Un condensador100V tampoco garantiza corriente RF, ni un inductor de altaQ garantiza no calentarse.

**Orden de magnitud:** a5W sobre50Ω se tienen15.8V RMS y22.4V pico antes de considerar ROE/red reactiva. Si hubiera35dB de aislamiento,5W≈37dBm dejarían aproximadamente2dBm en la rama opuesta, antes de otros filtros/pérdidas. Eso puede ser enorme frente a una señal satelital. No aprobar un futuro receptor/LNA por una cifra aislada de rechazo ni asumir que simulación de un filtro prueba desensibilización real.

La caja de plástico **no apantalla**. Planos de masa/vías ayudan pero no sustituyen un blindaje RF. Cinta/pintura conductora exige unión eléctrica continua, separación segura de nodos, verificación de aislamiento y ensayo posterior; no declarar una caja ASA estanca ni blindada sin pruebas.

### Geometría publicada EXACTA y bloqueo mecánico

| Interfaz publicada | SMA | BNC |
|---|---:|---:|
| PCB |37×23mm |55.5×33mm |
| Caja exterior |**45.2×27.6×14.1mm** |**59.9×37.6×23.5mm** |
| Conector |Amphenol132289, canto/bulkhead |AmphenolB6252HB-NPP3G-50, acodado PCB |
| Fijación |2×M2×10autorroscantes |2×M2×12autorroscantes |
| Taladros PCB |2×Ø2.2mm, metalizados a masa |2×Ø2.2mm, metalizados a masa |

Parámetros de `docs/MONTAJE.md`: SMA brida9.6mm de ancho y1.9mm espesor, eje «PCB+0.4mm», paso6.8mm para rosca1/4″-36. BNC cuerpo14.8mm sobre PCB, eje «PCB+7.5mm», frontal14.9mm. Pared/suelo/techo2.0/2.0/1.6mm; holgura labio0.15mm. Patillas BNC≤2.5mm bajo PCB.

**El README dice expresamente que las medidas de conectores son estimaciones desde huellas KiCad.** Los exteriores anteriores son los publicados, no mediciones del hardware del usuario. Medir caja y conectores reales con calibre; no atribuir a «PCB+» un origen de altura del nuevo soporte sin revisar sección CAD. Probar base antes de tapa final.

Mantener soporte paramétrico/abrazadera que no cargue conectores, acceso a tornillos y separación de electrónica/motores. El envolvente necesita **además** espacio para tuerca, acoplamiento BNC, plug SMA, alivio de tensión y radio mínimo de coaxial según fabricante. Esas reservas no están incluidas automáticamente en las dimensiones exteriores. No inventar coordenadas de taladros; recuperar `board_geometry.json` si se pretende apoyo directo a PCB y contrastarlo con el ejemplar.

## H/M — Híbridos: selección pendiente por banda, no por potencia

| Candidato de H | Afirmación de README | Evidencia fabricante conseguida | Decisión |
|---|---|---|---|
| CMX03A03 |200W + carga G150N50Ω |No se obtuvo ficha de banda/potencia legible |No seleccionar para145/435MHz |
| «RF Power», supuesto Florida RF Labs |200W, identidad incierta |No modelo inequívoco/ficha |Excluir de BOM de compra |
| Anaren10260-3 |250W, antiguo |No ficha legible en esta consulta |Banda y límites pendientes; no certificar |
| QCN3, escrito QCN-3 en BOM |15W, dos resistencias100Ω2512 de2W |Mini-Circuits **QCN-3+** declara **220–470MHz** |435MHz dentro de banda declarada; **145MHz fuera**. Identificar sufijo/ejemplar; no adoptar como dualband |

No se confirma la hipótesis225–400MHz para QCN-3+: la fuente del fabricante consultada dice220–470MHz. Tampoco se extrapola automáticamente al componente sin sufijo o a una copia vendida en marketplace. La banda nominal no demuestra por sí sola pérdida/fase aceptable en435MHz bajo nuestras cargas.

**Bug real de H:** enlace SMA bajo QCN3 apunta a `GERBER-CmxSma.zip`. No fabricar ese archivo como si fuera placa QCN3.

Dos100Ω en paralelo son50Ω nominales y4W de suma nominal, **no una carga RF validada** ni demostración de soporte15W. El puerto aislado puede absorber potencia significativa con cargas desadaptadas y, como límite conservador, dimensionarse para el peor caso de la red. Confirmar disipación, montaje, impedancia hasta435MHz, rating y temperatura. Una carga150W en aire sin disipador apropiado tampoco equivale a150W reales continuos.

## O0/O1 — Qué puede hacer realmente el RT-3S con OpenGD77

La guía antigua solicitada O0 solo acredita VFO con TX/RX diferentes para cross-band/split; no acredita RT-3S ni pantalla satélite actual. La guía mantenida O1 (`2289ba75…`,2026-03-10) sí enumera **MD-UV380(RT-3S)** y documenta:

1. **Satellite Screen:** predice próximos24h a partir de ubicación, fecha y hora; muestra AZ/EL y corrige automáticamente Doppler de **frecuencias TX y RX**.
2. El usuario debe introducir ubicación y fecha/hora y cargar **Keps por CPS**. Cargar Keps recientes también ajusta fecha/hora.
3. RT-3S/UV380 tiene RTC según esa guía, pero eso no demuestra exactitud actual ni batería/estado del ejemplar.
4. Frecuencias y CTCSS se cargan con los datos de CPS; cambios requieren editar los datos/satellites.txt del CPS correspondiente.
5. SO-50: SK1 durante TX aplica tono de armado según la guía; verificar estado/modo vigente.
6. Pantalla live ofrece tipos1FM Voice,2APRS,3Beacon; beacon no permite TX. No significa que todo satellite de la tabla local sea compatible con el radio.
7. «Sat / Manual» frente a«Auto» controla cambio al siguiente satélite después de LOS. **Manual aquí no significa necesariamente que Doppler sea manual.** Distinguir selección de satélite y ajuste de frecuencia.

### Plan de uso sin CAT inventado

- Registrar modelo/build de firmware y versión de CPS; guardar codeplug y configuración. Confirmar que el menú Satellite aparece y calcula correctamente en el radio real.
- Cargar Keps/datos con CPS en preparación; sincronizar UTC/ubicación del RT-3S y del controlador. El AP del rotor **no carga el CPS por magia**.
- Rotor calcula SGP4 y mueve AZ/EL autónomamente. RT-3S se maneja por teclado/PTT y usa su Doppler integrado si el build soporta lo descrito. Alternativa: presets/ajuste manual de Doppler si no está disponible.
- Comparar predicción/tiempo/frecuencias en ambos; diferencias en TLE, UTC o ubicación producen desalineación aunque cada pantalla funcione.
- No se ha verificado **CAT RT-3S**, protocolo USB de control en vivo, PTT remoto, full-duplex ni recepción durante TX. No implementarlos usando comandos de Yaesu/IC-820H ni una API imaginaria.
- No confundir DMR, hotspot digital o programación CPS con un puerto CAT satelital. No prometer SSB/CW con este portátil FM/DMR.

## Plan mínimo de aceptación física

1. **Documentación/cables:** identificar componentes reales, pinout/puertos, conectores, factor de velocidad y radio mínimo del coaxial. Inspección/continuidad sin alimentar.
2. **Antenas individuales:** VNA calibrado en plano de referencia real; medirS11 y ancho de banda sobre el soporte final, con coaxial ordenado. Registrar estado de plegado y proximidad a rotor.
3. **Diplexor separado:** SOL/through; barrido100–500MHz≥401puntos; cargas50Ω en puertos libres; medir todas las rutas/reflexiones. Guardar Touchstone, fotos, fecha y configuración. Comprobar ruido de fondo/dynamic range antes de atribuir35dB de aislamiento.
4. **Red de polarización, si existe:** pérdida, diferencia de amplitud/fase, adaptación y puerto aislado para cada banda. Prueba radiada de mano/relación axial/patrón con método y geometría definidos.
5. **Montaje completo:** medir adaptación/interacción entre antenas, aislación de banda y efecto del cable al variar AZ/EL. Repetir después de cambios de soporte/coaxial.
6. **Potencia sobre carga:** empezar bajo; subir solo dentro del rating demostrado. Temperatura/ROE/tiempo y peor desadaptación tolerada según componentes; no transmitir a antena durante puesta a punto indiscriminada.
7. **EMI de motores:** comparar recepción con drivers apagados/hold/movimiento, DC/DC y AP funcionando. Reubicar/filtrar si aparece ruido.
8. **Operación:** primero paso de recepción; verificar satélite/modo vigente, autorizaciones y potencia mínima razonable. No «ensayar aislamiento» saturando un LNA/receptor.

Estado actual: **arquitectura justificada, candidatos RF y pruebas definidos; antena/diplexor/híbridos y conjunto radio–rotor aún NO medidos ni aprobados**.

## A — Comparación con la nueva ficha comercial AV2040

La ficha local `TDS_AV2040.pdf`, p. PDF1, identifica una antena **UHF SATCOM plegable/manpack**. La extracción textual pierde cifras por codificación de fuentes; se leyeron visualmente de `TDS_AV2040-000001.png`, renderizado local140dpi. Fabricante Ultralife/Trivec-Avant, **23NOV2010, UBI-05273 REV:-**. Los valores son de la ficha comercial, no mediciones de PortableSatStation.

| Aspecto | Evidencia de ficha A disponible | Consecuencia para PortableSatStation |
|---|---|---|
| Frecuencia145MHz |Banda comercial **240–400MHz** |**145MHz fuera de banda**, no cobertura VHF acreditada |
| Frecuencia435MHz |Banda comercial **240–400MHz** |**435MHz fuera de banda**, no compatibilidad por apariencia SATCOM |
| VSWR |1.5:1 publicado |No extrapolar fuera de banda ni al diseño nuevo |
| Polarización |Circular derecha; relación axial3dB |No garantiza nuestra red de fase ni relación axial |
| Ganancia por versión |2040-3:+7dBic240–400;2040-2:+11dBic240–318;2040-1:+9dBic240–400MHz |No confundir versiones/bandas ni atribuir esos dBic a la antena ASA |
| Potencia |200WattsCW publicados |No es rating de híbridos/PCB/diplexor nuevo |
| Plegado |Descripción de antena plegable/manpack |Es requisito funcional, no licencia ni cota geométrica |
| Dimensiones abierta/plegada |**La página visual no publica cotas dimensionales** |Sin longitudes/anchuras/volumen verificables; no medir una foto como plano |
| Masa |6.5libras≈2.948kg de la ficha |No transferir masa ni centro de gravedad al diseño ASA original |
| Conector |BNCmacho |Comprobar interfaz/latiguillo, no confundir con BNChembra del diplexor |

La frecuencia449.550MHz pertenece al **blog B**, no a la ficha A; está además fuera de la banda240–400MHz comercial declarada. La realización del blog es un diseño distinto reajustado, no una prueba de extensión de banda del AV2040 de fábrica. AV2040 permanece **referencia funcional, no alternativa145/435MHz dentro de especificación**. La foto no tiene cotas de plegado y ningún OBJ/STL de licencia desconocida se distribuye con este proyecto. El pie declara datos de referencia, sin garantía de rendimiento y sujetos a cambio.
