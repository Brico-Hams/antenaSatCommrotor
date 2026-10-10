# Manual de transporte y operacion de campo

## Modulos transportados

- Antena: boom, radiadores y reflectores desmontables, redes RF y coax.
- Rotor: AZ/EL y saddle sin radio ni antena.
- Control: ESP32, GNSS, alimentacion, parada y modulo RF extraible.
- Radio RT3S con bateria propia y soporte desmontable.
- Tripode fotografico y adaptador metalico.

No usar los cables como asas. Proteger roscas y contactos de los empalmes
RF. El bulto objetivo <=450 mm requiere desmontar las secciones largas:
un brazo VHF de 475,5 mm no cabe plegandolo de manera magica sin dividirlo.

## Montaje

Con alimentacion desconectada, abrir el tripode sobre suelo estable,
verificar fijacion metalica y retencion secundaria. No asumir que
la capacidad vertical indicada para una camara autoriza torque lateral.
Colocar rotor, conectar limites, motores y sensores; usar alivio de tension.

Desplegar antena con bloqueos positivos y contactos metalicos; equilibrar
EL con su coax final. No colgar RT3S ni caja de bateria de la punta del boom.
Mantener personas fuera de la envolvente de giro.

## Posicion, UTC, nivel y norte

Un fix GNSS indica posicion, no orientacion de un tripode estacionario.
Nivelar la base y determinar norte verdadero mediante referencia conocida.
Si se usa brujula, compensar declinacion con fuente vigente y alejarla
de motor/ejes/iman; confirmar la desviacion despues de montar todo.

No introducir hora local como UTC. Registrar altura y unidades;
en montana la elevacion del observador y obstaculos del horizonte
son aspectos distintos. Homing solo calibra el eje mecanico.

## TLE en montana

Actualizar antes de salir; conservar cache y copia manual. En el lugar:

- AP permite navegador local pero no aporta Internet.
- Con STA/hotspot disponible, descargar desde proveedor permitido.
- Sin Internet, importar TLE con epoch reciente y confirmar satelite.
- Revisar antiguedad real del epoch, no solamente hora de descarga.

No tratar los TLE como lista de frecuencias. Confirmar transponder activo,
modo y frecuencias en fuentes actuales del operador del satelite.

## Durante el pase

Confirmar radio en el satelite correcto, UTC/site consistentes y
seguimiento armado. Verificar que el pase es alcanzable con limites
AZ/EL, velocidad y exclusion de cenit del controlador.

OpenGD77 puede gestionar su propia operacion satelital segun modelo/version;
seguir el manual de la version instalada. No se promete enlace CAT.
Una RT3S half-duplex no permite oir bajada simultaneamente durante TX.

La web no es una parada de emergencia fisica: mantener la parada
hardware accesible. Si hay viento, movimiento erratico, ruido RX nuevo
o conector flojo, parar y diagnosticar; no forzar un seguimiento.

## Desmontaje

Parar, verificar motores inmoviles, desconectar alimentacion, descargar
carga EL y desmontar antena. Retirar radio/modulo RF para usos independientes.
No plegar dipolos ni desacoplar planetarios con motores habilitados.
Guardar elementos secos; no inferir impermeabilidad de una caja ASA.

## Uso independiente

La antena puede utilizarse con montaje manual y su red RF sin rotor.
El rotor puede usar otra antena dentro de la envolvente de carga verificada.
El diplexor puede conectarse externamente sin caja de control.
La RT3S sigue funcionando con bateria propia fuera del soporte.
