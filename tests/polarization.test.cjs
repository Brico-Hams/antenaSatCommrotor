const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { parseCsv } = require('../scripts/component-catalog.cjs');
const validateStl = require('./mechanical-stl.cjs');
const design = require('../calc/polarization.json');
const report = require('../scripts/polarization-report.cjs').calculate(design);
const root = path.join(__dirname, '..');

test('POL uses one 20:100 GT2 stage without changing 25:1 BASE axes', () => {
  assert.equal(report.transmission.reduction, 5);
  assert.equal(report.transmission.commandedStepsPerRev, 16000);
  assert.equal(report.transmission.commandedMicrostepDegrees, 0.0225);
  assert.ok(Math.abs(report.transmission.centerDistanceMm - 60.563) < 0.01);
  assert.ok(Math.abs(report.transmission.calculatedBeltLengthMm - 252) < 1e-7);
  assert.ok(report.transmission.smallPulleyEngagedTeeth > 6);
  assert.ok(report.transmission.smallPulleyEnvelopeClearanceMm > 19);
  const base = fs.readFileSync(path.join(root, 'cad', 'belt_station.scad'), 'utf8');
  assert.match(base, /assert\(small_teeth==20&&large_teeth==100\)/);
  assert.equal((100 / 20) ** 2, 25);
  assert.equal(200 * 16 * 25, 80000);
});

test('NC limits, command limits, and mechanical stops have ordered margins', () => {
  assert.deepEqual(report.travel.hardStopDegrees, [-90, 90]);
  assert.equal(report.travel.hardStopAnglesAreCandidateTargetsNotValidated, true);
  assert.equal(report.travel.firstArticleStopAndSwitchTestingRequired, true);
  assert.deepEqual(report.travel.normallyClosedSwitchTripDegrees, [-85, 85]);
  assert.deepEqual(report.travel.commandedSoftLimitDegrees, [-80, 80]);
  assert.equal(report.travel.stopPinRadiusMm, 36);
  assert.equal(report.travel.camReachMm, 34);
  assert.equal(report.travel.idealTipToPinSurfaceClearanceAtHardStopMm, 0);
  assert.equal(report.travel.noContinuousRotation, true);
  assert.equal(report.travel.noSlipRing, true);
  assert.ok(Math.abs(report.loadExample.axes.polarization.inertiaKgM2 - 0.04545) < 1e-12);
  assert.ok(Math.abs(report.loadExample.axes.polarization.safetyFactoredIllustrativeMomentNm -
    0.463644) < 1e-6);
  assert.ok(Math.abs(report.loadExample.axes.elevation.safetyFactoredIllustrativeMomentNm -
    1.7055) < 1e-12);
  assert.ok(Math.abs(report.loadExample.axes.azimuth.safetyFactoredIllustrativeMomentNm -
    1.4112) < 1e-12);
  assert.ok(Math.abs(report.loadExample.counterbalance.exampleCounterweightMassKg - 0.15) < 1e-12);
});

test('controller-facing POL mechanics match the provisional design and load gates', () => {
  for (const file of [
    'docs/CM5-ROTOR.md',
    'docs/en/CM5-ROTOR.md'
  ]) {
    const doc = fs.readFileSync(path.join(root, file), 'utf8');
    assert.match(doc, /20:100 single belt stage/);
    assert.match(doc, /soft(?:ware)? bounds are \+\/-80 degrees/);
    assert.match(doc, /NC switch trip targets are \+\/-85 degrees/);
    assert.match(doc, /candidate\s+physical hard-stop travel of \+\/-90 degrees/);
    assert.match(doc, /measure the assembled[\s\S]*axis inertia/);
  }
  const huDoc = fs.readFileSync(path.join(root, 'docs', 'hu', 'CM5-ROTOR.md'), 'utf8');
  assert.match(huDoc, /20:100/);
  assert.match(huDoc, /-80 és \+80 fok/);
  assert.match(huDoc, /\+\/-85 fok/);
  assert.match(huDoc, /\+\/-90 fok/);
});

