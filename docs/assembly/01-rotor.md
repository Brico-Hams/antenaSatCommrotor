# Montaje del rotor

Rotor BASE por correa: 2 etapas GT2 20T:100T = 25:1, correas de 252 mm, placas de aluminio de 3 mm, poleas compradas, rodamientos 608/6000, copas ASA. Motor NEMA14 provisional. Ver [MECHANICAL.md](../MECHANICAL.md) y [MODULE-ROTOR.md](../MODULE-ROTOR.md).

## Preparacion y componentes

Seleccionar una revision y anotar el motor real, carga y tornilleria. Usar
las filas Bxx de la [BOM mecanica](../../bom/mechanical.csv) y MMA-001 a
MMA-012 de la [BOM del conjunto](../../bom/multimode-assembly.csv).
Los Pxx planetarios son LEGACY: no mezclar sus ejes ni placas con BASE.
Cada fila tiene su [ficha visual](components/README.md).
Herramientas: calibre, escuadra, llaves y medio de retencion de la carga.
Pares de apriete y tension de correa quedan pendientes del fabricante
seleccionado y del ensayo; no usar un valor generico.

## 1. Piezas
![R1 ](fig/R1-rotor-piezas.svg)

*R1* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

## 2. Reductor
![R2 ](fig/R2-reductor-despiece.svg)

*R2* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

Tensar la correa con las ranuras de ±1.5 mm de la placa antes de apretar. Las poleas y correas son compradas: el modelo solo muestra su envolvente.

1. Comparar DXF, espesor de placa y taladros con los componentes recibidos.
   Desbarbar; detenerse si hace falta forzar un rodamiento o doblar una placa.
2. Ensayar primero un cupon ASA de asiento. Montar copas y rodamientos sin
   transmitir la fuerza de insercion a traves de las bolas.
3. Montar motor, eje intermedio y salida con retencion metalica.
   Alinear las dos parejas 20T:100T en sus respectivos planos.
4. Colocar ambas correas con el motor desconectado, ajustar las ranuras y
   comprobar a mano que no hay roce ni puntos duros. No tensar hasta deformar
   las copas; verificar la tension con el procedimiento de la correa elegida.
5. Marcar las fijaciones para detectar desplazamiento y registrar holgura,
   alineacion y revision. Repetir el procedimiento para el segundo eje.

## 3. Eje de azimut
![R3 ](fig/R3-azimut.svg)

*R3* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

Fijar base y bandeja al tripode mediante interfaz metalica comprobada y
retencion secundaria. Montar AZ y comprobar que la carga se transmite por
los apoyos previstos, no por el sensor ni por el cableado.
Instalar iman diametral y encoder de salida sin contacto; comprobar campo
y lectura siguiendo la ficha del sensor, no una distancia supuesta.

## 4. Rotor completo AZ + EL
![R4 ](fig/R4-rotor-completo.svg)

*R4* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

**Parada:** no energizar hasta comprobar giro libre a mano, topes y cableado ([04-electronica.md](04-electronica.md)).

Instalar soporte EL, segundo reductor y silla compatible con el boom real.
Comprobar equilibrio con masa de ensayo y retencion EL independiente:
la correa es reversible y el motor sin energia no sostiene la carga.
Montar finales NC separados de los topes; comprobar continuidad y
apertura por cable roto antes del primer movimiento descargado.

## 5. Eje de polarizacion (POL: tercer eje de la variante CM5)
![R5 ](fig/R5-polarizacion-despiece.svg)

*R5* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

![R6 ](fig/R6-polarizacion-montada.svg)

*R6* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

Concepto de tercer eje de roll: una etapa GT2 5:1, eje hueco y dos
rodamientos 608. Ver [POLARIZATION-MECHANICAL.md](../POLARIZATION-MECHANICAL.md)
y [BOM POL](../../bom/polarization.csv). La base ESP32 no implementa este
tercer eje por anadir la pieza.

1. Verificar el ajuste de bastidor, retenedores, tubo y soportes metalicos
   antes de montar motor/correa. Los DXF son plantillas provisionales.
2. Fijar carrier y leva sin que los tornillos penetren el paso del coaxial.
   Los conectores permanecen fuera del taladro del eje.
3. Comprobar el lazo de servicio a mano en toda la envolvente AZ/EL/POL.
   El radio minimo depende del coaxial elegido.
4. Tomar +/-80 grados como limite suave de diseno, NC objetivo +/-85 y
   topes candidatos +/-90; **no son recorridos fisicamente aprobados**.
   Ajustarlos tras medir tolerancias, frenado y paso de cables.

POL gira el boom; no conmuta RHCP/LHCP. La red RF tiene su propio
interbloqueo sin TX durante cambios.

## Salida y criterio de parada

Registrar masa, CG, holgura, retencion y recorrido en
[pruebas mecanicas](../testing/04-mecanica.md). Si hay roce, perdida de
lectura, aflojamiento, deformacion o cable tirante, no pasar a motor bajo
carga. Los 80000 microsteps/vuelta AZ/EL y 16000 POL no prueban precision.
