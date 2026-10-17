# BricoHams: revision del proyecto y cobertura de verificacion

Fecha: **2026-10-17**. Revision local del arbol de trabajo.
Este informe no es una certificacion, una auditoria de seguridad ni
una aceptacion fisica de la estacion.

## Resultado y alcance

- Revisados estructura, variantes, BOM, validadores, guias de montaje,
  instalacion, branding y estados declarados.
- Completadas las cinco guias de montaje por modulo/conjunto y creada la
  [guia visual de instalacion](assembly/06-instalacion.md).
- Creadas **328 fichas SVG**, una por fila de **ocho BOM**, con ID,
  cantidad, especificacion, fuente/fila y marca BricoHams. Se incluyen
  referencias LEGACY, alternativas y herramientas, identificadas como tales.
  No son 328 piezas distintas obligatorias ni fotografias de productos.
- Conservados los despieces CAD y las vistas PCB existentes: no se han
  regenerado mallas ni alterado cobre, pinouts o rutas de potencia.
- Corregidas **34 filas CSV** con comas internas sin entrecomillar:
  seis en la BOM multimodo y 28 en POL. Se conserva el texto tecnico;
  ahora la importacion mantiene sus ocho y siete columnas respectivamente.
- Actualizado el orden de construccion para no recomendar el planetario
  LEGACY por defecto y separados los recorridos ESP32 y CM5.
- La documentacion ampliada esta en espanol. Los indices ingles y hungaro
  enlazan esta revision; no se declaran traducciones completas nuevas.

## Mapa del proyecto: donde esta documentado cada punto

| Area | Referencia principal | Comprobacion / limite |
| --- | --- | --- |
| Arquitectura y requisitos | [ARCHITECTURE](ARCHITECTURE.md), [REQUIREMENTS](REQUIREMENTS.md) | Separar BASE ESP32, ampliacion CM5 y PortableSatLite |
| Componentes y compras | [Catalogo visual](assembly/components/README.md), [REFERENCE-PRICES](REFERENCE-PRICES.md) | Cobertura por fila, no presupuesto completo ni aprobacion de partes TBD |
| Antena y redes RF | [Modulo antena](MODULE-ANTENNA.md), [RF-AND-RADIO](RF-AND-RADIO.md) | Ajuste VNA, fase, mano, aislamiento y emisiones pendientes de banco |
| Rotor BASE | [Montaje rotor](assembly/01-rotor.md), [MECHANICAL](MECHANICAL.md) | GT2 25:1; validar ajustes, retencion, carga y precision real |
| Tercer eje POL | [POLARIZATION-MECHANICAL](POLARIZATION-MECHANICAL.md) | Concepto 5:1, no cambia RHCP/LHCP; recorrido no aprobado |
| Alimentacion y sensores | [Montaje electronica](assembly/04-electronica.md), [ELECTRICAL](ELECTRICAL.md) | No cablear desde pictogramas; fusibles/convertidores requieren cualificacion |
| PCB ESP32 | [PCB](PCB.md), [puerta PCB](testing/03-puerta-pcb.md) | HOLD; revisar revision exacta y archivos despues del branding |
| Auxiliar CM5 | [CM5-PCB](CM5-PCB.md), [DESIGN-REVIEW](../hardware/cm5/DESIGN-REVIEW.md) | NO FABRICAR / NO ENERGIZAR; mapa GPIO no libera interconexion |
| Control ESP32 y AP | [CONTROL](CONTROL.md), [WEBFLASH](WEBFLASH.md) | Contratos/sintaxis Node no sustituyen compilacion ni placa fisica |
| Host rotor CM5 | [CM5-ROTOR](CM5-ROTOR.md), [rotor](../rotor/) | Proveedor/BSP y guard comisionados pendientes |
| Host radio y audio | [RADIO-HOST](RADIO-HOST.md), [radio](../radio/) | Doble RX previsto; TX unico, permiso fisico y PA/filtros pendientes |
| Sistema operativo | [BRICOHAMS-OS](BRICOHAMS-OS.md), [os](../os/) | Receta, no imagen CM5 arrancada/verificada; cambiar contrasena inicial publica |
| Android | [ANDROID](ANDROID.md), [matriz](ANDROID-FEATURE-MATRIX.md), [digital](ANDROID-DIGITAL.md) | Distinguir JVM, APK y telefono/BLE/audio fisicos |
| Montaje, cajas y marca | [Ensamblaje](assembly/README.md), [BRANDING](BRANDING.md) | Identificacion visual, no plano liberado ni prueba de encaje |
| Conjunto y operacion | [Integracion](assembly/05-integracion.md), [FIELD-MANUAL](FIELD-MANUAL.md) | Pesar <=5 kg sin bateria externa; autonomia de dos horas no acreditada |
| Pruebas y diagnostico | [testing](testing/README.md), [TROUBLESHOOTING](TROUBLESHOOTING-MULTIMODE.md) | Medida, instrumento, fecha y operador para cada aceptacion fisica |
| Subproyecto Lite | [PortableSatLite](../PortableSatLite/README.md) | Arquitectura, scripts y pruebas independientes; no transferir resultados BASE |
| Licencias y procedencia | [NOTICE](../NOTICE.md), [SOURCES](SOURCES.md), [AUTHORS](../AUTHORS.md) | Conservar autores, restricciones y avisos de terceros |

