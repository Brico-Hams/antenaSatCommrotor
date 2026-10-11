# Mecánica: rotor planetario herringbone 25:1 y accesorios

> Piezas generadas por código (`cad/build_all.py`, `cad/gears.py`) porque el entorno de diseño no disponía de OpenSCAD; ver ADR-014. STL en `cad/stl/`.

## Reductor (cada eje)
Dos etapas planetarias idénticas **5:1 × 5:1 = 25:1**, engranaje **doble helicoidal (espina de pescado)**, módulo 1,5, ángulo de presión 20°, hélice 25°, Z solar 12 / planeta 18 / corona 48, 3 planetas por etapa, ancho de cara 16 mm, holgura de impresión 0,30 mm (parámetro).

* Relación por etapa = 1 + Zr/Zs = 1 + 48/12 = 5. Condición de montaje (Zs+Zr)/3 = 20 (entero) y Zr = Zs + 2·Zp ✔ (comprobado en `cad/test_gears.py`).
* **Comprobación geométrica real de engrane**: con la fase correcta, el volumen de interferencia solar-planeta es **0 mm³**, pero planeta-corona queda en un mínimo de **≈68 mm³** (≈0,26 % del planeta; probable discretización del perfil/holgura) — **punto abierto**, a confirmar con el cupón de holgura impreso.
* Un solar de 12 dientes con 20° de presión tiene un ligero socavado en el pie; con hélice de 25° el número virtual de dientes es 16,1, por lo que el socavado es pequeño. Si se rompe un diente de la segunda etapa, el primer cambio a probar es +0,3 de desplazamiento de perfil.

## Cargas (`calc/rotor_calc.py`)
* Resolución: 0,0045°/micropaso con 16 micropasos (80 000 micropasos/vuelta). El haz es de ~82° (VHF) y ~70° (UHF): la reducción se elige por **par frente al viento y por enmascarar el juego**, no por precisión.
* Par de salida a rotor parado con el par de mantenimiento supuesto de 0,25 N·m: **5.1 N·m**.
* Tensión de flexión en el diente (Lewis, hélice, factor de reparto de carga 1,3): etapa 1 **1.9 MPa**; etapa 2 **8.4 MPa**, con un admisible conservador de 9 MPa para ASA impreso. La **etapa 2 es el límite**: con la corriente del driver al 100 % el coeficiente de seguridad es solo 1,1, por lo que **hay que limitar la corriente del TMC2209 al 50–60 %** (CS 1,8–2,1) — la carga de viento calculada no necesita más.
* Viento (varillas + boom, 387 cm², Cd 1,2): a 10 m/s el momento es 0,7–1,1 N·m (brazo 0,25–0,40 m), frente a 2,5–3 N·m disponibles con la corriente limitada. **Límite operativo recomendado: 10 m/s (36 km/h)**; con más viento, bajar la antena.
* Tras un corte de corriente la reducción **es reversible** (planetario sin autobloqueo): con el rotor desenergizado el viento puede girar la antena. Mantén los motores energizados o atornilla/lastra el conjunto.

## Interfaz universal (ADR-013)
Todo se une con **4×M4 sobre un círculo de 40 mm + espiga/zócalo de 20 mm**: salida de cada eje, adaptador de trípode, bandeja de la radio, tapa de la caja. Así se puede usar el rotor con otra antena (SpaceQuad, yagis portátiles) cambiando solo la pinza de boom (`boom_clamp_16/20/25`) o con un tubo de 20 mm propio.

