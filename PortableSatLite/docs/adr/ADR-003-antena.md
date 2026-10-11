# ADR-003: Antena: yagis cruzadas V/U en un solo boom, dos secciones no intercaladas

**Estado:** Aceptada

## Contexto
Hace falta cobertura circular en 145 y 435 MHz con una antena plegable, ligera y barata. Las yagis lineales pierden 5–20 dB por giro de polarización (artículo KX4Z, Fig. 1). La ficha comercial AV2040-2 es UHF solo y su licencia (Cults PU, No IA) impide reutilizar su geometría.

## Decisión
VHF de 3 elementos + UHF de 4 elementos, cruzadas (planos Y/Z en la misma estación), en secciones consecutivas de un boom de 0,83 m.

## Justificación y evidencia
NEC2: VHF 7,6 dBi/AR 0,27 dB/F-B 21,7 dB/haz 82°; UHF 9,1 dBi/AR 0,80 dB/F-B 17,0 dB/haz 70°, con los elementos de la otra banda presentes (`calc/antenna_nec.py`). Un haz de 70–82° tolera un apuntado impreciso, lo que además justifica un rotor barato.

## Consecuencias y límites
Ganancia moderada (no es una SpaceQuad); los resultados de NEC son de espacio libre y necesitan ajuste con NanoVNA.
