# Fuentes, trazabilidad y permisos

Consulta: **10 de octubre de 2026**. Investigación pública y lectura local; no se han enviado los PDF del usuario ni sus textos a servicios externos. Las conclusiones son del diseño nuevo PortableSatStation, no una homologación de los proyectos citados.

## Licencias del proyecto nuevo: elección expresa del usuario

El **software original** de PortableSatStation se licencia **MIT** y el **hardware original** **CERN-OHL-S-2.0**, conforme a la elección del usuario. Los textos de licencia y el `NOTICE` de ámbito del proyecto determinan los archivos cubiertos. Esta elección **no cambia las licencias de terceros**: una biblioteca SGP4, documentación o pieza externa conserva sus avisos/licencia y debe ser compatible con la distribución prevista. No se ha realizado publicación remota.

Las referencias analizadas aquí no se redistribuyen como assets originales: no se incorporan fuentes de licencia desconocida, PDF completos, modelos comerciales, Gerbers ajenos ni código GPL para después etiquetarlos MIT. Si se incorpora más adelante material externo, registrar origen, revisión, licencia y modificaciones en `NOTICE` y cumplir sus obligaciones antes de distribuir.

### Dependencia SGP4 seleccionada: licencia comprobada

`firmware/platformio.ini` fija **Hopperpop/Sgp4-Library** al commit **`7c82d31f9d9a286acde5ef55da8308fc93d2ba96`**:

- La revision del controlador confirmó también la copia descargada: biblioteca **1.0.3**, mismo commit y licencia MIT, sin marcadores GPL en sus fuentes inspeccionadas. Esta comprobación local coincide con la consulta pública, no sustituye el inventario de licencias del resto del firmware.
- Fuente/versionado: <https://github.com/Hopperpop/Sgp4-Library/tree/7c82d31f9d9a286acde5ef55da8308fc93d2ba96>.
- `LICENSE` consultada directamente: <https://github.com/Hopperpop/Sgp4-Library/blob/7c82d31f9d9a286acde5ef55da8308fc93d2ba96/LICENSE>; blob **`853b46db127831eb9f8e8a7a8576e41c98619be4`**.
- La licencia raíz es **MIT**, no GPL. Su línea de copyright dice literalmente «Copyright (c) 2016» sin titular nombrado; conservar el aviso original sin inventar autor. El README acredita código original de David Vallado y transformaciones de Grady Hillhouse bajo MIT. Antes de distribuir conservar también encabezados/avisos aplicables de fuentes incluidas.
- Obligación MIT: incluir copyright y texto de permiso en copias o partes sustanciales; no atribuir esa biblioteca al autor de PortableSatStation. La licencia permisiva raíz comprobada no impone por sí misma publicar todo el firmware bajo GPL.
- Esto **no convierte todo el binario ESP32 en software original MIT**: framework, librerías y otros componentes conservan sus licencias y obligaciones. El `NOTICE`/documentación de control debe inventariarlos separadamente.
- Si se sustituye la biblioteca por una implementación GPL, reevaluar compatibilidad y cumplir GPL del firmware enlazado distribuido, sin etiquetar silenciosamente ese conjunto MIT. La elección del usuario solo cubre archivos originales.

## Evidencia local del usuario

Se leyeron **íntegros los seis textos extraídos** de los originales facilitados
localmente, incluidas las tablas y las leyendas de figuras. Los textos extraidos
no se distribuyen en este repositorio; la tabla conserva sus hashes para
identificar la evidencia sin depender de una ruta privada de trabajo.

| ID | Archivo de texto / documento | Páginas con contenido | SHA-256 del texto extraído |
|---|---|---:|---|
| P1 | `SatelliteStationPart1.txt` — Gordon Gibby KX4Z, Part I: Introduction | 4 | `A46CFC72ECFD08243613A93B90E2598879992DFD2EF3500FD76B4882A15C9A8E` |
| P2 | `PartIIRotatorcontrol.txt` — Part II: Inexpensive Manual/Computer-Controlled Rotator Controller | 7 | `156B3CEE7E1C81DF888FAF061CD30D488805EFB4B926963C3BACC7E87EF5C289` |
| P3 | `PartIIIDualAxisRotator.txt` — Part III: Inexpensive Antenna Rotator | 5 | `69AEE5DB54D4E4A44DDA4205037845909FAFB65865FD9A963587DE47E80852D7` |
| P4 | `PartIVCrossPolarizedYagis.txt` — Part IV: Cross-Polarized Yagi's, julio de 2025 | 13 | `066817AAF5DB4880E3181403E83813943BC78B72B1CCED625FA71E85CC100E9C` |
| PC | `RotatorControllerPCBInstructionManual.txt` — Computer Robotic Antenna Rotator Controller Construction Manual | 10 | `0DF0812407B627CAF765D3D807EE579564D3582EF6A088456167D7E3B99831DC` |
| PT | `SatelliteTargets.txt` — tabla SATELLITES | 2 | `3166F7BD85882550A639DDB8BE329A9D59649A1133C45FA34A1468FE54D03D63` |
| A | `TDS_AV2040.txt` — Ultralife, AV 2040 UHF Satellite Communication (SATCOM) Antenna | 1 | `0F2937B350CDA2DD364B91E16B611C22865F9538D568B47898CC1B56CD66BCD2` |

