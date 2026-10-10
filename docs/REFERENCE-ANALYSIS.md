# Análisis de referencias y decisiones del diseño nuevo

Fecha: 2026-10-10. IDs y revisiones en [SOURCES.md](SOURCES.md). Se han leído completos los seis textos extraídos localmente. «p. imp.» es el folio impreso verificable del manual; «p. PDF» es posición de página de artículos sin folio verificable, no una numeración editorial inventada.

## 1. P1 — Introducción a la estación de Gordon Gibby KX4Z

**Contenido real.** P1, p. PDF 1, enumera antenas direccionales VHF/UHF, separación por filtros, apuntado por modelo orbital, radio full-duplex, Doppler y sensibilidad. Su ejemplo es una estación de construcción económica, no una estación integrada de mochila. P1, p. PDF 2, propone el controlador Arduino K3NG y motores/actuadores con potenciómetros. P1, pp. PDF 3–4, distingue:

- Gpredict: predicción y visualización.
- rigctld/Hamlib: interfaz de radio; el autor encontró dificultades en el IC-820H para controlar MAIN/SUB y ambos Dopplers.
- rotctld: protocolo de posición deseada, **no** control directo del motor ni lectura física del ángulo.
- SatPC32: alternativa Windows que funcionó con el IC-820H del autor.

**Aplicación.** Conservar separación entre predicción, planificación, motor y radio. En PortableSatStation, el modo normal debe calcular SGP4 en el controlador, ofrecer AP local y guardar TLE/ubicación/UTC sin depender de un PC. Un protocolo externo opcional no sustituye SGP4 embarcado.

**No transferible.** El requisito de full-duplex describe la estación del autor. Un RT-3S con TX y RX distintos no pasa por ello a recibir mientras transmite. Ni el funcionamiento con IC-820H ni los comandos CAT de otros radios acreditan una interfaz RT-3S.

## 2. P2 — Placa de control económica

**Contenido real.** P2, p. PDF 1, amplía K3NG a Nano, botones y salidas de movimiento/dirección, con advertencia de límites de memoria. P2, pp. PDF 2–3, presenta esquema, placa de doble cara y prototipo; LCD/botones están en cara opuesta al Nano/conectores. P2, pp. PDF 4–5, lista LM7805, diodos 1 A, transistores, MOSFET P y conexiones. P2, pp. PDF 6–7, explica:

- MOSFET para alimentación/PWM; placas externas de dos relés SPDT para **inversión de polaridad de motores DC**.
- Una placa de relés por eje; lógica 0/5 V y alimentación de relés 12 V.
- Giro del G-450ADC en unos 90 s y una estimación de fuente de 2 A; el regulador lineal puede requerir disipador a tensión más alta.

**Aplicación.** Son reutilizables como principios la separación potencia/lógica, control manual, supresión de interferencias y prueba progresiva. No se traslada el esquema DC a un paso a paso: NEMA14 necesita driver de corriente de dos fases, señales STEP/DIR/ENABLE, límites eléctricos y aceleración.

**No transferible.** 2 A o 90 s del Yaesu no dimensionan la batería, corriente ni velocidad del NEMA14. Una relación 25:1 tampoco acredita par de salida; faltan par dinámico, eficiencia, backlash y límite de la reductora concreta. La placa documentada no proporciona AP, SGP4, GNSS ni norte verdadero por sí sola.

## 3. PC — Manual de construcción de la placa

**Contenido real y folios impresos.**

| Folio | Evidencia | Decisión nueva |
|---|---|---|
| pp. imp. 1–2 | Seguridad de soldadura, protección ocular, polaridad de diodos/electrolíticos y orientación de semiconductores | Conservar buenas prácticas; no tomar todas las explicaciones químicas del texto como especificación técnica |
| p. imp. 3 | Construcción inicial solo de azimut | Puesta en marcha por subsistemas/ejes antes de seguimiento |
| pp. imp. 4–5 | 2N3904 y resistencias generan dirección lógica; MOSFET conmuta la energía del motor | En nuevo sistema, dirección y driver STEP/DIR no equivalen a estas salidas |
| p. imp. 6 | Diodo de rueda libre, condensador de filtrado, capacitor anti-reset opcional | Diseñar protección específica de drivers/inductancias; no copiar indiscriminadamente el circuito Nano |
| p. imp. 7 | Protección de polaridad, regulador 5 V, filtros RF y botones manuales | Fuente DC/DC y protección adecuadas a electrónica moderna y batería real |
| p. imp. 8 | Potenciómetro alimentado a 5 V, resistencia limitadora y ADC del Nano | Un ADC de MCU de 3.3 V **no** acepta automáticamente esta interfaz de 5 V |
| p. imp. 9 | Comprobar 5 V antes de soldar Nano; LCD 16×2 y separación mecánica | Verificar tensiones antes de conectar electrónica; dejar espacio para cables/servicio |
| p. imp. 10 | Revisar cortos, encender USB, programar | Ensayo sin motores, después drivers y cada eje sin carga |

