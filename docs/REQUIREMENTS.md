# Requisitos y trazabilidad

| ID | Requisito | Implementacion / evidencia | Aceptacion |
| --- | --- | --- | --- |
| R01 | Antena 145/435 | CAD y RF-AND-RADIO | VNA en ambas bandas, ensamblada |
| R02 | Plegable portable | MECHANICAL, piezas desmontables | Medir bulto y masa completos |
| R03 | Seguimiento AZ/EL | CONTROL, SGP4 | Referencia orbital y banco de dos ejes |
| R04 | Autonomia sin movil | Calculo en ESP32 | Cerrar navegador durante seguimiento |
| R05 | Interfaz web AP | web y firmware | Acceder sin Internet desde movil |
| R06 | Actualizar TLE | STA/TLS/importacion | Error visible y cache consistente |
| R07 | Ubicacion UTC | GNSS y estado de validez | Reinicio, sin fix, perdida de reloj |
| R08 | Orientacion/nivel | Calibracion verdadera separada | Error angular medido |
| R09 | RT3S OpenGD77 | Soporte y operacion independiente | Version y canales reales verificados |
| R10 | Diplexor anterior | Integracion modular RF | Cotas y S-parametros confirmados |
| R11 | Tripode fotografia | Inserto metalico | Ensayo de carga y torsion |
| R12 | Antenas intercambiables | Adaptadores de boom | Verificar masa/CG por antena |
| R13 | NEMA14/25:1 ASA | CAD, calculos | Giro manual, par, calentamiento |
| R14 | Seguridad de movimiento | NC, limites, fallos | Parada fisica sin navegador |
| R15 | Git y documentacion | Repositorio independiente | Archivos persistentes e historial |
| R16 | Bajo presupuesto | BOM orientativa | Cotizacion local, sin precios inventados |
| R17 | Materiales de referencia | SOURCES, REFERENCE-ANALYSIS | Citas por PDF y limites de licencia |
| R18 | PCB portadora y Gerber | hardware, fabrication, PCB | ERC/DRC y nets, huellas/corriente verificados |
| R19 | Sensores conectables | Mapa comun PCB/CONTROL | Dos AS5600 sin conflicto de direccion y GNSS |
| R20 | Proteccion de energia | Fusible, polaridad, sobretension y corte motor | Ensayos electricos antes de motor/RF |
| R21 | Calibracion web guiada | UI y control compartido | Homing/norte/nivel y errores explicitos |
| R22 | App Android BLE | android, firmware BLE | Emparejamiento/auth, permisos y pruebas de telefono |
| R23 | TLE via telefono | Descarga HTTPS, transferencia BLE atomica | Catalogo valido, errores y cache sin truncacion |
| R24 | Pases calculados por rotor en app | SGP4 ESP32 y consulta BLE | Sin dependencia de telefono durante pase |
| R25 | Radio integrada 145/435 full-duplex FM, AM y SSB/USB | Ampliacion solicitada; arquitectura RF multimodo por verificar | Recepcion durante TX en ambas combinaciones de bandas, espectro y desensibilizacion medidos |
| R26 | CAT y Doppler en la misma APK | Integracion pendiente; no atribuir CAT a RT3S | Frecuencias reales TX/RX, lectura de retorno y errores/interbloqueos |
| R27 | SSTV PD120/PD180 en Android | Desarrollo de decodificador de audio local | Vectores PCM conocidos e imagen, despues ensayo por radio |
| R28 | AX.25 AFSK1200 y APRS | Desarrollo de decodificacion y mensajes entre indicativos | CRC, NRZI, bit stuffing, destinatario, ID y ACK reales |
| R29 | Audio Bluetooth bidireccional | Enlace transparente independiente del BLE actual del rotor | Continuidad de muestras, perdidas visibles, latencia y convivencia verificadas |
| R30 | Altavoz y micro internos, accesorio tipo Baofeng | Interfaz y placa de audio pendientes | Pinout del accesorio exacto, bias, PTT, aislamiento y ausencia de realimentacion |
| R31 | Envio de mensajes APRS por radio | Modulacion y transporte RF requieren validacion independiente | No declarar enviado por generar audio ni entregado sin ACK remoto |
| R32 | Evaluar Raspberry Pi Zero o similar para radio y rotor sin ESP32 | Viabilidad solicitada; no hay seleccion ni ensayo de SBC aprobado | Recursos USB/CPU/RAM/Bluetooth medidos, generacion de movimiento determinista y parada independiente del SO |
| R33 | Actualizar PCB/Gerbers y documentacion del conjunto | Nueva revision condicionada a seleccion de modulos y SBC | ERC/DRC, huellas/pinout, corriente, audio, RF y mecanica; no reutilizar aprobacion del carrier ESP32 |
| R34 | Tercer eje POL de giro axial limitado | Diseno mecanico/control de tres motores en desarrollo | Recorrido, homing, limites NC, encoder, cables, masa/CG y par verificados |
| R35 | Conmutacion RF RHCP/LHCP | Independiente del giro POL y condicionada a antena circular compatible | Fase/amplitud, relacion axial, aislamiento y conmutacion sin TX en ambas bandas |
| R36 | Masa completa <=5 kg | Sustituye limite anterior de 3 kg con exclusiones | Pesar antena, tres ejes, radio/SBC, caja, sensores, bateria, cables y tripode juntos |
| R37 | GNSS, brujula e inclinacion en variante nueva | GNSS/UTC, magnetometro e IMU, mas encoders AZ/EL/POL | Calibracion, declinacion/norte verdadero, interferencias, validez visible y reaccion segura ante fallos |
| R38 | Conectores RF SMA 50 ohm | Antena, radio, diplexor y redes RHCP/LHCP; excluir RP-SMA y adaptadores BNC/N en variante nueva | Genero/contacto, huella, potencia, coaxial, alivio de tension y masa verificados; audio/energia no usan SMA |
| R39 | CM5 + LimeSDR Mini, sin ESP32 | Arquitectura elegida posteriormente; un modulo RF full-duplex reemplazable | Portadora, USB, recursos, potencia/bateria, refrigeracion y parada independientes ensayados |
| R40 | Funciones Android inspiradas en Look4Sat/Robot36 | Primera version seleccionada: catalogo/pases, mapa/radar, avisos, frecuencias/Doppler, tres ejes, PD120/180 y APRS | Matriz por funcion con pruebas; sin afirmar equivalencia completa ni copiar interfaz/codigo sin licencia |
| R41 | Dos LimeSDR Mini para RX simultanea VHF/UHF | Sustituye eleccion intermedia de un SDR; cada cadena es capaz de TX | Identificacion inequívoca por serie, dos streams reales, seleccion de audio, filtrado y desensibilizacion; un solo TX activo inicialmente |
| R42 | Documentacion espanol, ingles y hungaro | Ediciones completas y sincronizadas; glosario, diagramas/leyendas, montaje, advertencias y justificaciones | Cobertura por documento, enlaces y revision/hash fuente; licencias originales sin alterar |
| R43 | Precios de referencia de todos los componentes/materiales | BOM con cantidades, modelo, fecha, fuentes EUR, promedio comparable, IVA/portes y herramientas separadas | Verificar subtotales y cobertura; precio pendiente/provision no equivale a compra ni coste cero |
| R44 | Ilustraciones dentro de instrucciones de montaje | Figuras enlazadas por paso y mapa de componentes con IDs BOM | Correspondencia pieza/material/paso, revision del plano y limitaciones de dibujos conceptuales |
| R45 | Paquete JLCPCB Gerbers + BOM + CPL | Gerbers/taladros reales, BOM con LCSC exactos, CPL mm/cara/rotacion y lista manual/DNP | ERC/DRC/conectividad, correspondencia designadores/origen/orientacion/codigo proveedor; sin pedido ni liberacion fisica por defecto |
| R46 | USB-C para alimentacion y datos | Preferencia confirmada; RF SMA y audio K1 permanecen | Rol/velocidad y alimentacion por puerto, PD/cable/limites de corriente verificados; no aplicar tension incompatible al CM5 |
| R47 | Bateria externa excluida del limite de 5 kg | Sustituye inclusion inicial de bateria; mantener 2 horas con capacidad externa a dimensionar | Masa externa y coste separados, energia/corriente util y regulacion verificadas; 12 Wh no demuestran 2 horas |
| R48 | Sistema operativo BricoHams personalizado | Raspberry Pi OS oficial ARM64, branding/banner, componentes y servicios del proyecto, configuracion local segura | Fuente/version reproducible, imagen realmente construida separada de receta, arranque CM5, dependencias y permisos; sin credenciales compartidas ni autoarmado |
| R49 | Powerpole y fusibles de distribucion | Entrada externa 12 V por Powerpole, principal junto a bateria y ramas CM5/motor/RF | Polaridad, crimp/seccion, DC/interrupcion, curva/corriente/inrush, temperatura y coordinacion; BMS no sustituye fusible |
| R50 | Evaluar filtros EMI de alimentacion | Modo comun/diferencial amortiguado, desacoplos y segregacion de ramas | Corriente, saturacion, DCR/caida, estabilidad reguladores, inrush/transitorios y ruido recibido medidos; no confundir filtro DC con aislamiento RX/TX |
| R51 | Modulos independientes y guia general | Antena, rotor y radio SDR con materiales/montaje/configuracion propios; integracion ilustrada separada | Instalar rotor sin SDR, radio manual sin rotor y antena sin software; BOM compartida sin duplicar CM5/energia |

