const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const defaults = require('../calc/antenna-options.json');
const design = require('../calc/design.json');

function calculate(config = defaults) {
  const positive = (n) => Number.isFinite(n) && n > 0;
  for (const section of [config.eggbeater, config.qfh, config.power]) {
    for (const value of Object.values(section)) {
      if (typeof value === 'number' && !positive(value)) throw new Error('Invalid antenna option parameter');
    }
  }
  if (!config.frequenciesMHz.length || !config.frequenciesMHz.every(positive) ||
      !positive(config.conductorDiameterMm) || !positive(config.mastDiameterMm) ||
      !positive(config.feedGapMm) || config.feedGapMm <= config.mastDiameterMm + config.conductorDiameterMm ||
      config.qfh.turnsPerSide !== 0.5 || !Number.isInteger(config.eggbeater.segmentsPerLoop) ||
      config.eggbeater.segmentsPerLoop < 4 || !Number.isInteger(config.qfh.segmentsPerHelicalSide) ||
      config.qfh.segmentsPerHelicalSide < 1) throw new Error('Invalid antenna option geometry');
  if (config.power.maxConductedW !== 25 || config.power.maxSsbPepW !== 25 ||
      config.power.maxAmCarrierWAt100Percent * 4 !== config.power.maxSsbPepW ||
      config.power.simultaneousTransmitters !== 1) throw new Error('Invalid antenna power ceiling');
  return config.frequenciesMHz.flatMap((frequencyMHz) => {
    const wavelengthMm = design.rf.speedOfLightMps / (frequencyMHz * 1e6) * 1000;
    const e = config.eggbeater, q = config.qfh;
    const diameterMm = wavelengthMm * e.circumferenceWavelengths / Math.PI;
    if (config.feedGapMm >= diameterMm) throw new Error('Feed gap exceeds Eggbeater diameter');
    const gapAngle = 2 * Math.asin(config.feedGapMm / diameterMm);
    const circumferenceMm = Math.PI * diameterMm;
    const reflectorZ = 0;
    const bottom = wavelengthMm * e.reflectorSpacingWavelengths;
    const heightMm = bottom + diameterMm + e.loopVerticalOffsetMm;
    const loops = [q.largeLoopWavelengths, q.smallLoopWavelengths].map((factor) => {
      const lengthMm = factor * wavelengthMm;
      const diameterMm = lengthMm / (2 * Math.hypot(q.heightToDiameter, Math.PI / 2) + 2);
      const heightMm = q.heightToDiameter * diameterMm;
      if (config.feedGapMm >= diameterMm) throw new Error('Feed gap exceeds QFH diameter');
      return { factor, lengthMm, diameterMm, heightMm,
        helicalSideMm: Math.hypot(heightMm, Math.PI * diameterMm / 2) };
    });
    const large = loops[0];
    return [
      { id: `EB-${frequencyMHz}`, type: 'eggbeater', frequencyMHz, wavelengthMm,
        diameterMm, heightMm, bottomMm: bottom, reflectorZmm: reflectorZ,
        reflectorRadialMm: wavelengthMm * e.reflectorRadialWavelengths,
        verticalOffsetMm: e.loopVerticalOffsetMm, circumferenceMm, gapAngleRad: gapAngle,
        conductorPerLoopMm: (2 * Math.PI - gapAngle) * diameterMm / 2,
        maxArcSegmentMm: circumferenceMm / e.segmentsPerLoop,
        arcSegmentChordMm: diameterMm * Math.sin(Math.PI / e.segmentsPerLoop),
        loops: 2, segmentsPerLoop: e.segmentsPerLoop },
      { id: `QFH-${frequencyMHz}`, type: 'qfh', frequencyMHz, wavelengthMm,
        diameterMm: large.diameterMm, heightMm: large.heightMm + q.baseHeightMm,
        loops: loops.map((loop) => ({ ...loop,
          bottomMm: q.baseHeightMm + (large.heightMm - loop.heightMm) / 2,
          conductorMm: loop.lengthMm - config.feedGapMm,
          maxHelixSegmentMm: loop.helicalSideMm / q.segmentsPerHelicalSide })),
        segmentsPerHelicalSide: q.segmentsPerHelicalSide }
    ];
  });
}

