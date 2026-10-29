const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { calculate, pathsFor, outputs } = require('../scripts/antenna-options.cjs');
const { parseCsv } = require('../scripts/component-catalog.cjs');
const validateStl = require('./mechanical-stl.cjs');
const validateRenderedPng = require('./rendered-png.cjs');
const config = require('../calc/antenna-options.json');
const root = path.resolve(__dirname, '..');
const models = calculate();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
// Checkout may convert line endings (core.autocrlf); compare content only.
const lf = (text) => text.replace(/\r\n/g, '\n');
const near = (a,b,tolerance=1e-6) => assert.ok(Math.abs(a-b)<tolerance, `${a} != ${b}`);
const sub = (a,b) => a.map((v,i) => v-b[i]);
const dot = (a,b) => a.reduce((sum,v,i) => sum+v*b[i],0);
const norm = (a) => Math.sqrt(dot(a,a));
const pointDistance = (p,a,b) => {
  const u = sub(b,a);
  const t = Math.max(0,Math.min(1,dot(sub(p,a),u)/dot(u,u)));
  return norm(sub(p,a.map((v,i)=>v+t*u[i])));
};
function segmentDistance(a,b,c,d) {
  const u=sub(b,a),v=sub(d,c),w=sub(a,c);
  const aa=dot(u,u),bb=dot(u,v),cc=dot(v,v),dd=dot(u,w),ee=dot(v,w);
  const determinant=aa*cc-bb*bb;
  const distances=[pointDistance(a,c,d),pointDistance(b,c,d),pointDistance(c,a,b),pointDistance(d,a,b)];
  if (determinant>1e-10) {
    const s=(bb*ee-cc*dd)/determinant,t=(aa*ee-bb*dd)/determinant;
    if(s>=0 && s<=1 && t>=0 && t<=1) distances.push(norm(w.map((value,i)=>value+s*u[i]-t*v[i])));
  }
  return Math.min(...distances);
}

test('four independent monoband TX/RX candidates keep the 25 W ceiling and HOLD', () => {
  assert.deepEqual(models.map((m)=>m.id),['EB-145','QFH-145','EB-435','QFH-435']);
  assert.match(config.status,/not-rf-or-load-qualified/);
  assert.equal(config.power.maxConductedW,25);
  assert.equal(config.power.maxSsbPepW,25);
  assert.equal(config.power.maxAmCarrierWAt100Percent*4,25);
  assert.equal(config.power.simultaneousTransmitters,1);
  assert.match(config.power.qualification,/HOLD/);
});

test('Eggbeater circumference, feed gap, segmentation and height are mathematically consistent', () => {
  for(const m of models.filter((m)=>m.type==='eggbeater')) {
    near(m.diameterMm*Math.PI,299792458/m.frequencyMHz/1000);
    near(m.maxArcSegmentMm*8,m.circumferenceMm);
    near(m.arcSegmentChordMm,m.diameterMm*Math.sin(Math.PI/8));
    near(m.conductorPerLoopMm,(2*Math.PI-m.gapAngleRad)*m.diameterMm/2);
    const loops=pathsFor(m).filter((p)=>p.role==='radiator');
    assert.equal(loops.length,2);
    loops.forEach((p)=>near(norm(sub(p.points[0],p.points.at(-1))),config.feedGapMm));
    near(Math.max(...loops.flatMap((p)=>p.points.map((v)=>v[2]))),m.heightMm);
    assert.equal(pathsFor(m).filter((p)=>p.role==='reflector').length,4);
  }
});

test('QFH half-turn lengths account for both helices, bars and feed gaps', () => {
  for(const m of models.filter((m)=>m.type==='qfh')) {
    m.loops.forEach((loop,index)=>{
      near(loop.heightMm/loop.diameterMm,1.6);
      near(2*loop.helicalSideMm+2*loop.diameterMm,loop.lengthMm);
      near(loop.conductorMm+config.feedGapMm,loop.lengthMm);
      near(loop.maxHelixSegmentMm*4,loop.helicalSideMm);
      near(loop.bottomMm+loop.heightMm/2,m.loops[0].bottomMm+m.loops[0].heightMm/2);
      const bars=pathsFor(m).filter((p)=>p.loop===index && p.points.length===2);
      assert.equal(bars.length,3);
      near(norm(sub(bars[1].points[1],bars[2].points[1])),config.feedGapMm);
    });
  }
});