**Convención de páginas:** PC contiene folios impresos 1–10, citados como «p. imp.». Los otros textos no contienen folios impresos verificables: «p. PDF» significa el número ordinal de la página, reconstruido por los saltos de página `form feed` de la extracción, empezando en 1. No se presentan esos ordinales como números impresos inventados. El salto final vacío no es otra página con contenido. Las imágenes no se reconstruyen a partir del texto; solamente sus leyendas son evidencia textual. Para resolver una cota gráfica ambigua hay que consultar la imagen del original.

Las páginas web de la serie identificadas por el propio autor son:

- P1: <https://www.nf4rc.club/how-to-docs/satellite-system-part-i-overview/>
- P2: <https://www.nf4rc.club/how-to-docs/satellite-system-part-ii-rotator-control-board/>
- P3: <https://www.nf4rc.club/how-to-docs/satellite-system-part-iii-antenna-dual-axis-rotator-system/>

No se ha verificado una licencia permisiva de los seis PDF. Se hace síntesis crítica y referencia, **no se incorporan PDF completos, figuras, tablas extensas ni esquemas a los archivos del nuevo proyecto**. Que un artículo enlace Gerbers no convierte todo su contenido en hardware abierto.

### A — Nueva ficha TDS_AV2040: lectura visual local verificada

Original local añadido: `C:\Users\anatol.lopez\Downloads\TDS_AV2040.pdf` (83737 bytes); texto extraído localmente por el coordinador, consultado 2026-10-10. Es una ficha de una página, con título legible AV2040 y marca/URL Ultralife. No hay folio impreso legible.

**La extracción tiene codificación de fuente defectuosa:** palabras como «Right Hand Circular» aparecen desplazadas como «5LJKW +DQG &LUFXODU», y los valores numéricos desaparecen. Se resolvió la limitación leyendo **la imagen renderizada localmente a140dpi** por el coordinador: `pdf-text\TDS_AV2040-000001.png`. Las cifras siguientes provienen de lectura visual de p. PDF1, **no de adivinar la codificación**.

La ficha **Ultralife / Trivec-Avant**, fechada **23 NOV10**, documento **UBI-05273, REV:-**, declara: banda240–400MHz; VSWR1.5:1; circular derecha; AV2040-3 +7.0dBic240–400MHz, AV2040-2 +11.0dBic240–318MHz, AV2040-1 +9.0dBic240–400MHz;200WattsCW; relación axial3dB; masa6.5libras; BNCmacho; acabado negro; AV2040-3 NSN5985-01-149-2576. Son **especificaciones publicadas del producto comercial**, no prestaciones del diseño nuevo ni ensayos realizados aquí.

**145MHz y435MHz quedan ambos fuera de240–400MHz.** No hay cotas dimensionales de longitud, anchura ni volumen abierto/plegado en esta página. La descripción confirma «foldable, manpack» y la foto muestra bolsa/estructura, pero no aporta medidas ni autorización de copia. No se miden píxeles como cotas.

Intentos de recuperar ficha pública mediante antiguas rutas `/ECommerce/` de Ultralife devolvieron404; la portada actual del fabricante se obtiene pero no acredita especificaciones AV2040. El visor del PDF original devolvió403 por carpeta no confiable; la **imagen local sí se leyó posteriormente** con éxito. No se han enviado el PDF o sus assets a servicios externos. El pie del fabricante dice que los datos son solo referencia, no garantía de rendimiento, y están sujetos a cambio.

Los OBJ/STL externos que acompañan la referencia no tienen licencia confirmada en esta investigación: **no se redistribuyen ni se incorporan como hardware original**. La ficha comercial tampoco autoriza reproducción de su geometría. El coordinador gestiona metadatos geométricos y permisos por separado.

