# Registro de validacion de la entrega

Revision documental y repeticion de pruebas del 2026-10-17:
[PROJECT-REVIEW.md](PROJECT-REVIEW.md). Los resultados siguientes son
historicos de sus respectivas revisiones, no ejecuciones nuevas de hardware.

## Expediente rellenable para ensayos fisicos

Disponibles el [plan de bancos de laboratorio](testing/09-laboratorio.md),
[cuaderno imprimible por ensayo](testing/laboratorio/cuaderno.html) y
[plantillas CSV de resultados, lecturas, equipos, calibraciones y componentes](testing/laboratorio/README.md).
Se incluyen procedimientos detallados de [NanoVNA](testing/10-nanovna.md),
[RF activa y techo de 25 W](testing/11-rf-potencia.md) y
[calibracion DC, sensores, mecanica y sistema](testing/12-calibraciones.md).
Copiar plantillas a un expediente nuevo antes de rellenar.
**Son formularios PENDIENTES, no mediciones realizadas ni liberacion
de PCB/motores/TX.** El registro historico siguiente permanece intacto.

Verificacion digital del paquete de laboratorio, 2026-10-17:
101 fichas, 398 filas BOM trazables, regeneracion y enlaces comprobados.
Cuaderno A4 de 186 mm de ancho util, 101 hojas sin desbordamiento de
ancho/alto en emulacion de impresion del navegador. Suite completa:
105 pruebas, 104 aprobadas, cero fallos y una omitida de OS/Linux.
Estos resultados validan formularios y contratos, **no mediciones fisicas**.

Fecha: 2026-10-10. Estado: base ESP32 digital validada; auxiliar CM5 rutada
(revision digital) pero BLOQUEADA para fabricacion y energizacion; aceptacion
fisica pendiente. Digital, fabricable y seguro operacionalmente son hitos distintos.

## Matriz de variantes

Los resultados de la base ESP32 (29 pruebas JVM) y los de CM5 (58 pruebas JVM, 377 contratos) pertenecen a generaciones distintas; ver la matriz en [README](../README.md). Los heredados no cuentan como aceptacion CM5.

## Ampliacion CM5: limites vigentes

Los resultados PCB/firmware/Android de la base ESP32 que figuran abajo
no validan la nueva auxiliar CM5 ni su guard independiente.

| Superficie nueva | Evidencia | Limite |
| --- | --- | --- |
| Documentacion modular y precios | Tres pruebas Node de enlaces y coherencia de precios aprobadas | No constituye presupuesto completo ni ensayo fisico |
| Auxiliar CM5 y guard | Revision digital ENRUTADA (KiCad 10.0.7; ERC 0, DRC 0, 0 conexiones pendientes, 377 comprobaciones de contrato; ver `hardware/cm5/reports/validation-summary.json`) con Gerbers/BOM/CPL generados. Revision anterior (solo mapa GPIO, 11 pruebas de contrato) superada | ERC/DRC con comprobaciones opcionales ignoradas (listadas en el JSON): no prueba ausencia de fallos. Potencia DNP, fusibles sin cualificar, convertidores externos sin seleccionar, sin ensayo fisico. **DO NOT ORDER / NO FABRICAR / NO ENERGIZAR** |
| Radio y rotor | Conexion al adaptador existente y nueve rutas reportadas; 57 pruebas offline reportadas con controlador explicito de prueba | Proveedor/BSP CM5 real y guard pendientes; no demuestra seguimiento fisico ni permiso TX |
| Controlador rotor CM5 | 29 pruebas offline reportadas, incluido enlace open_adapter y rechazo de proveedor ausente | No existe proveedor CM5 comisionado; no sustituirlo por simulacion en produccion |
| Receta BricoHams OS | Repeticion local: nueve pruebas OS aprobadas y una prueba Linux/Python omitida; agregado con documentos/precios 12 aprobadas, cero fallos, una omitida | Sin construccion pi-gen ni arranque CM5; servicio OS integrado deliberadamente no habilitado |
| Mecanica POL | Siete pruebas reportadas; siete piezas imprimibles y tres plantillas DXF presentes; alivio de tension exportado y malla cerrada reportada | 5:1 y 16000 incrementos/vuelta no son precision; limites suaves +/-80 grados, NC objetivo +/-85 y topes candidatos +/-90; holgura nominal cero exige verificacion de tolerancias |
| Android CM5 | 58 pruebas JVM, lint/assemble y firma v2 reportados; 33 advertencias lint sin errores. APK de 1208309 bytes y SHA-256 comprobados localmente | Sin prueba BLE/RF fisica; mapas/radar siguen offline sin mapeo OrbitSnapshot verificado |
| Masa y autonomia | Objetivos <=5 kg excluyendo solo bateria externa y dos horas | Pendientes de pesar/medir conjunto CM5 con tripode y cables |

