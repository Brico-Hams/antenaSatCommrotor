const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,...p.split('/')),'utf8').replace(/^\uFEFF/,'');
const data=JSON.parse(read('hardware/connectivity.json'));
const release=JSON.parse(read('fabrication/release-status.json'));
test('carrier has original real copper connectivity and physical locator holes',()=>{
  assert.deepEqual(data.board_mm,[180,130]);
  assert.deepEqual(data.holes_mm,[[5,5],[175,5],[5,125],[175,125]]);
  assert.equal(data.router.unrouted.length,0);
  assert.ok(data.router.segments>500);
  const pcb=read('hardware/PortableSatCarrier.kicad_pcb');
  assert.ok((pcb.match(/\(segment /g)||[]).length>500);
  assert.ok((pcb.match(/\(via /g)||[]).length>0);
  assert.equal((pcb.match(/\(at 11\.25 0\) \(size 2\.7 2\.7\) \(drill 2\.7\)/g)||[]).length,4);
});
test('official KiCad report gate is zero, includes parity and no silent exclusions',()=>{
  assert.equal(release.cad_verified,true);
  assert.equal(release.production_release,false);
  assert.equal(release.assembly_operation_release,false);
  const drc=JSON.parse(read('fabrication/reports/drc.json'));
  const erc=JSON.parse(read('fabrication/reports/erc.json'));
  assert.equal(drc.violations.length,0);
  assert.equal(drc.unconnected_items.length,0);
  assert.equal(drc.schematic_parity.length,0);
  assert.equal(erc.sheets.flatMap(s=>s.violations||[]).length,0);
  assert.ok(drc.included_severities.includes('error'));
  assert.ok(drc.included_severities.includes('warning'));
});
test('Gerbers, drill, netlist and sources are bound to validated SHA256 manifest',()=>{
  for(const [file,hash] of Object.entries(release.sha256)) {
    const b=fs.readFileSync(path.join(root,...file.split('/')));
    assert.equal(crypto.createHash('sha256').update(b).digest('hex'),hash,file+' changed after verification');
  }
  for(const ext of ['gtl','gbl','gts','gbs','gto','gbo','gm1']) {
    const dir=path.join(root,'fabrication','gerbers');
    const f=fs.readdirSync(dir).find(f=>f.endsWith('.'+ext));
    assert.ok(f,'Missing fabrication layer '+ext);
    const s=fs.readFileSync(path.join(dir,f),'utf8');
    assert.ok(s.includes('M02*'));
    if(ext==='gtl'||ext==='gbl')assert.ok((s.match(/D0[13]\*/g)||[]).length>500,'Copper cannot be an outline-only dummy');
  }
  const drills=fs.readdirSync(path.join(root,'fabrication','gerbers')).filter(f=>f.endsWith('.drl'));
  assert.ok(drills.some(f=>f.includes('NPTH')));
  assert.ok(drills.some(f=>f.includes('PTH')&&!f.includes('NPTH')));
  for(const f of drills)assert.ok(read('fabrication/gerbers/'+f).includes('M48'));
  assert.ok(read('fabrication/PortableSatCarrier.net').includes('AZ_STEP'));
  const job=JSON.parse(read('fabrication/gerbers/PortableSatCarrier-job.gbrjob'));
  assert.equal(job.GeneralSpecs.LayerNumber,2);
  assert.deepEqual(job.MaterialStackup.filter(l=>l.Type==='Copper').map(l=>l.Thickness),[.07,.07]);
});
test('exact official 38pin ESP32 map matches firmware, never strap/flash pins',()=>{
  const u1=data.parts.find(p=>p.ref==='U1');
  assert.equal(u1.pins.length,38);
  const mapping={azStep:26,azDir:27,elStep:14,elDir:13,enable:25,estop:34,azMin:35,azMax:36,
    elMin:39,elMax:32,gpsRx:16,gpsTx:17,azSda:21,azScl:22,elSda:18,elScl:19};
  const cfg=read('firmware/include/board_config.h');
  for(const [name,gpio] of Object.entries(mapping))assert.match(cfg,new RegExp('\\b'+name+'\\s*=\\s*'+gpio+'\\b'),name);
  assert.equal(u1.pins[2].net,'AZ_MAX_N');
  assert.equal(u1.pins[3].net,'EL_MIN_N');
  assert.equal(u1.pins[29].net,'GNSS_RX');
  assert.equal(u1.pins[30].net,'GNSS_TX');
});
test('motor power cutoff is actual independent series branch, sensor rail never 5V',()=>{
  const p=ref=>data.parts.find(p=>p.ref===ref).pins.map(p=>p.net);
  assert.deepEqual(p('J2'),['STOP_SEND','VMOT']);
  assert.deepEqual(p('J3'),['STOP_N','GND']);
  assert.deepEqual(p('F2'),['FUSED12','STOP_SEND']);
  assert.deepEqual(p('D2'),['GND','FUSED12']);
  for(const ref of ['U2','U3']) {
    assert.deepEqual(p(ref).slice(0,4),['ENABLE_N','3V3','3V3','GND']);
    assert.equal(p(ref)[8],'VMOT');
    assert.equal(p(ref)[14],'3V3');
  }
  for(const ref of ['J6','J7','J8','J9'])assert.deepEqual(p(ref).slice(0,2),['3V3','GND']);
  assert.deepEqual(p('JP1'),['FUSED5','ESP5']);
  assert.equal(data.parts.filter(p=>p.value==='10k').length,6);
});
