# Ensayos y puertas de aceptacion

Registrar fecha, revision Git, instrumentos, operador, montaje y resultado.
Un criterio no medido queda PENDIENTE, no APROBADO por calculo.

## G0: software y geometria digital

1. Compilar firmware con las dependencias fijadas.
2. Ejecutar pruebas de orbital, limites, tiempo y datos erroneos.
3. Comparar SGP4 con implementacion independiente para mismo TLE/UTC/site:
   objetivo <=0,1 grados AZ/EL lejos del cenit, mismas convenciones/geodesia.
4. Comprobar unidades: altura GNSS en metros, biblioteca segun su API;
   latitud/longitud en grados, UTC sin correccion de hora local.
5. Renderizar TODAS las piezas con OpenSCAD; comprobar malla cerrada,
   volumen, auto-interseccion y ausencia de componentes inesperados.
6. Revisar engrane de ambas etapas, fase de planetas, rodamientos, eje,
   holguras, tornilleria y acceso de montaje; render no sustituye este paso.
7. TLE truncado, checksum malo, epoch viejo, nombres HTML, fuente caida
   y catalogo demasiado grande: fallo explicito, sin movimiento.

## G1: mecanica sin RF

1. Imprimir cupones: agujero, eje, inserto, diente y casquillo. Medir
   contraccion ASA y registrar compensacion, sin lijar hasta ocultar fallos.
2. Montar una etapa sin motor: giro completo suave, planetas libres,
   salida concentricamente soportada. Repetir dos etapas.
3. Confirmar fijacion del sol de segunda etapa al carrier de primera:
   un engranaje flotante no transmite par.
4. Verificar el corte fisico de motores por parada y limites NC.
5. Boot/reinicio/watchdog no debe producir giro ni restaurar homing.
6. Homing sin antena: switch desconectado, pegado y no alcanzado -> fallo
   con timeout, no movimiento ilimitado.
7. Medir backlash con indicador/protractor al invertir y registrar en grados.
8. Equilibrar carga objetivo 0,5 kg con CG <=30 mm; utilizar retencion
   secundaria y banco estable antes del tripode.
9. Ensayar precision <=2 grados RMS en recorrido lento sin viento y
   maxima desviacion <=5 grados. Separar error de rumbo y eje.
10. Mantener 30 minutos bajo carga: sin perdida de pasos, aflojamiento
    ni temperatura superior al limite de cada componente.
11. Validar limites AZ, EL y cables con margen de frenado calculado.
12. Pesar todo, incluidos cables y alimentacion: objetivo <=3 kg
    sin radio/tripode. Medir bulto; objetivo orientativo largo <=450 mm
    con radiadores desmontados. No medir solo la caja.

El presupuesto de par de calc/design.json muestra que el EJEMPLO de
8 m/s con 0,06 m2 y brazo de 0,25 m NO cumple margen 2 con 0,1 Nm
de motor supuesto. Por tanto 8 m/s NO es limite autorizado de viento.
Hasta medir par en marcha y carga real, operar solamente en banco
controlado sin viento. Revalidar cualquier antena alternativa.

## G1E: placa portadora y WebFlash, antes de alimentar motores

1. Fijar revision de esquema/PCB/Gerber, lista de modulos y pinout del
   firmware. Las 16 senales GPIO deben coincidir sin duplicados.
2. Ejecutar ERC, DRC, unconnected y paridad esquema/PCB con la herramienta
   documentada; no reemplazarlos por comprobar que existe un ZIP Gerber.
3. Revisar manualmente huellas, pin 1 y orientacion del DevKitC y drivers,
   corriente de trazas, terminales, fusibles, TVS y disipacion.
4. Placa sin modulos: medir continuidad de nets y ausencia de cortos,
   aplicar fuente limitada segun procedimiento electrico documentado.
5. Verificar 12 V, 5 V y 3,3 V en sus nodos; ningun GPIO recibe 5 V.
6. Medir ENABLE deshabilitado al arrancar. Comprobar corte fisico VMOT
   independiente de MCU, con logica alimentada para indicar fallo.
