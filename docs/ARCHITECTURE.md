# Arquitectura y registro de decisiones

## Limites del sistema

El objetivo es una estacion amateur de FM en 145/435 MHz, no un terminal
SATCOM comercial ni acceso a satelites militares. Los nombres de las
referencias comerciales no implican sus prestaciones.

> **Variante ESP32 (historica)**: el diagrama siguiente es la primera entrega; ver la matriz de variantes del README. CM5 = ADR-024 a ADR-026.

```text
                         navegador local
                              |
                        Wi-Fi AP / HTTP
                              |
Internet -- STA/TLS --> ESP32 -- SGP4 -- objetivos AZ/EL
TLE manual ----------> cache      ^            |
GNSS UTC/posicion ----------------+       control seguro
norte verdadero + nivel ----------+            |
parada NC / limites / encoders ------------ motores AZ/EL

RT3S -- coax comun -- diplexor RF metalico -- puerto VHF -- red VHF -- antena VHF
                                         -- puerto UHF -- red UHF -- antena UHF
```

Una red de polarizacion circular es otra funcion: hibrido de cuadratura,
dos dipolos ortogonales, alimentacion balanceada y control del sentido.
No sustituye al diplexor. Un unico transceptor half-duplex no se convierte
en full-duplex por combinar dos antenas.

## ADR-001: repositorio separado

**Decision:** repositorio Git local nuevo en Documents, rama main.
**Motivo:** el directorio abierto corresponde a Intune; no hay relacion
funcional y no debe contaminarse.
**Alternativa descartada:** reutilizar el script seleccionado del IDE.
**Consecuencia:** publicacion remota requiere accion posterior. El usuario
eligio MIT para software y CERN-OHL-S-2.0 para hardware original.

## ADR-002: dos bandas electricamente distintas

**Decision:** dos radiadores y redes de adaptacion independientes.
**Motivo:** la relacion de longitudes de onda es 3:1. Un diseno UHF
449,55 MHz escalado una vez no cubre ambas bandas con ROE y patron conocidos.
**Alternativa:** Yagi dualband optimizada por modelado electromagnetico.
**Consecuencia:** mas conexiones; cada puerto se mide primero individualmente
y despues en el ensamblaje completo por acoplamiento mutuo.

## ADR-003: dipolo cruzado con reflector como punto de partida

**Decision:** geometria original parametrica, plegado mecanico y piezas
conductoras desmontables. Las dimensiones empiricas son iniciales.
**Motivo:** coste y volumen inferiores a una Yagi larga de alta ganancia.
**Alternativa:** reutilizar la antena comercial de la captura.
**Consecuencia:** no copiar sus STL ni anunciar su ganancia; la polarizacion
circular y el patron requieren simulacion y ensayos. Si no cumplen,
usar una Yagi ligera externa con el mismo interfaz del rotor.

## ADR-004: interfaces desacopladas

**Decision:** antena con saddle desmontable; rotor acepta booms con
adaptadores y fijacion metalica; radio en base fija; diplexor independiente.
**Motivo:** usar la antena a mano, cambiar por Yagi/SpaceQuad o retirar la radio.
**Consecuencia:** universalidad MECANICA no implica compatibilidad de cargas
o RF. Cada antena externa debe cumplir masa, CG, viento y recorrido.

## ADR-005: NEMA 14 en vez de NEMA 17/23

**Decision del usuario:** priorizar portabilidad con NEMA 14.
**Motivo:** reducir masa, consumo y volumen.
**Consecuencia:** la serie NEMA define la brida, no el par. Deben seleccionarse
motor/driver por curva de par a la velocidad real. La carga queda limitada
por validacion; no se promete mover una SpaceQuad cualquiera.

## ADR-006: dos planetarios 5:1

**Decision:** corona fija, sol de entrada y portasatelites de salida
en cada etapa; total 25:1.
**Motivo:** eje compacto y reduccion distribuida.
**Criterio:** R=S+2P; (S+R)/numero_planetas entero. El calculo base usa
S=18, P=27, R=72 y modulo 1,5, evitando el subcorte de un sol de 12
dientes sin correccion.
**Consecuencia:** diametro primitivo de corona 108 mm; la envolvente supera
este valor. No cabe honestamente en una caja de 60 mm.