## Verificacion repetida en esta revision

Entorno: Windows, Node.js **22.23.3**.
El runner integrado de pruebas no descubre los CJS, por lo que se utiliza
el runner nativo ya adoptado por el proyecto.

| Comprobacion | Resultado | Que demuestra |
| --- | --- | --- |
| Validacion Node inicial, antes de cambios | 72 pruebas: 71 aprobadas, 0 fallos, 1 omitida | Estado inicial reproducido |
| Validacion Node final y calculos | 78 pruebas: 77 aprobadas, 0 fallos, 1 omitida; informe de ingenieria generado correctamente | Regresion de contratos, CAD/inventario, PCB, web, WebFlash, OS y documentacion |
| Catalogo de componentes | 328 SVG generados desde ocho BOM | Cada fila dispone de una ficha; especificacion y enlaces trazables |
| Nuevas pruebas de catalogo/guias | Parser, estructura BOM, regeneracion exacta, branding, enlaces e instalacion | Sincronizacion documental y ausencia de columnas desplazadas |
| XML de ilustraciones | Los 328 SVG se leen con el parser XML de PowerShell | Documentos XML bien formados |
| Revision en navegador | Ficha MMA-013 visible con logo, especificacion y avisos, sin textos fuera del ancho | Muestreo visual de una ficha larga, no inspeccion manual de las 328 |
| Android | `testDebugUnitTest lintDebug assembleDebug`: BUILD SUCCESSFUL; 59 pruebas JVM, cero fallos/omisiones; lint: 35 advertencias, cero errores | Compilacion/APK y pruebas de escritorio; no telefono, BLE ni RF fisicos |
| Hosts Python radio y rotor | 86 pruebas, cero fallos y cero omisiones, con Python 3.11.9 | Comportamiento offline, DSP y simuladores/adaptadores de prueba; no hardware de produccion |

Comandos reproducibles desde la raiz:

```powershell
.\scripts\validate.ps1
node scripts\component-catalog.cjs --check
```

