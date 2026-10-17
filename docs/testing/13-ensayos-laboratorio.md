# Ensayos suplementarios de laboratorio

Estas fichas amplian los PWR/DRV/SNS/PCB/MEC/ANT/RAD/SW/APP/SYS existentes.
Todos comienzan PENDIENTES. Los detalles de conexion, calibracion y parada
estan en [expediente](09-laboratorio.md), [NanoVNA](10-nanovna.md),
[RF activa](11-rf-potencia.md) y [calibraciones](12-calibraciones.md).
No ejecutar una etapa si la anterior no esta aceptada y autorizada.
Cada repeticion/unidad/puerto/canal necesita fila nueva; los limites
pendientes se resuelven antes de aplicar carga o emitir conformidad.

### LAB-01
- **Acción:** Recepcion sin energia de cada unidad seleccionada: identificar BOM/fabricante/modelo/revision/serie, fotos, daños, pinout, dimensiones, polaridad, ratings y continuidad contra circuito; excluir variantes no montadas con motivo firmado.
- **Esperado:** Identidad trazable y asignacion de ensayos por funcion para todas las unidades.
- **Criterio de aprobación:** Sin identidad/rating/asignacion pendiente; no aceptar componentes HOLD ni equivalencias sin revision. Piezas con daños o discrepancias se segregan.
- **Procedimiento:** 09-laboratorio.md, secciones 1 a 4; 12-calibraciones.md segun familia.

### LAB-02
- **Acción:** Identificar NanoVNA/firmware, rango, kit y plano; estabilizar, SOL y THRU segun modelo; verificar con patrones independientes en ambas bandas, tres reconexiones y verificacion posterior.
- **Esperado:** Calibracion identificada, dispersion y suelo de medida documentados.
- **Criterio de aprobación:** Error/incertidumbre dentro de tolerancias predefinidas de los patrones; si falta verificacion independiente indicar limitada; no emitir conformidad fuera de la capacidad demostrada.
- **Procedimiento:** 10-nanovna.md, secciones 1 a 4.

### LAB-03
- **Acción:** NanoVNA sin PA/DC: medir S11 de cada puerto alimentado con matching/balun y conjunto instalado, barridos 144-146/430-440 y canales con Doppler; repetir tras montaje y 50 ciclos.
- **Esperado:** S1P, ROE/retorno por canal, frecuencia minima y repetibilidad por alternativa/banda/puerto.
- **Criterio de aprobación:** G2: ROE <=1,5 en central elegida y <=2 en canales; incertidumbre y banda documentadas. Reflector sin puerto no tiene S11 propio. No inferir ganancia/circular.
- **Procedimiento:** 10-nanovna.md, secciones 2, 5 y 6; ANT-02/05.

### LAB-04
- **Acción:** Medir coaxiales, conectores, baluns, filtros y diplexor pasivos: S11 y S21 por ruta, puertos restantes terminados, sentido/plano registrado; repetir rutas inversas por reconexion.
- **Esperado:** Matriz por frecuencia con insercion, retorno, fuga y ficheros originales.
- **Criterio de aprobación:** Ficha de cada componente; para diplexor G2 <=1 dB insercion, >=14 dB retorno y >=40 dB aislamiento como cribado; no aceptar fuga bajo suelo de medida ni extrapolar 25 W.
- **Procedimiento:** 10-nanovna.md, secciones 4 a 6.

### LAB-05
- **Acción:** Hibrido/red de fase por banda: mismo plano/cable, medir entrada-A y entrada-B con otros puertos terminados; registrar fase compleja y reparto; verificar aislado.
- **Esperado:** Diferencia de amplitud/fase por canal y criterio de terminacion del aislado.
- **Criterio de aprobación:** G2 <=0,5 dB desequilibrio y 90 grados +/-5 grados, con signo/convenio e incertidumbre; sin inferir RHCP/LHCP ni 25 W.
- **Procedimiento:** 10-nanovna.md, seccion 5; 11-rf-potencia.md para potencia posterior.

