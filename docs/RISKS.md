# Riesgos tecnicos y mitigacion

| Riesgo | Causa | Mitigacion | Evidencia necesaria |
| --- | --- | --- | --- |
| Viento supera par | Area/brazo dominan, NEMA14 pequeno | Limitar operacion, equilibrar, parar | Par en marcha y prueba de carga |
| Deslizamiento de tripode | Capacidad de camara no es torque AZ | Metal, fijacion secundaria, ensayo | Torsion sin aflojamiento |
| Holgura planetaria | Juego, impresion, portaplanetas flexible | Tolerancias y feedback | Backlash medido en salida |
| Subcorte en sol | Numero dientes insuficiente | Base 18 dientes modulo1,5 | Perfil y contacto inspeccionados |
| Engrane imposible | Fase/clearance/soportes incorrectos | Montaje de una etapa primero | Giro completo manual |
| Perdida de referencia | Reinicio, switch, cable roto | Desarmar y rehome | Fault injection |
| Rumbo incorrecto | Magnetos/motores, declinacion | Norte verdadero verificado | Error de orientacion medido |
| UTC/posicion erroneas | GNSS sin fix, reloj viejo | Estados de validez y bloqueo | Test sin GNSS y reinicio |
| TLE viejo | Cache o proveedor viejo | Epoch por satelite, bloqueo | Tests de antiguedad |
| Acoplamiento V/U | Radiadores y reflector comunes | Simulacion y VNA ensamblado | ROE/patron final |
| Hibrido fuera de banda | SATCOM no es145/435 | Ficha fabricante y medicion | S-parametros por banda |
| Diplexor incompatible | Nombrado por proyecto, no por medicion | Revision exacta y ensayo | Cotas, potencia, aislamiento |
| Contacto plegable RF malo | Bisagra plastica, oxidacion | Empalme metalico positivo | 50 ciclos y VNA repetido |
| EMI del rotor | Driver/DC-DC y coax proximos | Subcaja metalica y filtrado | RX motor on/off |
| Full-duplex supuesto | Un solo RT3S half-duplex | Operacion explicita o receptor aparte | Prueba real de radio |
| Cenit / cable wrap | Velocidad singular y limites | Excluir pases no alcanzables | Simulacion y banco |
| Calentamiento / ASA | Caja al sol y corriente drivers | Corriente correcta y ventilacion | Temperatura medida |
| Masa sobre objetivo | Bateria, acero y coax olvidados | Pesar conjunto real | Pesaje documentado |
| Derechos de terceros | URL publica no es licencia | Original, citar sin copiar STL | Registro de procedencia |

Los riesgos mecanicos y RF no se cierran con pruebas de software.
Un estado 'pendiente' es intencional y debe mantenerse visible.