7. Comprobar NC abierto y cable roto en todos los sensores. Verificar
   pull-ups externos en GPIO de entrada que no disponen de internos.
8. Flashear solamente el ESP32 compatible, sin motores ni radio conectados.
   Verificar hash y offsets de aplicacion, particiones y LittleFS.
9. Imagen publica sin secretos: aprovisionar por USB, confirmar que no
   imprime contrasenas/token y permanece sin homing tras SETUP/reinicio.
10. NVS sin cifrar: proteger acceso fisico; no copiar su contenido a Git.
    La actualizacion de LittleFS puede reemplazar TLE/cache: documentar
    copia previa y no confundir preservar NVS con preservar filesystem.
11. GitHub Actions/Pages requiere prueba remota separada; un manifiesto
    local aprobado no demuestra permiso o despliegue remoto correcto.
12. Comprobar branding integrado a tapa, sin solapamiento con conectores,
    tornillos y ventilacion ni piezas sueltas.

## G2: RF pasiva

1. Calibrar VNA en plano de referencia de conector, sin radio conectada.
2. Medir cada dipolo/reflektor por banda y sus redes de adaptacion.
3. Conjunto desplegado, coax y rotor en posiciones reales:
   objetivo ROE <=1,5 en frecuencia central elegida y <=2 en canales
   de operacion. Documentar ancho de banda, no extrapolar.
4. Medir hibrido por banda: objetivo desequilibrio <=0,5 dB y
   fase 90 +/-5 grados en frecuencias elegidas; carga aislada adecuada.
5. Medir diplexor: objetivo perdida de insercion <=1 dB por rama,
   retorno >=14 dB y aislamiento >=40 dB como cribado inicial.
   Para un receptor simultaneo adicional, calcular aislamiento requerido
   por potencia TX y maximo nivel admisible del receptor, incluyendo margen;
   40 dB no garantiza ausencia de desensibilizacion.
6. Patron, sentido RHCP/LHCP y relacion axial: no inferirlos de un hibrido
   comercial ni de una ROE buena; medir/simular el conjunto. Objetivo
   inicial relacion axial <=3 dB hacia el satelite para anunciar circular.
7. Revisar continuidad y repetibilidad despues de 50 plegados. Las bisagras
   plasticas no pueden ser el unico contacto RF.

## G3: recepcion y control

1. Comparar un pase con referencia independiente, misma estacion y TLE.
2. AP sin Internet: importar TLE, seleccionar, predecir y seguir.
3. Cerrar movil durante pase: calculo y seguimiento siguen en ESP32.
4. Perdida de GNSS, UTC invalida, cache antigua, encoder perdido:
   verificar politica documentada, aviso y parada segura.
5. Pase bajo horizonte/no comenzado, cable wrap, cenit y velocidad
   inalcanzable: rechazar explicitamente, no apuntar al objetivo incorrecto.
6. Comparar ruido RX con convertidores y motores encendidos/apagados.
7. Confirmar orientacion verdadera con referencia conocida; repetir al
   mover tripode, no reutilizar calibracion en una ubicacion nueva.

## G4: transmision autorizada

Solo con licencia/autorizacion, frecuencias y satelite verificados.
Comenzar con potencia minima y carga adecuada para ensayos en banco,
revisar temperatura de redes y conectores. No transmitir con red
sin adaptacion o fuera del rango verificado del diplexor/hibrido.

Una RT3S no escucha la bajada mientras transmite si opera half-duplex.
Para monitorizar bajada propia usar segundo receptor y calcular proteccion
contra TX. No anunciar full-duplex mediante un filtro pasivo.

## Ficha de resultados

| Ensayo | Revision/instrumentos | Resultado medido | Estado | Accion |
| --- | --- | --- | --- | --- |
| G0 | Por completar | Ver VALIDATION | Parcial | Segun registro |
| G1 | Prototipo no montado | No medido | Pendiente | Imprimir y ensayar |
| G2 | VNA requerido | No medido | Pendiente | Adaptar y medir RF |
| G3 | Banco de seguimiento | No medido | Pendiente | Verificar autonomia |
| G4 | Radio/licencia | No medido | Pendiente | Solo tras G1-G3 |
