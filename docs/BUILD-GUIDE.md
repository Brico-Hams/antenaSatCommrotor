# Orden de construccion y adquisicion

Acceso visual: [componentes por BOM](assembly/components/README.md),
[montaje por modulos](assembly/README.md),
[instalacion de software y conjunto](assembly/06-instalacion.md).
La variante BASE vigente usa correa; el planetario solo es LEGACY.

## Antes de comprar o imprimir

1. Leer ARCHITECTURE, MECHANICAL, CONTROL y RF-AND-RADIO.
2. Elegir motor exacto; anotar masa, eje, longitud, corriente y curva de par.
3. Medir radio, tripode, diplexor y antena alternativa. Actualizar parametros
   CAD antes de imprimir soportes. La compatibilidad nominal no prueba encaje.
4. Obtener cotizaciones de las tres listas BOM. Los importes orientativos
   nunca son un compromiso de precio ni disponibilidad.
5. Definir frecuencias de operacion y simular/medir la arquitectura RF.
   No comprar hibridos por potencia anunciada sin revisar su banda.
6. Verificar herramientas: OpenSCAD para CAD, entorno PlatformIO del control,
   Node.js para calculos. En esta entrega los programas portables de
   validacion se han alojado fuera del repositorio; no son dependencias de campo.

## Fabricacion progresiva

### Iteracion A: engrane y montaje

Imprimir cupones de los asientos BASE y presentar una transmision por
correa con poleas compradas. Ensamblar y girar manualmente.
Confirmar alineacion, holgura, excentricidad y cadena de par.
No imprimir todo el conjunto antes de ajustar la primera etapa.
Solo si se elige conscientemente LEGACY, ensayar la etapa planetaria y
mantener sus parametros y BOM separados.

### Iteracion B: banco del controlador

Montar ESP32, GNSS, sensores, limites y parada con motores descargados.
Este paso corresponde solo a ESP32. Para CM5 seguir el perfil y los
bloqueos de [instalacion](assembly/06-instalacion.md); no trasladar el
pinout ESP32 a la auxiliar CM5.
Compilar/cargar la revision exacta y probar todos los errores.
El dispositivo debe permanecer desarmado al arrancar; verificar tambien
que drivers y cableado no habilitan motores por un GPIO flotante.

### Iteracion C: segundo eje y soporte

Montar ambas reducciones, ejes metalicos y fijacion al tripode.
Colocar masa de ensayo equilibrada, no antena larga sin validar.
Medir precision/backlash, corriente y temperaturas. Aplicar G1.

### Iteracion D: antena y diplexor

Cortar metal con margen de ajuste. Los valores publicados son
dimensiones iniciales; el aislante, coax, diametro, herrajes y otras
bandas alteran la longitud electrica. Ajustar con VNA en montaje final.
El reflector tambien necesita empalmes conductores fiables.
Integrar diplexor previo solo tras verificar revision, cotas y S-parametros.

### Iteracion E: campo

Realizar primero recepcion y comparar seguimiento independiente.
Solo tras G1-G3 realizar transmision autorizada y a potencia minima.
No dejar el sistema desatendido ni operar en viento no validado.

## Cambios y revisiones

Registrar cada cambio de modulo, motor, microsteps, diametro de conductor,
coax o montaje. Un cambio RF exige revalidacion RF; un cambio de gear,
eje, carga o tripode exige revalidacion mecanica. Evitar mantener
parametros firmware y CAD de reducciones distintas.

Antes de publicar en GitHub: verificar alcance MIT/CERN-OHL-S-2.0 elegido,
comprobar dependencias y sus avisos, revisar ausencia de credenciales
y adjuntos privados, y cumplir entrega de fuentes del hardware.
