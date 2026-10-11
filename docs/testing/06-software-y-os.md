# Software, hosts CM5 e imagen del sistema operativo

Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.

## SW — Software, hosts CM5 e imagen del sistema operativo

**Comportamiento esperado del componente.** Todo el software se prueba en un ordenador de desarrollo antes de tocar hardware. Compilar o pasar pruebas NO valida cableado, mecánica ni RF.

### SW-01
- [ ] **Acción:** En la raíz del repositorio ejecutar: node --test "tests/*.test.cjs"
- **Esperado:** Todas las pruebas pasan (66 en la revisión del 2026-10-11).
- **Criterio de aprobación:** 0 fallos; cualquier fallo bloquea el resto de puertas.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SW-02
- [ ] **Acción:** Ejecutar: PYTHONPATH=.:radio:rotor python3 -m pytest -q tests/rotor tests/radio_host
- **Esperado:** Pruebas del controlador de rotor y del host de radio.
- **Criterio de aprobación:** 0 fallos (86 aprobadas en la revisión).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SW-03
- [ ] **Acción:** Compilar y ejecutar la lógica de control nativa (tests/control_logic/test_native) con g++ y Unity; ejecutar node scripts/engineering-report.cjs.
- **Esperado:** Lógica de límites/tiempo/estado y cálculos de ingeniería.
- **Criterio de aprobación:** 6/6 pruebas nativas; el informe de ingeniería no marca fallos.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SW-04
- [ ] **Acción:** Comparar SGP4 con una implementación independiente (mismo TLE, UTC y sitio) en 10 instantes de un pase.
- **Esperado:** Diferencia AZ/EL.
- **Criterio de aprobación:** ≤ 0,1° lejos del cénit (G0-3); mismas convenciones y geodesia.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SW-05
- [ ] **Acción:** Alimentar datos erróneos: TLE truncado, checksum malo, epoch viejo, nombres con HTML, fuente caída, catálogo demasiado grande.
- **Esperado:** Fallo explícito en cada caso.
- **Criterio de aprobación:** Sin movimiento y sin corromper la caché válida (G0-7).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SW-06
- [ ] **Acción:** Renderizar con OpenSCAD todas las piezas y comprobar malla cerrada, volumen y ausencia de componentes inesperados (incluidas las tapas con el logo en relieve).
- **Esperado:** Mallas estancas.
- **Criterio de aprobación:** Todas las piezas estancas; el render no sustituye la revisión de engrane, holguras y acceso de montaje (G0-5/6).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SW-07
- [ ] **Acción:** Grabar la imagen BricoHams OS (os/build-image.sh en Linux con Docker, o el workflow build-os.yml) en la tarjeta/eMMC y arrancar el CM5.
- **Esperado:** Aparece el banner BricoHams en consola y en /etc/issue; inicio de sesión local con bricohams / Brico123.
- **Criterio de aprobación:** Cambiar la contraseña con passwd en el primer acceso; SSH desactivado (puerto 22 cerrado: nmap/ss); sin secretos, claves ni Wi-Fi en la imagen. La imagen NO ha sido construida ni arrancada hasta hoy.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SW-08
- [ ] **Acción:** En el CM5 ejecutar gpiodetect/gpioinfo y seleccionar el /dev/gpiochipN que expone los offsets BCM congelados; arrancar el selector de perfil (rotor-only, radio-only, integrated).
- **Esperado:** Perfil instalado y marcador /etc/bricohams/profile solo tras éxito.
- **Criterio de aprobación:** Ningún servicio de módulo arranca solo; el holder de estado seguro arranca tras verificar el mapa GPIO; instalación fallida deja marcador pendiente.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

[Volver al índice](README.md)
