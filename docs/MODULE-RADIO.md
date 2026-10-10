# Modulo independiente: radio SDR CM5

## Alcance y dependencias

Radio construible sin rotor ni antena especifica del proyecto, con antenas
externas o cargas de prueba compatibles. Usa CM5/CM5IO, dos LimeSDR Mini,
audio y alimentacion protegida. Las potencias objetivo requieren PA/filtros
adicionales; no son potencia de salida del SDR desnudo.

| Necesario | Opcional o dependiente de modo |
| --- | --- |
| CM5/CM5IO, dos SDR identificados por serie, USB/cooling y energia | Rotor mecanico y sus tres drivers |
| Caminos RF SMA 50 ohm, proteccion y filtrado de receptores | Antena portable del proyecto |
| Audio/PCM Bluetooth y micro/altavoz si se usan | GNSS/SGP4/rotor para Doppler automatico |
| Permiso fisico TX, watchdog, fusibles y camino RF cualificado para TX | Redes circular RHCP/LHCP |
| PA lineales/filtros/carga adecuada para objetivo 5 W | K1 externo en lugar de audio integrado |

[RADIO-HOST.md](RADIO-HOST.md) documenta interfaces y pruebas;
[CM5-RF-SELECTION.md](CM5-RF-SELECTION.md) registra evidencia de
componentes. [ANDROID-DIGITAL.md](ANDROID-DIGITAL.md) distingue DSP,
audio generado, transmision y ACK remoto. No confundirlos.

## Componentes y costes del modulo

[REFERENCE-PRICES.md](REFERENCE-PRICES.md) y
[reference-prices.csv](../bom/reference-prices.csv) conservan precios y
pendientes. Seleccionar CM5/CM5IO, SDR x2 y las categorias RF, AUDIO,
USB-DATA, COOLING y energia necesarias. Los sensores de movimiento,
motores y mecanica del rotor no son compras obligatorias de radio sola.
El permiso fisico TX y su watchdog siguen siendo obligatorios para TX:
no retirar la proteccion por retirar los motores. La BOM de RF anterior
no contiene automaticamente PA lineales multimodo cualificados ni el
presupuesto completo de la ampliacion.

## Montaje y configuracion independiente

1. Seleccionar revisiones CM5/CM5IO/Lime; anotar dos numeros de serie
   inequívocos y asignacion VHF/UHF. No seleccionar el primer USB hallado.
2. Montar componentes en base fija ventilada con fijaciones y blindaje
   apropiados; puertos USB3 ocupados requieren definir conexion de audio.
3. Preparar distribucion externa Powerpole/fusibles, regulacion CM5 y
   ramas RF. Medir tension/polaridad antes de conectar ordenadores/SDR.
4. Preparar SMA/cables/terminaciones, preseleccion y proteccion RX.
   Sin PA/camino RF verificado, permanecer en recepcion.
5. Instalar perfil radio-only y dependencias publicadas del host.
   Configurar en local identidades USB y credenciales privadas.
6. Verificar descubrimiento, tasas/frecuencias leidas del hardware y
   dos streams RX concurrentes. Una tasa solicitada no es tasa comprobada.
7. Seleccionar explicitamente canal de audio VHF/UHF y probar Bluetooth
   PCM/creditos/perdidas; no mezclar tonos SSTV/APRS de dos receptores.
8. Configurar frecuencia/modo manuales autorizados. Modo independiente
   no puede fingir posicion orbital ni activar Doppler sin datos validos.
9. Probar DSP con WAV/vectores y luego recepcion real. Configurar audio
   micro/altavoz/K1 solo tras pinout, bias y nivel verificados.
10. Para TX: cualificar PA/filtros, carga, espectro, temperatura y permiso
    fisico/watchdog/lease. Iniciar a minima potencia; un solo TX activo.

## Separacion de modos

Recepcion/manual no debe depender del rotor. Doppler automatico requiere
fuente orbital/UTC/sitio real, fresca y verificada; perdida de esa fuente
no debe cambiar silenciosamente a transmision manual.
El soporte standalone real se verifica contra codigo/pruebas del host,
no se considera terminado por este documento.
Objetivos 5 W FM, 5 W PEP USB y 1 W AM siguen sujetos a medicion.
