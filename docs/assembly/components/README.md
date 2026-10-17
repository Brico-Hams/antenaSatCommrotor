# BricoHams: catalogo visual de componentes

Generado desde las BOM mediante `node scripts/component-catalog.cjs`.
Cobertura: **398 filas de componentes en 12 listas**. Cada fila tiene una ficha SVG propia; una fila puede agrupar varias unidades o designadores.

**Son pictogramas funcionales de identificacion, no fotografias, renders CAD, huellas PCB, planos a escala ni instrucciones de cableado.** Para la geometria disponible, consulte los [despieces CAD y vistas de PCB](../README.md). No se inventan formas de componentes todavia sin seleccionar.

Las especificaciones y notas se reproducen de cada BOM, incluso si son historicas o provisionales. Los IDs solo son unicos dentro de su lista; los IDs LITE son numeros de fila de este catalogo, no referencias de fabricante. No sumar alternativas, LEGACY, herramientas ni piezas compartidas. Los precios se consultan por separado en [REFERENCE-PRICES](../../REFERENCE-PRICES.md).

La BOM no equivale a una autorizacion de compra, fabricacion o energizacion. Prevalecen [VALIDATION](../../VALIDATION.md), las fichas de fabricante y la revision liberada. Las filas con cantidad cero se muestran para identificar referencias excluidas, no para comprarlas.

[Montaje por modulos](../README.md) · [Instalacion de software y conjunto](../06-instalacion.md) · [Cobertura y limites de la revision](../../PROJECT-REVIEW.md)

## Control ESP32 (no CM5)

