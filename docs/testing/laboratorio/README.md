# BricoHams: plantillas de laboratorio

Generadas por [lab-workbook.cjs](../../../scripts/lab-workbook.cjs). **101 ensayos y 398 filas BOM**, todos PENDIENTES.

Copiar esta carpeta a un expediente nuevo antes de rellenar. No editar/regenerar sobre resultados reales.
Ver [procedimiento de uso y decision](../09-laboratorio.md), [NanoVNA](../10-nanovna.md), [RF activa](../11-rf-potencia.md) y [calibraciones](../12-calibraciones.md).

| Archivo | Uso |
| --- | --- |
| [cuaderno.html](cuaderno.html) | Imprimir A4, una pagina por ensayo; campos manuscritos, sin guardado interactivo |
| [resultados.csv](resultados.csv) | Cabecera y conclusion por ejecucion; duplicar filas para repeticiones/unidades |
| [lecturas.csv](lecturas.csv) | Valores brutos/corregidos, U/k y condiciones por punto; filas extra para canales de referencia, no autorizacion TX |
| [componentes.csv](componentes.csv) | Seleccion/exclusion de TODAS las filas BOM; expandir por unidad y asignar ensayos revisados |
| [instrumentos.csv](instrumentos.csv) | Equipos/patrones, series, ratings, certificados y vigencia; expandir grupos |
| [calibraciones.csv](calibraciones.csv) | As found/ajuste/as left y verificacion independiente antes/despues |
| [evidencias.csv](evidencias.csv) | Fotos, S1P/S2P, capturas, logs y SHA-256 |

Estados: PENDIENTE, BLOQUEADO, INDETERMINADO, APROBADO, RECHAZADO, NO_APLICA. Un blanco no significa cero, ni aprobado, ni no aplicable.

El cuaderno referencia guias relativas a la carpeta original. En una copia externa consultar los procedimientos desde el repositorio y registrar su revision; las fichas incluyen accion/criterio pero no reemplazan los manuales.

## Indice de fichas

