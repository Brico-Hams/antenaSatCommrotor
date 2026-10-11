# Montaje de la electronica

Ver [ELECTRICAL.md](../ELECTRICAL.md), [PCB.md](../PCB.md), [CM5-PCB.md](../CM5-PCB.md).

## 1. PCB portadora
![E1 ](fig/E1-pcb-carrier.svg)

*E1* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

## 2. PCB cm5-guard-A (solo revision)
![E2 ](fig/E2-pcb-cm5-guard.svg)

*E2* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

Esta placa **no es apta para fabricacion**; DRC/ERC en KiCad pendiente tras anadir el logo.

## 3. Cableado GPIO
![E3 ](fig/E3-cableado-gpio.svg)

*E3* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

Fuente unica: `hardware/cm5/interface.json`. Los pasos de motor nunca se generan por GPIO de Linux.