[BOM fuente](../../../bom/electrical.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| E01 | ESP32 DevKit classic ESP32-WROOM | 1 | [Ficha visual](electrical-001.svg) |
| E02 | NEMA14 bipolar 200step motor | 2 | [Ficha visual](electrical-002.svg) |
| E03 | Stepper driver with STEP DIR ENABLE | 2 | [Ficha visual](electrical-003.svg) |
| E04 | AS5600 output encoder module | 2 | [Ficha visual](electrical-004.svg) |
| E05 | Diametric encoder magnet | 2 | [Ficha visual](electrical-005.svg) |
| E06 | GNSS UART module and antenna | 1 | [Ficha visual](electrical-006.svg) |
| E07 | Commercial protected DC supply or battery | 1 | [Ficha visual](electrical-007.svg) |
| E08 | DC-DC converter | 1 | [Ficha visual](electrical-008.svg) |
| E09 | Main switch and fuse holder | 1 | [Ficha visual](electrical-009.svg) |
| E10 | Accessible latching motor-power emergency stop | 1 | [Ficha visual](electrical-010.svg) |
| E11 | Travel or home limit switch | 4 | [Ficha visual](electrical-011.svg) |
| E12 | Wiring and strain relief kit | 1 | [Ficha visual](electrical-012.svg) |
| E13 | Bubble level and true-north reference method | 1 | [Ficha visual](electrical-013.svg) |
| E14 | Metal RF subenclosure | 1 | [Ficha visual](electrical-014.svg) |

## Mecanica BASE y LEGACY: no sumar alternativas

[BOM fuente](../../../bom/mechanical.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| P01 | Sol etapa 1 | 2 | [Ficha visual](mechanical-001.svg) |
| P02 | Sol etapa 2 | 2 | [Ficha visual](mechanical-002.svg) |
| P03 | Planeta 27 dientes | 12 | [Ficha visual](mechanical-003.svg) |
| P04 | Corona fija 72 dientes | 4 | [Ficha visual](mechanical-004.svg) |
| P05 | Portaplanetas etapa 1 | 2 | [Ficha visual](mechanical-005.svg) |
| P06 | Portaplanetas etapa 2 | 2 | [Ficha visual](mechanical-006.svg) |
| P07 | Placa motor | 2 | [Ficha visual](mechanical-007.svg) |
| P08 | Placa intermedia 608 | 2 | [Ficha visual](mechanical-008.svg) |
| P09 | Placa salida 6000 | 4 | [Ficha visual](mechanical-009.svg) |
| P10 | Retenedor608 | 2 | [Ficha visual](mechanical-010.svg) |
| P11 | Retenedor6000 | 4 | [Ficha visual](mechanical-011.svg) |
| P12 | Separador15 | 24 | [Ficha visual](mechanical-012.svg) |
| P13 | Separador9 | 24 | [Ficha visual](mechanical-013.svg) |
| P14 | Separador38 | 6 | [Ficha visual](mechanical-014.svg) |
| P15 | Base tripode | 1 | [Ficha visual](mechanical-015.svg) |
| P16 | Brida salida | 2 | [Ficha visual](mechanical-016.svg) |
| P17 | Soporte EL | 1 | [Ficha visual](mechanical-017.svg) |
| P18 | Silla boom20 | 1 | [Ficha visual](mechanical-018.svg) |
| P19 | Adaptador plano opcional | 1 | [Ficha visual](mechanical-019.svg) |
| P20 | Soporte final NC | 4 | [Ficha visual](mechanical-020.svg) |
| P21 | Portaiman | 2 | [Ficha visual](mechanical-021.svg) |
| P22 | Soporte AS5600 | 2 | [Ficha visual](mechanical-022.svg) |
| P23 | Cuna RT3S | 1 | [Ficha visual](mechanical-023.svg) |
| P24 | Caja electronica | 1 | [Ficha visual](mechanical-024.svg) |
| P25 | Tapa electronica | 1 | [Ficha visual](mechanical-025.svg) |
| P26 | Caja diplexor desmontable | 1 | [Ficha visual](mechanical-026.svg) |
| P27 | Tapa diplexor | 1 | [Ficha visual](mechanical-027.svg) |
| P28 | Cubo bisagra antena | 4 | [Ficha visual](mechanical-028.svg) |
| P29 | Brazo bisagra antena | 16 | [Ficha visual](mechanical-029.svg) |
| P30 | Puente dos booms RF y boom estructural | 1 | [Ficha visual](mechanical-030.svg) |
| M01 | Motor NEMA14 | 2 | [Ficha visual](mechanical-031.svg) |
| M02 | Rodamiento608 | 2 | [Ficha visual](mechanical-032.svg) |
| M03 | Rodamiento6000 | 4 | [Ficha visual](mechanical-033.svg) |
| M04 | Eje intermedio8 mm L36 | 2 | [Ficha visual](mechanical-034.svg) |
| M05 | Eje salida10 mm L77 | 2 | [Ficha visual](mechanical-035.svg) |
| M06 | Perno hombro4 mm tramo23 mm | 12 | [Ficha visual](mechanical-036.svg) |
| M07 | Casquillo6x4x12 mm | 12 | [Ficha visual](mechanical-037.svg) |
| M08 | Varilla roscada M3 AZ180 y EL130 | 12 | [Ficha visual](mechanical-038.svg) |
| M09 | Pasadores o tornillos transversales M3 | 10 | [Ficha visual](mechanical-039.svg) |
| M10 | Tornilleria arandelas tuercas e insertos M3 M4 M5 | 1 | [Ficha visual](mechanical-040.svg) |
| M11 | Tuerca capturada1/4-20 UNC | 1 | [Ficha visual](mechanical-041.svg) |
| M12 | Adaptador metal3/8-16 a1/4-20 | 1 | [Ficha visual](mechanical-042.svg) |
| M13 | U-bolts M5 boom20 | 2 | [Ficha visual](mechanical-043.svg) |
| M14 | Final carrera NC | 4 | [Ficha visual](mechanical-044.svg) |
| M15 | Imanes diametrales6x2 | 2 | [Ficha visual](mechanical-045.svg) |
| M16 | Forro diplexor pared y tapa0.3 mm | 1 | [Ficha visual](mechanical-046.svg) |
| M17 | Correas velcro radio y seguridad | 3 | [Ficha visual](mechanical-047.svg) |
| M18 | Varillas RF diametro4 mm | 1 | [Ficha visual](mechanical-048.svg) |
| M19 | Manguitos conductores8 OD 4 ID L50 | 8 | [Ficha visual](mechanical-049.svg) |
| M20 | Trenza RF flexible y puentes reflector | 1 | [Ficha visual](mechanical-050.svg) |
| M21 | Boombase dielectrico20 mm desmontable | 3 | [Ficha visual](mechanical-051.svg) |
| M22 | Balun match50ohm e hibrido90 grados POR BANDA | 2 | [Ficha visual](mechanical-052.svg) |
| M23 | Diplexor145435 coaxial y conectores | 1 | [Ficha visual](mechanical-053.svg) |
| M24 | Filamento ASA | 1 | [Ficha visual](mechanical-054.svg) |
| M25 | Placas refuerzo y bandeja fija | 1 | [Ficha visual](mechanical-055.svg) |
| B01 | BASE ligera impresa | 1 | [Ficha visual](mechanical-056.svg) |
| B02 | Copa608 variante correa | 4 | [Ficha visual](mechanical-057.svg) |
| B03 | Copa6000 variante correa | 4 | [Ficha visual](mechanical-058.svg) |
| B04 | Soporte encoder variante correa | 2 | [Ficha visual](mechanical-059.svg) |
| B05 | Brida salida compartida | 2 | [Ficha visual](mechanical-060.svg) |
| B06 | Silla20 compartida | 1 | [Ficha visual](mechanical-061.svg) |
| B07 | Cuna RT3S fija compartida | 1 | [Ficha visual](mechanical-062.svg) |
| B08 | Caja carrier180x130 y diplexor separado | 1 | [Ficha visual](mechanical-063.svg) |
| B09 | Cubos antena y bisagras compartidos | 1 | [Ficha visual](mechanical-064.svg) |
| B10 | Soportes NC compartidos y portaimanes | 1 | [Ficha visual](mechanical-065.svg) |
| B11 | Motor NEMA14 con eje saliente&gt;=26 mm | 2 | [Ficha visual](mechanical-066.svg) |
| B12 | Polea METAL GT2 20t agujero5 | 2 | [Ficha visual](mechanical-067.svg) |
| B13 | Polea METAL GT2 100t agujero8 | 2 | [Ficha visual](mechanical-068.svg) |
| B14 | Polea METAL GT2 20t agujero8 | 2 | [Ficha visual](mechanical-069.svg) |
| B15 | Polea METAL GT2 100t agujero10 | 2 | [Ficha visual](mechanical-070.svg) |
| B16 | Correa GT2 126t252 mm ancho6 | 4 | [Ficha visual](mechanical-071.svg) |
| B17 | Aluminio6082 placas3mm 187.13x86 | 4 | [Ficha visual](mechanical-072.svg) |
| B18 | Espaciadores metal OD8 ID4.5 L51 | 8 | [Ficha visual](mechanical-073.svg) |
| B19 | Rodamientos608 y6000 | 1 | [Ficha visual](mechanical-074.svg) |
| B20 | Ejes intermedios8x60 salida10x89 | 1 | [Ficha visual](mechanical-075.svg) |
| B21 | SoporteEL aluminio3mm y bandejaAZ | 1 | [Ficha visual](mechanical-076.svg) |
| B22 | Herrajes collarines llaves Ubolts adaptadores NC imanes | 1 | [Ficha visual](mechanical-077.svg) |
| B23 | RF aluminio fibra coax redes y diplexor | 1 | [Ficha visual](mechanical-078.svg) |
| B24 | ASA para varianteBASE | 1 | [Ficha visual](mechanical-079.svg) |
| B25 | Control y bateria portatil | 1 | [Ficha visual](mechanical-080.svg) |
| B26 | Bandeja estacionaria carrier180x130 | 1 | [Ficha visual](mechanical-081.svg) |
| B27 | Reserva carrierPCB ensamblada reportadahardware | 1 | [Ficha visual](mechanical-082.svg) |
| L01 | Motor candidato Pololu1207 SOYO SY35ST26-0284A | 2 | [Ficha visual](mechanical-083.svg) |
| L02 | Bateria candidata TalentCell YB1203000-USB | 1 | [Ficha visual](mechanical-084.svg) |
| L03 | BuildLight objetivos por grupo NO compra aprobada | 1 | [Ficha visual](mechanical-085.svg) |

## Antena PF-01 portable: alternativa candidata, no sumar a la antena anterior

[BOM fuente](../../../bom/antenna-portable.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| PF-01 | Cassette hub | 4 | [Ficha visual](portable-001.svg) |
| PF-02 | Hinged rod root | 16 | [Ficha visual](portable-002.svg) |
| PF-03 | Dielectric boom section | 2 | [Ficha visual](portable-003.svg) |
| PF-04 | Internal boom spigot | 1 | [Ficha visual](portable-004.svg) |
| PF-05 | VHF inner radial rod | 8 | [Ficha visual](portable-005.svg) |
| PF-06 | VHF reflector removable outer tip | 4 | [Ficha visual](portable-006.svg) |
| PF-07 | VHF driven removable outer tip | 4 | [Ficha visual](portable-007.svg) |
| PF-08 | UHF reflector radial rod | 4 | [Ficha visual](portable-008.svg) |
| PF-09 | UHF driven radial rod | 4 | [Ficha visual](portable-009.svg) |
| PF-10 | Conductive VHF tip coupler | 8 | [Ficha visual](portable-010.svg) |
| PF-11 | Shoulder pivot and retention | 16 | [Ficha visual](portable-011.svg) |
| PF-12 | Deployed locking pin | 16 | [Ficha visual](portable-012.svg) |
| PF-13 | Cassette-to-boom indexing pin | 4 | [Ficha visual](portable-013.svg) |
| PF-14 | Boom-spigot retention pin | 2 | [Ficha visual](portable-014.svg) |
| PF-15 | Fixed feed stubs and flexible RF bridges | 1 set | [Ficha visual](portable-015.svg) |
| PF-16 | Band-specific feed and matching networks | 1 set | [Ficha visual](portable-016.svg) |
| PF-17 | RF coax and SMA service loops | 1 set | [Ficha visual](portable-017.svg) |
| PF-18 | Removable rotor or manual mount | 1 | [Ficha visual](portable-018.svg) |
| PF-19 | Transport retainers and protective sleeve | 1 set | [Ficha visual](portable-019.svg) |
| PF-20 | External radial rod clamp hardware | 1 set | [Ficha visual](portable-020.svg) |
| PF-21 | Flexible reflector mesh quadrant | 4 | [Ficha visual](portable-021.svg) |
| PF-22 | Mesh perimeter and central attachment | 1 set | [Ficha visual](portable-022.svg) |
| PF-23 | Reserved folded mesh packet | 1 | [Ficha visual](portable-023.svg) |

## Eggbeater TX/RX: dos bandas separadas, no sumar a PF-01

[BOM fuente](../../../bom/antenna-eggbeater.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| EB-145-01 | Conductive arc segment | 16 | [Ficha visual](eggbeater-001.svg) |
| EB-145-02 | Conductive arc splice | 14 | [Ficha visual](eggbeater-002.svg) |
| EB-145-03 | Optional reflector radial | 4 | [Ficha visual](eggbeater-003.svg) |
| EB-145-04 | Optional reflector mid-radial splice | 4 | [Ficha visual](eggbeater-004.svg) |
| EB-145-10 | Segmented dielectric mast | 1 | [Ficha visual](eggbeater-005.svg) |
| EB-145-11 | Dielectric conductor support | 8 | [Ficha visual](eggbeater-006.svg) |
| EB-145-12 | Dual-port feed network | 1 | [Ficha visual](eggbeater-007.svg) |
| EB-145-13 | Receive preamp and TX bypass kit | 1 | [Ficha visual](eggbeater-008.svg) |
| EB-145-14 | Transport retainers | 1 | [Ficha visual](eggbeater-009.svg) |
| EB-435-01 | Conductive arc segment | 16 | [Ficha visual](eggbeater-010.svg) |
| EB-435-02 | Conductive arc splice | 14 | [Ficha visual](eggbeater-011.svg) |
| EB-435-03 | Optional reflector radial | 4 | [Ficha visual](eggbeater-012.svg) |
| EB-435-10 | Segmented dielectric mast | 1 | [Ficha visual](eggbeater-013.svg) |
| EB-435-11 | Dielectric conductor support | 8 | [Ficha visual](eggbeater-014.svg) |
| EB-435-12 | Dual-port feed network | 1 | [Ficha visual](eggbeater-015.svg) |
| EB-435-13 | Receive preamp and TX bypass kit | 1 | [Ficha visual](eggbeater-016.svg) |
| EB-435-14 | Transport retainers | 1 | [Ficha visual](eggbeater-017.svg) |

## QFH TX/RX: dos bandas separadas, no sumar a Eggbeater

[BOM fuente](../../../bom/antenna-qfh.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| QFH-145-01 | Helix segment | 16 | [Ficha visual](qfh-001.svg) |
| QFH-145-02 | Conductive helix splice | 12 | [Ficha visual](qfh-002.svg) |
| QFH-145-03 | Top diameter bar | 2 | [Ficha visual](qfh-003.svg) |
| QFH-145-04 | Bottom half bar | 4 | [Ficha visual](qfh-004.svg) |
| QFH-145-05 | End transition joint | 8 | [Ficha visual](qfh-005.svg) |
| QFH-145-10 | Segmented dielectric mast | 1 | [Ficha visual](qfh-006.svg) |
| QFH-145-11 | Dielectric conductor support | 8 | [Ficha visual](qfh-007.svg) |
| QFH-145-12 | Dual-port feed network | 1 | [Ficha visual](qfh-008.svg) |
| QFH-145-13 | Receive preamp and TX bypass kit | 1 | [Ficha visual](qfh-009.svg) |
| QFH-145-14 | Transport retainers | 1 | [Ficha visual](qfh-010.svg) |
| QFH-435-01 | Helix segment | 16 | [Ficha visual](qfh-011.svg) |
| QFH-435-02 | Conductive helix splice | 12 | [Ficha visual](qfh-012.svg) |
| QFH-435-03 | Top diameter bar | 2 | [Ficha visual](qfh-013.svg) |
| QFH-435-04 | Bottom half bar | 4 | [Ficha visual](qfh-014.svg) |
| QFH-435-05 | End transition joint | 8 | [Ficha visual](qfh-015.svg) |
| QFH-435-10 | Segmented dielectric mast | 1 | [Ficha visual](qfh-016.svg) |
| QFH-435-11 | Dielectric conductor support | 8 | [Ficha visual](qfh-017.svg) |
| QFH-435-12 | Dual-port feed network | 1 | [Ficha visual](qfh-018.svg) |
| QFH-435-13 | Receive preamp and TX bypass kit | 1 | [Ficha visual](qfh-019.svg) |
| QFH-435-14 | Transport retainers | 1 | [Ficha visual](qfh-020.svg) |

## Previo RX y bypass TX: 25 W pendiente de cualificacion

[BOM fuente](../../../bom/antenna-preamps.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| PRE-01 | Receive preselector | 1 per band | [Ficha visual](preamps-001.svg) |
| PRE-02 | Low noise amplifier | 1 per band | [Ficha visual](preamps-002.svg) |
| PRE-03 | Main RF transfer switch | 1 per band | [Ficha visual](preamps-003.svg) |
| PRE-04 | LNA input isolation switch and termination | 1 per band | [Ficha visual](preamps-004.svg) |
| PRE-05 | Receive limiter and protection | 1 per band | [Ficha visual](preamps-005.svg) |
| PRE-06 | PA and output filter | 1 per band | [Ficha visual](preamps-006.svg) |
| PRE-07 | Fail-safe hardware TX sequencer | 1 per station | [Ficha visual](preamps-007.svg) |
| PRE-08 | Forward reflected power and thermal protection | 1 per band | [Ficha visual](preamps-008.svg) |
| PRE-09 | 50 ohm terminations and shielded interconnects | 1 set | [Ficha visual](preamps-009.svg) |
| PRE-10 | Rated dummy load attenuator and test instruments | 1 per station | [Ficha visual](preamps-010.svg) |

## Conjunto CM5 multimodo: diseno en revision

[BOM fuente](../../../bom/multimode-assembly.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| MMA-001 | Tripod and head | 1 | [Ficha visual](multimode-001.svg) |
| MMA-002 | Fixed metal tray / rotor adapter | 1 | [Ficha visual](multimode-002.svg) |
| MMA-003 | Tripod-to-tray fasteners and secondary restraint | 1 | [Ficha visual](multimode-003.svg) |
| MMA-004 | GT2 timing belts | 4 | [Ficha visual](multimode-004.svg) |
| MMA-005 | GT2 metal pulleys 20 tooth | 4 | [Ficha visual](multimode-005.svg) |
| MMA-006 | GT2 metal pulleys 100 tooth | 4 | [Ficha visual](multimode-006.svg) |
| MMA-007 | 608 bearings | 4 | [Ficha visual](multimode-007.svg) |
| MMA-008 | 6000 bearings | 4 | [Ficha visual](multimode-008.svg) |
| MMA-009 | Intermediate steel shafts | 2 | [Ficha visual](multimode-009.svg) |
| MMA-010 | Output steel shafts | 2 | [Ficha visual](multimode-010.svg) |
| MMA-011 | Aluminum 6082 plate/support parts | 1 set | [Ficha visual](multimode-011.svg) |
| MMA-012 | Metal elevation parking pin/restraint | 1 | [Ficha visual](multimode-012.svg) |
| MMA-013 | External ECO-WORTHY LiFePO4 12 V 30 Ah battery reference plus compatible charger and leads | 1 set | [Ficha visual](multimode-013.svg) |
| MMA-014 | DC-rated latching main / motor stop hardware | 1 | [Ficha visual](multimode-014.svg) |
| MMA-015 | Raspberry Pi Compute Module 5 (CM5) | 1 | [Ficha visual](multimode-015.svg) |
| MMA-016 | Deterministic motion pulse / safety interface | 1 set | [Ficha visual](multimode-016.svg) |
| MMA-017 | LimeSDR Mini replaceable SDR modules | 2 | [Ficha visual](multimode-017.svg) |
| MMA-018 | Conditional linear PA and thermal hardware | 1 set | [Ficha visual](multimode-018.svg) |
| MMA-019 | Band/harmonic filters and duplexing/isolation network | 1 set | [Ficha visual](multimode-019.svg) |
| MMA-020 | Shielded RF/audio enclosure and bonding hardware | 1 | [Ficha visual](multimode-020.svg) |
| MMA-021 | 50-ohm coax, jumpers and RF connectors | 1 set | [Ficha visual](multimode-021.svg) |
| MMA-022 | 50-ohm dummy load and calibrated attenuators/couplers | 1 set | [Ficha visual](multimode-022.svg) |
| MMA-023 | Audio codec and two-channel RX audio selector | 1 | [Ficha visual](multimode-023.svg) |
| MMA-024 | Internal speaker and microphone | 1 | [Ficha visual](multimode-024.svg) |
| MMA-025 | Baofeng K1 dual-plug external audio/PTT lead (3.5 mm + 2.5 mm) | 1 | [Ficha visual](multimode-025.svg) |
| MMA-026 | Bluetooth bidirectional audio transport | 1 set | [Ficha visual](multimode-026.svg) |
| MMA-027 | GNSS receiver and antenna | 1 set | [Ficha visual](multimode-027.svg) |
| MMA-028 | Power distribution harness Anderson Powerpole-family input and DC fuses | 1 set | [Ficha visual](multimode-028.svg) |
| MMA-029 | SOL calibration kit and RF test cables | 1 | [Ficha visual](multimode-029.svg) |
| MMA-030 | VNA | 1 | [Ficha visual](multimode-030.svg) |
| MMA-031 | Spectrum analyzer or calibrated receiver | 1 | [Ficha visual](multimode-031.svg) |
| MMA-032 | Current-limited supply | 1 | [Ficha visual](multimode-032.svg) |
| MMA-033 | DMM and oscilloscope with suitable probes | 1 | [Ficha visual](multimode-033.svg) |
| MMA-034 | Calipers scale level dial indicator and hand tools | 1 set | [Ficha visual](multimode-034.svg) |
| MMA-035 | Limited axial-roll POL motor and mechanical mount | 1 | [Ficha visual](multimode-035.svg) |
| MMA-036 | Watterott TMC5160 v1.5 POL driver module | 1 | [Ficha visual](multimode-036.svg) |
| MMA-037 | Independent AZ EL and POL output encoders | 3 | [Ficha visual](multimode-037.svg) |
| MMA-038 | Normally-closed AZ EL and POL end-limit switches | 6 | [Ficha visual](multimode-038.svg) |
| MMA-039 | Independent POL watchdog and fault interlock path | 1 | [Ficha visual](multimode-039.svg) |
| MMA-040 | Protected third-axis power branch and harness | 1 set | [Ficha visual](multimode-040.svg) |
| MMA-041 | Band-specific 145 MHz circular-feed / quadrature network | 1 | [Ficha visual](multimode-041.svg) |
| MMA-042 | Band-specific 435 MHz circular-feed / quadrature network | 1 | [Ficha visual](multimode-042.svg) |
| MMA-043 | Independent RF RHCP/LHCP selector network | 1 set | [Ficha visual](multimode-043.svg) |
| MMA-044 | Limited-travel POL coax/control service loop | 1 | [Ficha visual](multimode-044.svg) |
| MMA-045 | Axial-ratio and RF-switch isolation measurement capability | 1 set | [Ficha visual](multimode-045.svg) |
| MMA-046 | Remote compass magnetometer and base-inclination IMU | 1 | [Ficha visual](multimode-046.svg) |
| MMA-047 | Custom CM5 auxiliary PCB assembly | 1 | [Ficha visual](multimode-047.svg) |
| MMA-048 | Two direct CM5 I/O USB 3 SDR links and interface topology | 1 set | [Ficha visual](multimode-048.svg) |
| MMA-049 | CM5/SDR/motor power conversion and thermal solution | 1 set | [Ficha visual](multimode-049.svg) |
| MMA-050 | Official Raspberry Pi CM5 I/O board | 1 | [Ficha visual](multimode-050.svg) |
| MMA-051 | Nonconductive inert mechanical dummy load and restraint fixture | 1 set | [Ficha visual](multimode-051.svg) |
| MMA-052 | Optional qualified powered USB hub for USB audio route | 1 set | [Ficha visual](multimode-052.svg) |

## PCB ESP32: HOLD de fabricacion

[BOM fuente](../../../bom/pcb.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| J1 | DC_IN_12V | 1 | [Ficha visual](pcb-001.svg) |
| D1 | SB560_REVERSE_BLOCK | 1 | [Ficha visual](pcb-002.svg) |
| D2 | SMBJ15A_TVS | 1 | [Ficha visual](pcb-003.svg) |
| F1 | T3.15A_MAIN | 1 | [Ficha visual](pcb-004.svg) |
| F2 | T2.5A_MOTOR | 1 | [Ficha visual](pcb-005.svg) |
| J2 | LATCHED_STOP_POWER_OUT_RETURN | 1 | [Ficha visual](pcb-006.svg) |
| F4 | T1A_BUCK_INPUT | 1 | [Ficha visual](pcb-007.svg) |
| J4 | EXTERNAL_BUCK_INPUT | 1 | [Ficha visual](pcb-008.svg) |
| J5 | EXTERNAL_BUCK_5V_RETURN | 1 | [Ficha visual](pcb-009.svg) |
| F3 | T1A_LOGIC_5V | 1 | [Ficha visual](pcb-010.svg) |
| JP1 | REMOVE_FOR_USB | 1 | [Ficha visual](pcb-011.svg) |
| U1 | ESP32_DEVKITC_V4_38_WROOM32E | 1 | [Ficha visual](pcb-012.svg) |
| U2 | WATTEROTT_TMC2209_V2 | 1 | [Ficha visual](pcb-013.svg) |
| C1 | 220u_35V_LOW_ESR | 1 | [Ficha visual](pcb-014.svg) |
| JM1 | AZ_MOTOR | 1 | [Ficha visual](pcb-015.svg) |
| U3 | WATTEROTT_TMC2209_V2 | 1 | [Ficha visual](pcb-016.svg) |
| C2 | 220u_35V_LOW_ESR | 1 | [Ficha visual](pcb-017.svg) |
| JM2 | EL_MOTOR | 1 | [Ficha visual](pcb-018.svg) |
| J6 | GNSS_3V3_UART | 1 | [Ficha visual](pcb-019.svg) |
| J7 | AZ_AS5600_I2C0 | 1 | [Ficha visual](pcb-020.svg) |
| J8 | EL_AS5600_I2C1 | 1 | [Ficha visual](pcb-021.svg) |
| J9 | OPTIONAL_IMU_MAG_I2C0 | 1 | [Ficha visual](pcb-022.svg) |
| J3 | STOP_N_NC_AUX_ONLY | 1 | [Ficha visual](pcb-023.svg) |
| J10 | AZ_MIN_N_NC_AUX_ONLY | 1 | [Ficha visual](pcb-024.svg) |
| J11 | AZ_MAX_N_NC_AUX_ONLY | 1 | [Ficha visual](pcb-025.svg) |
| J12 | EL_MIN_N_NC_AUX_ONLY | 1 | [Ficha visual](pcb-026.svg) |
| J13 | EL_MAX_N_NC_AUX_ONLY | 1 | [Ficha visual](pcb-027.svg) |
| R1 | 10k | 1 | [Ficha visual](pcb-028.svg) |
| R2 | 10k | 1 | [Ficha visual](pcb-029.svg) |
| R3 | 10k | 1 | [Ficha visual](pcb-030.svg) |
| R4 | 10k | 1 | [Ficha visual](pcb-031.svg) |
| R5 | 10k | 1 | [Ficha visual](pcb-032.svg) |
| R6 | 10k | 1 | [Ficha visual](pcb-033.svg) |
| R7 | 4k7 | 1 | [Ficha visual](pcb-034.svg) |
| R8 | 4k7 | 1 | [Ficha visual](pcb-035.svg) |
| R9 | 4k7 | 1 | [Ficha visual](pcb-036.svg) |
| R10 | 4k7 | 1 | [Ficha visual](pcb-037.svg) |
| C3 | 100n_50V | 1 | [Ficha visual](pcb-038.svg) |
| C4 | 100n_50V | 1 | [Ficha visual](pcb-039.svg) |
| C5 | 100n_50V | 1 | [Ficha visual](pcb-040.svg) |
| PCB | 180x130mm 2layer 2oz 1.6mm | 1 | [Ficha visual](pcb-041.svg) |
| STOP | 12V &gt;=5A DC power NC + isolated NC auxiliary | 1 | [Ficha visual](pcb-042.svg) |
| BUCK | 5V 2.2A regulated | 1 | [Ficha visual](pcb-043.svg) |
| U1_SOCKET | 1x19 2.54mm female socket | 2 | [Ficha visual](pcb-044.svg) |
| U2_U3_SOCKET | 1x8 2.54mm female socket | 4 | [Ficha visual](pcb-045.svg) |
| GNSS | External 3.3V UART GPS | 1 | [Ficha visual](pcb-046.svg) |
| ENCODER | External AS5600 on qualified 3.3V breakout | 2 | [Ficha visual](pcb-047.svg) |

## POL, sensores y redes RF: concepto no cualificado

[BOM fuente](../../../bom/polarization.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| POL-01 | Stator frame | 1 | [Ficha visual](polarization-001.svg) |
| POL-02 | Rotating saddle carrier | 1 | [Ficha visual](polarization-002.svg) |
| POL-03 | 608 bearing retainer | 2 | [Ficha visual](polarization-003.svg) |
| POL-04 | Travel cam | 1 | [Ficha visual](polarization-004.svg) |
| POL-05 | NC switch bracket | 1 | [Ficha visual](polarization-005.svg) |
| POL-06 | Existing BASE 20 mm boom saddle | 1 | [Ficha visual](polarization-006.svg) |
| POL-07 | POL stepper motor | 1 | [Ficha visual](polarization-007.svg) |
| POL-08 | GT2 driver pulley | 1 | [Ficha visual](polarization-008.svg) |
| POL-09 | GT2 driven pulley | 1 | [Ficha visual](polarization-009.svg) |
| POL-10 | GT2 belt | 1 | [Ficha visual](polarization-010.svg) |
| POL-11 | 608 bearing | 2 | [Ficha visual](polarization-011.svg) |
| POL-12 | Hollow roll shaft | 1 | [Ficha visual](polarization-012.svg) |
| POL-13 | NC travel switch | 2 | [Ficha visual](polarization-013.svg) |
| POL-14 | Mechanical stop pin | 2 | [Ficha visual](polarization-014.svg) |
| POL-15 | Cheek reinforcement | 2 | [Ficha visual](polarization-015.svg) |
| POL-16 | Motor mounting plate | 1 | [Ficha visual](polarization-016.svg) |
| POL-17 | RF 90-degree hybrid coupler | 2 | [Ficha visual](polarization-017.svg) |
| POL-18 | Flexible coax trunk and service loop | 1 assembly | [Ficha visual](polarization-018.svg) |
| POL-19 | Fasteners and clamp hardware | As required | [Ficha visual](polarization-019.svg) |
| POL-20 | Motor-plate standoff | 4 | [Ficha visual](polarization-020.svg) |
| POL-21 | Carrier shaft clamp screw | 2 | [Ficha visual](polarization-021.svg) |
| POL-22 | Limit-cam split-clamp screw | 1 | [Ficha visual](polarization-022.svg) |
| POL-23 | RF RHCP/LHCP handedness DPDT transfer switch | 2 | [Ficha visual](polarization-023.svg) |
| POL-24 | RF termination load | 2 | [Ficha visual](polarization-024.svg) |
| POL-25 | Rotating-side dual-band diplexer | 1 | [Ficha visual](polarization-025.svg) |
| SEN-01 | AZ absolute encoder | 1 | [Ficha visual](polarization-026.svg) |
| SEN-02 | EL absolute encoder | 1 | [Ficha visual](polarization-027.svg) |
| SEN-03 | POL absolute encoder | 1 | [Ficha visual](polarization-028.svg) |
| SEN-04 | Encoder mounting brackets | 3 | [Ficha visual](polarization-029.svg) |
| SEN-05 | Remote fixed-base compass/IMU | 1 | [Ficha visual](polarization-030.svg) |
| SEN-06 | Compass/IMU placeholder mount | 1 | [Ficha visual](polarization-031.svg) |
| SEN-07 | GPS receiver | 1 | [Ficha visual](polarization-032.svg) |
| SEN-08 | Stationary GPS antenna | 1 | [Ficha visual](polarization-033.svg) |
| SEN-09 | GPS antenna placeholder mount | 1 | [Ficha visual](polarization-034.svg) |
| SEN-10 | Sensor cabling and connectors | 1 set | [Ficha visual](polarization-035.svg) |
| POL-26 | SMA bulkhead jack | 1 | [Ficha visual](polarization-036.svg) |
| POL-27 | Coax bulkhead and strain-relief interface plate | 1 | [Ficha visual](polarization-037.svg) |
| RF-26 | 145 MHz circular-feed coax branch A | 1 | [Ficha visual](polarization-038.svg) |
| RF-27 | 145 MHz circular-feed coax branch B | 1 | [Ficha visual](polarization-039.svg) |
| RF-28 | 435 MHz circular-feed coax branch A | 1 | [Ficha visual](polarization-040.svg) |
| RF-29 | 435 MHz circular-feed coax branch B | 1 | [Ficha visual](polarization-041.svg) |
| POL-28 | RF connector interface standard | All RF paths | [Ficha visual](polarization-042.svg) |
| COM-01 | Compute module | 1 | [Ficha visual](polarization-043.svg) |
| COM-02 | CM5 carrier board | 1 | [Ficha visual](polarization-044.svg) |
| COM-03 | CM5 thermal solution | 1 | [Ficha visual](polarization-045.svg) |
| COM-04 | CM5 carrier and enclosure mounts | 1 set | [Ficha visual](polarization-046.svg) |
| SDR-01 | LimeSDR Mini | 2 | [Ficha visual](polarization-047.svg) |
| SDR-02 | LimeSDR Mini mounts | 2 | [Ficha visual](polarization-048.svg) |
| RF-30 | SDR power amplifier(s) | As selected | [Ficha visual](polarization-049.svg) |
| RF-31 | SDR filters | As selected | [Ficha visual](polarization-050.svg) |
| COM-05 | Compute/SDR enclosure | 1 | [Ficha visual](polarization-051.svg) |
| COM-06 | Auxiliary station electronics | As installed | [Ficha visual](polarization-052.svg) |
| PWR-01 | External battery pack and BMS | 1 | [Ficha visual](polarization-053.svg) |
| PWR-02 | External battery charger | 1 | [Ficha visual](polarization-054.svg) |
| PWR-03 | Station-side power conversion and protection | 1 set | [Ficha visual](polarization-055.svg) |
| PWR-04 | Powerpole input connector pair and contacts | 1 mating pair | [Ficha visual](polarization-056.svg) |
| PWR-05 | Battery input wire pair | 1 positive/return pair | [Ficha visual](polarization-057.svg) |
| PWR-06 | Positive master fuse holder and fuse | 1 | [Ficha visual](polarization-058.svg) |
| PWR-07 | CM5IO converter branch fuse and holder | 1 | [Ficha visual](polarization-059.svg) |
| PWR-08 | Motor and emergency-stop branch fuse and holder | 1 | [Ficha visual](polarization-060.svg) |
| PWR-09 | RF PA branch fuse and holder | 1 | [Ficha visual](polarization-061.svg) |
| PWR-10 | CM5IO converter branch wiring | 1 positive/return pair | [Ficha visual](polarization-062.svg) |
| PWR-11 | Motor and emergency-stop branch wiring | 1 positive/return pair | [Ficha visual](polarization-063.svg) |
| PWR-12 | RF PA branch wiring | 1 positive/return pair | [Ficha visual](polarization-064.svg) |
| PWR-13 | Optional generic power-harness strain-relief plate | 1 | [Ficha visual](polarization-065.svg) |
| PWR-14 | Powerpole connector-housing panel bracket | Optional; 1 if selected | [Ficha visual](polarization-066.svg) |

## RF: referencias, alternativas y herramientas

[BOM fuente](../../../bom/rf.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| D-L13 | 68 nH 0805 alta Q | 2 | [Ficha visual](rf-001.svg) |
| D-L2 | 100 nH 0805 alta Q | 1 | [Ficha visual](rf-002.svg) |
| D-L45 | 15 nH 0805 alta Q | 2 | [Ficha visual](rf-003.svg) |
| D-C12 | 18 pF C0G NP0 0805 &gt;=100 V | 2 | [Ficha visual](rf-004.svg) |
| D-C35 | 8.2 pF C0G NP0 0805 &gt;=100 V | 2 | [Ficha visual](rf-005.svg) |
| D-C4 | 4.7 pF C0G NP0 0805 &gt;=100 V | 1 | [Ficha visual](rf-006.svg) |
| D-SMA | Amphenol 132289 SMA hembra canto bulkhead | 3 | [Ficha visual](rf-007.svg) |
| D-BNC | Amphenol B6252HB-NPP3G-50 BNC acodado | 3 | [Ficha visual](rf-008.svg) |
| D-CASE-SMA | Exterior publicado 45.2x27.6x14.1 mm PCB37x23 mm | 1 | [Ficha visual](rf-009.svg) |
| D-CASE-BNC | Exterior publicado 59.9x37.6x23.5 mm PCB55.5x33 mm | 1 | [Ficha visual](rf-010.svg) |
| D-SCREW-SMA | M2x10 autorroscante | 2 | [Ficha visual](rf-011.svg) |
| D-SCREW-BNC | M2x12 autorroscante | 2 | [Ficha visual](rf-012.svg) |
| HY-VHF | Hibrido90grados o red de fase a definir | 1 | [Ficha visual](rf-013.svg) |
| HY-UHF | Hibrido90grados o red de fase a definir | 1 | [Ficha visual](rf-014.svg) |
| HY-QCN | QCN-3+ Mini-Circuits | 0 | [Ficha visual](rf-015.svg) |
| HY-CMX | CMX03A03 | 0 | [Ficha visual](rf-016.svg) |
| HY-ANAREN | Anaren10260-3 | 0 | [Ficha visual](rf-017.svg) |
| HY-RFPOWER | RF Power identidad incierta | 0 | [Ficha visual](rf-018.svg) |
| HY-TERM | Carga RF50ohm para puerto aislado | 2 | [Ficha visual](rf-019.svg) |
| COAX-VHF | Coax50ohm y conectores compatibles longitud a medir | 1 | [Ficha visual](rf-020.svg) |
| COAX-UHF | Coax50ohm y conectores compatibles longitud a medir | 1 | [Ficha visual](rf-021.svg) |
| VNA-LOAD | Carga50ohm calibrada RF | 3 | [Ficha visual](rf-022.svg) |
| VNA-CAL | Kit SOL thru y cables50ohm | 1 | [Ficha visual](rf-023.svg) |
| RADIO | Retevis RT-3S con OpenGD77 build por verificar | 1 | [Ficha visual](rf-024.svg) |

## Auxiliar CM5: NO FABRICAR / NO ENERGIZAR

[BOM fuente](../../../hardware/cm5/fabrication/NOT_FOR_MANUFACTURE/JLCPCB-BOM-REVIEW.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| C12,C13,C14,C15,C17,C18,C19,C20,C21,C22,C23,C24,C25,C3,C4,C5,C6,C7,C8,C9 | 100n | 20 | [Ficha visual](cm5-001.svg) |
| R14,R15,R16,R17,R18,R19,R20,R21,R23,R24,R25,R26,R27,R28,R29,R3,R30,R31,R32,R33,R34,R35,R36,R37,R38,R39,R40,R41,R42,R43,R45,R46,R48,R49,R50,R51 | 10k | 36 | [Ficha visual](cm5-002.svg) |
| R22 | 1M | 1 | [Ficha visual](cm5-003.svg) |
| R44,R47 | 1k | 2 | [Ficha visual](cm5-004.svg) |
| C1,C10,C11,C2 | 1u | 4 | [Ficha visual](cm5-005.svg) |
| Q1,Q2,Q3,Q4,Q5,Q6 | 2N7002 | 6 | [Ficha visual](cm5-006.svg) |
| R1,R10,R11,R12,R13,R2,R4,R5,R6,R7,R8,R9 | 4.7k | 12 | [Ficha visual](cm5-007.svg) |
| R53,R54 | 5.1k | 2 | [Ficha visual](cm5-008.svg) |
| U1 | AP2112K-3.3TRG1 | 1 | [Ficha visual](cm5-009.svg) |
| U10,U11 | LTV-817S | 2 | [Ficha visual](cm5-010.svg) |
| U2 | MCP23017-E/SO | 1 | [Ficha visual](cm5-011.svg) |
| U14,U8,U9 | SN74HC08DR | 3 | [Ficha visual](cm5-012.svg) |
| U6 | SN74HC123DR | 1 | [Ficha visual](cm5-013.svg) |
| U12,U4,U5 | SN74HC14DR | 3 | [Ficha visual](cm5-014.svg) |
| U7 | SN74HC30DR | 1 | [Ficha visual](cm5-015.svg) |
| U13 | SN74HC74DR | 1 | [Ficha visual](cm5-016.svg) |
| U3 | TCA9548APWR | 1 | [Ficha visual](cm5-017.svg) |

## PortableSatLite independiente: no mezclar con BASE

[BOM fuente](../../../PortableSatLite/bom/bom.csv)

| ID / designadores | Componente | Cantidad | Imagen |
| --- | --- | --- | --- |
| LITE-001 | NEMA17 stepper 34 mm body | 2 | [Ficha visual](lite-001.svg) |
| LITE-002 | 6806 bearing 30x42x7 | 2 | [Ficha visual](lite-002.svg) |
| LITE-003 | Steel/stainless rod 4 mm | 1 | [Ficha visual](lite-003.svg) |
| LITE-004 | Hardware M3/M4 (screws, nuts, washers) | 1 | [Ficha visual](lite-004.svg) |
| LITE-005 | 20 mm aluminium/CF tube 1 mm wall | 1 | [Ficha visual](lite-005.svg) |
| LITE-006 | Micro switch NC | 2 | [Ficha visual](lite-006.svg) |
| LITE-007 | ESP32 DevKitC | 1 | [Ficha visual](lite-007.svg) |
| LITE-008 | TMC2209 module | 2 | [Ficha visual](lite-008.svg) |
| LITE-009 | GNSS NEO-6M/M8N + antenna | 1 | [Ficha visual](lite-009.svg) |
| LITE-010 | MPU6050 module | 1 | [Ficha visual](lite-010.svg) |
| LITE-011 | QMC5883L module | 1 | [Ficha visual](lite-011.svg) |
| LITE-012 | AS5600 module | 2 | [Ficha visual](lite-012.svg) |
| LITE-013 | Buck 12V to 5V | 1 | [Ficha visual](lite-013.svg) |
| LITE-014 | USB-C PD trigger 12 V (optional) | 1 | [Ficha visual](lite-014.svg) |
| LITE-015 | Fuse + holder + 100 uF caps + wire | 1 | [Ficha visual](lite-015.svg) |
| LITE-016 | Existing 2m/70cm diplexer PCB (BRICOHAMS) | 1 | [Ficha visual](lite-016.svg) |
| LITE-017 | 90 deg hybrid coupler board (SatcomRadio) - VERIFY BAND | 2 | [Ficha visual](lite-017.svg) |
| LITE-018 | SMA/BNC bulkheads | 3 | [Ficha visual](lite-018.svg) |
| LITE-019 | Coax 75 ohm RG-59 (qwt) 2 m | 1 | [Ficha visual](lite-019.svg) |
| LITE-020 | Coax 50 ohm RG-58 patch 1.5 m | 1 | [Ficha visual](lite-020.svg) |
| LITE-021 | 3 mm aluminium rod 4 m | 2 | [Ficha visual](lite-021.svg) |
| LITE-022 | PVC conduit 16 mm 1 m | 1 | [Ficha visual](lite-022.svg) |
| LITE-023 | ASA filament | 1 | [Ficha visual](lite-023.svg) |