**Metadatos de geometría aportados por el coordinador, inspección local de solo lectura:** `tinker.obj`,10416vértices,20964caras,1objeto, SHA-256 **`e231ba603e352d31570a9db748208d7c32dd5116dec796b633858a7191910a00`**; STLbinario20964triángulos, SHA-256 **`f40f044336ad46a0434f8fc512e112d51cf68c6c80ddca6992bfc786a474b71a`**. Ambos tienen envolvente **194×115.798×33 en unidades no especificadas**. No se declara «mm» sin evidencia de unidades. La envolvente describe malla/disposición de piezas, **no dimensiones de antena ensamblada ni plegada**.

No se encontró declaración de copyright/licencia en encabezados OBJ/MTL inspeccionados por el coordinador; ausencia de aviso **no equivale a dominio público ni permiso de derivación**. El inspector local del coordinador devuelve metadatos, no redistribuye la malla. Este análisis no importa el mesh al CAD nuevo ni produce derivados.

## Repositorios públicos consultados

### D — Diplexor del usuario

<https://github.com/anatolbricoham/DuplexorSpaceQuad>

- Rama solicitada: `main`.
- Commit consultado: **`f5c7dc375ed7b9882f52bd7757deaf44cd422b81`**, 2026-09-30.
- Archivos leídos: `README.md`, `LICENSE`, `docs/MONTAJE.md`, `docs/PRUEBAS.md`, `BOM/BOM_SMA.csv`, `BOM/BOM_BNC.csv`.
- Enlace estable: <https://github.com/anatolbricoham/DuplexorSpaceQuad/tree/f5c7dc375ed7b9882f52bd7757deaf44cd422b81>.
- Licencia: MIT, copyright 2026 anatolbricoham. Permite adaptación y redistribución de material cubierto conservando aviso de copyright y licencia; revisar derechos de cualquier material externo. Aquí se documentan valores e interfaces, no se copia el circuito/CAD.
- **No existe `bom/` minúsculo en esta revisión:** las listas están en `BOM/`. Una consulta a `bom/` falló; se corrigió al directorio real.
- Los parámetros S del README son de **simulación ideal**, mientras que PRUEBAS define criterios pendientes. No se encontraron en los archivos leídos resultados de medición de una unidad física.

### L — LibreSat del usuario

<https://github.com/anatolbricoham/libresat-rotator-HAM>

- Rama solicitada: `master`.
- Commit: **`a23fe016108cf6d1209eb15140df74d0469e5e38`**, 2026-10-01.
- Archivos leídos: `README.md`, `LICENSE`, `docs/MECHANICAL.md`, `docs/SIZING.md`.
- Enlace estable: <https://github.com/anatolbricoham/libresat-rotator-HAM/tree/a23fe016108cf6d1209eb15140df74d0469e5e38>.
- Hardware: **CERN-OHL-S-2.0**, fuertemente recíproca. Firmware/software: **GPL-3.0-or-later**. Documentación/imágenes: **CC BY-SA 4.0**. Estas licencias externas permanecen intactas aunque el software original del proyecto nuevo sea MIT. Una derivación de su software no puede declararse simplemente MIT sin cumplir las obligaciones GPL. El directorio real y el ámbito de cada archivo deben comprobarse antes de reutilizarlo.
- El README reconoce que **v1.0 todavía no ha sido construida y medida como conjunto**. Sus tests y simulaciones no certifican fabricación, par, autonomía ni seguridad física.
- PortableSatStation adopta requisitos e ideas generales de referencia; la mecánica NEMA14 + planetaria 25:1 de diseño nuevo y el controlador autónomo se diseñan separadamente, sin trasladar sus piezas ni cifras como si fueran las del nuevo rotor.

### O0 — Guía OpenGD77 solicitada expresamente

<https://github.com/open-ham/OpenGD77/blob/b843c1f050ebcfdb7aea7fad9182af13bc5ef3e6/docs/OpenGD77_User_Guide.md>

- Commit del repositorio: **`b843c1f050ebcfdb7aea7fad9182af13bc5ef3e6`**, 2022-05-19.
- Se examinó el texto completo para localizar referencias satelitales. La sección de frecuencias VFO explica TX/RX diferentes y **cross-band/split**. No contiene la sección Satellite Screen ni identifica RT-3S en el título.
- Esta revisión histórica **no basta** para acreditar las funciones satelitales actuales de un RT-3S.

### O1 — Guía mantenida que completa O0

<https://github.com/LibreDMR/OpenGD77_UserGuide>

