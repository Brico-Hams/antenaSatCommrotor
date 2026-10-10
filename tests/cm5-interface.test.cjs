const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const iface = JSON.parse(fs.readFileSync(
  path.join(root, 'hardware', 'cm5', 'interface.json'),
  'utf8',
));
const readme = fs.readFileSync(path.join(root, 'docs', 'CM5-PCB.md'), 'utf8');

test('CM5 GPIO assignment is unique, complete, and excludes ID_SD/ID_SC', () => {
  const bcm = iface.gpio.map((pin) => pin.bcm);
  const header = iface.gpio.map((pin) => pin.headerPin);
  assert.equal(new Set(bcm).size, bcm.length);
  assert.equal(new Set(header).size, header.length);
  assert.deepEqual([...bcm].sort((a, b) => a - b),
    Array.from({ length: 26 }, (_, i) => i + 2));
  assert.ok(!header.includes(27));
  assert.ok(!header.includes(28));
});

test('SPI1, I2C1, GNSS UART/PPS and mux channels match the frozen allocation', () => {
  const { spi, i2c, gnss } = iface.peripherals;
  assert.deepEqual([spi.mosiBcm, spi.misoBcm, spi.sclkBcm], [20, 19, 21]);
  assert.deepEqual([
    spi.chipSelects.AZ.bcm,
    spi.chipSelects.EL.bcm,
    spi.chipSelects.POL.bcm,
  ], [18, 17, 16]);
  assert.deepEqual([i2c.sdaBcm, i2c.sclBcm, i2c.mux.resetBcm], [2, 3, 13]);
  assert.deepEqual(Object.keys(i2c.channels), ['0', '1', '2', '3', '4']);
  assert.deepEqual([gnss.txBcm, gnss.rxBcm, gnss.ppsBcm], [14, 15, 27]);
});

test('sensor interfaces avoid the shared AS5600 address collision', () => {
  const { sensors, i2c } = iface.peripherals;
  assert.equal(sensors.encoders.count, 3);
  assert.equal(sensors.encoders.address, '0x36');
  assert.deepEqual(
    [0, 1, 2].map((ch) => i2c.channels[String(ch)]),
    ['ENCODER_AZ_AS5600', 'ENCODER_EL_AS5600', 'ENCODER_POL_AS5600'],
  );
  assert.equal(i2c.mux.address, '0x70');
  assert.equal(sensors.compass.productId, '4479');
  assert.equal(sensors.imu.productId, '4438');
});

test('reset, motor-enable, E-stop, limits, and PTT are fail-closed', () => {
  const safety = iface.safety;
  assert.equal(safety.limitInputs.count, 6);
  assert.equal(safety.limitInputs.contact, 'normally closed to GND');
  assert.equal(safety.limitInputs.softwareInputIsNotTheIndependentHardStop, true);
  assert.equal(safety.estop.contactRatingUnselected, true);
  assert.equal(safety.watchdog.exactWatchdogPartUnselected, true);
  assert.equal(safety.motorEnable.default, 'DISABLED');
  assert.deepEqual(safety.motorEnable.perAxisRequests, {
    AZ: 'MCP23017 GPA0',
    EL: 'MCP23017 GPA1',
    POL: 'MCP23017 GPA2',
  });
  assert.equal(safety.ptt.default, 'OPEN / INHIBITED');
  assert.equal(safety.ptt.separateIsolatedOutputs, true);
  assert.equal(iface.softwareContract.unverifiedHardwareMustRemainDisabled, true);
  assert.match(readme, /This map is frozen for\s+the rotor controller and radio hardware adapter/i);
  assert.match(readme, /healthy external\s+watchdog/i);
  assert.match(readme, /closed E-stop\s+chain/i);
  assert.match(readme, /Do not move the motors/i);
});