La ampliacion R25-R31 sustituye la eleccion intermedia FM-only para la
nueva radio, pero conserva el funcionamiento independiente RT3S/rotor de
la primera entrega. No convierte modulos FM en SSB ni declara implementada
una cadena RF por disponer de controles en la app. Reabrir masa, consumo,
refrigeracion y coste antes de liberar una nueva PCB/caja.
La posterior peticion de SBC unico reabre la decision de conservar ESP32:
es una evaluacion, no una sustitucion ya verificada.

## No objetivos de la primera iteracion

- Cobertura SATCOM militar o compatibilidad con antena comercial de la foto.
- Full-duplex con una RT3S; SSB en una radio FM/DMR.
- Mover toda antena SpaceQuad sin verificar carga o instalar sin calibrar.
- Precision subgrado garantizada con piezas impresas sin ensayos.
- Alimentacion ilimitada, impermeabilidad IP certificada o resistencia
  a cualquier viento.
- Automatizar CAT/PTT con un protocolo no verificado.

## Pendientes que requieren datos del equipo real

Motor exacto y su curva de par, dimensiones RT3S con bateria/funda,
medida de conectores y coax, referencia del tripode y carga admisible,
VNA del diplexor, alimentacion elegida, tolerancias de impresora,
masa/CG real y campo local del magnetometro si se incorpora.