**Advertencia de coherencia.** Las designaciones/valores de algunas resistencias en el manual y la tabla de P2 no coinciden limpiamente (por ejemplo R2/R3). No generar un nuevo PCB ni una BOM de montaje por mezcla automática de ambos textos; prevalecería un esquema/versionado comprobado. Este proyecto no construye esa placa.

## 4. P3 — Rotor de dos ejes

**Contenido real.** P3, p. PDF 1, expone opciones manuales, elevación fija y comerciales; no pretende instalación permanente estanca. P3, p. PDF 2, usa **Yaesu G450ADC** para azimut sobre madera y un actuador lineal 12 V de **2 pulgadas** de carrera para elevación. El intento de motor muy reducido y caja de 90° falló porque se dañaron engranajes. El pin a aproximadamente 1 pulgada del eje es una primera aproximación geométrica, no una solución cinemática general.

P3, p. PDF 3, usa finales internos del actuador y potenciómetro para elevación. P3, p. PDF 4, describe ejes de **10 mm**, adaptación PVC/goma/abrazadera, elevaciones aproximadamente 15–75° y sin uso de elevación >90°. El rotor inferior gira **toda** la parte superior. P3, p. PDF 5, solo aporta leyenda de conjunto con antenas.

**Aplicación.** Equilibrar antena/cables, soportar esfuerzos con rodamientos, verificar conexión eje/boom y tratar azimut como carga de todo el cabezal. El nuevo rotor ASA original con NEMA14 y planetaria 25:1 no se deriva de esas piezas de madera ni de la cinemática de pistón.

**No transferible.** La robustez del G450ADC no demuestra que una reductora NEMA14 admita cargas radiales o axiales. El eje de salida debe ir descargado mediante soporte estructural/rodamientos. No dar por autoblocante la planetaria: comprobar retención y comportamiento sin corriente. Fin de carrera de un actuador no sustituye referencias y topes de un paso a paso. Para pasos cenitales se exige planner que respete límites/velocidades, no un salto AZ arbitrario ni un «flip» mecánico no comprobado.

## 5. P4 — Yagis cruzadas, julio de 2025

**Contenido real.** P4, pp. PDF 1–2, trata desvanecimiento por polarización y propone dos planos. P4, pp. PDF 2–3, describe dos formas de generar 90°: línea de fase o desplazamiento físico longitudinal de λ/4, con planos ortogonales y orientación de alimentación. Da **20.36 pulgadas** en 2 m y **6.78 pulgadas** en 70 cm, equivalentes a 517.144 y 172.212 mm. Son desplazamientos entre planos del diseño de referencia, no dimensiones de una única antena dualband.

P4, p. PDF 4, usa boom no conductor y diseños Cheap Yagi, inicial de 4 elementos VHF + 6 UHF, segundo plano de 3 VHF + 5 UHF. Los diámetros de elementos modifican las longitudes. P4, pp. PDF 5–7, detalla uniones de flechas/aluminio, insertos y cobre con resultados variables; no son procesos industriales repetibles. P4, pp. PDF 8–10, ajusta con VNA y compara frente/espalda, y usa boom PVC desmontable/indexado.

P4, p. PDF 9, conecta alimentadores RG58 de λ/2 eléctrica corregida por factor de velocidad mediante una T BNC; el autor declara ROE general **2:1–3:1**, no una adaptación ideal. P4, p. PDF 11, una leyenda informa ROE 1.2:1 a **444.8 MHz**; esto no acredita la ROE a 435 MHz ni banda útil completa. P4, p. PDF 12, declara aislamiento entre antenas aproximadamente **40 dB o mejor** en su montaje y recepción con un preamplificador, un lado de diplexor como filtro, IC-820H ~30 W y 50 pies de LMR400. P4, p. PDF 13, incluye materiales y enlaces de la serie.

**Correcciones y límites esenciales.**

