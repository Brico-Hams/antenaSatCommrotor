# Montaje general: union de modulos independientes

## Elegir solo lo necesario

| Objetivo | Punto de entrada |
| --- | --- |
| Antena sola para radio externa/manual | [MODULE-ANTENNA.md](MODULE-ANTENNA.md) |
| Rotor solo para antena compatible del usuario | [MODULE-ROTOR.md](MODULE-ROTOR.md) |
| Radio SDR sola con antenas/cargas externas | [MODULE-RADIO.md](MODULE-RADIO.md) |
| Estacion completa | Este documento y [ASSEMBLY-MULTIMODE.md](ASSEMBLY-MULTIMODE.md) |

En el conjunto integrado CM5 es compartido por radio/rotor: no sumar dos
CM5, dos CM5IO ni dos sistemas de energia al agregar BOM independientes.
Eliminar un modulo no autoriza puentear sus interbloqueos dependientes.

## Secuencia de integracion

1. Terminar y aceptar mecanica/RF de la antena, movimiento/sensores del
   rotor y recepcion/audio de la radio por separado.
2. Montar tripode y base fija. CM5, radio, disipadores y bateria externa
   no giran con la antena. Confirmar estabilidad y CG.
3. Acoplar antena al rotor mediante interfaz desmontable; verificar carga
   de tres ejes, recorrido, coaxiales y alivio de tension.
4. Interconectar RF SMA por banda, red circular si esta cualificada y
   seleccion de mano separada del giro POL. Mantener TX inhibido.
5. Instalar distribucion Powerpole/fusibles, conversores y filtrado EMI
   conforme esquema congelado; verificar caidas/temperatura/transitorios.
6. Seleccionar perfil integrated en software cuando este implementado,
   identidades SDR y credenciales locales. No autoarmar al arrancar.
7. Calibrar UTC/sitio, nivel/norte y ceros AZ/EL/POL; verificar fallos de
   sensores, limites, reloj, Bluetooth, proceso y parada/watchdog.
8. Validar pases/mapa/radar y Doppler con datos orbitales reales; probar
   audio, SSTV/APRS y errores visibles antes de realizar TX.
9. Cualificar TX/full-duplex con instrumentos/carga: ambos sentidos
   VHF/UHF, armonicos (145 x 3 = 435 MHz), bloqueo y calentamiento.
10. Pesar conjunto operativo incluido tripode/cables, excluyendo solo
    bateria externa por eleccion vigente; registrar esta masa aparte.
    Verificar <=5 kg y autonomia objetivo 2 horas mediante ensayo.

## Ilustraciones, componentes y problemas

El [manual ilustrado](ASSEMBLY-MULTIMODE.md) relaciona figuras, IDs de
componentes, material externo y pasos. Los dibujos conceptuales no son
plantillas de mecanizado ni pinouts de fabricacion.
[TROUBLESHOOTING-MULTIMODE.md](TROUBLESHOOTING-MULTIMODE.md) recoge
problemas calculados, comprobaciones y puertas de parada.
Las listas de precios se cierran por referencias/fechas y distinguen
herramientas reutilizables, consumibles, piezas compartidas y pendientes.
Las observaciones actuales estan en [REFERENCE-PRICES.md](REFERENCE-PRICES.md)
y [reference-prices.csv](../bom/reference-prices.csv). No sumar el subtotal
electronico y el subtotal electronico mas ASA: son alternativas.
La bateria externa se presupuesta aunque se excluya de los 5 kg; el
cargador no esta incluido en su referencia. No declarar coste completo
mientras existan categorias pendientes o cantidades sin aprobar.

Este indice no acredita que la integracion fisica haya sido ensayada.
Prevalecen [VALIDATION.md](VALIDATION.md), [ACCEPTANCE.md](ACCEPTANCE.md)
y la revision concreta de PCB/Gerbers/BOM/CPL.