## ADR-007: precision real separada de resolucion

**Decision:** feedback/homing y calibracion; microstep nominal 0,0045 grados.
**Motivo:** microstepping no elimina elasticidad, holgura, errores de
magnetos, perdida de pasos ni orientacion inicial.
**Consecuencia:** criterio inicial de precision final <=2 grados RMS en
ensayo lento sin viento; no promesa de ultraprecision.

## ADR-008: ASA no reemplaza al metal

**Decision:** ASA para chasis y engranajes; ejes, tornillos, casquillos,
inserto de tripode y elementos RF metalicos.
**Motivo:** UV y masa favorables; resistencia/fluencia anisotropas.
**Consecuencia:** ajustar tolerancias con cupones, no roscar cargas primarias
en plastico ni considerar ASA un blindaje RF.

## ADR-009: dientes rectos para primera iteracion

**Decision:** priorizar engranajes verificables antes de doble helicoidal.
**Motivo:** impresion y ajuste accesibles; la espina de pescado no garantiza
backlash cero y agrega restricciones de montaje axial.
**Consecuencia:** doble helicoidal queda como variante posterior si mejora
resultados medidos. Los parametros concretos estan en el manual mecanico.

## ADR-010: calculo orbital en ESP32

**Decision del usuario:** SGP4 local, TLE almacenados, reloj y ubicacion validos.
**Motivo:** el navegador puede desconectarse tras iniciar seguimiento.
**Alternativa descartada:** movil/PC enviando cada punto durante el pase.
**Consecuencia:** biblioteca orbital real, presupuesto de RAM, limites de
catalogo y frecuencia de calculo; no sustituir SGP4 por orbita circular.

## ADR-011: AP no equivale a Internet

**Decision:** AP local siempre disponible; STA opcional con acceso a Internet;
importacion manual de TLE para operacion sin red.
**Motivo:** un ESP32 desconectado no puede descargar de Celestrak por su AP.
**Consecuencia:** cache persistente, errores visibles, HTTPS verificado y
antiguedad de cada TLE. Los ampersands HTML se normalizan a `&` en las URL.

## ADR-012: posicion, tiempo y orientacion son estados distintos

**Decision:** GNSS para UTC/posicion; referencia de norte verdadero y nivel
explicitamente calibradas; homing para referencia mecanica.
**Motivo:** un GPS quieto no da rumbo fiable. Un magnetometro junto a motores,
acero y coax puede dar rumbo incorrecto; declinacion es local y variable.
**Consecuencia:** calibracion por norte conocido y burbuja como fallback,
no autoorientacion ficticia. Un cambio de tripode exige recalibracion.

## ADR-013: limites de cable y cenit

**Decision:** no rotacion AZ ilimitada; limites mecanicos y logicos.
**Motivo:** proteger cables y prevenir atascos.
**Consecuencia:** un pase que exige mas velocidad o supera limites se rechaza
o detiene, no se sigue por el camino largo sin planificacion. Hay zona de
exclusion configurable cerca del cenit hasta demostrar seguimiento estable.

## ADR-014: fallo seguro

**Decision:** arranque desarmado, parada fisica NC, limites fisicos, homing
con timeout y fallo enclavado; rearmado explicito.
**Motivo:** reinicios y perdida de referencia no deben producir movimiento.
**Consecuencia:** datos corruptos, reloj invalido, TLE viejo o sensor perdido
no reciben respuestas de exito ni movimientos aproximados.

## ADR-015: RT3S independiente

**Decision:** no modificar firmware de radio, no conectar PTT automatico
ni afirmar CAT USB generico.
**Motivo:** un conector/programador de radio no es necesariamente una API CAT.
**Consecuencia:** programar OpenGD77 con datos compatibles; Doppler de radio
y seguimiento de rotor son calculos separados que deben concordar.

## ADR-016: compartimento RF extraible

