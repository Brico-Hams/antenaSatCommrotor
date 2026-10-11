# Electrónica

## Pines (ESP32-DevKitC, definidos en `firmware/src/config.h`)
| Función | GPIO | Notas |
|---|---|---|
| AZ STEP / DIR | 26 / 27 | TMC2209 modo STEP/DIR |
| EL STEP / DIR | 25 / 33 | |
| EN (activo bajo, común) | 14 | los drivers se habilitan solo al mover |
| Final de carrera AZ0 / EL0 | 32 / 13 | NC a GND, `INPUT_PULLUP`; cable roto = "pulsado" (fallo seguro) |
| GNSS RX / TX | 16 / 17 | UART2 a 9600 baud (NEO-6M/M8) |
| I2C0 SDA / SCL | 21 / 22 | MPU6050 0x68, QMC5883L 0x0D (y AS5600-AZ 0x36 opcional) |
| I2C1 SDA / SCL | 18 / 19 | AS5600-EL 0x36 (dos AS5600 comparten dirección: buses separados) |

El firmware **no lee aún los AS5600**; el cableado queda previsto para añadir detección de pasos perdidos.

## Sensores y colocación
* **Magnetómetro + acelerómetro en un pod pequeño en la base** (junto al adaptador de trípode), a ≥ 25 cm de los NEMA17, sin tornillería de acero cerca. Los NEMA17 llevan imanes e hierro: junto a ellos la brújula es inútil. La alternativa es **norte manual** (ADR-008).
* Orientación del pod: la matriz `to_body()` de `main.cpp` define cómo se mapean los ejes del sensor a x (adelante, cero del rotor), y (derecha), z (abajo). **Hay que ajustarla al pegar el pod** y comprobarla con la inclinación/rumbo que muestra la web.
* Calibración: web → Ajustes → *Calibrar brújula*: girar toda la estación ~360° despacio mientras corre. Se guarda el centro min/max (hard-iron). Sin calibración soft-iron.
* Declinación: introducir la del lugar y fecha (NOAA/IGRF); no está en el firmware.

## Alimentación
12 V (3S, pack externo o disparador USB-C PD a 12 V) → fusible → motores (TMC2209 VM) y buck a 5 V (ESP32, GNSS, sensores). Condensador de ≥ 100 µF cerca de cada driver. Corriente del driver al 50–60 % de la nominal del motor (ADR-006/007). **No hay medición de consumo**.

## Lista de materiales (precios orientativos, NO cotizados)
Ver `bom/bom.csv`.
