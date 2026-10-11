# Qué se tomó de cada referencia (y qué no)

| Referencia | Lo que se aprovechó | Lo que se descartó y por qué |
|---|---|---|
| KX4Z *Poor-Man's Satellite Station* Partes I–IV (PDF) | Requisitos de la estación (antena direccional, separación de bandas, apuntado, Doppler); anchura de haz amplia ⇒ apuntado tolerante; pérdida de 5–20 dB con una sola polarización; **dimensiones de las yagis** (tablas 144,1 y 432,1 MHz) como punto de partida; uso de boom no conductor y varilla de 1/8" | Boom de 1 m para el desfase λ/4 físico (ADR-004); rotor de actuador lineal + Yaesu G-450 (pesado, madera) |
| KX4Z Parte II + manual del PCB del controlador | Idea de controlador barato con control manual + automático, 2 ejes, y protocolo estándar de rotor | Arduino Nano (poca memoria para SGP4 + web), relés/PWM de motores DC |
| `docvacuumtubes/K3NG-based-...` | Arquitectura del controlador (tarjeta única, botones, protocolo) y la idea de usar el estándar K3NG/GS-232 | Se usa ESP32 con API HTTP propia. **No se implementó GS-232/Easycomm**, así que Gpredict/Look4Sat no pueden controlar este rotor sin añadirlo |
| `docvacuumtubes/ElevationRotatorVersion2` | Idea de casquillos impresos sobre tubo de aluminio y de pieza de límite | Actuador lineal: no sirve para 0–180° y es más pesado; su repositorio no declara licencia (no se copió ningún STL) |
| `SatcomRadio/Hybrid_Couplers` (MIT) | Híbridos de 90° (QCN3, CMX03A03, RF Power, Anaren) y el aviso de que cada puerto es un dipolo ⇒ sentido RHCP/LHCP según orientación | Falta confirmar la banda de cada placa (ADR-004) |
| `blog.tomasbrincil.cz` (OK1BT, AV2040) | Concepto de antena SATCOM plegable impresa en 3D; fórmulas de longitudes para 449,55 MHz | Las fórmulas no se usaron (son para UHF 449,55); el diseño se hizo con NEC2 |
| Ficha Cults3D AV2040-2 (imagen del usuario) | Concepto estético y de portabilidad | Licencia *Cults PU / No IA*: no se usó ningún archivo |
| Thingiverse 5904442 | — | El sitio bloqueó la lectura (detección de bots); **no se pudo analizar**. Pásame los STL o la descripción si quieres que se tenga en cuenta |
| `anatolbricoham/antenaSatCommrotor` + ZIP local (versión anterior) | Reparto del cálculo orbital en el rotor; interfaz de la radio independiente; idea de módulos separables; aprendizajes de masa | CM5, LimeSDR, Android, SO propio y 3 ejes (peso, complejidad y falta de validación física según su propio README) |