**HOLD CM5:** no fabricar la nueva auxiliar ni activar motores/TX a partir
del mapa GPIO o de las pruebas de contrato. Faltan circuito de seguridad,
interfaces electricas calificadas y activos reales de fabricacion.

APK CM5 debug preservada fuera de los resultados de compilacion:
[PortableSatStation-CM5-debug.apk](../releases/android/PortableSatStation-CM5-debug.apk).
SHA-256:
`ed52e0881353d7542dda1fac5062b372e2ea4bb8489710edc98386ecf5a77dd7`.
El panel Android consulta siete rutas reales y muestra sus respuestas;
no convierte esos JSON en mapa/radar ni confirma posicion alcanzada por
recibir un ACK. Homing/calibracion CM5 remotos no se exponen porque requieren
confirmacion local de confianza.

## Resumen de la base ESP32 anterior

| Entrega | Resultado | Limite |
| --- | --- | --- |
| Agregado Node | 35/35 aprobadas | No mide latencia ni hardware |
| Firmware ESP32 | Compilado; Unity 6/6 y vector SGP4 real | Sin pairing/motores fisicos |
| Android | APK debug, 29 JVM, lint cero, firma verificada | Sin telefono BLE fisico |
| WebFlash | Bundle real, 9 comprobaciones, smoke navegador | Sin USB fisico ni Pages remoto |
| PCB | ERC/DRC/paridad/unconnected cero; Gerber reales | HOLD de fabricacion/operacion |
| CAD | Mallas y matematicas verificadas; branding unido | Montaje/par/viento no ensayados |
| RF | Documentacion y dimensiones iniciales | ROE/ganancia/aislamiento no medidos |
| Masa | BuildLight 3,130-3,200 kg antes de adicionales | INCUMPLE objetivo <=3 kg |

Los apartados siguientes incluyen el historial de integracion. Este
resumen prevalece para estado de entrega; los hashes identifican
revisiones concretas y no deben mezclarse al flashear.

**Ultimo agregado: 35/35 pruebas aprobadas, cero fallos.**
Se resolvieron la malla de tapa, el campo de espesor de cobre y el
fixture de solapamiento NVS. Los registros historicos de fallos mas
abajo se conservan para trazabilidad; no representan el resultado actual.
La entrega digital aun espera los informes finales PCB/WebFlash.
Los informes finales PCB/WebFlash/Android ya se recibieron; permanece
pendiente la aceptacion fisica, no la compilacion de esos artefactos.
No hay prueba fisica de antena/rotor/PCB ni ejecucion remota de Pages.
Se repitio el agregado tras incorporar firmware BLE, USB, transferencia
TLE, versiones compartidas y caja grande: 35/35 aprobadas. Las pruebas
Android JVM/compilacion se registran separadamente al finalizar la app.

Este registro distingue pruebas digitales de comportamiento fisico.
Los resultados finales de firmware y CAD se incorporan al completar
la integracion; mientras tanto no se declaran aprobados.

