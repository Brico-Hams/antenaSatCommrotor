# Electrónica: alimentación, drivers y sensores

Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.

## PWR — Alimentación, protecciones y parada

**Comportamiento esperado del componente.** Con la parada pulsada, ningún motor puede recibir energía aunque el firmware o el host se bloqueen; el CM5 y la lógica siguen alimentados para indicar el fallo. Al soltar la parada NO se reanuda ningún movimiento: hay que rearmar y repetir el homing.

### PWR-01
- [ ] **Acción:** Sin motores ni radio, conectar la fuente de banco con límite de corriente a 0,2 A y subir a la tensión nominal de 12 V.
- **Esperado:** Consumo de reposo y temperatura medidos; el límite inicial corresponde solo al bloque sin CM5/SDR/motores, no al arranque de todo el conjunto.
- **Criterio de aprobación:** Corriente dentro del presupuesto aprobado sin saturar fuente; polaridad comprobada con DMM antes de conectar, temperatura dentro de ficha. No usar tacto o LED como verificación metrológica.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PWR-02
- [ ] **Acción:** Medir con multímetro 12 V, 5 V y 3,3 V en sus nodos (placa/CM5IO/auxiliar) y en reposo y con carga.
- **Esperado:** Tres raíles dentro de ±5 % y sin caída al arrancar motores.
- **Criterio de aprobación:** Ningún GPIO ve más de 3,3 V; 12 V jamás llega al CM5 (CM5-PCB).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PWR-03
- [ ] **Acción:** Con motores conectados y fuente a 12 V, pulsar la parada de emergencia y medir la tensión en VMOT de cada driver.
- **Esperado:** VMOT cae a 0 V en cada eje; la lógica/CM5 siguen vivos y reportan ESTOP.
- **Criterio de aprobación:** VMOT < 1 V; ESTOP_AUX_N (BCM10) pasa a alto-activo; sin giro residual.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PWR-04
- [ ] **Acción:** Con el sistema parado, apagar y reiniciar el host (kill -9 del servicio y reinicio) mientras la parada está pulsada.
- **Esperado:** El corte físico se mantiene: ningún eje se mueve al reiniciar.
- **Criterio de aprobación:** Cero movimiento; el estado tras arrancar es DISARMED y sin homing restaurado (G1-5).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PWR-05
- [ ] **Acción:** Detener el latido WATCHDOG_HEARTBEAT (BCM11) con motores armados en banco sin carga mecánica.
- **Esperado:** El permiso de motores cae y los drivers quedan deshabilitados (EN alto).
- **Criterio de aprobación:** Tiempo de corte medido con osciloscopio y anotado; el diseño exacto del watchdog está sin seleccionar, no inventar un valor.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PWR-06
- [ ] **Acción:** Con el equipo sin energía retirar fusible o preparar apertura simulada por fixture de cada cable NC; reenergizar solo el circuito de prueba autorizado y observar el fallo.
- **Esperado:** Fallo explícito en el software y motores inhibidos.
- **Criterio de aprobación:** Cable abierto = nivel ALTO = fallo; nunca se interpreta como límite sano (LOW = sano).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PWR-07
- [ ] **Acción:** Medir ondulación y transitorios en VMOT y 5 V con osciloscopio (sonda de masa corta) durante aceleración y parada de los tres motores.
- **Esperado:** Picos y caídas dentro de lo admitido por drivers y CM5.
- **Criterio de aprobación:** Sin reinicios del CM5, sin fallo de driver; registrar pico a pico (puerta EMI de CM5-PCB).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PWR-08
- [ ] **Acción:** Mantener 30 min con los motores en movimiento lento alterno y medir temperatura con cámara térmica/termopar en drivers, DC/DC, fusible y conectores Powerpole.
- **Esperado:** Estabilización térmica sin deriva continua.
- **Criterio de aprobación:** Ninguna pieza supera el límite de su hoja de datos; caída de tensión en conectores < 50 mV por contacto a la corriente de uso.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

## DRV — Drivers de motor (TMC5160 v1.5 en CM5; TMC2209 en la portadora ESP32)

**Comportamiento esperado del componente.** Cada driver arranca DESHABILITADO (EN alto); solo se habilita con permiso hardware común y petición por eje. Los pulsos STEP/rampa los genera el driver (TMC5160 en modo rampa por SPI), nunca un bucle de Linux.

