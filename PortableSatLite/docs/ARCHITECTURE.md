# Arquitectura

```
                      ┌───────────────────────────────────────────── CAJA DE CONTROL (control_box) ─────────────────────────────┐
 Teléfono / tablet    │  ESP32 ── Wi-Fi AP "SatLite-XXXX" (+ STA hotspot para bajar TLE)                                           │
 (navegador, offline) │   │  SGP4 · buscador de pases · Doppler · corrección de inclinación/rumbo (satcore)                         │
        │  HTTP       │   ├─ UART2 ── GNSS (lat, lon, alt, UTC)                                                                    │
        └────────────►│   ├─ I2C0  ── MPU6050 (vertical) · QMC5883L (rumbo, en pod remoto) · [AS5600 AZ]                           │
                      │   ├─ I2C1  ── [AS5600 EL]                                                                                  │
                      │   ├─ STEP/DIR ──► TMC2209 AZ ──► NEMA17 ──► planetario 25:1 ──► brida universal ─► ANTENA (o cualquier otra)│
                      │   ├─ STEP/DIR ──► TMC2209 EL ──► NEMA17 ──► planetario 25:1 ──► brida universal                           │
                      │   └─ finales de carrera NC (AZ0, EL0)                                                                       │
                      │  Diplexor 2 m/70 cm (PCB existente):  J1 ◄── RT3S/OpenGD77   J2 VHF ──► híbrido ──► yagi cruzada VHF        │
                      │                                                               J3 UHF ──► híbrido ──► yagi cruzada UHF        │
                      └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
        La radio RT3S va en una bandeja (radio_cradle_RT3S) sobre la caja o la pata del trípode; NO hay conexión de datos ni PTT con el rotor.
```

## Módulos separables (cada uno funciona solo)
| Módulo | Qué contiene | Se usa solo si... | Interfaz |
|---|---|---|---|
| Antena V/U | boom, 14 varillas, 2 híbridos, 4 transformadores | quieres apuntar a mano en un trípode | 2 × SMA/BNC + pinza de boom (16 mm) |
| Rotor AZ/EL | 2 ejes planetarios, motores, sensores en la caja | quieres montar otra antena (SpaceQuad, yagis) | brida 4×M4/Ø40 + espiga Ø20 |
| Caja de control | ESP32, drivers, GNSS, diplexor | cambias el rotor por otro con STEP/DIR | 2 conectores de motor, 2 de final de carrera, USB-C/12 V |
| Radio + soporte | RT3S + bandeja | operas a mano con antena omni | 4×M4/Ø40 |

## Flujo de datos de un pase
1. UTC y posición: GNSS (o hora/posición del móvil si no hay fijación). 2. La tarea de baja prioridad calcula pases de 24 h para los satélites con TLE. 3. El usuario pulsa *Seguir*. 4. Cada 0,5 s: SGP4 → az/el verdaderos y velocidad de rango → `satcore::target_to_rotor` (inclinación + rumbo + declinación) → eje del rotor → `unwrap_az` (0–450°) → el hardware genera los pulsos. 5. La web muestra rotor, objetivo y frecuencias corregidas por Doppler.

## Qué parte de esto está verificado
Ver `docs/TESTING.md`. En resumen: matemática, SGP4, pases, TLE y web **sí** (en PC); firmware en el ESP32, motores, sensores y RF **no**.