| ID | Guia / accion |
| --- | --- |
| PWR-01 | [02-electronica.md](../02-electronica.md) · Sin motores ni radio, conectar la fuente de banco con límite de corriente a 0,2 A y subir a la tensión nominal de 12 V. |
| PWR-02 | [02-electronica.md](../02-electronica.md) · Medir con multímetro 12 V, 5 V y 3,3 V en sus nodos (placa/CM5IO/auxiliar) y en reposo y con carga. |
| PWR-03 | [02-electronica.md](../02-electronica.md) · Con motores conectados y fuente a 12 V, pulsar la parada de emergencia y medir la tensión en VMOT de cada driver. |
| PWR-04 | [02-electronica.md](../02-electronica.md) · Con el sistema parado, apagar y reiniciar el host (kill -9 del servicio y reinicio) mientras la parada está pulsada. |
| PWR-05 | [02-electronica.md](../02-electronica.md) · Detener el latido WATCHDOG_HEARTBEAT (BCM11) con motores armados en banco sin carga mecánica. |
| PWR-06 | [02-electronica.md](../02-electronica.md) · Con el equipo sin energía retirar fusible o preparar apertura simulada por fixture de cada cable NC; reenergizar solo el circuito de prueba autorizado y observar el fallo. |
| PWR-07 | [02-electronica.md](../02-electronica.md) · Medir ondulación y transitorios en VMOT y 5 V con osciloscopio (sonda de masa corta) durante aceleración y parada de los tres motores. |
| PWR-08 | [02-electronica.md](../02-electronica.md) · Mantener 30 min con los motores en movimiento lento alterno y medir temperatura con cámara térmica/termopar en drivers, DC/DC, fusible y conectores Powerpole. |
| DRV-01 | [02-electronica.md](../02-electronica.md) · Sin motor, alimentar y leer por SPI (CS0 AZ, CS1 EL, CS2 POL) el registro de versión/IOIN de cada TMC5160. |
| DRV-02 | [02-electronica.md](../02-electronica.md) · Con carga retenida y EN alto, comprobar nivel, estado del driver y corriente de fase con instrumentación apropiada, sin ordenar movimiento. |
| DRV-03 | [02-electronica.md](../02-electronica.md) · Calcular la corriente de fase con Rsense y modelo exactos, configurar IRUN/IHOLD y medir RMS de fase con sonda/método apto para PWM chopper según LAB-08; la corriente DC de entrada o un DMM ordinario no son sustitutos. |
| DRV-04 | [02-electronica.md](../02-electronica.md) · Girar un eje exactamente 10 vueltas de motor por la rampa del driver y contar con marca/encoder. |
| DRV-05 | [02-electronica.md](../02-electronica.md) · Provocar fallo del driver (sobretemperatura simulada o desconectar una fase con el driver apagado) y observar FAULT_AZ_N/EL_N/POL_N (BCM24/25/26). |
| DRV-06 | [02-electronica.md](../02-electronica.md) · Medir temperatura del driver tras 10 min a corriente de trabajo en caja cerrada. |
| SNS-01 | [02-electronica.md](../02-electronica.md) · Escanear el bus I2C1 con el multiplexor TCA9548A (0x70): seleccionar cada canal y leer el AS5600 (0x36). |
| SNS-02 | [02-electronica.md](../02-electronica.md) · Leer STATUS (MD/ML/MH) y AGC del AS5600 con el imán a la distancia de montaje; girar 360°. |
| SNS-03 | [02-electronica.md](../02-electronica.md) · Comparar el ángulo del AS5600 con un goniómetro/indicador en 8 posiciones. |
| SNS-04 | [02-electronica.md](../02-electronica.md) · Accionar cada final de carrera (AZ min/max, EL min/max, POL min/max) y observar BCM4, 5, 6, 7, 8, 9. |
| SNS-05 | [02-electronica.md](../02-electronica.md) · GNSS en exterior o ventana: esperar fijación y comparar UTC y posición con una referencia conocida; medir PPS (BCM27) con osciloscopio. |
| SNS-06 | [02-electronica.md](../02-electronica.md) · Quitar la antena GNSS y observar el estado de hora/sitio en el host. |
| SNS-07 | [02-electronica.md](../02-electronica.md) · Brújula/IMU: apuntar la antena a un rumbo verdadero conocido (sol/referencia) con motores apagados y encendidos; anotar la diferencia. |
| PCB-01 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Abrir cada proyecto en KiCad y ejecutar ERC, DRC, "unconnected items" y paridad esquema/PCB con la versión documentada. |
| PCB-02 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Comprobar que cada archivo de fabricación coincide con su SHA-256 de reports/manifest-sha256.json y fabrication/release-status.json (sha256sum). |
| PCB-03 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Cargar los Gerber en un visor independiente (KiCad Gerber Viewer, Tracespace o gerbv) y revisar capas, taladros, contorno y logo BricoHams en serigrafía. |
| PCB-04 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Montar el circuito equivalente en banco (módulos reales + cableado de prototipo) para cada bloque: alimentación, drivers, sensores, parada/watchdog. |
| PCB-05 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Con el comprobador del contrato GPIO (banco, ver BANCO) recorrer las 26 señales de interface.json: cada salida mueve su LED, cada entrada responde a su interruptor. |
| PCB-06 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Revisar huellas contra hojas de datos: pin 1, orientación y paso de DevKitC, SilentStepStick, MCP23017, TCA9548A, conectores y fusibles; imprimir el PCB a escala 1:1 en papel y apoyar los módulos reales. |
| PCB-07 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Revisar el presupuesto de corriente de trazas y pistas de potencia (ancho, cobre, caída) con la corriente de los tres motores y el fusible. |
| PCB-08 | [03-puerta-pcb.md](../03-puerta-pcb.md) · Preparar el pedido: BOM, CPL (referencias, coordenadas, lado, rotación), lista DNP/módulos manuales, DFM del fabricante y confirmación de piezas LCSC exactas. |
| MEC-01 | [04-mecanica.md](../04-mecanica.md) · Imprimir cupones de prueba (agujero, eje, inserto) y medir contracción del ASA con calibre; imprimir copas de rodamiento y retenedores. |
| MEC-02 | [04-mecanica.md](../04-mecanica.md) · Montar el reductor de correa SIN motor (20T:100T ×2 = 25:1, correas GT2 de 252 mm); girar la salida a mano una vuelta completa. |
| MEC-03 | [04-mecanica.md](../04-mecanica.md) · Medir tensión de correa (flecha con carga en el centro del tramo) con las ranuras de ±1,5 mm; tras 30 min repetir. |
| MEC-04 | [04-mecanica.md](../04-mecanica.md) · Confirmar que la polea de entrada de la 2ª etapa está fija al eje de salida de la 1ª (no flota) y el eje de salida está sostenido por dos rodamientos. |
| MEC-05 | [04-mecanica.md](../04-mecanica.md) · Homing sin antena con el final de carrera: a) conectado, b) desconectado, c) pegado, d) no alcanzado. |
| MEC-06 | [04-mecanica.md](../04-mecanica.md) · Medir holgura (backlash) invirtiendo el sentido con indicador de dial o goniómetro en cada eje. |
| MEC-07 | [04-mecanica.md](../04-mecanica.md) · Equilibrar la carga objetivo (0,5 kg de antena) y medir el CG respecto al eje; ensayo con retención secundaria sobre banco estable antes del trípode. |
| MEC-08 | [04-mecanica.md](../04-mecanica.md) · Seguimiento lento sin viento: barrer cada eje y comparar la posición del encoder con goniómetro/indicador de referencia en 10 posiciones. |
| MEC-09 | [04-mecanica.md](../04-mecanica.md) · Mantener 30 min movimiento alterno bajo la carga objetivo; comprobar pérdida de pasos, aflojamiento y temperatura. |
| MEC-10 | [04-mecanica.md](../04-mecanica.md) · Pesar el conjunto completo operativo (incluye trípode, radio y cables; excluye la batería externa, que se pesa aparte) y medir el bulto plegado. |
| ANT-01 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Calibrar el VNA (OPEN, SHORT, LOAD, THRU) en el plano del conector, sin radio conectada. |
| ANT-02 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Medir cada puerto alimentado de antena por banda con balun/matching y conjunto desplegado, coaxial y rotor en posiciones reales; incluir canales y Doppler, no solo 145/435 MHz. Un reflector sin puerto se comprueba por geometría/continuidad y efecto instalado, no por S11 propio. |
| ANT-03 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Medir el híbrido por banda: amplitud y fase entre salidas con la otra puerta cargada a 50 Ω. |
| ANT-04 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Medir el diplexor 2 m/70 cm: pérdida de inserción por rama, pérdida de retorno y aislamiento entre ramas. |
| ANT-05 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Repetir ROE tras 50 plegados/despliegues y revisar continuidad de contactos RF. |
| ANT-06 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Medir o simular patrón, sentido RHCP/LHCP y relación axial con el conjunto completo (antena + coaxial + rotor). |
| ANT-07 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Con receptor y generador (o SDR como fuente), medir el nivel mínimo detectable con rotor y convertidores apagados y encendidos. |
| RAD-01 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Conectar ambos LimeSDR por USB y comprobar el descubrimiento; anotar los dos números de serie y la asignación VHF/UHF. |
| RAD-02 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Pedir tasas y frecuencias y leerlas del hardware; abrir dos flujos RX concurrentes (VHF y UHF). |
| RAD-03 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Alimentar un tono/FM de referencia y verificar demodulación en VHF y UHF; probar DSP primero con WAV/vectores y luego con recepción real. |
| RAD-04 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Probar el transporte de audio Bluetooth PCM (S16LE, mono, 8000 muestras/s): créditos, pérdidas y reconexión. |
| RAD-05 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Sin permiso físico de TX, intentar PTT desde el host/app y desde GPIO (PTT_VHF_REQUEST BCM22, PTT_UHF_REQUEST BCM23). |
| RAD-06 | [05-rf-y-radio.md](../05-rf-y-radio.md) · Solo con licencia y autorización: cualificar TX a mínima potencia con carga: espectro, armónicos (145×3 = 435 MHz), bloqueo y temperatura. |
| SW-01 | [06-software-y-os.md](../06-software-y-os.md) · En la raíz del repositorio ejecutar: node --test "tests/*.test.cjs" |
| SW-02 | [06-software-y-os.md](../06-software-y-os.md) · Ejecutar: PYTHONPATH=.:radio:rotor python3 -m pytest -q tests/rotor tests/radio_host |
| SW-03 | [06-software-y-os.md](../06-software-y-os.md) · Compilar y ejecutar la lógica de control nativa (tests/control_logic/test_native) con g++ y Unity; ejecutar node scripts/engineering-report.cjs. |
| SW-04 | [06-software-y-os.md](../06-software-y-os.md) · Comparar SGP4 con una implementación independiente (mismo TLE, UTC y sitio) en 10 instantes de un pase. |
| SW-05 | [06-software-y-os.md](../06-software-y-os.md) · Alimentar datos erróneos: TLE truncado, checksum malo, epoch viejo, nombres con HTML, fuente caída, catálogo demasiado grande. |
| SW-06 | [06-software-y-os.md](../06-software-y-os.md) · Renderizar con OpenSCAD todas las piezas y comprobar malla cerrada, volumen y ausencia de componentes inesperados (incluidas las tapas con el logo en relieve). |
| SW-07 | [06-software-y-os.md](../06-software-y-os.md) · Grabar la imagen BricoHams OS (os/build-image.sh en Linux con Docker, o el workflow build-os.yml) en la tarjeta/eMMC y arrancar el CM5. |
| SW-08 | [06-software-y-os.md](../06-software-y-os.md) · En el CM5 ejecutar gpiodetect/gpioinfo y seleccionar el /dev/gpiochipN que expone los offsets BCM congelados; arrancar el selector de perfil (rotor-only, radio-only, integrated). |
| APP-01 | [07-app-android.md](../07-app-android.md) · Instalar el APK debug (GitHub Actions android.yml) en un teléfono Android 8-11 y otro Android 12+; abrir la app. |
| APP-02 | [07-app-android.md](../07-app-android.md) · Pulsar Ayuda en cada pantalla con el teléfono en español, inglés y húngaro. |
| APP-03 | [07-app-android.md](../07-app-android.md) · Con Internet, probar los tres proveedores (CelesTrak, AMSAT, PE0SAT) uno a uno con Descargar TLE. |
| APP-04 | [07-app-android.md](../07-app-android.md) · Repetir la descarga de CelesTrak varias veces seguidas y luego en modo avión. |
| APP-05 | [07-app-android.md](../07-app-android.md) · Importar un archivo TLE local válido, luego uno con checksum malo, uno truncado y uno con líneas con espacios finales. |
| APP-06 | [07-app-android.md](../07-app-android.md) · Descargar un catálogo con más de 100 satélites. |
| APP-07 | [07-app-android.md](../07-app-android.md) · Escanear rotores (15 s), seleccionar explícitamente el rotor, confirmar el passkey y guardar el token cifrado. |
| APP-08 | [07-app-android.md](../07-app-android.md) · Con la hora UTC válida y modo READY/DISARMED, pulsar Transferir catálogo; observar el progreso en bytes hasta "transferencia completa". |
| APP-09 | [07-app-android.md](../07-app-android.md) · Durante la transferencia apagar el rotor o alejar el teléfono; esperar 60 s sin avance. |
| APP-10 | [07-app-android.md](../07-app-android.md) · Elegir un satélite del catálogo del controlador y consultar pases; comparar AOS/LOS con una referencia independiente (misma estación y TLE). |
| APP-11 | [07-app-android.md](../07-app-android.md) · Receptor digital: reproducir un WAV SSTV y uno APRS 1200 baudios por altavoz/cable hacia la entrada de audio del teléfono. |
| SYS-01 | [08-sistema.md](../08-sistema.md) · Seguir el pase de un satélite real y compararlo con una referencia independiente, misma estación y TLE. |
| SYS-02 | [08-sistema.md](../08-sistema.md) · Sin Internet (AP propio): importar TLE, seleccionar, predecir y seguir; cerrar la app durante el pase. |
| SYS-03 | [08-sistema.md](../08-sistema.md) · Provocar: pérdida de GNSS, UTC inválida, caché antigua, encoder perdido, pase bajo el horizonte, zenit, cable wrap y velocidad inalcanzable. |
| SYS-04 | [08-sistema.md](../08-sistema.md) · Confirmar el norte verdadero con una referencia conocida; mover el trípode y repetir la calibración. |
| SYS-05 | [08-sistema.md](../08-sistema.md) · Pesar el conjunto operativo y medir la autonomía con la batería elegida durante un ensayo continuo de 2 horas. |
| SYS-06 | [08-sistema.md](../08-sistema.md) · G4, solo con licencia: transmisión de prueba sobre carga a mínima potencia y luego pase real autorizado; vigilar temperatura de redes y conectores. |
| LAB-01 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Recepcion sin energia de cada unidad seleccionada: identificar BOM/fabricante/modelo/revision/serie, fotos, daños, pinout, dimensiones, polaridad, ratings y continuidad contra circuito; excluir variantes no montadas con motivo firmado. |
| LAB-02 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Identificar NanoVNA/firmware, rango, kit y plano; estabilizar, SOL y THRU segun modelo; verificar con patrones independientes en ambas bandas, tres reconexiones y verificacion posterior. |
| LAB-03 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · NanoVNA sin PA/DC: medir S11 de cada puerto alimentado con matching/balun y conjunto instalado, barridos 144-146/430-440 y canales con Doppler; repetir tras montaje y 50 ciclos. |
| LAB-04 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Medir coaxiales, conectores, baluns, filtros y diplexor pasivos: S11 y S21 por ruta, puertos restantes terminados, sentido/plano registrado; repetir rutas inversas por reconexion. |
| LAB-05 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Hibrido/red de fase por banda: mismo plano/cable, medir entrada-A y entrada-B con otros puertos terminados; registrar fase compleja y reparto; verificar aislado. |
| LAB-06 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Verificar DMM, fuente/carga, osciloscopio/sondas, corriente y temperatura con patrones en rango de uso; documentar antes, ajustes y despues. |
| LAB-07 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Ensayar alimentacion, fusibles/conectores/DC-DC y cadena ESTOP/watchdog en circuito autorizado; cargas ficticias primero, rails/transitorios/tiempos y temperatura despues. |
| LAB-08 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Por driver y motor: identificar Rsense, corriente nominal y modo; verificar EN/estado, medir corriente RMS de fase con equipo apropiado, conteo de vueltas, fallos seguros y temperatura. |
| LAB-09 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Por encoder/iman/mux/final: identificar canal/serie, STATUS y gap; comparar ocho posiciones ambos sentidos y tres repeticiones; simular NC abierto/pegado/cable roto por fixture seguro. |
| LAB-10 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · GNSS/PPS/UTC: comparar fix y tiempos con referencia independiente, registrar datum/altura/unidades, lock y latencias; probar perdida de fix/UTC y reanudacion controlada. |
| LAB-11 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Nivelar IMU/brujula, calibrar hard/soft iron segun fabricante, registrar matriz/ejes y comparar norte verdadero externo con motores/DC-DC apagados y activos. |
| LAB-12 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Verificar calibre, comparador, goniómetro, bascula y llave de par con referencias apropiadas; medir cero, puntos de uso y repetibilidad. |
| LAB-13 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Por ASA, rodamiento, eje, correa/polea, fijacion, tripode y antena: inspeccion/cotas, retencion, giro sin energia, holgura, CG, masa, envolvente y rearmado; carga progresiva retenida. |
| LAB-14 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Calibrar/verificar cadena generador, frecuencia, vatimetro/acoplador, atenuadores/cables/carga y analizador a fundamental/armonicos; documentar montaje, correcciones y presupuesto maximo de entrada. |
| LAB-15 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Conmutadores/bypass sin PA: medir rutas de insercion, retorno y aislamiento en estados RX/TX/seguro mediante fuente pequena senal y puertos terminados; caracterizar suelo. |
| LAB-16 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Previo/filtro/limitador/receptor por banda: alimentar con fuente limitada, ganancia a nivel conocido, consumo/temperatura, sensibilidad y recuperacion; NF solo con equipo/metodo calibrados. |
| LAB-17 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Secuenciador/PTT/guard con PA desconectado: capturar peticion, inhibicion, contactos y LNA en transiciones; reset/watchdog/retorno pegado/abierto/alimentacion perdida/PTT retenido. |
| LAB-18 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · TX en carga dimensionada: escalones 1/5/10/25 W solo dentro del menor rating aprobado; registrar directa/reflejada, DC, temperaturas, duty cycle, duracion y comprobacion pasiva tras enfriar. |
| LAB-19 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · En carga y cadena protegida: fundamental/armonicos/espurios, desviacion FM, PEP/IMD de dos tonos SSB, LSB/USB y envolvente AM si aplica; verificar no sobrecarga del analizador. |
| LAB-20 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Medir fuga TX->RX primero con detector protegido en lugar de LNA, ambas direcciones y armonicos; despues sensibilidad simultanea con inyeccion protegida y nivel deseado constante. |
| LAB-21 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · En campo/camara autorizados: patron, ganancia por sustitucion si existe referencia y relacion axial por polarizacion lineal giratoria; mano con referencia circular conocida, varias direcciones. |
| LAB-22 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Dos SDR/audio: verificar series, reloj/tasa/frecuencia con senal externa; loopback/tono/WAV y niveles, clipping, latencia, muestras perdidas, reconexion y demodulacion por banda. |
| LAB-23 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Integracion real: norte/UTC, >=10 posiciones ambos sentidos, seguimiento, masa/autonomia de dos horas con duty cycle registrado; probar fallos con carga retenida y TX inhibido. |
| LAB-24 | [13-ensayos-laboratorio.md](../13-ensayos-laboratorio.md) · Revisar cobertura por todas las unidades seleccionadas, calibraciones antes/despues, evidencias/hash, desviaciones y resultados; firmar alcance de liberacion por variante, banda, potencia y configuracion. |