### DRV-01
- [ ] **Acción:** Sin motor, alimentar y leer por SPI (CS0 AZ, CS1 EL, CS2 POL) el registro de versión/IOIN de cada TMC5160.
- **Esperado:** Los tres responden con la versión de chip esperada.
- **Criterio de aprobación:** Respuesta válida en los tres CS; si no responde, revisar cableado SPI1 (MOSI BCM20, MISO BCM19, SCLK BCM21).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### DRV-02
- [ ] **Acción:** Con carga retenida y EN alto, comprobar nivel, estado del driver y corriente de fase con instrumentación apropiada, sin ordenar movimiento.
- **Esperado:** Excitación deshabilitada; puede existir cogging mecánico aun sin corriente.
- **Criterio de aprobación:** Inhibición y corriente residual según ficha/contrato; girar libre no demuestra por sí solo que EN funciona. No mover cargas sin retención.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### DRV-03
- [ ] **Acción:** Calcular la corriente de fase con Rsense y modelo exactos, configurar IRUN/IHOLD y medir RMS de fase con sonda/método apto para PWM chopper según LAB-08; la corriente DC de entrada o un DMM ordinario no son sustitutos.
- **Esperado:** Corriente RMS medida ≈ la calculada.
- **Criterio de aprobación:** Dentro de ±10 % y nunca por encima de la corriente nominal del motor; no copiar el valor de otra NEMA14.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### DRV-04
- [ ] **Acción:** Girar un eje exactamente 10 vueltas de motor por la rampa del driver y contar con marca/encoder.
- **Esperado:** Vuelta mecánica = pasos esperados (200 pasos × 16 micropasos × relación).
- **Criterio de aprobación:** Error acumulado < 1 paso de motor; verifica que no cuentas 256 micropasos interpolados como pasos reales.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### DRV-05
- [ ] **Acción:** Provocar fallo del driver (sobretemperatura simulada o desconectar una fase con el driver apagado) y observar FAULT_AZ_N/EL_N/POL_N (BCM24/25/26).
- **Esperado:** El fallo se señaliza y los motores se inhiben; no se reintenta solo.
- **Criterio de aprobación:** Fallo visible en estado del host y en la app; limpiar exige rehome.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### DRV-06
- [ ] **Acción:** Medir temperatura del driver tras 10 min a corriente de trabajo en caja cerrada.
- **Esperado:** Temperatura estable.
- **Criterio de aprobación:** Por debajo del límite de la hoja de datos con margen; si no, añadir disipador/ventilación y repetir.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

## SNS — Sensores: AS5600, finales de carrera NC, GNSS, brújula/IMU

**Comportamiento esperado del componente.** Un sensor ausente o fuera de rango produce fallo explícito, nunca un valor inventado. Un GNSS parado NO da rumbo.

### SNS-01
- [ ] **Acción:** Escanear el bus I2C1 con el multiplexor TCA9548A (0x70): seleccionar cada canal y leer el AS5600 (0x36).
- **Esperado:** Un AS5600 por canal; el reset del multiplexor (BCM13) recupera el bus.
- **Criterio de aprobación:** Identificar cada sensor aislándolo/alimentándolo individualmente por canal; dos dispositivos de igual dirección pueden dar el mismo ACK y el escaneo NO prueba unicidad.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SNS-02
- [ ] **Acción:** Leer STATUS (MD/ML/MH) y AGC del AS5600 con el imán a la distancia de montaje; girar 360°.
- **Esperado:** MD=1 (imán detectado), ML=MH=0, AGC en rango medio; ángulo monótono de 0 a 4095.
- **Criterio de aprobación:** Sin MH/ML en todo el giro; imán diametral centrado; invertir sentido si la rotación sale al revés.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SNS-03
- [ ] **Acción:** Comparar el ángulo del AS5600 con un goniómetro/indicador en 8 posiciones.
- **Esperado:** Lectura acorde con la referencia.
- **Criterio de aprobación:** Error ≤ 0,5° (resolución de 12 bits ≈ 0,088°); registrar desviación y holgura mecánica.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SNS-04
- [ ] **Acción:** Accionar cada final de carrera (AZ min/max, EL min/max, POL min/max) y observar BCM4, 5, 6, 7, 8, 9.
- **Esperado:** Sano = BAJO; accionado o cable cortado = ALTO.
- **Criterio de aprobación:** Los seis responden; el motor se inhibe en el sentido del límite; el software NO sustituye al tope físico.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SNS-05
- [ ] **Acción:** GNSS en exterior o ventana: esperar fijación y comparar UTC y posición con una referencia conocida; medir PPS (BCM27) con osciloscopio.
- **Esperado:** NMEA válido, PPS de 1 Hz.
- **Criterio de aprobación:** UTC con error < 1 s respecto a referencia; PPS estable; coordenadas y altura en las unidades que usa el software (altura en metros).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SNS-06
- [ ] **Acción:** Quitar la antena GNSS y observar el estado de hora/sitio en el host.
- **Esperado:** UTC/sitio pasan a no válidos tras el tiempo de gracia; seguimiento bloqueado.
- **Criterio de aprobación:** Aviso explícito y parada segura (G3-4); nunca se sigue con UTC viejo sin avisar.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SNS-07
- [ ] **Acción:** Brújula/IMU: apuntar la antena a un rumbo verdadero conocido (sol/referencia) con motores apagados y encendidos; anotar la diferencia.
- **Esperado:** Lectura estable y repetible lejos de metal.
- **Criterio de aprobación:** Desviación documentada con declinación corregida; si motores activos cambian la lectura, alejar el sensor (compás remoto).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

[Volver al índice](README.md)
