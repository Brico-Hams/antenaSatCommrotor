const fs = require('node:fs');
const path = require('node:path');

function calculate(design) {
  const { rf, gear, load } = design;
  const reductionPerStage = 1 + gear.ringTeeth / gear.sunTeeth;
  const reduction = reductionPerStage ** gear.stages;
  const stepCount = gear.motorStepsPerRevolution * gear.microsteps * reduction;
  const windForceN = 0.5 * load.airDensityKgM3 * load.dragCoefficientAssumed *
    load.projectedAreaM2Example * load.windMpsCalculationOnly ** 2;
  const gravityTorqueNm = load.antennaMassKgTarget *
    load.gravityMps2 * load.antennaCgOffsetMMaximumTarget;
  const windTorqueNm = windForceN * load.windMomentArmMExample;
  const assumedOutputTorqueNm = load.motorTorqueNmExampleNotVerified *
    reduction * gear.efficiencyPerStageAssumed ** gear.stages;
  const safetyFactoredTorqueNm = (gravityTorqueNm + windTorqueNm) *
    load.designSafetyFactor;
  return {
    status: design.status,
    warning: 'Calculated examples, not measured RF performance or load certification.',
    rf: rf.bandsMHz.map((frequencyMHz) => {
      const wavelengthM = rf.speedOfLightMps / (frequencyMHz * 1e6);
      const drivenTotalMm = wavelengthM * 500 * rf.drivenShorteningFactor;
      return {
        frequencyMHz, wavelengthM, drivenTotalMm,
        drivenArmMm: drivenTotalMm / 2,
        initialStockArmMm: drivenTotalMm / 2 + rf.stockTrimAllowanceMmPerArm,
        reflectorTotalMm: drivenTotalMm * rf.reflectorFactor,
        spacingMm: wavelengthM * 1000 * rf.reflectorSpacingWavelengths,
        coaxQuarterWaveMmExampleOnly: wavelengthM * 250 * rf.coaxVelocityFactorExampleOnly
      };
    }),
    gearing: {
      reductionPerStage, reduction, stepCount,
      commandedMicrostepDeg: 360 / stepCount,
      sunPitchDiameterMm: gear.moduleMm * gear.sunTeeth,
      planetPitchDiameterMm: gear.moduleMm * gear.planetTeeth,
      ringPitchDiameterMm: gear.moduleMm * gear.ringTeeth,
      planetOrbitRadiusMm: gear.moduleMm * (gear.sunTeeth + gear.planetTeeth) / 2,
      planetSpacingAssemblyInteger: (gear.sunTeeth + gear.ringTeeth) / gear.planetCount,
      unshiftedMinimumSunTeeth: 2 / Math.sin(gear.pressureAngleDeg * Math.PI / 180) ** 2
    },
    loadExample: {
      gravityTorqueNm, windForceN, windTorqueNm,
      assumedOutputTorqueNm, safetyFactoredTorqueNm,
      passesAssumedMotorTorqueBudget: assumedOutputTorqueNm >= safetyFactoredTorqueNm,
      warning: 'Holding torque is not running torque; wind speed is not an operating limit.'
    }
  };
}

if (require.main === module) {
  const design = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'calc', 'design.json'), 'utf8'));
  process.stdout.write(JSON.stringify(calculate(design), null, 2) + '\n');
}
module.exports = { calculate };
