const assert = require('node:assert/strict');
const test = require('node:test');
const design = require('../calc/design.json');
const { calculate } = require('../scripts/engineering-report.cjs');
const result = calculate(design);

test('planetary topology, tooth closure and 25:1 reduction', () => {
  const g = design.gear;
  assert.equal(g.ringTeeth, g.sunTeeth + 2 * g.planetTeeth);
  assert.equal(result.gearing.reductionPerStage, 5);
  assert.equal(result.gearing.reduction, 25);
  assert.equal(result.gearing.planetSpacingAssemblyInteger % 1, 0);
  assert.ok(g.sunTeeth >= result.gearing.unshiftedMinimumSunTeeth);
});

test('three planets do not intersect in the transverse plane', () => {
  const g = design.gear;
  const neighborDistanceMm = 2 * result.gearing.planetOrbitRadiusMm * Math.sin(Math.PI / g.planetCount);
  const planetAddendumDiameterMm = g.moduleMm * (g.planetTeeth + 2);
  assert.ok(neighborDistanceMm > planetAddendumDiameterMm + 0.5);
});

test('command resolution is 80000 microsteps/revolution, not measured accuracy', () => {
  assert.equal(result.gearing.stepCount, 80000);
  assert.equal(result.gearing.commandedMicrostepDeg, 0.0045);
});

test('145 MHz radiators are three times the 435 MHz dimensions', () => {
  const [vhf, uhf] = result.rf;
  assert.ok(Math.abs(vhf.drivenTotalMm / uhf.drivenTotalMm - 3) < 1e-12);
  assert.ok(vhf.drivenArmMm > 470 && vhf.drivenArmMm < 480);
  assert.ok(uhf.drivenArmMm > 155 && uhf.drivenArmMm < 160);
  assert.ok(vhf.initialStockArmMm > vhf.drivenArmMm);
  assert.ok(vhf.spacingMm > 460 && vhf.spacingMm < 470);
});

test('the example wind load does not certify NEMA14 operation', () => {
  assert.ok(result.loadExample.gravityTorqueNm > 0.14);
  assert.ok(result.loadExample.safetyFactoredTorqueNm > result.loadExample.assumedOutputTorqueNm);
  assert.equal(result.loadExample.passesAssumedMotorTorqueBudget, false);
});
