# BricoHams: expediente real de laboratorio

Revision 2026-10-17. **Procedimientos y hojas en blanco, no resultados.**
Autores: Anatol EA5KAO, Diego EA5JEF y Pedro Roca Molina · bricohams.org.
Usar con [G0-G4](../ACCEPTANCE.md). Mantener HOLD de PCB, motores y TX
hasta la autorizacion especifica; disponer de un banco no levanta HOLD.

## 1. Preparar un expediente por ejemplar y configuracion

Las [plantillas](laboratorio/README.md) incluyen cuaderno imprimible HTML,
una ficha por ensayo, CSV de resultados, lecturas, equipos, calibraciones
y cobertura de **cada fila de las BOM**. No rellenar los originales
generados. Copiar el directorio a una carpeta nueva y trabajar en esa copia:

```powershell
$destino = Join-Path $env:USERPROFILE 'Documents\BricoHams-Laboratorio\LOTE-001'
if (Test-Path -LiteralPath $destino) { throw 'El expediente ya existe: elegir otro ID.' }
New-Item -ItemType Directory -Path $destino | Out-Null
Copy-Item -Path '.\docs\testing\laboratorio\*' -Destination $destino
```

Crear subcarpeta `evidencias` en la copia. Abrir `cuaderno.html` en navegador
e imprimir o guardar PDF A4: una hoja por ensayo. Los campos HTML son
casillas manuscritas, no un formulario que guarde datos al escribir.
CSV UTF-8 se puede abrir en LibreOffice/Excel importando **coma** como
separador y punto decimal para numeros; no convertir IDs/series en fechas.
No subir series, ubicaciones ni datos personales de laboratorio a servicios
externos. El registro historico [registro-pruebas.csv](registro-pruebas.csv)
se conserva: el nuevo expediente permite repeticiones, unidades y evidencias.

### Encabezado obligatorio en cada ensayo

Lote, ID de ejecucion unico, fecha/hora UTC, operador y revisor, variante
(ESP32/CM5/Lite), revision Git **y cambios sin commit**, DUT/serie/lote,
BOM/IDs y unidades fisicas, firmware, esquema de conexiones/revision,
instrumentos/series/firmware, calibracion e ID de verificacion, ambiente,
canales, potencia y ciclo de trabajo cuando proceda.

Las filas BOM de LEGACY, alternativas y herramientas no son compras
obligatorias. En `componentes.csv`, seleccionar o excluir cada fila con
motivo firmado. Expandir filas para cada unidad/serial/posicion, por
ejemplo cada uno de los 16 empalmes y cada eje; una fila de inventario no
aprueba automaticamente todas sus unidades. Todo componente seleccionado
requiere LAB-01 y asignacion revisada de ensayos funcionales/especificos.
La columna de asignacion empieza vacia deliberadamente: no se infiere
una cualificacion electrica a partir del nombre de una pieza.

## 2. Disposicion fisica y conexion

| Banco | Montaje real minimo | Separacion y parada | Procedimientos |
| --- | --- | --- | --- |
| B0 digital | PC, consola y DUT sin potencia de motores/PA | Guardar hashes, logs y revisiones; no reutilizar credenciales | SW, APP, PCB documental |
| B1 DC/control | Fuente limitada, DMM, osciloscopio, carga electronica, logica 3,3 V y circuito autorizado | Fusible y corte DC dimensionados; no puentear guard ni energizar auxiliar HOLD | PWR/DRV/SNS, LAB-06 a 11 |
| B2 mecanica | Base rigida anclada, retencion secundaria, carga gradual, calibre, comparador, goniómetro | Zona de giro despejada, EL retenido, sin manos junto a correas | MEC, LAB-12/13 |
| B3a RF pequena senal | NanoVNA, SOL/THRU y patrones de verificacion, coaxiales etiquetados, terminaciones 50 ohm | **PA/radio TX desconectados fisicamente**, comprobar ausencia DC; motores quietos | [NanoVNA](10-nanovna.md), LAB-02 a 05, 14/15 |
| B3b RX activo | Generador de nivel conocido, atenuacion, filtro/LNA, receptor, carga y medida de potencia | Fuente limitada y limite de entrada verificado; no conectar PA | LAB-16, [RF activa](11-rf-potencia.md) |
| B3c TX en carga | PA autorizado, filtro, acoplador/vatimetro, carga 50 ohm, atenuacion dimensionada, analizador | NanoVNA desconectado; operador dedicado, PA inhibit, disipacion y RF contenida | LAB-17 a 21, [25 W](11-rf-potencia.md) |
| B4 conjunto | Tripode/estacion aceptados, referencia UTC/norte, bateria y zona autorizada | Sin viento hasta cualificar; licencia, exposicion RF y estado del satelite revisados | SYS, LAB-22 a 24 |

