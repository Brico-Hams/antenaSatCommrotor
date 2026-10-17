# Pruebas: componentes, comportamiento y banco

Esta sección describe CÓMO probar cada componente del PortableSatStation **antes de fabricar las PCB** y antes de integrar la estación: banco de pruebas, checklists, comportamiento esperado y criterios de aprobación. Complementa las puertas G0-G4 de [ACCEPTANCE.md](../ACCEPTANCE.md) y el registro de [VALIDATION.md](../VALIDATION.md).

> **Estado:** prototipo digital, **no validado físicamente**. Nada de lo que sigue se ha medido todavía: todos los ensayos están PENDIENTES hasta anotar medida, fecha e instrumento. Los criterios con referencia `Gn-m` provienen de ACCEPTANCE.md; los demás son valores de ingeniería **propuestos** por esta revisión que deben confirmarse o ajustarse con el primer prototipo. Compilar o pasar pruebas de software no valida cableado, mecánica ni RF.

## Cómo usar esta sección
El [expediente real de laboratorio](09-laboratorio.md) añade hojas
rellenables por ensayo y componente, [cuaderno imprimible](laboratorio/cuaderno.html)
y procedimientos detallados de [NanoVNA](10-nanovna.md),
[RF activa hasta el techo de 25 W](11-rf-potencia.md) y
[calibración de instrumentos/sensores/mecánica](12-calibraciones.md).
Copiar las [plantillas](laboratorio/README.md) antes de rellenar; no se
han ejecutado estas pruebas ni se levantan los HOLD del proyecto.

1. Monte el banco de la guía [01-banco-de-pruebas.md](01-banco-de-pruebas.md) por niveles (B0 → B4).
2. Ejecute los checklists en orden: electrónica → puerta PCB → mecánica → RF/radio → software/OS → app Android → sistema.
3. Anote cada resultado en [registro-pruebas.csv](registro-pruebas.csv) (una fila por ensayo) con fecha, revisión Git, instrumentos y operador.
4. **Parada:** si falla un ensayo de seguridad (PWR, DRV-02/05, SNS-04, MEC-05) no avance a motores bajo carga ni a RF.
5. No pida la fabricación de ninguna PCB hasta cerrar la [puerta previa](03-puerta-pcb.md).

## Seguridad
Supervisión adulta, parada de emergencia accesible, fuente con límite de corriente, motores sin carga en las primeras pruebas, gafas al taladrar/lijar, sin transmitir sin licencia, carga de 50 Ω (no antena) para todo ensayo de TX, 12 V nunca en la cabecera del CM5.

## Mapa de ensayos
| Documento | Secciones | Puerta |
|---|---|---|
| [01-banco-de-pruebas.md](01-banco-de-pruebas.md) | Diseño del banco de pruebas | — |
| [02-electronica.md](02-electronica.md) | Electrónica: alimentación, drivers y sensores (PWR, DRV, SNS) | G1E |
| [03-puerta-pcb.md](03-puerta-pcb.md) | Puerta previa a fabricar las PCB (PCB) | G1E |
| [04-mecanica.md](04-mecanica.md) | Mecánica del rotor (MEC) | G1 |
| [05-rf-y-radio.md](05-rf-y-radio.md) | Antena, RF y radio SDR (ANT, RAD) | G2 / G4 |
| [06-software-y-os.md](06-software-y-os.md) | Software, hosts CM5 e imagen del sistema operativo (SW) | G0 |
| [07-app-android.md](07-app-android.md) | Aplicación Android (APP) | G3 |
| [08-sistema.md](08-sistema.md) | Integración del sistema (G3 / G4) (SYS) | G3 / G4 |
| [09-laboratorio.md](09-laboratorio.md) | Expediente, bancos físicos, estados, incertidumbre y formularios | Todas |
| [10-nanovna.md](10-nanovna.md) | SOL/THRU, verificación independiente, S11/S21, filtros y fase | G2 |
| [11-rf-potencia.md](11-rf-potencia.md) | LNA, interlock, cadena de medida, potencia/emisiones y campo | G2 / G4 |
| [12-calibraciones.md](12-calibraciones.md) | DC, tiempo, sensores, metrología mecánica, SDR/audio y sistema | G1E / G1 / G3 |
| [13-ensayos-laboratorio.md](13-ensayos-laboratorio.md) | LAB-01 a LAB-24 y fichas suplementarias | Todas |

Figuras con el logo de BricoHams y los autores: T1 (banco), T2 (comprobador GPIO), T3 (fixture mecánico) en `fig/`.

Registro: [registro-pruebas.csv](registro-pruebas.csv). Montaje: [guía de ensamblaje](../assembly/README.md). Ayuda de la app: `android/app/src/main/res/raw*/`.