test('operational station mass uses the authoritative limit and accounts for additions', () => {
  assert.equal(report.massBudget.existingBudgetIncludesExistingAzElMotors, true);
  assert.equal(report.massBudget.existingBudgetIncludesAntenna, true);
  assert.equal(report.massBudget.historicalBudgetExcludedRadioAndTripod, true);
  assert.equal(report.massBudget.historicalBudgetIncludedBatteryAllowance, true);
  assert.equal(report.massBudget.historicalIncludedBatteryAllowanceKg, null);
  assert.equal(report.massBudget.historicalBatteryAllowanceReconciled, false);
  assert.equal(report.massBudget.historicalBatteryReconciledBudgetKg, null);
  assert.equal(report.massBudget.existingBudgetIncludesBatteryHistorically, true);
  assert.equal(report.massBudget.existingBudgetIncludesLegacyCablesAndConnectors, true);
  assert.equal(report.massBudget.stationMassHeadroomMayBeReportedOnlyAfterHistoricalBatteryAndCurrentInventoryAreReconciled,
    true);
  assert.equal(report.massBudget.historicalUnadjustedHeadroomIsNotUsableBudget, true);
  assert.deepEqual(report.massBudget.historicalUnadjustedHeadroomToMaximumKg, [1.87, 1.8]);
  assert.deepEqual(report.massBudget.operationalMassScope, [
    'antenna',
    'AZ, EL, and POL rotor and motors',
    'radio',
    'SBC',
    'enclosure',
    'CM5 module, official carrier, and selected thermal solution',
    'two replaceable LimeSDR Mini units and their mounts',
    'SDR power amplifier(s), filters, shields, mounts, and RF hardware',
    'auxiliary station electronics, control/interface hardware, mounts, and fasteners',
    'station-side power input, conversion, protection, and distribution; external battery pack/BMS excluded',
    'Powerpole input connector pair and master battery-to-station wire pair',
    'one positive-line master fuse/holder and three separately fused branch harnesses, fuse holders, fuses and branch wires',
    'optional station-side cable strain-relief plate, ties, and mounting fasteners if fitted',
    'all operational cables and connectors',
    'tripod',
    'three axis encoders and encoder brackets',
    'fixed-base remote compass/IMU and mount',
    'stationary GPS receiver, antenna, and mount',
    'SMA bulkhead connector and mount',
    'POL-axis coax trunk and service loop',
    'four individual per-band circular-feed coax assemblies with connectors',
    'all other RF SMA connectors and adapters'
  ]);
  assert.equal(report.massBudget.newPolSubsystemMassKg, null);
  assert.equal(report.massBudget.stationSidePowerHardwareMassKg, null);
  assert.equal(report.massBudget.powerpoleInputConnectorPairAndContactsMassKg, null);
  assert.equal(report.massBudget.powerpoleInputConnectorPairMassIncludesBothMatingHalves, true);
  assert.equal(report.massBudget.powerpoleInputConnectorsAndHarnessIncludedInStationCap, true);
  assert.equal(report.massBudget.masterBatteryInputWirePairMassKg, null);
  assert.equal(report.massBudget.masterPositiveFuseAndHolderAssemblyMassKg, null);
  assert.deepEqual(report.massBudget.branchFuseAndHolderMassKg, {
    cm5Io5vConverter: null,
    motorAndEmergencyStopPath: null,
    rfPowerAmplifier: null
  });
  assert.deepEqual(report.massBudget.branchHarnessWireAndConnectorMassKg, {
    cm5Io5vConverter: null,
    motorAndEmergencyStopPath: null,
    rfPowerAmplifier: null
  });
  assert.equal(report.massBudget.separatelyFusedBranchCount, 3);
  assert.equal(report.massBudget.branchFuseRatingsSelected, false);
  assert.equal(report.massBudget.powerHarnessStrainReliefPlateMassKg, null);
  assert.equal(report.massBudget.powerHarnessStrainReliefPlateOptional, true);
  assert.equal(report.massBudget.powerpolePanelHousingBracketSelected, false);
  assert.equal(report.massBudget.powerpolePanelHousingOutlineVerified, false);
  assert.deepEqual(report.massBudget.computeAndSdr, {
    computeModule: 'Raspberry Pi Compute Module 5 (CM5)',
    computeCarrier: 'official CM5IO carrier board; exact configuration and any required mechanical changes TBD',
    thermalSolution: 'CM5-compatible heatsink/cooling solution; exact parts and mechanical changes TBD',
    softwareControllerHardware: 'CM5 only; no ESP32',
    sdrCount: 2,
    sdr: 'two replaceable LimeSDR Mini units',
    limeSdrMiniEnvelopeMm: {
      length: 69,
      width: 31.4,
      height: null,
      source: 'user-provided plan reference; verify exact LimeSDR Mini revision',
      measuredMassKg: null,
      isMassOrFitGuarantee: false
    },
    existingEnclosureFitVerified: false,
    paAndFiltersSelection: 'TBD; include installed amplifiers, filters, shields, mounts and hardware in weighed station'
  });
  assert.equal(report.massBudget.cm5ComputeModuleMassKg, null);
  assert.equal(report.massBudget.officialCm5CarrierBoardMassKg, null);
  assert.equal(report.massBudget.cm5ThermalSolutionMassKg, null);
  assert.equal(report.massBudget.cm5AndCarrierMountHardwareMassKg, null);
  assert.equal(report.massBudget.limeSdrMiniUnitsMassKg, null);
  assert.equal(report.massBudget.limeSdrMiniMountsMassKg, null);
  assert.equal(report.massBudget.limeSdrMiniQuantity, 2);
  assert.equal(report.massBudget.sdrPowerAmplifiersMassKg, null);
  assert.equal(report.massBudget.sdrFiltersAndShieldsMassKg, null);
  assert.equal(report.massBudget.computeSdrEnclosureMassKg, null);
  assert.equal(report.massBudget.otherRadioHardwareMassKg, null);
  assert.equal(report.massBudget.auxiliaryStationHardwareMassKg, null);
  assert.equal(report.massBudget.tripodMassKg, null);
  assert.equal(report.massBudget.stationTotalIncludesTripod, true);
  assert.equal(report.massBudget.externalBatteryPackAndBmsCarriedMassKg, null);
  assert.equal(report.massBudget.externalBatteryMustHaveMeasuredCarriedMassBeforeTransportTotal, true);
  assert.equal(report.massBudget.externalBatteryPackAndBmsExcludedFromStationMassCap, true);
  assert.equal(report.massBudget.externalBatteryChargerMassKg, null);
  assert.equal(report.massBudget.externalBatteryChargerIncludedInStationMassIfCarried, true);
  assert.equal(report.massBudget.totalTransportedMassKg, null);
  assert.equal(report.massBudget.otherOperationalCablesAndConnectorsExcludingSensorAndRfKg, null);
  assert.deepEqual(report.massBudget.addedSensorMassesKg, {
    azimuthEncoder: null,
    elevationEncoder: null,
    polarizationEncoder: null,
    threeEncoderBrackets: null,
    remoteFixedBaseCompassImu: null,
    compassPlaceholderMount: null,
    stationaryGpsReceiver: null,
    stationaryGpsAntenna: null,
    gpsAntennaMount: null
  });
  assert.equal(report.massBudget.sensorCablesAndConnectorsKg, null);
  assert.equal(report.massBudget.compassMountDimensionsMm, null);
  assert.equal(report.massBudget.compassImuModuleSelected, false);
  assert.equal(report.massBudget.gpsReceiverModuleSelected, false);
  assert.equal(report.massBudget.gpsAntennaMountDimensionsMm, null);
  assert.equal(report.massBudget.gpsAntennaStationaryWithSkyView, true);
  assert.equal(report.massBudget.compassIsEncoder, false);
  assert.equal(report.massBudget.smaBulkheadConnectorMassKg, null);
  assert.equal(report.massBudget.coaxBulkheadInterfacePlateMassKg, null);
  assert.equal(report.massBudget.axisCoaxServiceLoopAssemblyMassKg, null);
  assert.equal(report.massBudget.coaxBulkheadInterfacePlateMassKg, null);
  assert.deepEqual(report.massBudget.rfFeedBranchCoaxMassKg, {
    '145MHzOrthogonalFeedA': null,
    '145MHzOrthogonalFeedB': null,
    '435MHzOrthogonalFeedA': null,
    '435MHzOrthogonalFeedB': null
  });
  assert.equal(report.massBudget.rfFeedBranchCoaxAssemblyCount, 4);
  assert.equal(report.massBudget.remainingSmaRfConnectorsAndAdaptersMassKg, null);
  assert.equal(report.massBudget.completeStationMassKg, null);
  assert.equal(report.massBudget.stationMassReconciliationFormula,
    'historical_two_axis_budget_kg - measured_historical_battery_allowance_kg + CM5_official_CM5IO_thermal_mounts_kg + two_LimeSDR_Mini_units_and_mounts_kg + radio_PAs_filters_enclosure_auxiliary_hardware_kg + new_POL_kg + tripod_kg + sensors_mounts_kg + station_power_and_all_station_cables_connectors_kg');
  assert.equal(report.massBudget.maximumOperationalStationMassKg, 5);
  assert.equal(report.massBudget.engineeringTargetOperationalStationMassKg, 4.5);
  assert.equal(report.massBudget.preferredMeasuredReserveKg, 0.5);
  assert.equal(report.massBudget.remainingToMaximumBeforeUnknownAdditionsKg, null);
  assert.equal(report.massBudget.remainingToEngineeringTargetBeforeUnknownAdditionsKg, null);
  assert.equal(report.massBudget.stationTotalFormula,
    '(historical_two_axis_budget_kg - measured_historical_battery_allowance_kg) + CM5_module_official_CM5IO_carrier_thermal_mounts_two_LimeSDR_Mini_units_enclosure_radio_PAs_filters_and_auxiliary_hardware_kg + new_POL_subsystem_kg + tripod_kg + sensors_mounts_station_side_power_and_all_station_cables_connectors_kg');
  assert.equal(report.massBudget.transportedTotalFormula,
    'complete_station_mass_kg + external_battery_pack_and_BMS_mass_kg');
  assert.match(report.massBudget.operationalStationTotalFormula,
    /historical_two_axis_budget_kg - measured_historical_battery_allowance_kg.*CM5_module_official_CM5IO_carrier_thermal_and_mounts_kg.*two_LimeSDR_Mini_units_and_mounts_kg.*tripod_kg.*four_individual_rf_feed_branch_coax_assemblies_kg/);
  assert.equal(report.externalPower.nominalVoltageV, 12);
  assert.equal(report.externalPower.smallPackCapacityAhExampleOnly, 1);
  assert.equal(report.externalPower.smallPackNominalEnergyWhExampleOnly, 12);
  assert.equal(report.externalPower.targetAutonomyHours, 2);
  assert.equal(report.externalPower.smallPackIdealAveragePowerWForTargetAutonomy, 6);
  assert.equal(report.externalPower.externalPackExcludedFromStationMassCap, true);
  assert.equal(report.externalPower.externalPackMassKg, null);
  assert.equal(report.externalPower.largerExternalPackSelected, false);
  assert.equal(report.externalPower.twoHourAutonomyMeasured, false);
  assert.equal(report.externalPower.idealEnergyInsufficientForTwoHourStationTarget, true);
  assert.equal(report.externalPower.oneAhPackInsufficientForTwoHourStationTarget, true);
  assert.equal(report.massBudget.measured, false);
  assert.match(report.massBudget.status,
    /reconcile the battery allowance and weigh the complete current station inventory before calculating station total/);
  assert.equal(report.addedPolarizationHardwareLoadContribution.totalCannotBeRecalculatedUntilWeighedAndMeasured,
    true);
  assert.match(report.addedPolarizationHardwareLoadContribution.azimuthInertiaKgM2Formula, /m_POL/);
});

