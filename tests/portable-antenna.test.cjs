const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { calculate, outputs } = require('../scripts/portable-antenna.cjs');
const { parseCsv } = require('../scripts/component-catalog.cjs');
const validateStl = require('./mechanical-stl.cjs');
const validateRenderedPng = require('./rendered-png.cjs');
const config = require('../calc/portable-antenna.json');
const base = require('../calc/design.json');
const report = calculate(config, base);
const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
// Checkout may convert line endings (core.autocrlf); compare content only.
const lf = (text) => text.replace(/\r\n/g, '\n');
const near = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-6, `${actual} != ${expected}`);

test('PF-01 uses project RF formulas, not unscaled dimensions from the video', () => {
  assert.deepEqual(report.planes.map((plane) => plane.id), ['VR', 'UR', 'UD', 'VD']);
  const [vr, ur, ud, vd] = report.planes;
  near(vd.zMm - vr.zMm, 299792458 / 145e6 * 1000 * 0.225);
  near(ud.zMm - ur.zMm, 299792458 / 435e6 * 1000 * 0.225);
  near((ur.zMm + ud.zMm) / 2, vd.zMm / 2);
  near(vd.spanMm, 299792458 / 145e6 * 500 * 0.92);
  near(vr.spanMm / vd.spanMm, 1.05);
  assert.match(config.status, /not-rf-or-load-qualified/);
  assert.equal(config.reference.sha256.length, 64);
});

test('PF-01 nominal packing including allowance meets every chosen package dimension', () => {
  assert.deepEqual(report.package.targetMm, [170, 140, 300]);
  assert.equal(report.package.fitsNominalTarget, true);
  report.package.withAllowanceMm.forEach((size, index) => assert.ok(size <= report.package.targetMm[index]));
  assert.ok(report.package.longestLooseTipMm < 250);
  assert.ok(report.package.minNominalRodCenterSpacingMm > config.mechanical.rodDiameterMm + 4);
  assert.deepEqual(report.stowed.map((plane) => plane.plane), ['VR', 'VD', 'UR', 'UD']);
  assert.ok(report.stowed.every((plane) => plane.foldedTipZmm + 2 < 250));
});

test('boom joint is between UHF planes and fits stock with positive front clearance', () => {
  assert.equal(report.boom.lengthMm, 500);
  assert.equal(report.boom.spigotOverlapMmPerSide, 40);
  const [,ur,ud] = report.planes;
  assert.ok(report.boom.splitZmm - 40 > ur.zMm + config.mechanical.hubHeightMm);
  assert.ok(report.boom.splitZmm + 40 < ud.zMm);
  assert.ok(report.boom.frontClearanceMm > config.mechanical.hubHeightMm);
});

test('portable BOM nominal conductive lengths and quantities match the CAD calculation', () => {
  const rows = parseCsv(read('bom/antenna-portable.csv'));
  assert.equal(rows.length, 23);
  assert.equal(new Set(rows.map((row) => row.id)).size, rows.length);
  const byId = Object.fromEntries(rows.map((row) => [row.id, row]));
  assert.equal(byId['PF-01'].quantity, '4');
  assert.equal(byId['PF-02'].quantity, '16');
  for (const [id, plane, type] of [
    ['PF-05', 'VR', 'innerRodMm'], ['PF-06', 'VR', 'outerRodMm'],
    ['PF-07', 'VD', 'outerRodMm'], ['PF-08', 'UR', 'innerRodMm'], ['PF-09', 'UD', 'innerRodMm']
  ]) {
    const length = Number(byId[id].specification.match(/x ([\d.]+) mm nominal/)[1]);
    near(length, report.arms.find((arm) => arm.plane === plane)[type]);
    assert.match(byId[id].specification, /4 OD x 2 ID/);
  }
  assert.ok(rows.every((row) => !/APPROVED|VERIFIED/.test(row.status)));
});

test('PF-01 partial mass accounts for hollow rods without claiming total antenna mass', () => {
  assert.ok(report.partialStockMassG.radialRods > 100 && report.partialStockMassG.radialRods < 120);
  assert.match(report.partialStockMassG.excluded, /Printed parts.*coax.*hybrids/);
  assert.match(report.warning, /No RF/);
  for (const value of Object.values(report.partialStockMassG).filter((value) => typeof value === 'number')) {
    assert.ok(Number.isFinite(value) && value > 0);
  }
});

test('PF-01 generated parameters, report and branded view frames are synchronized', () => {
  for (const [file, content] of outputs()) assert.equal(lf(read(file)), lf(content), file);
  for (const view of ['deployed', 'front', 'folded', 'hinge', 'reflector']) {
    const file = path.join(root, `docs/assembly/portable/PF-${view}.png`);
    validateRenderedPng(file);
  }
});

test('satellite reflector has an explicit conductive mesh and no unmeasured gain promise', () => {
  const mesh = report.reflectorMesh;
  assert.equal(mesh.plane, 'VR');
  assert.equal(mesh.panels, 4);
  assert.ok(mesh.areaM2 > 0.48 && mesh.areaM2 < 0.50);
  assert.ok(mesh.pitchToUhfWavelength < 1 / 20);
  assert.ok(mesh.wireMassGApprox > 10 && mesh.wireMassGApprox < 20);
  assert.match(mesh.warning, /Reflects both bands/);
  assert.match(mesh.warning, /not a simulated textile fold/);
  assert.match(read('cad/portable_antenna.scad'), /module pf_reflector_mesh\(\)/);
});

test('PF-01 printable candidate meshes are closed single connected solids', () => {
  for (const part of ['hub','arm']) {
    const result = validateStl(path.join(root, `cad/portable-stl/${part}.stl`));
    assert.equal(result.components, 1, `${part}: disconnected geometry`);
    assert.ok(result.volume > 1000);
  }
});

test('nominal hinge sweep has radial clearance and CAD provides exact intersection diagnostics', () => {
  const m = config.mechanical;
  assert.ok(m.pivotRadiusMm - Math.hypot(6, 6) > m.hubRingRadiusMm);
  const scad = read('cad/portable_antenna.scad');
  assert.match(scad, /angle=\[0:5:90\]/);
  assert.match(scad, /module pf_stow_collisions\(\)/);
  assert.match(scad, /intersection\(\)/);
  assert.match(read('cad/export-portable-antenna.ps1'), /Current top level object is empty/);
});

test('bad dimensions fail explicitly rather than producing success-shaped packing results', () => {
  for (const [key,value] of [['rodDiameterMm',-4],['boomInnerMm',21],['spigotOuterMm',17],['boomSectionMm',200]]) {
    const bad = structuredClone(config);
    bad.mechanical[key] = value;
    assert.throws(() => calculate(bad, base), /Invalid PF-01|PF-01 stock/);
  }
});

test('portable guide preserves RF, load and multiview-reference limits', () => {
  const guide = read('docs/ANTENNA-PORTABLE.md');
  for (const term of ['No se ve un ciclo completo', 'No cortocircuitar', '0,5 kg', 'RHCP/LHCP', 'no una lista de corte final']) {
    assert.ok(guide.includes(term), term);
  }
  assert.match(guide, /no se han alterado sus exports/);
});
