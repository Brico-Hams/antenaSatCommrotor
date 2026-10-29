# ADR-001: Arquitectura "Lite": un único ESP32, sin ordenador embebido ni SDR

**Estado:** Aceptada

## Contexto
La versión anterior del usuario (ZIP `PortableSatStation-20261010`, repo `Brico-Hams/antenaSatCommrotor`) integraba Raspberry Pi CM5, dos LimeSDR Mini, Android, imagen de SO y 3 ejes; su propio README admite que el objetivo de ≤3 kg **no se cumplía** (3,13–3,20 kg antes de adicionales) y que casi nada está validado físicamente. El encargo actual pide un rotor + antena **ligeros, baratos y autónomos** con una radio RT3S/OpenGD77 independiente.

## Decisión
Un ESP32 hace todo lo que el rotor necesita: punto de acceso Wi-Fi y servidor web, SGP4, GNSS, sensores y pulsos de paso. La radio es un equipo aparte.

## Justificación y evidencia
La librería SGP4 de Hopperpop (MIT) no depende del hardware (`architectures=*`, pensada para ESP8266) y aquí se validó numéricamente (`tests/test_sgp4_lib.py`: 0,002° de error frente a python-sgp4). Quitar CM5, 2 LimeSDR, refrigeración y su alimentación elimina la mayor parte de la masa, del consumo y del riesgo de integración. Se mantiene la idea útil de la versión anterior: el cálculo orbital va en el rotor, no en el móvil.

## Consecuencias y límites
No hay audio digital, SSTV ni APRS en el rotor (eso lo hace la radio o una app aparte). Si en el futuro se quiere un SDR, el rotor sigue valiendo: solo expone una API HTTP.
