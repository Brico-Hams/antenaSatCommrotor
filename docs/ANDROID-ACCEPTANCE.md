# Aceptacion de control Android y transferencia TLE

Estos criterios son ensayos pendientes, no afirmaciones de implementacion.
El contrato BLE definitivo debe corresponder al firmware compilado.

## Conexion y autorizacion

1. Android 12 o posterior: permiso de scan/connect denegado produce aviso,
   no reconexion infinita ni excepcion oculta. Versiones anteriores:
   revisar requisitos de ubicacion del sistema para escaneo BLE.
2. Seleccion explicita de dispositivo. UUID y version del contrato deben
   coincidir; no conectar al primer dispositivo que anuncia un nombre parecido.
3. Verificar cifrado/emparejamiento exigido por firmware y token de control
   configurado localmente; token falso no ejecuta comandos.
4. Token no aparece en logs, preferencias sin cifrar, capturas de errores
   ni archivos de compilacion. Clave protegida por Android Keystore.
5. Conectar, desconectar o reiniciar app no arma motores ni restaura homing.
6. Android y web simultaneos no deben evadir estado busy/interbloqueos.

## Protocolo y errores

1. Negociar MTU y probar tambien el minimo: dividir y recomponer mensajes
   segun contrato, no suponer que un TLE cabe en una escritura.
2. Request ID, longitud, secuencia, fragmento perdido y timeout deben
   producir errores claros y no aplicar mensajes parciales.
3. Respuesta no reconocida o version distinta no se muestra como exito.
4. Notificaciones y callbacks no bloquean UI ni el control seguro del rotor.
5. El rotor no hace filesystem/SGP4 pesado dentro del callback BLE;
   delega a su mecanismo seguro documentado.

## Calibracion

1. Mostrar estados separados: homing, UTC/posicion, nivel, norte verdadero
   y cero de encoder cuando se emplea. Un GNSS quieto no da orientacion.
2. Valores finitos, rangos y unidades coinciden con firmware.
3. Rechazar calibracion durante movimiento/seguimiento y con prerrequisitos
   incompletos; no limitar silenciosamente a un valor valido.
4. Usuario confirma verificacion fisica. La app no supone mediciones
   de sensores de inclinacion/orientacion no implementados.
5. Mover tripode o repetir homing invalida lo que corresponda segun politica.

## TLE por Internet del telefono

1. HTTPS de fuentes permitidas; sin TLS inseguro ni HTTP claro.
2. Error de red conserva ultimo catalogo valido y muestra antiguedad,
   sin marcar como nuevo el epoch por volver a descargar.
3. Validar longitud, checksum, epoch y limites de catalogo.
4. Transferir atomicamente: interrupcion BLE no deja cache truncada.
5. Actualizar TLE solo con rotor en estado permitido, sin pausar parada.
6. Frecuencias no se deducen del TLE; la radio se configura aparte.

## Pases y autonomia

1. App consulta pases calculados por SGP4 en ESP32; hora UTC inequívoca.
2. Seleccionar mismo satelite en lista/pase/seguimiento, sin confundir
   indices tras actualizar catalogo; utilizar identificacion NORAD.
3. Horizonte, limites de cable, adquisicion, cenit y velocidad:
   destinos imposibles provocan rechazo explicito del rotor.
4. Cerrar app durante pase: rotor continua autonomamente SOLO si datos,
   sensores y estado de seguridad permanecen validos.
5. Parada fisica sigue operando sin movil, Bluetooth o navegador.

## Entrega Android

Compilar APK con versiones fijadas y conservar hash/commit.
Pruebas de parser/UI no equivalen a ensayos con telefono y rotor.
GitHub Actions preparado no implica ejecucion remota ni distribucion
en tienda; la firma de release debe protegerse fuera del repositorio.
