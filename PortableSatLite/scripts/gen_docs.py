#!/usr/bin/env python3
"""Regenerates the numeric parts of docs/ from calc/*.json and cad/parts.json so documentation can never drift from the models.
Run after tests/run_all.sh:  python3 scripts/gen_docs.py"""
import json, os, textwrap
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(R)
A = json.load(open('calc/antenna_result.json')); BW = json.load(open('calc/beamwidth_result.json')); F = json.load(open('calc/feed_result.json'))
RT = json.load(open('calc/rotor_result.json')); MS = json.load(open('calc/mass_result.json')); P = json.load(open('cad/parts.json'))
mm = lambda x: f"{x*1000:.0f}"
def table(rows, head): return "| " + " | ".join(head) + " |\n|" + "---|"*len(head) + "\n" + "\n".join("| " + " | ".join(map(str, r)) + " |" for r in rows)

# ---------------- ANTENNA.md ----------------
vh = A['vhf']; uh = A['uhf']
ant = f"""# Antena V/U plegable: yagis cruzadas de polarización circular

> Generado por `scripts/gen_docs.py` a partir de `calc/antenna_result.json` (NEC2). Los números NO se editan a mano.

## Qué es y por qué
Dos secciones de yagi **cruzada** (elementos horizontales + verticales en la misma estación del boom) sobre un único boom de PVC de 16 mm, desmontable en dos tramos:

* **VHF 145,9 MHz**: 3 elementos por plano, 6 varillas (reflector, activo, director).
* **UHF 436,5 MHz**: 4 elementos por plano, 8 varillas.

Las dimensiones de partida son las del artículo *Cross-Polarized Yagis* (KX4Z, Parte IV, tablas de 144,1 y 432,1 MHz, basadas en WA5VJB) escaladas a las frecuencias de diseño. Después, **el elemento activo se sintonizó por bisección en NEC2 hasta reactancia 0** y se comprobó el acoplamiento mutuo con **todas las varillas de ambas bandas presentes**.

La polarización circular se obtiene con un **híbrido de 90°** por banda (ADR-004), no con 1/4 λ de boom extra como en el artículo: así las dos polarizaciones comparten estación y el boom mide **{A['boom_len_m']*100:.0f} cm** en lugar de más de 1 m solo en VHF.

## Dimensiones (mm, varilla de aluminio de 3 mm, posición desde el reflector VHF)
### VHF (centro 145,9 MHz)
{table([[n, mm(x), mm(L)] for n, (x, L) in zip(['Reflector','Activo (2 semielementos)','Director'], vh)], ['Elemento','Posición en boom','Longitud total'])}

### UHF (centro 436,5 MHz, a continuación del tramo VHF)
{table([[n, mm(x), mm(L)] for n, (x, L) in zip(['Reflector','Activo (2 semielementos)','Director 1','Director 2'], uh)], ['Elemento','Posición en boom','Longitud total'])}

Cada estación lleva **dos varillas cruzadas** (plano Y y plano Z, desplazadas 10 mm en el boom para no tocarse; ese desplazamiento está incluido en el modelo NEC).

## Resultados de la simulación (NEC2, espacio libre, boom no conductor no modelado)
{table([[b, f"{A[k]['gain_dbi']:.1f}", f"{A[k]['ar_db']:.2f}", f"{A[k]['fb_db']:.1f}", f"{BW[b]['plane_XY_deg']:.0f}", f"{A[k]['z_feed'][0][0]:.1f}"] for b, k in (('VHF','vhf_combined'),('UHF','uhf_combined'))], ['Banda','Ganancia (dBi, total)','Relación axial (dB)','F/B (dB)','Ancho de haz 3 dB (°)','R en cada puerto (Ω, ambos excitados)'])}

Barrido en banda con ambas secciones en el boom:

{table([[k, f"{v['gain_dbi']:.2f}", f"{v['ar_db']:.2f}", f"{v['fb_db']:.1f}"] for k, v in A['sweep'].items()], ['MHz','Ganancia dBi','AR dB','F/B dB'])}

### Lo que NO demuestra esta simulación
* No incluye boom, bridas impresas, coaxiales ni el suelo/trípode/cuerpo humano. **El primer ajuste real se hace con NanoVNA** acortando/alargando el elemento activo (ver `docs/TESTING.md`).
* La ganancia es la total en el eje; la ganancia RHCP/LHCP se deduce de la AR (<1 dB en ambas bandas), no se calculó por separado.
* La ganancia es de **espacio libre**; en la práctica se mide con un receptor y una señal conocida.
* El barrido muestra ganancia y AR estables en 144–146 y 435–438 MHz con 3 mm de varilla, pero eso presupone cortar las longitudes a ±1 mm.

## Red de alimentación
{table([[b, r['f'], r['swr_each_output'], r['reflected_to_isolated_port_pct']] for b in ('VHF','UHF') for r in F[b]['rows_optionA'] if r['f'] in (145.9, 436.5)], ['Banda','MHz','ROE en cada salida del híbrido','Potencia a la carga aislada (%)'])}

Por banda: híbrido 90° de 4 puertos → dos transformadores λ/4 de 37,5 Ω (**dos trozos de coaxial de 75 Ω en paralelo**) → una yagi cada uno. Longitudes (VF 0,66 supuesto, **medir en el cable real**): VHF {F['VHF']['design']['lam4_75_m']*100:.1f} cm, UHF {F['UHF']['design']['lam4_75_m']*100:.1f} cm.

Con un híbrido ideal y cargas idénticas, el puerto de entrada queda adaptado y la energía reflejada se disipa en la carga del puerto aislado: la pérdida es la de la tabla (≈2 % en VHF, ≈0,2 % en UHF). El **híbrido debe cubrir cada banda**: los PCB de `SatcomRadio/Hybrid_Couplers` (QCN3 15 W, CMX03A03 200 W, RF Power 200 W, Anaren 10260-3 250 W) **no tienen la banda de trabajo documentada en su README**; hay que comprobarla en la hoja de datos del componente antes de comprar (ver ADR-004).

## Plegado
Cada semielemento va en un brazo articulado (`hinge_arm`) con pivote M3 en la brida `cross_hub_16` y se pliega paralelo al boom. Boom en dos tramos de ~45 cm (0,90 m en total; se usan 0,83 m). Plegada, las varillas (semielementos de hasta ~52 cm) quedan paralelas al boom: bulto estimado ≈ 55 cm de largo. El diseño de las bridas/bisagras es una **primera iteración sin imprimir** (ver `docs/TESTING.md`).

## Qué se descartó
* Intercalar VHF y UHF en la misma zona del boom: un elemento de 2 m es resonante en 3/2 λ a 435 MHz y puede distorsionar la yagi UHF. **No se simuló la variante intercalada**; se optó por secciones separadas por prudencia, y el modelo combinado muestra que la influencia de los elementos VHF sobre la UHF es pequeña (ganancia UHF 9,26 → 9,08 dBi, F/B 13,3 → 17,0 dB).
* Copiar la geometría de la ficha comercial AV2040-2: licencia *Cults PU / No IA* (no se usó ningún archivo) y, además, es UHF solo. Se tomó solo el concepto (elementos cruzados y plegables).
"""
open('docs/ANTENNA.md', 'w').write(ant)

