# ADR-015: Alimentación: 12 V externos; batería, trípode y radio contabilizados aparte

**Estado:** Aceptada

## Contexto
Estación portable en montaña, presupuesto bajo, masa mínima.

## Decisión
Entrada 12 V (pack 3S o disparador USB-C PD a 12 V sobre un power bank que ya se lleve), buck a 5 V para ESP32/GNSS, motores a 12 V. Fusible en el positivo.

## Justificación y evidencia
Potencia de motores limitada al 50–60 % de la nominal. Consumo y autonomía **no calculados ni medidos**.

## Consecuencias y límites
No se ha medido consumo ni autonomía; no se afirma ninguna.
