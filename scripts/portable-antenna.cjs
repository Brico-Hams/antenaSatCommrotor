const fs = require('node:fs');
const path = require('node:path');
const { calculate: engineering } = require('./engineering-report.cjs');
const root = path.resolve(__dirname, '..');

function calculate(config, base) {
  const m = config.mechanical;
  for (const [name, value] of Object.entries(m)) {
    for (const number of Array.isArray(value) ? value : [value]) {
      if (!Number.isFinite(number) || (name !== 'stowTipsXmm' && number <= 0)) {
        throw new Error(`Invalid PF-01 dimension: ${name}`);
      }
    }
  }
  if (m.boomInnerMm >= m.boomOuterMm || m.rodInnerMm >= m.rodDiameterMm ||
      m.spigotOuterMm >= m.boomInnerMm || m.hubBaseHeightMm >= m.hubHeightMm) {
    throw new Error('Invalid PF-01 tube or hub wall dimensions');
  }
  const rf = engineering(base).rf;
  const vhf = rf.find((band) => band.frequencyMHz === 145);
  const uhf = rf.find((band) => band.frequencyMHz === 435);
  if (!vhf || !uhf) throw new Error('PF-01 requires the 145/435 MHz design bands');
  const planes = [
    { id: 'VR', bandMHz: 145, role: 'reflector', zMm: 0, clockDeg: 0, spanMm: vhf.reflectorTotalMm },
    { id: 'UR', bandMHz: 435, role: 'reflector', zMm: (vhf.spacingMm - uhf.spacingMm) / 2, clockDeg: 45, spanMm: uhf.reflectorTotalMm },
    { id: 'UD', bandMHz: 435, role: 'driven', zMm: (vhf.spacingMm + uhf.spacingMm) / 2, clockDeg: 45, spanMm: uhf.drivenTotalMm },
    { id: 'VD', bandMHz: 145, role: 'driven', zMm: vhf.spacingMm, clockDeg: 0, spanMm: vhf.drivenTotalMm }
  ];
  const arms = planes.map((plane) => ({
    plane: plane.id, quantity: 4,
    innerRodMm: (plane.bandMHz === 145 ? m.vhfSplitRadiusMm : plane.spanMm / 2) - m.rodStartRadiusMm,
    outerRodMm: plane.bandMHz === 145 ? plane.spanMm / 2 - m.vhfSplitRadiusMm : 0,
    nominalTipRadiusMm: plane.spanMm / 2
  }));
  const boomLengthMm = m.boomSectionMm * m.boomSections;
  const mesh = config.reflectorMesh;
  if (mesh.plane !== 'VR' || mesh.panels !== 4 ||
      !Number.isFinite(mesh.pitchMm) || mesh.pitchMm <= mesh.wireDiameterMm ||
      mesh.wireDiameterMm <= 0 || mesh.centralOpeningRadiusMm <= m.clevisOuterRadiusMm ||
      mesh.reservedFoldedPacketMm.some((value) => !Number.isFinite(value) || value <= 0)) {
    throw new Error('Invalid PF-01 reflector mesh dimensions');
  }
  const meshAreaM2 = 2 * ((vhf.reflectorTotalMm / 2) ** 2 - mesh.centralOpeningRadiusMm ** 2) / 1e6;
  const meshWireLengthMApprox = 2 * meshAreaM2 / (mesh.pitchMm / 1000);
  const stowOrder = ['VR', 'VD', 'UR', 'UD'];
  const stowed = stowOrder.map((id, index) => {
    const plane = planes.find((item) => item.id === id);
    const arm = arms.find((item) => item.plane === id);
    return {
      plane: id, baseZmm: index * m.stowHubPitchMm,
      clockDeg: index * m.stowHubClockingDeg,
      foldedTipZmm: index * m.stowHubPitchMm + m.pivotHeightMm +
        (plane.bandMHz === 145 ? m.vhfSplitRadiusMm : arm.nominalTipRadiusMm) - m.pivotRadiusMm
    };
  });
  const packageMin = [
    Math.min(-m.clevisOuterRadiusMm, m.stowTipsXmm - m.rodDiameterMm / 2, -mesh.reservedFoldedPacketMm[0] / 2),
    Math.min(-m.clevisOuterRadiusMm, -mesh.reservedFoldedPacketMm[1] / 2), 0
  ];
  const packageMax = [
    Math.max(m.clevisOuterRadiusMm, m.stowSpareBoomXmm + m.boomOuterMm / 2, mesh.reservedFoldedPacketMm[0] / 2),
    Math.max(m.clevisOuterRadiusMm, mesh.reservedFoldedPacketMm[1] / 2),
    Math.max(m.boomSectionMm, mesh.packetBaseZmm + mesh.reservedFoldedPacketMm[2],
      ...stowed.map((plane) => plane.foldedTipZmm + m.rodDiameterMm / 2))
  ];
  const nominalPackageMm = packageMax.map((max, i) => max - packageMin[i]);
  const withAllowanceMm = nominalPackageMm.map((length) => length + 2 * m.packingAllowanceMmPerSide);
  const rodLengthMm = arms.reduce((sum, arm) => sum + arm.quantity * (arm.innerRodMm + arm.outerRodMm), 0);
  const tubeVolumeCm3 = Math.PI / 4 * (m.boomOuterMm ** 2 - m.boomInnerMm ** 2) * boomLengthMm / 1000;
  const rodVolumeCm3 = Math.PI / 4 * (m.rodDiameterMm ** 2 - m.rodInnerMm ** 2) * rodLengthMm / 1000;
  const couplerVolumeCm3 = 8 * Math.PI / 4 * (m.vhfCouplerOuterMm ** 2 - m.vhfCouplerInnerMm ** 2) * m.vhfCouplerLengthMm / 1000;
  const spigotVolumeCm3 = Math.PI / 4 * m.spigotOuterMm ** 2 * m.spigotLengthMm / 1000;
  const result = {
    revision: config.revision, status: config.status,
    warning: 'Nominal geometric packing and partial stock mass only. No RF, swept-volume, tolerance, strength or complete-mass acceptance.',
    planes, arms, stowed,
    boom: { lengthMm: boomLengthMm, splitZmm: m.boomSectionMm - m.boomRearOverhangMm,
      frontClearanceMm: boomLengthMm - m.boomRearOverhangMm - vhf.spacingMm,
      spigotOverlapMmPerSide: m.spigotLengthMm / 2 },
    package: { nominalMm: nominalPackageMm, withAllowanceMm, targetMm: m.packageTargetMm,
      fitsNominalTarget: withAllowanceMm.every((size, i) => size <= m.packageTargetMm[i]),
      longestLooseTipMm: Math.max(...arms.map((arm) => arm.outerRodMm)),
      minNominalRodCenterSpacingMm: 2 * m.pivotRadiusMm * Math.sin(m.stowHubClockingDeg * Math.PI / 360),
      method: 'Four released cassettes stacked and clocked; VHF tips detached; one boom section through centers, spare alongside; assumed reserved mesh packet above. Not a one-motion collapse.' },
    reflectorMesh: {
      ...mesh, areaM2: meshAreaM2,
      diagonalMm: vhf.reflectorTotalMm,
      wireLengthMApprox: meshWireLengthMApprox,
      wireMassGApprox: meshWireLengthMApprox * Math.PI / 4 * mesh.wireDiameterMm ** 2 * mesh.densityGcm3Assumed,
      pitchToUhfWavelength: mesh.pitchMm / (uhf.wavelengthM * 1000),
      geometricOpenAreaFractionApprox: (1 - mesh.wireDiameterMm / mesh.pitchMm) ** 2,
      warning: 'Reflects both bands; RF pattern, mesh contacts, wind and real folded thickness require tests. Reserved packet is a packing allocation, not a simulated textile fold.'
    },
    partialStockMassG: {
      boomTubes: tubeVolumeCm3 * config.massAssumptions.glassFibreDensityGcm3,
      radialRods: rodVolumeCm3 * config.massAssumptions.aluminiumDensityGcm3,
      eightTipCouplers: couplerVolumeCm3 * config.massAssumptions.aluminiumDensityGcm3,
      solidSpigot: spigotVolumeCm3 * config.massAssumptions.glassFibreDensityGcm3,
      excluded: config.massAssumptions.excluded
    }
  };
  if (arms.some((arm) => arm.innerRodMm <= 0 || arm.outerRodMm < 0) ||
      result.boom.frontClearanceMm <= m.hubHeightMm) {
    throw new Error('PF-01 stock lengths or front clearance invalid');
  }
  return result;
}