**Decision:** integrar fisicamente, no redisenar sin pruebas el diplexor previo.
**Motivo:** preservar trabajo del usuario y permitir antena/radio independientes.
**Consecuencia:** cotas reales, esquemas, aislamiento y potencia del proyecto
previo se verifican antes de cortar soporte o conectar TX.

## ADR-017: objetivo de masa no certificado

**Decision:** pesar prototipo completo, no sumar solo gramos de filamento.
**Motivo:** motores, rodamientos, ejes, bateria, coax y conectores dominan.
**Consecuencia:** <=3 kg excluye radio y tripode, e incluye alimentacion
cuando se evalua estacion; si se supera, registrar y redisenar.

## ADR-018: validacion por puertas

**Decision:** G0 software/CAD, G1 mecanica sin RF, G2 RF pasiva, G3 recepcion,
G4 transmision permitida.
**Motivo:** un STL o una prueba unitaria no garantiza un equipo funcional.
**Consecuencia:** no llamar listo para campo antes de superar G1-G4;
documentar bloqueos en vez de esconderlos.

## ADR-019: prioridad de masa sobre tipo de transmision

**Revision aprobada por el usuario:** priorizar <=3 kg y permitir reemplazar
los planetarios por una transmision mas ligera, manteniendo seguimiento AZ/EL.
**Evidencia:** incluso con aligeramiento acotado, ASA equivalente macizo
2,521 kg; escenario hipotetico impreso mas componentes y bateria
3,208-4,038 kg. No se cumple el objetivo anterior.
**Decision:** BASE con dos etapas de correa GT2 20:100, total 25:1;
conservar la planetaria como LEGACY. La relacion real se coordina con firmware.
**Alternativa descartada por el usuario:** aceptar el peso planetario actual.
**Consecuencia:** reevaluar rigidez, backlash, tension, limites y comportamiento
sin alimentacion. Una correa es reversible y no constituye freno de EL.
No declarar <=3 kg hasta pesar, ni sustituir el presupuesto completo por
la masa de unos pocos STL.

Resultado digital inicial BASE: ASA macizo equivalente 0,862 kg.
Presupuesto total 3,121-4,006 kg; escenario hipotetico aligerado
2,905-3,790 kg. El objetivo <=3 kg continua abierto y exige seleccionar
componentes dentro del presupuesto y pesar el conjunto, no declarar
exito por el extremo inferior de una estimacion.

## ADR-020: PCB portadora reparable y Gerber verificables

**Ampliacion solicitada por el usuario:** placa de control propia con
conectores para GNSS, sensores de eje/orientacion, motores, energia y
proteccion, y archivos Gerber para fabricacion.
**Eleccion expresa:** placa portadora de modulos reemplazables, no
ESP32/drivers/GNSS soldados como circuitos integrados discretos.
**Motivo:** reparacion de campo, menor riesgo y costo en primera iteracion.
**Decision:** esquema y PCB editables, mapa GPIO consistente con firmware,
reglas de diseno, salidas Gerber/Excellon y BOM con referencias concretas.
**Consecuencia:** validar modelos EXACTOS de los modulos y sus dimensiones.
Un nombre generico DevKit o StepStick no demuestra compatibilidad electrica.
El corte de potencia de motores debe ser independiente del software;
la logica puede mantenerse alimentada para informar el fallo.
**Limite:** los archivos no se consideran liberados a fabricacion solo
por existir; ERC/DRC, revision de huellas, corriente, aislamiento,
continuidad y pruebas de banco son puertas independientes.
Los sensores de orientacion opcionales no se anuncian implementados en
firmware por tener un conector. GNSS quieto sigue sin medir norte verdadero.

## ADR-021: branding impreso Bricohams

**Eleccion expresa del usuario:** texto `BRICOHAMS` y `bricohams.org`
en relieve, integrado en la tapa de la caja de control.
**Decision:** geometria conectada a la tapa, con profundidad y posicion
parametricas fuera de tornillos, ventilacion y conectores. Regenerar
STL y verificar malla tras el cambio.
**Motivo:** identificacion durable sin adhesivos ni pieza suelta.
**Limite:** no se reproduce un logotipo oficial no aportado; la marca
textual no implica certificacion ni aval de terceros.