- Una T con dos antenas no crea por sí misma cuadratura ni adaptación. Requiere impedancias y fases conocidas; el caso observado no se convierte en regla para otros dipolos.
- **No** aceptar como criterio universal la observación del artículo de que cambiar RHCP/LHCP solo cuesta 3 dB: circular ideal de mano opuesta tiene rechazo mucho mayor. Los 3 dB corresponden a circular ideal frente a lineal ideal. El resultado real depende de relación axial, orientación y trayecto.
- La tabla UHF entre pp. PDF 4–5 contiene un valor contradictorio: Director 1 inicial 12.3 pulgadas y texto de «acortamiento» a 13.1. Se registra la inconsistencia; **no se usa como plano de corte**. Revisar original/fuente y medir.
- El diagrama polar a 30 pies y el aislamiento de su estructura no acreditan ganancia absoluta, relación axial o aislamiento de la antena portátil nueva. No se suman automáticamente a los dB del diplexor ideal.
- Dos planos VHF de ~λ/4 separados afectan longitud, centro de gravedad, momento y área al viento. No se heredan masa ni presupuesto de par de otra antena.

**Aplicación.** Elegir primero arquitectura RF verificable: una antena direccional por banda, inicialmente lineal si facilita validación, o planos ortogonales con red de fase **específica por banda**. Ajustar en el montaje final ASA/cables/soportes. Circular es una ampliación pendiente de medición, no una etiqueta estética.

## 6. PT — Lista SatelliteTargets

**Contenido real.** PT, p. PDF 1, mezcla repetidores FM (ISS, SO-50, HADES-R) y transpondedores lineales de VHF descendente; indica frecuencias, centros y tonos de armado/CTCSS. PT, p. PDF 2, incluye RS-44 y MESAT1 lineales UHF descendente, ISS packet 145.825 y SONATE-2. No tiene fecha de vigencia ni TLE.

**Aplicación.** Sirve para mostrar que «145/435» son bandas y no un par único de canales, y que hacen falta modo, TX/RX, tono y efemérides por satélite. La tabla **no se importa como lista operativa autorizada**. Verificar AMSAT/operador antes de transmitir y seleccionar FM compatible con el radio.

**No transferible.** RT-3S FM/DMR no se convierte en SSB/CW por cargar RS-44, AO-7 u otro transpondedor lineal. Packet requiere ruta de datos/modem apropiada; el seguimiento mecánico no aporta por sí mismo AX.25. La exención FCC mencionada para AO-7 corresponde a otra jurisdicción; no es permiso local automático. ISS puede cambiar entre modos: no garantizar que dos entradas históricas funcionen simultáneamente.

## 7. L — LibreSat como referencia de sistema, no como prototipo medido

La revisión pública usa Pi Zero 2 W + RP2040 y NEMA17 con **cicloidal impresa 25:1**, no NEMA14 con planetaria original nueva. README: actuador Ø94 mm, aproximadamente 45 mm más motor, dos rodamientos 61810 y encoder AS5600 en eje trasero del motor. MECHANICAL: eje frontal motor 5 mm, rodamientos 6803 **17×26×5 mm**, 61810 **50×65×7 mm**, stub Ø20×250 mm insertado 42 mm y antena separada aproximadamente 200 mm de la cara del actuador.

También declara ASA para piezas al sol, adaptadores de trípode, loop de cable 60 cm centrado en AZ225° para rango0–450°, y extensión de mástil300–500 mm para ciertos booms >1.1 m. Son **cotas de LibreSat**, no piezas compatibles garantizadas para PortableSatStation.

SIZING parte de antena1 kg, área0.1 m², brazo de presión0.15 m, desequilibrio20 mm, viento10 m/s y eficiencia75%. Calcula EL1.30 Nm y AZ1.10 Nm, 4.1 W medios y resultados de simulación de pasos con flip. No se reutilizan esos factores de seguridad, autonomía ni errores de apuntado como resultados del diseño nuevo. El propio README reconoce conjunto aún no construido/medido.

**Lecciones:** conservar AP local, TLE offline, reloj/ubicación, planner de cable-wrap, montaje equilibrado y recalibración. Un encoder sobre motor detecta pasos perdidos pero **no mide backlash o deslizamiento posterior a la reductora**. Guardar pasos no recupera orientación después de movimiento sin energía. GNSS de una antena da posición/UTC, no rumbo absoluto de una estación parada. Nivel/gravedad dan inclinación, no azimut. Norte verdadero requiere un método explícito con calibración, declinación si usa magnetómetro y detección de interferencia.