| Superficie | Evidencia actual | Estado |
| --- | --- | --- |
| Calculos de RF/engranajes/carga | Node.js 22.16.0, 5/5 pruebas | Aprobado aritmetica |
| Inspector de referencias OBJ/STL | 2/2 pruebas, no altera entrada ni supone unidades | Aprobado metadatos |
| Enlaces de documentacion | Enlaces locales resueltos, incluido CONTROL.md | Aprobado |
| Diagnosticos del calculador y pruebas | VS Code sin errores | Aprobado diagnosticos |
| PDF originales | SHA-256 en input-hashes.json, extraccion local Xpdf | Registrado |
| Firmware ESP32 | Compilacion satisfactoria del controlador; aprovisionamiento WebFlash en revision | Aprobado compilacion, no banco |
| Web AP | Prueba sintaxis/DOM/API y ocho acciones autenticadas | Aprobado digital; hardware pendiente |
| CAD / STL | 34 STL exportados; pruebas de matematica e inventario pasan | Digital parcial; masa en revision |
| Montaje mecanico | No se dispone del prototipo construido | Pendiente G1 |
| Antena/diplexor/hibridos RF | No se dispone de VNA del conjunto | Pendiente G2 |
| Seguimiento en campo | No se ha operado el equipo fisico | Pendiente G3/G4 |

## Herramientas del entorno

Inicialmente no habia Node, OpenSCAD, PlatformIO ni pdftotext disponibles
en PATH. La extension tampoco proporciono implementacion para configurar
el entorno Python. Se utilizo Node portable y Xpdf local en la carpeta
de artefactos de la sesion, no una instalacion global ni el directorio Intune.

Node 22.16.0: descarga oficial, ZIP contrastado contra SHASUMS256 oficial:

`21c2d9735c80b8f86dab19305aa6a9f6f59bbc808f68de3eef09d5832e3bfbbd`

Xpdf tools 4.06: `https://dl.xpdfreader.com/xpdf-tools-win-4.06.zip`.
Los PDF no se enviaron a terceros. Los dos PartIIRotatorcontrol tienen
el mismo SHA-256; se analizan como una fuente duplicada, no dos estudios.

## Comandos de calculo ejecutados

```powershell
node --test tests\engineering.test.cjs
node scripts\engineering-report.cjs
```

Resultado: 5 pruebas, 5 aprobadas, 0 fallos. El runner de tests integrado
de VS Code no descubrio las pruebas CJS; se ejecuto el runner nativo Node.

Ultima ejecucion integrada de scripts/validate.ps1: 12 pruebas,
12 aprobadas y 0 fallos. El anterior fallo de integracion por CONTROL.md
se resolvio al recibir la documentacion del control. La prueba web
comprueba sintaxis, DOM, esquema API, ocho acciones autenticadas y
renderizado seguro de nombres; no es prueba de un ESP32 fisico.
El inspector de metadatos paso sus 2 pruebas propias; OBJ/STL originales
se leen sin alterarlos. TDS_AV2040 requirio rasterizado local debido a
la codificacion corrupta del texto: las cifras se comprobaron visualmente.

La entrega mecanica inicial exporto 34 STL con OpenSCAD y comprobo
aristas cerradas/orientadas y volumen positivo. Las pruebas mecanicas
incluyen involutas, relacion 25:1, fase planetaria y 121 posiciones
de engrane ideal en seccion. No constituyen barrido completo de
colisiones de toda la estacion ni ensayos de montaje.

El calculo inicial de ASA equivalente completamente macizo fue
2,641 kg antes de sumar piezas metalicas. El objetivo de masa
<=3 kg no queda demostrado y se ha solicitado optimizacion de
geometria y presupuesto de masa completo. No presentar el valor
macizo como peso de una impresion con infill ni omitir la bateria.

