# Antena V/U plegable: yagis cruzadas de polarización circular

> Generado por `scripts/gen_docs.py` a partir de `calc/antenna_result.json` (NEC2). Los números NO se editan a mano.

## Qué es y por qué
Dos secciones de yagi **cruzada** (elementos horizontales + verticales en la misma estación del boom) sobre un único boom de PVC de 16 mm, desmontable en dos tramos:

* **VHF 145,9 MHz**: 3 elementos por plano, 6 varillas (reflector, activo, director).
* **UHF 436,5 MHz**: 4 elementos por plano, 8 varillas.

Las dimensiones de partida son las del artículo *Cross-Polarized Yagis* (KX4Z, Parte IV, tablas de 144,1 y 432,1 MHz, basadas en WA5VJB) escaladas a las frecuencias de diseño. Después, **el elemento activo se sintonizó por bisección en NEC2 hasta reactancia 0** y se comprobó el acoplamiento mutuo con **todas las varillas de ambas bandas presentes**.

La polarización circular se obtiene con un **híbrido de 90°** por banda (ADR-004), no con 1/4 λ de boom extra como en el artículo: así las dos polarizaciones comparten estación y el boom mide **83 cm** en lugar de más de 1 m solo en VHF.

## Dimensiones (mm, varilla de aluminio de 3 mm, posición desde el reflector VHF)
### VHF (centro 145,9 MHz)
| Elemento | Posición en boom | Longitud total |
|---|---|---|
| Reflector | 0 | 1049 |
| Activo (2 semielementos) | 213 | 991 |
| Director | 483 | 936 |

### UHF (centro 436,5 MHz, a continuación del tramo VHF)
| Elemento | Posición en boom | Longitud total |
|---|---|---|
| Reflector | 543 | 334 |
| Activo (2 semielementos) | 606 | 323 |
| Director 1 | 681 | 309 |
| Director 2 | 826 | 297 |

Cada estación lleva **dos varillas cruzadas** (plano Y y plano Z, desplazadas 10 mm en el boom para no tocarse; ese desplazamiento está incluido en el modelo NEC).

## Resultados de la simulación (NEC2, espacio libre, boom no conductor no modelado)
| Banda | Ganancia (dBi, total) | Relación axial (dB) | F/B (dB) | Ancho de haz 3 dB (°) | R en cada puerto (Ω, ambos excitados) |
|---|---|---|---|---|---|
| VHF | 7.6 | 0.27 | 21.7 | 82 | 21.0 |
| UHF | 9.1 | 0.80 | 17.0 | 70 | 25.8 |

Barrido en banda con ambas secciones en el boom:

| MHz | Ganancia dBi | AR dB | F/B dB |
|---|---|---|---|
| 144.0 | 7.44 | 0.26 | 27.3 |
| 145.9 | 7.61 | 0.27 | 21.7 |
| 146.0 | 7.62 | 0.27 | 21.2 |
| 435.0 | 9.06 | 0.79 | 16.6 |
| 436.5 | 9.08 | 0.80 | 17.0 |
| 438.0 | 9.10 | 0.80 | 17.2 |

### Lo que NO demuestra esta simulación
* No incluye boom, bridas impresas, coaxiales ni el suelo/trípode/cuerpo humano. **El primer ajuste real se hace con NanoVNA** acortando/alargando el elemento activo (ver `docs/TESTING.md`).
* La ganancia es la total en el eje; la ganancia RHCP/LHCP se deduce de la AR (<1 dB en ambas bandas), no se calculó por separado.
* La ganancia es de **espacio libre**; en la práctica se mide con un receptor y una señal conocida.
* El barrido muestra ganancia y AR estables en 144–146 y 435–438 MHz con 3 mm de varilla, pero eso presupone cortar las longitudes a ±1 mm.

## Red de alimentación
| Banda | MHz | ROE en cada salida del híbrido | Potencia a la carga aislada (%) |
|---|---|---|---|
| VHF | 145.9 | 1.34 | 2.1 |
| UHF | 436.5 | 1.09 | 0.2 |

Por banda: híbrido 90° de 4 puertos → dos transformadores λ/4 de 37,5 Ω (**dos trozos de coaxial de 75 Ω en paralelo**) → una yagi cada uno. Longitudes (VF 0,66 supuesto, **medir en el cable real**): VHF 33.9 cm, UHF 11.3 cm.

Con un híbrido ideal y cargas idénticas, el puerto de entrada queda adaptado y la energía reflejada se disipa en la carga del puerto aislado: la pérdida es la de la tabla (≈2 % en VHF, ≈0,2 % en UHF). El **híbrido debe cubrir cada banda**: los PCB de `SatcomRadio/Hybrid_Couplers` (QCN3 15 W, CMX03A03 200 W, RF Power 200 W, Anaren 10260-3 250 W) **no tienen la banda de trabajo documentada en su README**; hay que comprobarla en la hoja de datos del componente antes de comprar (ver ADR-004).

## Plegado
Cada semielemento va en un brazo articulado (`hinge_arm`) con pivote M3 en la brida `cross_hub_16` y se pliega paralelo al boom. Boom en dos tramos de ~45 cm (0,90 m en total; se usan 0,83 m). Plegada, las varillas (semielementos de hasta ~52 cm) quedan paralelas al boom: bulto estimado ≈ 55 cm de largo. El diseño de las bridas/bisagras es una **primera iteración sin imprimir** (ver `docs/TESTING.md`).

## Qué se descartó
* Intercalar VHF y UHF en la misma zona del boom: un elemento de 2 m es resonante en 3/2 λ a 435 MHz y puede distorsionar la yagi UHF. **No se simuló la variante intercalada**; se optó por secciones separadas por prudencia, y el modelo combinado muestra que la influencia de los elementos VHF sobre la UHF es pequeña (ganancia UHF 9,26 → 9,08 dBi, F/B 13,3 → 17,0 dB).
* Copiar la geometría de la ficha comercial AV2040-2: licencia *Cults PU / No IA* (no se usó ningún archivo) y, además, es UHF solo. Se tomó solo el concepto (elementos cruzados y plegables).
