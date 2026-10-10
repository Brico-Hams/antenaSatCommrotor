# Modulo independiente: rotor AZ/EL/POL

## Alcance y dependencias

Construible sin LimeSDR, PA, filtros RF, antena del proyecto ni sistema
de audio. Acepta otra antena solo si su masa, CG y carga son cualificados.
La variante nueva usa CM5/CM5IO y auxiliar; la variante ESP32 de dos ejes
se conserva separada, no satisface automaticamente el tercer eje POL.

| Necesario | No requerido para rotor solo |
| --- | --- |
| Tres ejes, motores/trasmisiones, soportes y fijacion/tripode | Dos LimeSDR y radio de potencia |
| CM5/CM5IO, auxiliar, tres drivers de rampas y alimentacion protegida | Audio Bluetooth/codec/micro/altavoz |
| GNSS, orientacion/calibracion, encoders y finales NC, parada/watchdog | Antena circular o redes RHCP/LHCP |
| Cables, fusibles, Powerpole y regulacion compatible | Transmision/APRS/SSTV |

Referencias propias: [CM5-ROTOR.md](CM5-ROTOR.md),
[POLARIZATION-MECHANICAL.md](POLARIZATION-MECHANICAL.md),
[MECHANICAL.md](MECHANICAL.md), [CM5-PCB.md](CM5-PCB.md).
Estas fuentes indican que esta implementado y que requiere banco;
no comprar componentes de una revision no congelada como si estuviera liberada.

## Componentes y costes del modulo

Consultar [REFERENCE-PRICES.md](REFERENCE-PRICES.md) y
[reference-prices.csv](../bom/reference-prices.csv): CM5, CM5IO, DRV x3,
ENC x3, COMPASS, IMU y GPS son referencias del rotor. MOTION, HARDWARE,
STRUCTURE, PCB-FAB/PCB-PCBA y POWER-RAILS/HARNESS siguen pendientes de
cotizacion/seleccion completa. Seleccionar solo los consumibles y piezas
compartidas realmente montados. No incluir SDR, PA, audio ni filtros RF
en la compra de rotor solo. Parada, watchdog y protecciones de movimiento
no se eliminan por carecer de radio.

## Montaje y configuracion independiente

1. Elegir revision de rotor y auxiliar compatibles. No usar portadora
   de dos TMC2209/ESP32 para una configuracion CM5 de tres ejes.
2. Montar estructura, rodamientos/ejes metalicos y transmisiones sin
   alimentacion, comprobando recorrido y equilibrio. POL es giro limitado.
3. Instalar encoders de salida y seis finales NC; comprobar extremos
   y servicio de coaxial para la antena que se utilizara.
4. Montar CM5/CM5IO y auxiliar segun mapa congelado de placa, drivers en
   modo de rampas y logica compatible; no generar STEP con un bucle Linux.
5. Instalar GNSS con vista al cielo y compas/IMU remoto de campos
   perturbadores. GPS estacionario no mide norte.
6. Cablear fuente externa, Powerpole/fusibles y regulacion; comprobar
   continuidad/polaridad con motores desconectados. No aplicar 12 V a CM5.
7. Configurar perfil rotor-only cuando este disponible en el instalador:
   no iniciar ni exigir dispositivos SDR. Verificar comandos reales
   publicados por [CM5-ROTOR.md](CM5-ROTOR.md), no servicios ficticios.
8. Probar parada/watchdog/cable abierto/reinicio antes de habilitar
   movimiento, con cargas seguras y puesta en servicio local explicita.
9. Hacer homing, nivel, norte verdadero y ceros EL/POL. Calibrar sensores,
   documentar declinacion y variacion con motores activados/desactivados.
10. Importar TLE, verificar UTC/sitio y predecir pase; ensayar seguimiento
    sin antena o con carga de prueba cualificada antes de instalarla.

## Independencia y seguridad

RF apagada o ausente no debe impedir control de movimiento cualificado.
Un sensor invalido no se sustituye por cero. Limites, fallo de seguimiento,
perdida de posicion y parada se prueban en banco.
La mano circular no se cambia mediante POL: el rotor solo no aporta
red RF RHCP/LHCP. Una app o SBC no sustituyen parada fisica.