## ADR-022: calibracion guiada y Android BLE

**Ampliacion expresa:** calibracion en interfaz web y app Android nativa
para control Bluetooth. El usuario eligio BLE.
**Decision:** protocolo compartido de control, autenticacion y estados;
no duplicar comandos que puedan eludir interbloqueos por otro transporte.
La calibracion separa homing, posicion/UTC, nivel y norte verdadero,
con validacion de estado y confirmacion fisica explicita.
**Consecuencia:** evaluar memoria y coexistencia radio Wi-Fi/BLE en el
ESP32-WROOM-32E; recompilar y revalidar WebFlash tras incorporar BLE.
La app no habilita motores al conectar y no sustituye parada fisica.

## ADR-023: telefono como puente TLE, rotor como calculador

**Eleccion expresa:** la app descarga TLE por HTTPS y los transfiere por
BLE; el ESP32 calcula pases y seguimiento SGP4 autonomos. La app consulta
y muestra los resultados. No se envia una trayectoria calculada por telefono.
**Motivo:** permite actualizar datos en campo con Internet del movil sin
dar por supuesto que el AP del rotor proporciona Internet.
**Consecuencia:** transferencia fragmentada acotada y atomica, validacion
TLE en ambos extremos, errores visibles y prohibicion de actualizar cache
durante movimiento. Pasar una lista de TLE no proporciona frecuencias
de satelite ni orientacion verdadera del tripode.
La perdida de conexion del telefono no convierte el seguimiento
autonomo en control manual ni invalida por si sola un pase; manda la
politica de seguridad del rotor y la validez de UTC/posicion/sensores.

## ADR-024: ampliacion a radio multimodo modular de satelites

**Eleccion expresa:** radio integrada con modulos RF reemplazables,
145/435 MHz full-duplex, CAT/Doppler y manejo desde la misma APK.
La peticion posterior agrega AM y SSB/USB y sustituye la seleccion
intermedia exclusivamente FM.
**Decision:** verificar una arquitectura realmente multimodo antes de
seleccionar modulos o producir Gerbers. Mantener la radio extraible y el
rotor/antena independientes. La placa portadora del rotor ya validada
no queda automaticamente validada para RF/audio ni recibe otro pinout.
**Motivo:** (tr)uSDX y uSDX SOTA son referencias HF de modularidad y CAT,
no cadenas RF 145/435 MHz. El ATU-100 no es un transceptor ni un diplexor.
**Consecuencia:** nueva revision de coste, masa, consumo, blindaje y
aislamiento RX/TX; dos frecuencias configuradas no prueban full-duplex.

## ADR-025: audio, SSTV y mensajes APRS

**Elecciones expresas:** audio Bluetooth bidireccional, altavoz y micro
integrados, conectores externos tipo Baofeng, SSTV ISS PD120/PD180 y
AX.25 Bell202 AFSK1200, con mensajes APRS entre indicativos.
**Decision:** enlace de audio transparente separado del BLE de control
actual; no atribuir audio al protocolo de tramas de 20 bytes del rotor.
Verificar el accesorio y su pinout antes de llamarlo compatible Baofeng.
No conectar directamente una salida de altavoz BTL a una masa de jack.
**Motivo:** compresion de voz, AGC y supresion de ruido pueden alterar
los tonos necesarios para decodificar. El audio exige continuidad y
pruebas de caudal/coexistencia, ademas de autenticar el control.
**Consecuencia:** decodificacion/encodificacion PCM verificables
independientemente de RF; generar un WAV no equivale a transmitir.
Un ACK APRS remoto es diferente de un ACK local del transporte.
No hay pasarela SMS celular ni garantia de entrega por satelite.
PTT debe fallar a recepcion ante errores, expiracion o desconexion.

## ADR-026: evaluar SBC unico y nueva portadora

