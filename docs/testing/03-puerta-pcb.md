# Puerta previa a fabricar las PCB

Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.

## PCB — Puerta previa a fabricar las PCB (portadora ESP32 y cm5-guard-A)

**Comportamiento esperado del componente.** No se pide ni se fabrica ninguna placa hasta que cada punto de esta puerta esté APROBADO con medida y fecha. Un ZIP Gerber o un render no sustituyen ERC/DRC ni el banco.

### PCB-01
- [ ] **Acción:** Abrir cada proyecto en KiCad y ejecutar ERC, DRC, "unconnected items" y paridad esquema/PCB con la versión documentada.
- **Esperado:** Cero errores y cero advertencias sin justificar.
- **Criterio de aprobación:** Informe guardado en reports/; el logo de serigrafía añadido por script exige repetir DRC (pendiente en esta revisión).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PCB-02
- [ ] **Acción:** Comprobar que cada archivo de fabricación coincide con su SHA-256 de reports/manifest-sha256.json y fabrication/release-status.json (sha256sum).
- **Esperado:** Todos los hashes coinciden.
- **Criterio de aprobación:** Cualquier diferencia = no fabricar; regenerar manifiesto con el script del repositorio.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PCB-03
- [ ] **Acción:** Cargar los Gerber en un visor independiente (KiCad Gerber Viewer, Tracespace o gerbv) y revisar capas, taladros, contorno y logo BricoHams en serigrafía.
- **Esperado:** Capas completas, logo legible sin solapar pads ni agujeros.
- **Criterio de aprobación:** Holgura del logo ≥ 8 mm (carrier) y ≥ 21 mm (guard-A) según BRANDING.md; sin serigrafía sobre pads.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PCB-04
- [ ] **Acción:** Montar el circuito equivalente en banco (módulos reales + cableado de prototipo) para cada bloque: alimentación, drivers, sensores, parada/watchdog.
- **Esperado:** Cada bloque cumple las pruebas PWR, DRV y SNS en el banco.
- **Criterio de aprobación:** Todas las pruebas de esas secciones APROBADAS antes de pedir la placa.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PCB-05
- [ ] **Acción:** Con el comprobador del contrato GPIO (banco, ver BANCO) recorrer las 26 señales de interface.json: cada salida mueve su LED, cada entrada responde a su interruptor.
- **Esperado:** Las 26 señales coinciden con BCM, pin de cabecera y nivel seguro por defecto.
- **Criterio de aprobación:** Cero señales cruzadas o duplicadas; todas las salidas en su nivel seguro tras reinicio.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PCB-06
- [ ] **Acción:** Revisar huellas contra hojas de datos: pin 1, orientación y paso de DevKitC, SilentStepStick, MCP23017, TCA9548A, conectores y fusibles; imprimir el PCB a escala 1:1 en papel y apoyar los módulos reales.
- **Esperado:** Todas las huellas encajan físicamente.
- **Criterio de aprobación:** Ningún módulo choca con otro, con tornillos de carcasa ni con la tapa (G1E-12).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PCB-07
- [ ] **Acción:** Revisar el presupuesto de corriente de trazas y pistas de potencia (ancho, cobre, caída) con la corriente de los tres motores y el fusible.
- **Esperado:** Caída y temperatura calculadas dentro de límite.
- **Criterio de aprobación:** Calculado y confirmado por medida en el banco (PWR-02, PWR-08).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### PCB-08
- [ ] **Acción:** Preparar el pedido: BOM, CPL (referencias, coordenadas, lado, rotación), lista DNP/módulos manuales, DFM del fabricante y confirmación de piezas LCSC exactas.
- **Esperado:** Pedido sin advertencias DFM bloqueantes; ningún pedido enviado sin aprobación explícita.
- **Criterio de aprobación:** Todo APROBADO y revisado por una segunda persona; no pagar hasta cerrar PCB-01…07.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

[Volver al índice](README.md)
