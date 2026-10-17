# Montaje de la antena

Para escoger otra geometria ver la [comparativa TX/RX](../ANTENNA-OPTIONS.md),
[Eggbeater](../ANTENNA-EGGBEATER.md) o [QFH](../ANTENNA-QFH.md), con
[previo RX y bypass TX](../ANTENNA-PREAMPS.md). No mezclar sus piezas
con el montaje historico siguiente; 25 W es requisito, no rating aprobado.

**Nueva candidata portable:** seguir [PF-01](../ANTENNA-PORTABLE.md)
para el rediseno de boom unico y cassettes plegables. Los pasos y vistas
A1/A2 de abajo corresponden a la antena anterior y se conservan para
trazabilidad; no usar sus piezas o longitudes como lista PF-01.

Antena V/U sobre mastil. Ver [MODULE-ANTENNA.md](../MODULE-ANTENNA.md).

## Antes de empezar

Separar piezas ASA, booms, conductores, manguitos, puentes RF, tornilleria
y coaxiales. Identificar P28-P30 y M18-M23 de la
[BOM mecanica](../../bom/mechanical.csv), las referencias aplicables de la
[BOM RF](../../bom/rf.csv) y sus [fichas visuales](components/README.md).
No comprar referencias excluidas ni sumar SMA y BNC como si fueran dos
interfaces obligatorias. La ampliacion CM5 utiliza SMA convencional 50 ohm.

## 1. Piezas impresas
![A1 ](fig/A1-antena-piezas.svg)

*A1* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

1. Verificar el diametro real del boom y el ajuste de las piezas impresas.
   No escalar toda la pieza para corregir un unico alojamiento.
2. Presentar cubos, bisagras y bloqueo en seco. Comprobar que ningun
   elemento puede soltarse o plegarse involuntariamente.
3. Preparar conductores con margen de ajuste segun
   [MECHANICAL](../MECHANICAL.md) y [RF-AND-RADIO](../RF-AND-RADIO.md).
   Las longitudes calculadas no son una tabla de cortes final validada.
4. Montar empalmes y puentes conductores repetibles en las articulaciones.
   Una bisagra mecanica no garantiza continuidad RF.

## 2. Montaje
![A2 ](fig/A2-antena-montada.svg)

*A2* — BricoHams · Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina

5. Montar las dos bandas y su alimentacion, etiquetar VHF/UHF y los puertos
   ortogonales si los hay. Respetar genero y contacto central SMA, sin RP-SMA.
6. Sujetar coaxiales al boom con alivio de tension y lazos de servicio:
   no sujetar el peso de la antena por un conector.
7. Comprobar plegado, bloqueo, masa y centro de gravedad en soporte manual
   antes de acoplar al rotor. No plegar con el sistema energizado.
8. Calibrar el VNA en el plano de medida; medir cada banda y luego el
   conjunto con puertos libres terminados. Guardar Touchstone, configuracion
   y frecuencias. Ajustar gradualmente, no recortar ambas bandas a ciegas.
9. Si se monta circular, cualificar por banda hibrido, fase, amplitud, mano
   y terminaciones. Ni el giro POL ni una ROE baja demuestran polarizacion.

## Aceptacion

Aplicar [ensayos RF](../testing/05-rf-y-radio.md) y
[ACCEPTANCE](../ACCEPTANCE.md). Medir ROE por banda antes de conectar al
sistema; no transmitir sin carga o antena verificada. Si cambian coaxial,
diametro, aislantes o geometria, repetir el ajuste. Antena sola no requiere
instalar CM5, app ni firmware de rotor.
