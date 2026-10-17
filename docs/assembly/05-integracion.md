# Montaje colectivo

Solo tras aceptar cada modulo por separado. No sumar dos CM5 ni dos sistemas de energia.

## Prerrequisitos

Reunir registros de [rotor](01-rotor.md), [antena](02-antena.md),
[cajas](03-cajas.md) y [electronica](04-electronica.md).
Elegir ESP32 con RT3S independiente o CM5 multimodo; no mezclar firmware,
pinouts ni resultados de aceptacion de generaciones distintas.
La variante CM5 integrada continua bloqueada para operacion real.

## 1. Secuencia
![I2 ](fig/I2-integracion.svg)

*I2* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

| Paso | Accion sin saltarse los bloqueos | Comprobacion antes de avanzar |
| --- | --- | --- |
| 1 | Desplegar y nivelar tripode, fijar bandeja y retencion | Carga, CG y fijaciones revisados; EL retenido sin motor |
| 2 | Instalar AZ/EL y, en CM5, concepto POL | Giro manual, topes, NC y recorridos sin colision |
| 3 | Acoplar antena equilibrada y asegurar boom | Ninguna carga estructural sobre coaxial o sensor |
| 4 | Fijar cajas, CM5/SDR o RT3S en base estacionaria | Ventilacion, parada y fusibles accesibles |
| 5 | Tender RF, energia y sensores con bucles de servicio | Separacion, alivio de tension y recorrido completo a mano |
| 6 | Revisar ramas protegidas con energia desconectada | Polaridad, niveles y ausencia de cortos; esquema liberado |
| 7 | Preparar software de la variante elegida | [Guia de instalacion](06-instalacion.md); sin autoarmado |
| 8 | Probar primero logica y movimiento descargado | Fallos de sensor/parada/watchdog inhiben movimiento/TX |
| 9 | Configurar UTC, sitio, norte, nivel y ceros | Datos reales y frescos; ACK no prueba posicion alcanzada |
| 10 | Ensayar solo RX; cualificar TX en banco aparte | RF aprobada, carga 50 ohm, instrumentos e interbloqueos |

## 2. Estacion montada
![I1 ](fig/I1-estacion-completa.svg)

*I1* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

La electronica, la radio y la bateria quedan en la base fija y no giran con la antena. Detalle en [MODULE-INTEGRATED.md](../MODULE-INTEGRATED.md).

La figura I1 ilustra disposicion mecanica: no acredita encaje o masa de
CM5IO, ambos SDR, amplificadores y refrigeracion. No taladrar desde su
perspectiva ni interpretar lineas conceptuales como cables liberados.

## Cierre y desmontaje

1. Aplicar [08-sistema](../testing/08-sistema.md): perdida de enlace,
   proceso, reloj, sensor, energia y reinicio deben acabar en estado seguro.
2. Medir conjunto listo para operar con tripode, cables y retenciones:
   limite <=5 kg excluyendo solo bateria externa, que se pesa aparte.
   El objetivo de dos horas exige ensayo de mision, no aritmetica nominal.
3. Documentar revision, instrumentos y resultados. No marcar PENDIENTE
   como aprobado por haber seguido los pasos.
4. Para desmontar: inhibir TX, parar, retener EL, apagar y aislar bateria;
   desconectar sin carga, proteger conectores y plegar sin movimiento.

Si una puerta no esta cerrada, quedarse en la etapa de revision/banco.
No ejecutar homing ni activar un servicio real solo para completar la guia.
