# Antena, RF y radio SDR

Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.

Ejecutar con el [procedimiento NanoVNA](10-nanovna.md) y las
[hojas rellenables](laboratorio/README.md). Para LNA, protección, PA,
aislamiento y 25 W usar el [banco RF activo](11-rf-potencia.md):
el NanoVNA nunca se conecta a TX. La verificación con la misma carga
de calibración no sustituye un patrón independiente.

## ANT — Antena y RF pasiva (VNA, híbrido, diplexor)

**Comportamiento esperado del componente.** Con el rotor y los coaxiales en posición real, ROE ≤ 1,5 en la frecuencia central y ≤ 2 en los canales de operación. Una buena ROE NO demuestra polarización circular ni ganancia: se mide o simula el conjunto.

### ANT-01
- [ ] **Acción:** Calibrar el VNA (OPEN, SHORT, LOAD, THRU) en el plano del conector, sin radio conectada.
- **Esperado:** Verificación con carga de 50 Ω: ROE ≈ 1,0.
- **Criterio de aprobación:** Calibración válida antes de cada serie de medidas (G2-1).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### ANT-02
- [ ] **Acción:** Medir cada puerto alimentado de antena por banda con balun/matching y conjunto desplegado, coaxial y rotor en posiciones reales; incluir canales y Doppler, no solo 145/435 MHz. Un reflector sin puerto se comprueba por geometría/continuidad y efecto instalado, no por S11 propio.
- **Esperado:** Curva ROE y frecuencia de mínimo.
- **Criterio de aprobación:** ROE ≤ 1,5 en la central y ≤ 2 en canales; documentar el ancho de banda sin extrapolar (G2-3).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### ANT-03
- [ ] **Acción:** Medir el híbrido por banda: amplitud y fase entre salidas con la otra puerta cargada a 50 Ω.
- **Esperado:** Desequilibrio y fase.
- **Criterio de aprobación:** Desequilibrio ≤ 0,5 dB y fase 90° ± 5° en las frecuencias elegidas (G2-4); carga aislada adecuada.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### ANT-04
- [ ] **Acción:** Medir el diplexor 2 m/70 cm: pérdida de inserción por rama, pérdida de retorno y aislamiento entre ramas.
- **Esperado:** S21, S11 y S21 cruzado.
- **Criterio de aprobación:** Pérdida ≤ 1 dB por rama, retorno ≥ 14 dB y aislamiento ≥ 40 dB como cribado (G2-5); 40 dB no garantiza ausencia de desensibilización con TX.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### ANT-05
- [ ] **Acción:** Repetir ROE tras 50 plegados/despliegues y revisar continuidad de contactos RF.
- **Esperado:** ROE y continuidad sin deriva.
- **Criterio de aprobación:** Variación de ROE < 0,1 y continuidad estable; las bisagras plásticas no son el único contacto RF (G2-7).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### ANT-06
- [ ] **Acción:** Medir o simular patrón, sentido RHCP/LHCP y relación axial con el conjunto completo (antena + coaxial + rotor).
- **Esperado:** Relación axial hacia el satélite.
- **Criterio de aprobación:** Relación axial ≤ 3 dB para anunciar polarización circular (G2-6); sin este dato se anuncia solo lineal/cruzada.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### ANT-07
- [ ] **Acción:** Con receptor y generador (o SDR como fuente), medir el nivel mínimo detectable con rotor y convertidores apagados y encendidos.
- **Esperado:** Piso de ruido con y sin motores.
- **Criterio de aprobación:** Diferencia documentada; el aumento de ruido con motores activos debe ser aceptable para la señal objetivo (G3-6).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

## RAD — Radio SDR (2 × LimeSDR Mini + CM5) y audio

**Comportamiento esperado del componente.** La radio funciona en recepción sin rotor, con dos SDR identificados por número de serie (VHF y UHF). TX permanece inhibido: solo se habilita con permiso físico, watchdog y lease, tras cualificar con carga.

### RAD-01
- [ ] **Acción:** Conectar ambos LimeSDR por USB y comprobar el descubrimiento; anotar los dos números de serie y la asignación VHF/UHF.
- **Esperado:** Dos dispositivos distintos reconocidos.
- **Criterio de aprobación:** Nunca "el primer USB hallado": selección explícita por número de serie.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### RAD-02
- [ ] **Acción:** Pedir tasas y frecuencias y leerlas del hardware; abrir dos flujos RX concurrentes (VHF y UHF).
- **Esperado:** Valores leídos del hardware.
- **Criterio de aprobación:** Una tasa solicitada no es una tasa comprobada: se anota la leída; sin pérdidas de muestras en 10 min.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### RAD-03
- [ ] **Acción:** Alimentar un tono/FM de referencia y verificar demodulación en VHF y UHF; probar DSP primero con WAV/vectores y luego con recepción real.
- **Esperado:** Audio demodulado correcto.
- **Criterio de aprobación:** SNR y distorsión anotados; sin mezclar los tonos SSTV/APRS de los dos receptores.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### RAD-04
- [ ] **Acción:** Probar el transporte de audio Bluetooth PCM (S16LE, mono, 8000 muestras/s): créditos, pérdidas y reconexión.
- **Esperado:** Flujo continuo sin cortes.
- **Criterio de aprobación:** Sin underruns en 10 min; el canal VHF/UHF activo se selecciona explícitamente; el transporte no implica HFP/A2DP.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### RAD-05
- [ ] **Acción:** Sin permiso físico de TX, intentar PTT desde el host/app y desde GPIO (PTT_VHF_REQUEST BCM22, PTT_UHF_REQUEST BCM23).
- **Esperado:** PTT rechazado; salidas aisladas abiertas (inhibidas); realimentación PTT coherente.
- **Criterio de aprobación:** Ningún TX posible sin permiso, watchdog y lease; probar con carga de 50 Ω, nunca con antena.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### RAD-06
- [ ] **Acción:** Solo con licencia y autorización: cualificar TX a mínima potencia con carga: espectro, armónicos (145×3 = 435 MHz), bloqueo y temperatura.
- **Esperado:** Espectro limpio y temperatura estable.
- **Criterio de aprobación:** Armónicos y espurios dentro de los límites; un solo TX activo; G4 solo tras G1-G3 aprobados.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

[Volver al índice](README.md)