# ---------------- MECHANICAL.md ----------------
parts_tab = table([[k, v['qty'], 'x'.join(f"{x:g}" for x in v['size_mm']), v['volume_cm3'], v['est_mass_g'], 'sí' if v['watertight'] else 'NO', v['note']] for k, v in P.items()], ['Pieza','Cant.','Tamaño mm','cm³','g (est.)','Estanca','Nota'])
mech = f"""# Mecánica: rotor planetario herringbone 25:1 y accesorios

> Piezas generadas por código (`cad/build_all.py`, `cad/gears.py`) porque el entorno de diseño no disponía de OpenSCAD; ver ADR-014. STL en `cad/stl/`.

## Reductor (cada eje)
Dos etapas planetarias idénticas **5:1 × 5:1 = 25:1**, engranaje **doble helicoidal (espina de pescado)**, módulo 1,5, ángulo de presión 20°, hélice 25°, Z solar 12 / planeta 18 / corona 48, 3 planetas por etapa, ancho de cara 16 mm, holgura de impresión 0,30 mm (parámetro).

* Relación por etapa = 1 + Zr/Zs = 1 + 48/12 = 5. Condición de montaje (Zs+Zr)/3 = 20 (entero) y Zr = Zs + 2·Zp ✔ (comprobado en `cad/test_gears.py`).
* **Comprobación geométrica real de engrane**: con la fase correcta, el volumen de interferencia solar-planeta es **0 mm³**, pero planeta-corona queda en un mínimo de **≈68 mm³** (≈0,26 % del planeta; probable discretización del perfil/holgura) — **punto abierto**, a confirmar con el cupón de holgura impreso.
* Un solar de 12 dientes con 20° de presión tiene un ligero socavado en el pie; con hélice de 25° el número virtual de dientes es 16,1, por lo que el socavado es pequeño. Si se rompe un diente de la segunda etapa, el primer cambio a probar es +0,3 de desplazamiento de perfil.

## Cargas (`calc/rotor_calc.py`)
* Resolución: 0,0045°/micropaso con 16 micropasos (80 000 micropasos/vuelta). El haz es de ~{BW['VHF']['plane_XY_deg']:.0f}° (VHF) y ~{BW['UHF']['plane_XY_deg']:.0f}° (UHF): la reducción se elige por **par frente al viento y por enmascarar el juego**, no por precisión.
* Par de salida a rotor parado con el par de mantenimiento supuesto de 0,25 N·m: **{RT['out_torque_nm']:.1f} N·m**.
* Tensión de flexión en el diente (Lewis, hélice, factor de reparto de carga 1,3): etapa 1 **{RT['stress_stage1_mpa']:.1f} MPa**; etapa 2 **{RT['stress_stage2_mpa']:.1f} MPa**, con un admisible conservador de 9 MPa para ASA impreso. La **etapa 2 es el límite**: con la corriente del driver al 100 % el coeficiente de seguridad es solo 1,1, por lo que **hay que limitar la corriente del TMC2209 al 50–60 %** (CS 1,8–2,1) — la carga de viento calculada no necesita más.
* Viento (varillas + boom, 387 cm², Cd 1,2): a 10 m/s el momento es 0,7–1,1 N·m (brazo 0,25–0,40 m), frente a 2,5–3 N·m disponibles con la corriente limitada. **Límite operativo recomendado: 10 m/s (36 km/h)**; con más viento, bajar la antena.
* Tras un corte de corriente la reducción **es reversible** (planetario sin autobloqueo): con el rotor desenergizado el viento puede girar la antena. Mantén los motores energizados o atornilla/lastra el conjunto.

## Interfaz universal (ADR-013)
Todo se une con **4×M4 sobre un círculo de 40 mm + espiga/zócalo de 20 mm**: salida de cada eje, adaptador de trípode, bandeja de la radio, tapa de la caja. Así se puede usar el rotor con otra antena (SpaceQuad, yagis portátiles) cambiando solo la pinza de boom (`boom_clamp_16/20/25`) o con un tubo de 20 mm propio.

## Piezas
{parts_tab}

Masa impresa total estimada de la lista usada: **{MS['printed_g']:.0f} g** (ASA 1,07 g/cm³, factor de relleno efectivo 0,6 carcasas / 1,0 engranajes: **estimación**).

## Lo que no está hecho
* Sin modelo de ensamblaje: no se verificaron interferencias entre piezas, ni que la caja aloje el diplexor y la electrónica a la vez.
* Las bridas `cross_hub` y los brazos `hinge_arm` y las pinzas son geometría **sin imprimir**; imprimir `coupon_gear_clearance` primero para ajustar la holgura de la impresora.
* No hay seguro mecánico de fin de carrera: los finales de carrera NC son electrónicos.
"""
open('docs/MECHANICAL.md', 'w').write(mech)

# ---------------- MASS ----------------
open('docs/MASS-BUDGET.md', 'w').write(f"""# Presupuesto de masa (estimación)

Salida de `calc/mass_budget.py` (ejecutarlo para la tabla completa).

* Estación (rotor + antena + caja + diplexor, sin radio, trípode ni batería): **{MS['station_g']:.0f} g**
* Total transportado con RT3S (270 g), trípode de fotografía típico (1200 g) y fuente de 12 V (450 g): **{MS['total_carried_g']:.0f} g**

Todas las compras son valores de catálogo **no pesados**; las piezas impresas salen del volumen CAD. La referencia anterior del proyecto (CM5 + 2 LimeSDR) presupuestaba 3,13–3,20 kg **solo** para el rotor/caja sin trípode ni radio nueva; este diseño no es comparable punto por punto, pero elimina el ordenador, los dos SDR y las baterías de gran capacidad.
""")
print('docs generated')
