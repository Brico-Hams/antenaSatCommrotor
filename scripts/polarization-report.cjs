const fs = require('node:fs');
const path = require('node:path');

function beltPathLength(centerMm, smallRadiusMm, largeRadiusMm) {
  const radiusDifferenceMm = largeRadiusMm - smallRadiusMm;
  const tangentAngleRad = Math.asin(radiusDifferenceMm / centerMm);
  return 2 * Math.sqrt(centerMm ** 2 - radiusDifferenceMm ** 2) +
    Math.PI * (largeRadiusMm + smallRadiusMm) +
    2 * tangentAngleRad * radiusDifferenceMm;
}

function solveBeltCenter(beltLengthMm, smallRadiusMm, largeRadiusMm) {
  let low = largeRadiusMm - smallRadiusMm + 0.1;
  let high = beltLengthMm;
  for (let iteration = 0; iteration < 80; iteration += 1) {
    const centerMm = (low + high) / 2;
    if (beltPathLength(centerMm, smallRadiusMm, largeRadiusMm) > beltLengthMm) {
      high = centerMm;
    } else {
      low = centerMm;
    }
  }
  return (low + high) / 2;
}

function calculate(design) {
  const { mechanics, examples, massBudget, addedAxisLoadInputs } = design;
  const reduction = mechanics.drivenPulleyTeeth / mechanics.driverPulleyTeeth;
  const commandedStepsPerRev =
    mechanics.motorStepsPerRevolution * mechanics.microsteps * reduction;
  const smallRadiusMm = mechanics.driverPulleyTeeth * mechanics.beltPitchMm / (2 * Math.PI);
  const largeRadiusMm = mechanics.drivenPulleyTeeth * mechanics.beltPitchMm / (2 * Math.PI);
  const centerMm = solveBeltCenter(mechanics.beltLengthMm, smallRadiusMm, largeRadiusMm);
  const smallWrapRad = Math.PI - 2 * Math.asin((largeRadiusMm - smallRadiusMm) / centerMm);
  const engagedSmallPulleyTeeth = mechanics.driverPulleyTeeth * smallWrapRad / (2 * Math.PI);
  const windForceN = 0.5 * examples.airDensityKgM3Assumed *
    examples.dragCoefficientAssumed * examples.projectedAreaM2ExampleOnly *
    examples.windMpsCalculationOnly ** 2;
  const antennaWeightN = examples.antennaMassKgExampleOnly * examples.gravityMps2;
  const gravityMomentNm = antennaWeightN * examples.antennaCgOffsetMExampleOnly;
  const rollWindMomentNm = windForceN * examples.rollPressureCenterOffsetMExampleOnly;
  const pointingWindMomentNm = windForceN * examples.pointingWindArmMExampleOnly;
  const azimuthMomentOfInertiaKgM2 =
    examples.antennaMassKgExampleOnly * examples.azimuthCgRadiusMExampleOnly ** 2;
  const elevationMomentOfInertiaKgM2 =
    examples.antennaMassKgExampleOnly *
    (examples.antennaRadiusOfGyrationMExampleOnly ** 2 +
      examples.antennaCgOffsetMExampleOnly ** 2);
  const polarizationMomentOfInertiaKgM2 = elevationMomentOfInertiaKgM2;
  const alpha = examples.angularAccelerationRadS2ExampleOnly;
  const safetyFactor = examples.safetyFactorIllustrative;
  const externalBatteryNominalEnergyWh =
    design.externalPower.nominalVoltageV * design.externalPower.smallPackCapacityAhExampleOnly;
  const externalBatteryIdealAveragePowerW =
    externalBatteryNominalEnergyWh / design.externalPower.targetAutonomyHours;

  return {
    status: design.status,
    warnings: [
      'Illustrative antenna-only loads; no field torque, motor capability, or safety qualification is claimed.',
      'Mount, motor, belt, shaft, cable, counterweight, and switch masses are unmeasured or unspecified.',
      'Pointing-axis totals require measured complete-axis mass, center of gravity, and inertia.'
    ],
    transmission: {
      ratio: `${mechanics.drivenPulleyTeeth}:${mechanics.driverPulleyTeeth}`,
      reduction,
      commandedStepsPerRev,
      commandedMicrostepDegrees: 360 / commandedStepsPerRev,
      beltLengthMm: mechanics.beltLengthMm,
      centerDistanceMm: centerMm,
      calculatedBeltLengthMm: beltPathLength(centerMm, smallRadiusMm, largeRadiusMm),
      smallPulleyWrapDegrees: smallWrapRad * 180 / Math.PI,
      smallPulleyEngagedTeeth: engagedSmallPulleyTeeth,
      smallPulleyEnvelopeClearanceMm: centerMm -
        (smallRadiusMm + 1.5) - (largeRadiusMm + 1.5),
      stepResolutionWarning: 'Command increment is not positioning accuracy.'
    },
    travel: {
      hardStopDegrees: mechanics.hardStopDegrees,
      hardStopAnglesAreCandidateTargetsNotValidated:
        mechanics.hardStopAnglesAreCandidateTargetsNotValidated,
      firstArticleStopAndSwitchTestingRequired:
        mechanics.firstArticleStopAndSwitchTestingRequired,
      normallyClosedSwitchTripDegrees: mechanics.normallyClosedSwitchTripDegrees,
      commandedSoftLimitDegrees: mechanics.commandedSoftLimitDegrees,
      stopPinRadiusMm: mechanics.stopPinRadiusMm,
      camReachMm: mechanics.camReachMm,
      stopPinDiameterMm: 4,
      camToStopPinCenterClearanceMm: mechanics.stopPinRadiusMm - mechanics.camReachMm,
      idealTipToPinSurfaceClearanceAtHardStopMm:
        mechanics.stopPinRadiusMm - mechanics.camReachMm - 2,
      noContinuousRotation: true,
      noSlipRing: true
    },
    loadExample: {
      windForceN,
      antennaWeightN,
      axes: {
        polarization: {
          gravityMomentNm: gravityMomentNm,
          windMomentNm: rollWindMomentNm,
          safetyFactoredIllustrativeMomentNm:
            safetyFactor * (gravityMomentNm + rollWindMomentNm),
          inertiaKgM2: polarizationMomentOfInertiaKgM2,
          inertialMomentAtExampleAccelerationNm: polarizationMomentOfInertiaKgM2 * alpha,
          inertiaAssumption: 'Antenna-only radius of gyration plus parallel-axis CG offset.'
        },
        elevation: {
          gravityMomentNm,
          windMomentNm: pointingWindMomentNm,
          safetyFactoredIllustrativeMomentNm:
            safetyFactor * (gravityMomentNm + pointingWindMomentNm),
          inertiaKgM2: elevationMomentOfInertiaKgM2,
          inertialMomentAtExampleAccelerationNm: elevationMomentOfInertiaKgM2 * alpha,
          omittedMovingHardware: true
        },
        azimuth: {
          gravityMomentNm: 0,
          windMomentNm: pointingWindMomentNm,
          safetyFactoredIllustrativeMomentNm: safetyFactor * pointingWindMomentNm,
          inertiaKgM2: azimuthMomentOfInertiaKgM2,
          inertialMomentAtExampleAccelerationNm: azimuthMomentOfInertiaKgM2 * alpha,
          inertiaAssumption: 'Antenna treated as a point mass at the example radial CG offset; lower-bound illustration only.',
          omittedMovingHardware: true
        }
      },
      counterbalance: {
        exampleCounterweightMassKg:
          examples.antennaMassKgExampleOnly * examples.antennaCgOffsetMExampleOnly /
          examples.counterweightRadiusMExampleOnly,
        counterweightRadiusM: examples.counterweightRadiusMExampleOnly,
        warning: 'Illustrative static balance only; mass is not in the CAD or mass budget.'
      },
      assumptions: [
        'The example uses the inherited 0.5 kg antenna, 0.06 m2 projected area, and 8 m/s calculation-only wind case.',
        'POL gravity moment uses the full 30 mm CG offset as a worst-orientation example; actual gravity torque varies with pointing.',
        'POL wind moment uses a 30 mm center-of-pressure eccentricity; pointing wind moment uses the separate 250 mm arm.',
        'AZ gravity moment is zero only for an ideal vertical yaw axis; the AZ inertia ignores the array distributed inertia.',
        'Wind speed is not an approved operating limit. Motor dynamic torque and complete-axis inertia remain TBD.'
      ]
    },
    addedPolarizationHardwareLoadContribution: {
      measuredInputs: addedAxisLoadInputs,
      elevationGravityMomentNmFormula: 'm_POL_kg * 9.81 * perpendicular_CG_offset_from_EL_axis_m',
      elevationInertiaKgM2Formula:
        'I_centroid_about_EL_axis_kgm2 + m_POL_kg * perpendicular_CG_offset_from_EL_axis_m^2',
      azimuthInertiaKgM2Formula:
        'I_centroid_about_AZ_axis_kgm2 + m_POL_kg * perpendicular_CG_offset_from_AZ_axis_m^2',
      azimuthWindTorqueNmFormula:
        '0.5 * 1.225 * Cd_POL * area_POL_m2 * wind_mps^2 * pressure_center_arm_m',
      totalCannotBeRecalculatedUntilWeighedAndMeasured:
        Object.values(addedAxisLoadInputs).some(value => value === null),
      warning: 'Do not add a third-motor torque or mass estimate: the motor and POL assembly have not been selected or weighed.'
    },
    externalPower: {
      ...design.externalPower,
      smallPackNominalEnergyWhExampleOnly: externalBatteryNominalEnergyWh,
      smallPackIdealAveragePowerWForTargetAutonomy: externalBatteryIdealAveragePowerW,
      idealEnergyInsufficientForTwoHourStationTarget: true,
      oneAhPackInsufficientForTwoHourStationTarget: true,
      externalPackMassKg: massBudget.externalBatteryPackAndBmsCarriedMassKg,
      chargerMassKg: massBudget.externalBatteryChargerMassKg,
      packAndBmsExcludedFromStationMassCap:
        massBudget.externalBatteryPackAndBmsExcludedFromStationMassCap,
      warning: '12 V x 1 Ah provides 12 Wh nominal, only 6 W ideal average over 2 h before losses; do not claim the CM5/SDR station can run for 2 h on this example pack.'
    },
    massBudget: {
      existingTwoAxisConditionalBudgetKg: massBudget.existingTwoAxisBudgetKgConditional,
      historicalBudgetExcludedRadioAndTripod: massBudget.historicalBudgetExcludedRadioAndTripod,
      historicalBudgetIncludedBatteryAllowance: massBudget.historicalBudgetIncludedBatteryAllowance,
      historicalIncludedBatteryAllowanceKg: massBudget.historicalIncludedBatteryAllowanceKg,
      historicalBatteryReconciledBudgetKg: massBudget.historicalBatteryReconciledBudgetKg,
      historicalBatteryAllowanceReconciled: massBudget.historicalBatteryAllowanceReconciled,
      historicalUnadjustedHeadroomToMaximumKg:
        massBudget.historicalUnadjustedHeadroomToMaximumKg,
      historicalUnadjustedHeadroomIsNotUsableBudget:
        massBudget.historicalUnadjustedHeadroomIsNotUsableBudget,
      stationMassHeadroomAfterHistoricalReconciliationKg:
        massBudget.stationMassHeadroomAfterHistoricalReconciliationKg,
      stationMassHeadroomToEngineeringTargetAfterHistoricalReconciliationKg:
        massBudget.stationMassHeadroomToEngineeringTargetAfterHistoricalReconciliationKg,
      stationMassReconciliationFormula: massBudget.stationMassReconciliationFormula,
      stationMassHeadroomMayBeReportedOnlyAfterHistoricalBatteryAndCurrentInventoryAreReconciled:
        massBudget.stationMassHeadroomMayBeReportedOnlyAfterHistoricalBatteryAndCurrentInventoryAreReconciled,
      existingBudgetIncludesExistingAzElMotors: massBudget.existingBudgetIncludesTwoAzElMotors,
      existingBudgetIncludesAntenna: massBudget.existingBudgetIncludesAntenna,
      existingBudgetIncludesBatteryHistorically:
        massBudget.existingBudgetIncludesBatteryHistorically,
      existingBudgetIncludesLegacyCablesAndConnectors:
        massBudget.existingBudgetIncludesLegacyCablesAndConnectors,
      operationalMassScope: massBudget.operationalMassScope,
      maximumOperationalStationMassKg: massBudget.maximumOperationalStationMassKg,
      engineeringTargetOperationalStationMassKg:
        massBudget.engineeringTargetOperationalStationMassKg,
      preferredMeasuredReserveKg: massBudget.preferredMeasuredReserveKg,
      externalBatteryPackAndBmsCarriedMassKg:
        massBudget.externalBatteryPackAndBmsCarriedMassKg,
      externalBatteryPackMassMustNotBeAssumedZero:
        massBudget.externalBatteryPackMassMustNotBeAssumedZero,
      externalBatteryPackAndBmsExcludedFromStationMassCap:
        massBudget.externalBatteryPackAndBmsExcludedFromStationMassCap,
      stationTotalIncludesTripod: massBudget.stationTotalIncludesTripod,
      externalBatteryMustHaveMeasuredCarriedMassBeforeTransportTotal:
        massBudget.externalBatteryMustHaveMeasuredCarriedMassBeforeTransportTotal,
      externalBatteryChargerMassKg: massBudget.externalBatteryChargerMassKg,
      externalBatteryChargerIncludedInStationMassIfCarried:
        massBudget.externalBatteryChargerIncludedInStationMassIfCarried,
      totalTransportedMassKg: massBudget.totalTransportedMassKg,
      computeAndSdr: design.computeAndSdr,
      remainingToMaximumBeforeUnknownAdditionsKg: null,
      remainingToEngineeringTargetBeforeUnknownAdditionsKg: null,
      newPolSubsystemMassKg: massBudget.newPolSubsystemMassKg,
      stationSidePowerHardwareMassKg: massBudget.stationSidePowerHardwareMassKg,
      stationPowerMassAccounting: massBudget.stationPowerMassAccounting,
      powerpoleInputConnectorPairAndContactsMassKg:
        massBudget.powerpoleInputConnectorPairAndContactsMassKg,
      powerpoleInputConnectorPairMassIncludesBothMatingHalves:
        massBudget.powerpoleInputConnectorPairMassIncludesBothMatingHalves,
      powerpoleInputConnectorsAndHarnessIncludedInStationCap:
        massBudget.powerpoleInputConnectorsAndHarnessIncludedInStationCap,
      masterBatteryInputWirePairMassKg: massBudget.masterBatteryInputWirePairMassKg,
      masterBatteryInputWireGaugeAndLength: massBudget.masterBatteryInputWireGaugeAndLength,
      masterPositiveFuseAndHolderAssemblyMassKg:
        massBudget.masterPositiveFuseAndHolderAssemblyMassKg,
      masterFuseIsDCAndBatteryFaultCurrentRated:
        massBudget.masterFuseIsDCAndBatteryFaultCurrentRated,
      branchFuseAndHolderMassKg: massBudget.branchFuseAndHolderMassKg,
      branchHarnessWireAndConnectorMassKg: massBudget.branchHarnessWireAndConnectorMassKg,
      branchWireGaugeAndLengthByBranch: massBudget.branchWireGaugeAndLengthByBranch,
      separatelyFusedBranchCount: massBudget.separatelyFusedBranchCount,
      branchFuseRatingsSelected: massBudget.branchFuseRatingsSelected,
      powerHarnessStrainReliefPlateMassKg:
        massBudget.powerHarnessStrainReliefPlateMassKg,
      powerHarnessStrainReliefPlateOptional:
        massBudget.powerHarnessStrainReliefPlateOptional,
      powerHarnessStrainReliefPlateDimensionsMm:
        massBudget.powerHarnessStrainReliefPlateDimensionsMm,
      powerpolePanelHousingBracketMassKg:
        massBudget.powerpolePanelHousingBracketMassKg,
      powerpolePanelHousingBracketSelected:
        massBudget.powerpolePanelHousingBracketSelected,
      powerpolePanelHousingOutlineVerified:
        massBudget.powerpolePanelHousingOutlineVerified,
      cm5ComputeModuleMassKg: massBudget.cm5ComputeModuleMassKg,
      officialCm5CarrierBoardMassKg: massBudget.officialCm5CarrierBoardMassKg,
      cm5ThermalSolutionMassKg: massBudget.cm5ThermalSolutionMassKg,
      cm5AndCarrierMountHardwareMassKg: massBudget.cm5AndCarrierMountHardwareMassKg,
      limeSdrMiniQuantity: design.computeAndSdr.sdrCount,
      limeSdrMiniUnitsMassKg: massBudget.limeSdrMiniUnitsMassKg,
      limeSdrMiniMountsMassKg: massBudget.limeSdrMiniMountsMassKg,
      sdrPowerAmplifiersMassKg: massBudget.sdrPowerAmplifiersMassKg,
      sdrFiltersAndShieldsMassKg: massBudget.sdrFiltersAndShieldsMassKg,
      computeSdrEnclosureMassKg: massBudget.computeSdrEnclosureMassKg,
      otherRadioHardwareMassKg: massBudget.otherRadioHardwareMassKg,
      auxiliaryStationHardwareMassKg: massBudget.auxiliaryStationHardwareMassKg,
      tripodMassKg: massBudget.tripodMassKg,
      otherOperationalCablesAndConnectorsExcludingSensorAndRfKg:
        massBudget.otherOperationalCablesAndConnectorsExcludingSensorAndRfKg,
      addedSensorMassesKg: massBudget.addedSensorMassesKg,
      sensorCablesAndConnectorsKg: massBudget.sensorCablesAndConnectorsKg,
      compassMountDimensionsMm: massBudget.compassMountDimensionsMm,
      compassImuModuleSelected: massBudget.compassImuModuleSelected,
      gpsReceiverModuleSelected: massBudget.gpsReceiverModuleSelected,
      gpsAntennaMountDimensionsMm: massBudget.gpsAntennaMountDimensionsMm,
      smaBulkheadConnectorMassKg: massBudget.smaBulkheadConnectorMassKg,
      coaxBulkheadInterfacePlateMassKg: massBudget.coaxBulkheadInterfacePlateMassKg,
      axisCoaxServiceLoopAssemblyMassKg: massBudget.axisCoaxServiceLoopAssemblyMassKg,
      rfFeedBranchCoaxMassKg: massBudget.rfFeedBranchCoaxMassKg,
      rfFeedBranchCoaxAssemblyCount: Object.keys(massBudget.rfFeedBranchCoaxMassKg).length,
      remainingSmaRfConnectorsAndAdaptersMassKg:
        massBudget.remainingSmaRfConnectorsAndAdaptersMassKg,
      gpsAntennaStationaryWithSkyView: massBudget.gpsAntennaStationaryWithSkyView,
      compassIsEncoder: massBudget.compassIsEncoder,
      completeStationMassKg: massBudget.stationTotalKg,
      stationTotalFormula:
        '(historical_two_axis_budget_kg - measured_historical_battery_allowance_kg) + CM5_module_official_CM5IO_carrier_thermal_mounts_two_LimeSDR_Mini_units_enclosure_radio_PAs_filters_and_auxiliary_hardware_kg + new_POL_subsystem_kg + tripod_kg + sensors_mounts_station_side_power_and_all_station_cables_connectors_kg',
      transportedTotalFormula:
        'complete_station_mass_kg + external_battery_pack_and_BMS_mass_kg',
      measured: massBudget.measured,
      operationalStationTotalFormula:
        '(historical_two_axis_budget_kg - measured_historical_battery_allowance_kg) + CM5_module_official_CM5IO_carrier_thermal_and_mounts_kg + two_LimeSDR_Mini_units_and_mounts_kg + compute_SDR_enclosure_kg + SDR_PA_filters_shields_other_radio_and_auxiliary_station_hardware_kg + new_POL_subsystem_kg + tripod_kg + added_encoder_compass_GPS_sensors_and_mounts_kg + sensor_cables_and_connectors_kg + sma_bulkhead_connector_kg + coax_bulkhead_interface_plate_kg + axis_coax_service_loop_assembly_kg + four_individual_rf_feed_branch_coax_assemblies_kg + remaining_SMA_connectors_adapters_kg + station_side_power_and_cables_kg + other_additional_operational_cables_connectors_kg',
      status: 'Historical baseline is not directly comparable: it includes an unquantified battery allowance and excludes radio and tripod. Do not use raw baseline headroom; reconcile the battery allowance and weigh the complete current station inventory before calculating station total or cap margin. External battery pack/BMS is carried and reported separately, excluded from the 5 kg station cap.'
    }
  };
}

if (require.main === module) {
  const design = JSON.parse(fs.readFileSync(
    path.join(__dirname, '..', 'calc', 'polarization.json'), 'utf8'));
  process.stdout.write(`${JSON.stringify(calculate(design), null, 2)}\n`);
}

module.exports = { beltPathLength, calculate, solveBeltCenter };
