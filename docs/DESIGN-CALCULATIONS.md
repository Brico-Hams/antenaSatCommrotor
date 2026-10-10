# Calculos reproducibles y limites de su interpretacion

Entrada unica de estos ejemplos: [design.json](../calc/design.json).
Ejecutar [engineering-report.cjs](../scripts/engineering-report.cjs)
para recomputar, y las pruebas del proyecto para verificar las relaciones.
Estos calculos son independientes de los ensayos RF y de carga.

## Longitudes iniciales por banda

Modelo empirico de partida de la referencia de Tomas Brincil:

```text
lambda = c / f
L_dipolo_total = lambda / 2 * 0,92
L_reflector_total = 1,05 * L_dipolo_total
distancia_reflector = 0,225 * lambda
```

| Magnitud | 145 MHz | 435 MHz |
| --- | ---: | ---: |
| Longitud de onda, mm | 2067,534 | 689,178 |
| Dipolo TOTAL, mm | 951,066 | 317,022 |
| Cada brazo del dipolo, mm | 475,533 | 158,511 |
| Corte inicial por brazo (+10 mm), mm | 485,533 | 168,511 |
| Reflector TOTAL, mm | 998,619 | 332,873 |
| Separacion reflector, mm | 465,195 | 155,065 |

No confundir longitud total con cada brazo. Un dipolo cruzado tiene dos
dipolos ortogonales por banda; un reflector cruzado tambien tiene dos
elementos ortogonales. Diametro de conductor, gap de alimentacion,
empalmes, plasticos, boom y otras bandas afectan resonancia e impedancia.
Estos numeros no constituyen una Yagi optimizada ni demuestran circularidad.

La separacion VHF explica por que un boom rigido de 300 mm no basta
para esta geometria; el montaje original debe contemplar secciones
desmontables. El plegado conductor conserva continuidad por metal y
bloqueos mecanicos, no por el contacto casual de una bisagra.

### Cuarto de onda en coax: ejemplo, no hibrido completo

`L_coax = lambda / 4 * VF`

Con VF supuesto 0,66: 341,143 mm a 145 MHz y 113,714 mm a 435 MHz.
Medir VF real del cable. Dos latiguillos de 50 ohm de estas longitudes
no construyen automaticamente un divisor/hibrido adaptado de 50 ohm.
Se necesitan topologia, impedancias, terminacion, balance y medicion
descritos en el manual RF.

## Planetario

Para corona fija, sol entrada y carrier salida:

`i = 1 + N_corona / N_sol = 1 + 72/18 = 5`

Dos etapas en cascada: `i_total = 5*5 = 25`.

| Parametro | Valor |
| --- | ---: |
| Modulo | 1,5 mm |
| Angulo de presion | 20 grados |
| Sol / planeta / corona | 18 / 27 / 72 dientes |
| Diametros primitivos | 27 / 40,5 / 108 mm |
| Radio de orbita del planeta | 33,75 mm |
| Numero de planetas | 3 |
| Condicion de fase | (18+72)/3 = 30, entero |

`N_corona = N_sol + 2*N_planeta = 18+54 = 72`.
Separacion entre centros de planetas vecinos:
`2*33,75*sin(60 grados) = 58,46 mm`.
Diametro exterior aproximado de planeta con adendo de un modulo:
`1,5*(27+2) = 43,5 mm`. No hay interseccion entre planetas en esta
seccion ideal; esto no comprueba soportes, tornillos ni apilamiento axial.

Para diente involuta estandar no corregido a 20 grados:
`N_min ~= 2/sin(20 grados)^2 = 17,10`.
Un sol de 12 dientes exige correccion de perfil/otro criterio.
La base de 18 evita aceptar un engranaje pequeno sin analizar subcorte.

## Resolucion, no exactitud

```text
200 pasos/vuelta * 16 microsteps * 25 = 80000 comandos/vuelta
360 / 80000 = 0,0045 grados/comando
```

No se suma interpolacion interna de driver como resolucion de comando.
La precision final depende de sensores, rumbo, inclinacion, juego,
deformacion, excentricidad y par disponible. Se mide en la salida.

## Par de carga: ejemplo que NO cumple viento de 8 m/s

Suposiciones del ejemplo, no prestaciones de un motor comprado:

- Masa antena 0,5 kg y desequilibrio 0,03 m.
- Par motor 0,1 Nm y eficiencia 0,7 por etapa.
- Area proyectada 0,06 m2, Cd=1,2, densidad aire=1,225 kg/m3.
- Viento 8 m/s y brazo aerodinamico 0,25 m.
- Margen de seguridad requerido 2.

```text
T_gravedad = m*g*d = 0,14715 Nm
F_viento = 0,5*rho*Cd*A*v^2 = 2,8224 N
T_viento = F*brazo = 0,7056 Nm
T_requerido_con_margen = 2*(0,14715+0,7056) = 1,7055 Nm
T_salida_supuesto = 0,1*25*0,7^2 = 1,225 Nm
```

**El margen no se cumple. No operar a 8 m/s por este calculo.**
El par de retencion anunciado de un paso a paso no es su par en marcha.
Viento racheado, friccion, aceleracion e inclinacion requieren margen
adicional. Equilibrar ayuda a gravedad pero no elimina viento.

No resolver este fallo aumentando corriente fuera de especificacion ni
suponiendo que un engranaje impreso tolera todo el par reducido.
Medir, bajar carga/viento, modificar aerodinamica o cambiar arquitectura.

## Tripode

La rosca fotografica de 1/4-20 significa diametro nominal 6,35 mm y
paso 25,4/20 = 1,27 mm. La de 3/8-16 tiene diametro nominal 9,525 mm
y paso 1,5875 mm. Usar inserto/tuerca metalica, no hilo ASA de soporte.
Estas cotas no prueban rigidez torsional ni capacidad del tripode.