## Piezas
| Pieza | Cant. | Tamaño mm | cm³ | g (est.) | Estanca | Nota |
|---|---|---|---|---|---|---|
| gear_sun_motor | 2 | 20.7x20.7x16 | 3.26 | 3.5 | sí | NEMA17 5 mm shaft (use grub screw M3 on a flat); 1 per axis |
| gear_planet | 12 | 29.7x29.7x16 | 8.24 | 8.8 | sí | 3 per stage x 2 stages x 2 axes |
| rotor_housing | 2 | 92x92x48 | 105.99 | 68.0 | sí | two internal herringbone rings, one piece; 6 x M3 through-bolts |
| carrier1_plate_A | 2 | 76.4x76.4x4 | 17.55 | 11.3 | sí | planet axles pressed (4 mm rod, 3 per plate) |
| carrier1_plate_B_sun2 | 2 | 76.4x76.4x20 | 21.52 | 23.0 | sí | plate with integrated 2nd-stage sun (print upright, tune clearance) |
| carrier2_plate_A | 2 | 76.4x76.4x4 | 17.36 | 11.1 | sí | rides on sun2 hub, axles pressed |
| output_flange | 2 | 76.4x76.4x22 | 28.68 | 18.4 | sí | universal interface: 4xM4 on 40 mm PCD + 20 mm spigot |
| rotor_endcap | 2 | 92x92x10 | 53.73 | 34.5 | sí | 6806 bearing seat; 6 x M3 same circle as the housing |
| motor_plate | 2 | 92x92x6 | 36.85 | 23.7 | sí | NEMA17 31 mm square pattern, 6xM3 to the housing |
| tripod_adapter_1-4 | 1 | 68x68x18 | 30.72 | 19.7 | sí | M4 flange side + 1/4"-20 screw (hex nut M6.35 trap underneath); 3/8" tripods: use stock reducer bush |
| stub_spigot_20 | 2 | 20x20x80 | 18.83 | 12.1 | sí | OPTIONAL printed stub; cheaper: 20 mm aluminium/CF tube 1 mm wall (BOM) |
| boom_clamp_16_lower | 1 | 40x36x17 | 16.6 | 10.7 | sí | for 16 mm boom; bolts 2xM4 (nut traps omitted -> use nylock + washer) |
| boom_clamp_16_upper | 1 | 40x36x17 | 20.19 | 13.0 | sí |  |
| boom_clamp_20_lower | 1 | 40x36x17 | 15.41 | 9.9 | sí | for 20 mm boom; bolts 2xM4 (nut traps omitted -> use nylock + washer) |
| boom_clamp_20_upper | 1 | 40x36x17 | 18.19 | 11.7 | sí |  |
| boom_clamp_25_lower | 1 | 40x36x17 | 13.16 | 8.5 | sí | for 25 mm boom; bolts 2xM4 (nut traps omitted -> use nylock + washer) |
| boom_clamp_25_upper | 1 | 40x36x17 | 14.98 | 9.6 | sí |  |
| cross_hub_16 | 7 | 20x38x38 | 7.57 | 4.9 | sí | 1 per element station (3 VHF + 4 UHF); 4 hinge lugs for M3 pivots |
| hinge_arm | 28 | 12x5x21 | 1.0 | 0.6 | sí | swing arm: 3.1 mm bore for the 3 mm aluminium rod (epoxy/M2 grub); folds along the boom |
| radio_cradle_RT3S | 1 | 68x44x40 | 32.81 | 21.1 | sí | open-top tray, 4xM4 on 40 mm PCD (same as every interface) + Velcro strap through the side windows; internal size is a PARAMETER |
| control_box | 1 | 112x82x42.2 | 62.03 | 39.8 | sí | ESP32 + 2xTMC2209 + buck/PD + diplexer bay (72x40 PCB, BNC/SMA bulkheads on +X face) |
| control_box_lid | 1 | 112x82x2.4 | 21.9 | 14.1 | sí |  |
| coupon_gear_clearance | 1 | 30x30x8 | 4.35 | 4.6 | sí | print this first: check it slides on the 4 mm pin and meshes with a printed sun tooth coupon |

Masa impresa total estimada de la lista usada: **662 g** (ASA 1,07 g/cm³, factor de relleno efectivo 0,6 carcasas / 1,0 engranajes: **estimación**).

## Lo que no está hecho
* Sin modelo de ensamblaje: no se verificaron interferencias entre piezas, ni que la caja aloje el diplexor y la electrónica a la vez.
* Las bridas `cross_hub` y los brazos `hinge_arm` y las pinzas son geometría **sin imprimir**; imprimir `coupon_gear_clearance` primero para ajustar la holgura de la impresora.
* No hay seguro mecánico de fin de carrera: los finales de carrera NC son electrónicos.