test('different feed loops have no conductor intersections in their actual sampled CAD paths', () => {
  for(const m of models) {
    const paths=pathsFor(m).filter((p)=>p.role==='radiator');
    let minimum=Infinity;
    for(const a of paths.filter((p)=>p.loop===0)) for(const b of paths.filter((p)=>p.loop===1)) {
      for(let i=1;i<a.points.length;i++) for(let j=1;j<b.points.length;j++) {
        minimum=Math.min(minimum,segmentDistance(a.points[i-1],a.points[i],b.points[j-1],b.points[j]));
      }
    }
    assert.ok(minimum>config.conductorDiameterMm+0.1,`${m.id}: loop separation ${minimum} mm`);
    for(const p of paths) for(const v of p.points) {
      assert.ok(v.every(Number.isFinite));
      assert.ok(v[2]>=0 && v[2]<=m.heightMm+1e-6);
    }
  }
});

test('sampled paths approximate seed conductor lengths within tessellation error', () => {
  for(const m of models) for(let loop=0;loop<2;loop++) {
    const length=pathsFor(m).filter((p)=>p.role==='radiator' && p.loop===loop).reduce((total,p)=>
      total+p.points.slice(1).reduce((sum,v,i)=>sum+norm(sub(v,p.points[i])),0),0);
    const expected=m.type==='eggbeater'?m.conductorPerLoopMm:m.loops[loop].conductorMm;
    assert.ok(Math.abs(length-expected)/expected<0.0003,`${m.id}: ${length} vs ${expected}`);
  }
});

test('CAD parameters, two BOMs, report and eight branded views exactly regenerate', () => {
  for(const [file,content] of outputs()) assert.equal(lf(read(file)),lf(content),file);
  for(const type of ['eggbeater','qfh']) {
    const rows=parseCsv(read(`bom/antenna-${type}.csv`));
    assert.equal(new Set(rows.map((r)=>r.id)).size,rows.length);
    assert.ok(rows.every((r)=>Number(r.quantity)>0 && r.status==='DESIGN_AND_RF_HOLD'));
    for(const m of models.filter((m)=>m.type===type)) {
      assert.equal(rows.find((r)=>r.id===`${m.id}-01`).quantity,'16');
      const prefix=`${m.id}-`;
      assert.equal(rows.filter((r)=>r.id.startsWith(prefix) && /preamp/.test(r.component)).length,1);
    }
  }
  const preamps=parseCsv(read('bom/antenna-preamps.csv'));
  assert.equal(preamps.length,10);
  assert.ok(preamps.every((r)=>r.status.endsWith('HOLD')));
});

test('all option CAD previews exist and support coupon is a closed connected solid', () => {
  for(const m of models) {
    validateRenderedPng(path.join(root,`docs/assembly/options/${m.id}-cad.png`));
  }
  const support=validateStl(path.join(root,'cad/options-stl/support.stl'));
  assert.equal(support.components,1);
  assert.ok(support.volume>2000);
});

test('antenna guides resolve local links and do not claim released RF or packed volume', () => {
  const files=['ANTENNA-OPTIONS','ANTENNA-EGGBEATER','ANTENNA-QFH','ANTENNA-PREAMPS','SATELLITE-COMMS','ANTENNA-PORTABLE'];
  for(const name of files) {
    const file=`docs/${name}.md`,s=read(file);
    for(const match of s.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
      const target=match[1].split('#')[0];
      if(!target || /^[a-z]+:/i.test(target)) continue;
      assert.ok(fs.existsSync(path.resolve(root,path.dirname(file),target)),`${file}: ${target}`);
    }
  }
  for(const name of ['EGGBEATER','QFH']) assert.match(read(`docs/ANTENNA-${name}.md`),/no.*envolvente|No hay envolvente/i);
  const guide=read('docs/ANTENNA-PREAMPS.md').replace(/\s+/g,' ');
  for(const term of ['HOLD','retorno','25 W','otra banda','No se ha modificado firmware']) assert.ok(guide.toLowerCase().includes(term.toLowerCase()),term);
  assert.match(read('docs/SATELLITE-COMMS.md'),/59,98 dB/);
});

test('invalid parameters fail explicitly and power ceiling cannot silently increase', () => {
  for(const mutate of [
    (c)=>c.frequenciesMHz[0]=-145,
    (c)=>c.feedGapMm=4,
    (c)=>c.feedGapMm=1000,
    (c)=>c.qfh.heightToDiameter=NaN,
    (c)=>c.qfh.turnsPerSide=1,
    (c)=>c.eggbeater.segmentsPerLoop=4.5,
    (c)=>c.power.maxConductedW=50
  ]) {
    const bad=structuredClone(config);mutate(bad);
    assert.throws(()=>calculate(bad),/Invalid|Feed gap/);
  }
});