test('BASE mechanical interfaces are called from their original definitions', () => {
  const cad = fs.readFileSync(path.join(root, 'cad', 'polarization_station.scad'), 'utf8');
  const mechanical = fs.readFileSync(path.join(root, 'cad', 'mechanical.scad'), 'utf8');
  assert.match(cad, /use <mechanical\.scad>/);
  assert.match(cad, /pol_part = 0/);
  assert.match(cad, /pol_clamp_y = 0/);
  assert.match(cad, /pol_clamp_z = 0/);
  assert.match(cad, /pol_clamp_y\+35-pol_axis_y/);
  assert.match(cad, /pol_clamp_z\+24-pol_axis_z/);
  assert.match(cad, /output_flange\(\)/);
  assert.match(cad, /saddle\(20\)/);
  assert.match(cad, /bearing\(8,22,7\)/);
  assert.match(cad, /pol_sma_panel_hole_diameter = 6\.5/);
  assert.match(cad, /pol_sma_panel_thickness = 3/);
  assert.match(cad, /pol_coax_strain_hole_diameter = 3\.4/);
  assert.match(cad, /pol_coax_strain_hole_spacing = 10/);
  assert.match(cad, /pol_coax_plate_width = 30/);
  assert.match(cad, /pol_coax_plate_height = 22/);
  assert.match(cad, /pol_part==9\) pol_coax_interface_2d/);
  assert.match(cad, /module pol_power_harness_strain_relief_2d\(\)/);
  assert.match(cad, /square\(\[48,84\],center=true\)/);
  assert.match(cad, /for \(x=\[-19,19\],y=\[-38,38\]\)/);
  assert.match(cad, /for \(y=\[-24,-8,8,24\],x=\[-6,6\]\)/);
  assert.match(cad, /pol_part==10\) pol_power_harness_strain_relief\(\)/);
  assert.match(mechanical, /cylinder\(d=60,h=6\)/);
  assert.match(mechanical, /translate\(\[0,0,-1\]\) cylinder\(d=10\+fit,h=22\)/);
  assert.match(mechanical, /cylinder\(d=22,h=26\)/);
  assert.match(mechanical, /cylinder\(d=4\.5,h=26\)/);
  assert.equal(design.mechanics.rf.independentHandednessSwitchRequired, true);
  assert.deepEqual(design.mechanics.rf.hybridBandsMHz, [145, 435]);
  assert.equal(design.mechanics.rf.transmitInterlockRequired, true);
  assert.equal(design.mechanics.rf.switchTopologyValidated, false);
  assert.match(design.mechanics.rf.handednessSwitchingConcept, /DPDT/);
  assert.match(design.mechanics.rf.commonFeedConcept, /diplexer/);
  assert.match(design.mechanics.rf.connectorStandard, /50-ohm standard-polarity SMA/);
  assert.match(design.mechanics.rf.connectorStandard, /no RP-SMA, BNC, or N-type/);
  assert.equal(design.mechanics.rf.audioAccessoryConnectorsUnchanged, true);
  assert.equal(design.mechanics.rf.audioConnectorsAreNotSma, true);
  assert.equal(design.mechanics.rf.smaBulkheadInterface.panelClearanceHoleDiameterMm, 6.5);
  assert.equal(design.mechanics.rf.smaBulkheadInterface.panelThicknessMm, 3);
  assert.equal(design.mechanics.rf.smaBulkheadInterface.strainReliefHoleDiameterMm, 3.4);
  assert.equal(design.mechanics.rf.smaBulkheadInterface.strainReliefHoleSpacingMm, 10);
  assert.equal(design.mechanics.rf.smaBulkheadInterface.dimensionsAreDesignInterfaceNotMeasuredConnector,
    true);
});