Un SDR sin calibracion de nivel es monitor relativo, no patron de potencia,
NF o emisiones. Un NanoVNA no sustituye un analizador de espectro ni
vatimetro de TX. No conectar un PA al VNA ni usar solo un atenuador como
excusa para medir TX con el VNA.

## 3. Regla de decision y trazabilidad metrologica

- Antes del ensayo, copiar la especificacion aplicable, fuente/revision,
  limite inferior/superior, unidad y tolerancia. Distinguir objetivo de
  proyecto de limite obligatorio del componente/normativa.
- Cuando falte un rating, intervalo de calibracion o limite, marcar
  **BLOQUEADO**, no APROBADO ni «parece correcto». La autoridad tecnica
  debe fijarlo antes de aplicar energia/carga o emitir conformidad.
- Registrar lectura bruta, correcciones, resultado, incertidumbre
  expandida U, factor k y metodo. No dar a un NanoVNA de aficionado una
  trazabilidad o incertidumbre de laboratorio que no tiene.
- Regla conservadora propuesta: intervalo `[resultado-U, resultado+U]`
  dentro de limites -> APROBADO; completamente fuera -> RECHAZADO;
  solapa el limite o U no evaluada -> INDETERMINADO. Criterios logicos
  requieren evidencia de cada condicion; no inventar U para un booleano.
- PENDIENTE: no ejecutado. BLOQUEADO: falta prerrequisito/rating.
  NO_APLICA: motivo y firma para variante no montada. INDETERMINADO
  nunca cuenta como aprobado. Los fallos de seguridad detienen integracion.
- Repeticion: nueva fila/ID, conservando fallo y accion correctiva; nunca
  borrar lecturas desfavorables ni sustituir «as found» por «as left».
- Archivo: fotografia del montaje y seriales; CSV/S1P/S2P, capturas y
  logs originales con ID de ejecucion. Guardar SHA-256 y ruta relativa.
  Un CSV o fichero Touchstone renombrado no prueba una calibracion.

## 4. Secuencia de liberacion

1. LAB-01 recepcion de todas las unidades seleccionadas y revision de
   fichas; calibraciones LAB-02/06/12/14 antes de utilizar instrumentos.
2. PCB documental y circuito autorizado B1, despues PWR/DRV/SNS. No
   montar una placa bloqueada por el simple hecho de cerrar una casilla.
3. MEC y geometria de antena; B3a pasivo; despues RX y control.
4. Cualificacion de interlock **sin RF**, luego RX protegido y PA en carga.
5. Potencia progresiva solo con ratings confirmados; medicion de
   proteccion cruzada y emisiones antes de conectar una antena.
6. B4 autorizado, masa/autonomia/apuntamiento y revision final LAB-24.

No se exige exponer a nadie a una estructura bajo carga ni ensayar
destruccion/volcado de tripode en este procedimiento. Una prueba de
viento o sobrecarga necesita plan de seguridad especifico y recinto.

## 5. Protocolos y formularios

- [NanoVNA, SOLT y RF pasiva](10-nanovna.md).
- [Previos, conmutacion, 25 W y emisiones](11-rf-potencia.md).
- [Calibraciones DC, sensores, mecanica y sistema](12-calibraciones.md).
- [Ensayos suplementarios LAB-01 a LAB-24](13-ensayos-laboratorio.md).
- [Cuaderno imprimible](laboratorio/cuaderno.html), [resultados](laboratorio/resultados.csv),
  [lecturas](laboratorio/lecturas.csv), [instrumentos](laboratorio/instrumentos.csv),
  [calibraciones](laboratorio/calibraciones.csv),
  [componentes](laboratorio/componentes.csv) y [evidencias](laboratorio/evidencias.csv).

Las fichas heredadas conservan criterios propuestos. Las aclaraciones de
estos protocolos prevalecen ante afirmaciones antiguas insuficientes:
un escaneo I2C no identifica duplicados, giro libre no prueba EN, y
«sin calentamiento al tacto» no es medicion de temperatura.
