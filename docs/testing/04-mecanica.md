# Mecánica del rotor

Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.

## MEC — Mecánica del rotor (AZ / EL / POL)

**Comportamiento esperado del componente.** Los ejes giran suaves sin motor, la correa mantiene tensión, los topes físicos detienen antes de dañar cables y la transmisión no pierde pasos bajo la carga objetivo. 8 m/s de viento NO es un límite autorizado hasta medir par real.

### MEC-01
- [ ] **Acción:** Imprimir cupones de prueba (agujero, eje, inserto) y medir contracción del ASA con calibre; imprimir copas de rodamiento y retenedores.
- **Esperado:** Cotas medidas frente a nominales.
- **Criterio de aprobación:** Compensación registrada; encaje 608/6000 sin forzar ni holgura apreciable; sin lijar para ocultar fallos.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-02
- [ ] **Acción:** Montar el reductor de correa SIN motor (20T:100T ×2 = 25:1, correas GT2 de 252 mm); girar la salida a mano una vuelta completa.
- **Esperado:** Giro suave y uniforme, sin saltos de diente ni roce de correa.
- **Criterio de aprobación:** Par de giro a mano uniforme; correa alineada y sin tocar placas; separación de 1 mm entre etapas.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-03
- [ ] **Acción:** Medir tensión de correa (flecha con carga en el centro del tramo) con las ranuras de ±1,5 mm; tras 30 min repetir.
- **Esperado:** Tensión estable tras el rodaje.
- **Criterio de aprobación:** Sin deslizamiento ni pérdida de tensión >10 %; tornillos con fijador/arandelas, sin aflojarse.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-04
- [ ] **Acción:** Confirmar que la polea de entrada de la 2ª etapa está fija al eje de salida de la 1ª (no flota) y el eje de salida está sostenido por dos rodamientos.
- **Esperado:** Par transmitido sin deslizamiento con el motor bloqueado y par aplicado a mano en la salida.
- **Criterio de aprobación:** Cero giro relativo entre polea y eje; salida concéntrica.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-05
- [ ] **Acción:** Homing sin antena con el final de carrera: a) conectado, b) desconectado, c) pegado, d) no alcanzado.
- **Esperado:** a) fija AZ=-180°, EL=0°; b,c,d) fallo con timeout.
- **Criterio de aprobación:** Nunca movimiento ilimitado; el fallo exige rehome (G1-6).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-06
- [ ] **Acción:** Medir holgura (backlash) invirtiendo el sentido con indicador de dial o goniómetro en cada eje.
- **Esperado:** Valor en grados por eje.
- **Criterio de aprobación:** Registrado y compensado en software; objetivo orientativo ≤ 1°; coherente con SNS-03.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-07
- [ ] **Acción:** Equilibrar la carga objetivo (0,5 kg de antena) y medir el CG respecto al eje; ensayo con retención secundaria sobre banco estable antes del trípode.
- **Esperado:** CG dentro de 30 mm del eje.
- **Criterio de aprobación:** CG ≤ 30 mm; el eje EL no cae al cortar la energía o está retenido (par de reposo sin motor).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-08
- [ ] **Acción:** Seguimiento lento sin viento: barrer cada eje y comparar la posición del encoder con goniómetro/indicador de referencia en 10 posiciones.
- **Esperado:** Error por posición.
- **Criterio de aprobación:** Precisión ≤ 2° RMS y desviación máxima ≤ 5° (G1-9); separar error de rumbo y error de eje.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-09
- [ ] **Acción:** Mantener 30 min movimiento alterno bajo la carga objetivo; comprobar pérdida de pasos, aflojamiento y temperatura.
- **Esperado:** Posición de retorno idéntica al inicio.
- **Criterio de aprobación:** Sin pérdida de pasos (error final < 1°), sin tornillos flojos, temperaturas dentro de límite (G1-10).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### MEC-10
- [ ] **Acción:** Pesar el conjunto completo operativo (incluye trípode, radio y cables; excluye la batería externa, que se pesa aparte) y medir el bulto plegado.
- **Esperado:** Masa total y dimensiones.
- **Criterio de aprobación:** Masa ≤ 5 kg según el requisito vigente (el ≤ 3 kg anterior es histórico); registrar la masa de la batería aparte.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

[Volver al índice](README.md)
