# Cajas y soporte de radio

Las tapas llevan el logo BricoHams en relieve (0.6 mm, cara exterior). Imprimir en ASA. Ver [MODULE-RADIO.md](../MODULE-RADIO.md).

![C1 ](fig/C1-cajas.svg)

*C1* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

## Componentes y compatibilidad

Consultar las [fichas visuales](components/README.md) y la
[BOM mecanica](../../bom/mechanical.csv): B07 es la cuna RT3S; B08 agrupa
carrier y diplexor. No sumar ademas las cajas LEGACY como un segundo juego.
La caja de carrier ESP32 de PCB 180 x 130 mm no define el alojamiento
de CM5/CM5IO. La antigua caja interior 124 x 64 mm no sirve para esa PCB.
Confirmar dimensiones, conectores, alturas y disipacion con unidades reales.

## Secuencia

1. Imprimir un cupon de inserto y asiento antes de la carcasa. Comprobar
   deformacion y fisuras; seguir temperatura y procedimiento del inserto.
2. Presentar componentes y tapas sin energia. Comprobar acceso a parada,
   fusibles y conexiones, ventilacion y separacion de partes conductoras.
3. Colocar insertos con herramienta adecuada, sin fundir paredes ni
   respirar humos. Practicar primero en el cupon; no recalentar la PCB.
4. Montar PCB sobre separadores compatibles con los taladros y la
   separacion electrica prevista. Ninguna soldadura debe tocar la bandeja.
5. Sujetar conectores de panel y cables con alivio de tension antes de
   cerrar. No usar un SMA como asa, ni perforar sin revisar la cara opuesta.
6. Montar blindaje metalico del diplexor con continuidad comprobada;
   ASA y pintura no sustituyen blindaje RF. Conservar accesos y refrigeracion.
7. Fijar radio/cajas a la bandeja estacionaria con retencion secundaria.
   La cuna RT3S es provisional: medir la radio y comprobar que no pulsa PTT.
8. Cerrar sin pinzar cables, comprobar acceso y registrar revision/masa.
   No afirmar estanqueidad ni uso bajo lluvia sin ensayo especifico.

## Marca y revision

Orientar el logo hacia el exterior sin lijar detalles ni debilitar paredes.
No mover el relieve a engranajes, apoyos o superficies de ajuste.
Los nombres BricoHams no deben tapar avisos del fabricante, polaridad ni
etiquetas de seguridad. Ver [BRANDING](../BRANDING.md).
Detener el montaje si la carcasa impide refrigeracion, retencion o parada.