test('exported polarization print parts are solid, manifold and nonempty', () => {
  for (const name of [
    'polarization-frame.stl',
    'polarization-rotor-carrier.stl',
    'polarization-bearing-retainer.stl',
    'polarization-limit-cam.stl',
    'polarization-limit-bracket.stl',
    'polarization-boom-clamp.stl',
    'polarization-power-strain-relief.stl'
  ]) {
    const mesh = validateStl(path.join(root, 'cad', name));
    assert.ok(mesh.triangles > 100, `${name} should be a meaningful rendered part`);
    assert.equal(mesh.components, 1, `${name} should be one connected solid`);
    if (name === 'polarization-power-strain-relief.stl') {
      assert.ok(mesh.volume > 11000 && mesh.volume < 12500,
        `${name} should retain the specified 48 x 84 x 3 mm plate with holes`);
    }
  }
});

test('metal templates and BOM identify unresolved manufacturing and mass inputs', () => {
  for (const name of [
    'polarization-motor-plate.dxf',
    'polarization-cheek-plate.dxf',
    'polarization-coax-interface.dxf'
  ]) {
    const contents = fs.readFileSync(path.join(root, 'cad', name), 'utf8');
    assert.ok(contents.length > 100, `${name} must contain real DXF geometry`);
  }
  const bom = fs.readFileSync(path.join(root, 'bom', 'polarization.csv'), 'utf8');
  assert.match(bom, /Measured mass[\s\S]*?TBD \(not weighed\)/i);
  assert.match(bom, /RF RHCP\/LHCP handedness DPDT transfer switch/i);
  assert.match(bom, /torque.*TBD/i);
  assert.match(bom, /Cost[\s\S]*?TBD \(not quoted\)/i);
  assert.match(bom, /Encoder mounting brackets,3/);
  assert.match(bom, /Remote fixed-base compass\/IMU/);
  assert.match(bom, /Stationary GPS antenna/);
  assert.match(bom, /GPS antenna placeholder mount/);
  assert.match(bom, /Sensor cabling and connectors/);
  assert.match(bom, /COM-01,Compute module,1,Raspberry Pi Compute Module 5/);
  assert.match(bom, /COM-02,CM5 carrier board,1,Official CM5IO carrier board/);
  assert.match(bom, /COM-03,CM5 thermal solution/);
  assert.match(bom, /PWR-01,External battery pack and BMS/);
  assert.match(bom, /separate carried mass/);
  assert.match(bom, /PWR-02,External battery charger/);
  assert.match(bom, /PWR-03,Station-side power conversion and protection/);
  assert.match(bom, /PWR-04,Powerpole input connector pair and contacts/);
  const sdr = parseCsv(bom).find((row) => row.ID === 'SDR-01');
  assert.equal(sdr.Component, 'LimeSDR Mini');
  assert.equal(sdr.Quantity, '2');
  assert.match(sdr['Material or specification'], /^Two replaceable LimeSDR Mini units/);
  assert.match(bom, /SDR-02,LimeSDR Mini mounts,2/);
  assert.match(bom, /COM-06,Auxiliary station electronics/);
  assert.match(bom, /RF-30,SDR power amplifier/);
  assert.match(bom, /RF-31,SDR filters/);
  assert.match(bom, /no ESP32/);
  assert.match(bom, /No claim of fit in the existing box/);
  assert.match(bom, /POL-26,SMA bulkhead jack/);
  assert.match(bom, /POL-27,Coax bulkhead and strain-relief interface plate/);
  assert.match(bom, /SMA bulkhead jack/);
  assert.match(bom, /no RP-SMA, BNC, or N-type/);
  for (const id of ['RF-26', 'RF-27', 'RF-28', 'RF-29']) {
    assert.match(bom, new RegExp(`^${id},`, 'm'), `${id} must have a separately weighed feed coax`);
  }
  for (const id of [
    'PWR-04', 'PWR-05', 'PWR-06', 'PWR-07', 'PWR-08', 'PWR-09',
    'PWR-10', 'PWR-11', 'PWR-12', 'PWR-13', 'PWR-14'
  ]) {
    assert.match(bom, new RegExp(`^${id},`, 'm'), `${id} must have its own mass accounting`);
  }
  for (const branch of ['CM5IO converter', 'Motor and emergency-stop', 'RF PA']) {
    assert.match(bom, new RegExp(`${branch} branch wiring`));
  }
  assert.match(bom, /Powerpole connector-housing panel bracket[\s\S]*?exact Powerpole housing part and manufacturer drawing are verified/);
  assert.match(bom, /generic power-harness strain-relief plate[\s\S]*?OpenSCAD 2021\.01[\s\S]*?checked as a single closed oriented 3132-triangle mesh/);
  assert.match(bom, /not a Powerpole connector mount/);
  assert.match(bom, /Powerpole input connector pair and contacts[\s\S]*?Include both mating halves, housings and contacts in station mass/);
  assert.match(bom, /Positive master fuse holder and fuse[\s\S]*?Include holder, cover, fuse, terminals and installed hardware in the 5 kg station mass/);
  assert.match(bom, /Baofeng\/audio\/accessory jacks are outside this RF connector rule/);
});
