# Alimentacion, cableado y separacion electrica

Este documento define la arquitectura electrica, no una PCB fabricada
ni una declaracion de compatibilidad de todos los modulos disponibles.
El usuario ha solicitado ademas una PCB portadora de modulos reemplazables
con esquema, Gerber y conexiones de sensores/proteccion. Su desarrollo
se registra separadamente; no se presume que todos los modulos DevKit
o StepStick tengan la misma huella. Ver ADR-020.
La asignacion final GPIO y las conexiones del controlador se encuentran
en CONTROL.md y en su firmware.

## Arbol de alimentacion

```text
fuente comercial protegida 12 V nominal, rango verificado con drivers
  |
  +-- fusible dimensionado por cable/consumo -- interruptor general
        |
        +-- corte fisico de potencia motores por parada accesible
        |     +-- driver AZ -- motor AZ
        |     +-- driver EL -- motor EL
        |
        +-- DC/DC 5 V -- placa ESP32
                    +-- regulacion 3,3 V para sensores compatibles

RT3S: bateria propia, independiente
RF: pasiva en caja metalica, sin PTT automatico
```

Usar fuente/bateria comercial con protecciones verificadas y su cargador
adecuado. No fabricar un pack de litio improvisado. La parada debe inhibir
movimiento incluso si el firmware o el navegador se bloquean. El NC
monitorizado por software es complementario al corte hardware; no es
un relé de seguridad certificado.

## Drivers y corriente

Un TMC2209 o equivalente limita corriente de fase; el ajuste se calcula
segun su placa, resistencia de sensado y corriente RMS nominal del motor,
no por copiar el valor de otra NEMA14. Confirmar modo 16 microsteps real:
80000 pasos/vuelta presupone 200 pasos/vuelta del motor, 16 microsteps
y 25:1, no los 256 pasos internos interpolados.

Colocar desacoplo cerca de VMOT segun fabricante, proteger polaridad,
aportar ventilacion y verificar temperaturas en caja cerrada al sol.
No conectar/desconectar motor con driver alimentado. Revisar masa comun
logica/driver y separacion entre potencia, coax y GNSS.

## Sensores y cableado

- ESP32 no tolera entradas de 5 V salvo adaptacion documentada.
- AS5600 comparte direccion I2C: separar buses o usar multiplexor;
  dos sensores en el mismo bus sin direccion distinta no sirven.
- La orientacion mecanica del magneto, su distancia y el eje importan.
  Verificar campo fuera de rango y giro antes de confiar en feedback.
- GNSS serie debe tener niveles logicos compatibles; una antena GNSS
  necesita cielo visible y no referencia de azimut por estar quieta.
- Cablear NC para que un cable cortado genere fallo. Confirmar polaridad
  electrica y logica con motores desconectados.
- Los limites de recorrido necesitan ubicacion fisica y margen de frenado:
  no basta con dibujarlos o limitar variables.

## RF All-in-One, pero modular

Separar caja metalica del diplexor y redes RF de drivers y convertidores.
ASA es envolvente mecanica, no blindaje. Conectores con fijacion y alivio
de tension; evitar cargar el SMA de la RT3S con el peso del coax.
La pieza de radio debe dejar accesibles PTT, volumen, pantalla, bateria
y conexion de antena. No especificar un adaptador SMA hasta comprobar
su genero y rosca en la unidad real.

Comparar ruido recibido con motores/DC/DC encendidos y apagados;
si aumenta, corregir filtrado, ubicacion, blindaje y retornos antes de TX.
Las conexiones de RF y el diplexor no se mezclan con una supuesta
interfaz USB de control de radio.

## Autonomia energetica: metodo, no cifra prometida

Medir potencia de seguimiento, reposo, homing y Wi-Fi. La energia util
es la medida en salida de la fuente, no capacidad de celda multiplicada
por 12 V si el fabricante declara mAh a otra tension.

`horas = Wh_utiles / W_medios`

Ejemplo solo aritmetico: 30 Wh utiles y 8 W medios -> 3,75 h.
No constituye estimacion de esta estacion sin medir la corriente.
Registrar margen para frio, envejecimiento y reduccion del convertidor.
