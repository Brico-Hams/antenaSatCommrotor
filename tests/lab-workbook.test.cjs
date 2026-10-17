const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { tests, outputs, statuses, writeTemplates } = require('../scripts/lab-workbook.cjs');
const os = require('node:os');
const { entries, parseCsv } = require('../scripts/component-catalog.cjs');
const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root,file),'utf8');
const readCsv = (name) => parseCsv(read(`docs/testing/laboratorio/${name}.csv`).replace(/^\ufeff/,''));

test('lab workbook covers all existing test headings plus 24 complete supplemental procedures', () => {
  const all=tests();
  assert.equal(new Set(all.map((t)=>t.id)).size,all.length);
  assert.equal(all.length,101);
  assert.equal(all.filter((t)=>t.id.startsWith('LAB-')).length,24);
  const historical=parseCsv(read('docs/testing/registro-pruebas.csv'));
  assert.deepEqual(new Set(all.filter((t)=>!t.id.startsWith('LAB-')).map((t)=>t.id)),
    new Set(historical.map((t)=>t.id)));
  for(const t of all) {
    for(const key of ['action','expected','criterion','procedure']) assert.ok(t[key].length>10,`${t.id}: ${key}`);
    assert.ok(fs.existsSync(path.join(root,'docs/testing',t.guide)));
  }
});

test('each BOM row has a blank unit-level disposition without inferring functional qualification', () => {
  const rows=readCsv('componentes'),all=entries();
  assert.equal(rows.length,all.length);
  assert.equal(new Set(rows.map((r)=>r.catalogo_id)).size,all.length);
  rows.forEach((r,i)=>{
    assert.equal(r.catalogo_id,all[i].key);
    assert.equal(r.bom_fuente,all[i].source);
    assert.equal(Number(r.fila_fuente),all[i].row);
    assert.equal(r.bom_id,all[i].id);
    assert.equal(r.inspeccion_requerida,'LAB-01');
    for(const key of ['seleccionado_si_no','motivo_exclusion','unidad_serie_lote_posicion','modelo_revision_real',
      'ensayos_asignados_por_revisor','ejecuciones_ids','firma']) assert.equal(r[key],'',`${r.catalogo_id}: ${key}`);
    assert.equal(r.estado,'PENDIENTE');
  });
});

test('result, reading and calibration templates contain no fabricated measurements, identity or approvals', () => {
  const results=readCsv('resultados');
  assert.deepEqual(results.map((r)=>r.ensayo_id),tests().map((t)=>t.id));
  const allowed=new Set(['ensayo_id','guia','accion','esperado','criterio_fuente','estado']);
  for(const r of results) for(const [key,value] of Object.entries(r)) {
    if(!allowed.has(key)) assert.equal(value,'',`${r.ensayo_id}: ${key}`);
  }
  for(const name of ['resultados','lecturas','calibraciones','instrumentos']) {
    const rows=readCsv(name);
    assert.ok(rows.length>0);
    for(const r of rows) {
      assert.equal(r.estado,'PENDIENTE');
      for(const key of ['lectura_bruta','resultado','correccion','u_expandida','factor_k',
        'incertidumbre_expandida','as_found','as_left','ajuste','fecha_utc','operador','firma',
        'certificado_id','fecha_calibracion','vencimiento','ejecucion_id']) {
        if(key in r) assert.equal(r[key],'',`${name}: ${key}`);
      }
    }
  }
  assert.deepEqual(statuses,['PENDIENTE','BLOQUEADO','INDETERMINADO','APROBADO','RECHAZADO','NO_APLICA']);
  assert.ok(readCsv('lecturas').every((r)=>tests().some((t)=>t.id===r.ensayo_id)));
});

test('printable workbook provides one blank evidence sheet per test and repeatable source criteria', () => {
  const html=read('docs/testing/laboratorio/cuaderno.html');
  assert.equal((html.match(/<section class="sheet">/g)||[]).length,tests().length);
  assert.equal((html.match(/<tr><td><\/td><td><\/td><td><\/td><td><\/td><\/tr>/g)||[]).length,tests().length*6);
  assert.match(html,/@page\{size:A4/);
  assert.match(html,/page-break-after:always/);
  assert.match(html,/NO evidencia de ensayo/);
  assert.ok(!/<script|<form/i.test(html),'Printable only, no misleading persistence');
});

test('generated lab templates regenerate exactly and generator refuses overwriting modified records', () => {
  for(const [file,content] of outputs()) assert.equal(read(file),content,file);
  const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'bricohams-lab-test-'));
  try {
    const files=new Map([['resultados.csv','plantilla'],['lecturas.csv','blanco']]);
    assert.throws(()=>writeTemplates(files,temporary,true),/Missing or modified/);
    assert.deepEqual(fs.readdirSync(temporary),[]);
    writeTemplates(files,temporary);
    writeTemplates(files,temporary,true);
    writeTemplates(files,temporary);
    fs.writeFileSync(path.join(temporary,'resultados.csv'),'MEDICIONES REALES');
    const expanded=new Map([['nuevo.csv','no crear si hay conflicto'],...files]);
    assert.throws(()=>writeTemplates(expanded,temporary),/Preserve filled records/);
    assert.equal(fs.readFileSync(path.join(temporary,'resultados.csv'),'utf8'),'MEDICIONES REALES');
    assert.ok(!fs.existsSync(path.join(temporary,'nuevo.csv')));
  } finally {
    fs.rmSync(temporary,{recursive:true});
  }
});

test('lab protocols and generated index resolve local markdown links', () => {
  for(const file of [
    'docs/testing/09-laboratorio.md','docs/testing/10-nanovna.md','docs/testing/11-rf-potencia.md',
    'docs/testing/12-calibraciones.md','docs/testing/13-ensayos-laboratorio.md',
    'docs/testing/laboratorio/README.md','docs/testing/README.md','docs/VALIDATION.md'
  ]) {
    for(const m of read(file).matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
      const target=m[1].split('#')[0];
      if(!target||/^[a-z]+:/i.test(target))continue;
      assert.ok(fs.existsSync(path.resolve(root,path.dirname(file),target)),`${file}: ${target}`);
    }
  }
});

test('procedures explicitly bound NanoVNA, uncertainty, active RF and calibration claims', () => {
  const vna=read('docs/testing/10-nanovna.md');
  for(const term of ['patrones independientes','S11/S21','S22/S12','suelo','THRU','PA','fase','50 ciclos']) {
    assert.ok(vna.includes(term),term);
  }
  const rf=read('docs/testing/11-rf-potencia.md');
  for(const term of ['24,975 W','NO_MEDIDA','59,98 dB','IMD','LSB','RHCP/LHCP','break-before-make']) assert.ok(rf.includes(term),term);
  const cal=read('docs/testing/12-calibraciones.md');
  for(const term of ['OTP','ACK','chopper','Wh','LCR','caducidad','antes','despues']) assert.ok(cal.includes(term),term);
  const plan=read('docs/testing/09-laboratorio.md');
  for(const term of ['INDETERMINADO','BLOQUEADO','SHA-256','incertidumbre','cada unidad','HOLD']) assert.ok(plan.includes(term),term);
});