test('CM5 candidate, CM5IO voltage and occupied native USB3 ports are explicit', () => {
  assert.equal(iface.board.hostModuleCandidate, 'CM5104016');
  assert.equal(iface.board.moduleSkuConfirmed, false);
  assert.equal(iface.board.hostHeaderVoltageV, 3.3);
  assert.equal(iface.board.usb3RouteOnAuxiliaryBoard, false);
  assert.equal(iface.board.gpioContractStatus, 'frozen for software integration');
  assert.equal(iface.board.hardwareStatus, 'routed digital review; not fabricated; power front-end DNP; not commissioned; DO NOT ORDER');
  assert.match(readme, /VIO jumper to \*\*3\.3 V\*\*/);
  assert.match(readme, /two native USB 3 ports/);
});

test('USB-C power and data are separate, and power budget does not overclaim', () => {
  const usb = iface.board.usbPowerDataTopology;
  assert.equal(usb.cm5ioUsbCPowerInputSeparateFromUsbDataHost, true);
  assert.equal(usb.combinedPowerDataPortAssumed, false);
  assert.equal(usb.powerTargetV, 5);
  assert.equal(usb.powerTargetA, 5);
  assert.match(usb.powerTargetStatus, /conditional design target/);
  assert.equal(usb.requiresNegotiatedUsbCPdContract, true);
  assert.equal(usb.requiresCm5ioInputRatingVerification, true);
  assert.equal(usb.requiresFullConcurrentLoadMeasurement, true);
  assert.equal(usb.sourceAt5V3AAccepted, false);
  assert.equal(usb.limeSdrMiniCount, 2);
  assert.equal(usb.limeSdrMiniCombinedMinimumCurrentA, 1.2);
  assert.equal(usb.currentRemainingAt5V3AAfterLimeSdrsA, 1.8);
  assert.equal(usb.requires5AEMarkedUsbCCableWhenNegotiatedCurrentRequires, true);
  assert.equal(usb.auxiliaryBoardMayPowerLimeSdrsFrom40Pin5VRail, false);
  assert.equal(usb.limeSdrUsb3DataRoutedThroughAuxiliaryBoard, false);
  assert.match(readme, /separate USB-C power input and USB data\/host connectors/);
  assert.match(readme, /5 V \/ 3 A source is not accepted as sufficient/);
  assert.match(readme, /5 A e-marked USB-C cable/);
  assert.match(readme, /Do not\s+feed the two LimeSDR Minis from the auxiliary board's 40-pin header 5 V rail/);
});

test('external battery is excluded from mass and 2-hour sizing is not inferred from 12 Wh', () => {
  const { externalBattery: battery, conversion } = iface.board;
  assert.equal(battery.required, true);
  assert.equal(battery.massIncludedInFiveKgObjective, false);
  assert.equal(battery.nominalInterfaceV, 12);
  assert.equal(battery.installation, 'external battery pack; not installed inside the 5 kg station mass tally');
  assert.equal(battery.chemistry, 'LiFePO4 candidate; confirm exact delivered pack');
  assert.equal(battery.candidate.manufacturer, 'ECO-WORTHY');
  assert.equal(battery.candidate.product, '12 V 30 Ah LiFePO4');
  assert.equal(battery.candidate.variant, '40308275183822');
  assert.match(battery.candidate.status, /reference candidate only/);
  assert.match(battery.candidate.status, /vendor listing describes an internal BMS/);
  assert.equal(battery.candidate.nominalCapacityAh, 30);
  assert.equal(battery.candidate.nominalEnergyWhIfCapacityVerified, 360);
  assert.equal(battery.provisionalFullChargeV, 14.6);
  assert.match(battery.provisionalFullChargeVoltageStatus, /not confirmed/);
  assert.match(battery.fullChargeAndMinimumVoltageRange, /not verified/);
  const input = battery.inputConnector;
  assert.match(input.batterySideFamily, /Anderson Powerpole PP15\/30\/45/);
  assert.match(input.batterySideConnection, /exact crimp contacts selected/);
  assert.match(input.boardSideConnection, /separately selected rated PCB terminal connector/);
  assert.match(input.contactCurrentClass, /not selected/);
  assert.match(input.wireGauge, /not selected/);
  assert.match(input.exactConnectorPartNumbers, /not selected or source-verified/);
  assert.equal(input.connectorAndPolarityBenchCheckRequired, true);
  const fuses = battery.fuseAndDistribution;
  assert.deepEqual(fuses.batteryPositiveSequence, [
    'battery positive',
    'pack-adjacent main DC-rated fuse',
    'main service disconnect',
    'protected distribution',
  ]);
  assert.deepEqual(fuses.branchFuseLoads, [
    'CM5IO USB-C 5 V converter',
    'motor supply/converter',
    'each PA/RF supply branch as applicable',
  ]);
  assert.match(fuses.fuseAmpRatings, /not selected/);
  assert.match(fuses.maximumFuseRule, /lowest safe-current-rated/);
  assert.equal(fuses.bmsIsNotSubstituteForExternalFuses, true);
  assert.equal(fuses.dcRatedIndependentMotorEstopRequired, true);
  assert.ok(battery.protectionRequired.includes('reverse-polarity protection'));
  assert.ok(battery.protectionRequired.includes(
    'transient suppression coordinated with verified pack and converter ratings',
  ));
  assert.ok(battery.protectionRequired.includes('controlled inrush'));
  const emi = battery.emiPowerIntegrity;
  assert.match(emi.status, /routed digital candidates only/);
  assert.deepEqual(emi.batteryEntrySequence, [
    'Powerpole battery harness',
    'pack-adjacent main DC-rated fuse',
    'service disconnect',
    'reverse-polarity protection',
    'coordinated TVS or equivalent transient suppression',
    'controlled inrush',
    'optional DC-current-rated common-mode choke carrying positive and return',
    'optional exact-rated connector/header filter module only if specified and verified',
    'damped differential filter only if converter vendor guidance and impedance analysis support it',
    'fused separate CM5IO, motor, and applicable PA/RF branches',
    'local converter/load decoupling',
  ]);
  assert.equal(emi.commonModeChoke.bothSupplyAndReturnPassThroughCoupledWindings, true);
  assert.match(emi.commonModeChoke.exactPartNumber, /not selected/);
  assert.equal(emi.commonModeChoke.smallSignalOr300mABeadAllowedIn5ACm5ioPath, false);
  assert.equal(emi.connectorHeaderFilterModule.inventedFootprintAllowed, false);
  assert.equal(emi.differentialFilter.idealUndampedHighQFilterAllowed, false);
  assert.equal(emi.differentialFilter.requiresConverterVendorInputImpedanceAndFilterGuidance, true);
  assert.equal(emi.physicalSeparation.separateFusedCm5ioMotorAndPaRfBranches, true);
  assert.equal(emi.physicalSeparation.motorReturnThroughSensorOrAudioGroundAllowed, false);
  assert.ok(emi.verificationRequired.includes(
    'Linux stability under dual LimeSDR streaming, motor motion and radio transmission',
  ));
  assert.ok(emi.verificationRequired.includes(
    'SMA-port transmit spurs and harmonic measurement including 145 MHz third harmonic near 435 MHz',
  ));
  assert.equal(emi.dcInputFilterProvesRfComplianceOrDesense, false);
  assert.equal(battery.minimumNominalCapacityAhExclusive, 1);
  assert.equal(battery.minimumNominalEnergyWhExclusive, 12);
  assert.equal(battery.minimumCapacityEstablishesTwoHourAutonomy, false);
  assert.equal(battery.autonomyObjectiveHours, 2);
  assert.match(battery.sizing, /measured average battery-side W \* 2 h/);
  assert.ok(battery.protectionRequired.includes('chemistry-compatible pack protection or BMS'));
  assert.ok(battery.protectionRequired.includes('pack-adjacent fuse'));
  assert.equal(battery.inputVoltageAndCurrentRatingsFrozen, false);
  assert.equal(battery.motorAndLogicRailsFrozen, false);
  assert.equal(conversion.raw12VBatteryMayConnectToCm5ioUsbCPower, false);
  assert.equal(conversion.raw12VBatteryMayConnectToCm5io40Pin5V, false);
  assert.equal(conversion.preliminaryBatteryInputComponentRatingV, 30);
  assert.match(conversion.preliminaryInputRatingStatus, /stress screening only/);
  assert.match(conversion.preliminaryInputRatingStatus, /14\.6 V pack maximum is unverified/);
  assert.equal(conversion.auxiliaryLogicMustBeIsolatedFromBatteryInput, true);
  assert.match(conversion.auxiliaryLogicSupply, /5 V isolated regulator required/);
  assert.equal(conversion.inputTransientSuppressionAndInrushRequired, true);
  assert.match(conversion.cm5ioPowerConversion, /never raw battery to CM5IO/);
  assert.equal(conversion.limeSdrLoadMayUseAuxiliary40Pin5VRail, false);
  assert.equal(conversion.smaRfAndExternalK1AudioRetained, true);
  assert.equal(conversion.smaRfOrK1AudioRoutedThroughUsbCPower, false);
  assert.equal(conversion.allProtectionAndRegulatorRatingsFrozen, false);
  assert.match(readme, /external 12 V battery is\s+explicitly excluded from the 5 kg mass objective/);
  assert.match(readme, /12 Wh is only a minimum floor and does\s+\*\*not\*\*\s+establish two-hour runtime/);
  assert.match(readme, /Do not send raw 12 V to a USB-C\s+power pin, the 40-pin header, or the CM5/);
  assert.match(readme, /ECO-WORTHY 12 V 30 Ah LiFePO4 candidate/);
  assert.match(readme, /14\.6 V as provisional for component stress screening only/);
  assert.match(readme, /Anderson Powerpole 15\/30\/45 family/);
  assert.match(readme, /The pack\s+BMS is not a substitute for the external pack-adjacent fuse/);
  assert.match(readme, /Do not select arbitrary fuse amperages/);
  assert.match(readme, /battery positive -> pack-adjacent main DC fuse ->/);
  assert.match(readme, /separate\s+DC-rated branch fuses/);
  assert.match(readme, /a TVS by itself does not establish surge\s+immunity/i);
  assert.match(readme, /at\s+least 30 V/);
  assert.match(readme, /5 V logic rail must use an isolated regulator/);
  assert.match(readme, /independent.*DC-rated latching E-stop path/s);
  assert.match(readme, /existing SMA RF paths or separate external K1 audio\s+target/);
});

test('OS peripheral and boot contract prevents stale SPI0 aliases and auto-arm', () => {
  const boot = iface.softwareContract.bootSafety;
  assert.equal(boot.spiBus, 'SPI1');
  assert.equal(boot.i2cBus, 'I2C1');
  assert.equal(boot.gnssUart, 'UART0');
  assert.equal(boot.spi0SubstituteAllowed, false);
  assert.equal(boot.staleDeviceTreeOverlayMayReassignFrozenGpio, false);
  assert.equal(boot.verifyTargetImageOverlaysAndDeviceNodes, true);
  assert.equal(boot.motorArmOnColdBoot, 'OFF');
  assert.equal(boot.perAxisEnablesOnColdBoot, 'OFF');
  assert.equal(boot.pttRequestsOnColdBoot, 'OFF');
  assert.equal(boot.automaticMotorArmOnStartupAllowed, false);
  assert.equal(boot.automaticPttOnStartupAllowed, false);
  assert.deepEqual(boot.repeatFailOffInitializationAfter, [
    'reboot',
    'service restart',
    'GPIO provider recovery',
    'MCP23017 reset or power loss',
  ]);
  assert.equal(boot.softwareDoesNotReplaceExternalHardwareFailOff, true);
  assert.match(readme, /OS integration contract is SPI1, I2C1, and UART0/);
  assert.match(readme, /Do not enable or alias SPI0 in place of SPI1/);
  assert.match(readme, /No OS service,\s+overlay, or application may automatically arm motors or request transmit/);
});

test('audio remains unverified without invented K1 pinout or CPL placement', () => {
  const { audio } = iface;
  assert.equal(audio.onboard.target, 'built-in speaker and microphone through a USB codec');
  assert.equal(audio.onboard.codecCandidate.part, 'PCM2902C');
  assert.equal(audio.onboard.codecCandidate.status,
    'public candidate only; not selected or implemented on the PCB');
  assert.equal(audio.onboard.microphoneFrontEnd, 'not selected or designed');
  assert.equal(audio.onboard.speakerAmplifier, 'not selected or designed');
  assert.equal(audio.externalRadio.accessoryPinoutFrozen, false);
  assert.match(audio.externalRadio.target, /K1 dual 3\.5 mm \/ 2\.5 mm/);
  assert.match(audio.externalRadio.target, /UV-5R\/UV-82/);
  assert.equal(audio.externalRadio.separateJackDaughterboard, true);
  assert.equal(audio.externalRadio.jackPopulation, 'DNP pending exact accessory pinout and electrical qualification');
  assert.equal(audio.externalRadio.daughterboardHeader, 'not selected, pin-assigned, or verified');
  assert.match(audio.externalRadio.audioGroundPolicy, /do not bond an assumed BTL contact/);
  assert.equal(audio.externalRadio.btlContactPolicy, 'never assume the busy-tone lamp contact is ground');
  assert.equal(audio.assembly.dnpPartsInCpl, false);
  assert.match(audio.assembly.cplDesignators, /exactly match unique schematic\/PCB references/);
  assert.deepEqual(audio.assembly.jlcpcbCplColumns,
    ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation']);
  assert.equal(audio.assembly.generatedCplRows, 0);
  assert.equal(audio.assembly.generatedCplStatus,
    'not issued; no validated CM5 auxiliary PCB exists');
  assert.match(audio.assembly.pricing, /deferred until exact sourceable/);
  assert.match(readme, /never infer the\s+BTL/i);
  assert.match(readme, /PCM2902C is a public codec candidate/i);
  assert.match(readme, /CPL Designator\s+values must be the exact unique reference designators/i);
  assert.match(readme, /Designator,Mid X,Mid Y,Layer,Rotation/);
});

test('each axis maps limits, encoder channel, SPI select, fault and hardware enable', () => {
  const { axes } = iface.softwareContract.rotor;
  assert.deepEqual(axes.AZ, {
    spiChipSelect: 'SPI1 CS0 / BCM18 / physical pin 12',
    encoderMuxChannel: 0,
    minimumLimitBcm: 4,
    maximumLimitBcm: 5,
    driverFaultBcm: 24,
    enableRequest: 'MCP23017 GPA0',
  });
  assert.deepEqual(axes.EL, {
    spiChipSelect: 'SPI1 CS1 / BCM17 / physical pin 11',
    encoderMuxChannel: 1,
    minimumLimitBcm: 6,
    maximumLimitBcm: 7,
    driverFaultBcm: 25,
    enableRequest: 'MCP23017 GPA1',
  });
  assert.deepEqual(axes.POL, {
    spiChipSelect: 'SPI1 CS2 / BCM16 / physical pin 36',
    encoderMuxChannel: 2,
    minimumLimitBcm: 8,
    maximumLimitBcm: 9,
    driverFaultBcm: 26,
    enableRequest: 'MCP23017 GPA2',
  });
});

test('GPIO direction and inactive startup levels are explicit for outputs', () => {
  for (const pin of iface.gpio) {
    assert.ok(pin.direction, `GPIO${pin.bcm} direction`);
    if (pin.direction === 'output') assert.ok(pin.safeLevel, `GPIO${pin.bcm} safe level`);
  }
  assert.deepEqual(
    iface.gpio.filter((pin) => [11, 12, 16, 17, 18, 22, 23].includes(pin.bcm))
      .map(({ bcm, safeLevel }) => [bcm, safeLevel]),
    [[11, 'LOW'], [12, 'LOW'], [16, 'HIGH'], [17, 'HIGH'], [18, 'HIGH'], [22, 'LOW'], [23, 'LOW']],
  );
});