## 8. B/T/C — Referencias de forma

El blog B declara **449.550 MHz** y calcula longitud activa `0.92·c/(2f)`, reflector1.05 veces esa longitud y separación0.225λ. Evaluadas solo como primera estimación:

| Frecuencia | Activo total | Reflector total | Separación |
|---|---:|---:|---:|
| 145 MHz | 951.066 mm | 998.619 mm | 465.195 mm |
| 435 MHz | 317.022 mm | 332.873 mm | 155.065 mm |

Son longitudes completas, no de cada brazo, y no un diseño dualband validado. La diferencia de escala obliga a una arquitectura propia; soporte dieléctrico, diámetro de tubos, proximidad entre bandas y red de alimentación desplazan impedancia/patrón. «SATCOM» o parecido al AV-2040 no garantiza cobertura145/435.

T solo aporta título verificable; no cotas ni licencia. C tiene condiciones comercial/uso privado/NoAI; no se copia su modelo ni se genera una derivación trazada. Inspiración funcional general (plegado, trípode, portabilidad) no autoriza reproducción de geometría ajena.

## 9. Decisiones y bloqueos de integración

1. **Diseño nuevo original**, ASA para estructura; NEMA14 planetaria25:1 solo tras fijar modelo/datos reales. Comprobar fluencia, temperatura, rodamientos, carga y tornillería por ensayo. `calc/design.json` usa motor de 200 pasos, 16 micropasos y reducción 25:1: **80000 micropasos/vuelta de salida** es resolución nominal de mando, no exactitud medida. El par motor de 0.1 Nm y eficiencia 0.7 por etapa son supuestos; el ejemplo de viento de 8 m/s **no supera** el margen de seguridad exigido y no autoriza operación a esa velocidad ni establece un límite de viento seguro.
2. **AP y seguimiento SGP4 a bordo** independiente del RT-3S. Sin UTC/posición/TLE válido o norte/nivel calibrados no declarar seguimiento válido.
3. **Radio asistido manualmente**, con Doppler propio de OpenGD77 si build comprobado; sin CAT inventado, control de PTT ni supuesto full-duplex.
4. **Diplexor opcional y pendiente de medición**, geometría publicada en [RF-AND-RADIO.md](RF-AND-RADIO.md). Reservar holgura de plugs, radio y flexión de coaxial; no usar el conector como soporte estructural.
5. **Polarización separada por banda.** Híbridos no pedidos hasta conocer banda, fase, potencia y puerto aislado; QCN-3+ excluido para145MHz.
6. **Bloqueo físico:** bridas/altura de conectores del diplexor son estimaciones explícitas de su autor. CAD de interfaz final debe quedar paramétrico hasta medir el ejemplar con calibre.
7. **Bloqueo de aprobación:** no hay ensayo físico completo del nuevo rotor, antena o red RF. Simulaciones, fuentes y CAD no justifican la etiqueta «listo para transmitir».
8. **Licencias elegidas por el usuario:** software original MIT y hardware original CERN-OHL-S-2.0. Las referencias externas mantienen sus propias licencias; no se redistribuyen fuentes desconocidas ni se cambia la GPL del software LibreSat. La síntesis de ingeniería no incorpora sus archivos. No hay publicación remota en esta fase.

### Condiciones del seguimiento autónomo, no APIs de apariencia