Para repetir los hosts Python en un entorno local con sus dependencias
declaradas ya instaladas:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests\radio_host
.\.venv\Scripts\python.exe -B -m unittest discover -s tests\rotor
```

La integracion Python del editor no estaba disponible. Se encontro un
interprete aislado existente, pero su primer intento fallo por dependencias
ausentes. Se creo `.venv` local con virtualenv oficial de PyPA y se
instalaron los dos proyectos con sus manifiestos, sin modificar paquetes
globales. Versiones usadas: NumPy 2.4.6, SciPy 1.17.1, dbus-next 0.2.3,
SGP4 2.25, smbus2 0.5.0 y pyserial 3.5. La captura de `pip freeze` queda
en el entorno ignorado como `validation-requirements.txt`, no como una
nueva politica de dependencias de produccion.

La comprobacion POL que antes buscaba texto CSV sin comillas se adapto a
columnas parseadas: verifica las mismas dos unidades SDR y su especificacion,
sin volver a exigir el formato defectuoso.

La omision Node corresponde al ensayo de configuracion OS reservado a
Linux/Python. No se contabiliza como aprobado. Los numeros historicos de
[VALIDATION](VALIDATION.md) corresponden a otras revisiones; no deben
sumarse como ejecuciones nuevas.

Para Android se reutilizaron JDK 17.0.16 y SDK/caches locales existentes,
sin descargas, con el wrapper en modo `--offline --no-daemon`. Las rutas de
herramientas se pasaron por variables de entorno, no se incorporaron al
proyecto. La APK debug nueva permanece en el directorio de compilacion
ignorado; no reemplaza el artefacto historico de `releases/`.
SHA-256 de esa compilacion:
`a99d052dc2bde15721bdd6fd1f416697a691a59bcfc7d3de38a55d74b9a6623c`.

## Superficies que necesitan herramientas o hardware adicionales

| Superficie | Situacion de esta revision | Como cerrar |
| --- | --- | --- |
| Proveedor CM5 y contratos electricos fisicos | Suites offline aprobadas; proveedor real y hardware no comisionados | Los ensayos de GPIO/guard/PCB de produccion requieren KiCad/Linux y banco aparte |
| Android en dispositivo | JVM/lint/APK correctos; las 35 advertencias lint existentes no se han corregido como parte de esta ampliacion documental | Ejecutar permisos, reconexion, BLE/audio y aceptacion sobre telefono real |
| Firmware ESP32 / Unity | Dos intentos con PlatformIO local: fallo del toolchain Xtensa `CreateProcess: No such file or directory`, incluso con su binario en PATH y un solo trabajo | Reparar instalacion del toolchain, repetir build y Unity; no hay binario nuevo aprobado |
| CAD / STL | Inventario y contratos Node, no nuevas exportaciones OpenSCAD ni analisis de todas las mallas | OpenSCAD y herramientas del manual mecanico; inspeccion y primer articulo |
| PCB ERC/DRC y Gerber | No repetidos: KiCad CLI no disponible en PATH | Reexportar desde KiCad, revisar branding y renovar evidencia/manifiestos |
| OS Linux / pi-gen | No construido ni arrancado | Linux/Docker segun receta, checksum de imagen, primer arranque CM5 y banco |
| RF y mecanica real | Sin prototipo ni instrumentos conectados | Completar G0-G4 y registro de pruebas; no aprobar por simulacion |

No se han instalado herramientas globales, encargado PCB, escrito discos,
flasheado dispositivos, activado motores/TX ni publicado cambios.

## Pendientes que la documentacion no puede resolver

1. Liberar circuito, conectores, fusibles, convertidores, guard y proveedor
   real CM5; repetir ERC/DRC y correspondencia esquema/PCB/Gerber/BOM/CPL.
2. Seleccionar motores/sensores/accesorios exactos; medir encaje, limites,
   carga, retencion, holgura y comportamiento ante fallo.
3. Cualificar PA lineales, filtros, audio y red RF, incluidos armonico de
   145 MHz en 435 MHz, desensibilizacion y un unico TX activo.
4. Validar GNSS/UTC/norte, seguimiento real, Bluetooth, funciones Android
   y decodificacion con señales y equipos fisicos.
5. Pesar conjunto completo, medir autonomia y cerrar presupuesto. Datos
   TBD no se convierten en coste/masa cero.
6. Sincronizar traducciones EN/HU con las ampliaciones ES y comprobarlas.

## Limpieza editorial y trazabilidad

Se retiraron referencias a herramientas de redaccion y coordinacion en
los textos tecnicos, sin atribuir pruebas nuevas ni eliminar avisos.
Los tres exportadores CAD ahora usan `node` de PATH o el parametro
`-Node`, no una ruta privada fija; se mantiene el parametro `-OpenSCAD`.
Las fuentes locales se identifican por sus hashes, no por directorios
privados de trabajo. En
[commands.json](../hardware/cm5/reports/commands.json) solo se normalizo
el ejecutable a `kicad-cli.exe`; los argumentos y codigos de salida
historicos se conservan. Su entrada SHA-256 se actualiza en el manifiesto;
esto no equivale a volver a ejecutar KiCad.

Se conservan sin alterar las restricciones de licencias de terceros,
incluidas las referencias de procedencia que forman parte de esas
restricciones. No se ha reescrito el historial Git.

## Ampliacion posterior: tres antenas TX/RX y techo de 25 W

Los numeros anteriores describen la revision inicial; los siguientes
corresponden a la ampliacion de antenas realizada el mismo dia.

- [PF-01](ANTENNA-PORTABLE.md): boom unico, cuatro cassettes abatibles,
  puntas VHF retirables y cuatro cuadrantes de reflector flexible.
  Corregida una interferencia real del primer apilado desplazando
  pivotes y orejas, sin adelgazar mas las raices. Objetivo actualizado
  de transporte 170 x 140 x 300 mm; envolvente calculada con margen
  162 x 134 x 292 mm. Incluye solo una reserva para el tejido recogido.
- [Eggbeater](ANTENNA-EGGBEATER.md) y [QFH](ANTENNA-QFH.md): cuatro
  modelos separados a 145/435 MHz, CAD parametrico, ocho vistas
  geometricas, cuatro previews CAD, dos BOM y cupon de soporte.
  Formulas originales analiticas; no son simulaciones EM ni redes RF
  liberadas. No se afirma una envolvente de transporte comprobada.
- [Comparativa](ANTENNA-OPTIONS.md) y [previos RX](ANTENNA-PREAMPS.md):
  guias con secuencia visual de montaje y bypass/interbloqueo TX.
  La BOM comun no selecciona componentes sin fichas y ensayo.
- [Contraste AMSAT](SATELLITE-COMMS.md): repetidores FM, transpondedores
  inversores LSB/USB, frecuencias, Doppler y restricciones de consulta.
  El techo de 25 W no eleva ratings de los filtros/hibridos QRP anteriores
  ni modifica firmware/PTT. PA, proteccion RX y potencia siguen en HOLD.

| Comprobacion repetida | Resultado | Limite |
| --- | --- | --- |
| Validacion Node completa y calculos | **98 pruebas: 97 aprobadas, 0 fallos, 1 omitida**; informe de ingenieria generado | La omision sigue siendo Linux/Python OS; no se ocultan fallos |
| Catalogo visual actual | **398 SVG desde 12 BOM**, regeneracion exacta | Filas de alternativas/herramientas, no 398 compras obligatorias |
| XML de imagenes | **413 SVG** nuevos/de catalogo parseados correctamente | No equivale a comprobar RF |
| PF-01 CAD | Hub y brazo cerrados, una componente; `hinge-clearance` y `stow-clearance` vacios | Bisagra muestreada cada 5 grados; apilado nominal sin tornilleria/coax reales |
| Alternativas CAD | Cuatro renders 1200 x 800; cupon de soporte cerrado, una componente | Conductores y soportes candidatos, no ensamblaje estructural liberado |
| Aros/helices | Ecuaciones, aberturas, cantidades y separacion entre lazos verificados sobre los segmentos CAD | No prueba impedancia, polarizacion, patron o potencia |
| PNG | Nueve renders decodificados, dimensiones y pixeles de geometria comprobados | No se usa tamano comprimido como prueba de imagen no vacia |
| Navegador | Cuatro isometricas y dos diagramas sin texto fuera del lienzo; inspeccion de QFH y bypass | Muestreo visual, no ensayo fisico |
| Fuentes AMSAT | Frecuencias contrastadas con listados FM/lineales y buenas practicas; calculos 25 W revisados | El estado de cada satelite se consulta antes de cada pase |

No se recompilaron Android/Python/ESP32 por cambios de CAD/documentacion:
los resultados de sus ejecuciones anteriores siguen siendo historicos,
incluido el bloqueo del compilador ESP32. No se ordenaron placas, no
se flasheo hardware ni se transmitio. La aceptacion mecanica y RF exige
prototipo, instrumentos, componentes identificados y operador autorizado.