### LAB-06
- **Acción:** Verificar DMM, fuente/carga, osciloscopio/sondas, corriente y temperatura con patrones en rango de uso; documentar antes, ajustes y despues.
- **Esperado:** Certificados/verificaciones, errores, correcciones, U/k y vigencia registrados.
- **Criterio de aprobación:** Dentro de tolerancias fijadas para la medida; instrumento sin capacidad suficiente queda excluido de conformidad cuantitativa.
- **Procedimiento:** 12-calibraciones.md, LAB-06.

### LAB-07
- **Acción:** Ensayar alimentacion, fusibles/conectores/DC-DC y cadena ESTOP/watchdog en circuito autorizado; cargas ficticias primero, rails/transitorios/tiempos y temperatura despues.
- **Esperado:** Limite de corriente y corte independientes, logica viva, rearme manual, ningun arranque intempestivo.
- **Criterio de aprobación:** PWR/G1E y limites de ficha confirmados; seguridad sin fallo; cortar ante corriente/temperatura/retorno anomalo. No energizar auxiliar HOLD.
- **Procedimiento:** 12-calibraciones.md, LAB-07/08; 02-electronica.md PWR.

### LAB-08
- **Acción:** Por driver y motor: identificar Rsense, corriente nominal y modo; verificar EN/estado, medir corriente RMS de fase con equipo apropiado, conteo de vueltas, fallos seguros y temperatura.
- **Esperado:** Corriente, configuracion, relacion y trazas por AZ/EL/POL; sin confundir corriente DC de entrada con fase.
- **Criterio de aprobación:** DRV y ratings; corriente +/-10% propuesto sin exceder nominal, inhibicion demostrada y sin rearme automatico. No desconectar fases con energia.
- **Procedimiento:** 12-calibraciones.md, LAB-07/08; 02-electronica.md DRV.

### LAB-09
- **Acción:** Por encoder/iman/mux/final: identificar canal/serie, STATUS y gap; comparar ocho posiciones ambos sentidos y tres repeticiones; simular NC abierto/pegado/cable roto por fixture seguro.
- **Esperado:** Curva error/histeresis y diagnostico por unidad; bus identifica sensores por aislamiento individual, no solo ACK.
- **Criterio de aprobación:** Error sensor <=0,5 grados propuesto con U compatible, campo valido y fallos detectados segun contrato; no escribir OTP.
- **Procedimiento:** 12-calibraciones.md, LAB-09; 02-electronica.md SNS.

### LAB-10
- **Acción:** GNSS/PPS/UTC: comparar fix y tiempos con referencia independiente, registrar datum/altura/unidades, lock y latencias; probar perdida de fix/UTC y reanudacion controlada.
- **Esperado:** Errores de posicion/tiempo y comportamiento sin referencia valida documentados.
- **Criterio de aprobación:** Tolerancias de receptor y tracking aprobadas antes; ningun seguimiento con UTC invalida, ni rumbo supuesto desde GNSS estacionario.
- **Procedimiento:** 12-calibraciones.md, LAB-10.

### LAB-11
- **Acción:** Nivelar IMU/brujula, calibrar hard/soft iron segun fabricante, registrar matriz/ejes y comparar norte verdadero externo con motores/DC-DC apagados y activos.
- **Esperado:** Error de rumbo por orientacion, interferencia y parametros reversibles registrados.
- **Criterio de aprobación:** Presupuesto de error de rumbo definido y cumplido; referencia independiente/declinacion documentadas; repetir tras cambio de montaje/ubicacion.
- **Procedimiento:** 12-calibraciones.md, LAB-11.