- La propagación **SGP4 se ejecuta realmente en ESP32** a partir de TLE, UTC y ubicación; un móvil sirve de interfaz, no de motor oculto de predicción. Una API no se declara implementada si no existe ruta completa desde validación de entrada hasta cálculo, planificación y control seguro.
- Un reloj/UTC ausente, inválido o vencido bloquea el movimiento automático. Posición GNSS guardada tras apagado es **caché con metadatos**, no una nueva posición válida ni un fix vigente al arrancar. Hay que confirmar o adquirir ubicación/UTC y validar antigüedad de TLE.
- AZ geográfico/verdadero y AZ mecánico no son intercambiables: transformar mediante offset de norte y escoger una solución equivalente ±360° **dentro de los límites mecánicos y de cable**, sin normalizar un ángulo prohibido hasta convertirlo en permitido. Verificar cruces 359°→0°, offset no cero y bordes del recorrido.
- En cenit, el azimut geográfico queda singular; no generar movimiento ilimitado para seguirlo. Rechazar pasos que alcancen/superen el límite cenital si no hay trayectoria continua, velocidad y margen mecánico demostrados. No afirmar seguimiento sobre el cenit mediante un flip que la geometría/planner no admite.
- Importación manual de TLE es obligatoria para uso offline. Descarga automática, si se ofrece, requiere HTTPS con **verificación de certificado** y validación de respuesta/TLE; si no puede implementarse de extremo a extremo se omite. Nunca suplir validación TLS con `setInsecure`.
- Las pruebas deben cubrir explícitamente arranque sin UTC, UTC inválida, caché GNSS tras reinicio, offset AZ y cable-wrap, objetivo cenital, pérdida de validez durante seguimiento y fallo de importación. La existencia de endpoints/AP no sustituye estas pruebas ni la compilación real del firmware.
- **Latencia es seguridad:** con motores habilitados se rechazan descargas HTTPS o predicciones bloqueantes largas; alternativa admisible es cómputo incremental con servicio continuo y latencia de parada demostrada. Un timeout HTTP de 10 s dentro del mismo bucle puede dejar sin servicio parada, homing y límites. La parada física requiere supervisión independiente y/o corte hardware apropiado, no depende de que termine un handler web.
- La predicción se limita al satélite seleccionado y a un horizonte acotado. Consultar estado no recalcula repetidamente un catálogo completo ni desencadena descargas. Limitar tamaño de catálogo/TLE y trabajo por petición antes de mover motores.
- Un destino que supera velocidad alcanzable, límites de recorrido o restricciones cenitales produce **fallo explícito de la API** y no movimiento; recortar el ángulo silenciosamente y responder «éxito» no equivale a alcanzar la orden. La lógica de parada no espera a un handler largo durante seguimiento.
- Los nombres TLE y otros textos importados son entrada no confiable: mostrarlos con `textContent` o escape equivalente, nunca insertarlos como `innerHTML`. Una importación válida orbitalmente tampoco autoriza inyección de marcado en el AP.

## 10. A — Ficha AV2040 añadida: comparación visual verificada

Se leyó íntegra la extracción local nueva `TDS_AV2040.txt` de **una página** y, al detectar pérdida de cifras por mapa de fuentes, se leyó la página rasterizada localmente a140dpi, `TDS_AV2040-000001.png`. Fuente **Ultralife/Trivec-Avant, 23NOV2010, UBI-05273 REV:-**, p. PDF1. No se reconstruyeron números mediante conjeturas de codificación.

**Datos publicados del AV2040 comercial:**240–400MHz, VSWR1.5:1, circular derecha, relación axial3dB,200WCW,6.5libras (≈2.948kg), BNCmacho. Ganancias por variante: AV2040-3 +7.0dBic240–400MHz; AV2040-2 +11.0dBic240–318MHz; AV2040-1 +9.0dBic240–400MHz. Son prestaciones de la ficha fabricante, **no prestaciones del nuevo145/435MHz ni verificaciones físicas de nuestra estación**.

**Ambas frecuencias objetivo,145y435MHz, están fuera de la banda240–400MHz.** También449.550MHz del blog está fuera: el blog describe su propia realización reajustada, no evidencia de extensión de banda del producto original. La ficha muestra y describe plegado/manpack, pero **no publica cotas abierta/plegada ni volumen de bolsa**, ni define qué incluye la masa. No se obtienen dimensiones o CG de la foto.

Aplicación al diseño: portabilidad/plegado son requisitos funcionales razonables, pero antena, polarización y soporte145/435 necesitan diseño y medida propios. No heredar200W,3dB de relación axial,7/9/11dBic,2.948kg ni margen de rotor del producto comercial. La advertencia del fabricante declara información de referencia, no garantía de rendimiento y sujeta a cambio. OBJ/STL externos con licencia sin confirmar **no se redistribuyen**; el nuevo diseño conserva geometría original y el coordinador gestiona metadatos/consentimiento. El bloqueo dimensional continúa porque la ficha no contiene las cotas, no porque la imagen sea ilegible.

La inspección local de metadatos realizada por el coordinador cuenta10416vértices/20964caras/1objeto en `tinker.obj` y20964triángulos en el STLbinario. Coinciden en envolvente194×115.798×33 **unidades no especificadas**; trazabilidad SHA-256 en SOURCES. No se interpreta esa caja de malla/disposición de piezas como dimensiones de antena ensamblada, tamaño de plegado o escala en mm. No hay licencia declarada en encabezados OBJ/MTL inspeccionados y no se importa la geometría a ningún derivado.
