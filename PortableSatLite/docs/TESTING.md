# Pruebas: qué está verificado y qué no

`tests/run_all.sh` ejecuta todo lo verificable en un PC. Resultados de la última ejecución (ver también `docs/ANTENNA.md`, `docs/MECHANICAL.md`):

| Qué | Cómo | Resultado |
|---|---|---|
| `satcore.h` (inclinación, rumbo, declinación, az/el ↔ ejes del rotor, modo norte manual) | 2000 casos aleatorios frente a un modelo independiente de matrices de rotación | error máx. 1,7·10⁻⁶ ° (limitado por la precisión del texto de entrada); ida y vuelta 5·10⁻¹⁰ ° |
| Librería SGP4 usada por el firmware | 120 muestras (10 h) frente a `python-sgp4` | Δaz 0,001°, Δel 0,002°, Δdistancia 0,03 km |
| Buscador de pases | ISS, 36 h, frente a barrido de referencia a 10 s | 6/6 pases, AOS/TCA/LOS ≤ 9 s, Δelevación máx ≤ 0,34° |
| Parser de TLE | checksum, filtro por alias, época | rechaza checksum malo; época = python-sgp4 |
| Interfaz web | Chromium sin cabeza contra `mock_server.py`, 390 px de ancho | sin errores de consola, lista pases, inicia seguimiento, sin desbordamiento horizontal, cambia de idioma |
| Engrane del planetario | intersección booleana de sólidos | sol–planeta 0 mm³ en fase correcta; planeta–corona mínimo 68 mm³ (≈0,26 % del volumen del planeta, probable efecto de la discretización del perfil/holgura CLR=0,30) → **sin resolver**: confirmar con el cupón de holgura impreso |
| Antena | NEC2 (`calc/antenna_nec.py`) | tablas de `docs/ANTENNA.md` |
| Piezas | trimesh | todas estancas |

## NO verificado (hay que hacerlo con hardware)
1. **El firmware no se ha compilado ni ejecutado en un ESP32** (no hay PlatformIO en el entorno de creación). Es lo primero que fallará: errores de sintaxis/API son probables. Se compiló en PC solo `satcore.h`, `tracker.h`, `tle.h` y la librería SGP4 con un `Arduino.h` simulado.
2. Motores, drivers, finales de carrera, GNSS, IMU y magnetómetro, y la coherencia de ejes de `to_body()`.
3. Piezas impresas: ajuste de holgura, bisagras, bridas, pinzas, encaje de la caja con el diplexor, resistencia real del diente de la etapa 2.
4. RF: ROE, ganancia, relación axial, aislamiento del diplexor y banda de los híbridos.
5. Consumo, autonomía, masa real.

## Orden de puesta en marcha
1. Imprimir `coupon_gear_clearance`; ajustar `CLR`. Montar **un eje** sin antena.
2. Cargar el firmware (`pio run -t upload && pio run -t uploadfs`). Comprobar la web en `SatLite-XXXX` y los sensores en `/api/state` **antes de alimentar motores** (inclinar a mano y ver roll/pitch; girar y ver el rumbo).
3. Finales de carrera: probar que abrir el cable los activa. Driver al 50 % de corriente. Mover 10° y comprobar el sentido; si es inverso, invertir DIR.
4. Con el motor sin carga, `home` y seguir un pase real **sin antena** y comparar con la posición del satélite en otra app.
5. Montar antena VHF/UHF; **NanoVNA**: cortar el elemento activo, ajustar ±1 mm hasta ROE mínima en 145,9 y 436,5 MHz; comprobar los transformadores λ/4 (VF real) y el híbrido; luego diplexor con carga de 50 Ω y baja potencia.
6. Primera recepción de la ISS antes de transmitir. TX solo con licencia y verificando las frecuencias vigentes (AMSAT).