Revision acotada: 2,521 kg ASA equivalente macizo, ahorro 120,45 g.
Presupuesto adicional 1,464-2,294 kg; escenario hipotetico de impresion
3,208-4,038 kg total sin radio/tripode. No cumple <=3 kg.
El usuario autoriza cambiar la transmision y priorizar peso. Nueva
variante ligera BASE con dos etapas GT2 20:100 ya generada; los resultados
anteriores corresponden a la variante planetaria y no validan
automaticamente la nueva.

Ultima ejecucion agregada antes de terminar PCB/WebFlash: 16 pruebas,
16 aprobadas y cero fallos. Incluye matematicas de correa, mallas nuevas,
auditoria de masa, documentacion y superficies de seguridad web.
Las comprobaciones de interbloqueos estaticas no son ensayos de latencia.

BASE: ASA equivalente macizo 0,862 kg; presupuesto 3,121-4,006 kg y
escenario hipotetico aligerado 2,905-3,790 kg. <=3 kg aun no demostrado.
Correas reversibles: equilibrio y retencion mecanica independiente necesarios.

Control compilado para ESP32-DevKitC V4/WROOM-32E, sin PSRAM:
PlatformIO 6.1.18, plataforma espressif32 6.10.0, Arduino 2.0.17.
La validacion del controlador registro 4 pruebas Unity y una comprobacion de
SGP4 con vector Vallado, satisfactorias. La version de firmware comunicada
con pinout PCB congelado tiene SHA-256
`99B550AF144C31B5B7918F3A5E17D245F108D1C602CB234E8E79358E066045B3`.
LittleFS comunicado tras atribucion:
`EDBDB2F968F6CC0DA83A04061E3806A4C7C403735B9C8C3EA44B897F62E8D9C2`.
Estos hashes identifican esa revision; cambios posteriores de
aprovisionamiento requieren recompilar y registrar hashes nuevos.

Carrier PCB en desarrollo: 180x130 mm, no cabe en la antigua caja
124x64 mm utiles. Integracion de una nueva caja solicitada; no declarar
encaje por compartir mapa GPIO. Gerber/ERC/DRC pendientes de informe.

Actualizacion de integracion: 28 pruebas Node agregadas, 28 aprobadas
y cero fallos, incluyendo caja nueva para carrier 180x130, presupuesto
de masa actualizado y pruebas de manifiesto/WebFlash. El resultado
no certifica PCB, flasheo USB ni GitHub Actions ejecutado remotamente.

El controlador incorpora aprovisionamiento USB local a 115200 baud
(`setup`, `config`, `carrier`, `reboot` en JSON), sin recompilar para
introducir credenciales. SETUP deshabilita motores/Wi-Fi/API e invalida
homing/calibracion; NVS no esta cifrada y requiere resguardo fisico.
Pruebas Unity comunicadas: 5/5. Ultimo binario comunicado en build
aislado tiene SHA-256:
`C413748CDDF16C3AFF782FF3663F93D7B9BB613DB90DAF1FD73C067CEF0771CE`.
La instalacion WebFlash debe reconstruir desde la misma revision y
emitir sus propios hashes verificables; no mezclar los historicos.
HTTPS permanece deshabilitado en imagen publica sin CA configurada;
importacion manual TLE disponible. No se ha ensayado USB fisico.

Ejecucion posterior con PCB y branding en integracion: 35 pruebas,
31 aprobadas y 4 fallos por triangulos degenerados en la nueva tapa
de caja. Se solicito corregir geometria/exportacion sin relajar el
validador. La tapa no esta aprobada mientras persista este fallo.
Las cinco pruebas de PCB aprobaron, incluyendo manifiesto SHA-256,
pinout de 38 pines y reportes ERC/DRC/paridad. Pendiente informe final
de propietario de PCB y revision fisica, no liberacion automatica.

Tapa corregida: exportacion binaria validada antes de reemplazar archivo;
9024 triangulos, un componente conectado y relieve de 0,7 mm.
SHA-256 comunicado:
`EC5806AA9FF4EB068FBC695D6CEEF794CD9DDE1DB68270D784114A5068320E34`.
Ultimo agregado: 35 pruebas, 33 aprobadas y dos fallos de integracion:
campo de espesor de cobre en test PCB y fixture WebFlash que falla
por cabecera invalida antes de alcanzar la prueba de solapamiento NVS.
Se solicito corregir la evidencia/fixture sin debilitar los criterios.
La aprobacion agregada final aun esta pendiente.