### LAB-12
- **Acción:** Verificar calibre, comparador, goniómetro, bascula y llave de par con referencias apropiadas; medir cero, puntos de uso y repetibilidad.
- **Esperado:** Correcciones/U/vigencia y aptitud para tolerancias del DUT.
- **Criterio de aprobación:** Instrumentos capaces y limites de par/cotas aprobados; resolucion sola no implica exactitud.
- **Procedimiento:** 12-calibraciones.md, LAB-12/13.

### LAB-13
- **Acción:** Por ASA, rodamiento, eje, correa/polea, fijacion, tripode y antena: inspeccion/cotas, retencion, giro sin energia, holgura, CG, masa, envolvente y rearmado; carga progresiva retenida.
- **Esperado:** Medidas por pieza/unidad y montaje; geometria RF repetible sin cable como soporte.
- **Criterio de aprobación:** Planos/tolerancias revisados y MEC/G1; objetivo antena <=0,5 kg y CG <=30 mm sin aumentar carga autorizada; no viento/sobrecarga sin plan especifico.
- **Procedimiento:** 12-calibraciones.md, LAB-12/13; 04-mecanica.md y guia de antena elegida.

### LAB-14
- **Acción:** Calibrar/verificar cadena generador, frecuencia, vatimetro/acoplador, atenuadores/cables/carga y analizador a fundamental/armonicos; documentar montaje, correcciones y presupuesto maximo de entrada.
- **Esperado:** Potencia conocida en plano DUT y proteccion termica/electrica de todo el camino.
- **Criterio de aprobación:** Ratings/margenes y tolerancias aprobados; no conectar TX si falta presupuesto o carga; sin NanoVNA en camino de TX.
- **Procedimiento:** 11-rf-potencia.md, seccion 1.

### LAB-15
- **Acción:** Conmutadores/bypass sin PA: medir rutas de insercion, retorno y aislamiento en estados RX/TX/seguro mediante fuente pequena senal y puertos terminados; caracterizar suelo.
- **Esperado:** Matriz RF por banda, posicion y sentido con realimentacion real.
- **Criterio de aprobación:** Ratings y presupuesto de aislamiento aplicables; ruido/fuga del instrumento no cuenta como aislamiento demostrado; potencia pendiente de ensayo posterior.
- **Procedimiento:** 10-nanovna.md, secciones 4 a 6; 11-rf-potencia.md, seccion 6.

### LAB-16
- **Acción:** Previo/filtro/limitador/receptor por banda: alimentar con fuente limitada, ganancia a nivel conocido, consumo/temperatura, sensibilidad y recuperacion; NF solo con equipo/metodo calibrados.
- **Esperado:** Ganancia/sensibilidad por canal, estabilidad y ruido con motores/DC-DC; NF NO_MEDIDA si no hay cadena apta.
- **Criterio de aprobación:** Fichas/requisitos aprobados, sin compresion/oscillacion ni sobrepasar entrada; no sustituir NF por ganancia.
- **Procedimiento:** 11-rf-potencia.md, seccion 2.

### LAB-17
- **Acción:** Secuenciador/PTT/guard con PA desconectado: capturar peticion, inhibicion, contactos y LNA en transiciones; reset/watchdog/retorno pegado/abierto/alimentacion perdida/PTT retenido.
- **Esperado:** Tabla temporal de cada fallo, break-before-make y PA siempre inhibido sin camino seguro.
- **Criterio de aprobación:** Todos los fallos seguros y tiempos fijados por fichas/medidas; rearme manual, sin VOX unico ni permiso basado solo en ACK.
- **Procedimiento:** 11-rf-potencia.md, seccion 3.

### LAB-18
- **Acción:** TX en carga dimensionada: escalones 1/5/10/25 W solo dentro del menor rating aprobado; registrar directa/reflejada, DC, temperaturas, duty cycle, duracion y comprobacion pasiva tras enfriar.
- **Esperado:** Curvas termicas y potencia por banda/etapa; ningun paso al escalon siguiente sin revision.
- **Criterio de aprobación:** Potencia <=25 W FM/CW o PEP SSB y menor limite de la cadena; ROE/temperatura dentro de ratings; sin ensayo sobre satelite.
- **Procedimiento:** 11-rf-potencia.md, seccion 4.

