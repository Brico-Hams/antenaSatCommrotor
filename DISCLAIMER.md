# Aviso de responsabilidad y uso educativo

PortableSatStation es un **prototipo experimental de ingenieria**.
No es un producto certificado, un juguete, un dispositivo de seguridad,
un equipo para comunicaciones de emergencia ni un terminal SATCOM comercial.
Se entrega sin garantia, conforme a las licencias aplicables, en la
medida permitida por la ley. Este aviso no excluye derechos ni
responsabilidades que legalmente no puedan excluirse.

## Estado de validacion

Los calculos, pruebas de software, compilacion y comprobaciones de malla
no demuestran seguridad electrica/mecanica, capacidad de carga,
impermeabilidad, resistencia al viento, ROE, ganancia, aislamiento RF
ni precision real de seguimiento. Consultar [VALIDATION.md](docs/VALIDATION.md)
y superar las puertas de [ACCEPTANCE.md](docs/ACCEPTANCE.md).

Un Gerber generado no equivale a una placa revisada o ensayada.
No enviar a fabricacion sin comprobar huellas, conexiones, reglas de
diseno, corriente, disipacion, protecciones y revision del conjunto.
Flashear firmware tampoco valida el hardware al que se conecta.

## Radio y normativa

Transmitir solo con autorizaciones/licencia, bandas, potencia y condiciones
legales aplicables y respetando instrucciones del operador del satelite.
La referencia a equipos comerciales o militares no autoriza su uso ni
acceso a sus sistemas. No transmitir con redes RF sin medir.
Una RT3S half-duplex no se convierte en full-duplex con un diplexor.

## Movimiento, energia y fabricacion

Desconectar alimentacion antes de montar, plegar, cambiar cables o drivers.
Mantener parada fisica independiente del navegador/firmware y personas
fuera del recorrido. No utilizar motores para sostener una carga insegura
tras perder energia. Validar tripode, retenciones, equilibrio y limites.

Utilizar fuentes/baterias comerciales protegidas y cargadores adecuados.
No improvisar packs ni puentear fusibles o protecciones. No conectar
motores/RF durante el primer arranque o flasheo.
La impresion ASA, mecanizado y soldadura requieren equipos, ventilacion
y proteccion adecuados segun sus fabricantes.

## Ninos y adolescentes

El uso educativo vinculado a [Bricohams](https://bricohams.org) debe realizarse
con supervision adulta competente. Priorizar simulaciones y recepcion.
Los menores no deben acceder sin supervision a partes moviles, herramientas,
soldadura, baterias, circuitos energizados ni transmisores.
No publicar ubicaciones personales, credenciales o datos identificativos
de menores en el repositorio, la web de flasheo o registros compartidos.

## Terceros, marcas y datos

Las marcas y autores citados conservan sus derechos. No existe aval,
patrocinio o colaboracion implicita con los autores originales.
TLE y servicios externos pueden fallar o estar desactualizados.
Comprobar epoch y validez; no utilizarlos para decisiones criticas.

Los autores actuales son **Anatol EA5KAO, Diego EA5JEF y Pedro Roca Molina**.
Los trabajos anteriores y las dependencias se atribuyen por separado.