Caja final ampliada para cableado: interior 224x174 mm, exterior
228x178 mm y 32 mm sobre la PCB; 22 mm por borde. Cuatro STL y bandeja
240x196x2 mm regenerados y once pruebas mecanicas comunicadas aprobadas.
La tapa conserva branding integrado, un componente conectado.
El presupuesto BuildLight actualizado es 3,130-3,200 kg ANTES de
adicionales pendientes. **El requisito <=3 kg no se cumple en esta revision.**
No presentar anteriores escenarios inferiores como masa final validada.

PCB final: KiCad 10.0.7, ERC/DRC/paridad/conexiones pendientes cero;
180x130 mm, dos capas 2 oz, 40 componentes, 17349 segmentos y 55 vias.
Gerber reales de cobre/mascara/serigrafia/contorno, Excellon PTH/NPTH,
netlist y manifiesto SHA-256 exportados. ZIP:
`fabrication/PortableSatCarrier-Gerbers-CAD-VERIFIED-NOT-RELEASED.zip`.
HOLD de produccion/operacion por mediciones de modulos, parada DC
exacta y cualificacion fisica electrica/termica.

Ampliacion BLE/Android y calibracion guiada en desarrollo.
La app descargara TLE por HTTPS y los transferira por BLE; el ESP32
seguira siendo el calculador de pases/seguimiento. Requiere nuevo
binario y reconstruccion WebFlash con evidencia de la misma revision.

Firmware BLE final comunicado: NimBLE 1.4.3 (Apache-2.0), bonding,
MITM/cifrado y token; passkey por USB, BLE desactivado inicialmente.
Handlers HTTP/BLE compartidos, callback ensambla/encola y no ejecuta
filesystem/SGP4 pesado. TLE begin/chunk/commit/abort con longitud,
SHA-256 y offsets secuenciales; lista de satelites paginada.
Versiones congeladas: apiVersion=1, protocolVersion=1,
firmwareVersion=0.2.0-prototype (la build 0.3.0-prototype con API 2 y el perfil
`esp32_nema17` compila, pero no tiene medidas de placa ni rotor).
Build controlador comunicado: flash 1199509 bytes, RAM estatica
59084 bytes. SHA-256 firmware:
`64194FB5A0FBDB16D5ECBB6233F56D88C587E91C998A8E8A4F621B9C6C185DD3`.
Unity 6/6 comunicadas aprobadas; Node control 3/3.
No prueba fisica de pairing, latencia BLE ni coexistencia Wi-Fi/motores.

Revision final de transferencia: desconexion BLE aborta inmediatamente
upload en RAM y libera propietario, conservando cache persistida.
Firmware recompilado comunicado SHA-256:
`143A541D86F87922459371FB4F7E5C2B615AC8932382A9E2521BDFC0362EFF81`.
Este hash sustituye al anterior para esa revision; WebFlash debe
reconstruirse con el mismo cambio. Importar TLE no requiere fix GNSS,
pero iniciar seguimiento sigue exigiendo UTC/sitio/TLE validos.

Validacion con proveedor real: AMSAT HTTPS devolvio un catalogo que
incluye signo de exponente positivo en blanco. Se ajustaron parser
controlador y app sin modificar lineas ni relajar checksum. Unity 6/6
y comprobacion de SGP4 real comunicadas aprobadas.
Firmware comunicado tras correccion:
`549B1DAB4121E490E355D6259675483B8C752780CF0B7A52CDEB4CBC568BAD02`.
Descarga ejecutada por el codigo Android: 14434 bytes, 97 satelites
validos, SHA-256:
`ec291294636090d712fc901e4a7e3fa15bbeb8366fb771d7aad131b5c8db1ce9`.
CelesTrak y PE0SAT dieron timeout en la comprobacion de escritorio;
se conserva cache y no se deshabilita TLS. La disponibilidad futura
de los proveedores no esta garantizada por esta prueba.