### LAB-19
- **Acción:** En carga y cadena protegida: fundamental/armonicos/espurios, desviacion FM, PEP/IMD de dos tonos SSB, LSB/USB y envolvente AM si aplica; verificar no sobrecarga del analizador.
- **Esperado:** Espectros y ajustes completos, niveles corregidos por frecuencia, banda ocupada y linealidad.
- **Criterio de aprobación:** Normativa/licencia/operador y limites de diseno previamente citados; sin criterio o equipo capaz no emitir aprobado.
- **Procedimiento:** 11-rf-potencia.md, seccion 5.

### LAB-20
- **Acción:** Medir fuga TX->RX primero con detector protegido en lugar de LNA, ambas direcciones y armonicos; despues sensibilidad simultanea con inyeccion protegida y nivel deseado constante.
- **Esperado:** Aislamiento, margen de dano/compresion y desensibilizacion por banda/configuracion.
- **Criterio de aprobación:** Presupuesto con ratings reales y criterio RX aprobado cumplidos; no conectar receptor ni anunciar full-duplex si la proteccion no esta demostrada.
- **Procedimiento:** 11-rf-potencia.md, seccion 6.

### LAB-21
- **Acción:** En campo/camara autorizados: patron, ganancia por sustitucion si existe referencia y relacion axial por polarizacion lineal giratoria; mano con referencia circular conocida, varias direcciones.
- **Esperado:** Diagramas por frecuencia/orientacion, entorno/distancia y correcciones/incertidumbre.
- **Criterio de aprobación:** G2 relacion axial <=3 dB en direcciones declaradas para circular; sin referencia apropiada ganancia/mano NO_MEDIDAS, no inferidas de S11.
- **Procedimiento:** 11-rf-potencia.md, seccion 7.

### LAB-22
- **Acción:** Dos SDR/audio: verificar series, reloj/tasa/frecuencia con senal externa; loopback/tono/WAV y niveles, clipping, latencia, muestras perdidas, reconexion y demodulacion por banda.
- **Esperado:** Lecturas de hardware y registros temporales/audio sin confundir RX simultaneos.
- **Criterio de aprobación:** RAD y requisitos de audio aprobados; 10 min sin perdidas/underruns como objetivo; sin PTT habilitado por una prueba de RX.
- **Procedimiento:** 12-calibraciones.md, LAB-22/23/24; 05-rf-y-radio.md RAD.

### LAB-23
- **Acción:** Integracion real: norte/UTC, >=10 posiciones ambos sentidos, seguimiento, masa/autonomia de dos horas con duty cycle registrado; probar fallos con carga retenida y TX inhibido.
- **Esperado:** Error RMS/max, tiempos, Wh, masa operativa y ausencia de movimiento inseguro.
- **Criterio de aprobación:** G1/G3: <=2 grados RMS, <=5 maximo; masa <=5 kg excluyendo solo bateria externa y dos horas medidas; nuevos lugares exigen orientacion/calibracion.
- **Procedimiento:** 12-calibraciones.md, LAB-22/23/24; 08-sistema.md.

### LAB-24
- **Acción:** Revisar cobertura por todas las unidades seleccionadas, calibraciones antes/despues, evidencias/hash, desviaciones y resultados; firmar alcance de liberacion por variante, banda, potencia y configuracion.
- **Esperado:** Expediente reproducible con fallos y repeticiones preservados; exclusiones justificadas.
- **Criterio de aprobación:** Ningun pendiente/bloqueado/indeterminado en alcance liberado; G0-G4 y autorizaciones cerradas por responsables. Un formulario generado no aprueba hardware.
- **Procedimiento:** 09-laboratorio.md, secciones 1 a 4; ACCEPTANCE.md.
