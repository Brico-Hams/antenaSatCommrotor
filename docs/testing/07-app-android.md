# Aplicación Android

Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.

## APP — Aplicación Android (marca, ayuda, descarga de TLE y sincronización BLE)

**Comportamiento esperado del componente.** La app descarga TLE por HTTPS desde CelesTrak, AMSAT o PE0SAT y los guarda en una caché privada validada; solo el controlador calcula órbitas. La transferencia a la Raspberry/rotor es BLE local, con detección de bloqueo de 60 s, y la última caché válida nunca se sobrescribe si falla.

### APP-01
- [ ] **Acción:** Instalar el APK debug (GitHub Actions android.yml) en un teléfono Android 8-11 y otro Android 12+; abrir la app.
- **Esperado:** Aparece el logotipo BricoHams, la línea de autores (Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina) y bricohams.org; el icono del lanzador es el logo BH.
- **Criterio de aprobación:** Logo visible en las tres pantallas (principal, receptor digital, radio host) y en Ayuda; sin recortes en modo oscuro/claro.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-02
- [ ] **Acción:** Pulsar Ayuda en cada pantalla con el teléfono en español, inglés y húngaro.
- **Esperado:** Se abre el texto de ayuda de la pantalla en el idioma del teléfono (es, en o hu); sin red.
- **Criterio de aprobación:** Ayuda legible y sin errores; el nombre de los botones citados coincide con la interfaz (la interfaz está en es/en; el húngaro cita ambos).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-03
- [ ] **Acción:** Con Internet, probar los tres proveedores (CelesTrak, AMSAT, PE0SAT) uno a uno con Descargar TLE.
- **Esperado:** Progreso en bytes y mensaje "descarga completa"; catálogo en la lista local; un proveedor caído o bloqueado muestra un mensaje claro (tiempo agotado, límite de uso o redirección).
- **Criterio de aprobación:** Entradas > 0 con epoch reciente en al menos un proveedor; anote en el registro cuál de los tres (CelesTrak, AMSAT, PE0SAT) responde desde su red y cuáles no.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-04
- [ ] **Acción:** Repetir la descarga de CelesTrak varias veces seguidas y luego en modo avión.
- **Esperado:** Tras varias descargas seguidas CelesTrak puede devolver 403/429; en modo avión falla por red.
- **Criterio de aprobación:** Mensaje específico de límite de uso (esperar unas horas/otro proveedor) o de descarga fallida; la última caché válida se conserva; ningún "TLE inválido: tle_http_…" engañoso.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-05
- [ ] **Acción:** Importar un archivo TLE local válido, luego uno con checksum malo, uno truncado y uno con líneas con espacios finales.
- **Esperado:** Válido y con espacios finales: se importan; malo/truncado: error explícito.
- **Criterio de aprobación:** La caché solo cambia tras validación y reemplazo atómico; los errores muestran el motivo.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-06
- [ ] **Acción:** Descargar un catálogo con más de 100 satélites.
- **Esperado:** Se pide elegir un subconjunto (máximo 100).
- **Criterio de aprobación:** Con 101 marcados el diálogo rechaza; con ≤ 100 se guarda.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-07
- [ ] **Acción:** Escanear rotores (15 s), seleccionar explícitamente el rotor, confirmar el passkey y guardar el token cifrado.
- **Esperado:** Conexión autenticada con versiones verificadas.
- **Criterio de aprobación:** Mensaje "Autenticado y versiones verificadas"; conectar NO habilita motores. Si falla con error 133 la app reintenta hasta 2 veces antes de avisar.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-08
- [ ] **Acción:** Con la hora UTC válida y modo READY/DISARMED, pulsar Transferir catálogo; observar el progreso en bytes hasta "transferencia completa".
- **Esperado:** Los TLE llegan al controlador (Raspberry/CM5); el host muestra el catálogo actualizado en el mismo orden.
- **Criterio de aprobación:** Tiempo total anotado (≈ 512 caracteres por trozo sobre tramas de 20 bytes); hash del catálogo coincide en app y host; sin errores de offset.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-09
- [ ] **Acción:** Durante la transferencia apagar el rotor o alejar el teléfono; esperar 60 s sin avance.
- **Esperado:** La transferencia se cancela y se desconecta con mensaje de tiempo agotado; en el controlador el catálogo anterior sigue intacto.
- **Criterio de aprobación:** El catálogo previo del host no se altera (transferencia atómica con commit); se puede reintentar tras reconectar.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-10
- [ ] **Acción:** Elegir un satélite del catálogo del controlador y consultar pases; comparar AOS/LOS con una referencia independiente (misma estación y TLE).
- **Esperado:** Pases coherentes; el cálculo lo hace el controlador, no el teléfono.
- **Criterio de aprobación:** Diferencia de AOS/LOS < 30 s; límite de consultas de pase informado al usuario si el cálculo no termina.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### APP-11
- [ ] **Acción:** Receptor digital: reproducir un WAV SSTV y uno APRS 1200 baudios por altavoz/cable hacia la entrada de audio del teléfono.
- **Esperado:** Imagen SSTV y paquetes AX.25 decodificados; registro guardable.
- **Criterio de aprobación:** Decodificación correcta con nivel de audio razonable; sin TX desde la app.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

[Volver al índice](README.md)