function outputs() {
  const config = JSON.parse(fs.readFileSync(path.join(root, 'calc/portable-antenna.json'), 'utf8'));
  const base = JSON.parse(fs.readFileSync(path.join(root, 'calc/design.json'), 'utf8'));
  const result = calculate(config, base);
  if (!result.package.fitsNominalTarget) throw new Error('Nominal package exceeds target');
  const parameters = [
    '// Generated by scripts/portable-antenna.cjs. Edit calc/portable-antenna.json, not this file.',
    ...Object.entries(config.mechanical).map(([key, value]) => `pf_${key} = ${JSON.stringify(value)};`),
    ...Object.entries(config.reflectorMesh).filter(([,value]) => typeof value === 'number' || Array.isArray(value))
      .map(([key,value]) => `pf_mesh_${key} = ${JSON.stringify(value)};`),
    `pf_planes = ${JSON.stringify(result.planes.map((plane) => [plane.zMm, plane.spanMm, plane.bandMHz, plane.clockDeg]))};`,
    `pf_boomSplitZmm = ${result.boom.splitZmm};`,
    'pf_stowOrder = [0, 3, 1, 2];', ''
  ].join('\n');
  const files = new Map([
    ['cad/portable-antenna-parameters.scad', parameters],
    ['calc/portable-antenna-report.json', JSON.stringify(result, null, 2) + '\n']
  ]);
  const views = [
    ['deployed', 'PF-01 desplegada', 'Cuatro planos radiales / VHF y UHF sobre boom comun'],
    ['front', 'PF-01 vista frontal', 'Cruces ortogonales por banda; UHF girada 45 grados'],
    ['folded', 'PF-01 transporte', 'Puntas y malla desmontadas; paquete de malla solo reservado'],
    ['hinge', 'PF-01 articulacion', 'Pasador M4 y bloqueo M3 separados; puente RF externo'],
    ['reflector', 'PF-01 reflector plegable', 'Cuatro paneles conductores flexibles sobre brazos VHF posteriores']
  ];
  for (const [name, title, subtitle] of views) {
    files.set(`docs/assembly/portable/PF-${name}.svg`, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 940" role="img" aria-labelledby="title desc" font-family="Arial, sans-serif">
<title id="title">${title} - BricoHams</title><desc id="desc">${subtitle}. Concepto no validado fisicamente.</desc>
<rect width="1200" height="940" fill="white"/><rect x="8" y="8" width="1184" height="924" fill="none" stroke="#12263f" stroke-width="2"/>
<image href="../../../branding/bricohams_horizontal.png" x="25" y="20" width="220" height="65"/>
<text x="280" y="47" fill="#12263f" font-size="28" font-weight="bold">${title}</text>
<text x="280" y="79" fill="#5b6b7b" font-size="18">${subtitle}</text><path d="M10 100h1180" stroke="#e8871e" stroke-width="5"/>
<image href="PF-${name}.png" x="25" y="115" width="1150" height="680" preserveAspectRatio="xMidYMid meet"/>
<rect x="25" y="810" width="1150" height="40" fill="#fff0db"/>
<text x="40" y="837" font-size="18" fill="#12263f">CANDIDATA PF-01 / RF, tolerancias, plegado y carga pendientes de ensayo</text>
<text x="25" y="883" font-size="17" fill="#12263f">BricoHams | Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina | bricohams.org</text>
<text x="25" y="912" font-size="15" fill="#5b6b7b">Render del CAD original. No es plano a escala ni autorizacion de fabricacion. Ver ANTENNA-PORTABLE.md.</text>
</svg>
`);
  }
  return files;
}
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.some((arg) => arg !== '--check')) throw new Error('Usage: node scripts/portable-antenna.cjs [--check]');
  for (const [file, content] of outputs()) {
    const absolute = path.join(root, file);
    if (args.includes('--check')) {
      if (!fs.existsSync(absolute) || fs.readFileSync(absolute, 'utf8') !== content) throw new Error(`Regenerate ${file}`);
    } else {
      fs.mkdirSync(path.dirname(absolute), { recursive: true });
      fs.writeFileSync(absolute, content);
    }
  }
  console.log('PF-01 parameters, packing report and branded view frames synchronized.');
}
module.exports = { calculate, outputs };