function pathsFor(model, config = defaults) {
  const paths = [];
  const sample = (fn, count = 96) => Array.from({ length: count + 1 }, (_, i) => fn(i / count));
  const d = config.conductorDiameterMm;
  if (model.type === 'eggbeater') {
    for (let loop = 0; loop < 2; loop++) {
      const r = model.diameterMm / 2, start = model.gapAngleRad / 2;
      paths.push({ role: 'radiator', loop, diameterMm: d, points: sample((t) => {
        const a = start + (2 * Math.PI - 2 * start) * t;
        const x = r * Math.sin(a), z = model.bottomMm + loop * model.verticalOffsetMm + r * (1 - Math.cos(a));
        return loop === 0 ? [x, 0, z] : [0, x, z];
      }) });
    }
    for (let i = 0; i < 4; i++) {
      const a = i * Math.PI / 2;
      paths.push({ role: 'reflector', diameterMm: d,
        points: [[0, 0, 0], [model.reflectorRadialMm * Math.cos(a), model.reflectorRadialMm * Math.sin(a), 0]] });
    }
  } else {
    model.loops.forEach((loop, index) => {
      const r = loop.diameterMm / 2, phase = index * Math.PI / 2;
      const polar = (a, z, radius = r) => [radius * Math.cos(a), radius * Math.sin(a), z];
      for (let side = 0; side < 2; side++) {
        paths.push({ role: 'radiator', loop: index, diameterMm: d, points: sample((t) =>
          polar(phase + side * Math.PI + t * Math.PI, loop.bottomMm + t * loop.heightMm), 64) });
      }
      paths.push({ role: 'radiator', loop: index, diameterMm: d,
        points: [polar(phase + Math.PI, loop.bottomMm + loop.heightMm), polar(phase, loop.bottomMm + loop.heightMm)] });
      for (let side = 0; side < 2; side++) {
        const a = phase + side * Math.PI;
        paths.push({ role: 'radiator', loop: index, diameterMm: d,
          points: [polar(a, loop.bottomMm), polar(a, loop.bottomMm, config.feedGapMm / 2)] });
      }
    });
  }
  return paths;
}

const xml = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const round = (n) => Number(n.toFixed(3));
function illustration(model, paths, front = false, config = defaults) {
  const project = ([x, y, z]) => front ? [x, -z] : [0.86 * x - 0.6 * y, 0.3 * x + 0.43 * y - z];
  const all = paths.flatMap((p) => p.points).concat([[0, 0, 0], [0, 0, model.heightMm]]);
  const projected = all.map(project);
  const min = [0, 1].map((axis) => Math.min(...projected.map((p) => p[axis])));
  const max = [0, 1].map((axis) => Math.max(...projected.map((p) => p[axis])));
  const scale = Math.min(870 / (max[0] - min[0]), 480 / (max[1] - min[1]));
  const screen = (p) => {
    const v = project(p);
    return [round(590 + (v[0] - (min[0] + max[0]) / 2) * scale), round(360 + (v[1] - (min[1] + max[1]) / 2) * scale)];
  };
  const polyline = (points, color, width) => `<polyline points="${points.map((p) => screen(p).join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc">
<title id="title">BricoHams ${xml(model.id)} ${front ? 'frontal' : 'isometrica'}</title>
<desc id="desc">Geometria candidata calculada. Dos puertos equilibrados abiertos; redes de adaptacion y fase no representadas. Sin prestaciones RF medidas.</desc>
<rect width="1200" height="800" fill="#f4f7fa"/>
<image href="../../../branding/bricohams_horizontal.png" x="950" y="100" width="220" height="65"/>
<rect width="1200" height="95" fill="#16324a"/><text x="35" y="44" fill="white" font-family="sans-serif" font-size="27">BricoHams | ${xml(model.id)} | ${front ? 'frontal' : 'isometrica'}</text>
<text x="35" y="77" fill="#bce8eb" font-family="sans-serif" font-size="18">TX/RX candidato | techo solicitado 25 W, NO CUALIFICADO</text>
${polyline([[0, 0, 0], [0, 0, model.heightMm]], '#aebbc2', 10)}
${paths.map((p) => polyline(p.points, p.role === 'reflector' ? '#628a7d' : p.loop === 0 ? '#e8871e' : '#326488', 4)).join('\n')}
<g font-family="sans-serif" font-size="18" fill="#16324a"><text x="35" y="645">Diametro mayor ${round(model.diameterMm)} mm | altura ${round(model.heightMm)} mm</text>
<text x="35" y="675">Naranja: lazo 1 | azul: lazo 2 | verde: reflector opcional (Eggbeater)</text>
<text x="35" y="705">Separacion de alimentacion ${config.feedGapMm} mm; soportes dielectricos. No es plano final de corte.</text></g>
<rect y="730" width="1200" height="70" fill="#16324a"/><g fill="white" font-family="sans-serif" font-size="16"><text x="35" y="758">Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina | bricohams.org</text><text x="35" y="785">PROTOTIPO ANALITICO | Sin ganancia, ROE, polarizacion ni potencia verificadas</text></g></svg>\n`;
}

