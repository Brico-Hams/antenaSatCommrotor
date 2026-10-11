# ADR-004: Polarización circular con híbrido de 90° por banda; descartada la línea de retardo

**Estado:** Aceptada (con punto abierto)

## Contexto
El artículo KX4Z consigue 90° separando físicamente un plano λ/4 del otro (boom largo) y menciona el retardo por coaxial. El repo de SatcomRadio ofrece placas híbridas (MIT) que el usuario pidió combinar.

## Decisión
Un híbrido 90° por banda, cada salida con un transformador λ/4 de 37,5 Ω (2 × coaxial 75 Ω en paralelo) a la yagi. Se desecha la red con línea de retardo.

## Justificación y evidencia
`calc/feed_network.py`: la red con línea de retardo λ/4 y T **no funciona** con las R reales del NEC (21 Ω VHF, 26 Ω UHF): ROE 2,8 y 2,45 y desequilibrio de corrientes de 2,4:1 / 1,9:1 porque la línea de retardo no queda adaptada; con híbrido la ROE por salida es 1,34 (VHF) y 1,09 (UHF) y solo se pierde el 2 % y 0,2 % en la carga aislada. El híbrido además es independiente de la longitud de cables.

## Consecuencias y límites
**Punto abierto**: el README de SatcomRadio no indica la banda de cada placa (QCN3 15 W: "solo para portátiles"; CMX03A03/RF Power 200 W; Anaren 250 W). Hay que verificar en la hoja de datos de cada componente que cubre 145 **y** 435 MHz (si no, un híbrido por banda). Si ninguno cumple, la alternativa es un híbrido de línea acoplada o de ramas λ/4 en PCB propio (no diseñado aquí).