**Peticion posterior:** Raspberry Pi Zero o similar para radio, audio,
seguimiento y rotor, prescindiendo del ESP32 si resulta viable.
**Decision provisional:** evaluar recursos, puertos y una generacion
de movimiento independiente de la planificacion no determinista de Linux.
No asignar pulsos STEP desde un bucle Python/Linux y calificarlos de precisos.
Considerar drivers con generador de rampas integrado y parada de potencia
fisica/watchdog independiente; confirmar dispositivos y registros antes
de disenar el esquema.
**Consecuencia:** la eliminacion de ESP32 todavia no esta aprobada por
ensayo; nueva PCB y Gerbers con identidad/revision separadas de la portadora
original. Un boot de Linux, Bluetooth caido o proceso bloqueado no debe
mantener PTT ni movimiento peligroso. El WebFlash ESP32 anterior no instala
un sistema Raspberry Pi; documentar aprovisionamiento distinto si se adopta.

## ADR-027: tercer eje POL y seleccion independiente de mano circular

**Eleccion expresa:** giro axial limitado mas conmutacion RF RHCP/LHCP
para antena circular compatible.
**Decision:** nueva variante AZ/EL/POL con tercer motor, limites, homing y
posicion calibrada. Recalcular carga EL/AZ por masa giratoria adicional,
CG, torsion/coaxiales, energia y estructura; recorrido y relacion POL
requieren especificacion propia, no copiar 25:1 automaticamente.
**Motivo:** POL permite orientar polarizacion lineal; una rotacion axial
no invierte la mano circular. RHCP/LHCP se selecciona en la red de fase/
alimentacion verificada de cada banda y con transmision inhibida.
**Consecuencia:** no habilitar giro continuo, juntas RF ni tercer driver
por defecto. La portadora de dos motores anterior no cubre este requisito.
El presupuesto anterior ya superaba 3 kg; el nuevo eje no recupera ese
objetivo sin otro rediseno y medicion.

## ADR-028: masa completa y sensores de la variante nueva

**Eleccion expresa:** limite 5 kg incluido tripode y todos los elementos
listos para operar; reemplaza el anterior 3 kg con exclusiones.
**Decision:** inventario pesado completo y reserva propuesta 500 g
(objetivo interno 4,5 kg), no presupuesto ficticio de piezas desconocidas.
GNSS para sitio/UTC, magnetometro calibrado para rumbo con declinacion,
IMU para inclinacion y encoders independientes para AZ/EL/POL.
**Motivo:** GPS estacionario no da norte y compas no da posicion de eje;
los motores y corrientes alteran el magnetometro.
**Consecuencia:** incluir masa, alimentacion, conectores, montaje y
pruebas de sensores en nueva PCB/documentacion; tres AS5600 requieren
resolver direccion I2C comun. No anunciar PPS, brujula o encoders como
funcionales por dibujarlos. Fallos de validez son visibles y bloquean
las funciones dependientes; calibracion manual solo como procedimiento
explicito y comprobado, no como sustitucion silenciosa.

## ADR-029: interfaces RF SMA

**Eleccion expresa:** SMA convencional 50 ohm para reducir masa y volumen
de radio, antena, diplexor y redes de polarizacion.
**Decision:** no usar RP-SMA, adaptadores BNC/N ni sujetar coaxiales a la
PCB sin alivio de tension; confirmar contacto central y genero por pieza.
**Consecuencia:** huellas/cotas y ratings dependen del conector real;
el ahorro de masa se mide, no se presume. No aplicar SMA a potencia,
sensores ni accesorio de micro/altavoz. Las variantes BNC anteriores son
referencias historicas, no la interfaz RF de esta ampliacion.

## ADR-030: CM5 y un SDR full-duplex reemplazable

**Eleccion expresa:** Raspberry Pi Compute Module 5 y LimeSDR Mini.
El usuario confirma conservar transmision/full-duplex tras explicar
que RTL-SDR Blog V4 es solamente receptor.
**Decision:** CM5 para calculo/control/audio y un SDR con RX/TX
independientes; sustituye propuestas intermedias Zero/Pi4 y dos modulos.
**Consecuencia:** no existe todavia una portadora CM5 validada ni
potencia RF de varios vatios. Seleccionar revisiones y refrigeracion,
USB de alta velocidad, alimentacion, PA lineales y filtros con pruebas.
Conservar el rotor ESP32 anterior solo como variante historica separada.