WebFlash final: build real y bundle generados desde el arbol de
fuentes actual, incluyendo cabecera con fix AMSAT. Nueve comprobaciones
con artefactos reales aprobadas y smoke local de navegador (HTTP 200,
gate de advertencias e imports locales del dialogo), sin abrir USB.
Firmware del bundle coincide con SHA-256 `549B1D...BAD02`.
LittleFS SHA-256:
`866C1AF7C5B1FFE96C5DCC4DCF8C692383DDDE28FEF7C772581148DC37D12256`.
Metadatos del bundle enlazan fuentes/config/UI, versiones de paquetes
y lock npm. Flash usada 1199553 bytes, RAM estatica 59084 bytes.
LittleFS puede variar entre builds por metadatos; se valida su hash
real, no se supone reproducibilidad binaria.

ESP Web Tools requiere `new_install_prompt_erase=true` para mostrar
opcion de borrado inicialmente desmarcada; false puede borrar
automaticamente dispositivos no Improv. Advertencia y confirmacion
conservadas. Pages requiere variable de aprobacion prototype-only y
entorno protegido con revision; no se publico ni ejecuto GitHub CI.

## Android final

APK: `android/app/build/outputs/apk/debug/app-debug.apk`, 980724 bytes.
SHA-256:
`47997a78abd87b3aa4e26a33106f9b122a817121dd02c2abc7d6b72717ca399b`.
Build satisfactorio, 29 pruebas JVM sin fallos, lint cero incidencias
y verificacion de firma debug aprobada. No es una firma release ni
distribucion en tienda. La CI preparada permite regenerar artefactos;
el directorio build no forma parte del codigo versionado.

Descarga HTTPS limitada a los tres proveedores, importacion de archivo,
cache privada atomica, transferencia completa/seleccionada por BLE,
preflight de estado del rotor, consulta de pases hasta 60 y hora UTC.
Credenciales cifradas con Android Keystore; permiso INTERNET usado para
descarga autorizada, sin subir token ni datos privados a proveedores.
El rotor sigue calculando SGP4 y no recibe trayectoria del telefono.
Prueba con AMSAT real aprobada; timeouts de CelesTrak/PE0SAT documentados.
No se ha probado Android, BLE y motores en un conjunto fisico.

El ejemplo de viento de 8 m/s FALLO el presupuesto de par con margen 2.
La prueba PASA precisamente porque detecta este limite; no valida operar
en ese viento.

## Interpretacion

Una biblioteca orbital compilada no confirma el cableado, la precision
de sensores ni un seguimiento completo sin pruebas de banco.
Una malla exportada no confirma encaje, montaje, resistencia o engrane.
Las dimensiones iniciales no son una garantia de adaptacion/ganancia RF.
Los limites pendientes estan descritos en ACCEPTANCE.md y RISKS.md.

## Verificacion 2026-10-11 (entorno de revision, sin hardware)

| Suite | Resultado | Notas |
| --- | --- | --- |
| `node --test "tests/*.test.cjs"` | 66/66 | `npm test` corregido para Node 22 |
| `pytest tests/rotor tests/radio_host` | 86 aprobadas | helper `test_controller` renombrado (pytest lo recogia como prueba); `PYTHONPATH=.:radio:rotor` |
| Logica de control nativa (Unity, g++) | 6/6 | `tests/control_logic/test_native` |
| Render OpenSCAD 2021.01 de las piezas con logo | estancas | 4 piezas |
| JVM Android, KiCad ERC/DRC, `control_sgp4.cpp`, imagen OS | **no ejecutados** | sin red para Gradle, sin KiCad, sin libreria SGP4 fijada, sin Docker/espejos Debian |
