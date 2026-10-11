# ADR-016: Diplexor existente integrado en la caja de control

**Estado:** Aceptada con punto abierto

## Contexto
El usuario ya tiene el diplexor BRICOHAMS (72 × 40 mm, Gerbers) y el Rev A BNC de 25 W (80 × 60 mm, no validado en laboratorio según su propio README).

## Decisión
La caja de control incluye una cara con tres pasamuros (J1 antena, J2 VHF, J3 UHF) y una bahía para el PCB. La radio RT3S (5 W) entra por J1; J2/J3 llevan a los dos híbridos.

## Justificación y evidencia
Se reutiliza hardware ya diseñado y a 5 W queda muy por debajo de su objetivo de 25 W.

## Consecuencias y límites
El encaje físico del PCB de 80 × 60 mm junto a la electrónica en la caja de 112 × 82 mm **no está verificado en un ensamblaje**; los taladros de los conectores son aproximados. Verificar con VNA antes de usar.