## ADR-031: alcance Android inspirado en otras aplicaciones

**Eleccion expresa:** primera version con catalogo/pases, mapa/radar,
avisos, frecuencias/Doppler, control AZ/EL/POL, SSTV ISS PD120/PD180 y
mensajes APRS. No equivalencia completa Look4Sat/Robot36.
**Decision:** matriz de funciones/estado/pruebas, implementacion original
y revision de licencias antes de reutilizar bibliotecas o recursos.
**Consecuencia:** un mapa sin datos orbitales reales no demuestra
seguimiento; una imagen sintetica prueba DSP, no recepcion RF.
Avisos Android dependen de permisos, reloj y restricciones del sistema.

## ADR-032: dos SDR para dos bandas de recepcion simultanea

**Eleccion expresa posterior:** dos LimeSDR Mini, no Lime + RTL-SDR;
se sustituye la seleccion intermedia de un SDR de ADR-030.
**Decision:** una cadena identificada por numero de serie para VHF y
otra para UHF, dos receptores concurrentes y capacidad TX por cadena.
Politica inicial conservadora: un solo TX activo, sin asumir autorizacion
para dos transmisiones simultaneas. Seleccionar explicitamente el audio
VHF/UHF hacia el decodificador; no mezclar dos canales de tonos.
**Consecuencia:** recalcular USB, consumo, calor, masa, filtros y
proteccion de ambos receptores. Dos conectores/instancias de software
no acreditan recepcion simultanea en presencia de TX.

## ADR-033: CM5IO oficial y auxiliar original para PCBA

**Eleccion expresa:** CM5IO oficial adquirida mas placa auxiliar propia
con Gerbers/BOM/CPL para JLCPCB. Se descarta para esta revision una
portadora CM5 unica personalizada de alta velocidad.
**Decision:** CM5IO resuelve montaje CM5 y dos USB3 nativos; auxiliar
original para tres drivers, sensores e interbloqueos, con interfaces
verificadas. No distribuir archivos oficiales bajo licencia del proyecto.
**Consecuencia:** incluir CM5IO, refrigeracion, cableado y placa auxiliar
en masa/precio. Tercer dispositivo de audio USB requiere host/hub
especificado; dos puertos USB ocupados no dejan un tercero ficticio.
CM5IO VIO debe configurarse a 3,3 V si la auxiliar usa esa logica;
la seleccion 1,8 V no es intercambiable sin revisar interfaces.

## ADR-034: USB-C y bateria externa

**Elecciones expresas:** preferir USB-C para potencia y datos conservando
SMA RF/K1 audio; excluir bateria externa del limite 5 kg. Se mantiene
objetivo 2 horas y se autoriza una bateria externa mayor que 12 V/1 Ah.
**Decision:** registrar masa transportada de bateria aparte, incluir
su coste y dimensionar corriente/energia/regulacion por consumo real.
12 Wh nominales solo permiten 6 W medios durante 2 horas antes de
perdidas; no declararlos suficientes. La unica exclusion de masa es bateria,
no tripode/radio/cables. Verificar tension por puerto y rol USB-C/PD;
no conectar 12 V directamente a un rail CM5 de 5 V.

## ADR-035: construccion y software por modulo

**Peticion expresa:** documentacion y montaje independientes de antena,
rotor y radio, mas manual general ilustrado.
**Decision:** cuatro puntos de entrada MODULE-ANTENNA, MODULE-ROTOR,
MODULE-RADIO y MODULE-INTEGRATED; perfiles rotor-only, radio-only y
integrated sin dependencias de hardware ficticias.
**Consecuencia:** radio manual independiente no exige rotor/SGP4, pero
conserva permiso TX y camino RF reales; Doppler integrado no cae
silenciosamente a manual. Rotor solo no inicia SDR ni depende de audio.
Antena sola no exige ordenador. La BOM integrada elimina duplicacion
de CM5/portadora/energia y mantiene piezas compartidas trazables.