- Commit fijado: **`2289ba75afebd044b85d38f03b6e279defe3645d`**, 2026-03-10.
- Texto: <https://github.com/LibreDMR/OpenGD77_UserGuide/blob/2289ba75afebd044b85d38f03b6e279defe3645d/OpenGD77_User_Guide.md>.
- Secciones leídas: cabecera de modelos, Satellite Screen, Polar view, Satellite individual predictions, Satellite live data, Squelch and Power, Sat (Satellite follow mode); referencias de fecha/ubicación.
- El README del repositorio explica que la guía se separó del antiguo repositorio por cuestiones de licencia y que permanece cubierta por GPL 2. Solo la versión inglesa se mantiene.
- Esta guía sí nombra **MD-UV380 (RT-3S)** y describe Doppler integrado. La revisión de la guía no identifica automáticamente la versión de firmware instalada en el radio del usuario: registrar build, CPS y copia de seguridad antes de usarla.
- <https://www.opengd77.com> comunica el cierre del foro interactivo por tráfico de bots y remite al archivo estático <https://www.opengd77.com/archive/index.html>. No se presupone que las rutas antiguas sigan disponibles; `/downloads/MDUV380/Firmware/` devolvió 404.

### H — Placas de híbridos

<https://github.com/SatcomRadio/Hybrid_Couplers/blob/master/README.md>

Lectura del README público el 2026-10-10. Presenta placas para polarización circular, no un diplexor de 145/435 MHz. Reclama CMX03A03 200 W, «RF Power» 200 W, Anaren 10260-3 250 W y QCN3 15 W, **sin declarar banda de trabajo**. Las potencias son afirmaciones del README, no ensayos acreditados. No se verificó licencia aplicable a Gerbers; no se incorporan al proyecto.

**Error de enlace comprobado:** «QCN3 / SMA version» apunta a `GERBER-CmxSma.zip`, no a un Gerber QCN3. No pedir esa PCB suponiendo que sea el diseño QCN3.

### M — Fabricantes y disponibilidad

- Mini-Circuits **QCN-3+**: <https://www.minicircuits.com/WebStore/dashboard.html?model=QCN-3%2B> muestra explícitamente «LTCC 90° Hybrid, **220–470 MHz**, 50 Ω». Consultado 2026-10-10. Incluye 435 MHz, excluye 145 MHz. No confundir con la denominación sin «+» del README.
- Hoja enlazada: <https://www.minicircuits.com/pdfs/QCN-3+.pdf>. La respuesta fue PDF binario, no una extracción legible de la tabla de límites; **no se atribuyen potencia, fase ni aislamiento concretos a esa hoja**.
- No se obtuvo ficha fabricante legible para **CMX03A03** ni **Anaren 10260-3**. Intentos de consulta a Anaren fallaron por transporte/DNS/TLS y el índice TTM devolvió 403; una ruta tentativa de CMX no resolvió. DigiKey/Coilcraft devolvieron 403 en las rutas consultadas. No se inventan bandas ni límites de corriente/Q/SRF. La identificación exacta y las fichas originales son condiciones de compra.

## Referencias de antena visuales

- **B — Blog**, archivo abril de 2020: <https://blog.tomasbrincil.cz/?m=202004>. Se leyó la explicación y las tres fórmulas; declara diseño a **449.550 MHz** inspirado en AV-2040. No se verificó licencia explícita de STL/OBJ. El acceso a archivos enlazados no se interpreta como autorización para derivarlos.
- **T — Thingiverse 5904442**: <https://www.thingiverse.com/thing:5904442>. Solo accesible el título **«AV-2040 MilSat Antenna by German_Panda»**. No disponibles durante esta consulta detalles, cotas, archivos ni licencia; no se afirma haber validado su geometría o RF.
- **C — Captura de Cults aportada al proyecto**: condiciones indicadas **comercial / uso privado / NoAI**. La captura no es una licencia de derivación. No se trazan, reproducen ni adaptan piezas comerciales a partir de ella y no se someten esos archivos a análisis generativo. Sin ficha/licencia completa verificable no se incorporan assets.

## Qué evidencia falta para cerrar el diseño

1. Medidas de los motores NEMA14 **con referencia exacta**, ejes y taladros del proveedor; par/backlash, eficiencia y resistencia de la planetaria 25:1 nueva mediante fabricación y ensayo.
2. Medidas reales de caja, conectores y cableado del diplexor; las cotas publicadas de bridas/frontales son estimadas.
3. VNA de antenas y red ensamblada, polarización/relación axial y ensayo de potencia del ejemplar.
4. Identificación de las fichas de híbridos candidatos para ambas bandas. Potencia elevada sin banda no es una especificación suficiente.
5. Firmware/CPS exactos del RT-3S y prueba local de pantalla Satellite. No se ha ensayado el radio del usuario ni un protocolo CAT.
6. Efemérides y estado actuales del satélite: los listados históricos son ejemplos, nunca autorización de transmisión.
