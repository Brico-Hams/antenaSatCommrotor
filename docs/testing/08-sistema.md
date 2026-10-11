# Integración del sistema (G3 / G4)

Cada ensayo es una casilla: márquela solo con medida, fecha e instrumento anotados en el registro.

## SYS — Integración del sistema y puertas G3 / G4

**Comportamiento esperado del componente.** Con todos los módulos aceptados por separado se integra en este orden: mecánica sin RF, RF pasiva, recepción y control, y solo al final transmisión autorizada. Nada se reutiliza al cambiar de ubicación: se vuelve a calibrar.

### SYS-01
- [ ] **Acción:** Seguir el pase de un satélite real y compararlo con una referencia independiente, misma estación y TLE.
- **Esperado:** Apuntamiento durante todo el pase.
- **Criterio de aprobación:** Error de apuntamiento dentro del haz de la antena (G3-1); registro AZ/EL comandado vs. medido.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SYS-02
- [ ] **Acción:** Sin Internet (AP propio): importar TLE, seleccionar, predecir y seguir; cerrar la app durante el pase.
- **Esperado:** El seguimiento continúa en el controlador.
- **Criterio de aprobación:** Cálculo y seguimiento no dependen del teléfono (G3-2/3).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SYS-03
- [ ] **Acción:** Provocar: pérdida de GNSS, UTC inválida, caché antigua, encoder perdido, pase bajo el horizonte, zenit, cable wrap y velocidad inalcanzable.
- **Esperado:** Política documentada, aviso y parada segura en cada caso.
- **Criterio de aprobación:** Se rechaza explícitamente; nunca se apunta a un objetivo incorrecto (G3-4/5).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SYS-04
- [ ] **Acción:** Confirmar el norte verdadero con una referencia conocida; mover el trípode y repetir la calibración.
- **Esperado:** Orientación verdadera confirmada en cada ubicación.
- **Criterio de aprobación:** La calibración no se reutiliza en una ubicación nueva (G3-7).
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SYS-05
- [ ] **Acción:** Pesar el conjunto operativo y medir la autonomía con la batería elegida durante un ensayo continuo de 2 horas.
- **Esperado:** Masa y autonomía medidas.
- **Criterio de aprobación:** ≤ 5 kg sin la batería externa y autonomía objetivo de 2 h demostrada por ensayo, no por cálculo.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

### SYS-06
- [ ] **Acción:** G4, solo con licencia: transmisión de prueba sobre carga a mínima potencia y luego pase real autorizado; vigilar temperatura de redes y conectores.
- **Esperado:** Transmisión limpia; ningún TX con red sin adaptar o fuera del rango del diplexor/híbrido.
- **Criterio de aprobación:** Un solo TX activo; el monitoreo de bajada propia exige un segundo receptor protegido; no se anuncia full-duplex con un filtro pasivo.
- _Resultado medido ____ · Fecha ____ · Instrumento ____ · Estado: PENDIENTE_

[Volver al índice](README.md)