function bom(models, type, config) {
  const rows = [['id','quantity','component','specification','status','notes']];
  const add = (id, quantity, component, specification, notes) =>
    rows.push([id, quantity, component, specification, 'DESIGN_AND_RF_HOLD', notes]);
  for (const m of models.filter((m) => m.type === type)) {
    if (type === 'eggbeater') {
      add(`${m.id}-01`,16,'Conductive arc segment',`4 mm OD; reference full-circle arc <=${round(m.maxArcSegmentMm)} mm`,
        'Eight sectors per loop; two feed-end sectors shortened by half the feed gap arc; coupler overlap not included; not final cuts');
      add(`${m.id}-02`,14,'Conductive arc splice','Repeatable metal coupler for 4 mm conductor',
        'Seven non-feed joints per loop; no plastic electrical path; qualify contact heating at 25 W');
      add(`${m.id}-03`,4,'Optional reflector radial',`4 mm OD x ${round(m.reflectorRadialMm)} mm nominal`,
        'Radials at z0 with conductive central junction; VHF radial splits into two 258.442 mm nominal halves; coupler overlap excluded; tune pattern');
      if (m.frequencyMHz === 145) add(`${m.id}-04`,4,'Optional reflector mid-radial splice','Metal conductive 4 mm rod coupler',
        'Needed only if VHF radials split for transport; tune with actual couplers installed');
    } else {
      add(`${m.id}-01`,16,'Helix segment',`4 mm OD; large <=${round(m.loops[0].maxHelixSegmentMm)} mm; small <=${round(m.loops[1].maxHelixSegmentMm)} mm`,
        'Four segments per helical side; four sides total; lengths exclude coupler overlap; retain handed winding geometry');
      add(`${m.id}-02`,12,'Conductive helix splice','Repeatable metal coupler for 4 mm conductor',
        'Three internal joints per side; plus end transitions selected separately; test RF continuity and heating');
      add(`${m.id}-03`,2,'Top diameter bar',`Large ${round(m.loops[0].diameterMm)} mm; small ${round(m.loops[1].diameterMm)} mm`,
        'One per loop; top bars at different heights; preserve insulation at mast');
      add(`${m.id}-04`,4,'Bottom half bar',`Large ${round((m.loops[0].diameterMm-config.feedGapMm)/2)} mm; small ${round((m.loops[1].diameterMm-config.feedGapMm)/2)} mm`,
        'Two halves per loop; central 30 mm feed gap; do not short feed terminals');
      add(`${m.id}-05`,8,'End transition joint','Conductive helix-to-bar elbow or bend with retention',
        'Two upper and two lower transitions per loop; not included in ideal electrical length');
    }
    add(`${m.id}-10`,1,'Segmented dielectric mast',`20 mm OD; minimum model height ${round(m.heightMm)} mm`,
      'No carbon fibre; section lengths and structural joints require packing and load trial; not released stock cuts');
    add(`${m.id}-11`,8,'Dielectric conductor support','ASA 4.4 mm bore support coupon; positive metal retention',
      'Start with one print coupon; bracket layout and attachment to mast pending; no structural qualification');
    add(`${m.id}-12`,1,'Dual-port feed network','Two balanced ports; matching baluns and quadrature network selected by band',
      'Geometry does not prove self-phasing; no unqualified QCN-3+ at VHF or 25 W; isolated port load required');
    add(`${m.id}-13`,1,'Receive preamp and TX bypass kit','One band-specific set from antenna-preamps.csv',
      'Do not sum two copies for the same band; no TX through LNA; interlocked PA and physical RF bypass');
    add(`${m.id}-14`,1,'Transport retainers','Separate arc or helix sectors and insulated feed terminals',
      'No packed box size claimed until real packing trial; never straighten a tuned helix for transport');
  }
  return rows.map((r) => r.map((v) => `"${String(v).replace(/"/g,'""')}"`).join(',')).join('\n')+'\n';
}

function outputs(config = defaults) {
  const models = calculate(config);
  const geometries = models.map((m) => ({ ...m, paths: pathsFor(m, config) }));
  const report = {
    revision: config.revision, status: config.status,
    warning: 'Analytic seed geometry only. Not NEC/EM simulation or a released feed design. No measured gain, match, axial ratio, power or packed size.',
    power: config.power, models
  };
  const files = new Map([
    ['calc/antenna-options-report.json', JSON.stringify(report, null, 2)+'\n'],
    ['bom/antenna-eggbeater.csv', bom(models, 'eggbeater', config)],
    ['bom/antenna-qfh.csv', bom(models, 'qfh', config)],
    ['cad/antenna-options-parameters.scad', '// Generated by scripts/antenna-options.cjs; do not edit.\n' +
      `ao_names = ${JSON.stringify(models.map((m) => m.id))};\n`+
      `ao_heights = ${JSON.stringify(models.map((m) => m.heightMm))};\n`+
      `ao_mast_diameter = ${config.mastDiameterMm};\n`+
      `ao_paths = ${JSON.stringify(geometries.map((m) => m.paths.map((p) => [p.role === 'reflector' ? 2 : p.loop, p.diameterMm, p.points])))};\n`]
  ]);
  for (const m of geometries) {
    for (const front of [false, true]) files.set(`docs/assembly/options/${m.id}-${front ? 'front' : 'iso'}.svg`, illustration(m, m.paths, front, config));
  }
  return files;
}

if (require.main === module) {
  if (process.argv.slice(2).some((arg) => arg !== '--check')) throw new Error('Usage: node scripts/antenna-options.cjs [--check]');
  const check = process.argv.includes('--check');
  for (const [file, contents] of outputs()) {
    const target = path.join(root, file);
    if (check) {
      if (!fs.existsSync(target) || fs.readFileSync(target,'utf8') !== contents) throw new Error(`Regenerate ${file}`);
    } else {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, contents);
    }
  }
  console.log('Eggbeater/QFH: four band-specific candidates, eight views, two BOMs and CAD parameters synchronized.');
}
module.exports = { calculate, pathsFor, outputs };
