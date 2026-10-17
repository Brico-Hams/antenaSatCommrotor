const fs = require('node:fs');
const path = require('node:path');
const { entries } = require('./component-catalog.cjs');
const root = path.resolve(__dirname, '..');
const directory = 'docs/testing/laboratorio';
const guides = [
  '02-electronica.md', '03-puerta-pcb.md', '04-mecanica.md', '05-rf-y-radio.md',
  '06-software-y-os.md', '07-app-android.md', '08-sistema.md', '13-ensayos-laboratorio.md'
];
const statuses = ['PENDIENTE', 'BLOQUEADO', 'INDETERMINADO', 'APROBADO', 'RECHAZADO', 'NO_APLICA'];
const csv = (rows) => '\ufeff' + rows.map((row) => row.map((v) =>
  `"${String(v).replace(/"/g, '""')}"`).join(',')).join('\r\n') + '\r\n';
const html = (text) => String(text).replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
function tests() {
  const result = [];
  for (const guide of guides) {
    const text = fs.readFileSync(path.join(root, 'docs/testing', guide), 'utf8');
    for (const block of text.split(/^### /m).slice(1)) {
      const id = block.split(/\r?\n/, 1)[0].trim();
      if (!/^(PWR|DRV|SNS|PCB|MEC|ANT|RAD|SW|APP|SYS|LAB)-\d{2}$/.test(id)) {
        throw new Error(`Invalid lab test heading: ${guide}: ${id}`);
      }
      const field = (label) => {
        const match = block.match(new RegExp(`\\*\\*${label}:\\*\\*\\s*([^\\r\\n]+)`));
        if (!match) throw new Error(`Missing ${label}: ${id}`);
        return match[1].trim();
      };
      result.push({ id, guide, action: field('Acción'), expected: field('Esperado'),
        criterion: field('Criterio de aprobación'),
        procedure: guide === '13-ensayos-laboratorio.md' ? field('Procedimiento') : guide });
    }
  }
  if (new Set(result.map((t) => t.id)).size !== result.length) throw new Error('Duplicate lab test ID');
  return result;
}

function outputs() {
  const all = tests();
  const components = entries();
  const files = new Map();
  const add = (name, rows) => files.set(`${directory}/${name}.csv`, csv(rows));
  const resultHeaders = ['ejecucion_id','ensayo_id','guia','accion','esperado','criterio_fuente',
    'lote','fecha_utc','operador','revisor','variante','revision_git_y_dirty','dut_serie_posicion',
    'bom_ids','configuracion_firmware','montaje_revision','instrumentos_ids','calibraciones_ids',
    'ambiente','frecuencia_mhz','puertos_sentido','modo','potencia_w','duracion_s','duty_pct',
    'limite_inferior','limite_superior','unidad','criterio_aprobado_por','lectura_bruta',
    'correccion','resultado','incertidumbre_expandida','factor_k','metodo_incertidumbre',
    'regla_decision','evidencias_ids','desviacion_accion','estado','firma'];
  add('resultados', [resultHeaders, ...all.map((t) => resultHeaders.map((key) => ({
    ensayo_id: t.id, guia: t.guide, accion: t.action, esperado: t.expected,
    criterio_fuente: t.criterion, estado: 'PENDIENTE'
  })[key] || ''))]);
  add('componentes', [
    ['catalogo_id','bom_fuente','fila_fuente','bom_id','componente','cantidad_bom','especificacion',
      'nota_bom','seleccionado_si_no','motivo_exclusion','unidad_serie_lote_posicion','modelo_revision_real',
      'inspeccion_requerida','ensayos_asignados_por_revisor','ejecuciones_ids','estado','firma'],
    ...components.map((c) => [c.key,c.source,c.row,c.id,c.name,c.quantity,c.detail,c.note,
      '','','','','LAB-01','','','PENDIENTE',''])
  ]);
  const instruments = [
    ['EQ-L01','NanoVNA y kit SOL/THRU'],['EQ-L02','Patrones independientes carga y atenuador'],
    ['EQ-L03','DMM y referencia DC'],['EQ-L04','Fuente limitada y carga electronica'],
    ['EQ-L05','Osciloscopio y sondas/diferencial/corriente'],['EQ-L06','Analizador logico'],
    ['EQ-L07','Termopar o camara termica y referencia'],['EQ-L08','Calibre/comparador/goniómetro/masas/bascula/par'],
    ['EQ-L09','Generador RF y referencia de frecuencia'],['EQ-L10','Vatimetro/acoplador/sensor'],
    ['EQ-L11','Carga RF/atenuadores/filtros/limitadores'],['EQ-L12','Analizador espectro/NF y fuente ENR si procede'],
    ['EQ-L13','Referencia antena/posicionador/campo'],['EQ-L14','Referencia UTC/PPS/norte'],
    ['EQ-L15','Audio/PC/telefonos y herramientas software']
  ];
  add('instrumentos', [
    ['equipo_id','funcion','fabricante_modelo','serie','firmware','manual_revision','rango',
      'max_entrada_dc_rf','incertidumbre_certificado','certificado_id','fecha_calibracion',
      'vencimiento','verificacion_antes_id','verificacion_despues_id','apto_por','estado'],
    ...instruments.map(([id, name]) => [id,name,...Array(13).fill(''),'PENDIENTE'])
  ]);
  add('calibraciones', [
    ['calibracion_id','ensayo_id','ejecucion_id','equipo_id','fecha_utc','operador','patron_serie_certificado',
      'metodo_revision','plano_cables_adaptadores','rango_inicio','rango_fin','puntos','nivel_ifbw_promedio',
      'temperatura','valor_patron','tolerancia','as_found','ajuste','as_left','correccion','unidad',
      'incertidumbre_expandida','factor_k','verificacion_independiente_antes','verificacion_despues',
      'vigencia_condiciones','archivo_estado_cal','evidencia_id','estado','firma'],
    ...['LAB-02','LAB-06','LAB-12','LAB-14'].map((id) => [
      '',id,...Array(26).fill(''),'PENDIENTE',''])
  ]);
  const readingHeaders = ['ejecucion_id','ensayo_id','dut_unidad','punto_repeticion','fecha_utc',
    'frecuencia_mhz','puerto_entrada','puerto_salida','otros_puertos_terminados','estado_ruta',
    'magnitud','lectura_bruta','correccion','resultado','unidad','u_expandida','k','limite_inferior',
    'limite_superior','potencia_w','duracion_s','duty_pct','temperatura_amb_c','temperatura_dut_c',
    'referencia','evidencia_id','estado'];
  const reading = (id, point = '', frequency = '') => readingHeaders.map((key) =>
    ({ ensayo_id:id, punto_repeticion:point, frecuencia_mhz:frequency, estado:'PENDIENTE' })[key] || '');
  add('lecturas', [readingHeaders, ...all.map((t) => reading(t.id)),
    ...[144,145,145.85,145.99,146,430,432.125,432.175,435,436.795,437.8,440]
      .map((f) => reading('LAB-03','CANAL_REFERENCIA_NO_AUTORIZA_TX',f))]);
  add('evidencias', [
    ['evidencia_id','ejecucion_id','fecha_utc','ruta_relativa','tipo','sha256','instrumento_exportacion',
      'descripcion_montaje','operador','original_o_derivado'],
    Array(10).fill('')
  ]);

  const line = (label) => `<div class="line"><b>${html(label)}</b><span></span></div>`;
  const pages = all.map((t) => `<section class="sheet">
<header><strong>BricoHams | ${html(t.id)}</strong><small>Laboratorio · bricohams.org | PENDIENTE</small></header>
${line('Lote / ejecucion / fecha UTC / operador / revisor:')}
${line('Variante / Git y dirty / firmware / DUT serie-posicion:')}
${line('BOM IDs-unidades / montaje-revision / ambiente:')}
${line('Instrumentos-series / calibraciones antes-despues / evidencias:')}
<p><b>Prerrequisito:</b> autorizacion y etapa previa aceptadas; ratings y capacidad de medida confirmados. PA/motores inhibidos salvo etapa autorizada. Si falta algo: BLOQUEADO.</p>
<p><b>Accion:</b> ${html(t.action)}</p>
<p><b>Esperado:</b> ${html(t.expected)}</p>
<p><b>Criterio de referencia:</b> ${html(t.criterion)}</p>
<p><b>Procedimiento:</b> ${html(t.procedure)} | Guia <a href="../${html(t.guide)}">${html(t.guide)}</a>. Antes de trabajar consultar 09-12; conexion/ratings segun DUT exacto.</p>
${line('Limites/unidades/fuente-revision aprobados ANTES / responsable:')}
${line('Ajustes: rango/puntos/plano/puertos/nivel/modo/potencia/duty/duracion:')}
<table><thead><tr><th>Punto, f, puerto, sentido, repeticion</th><th>Lectura bruta / unidad</th><th>Correccion / resultado</th><th>U / k / evidencia</th></tr></thead>
<tbody>${'<tr><td></td><td></td><td></td><td></td></tr>'.repeat(6)}</tbody></table>
${line('Metodo U / regla de decision / repetibilidad / verificacion posterior:')}
${line('Paradas/fallos/desviacion/accion correctiva / repeticion nueva ID:')}
${line('Estado: PENDIENTE / BLOQUEADO / INDETERMINADO / APROBADO / RECHAZADO / NO_APLICA')}
${line('Conclusion, alcance y firma operador / revisor:')}
<footer>Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina | Hoja en blanco: NO evidencia de ensayo.</footer>
</section>`).join('\n');
  files.set(`${directory}/cuaderno.html`, `<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>BricoHams | Cuaderno de laboratorio rellenable</title>
<style>
@page{size:A4;margin:12mm}*{box-sizing:border-box}body{font:10pt Arial,sans-serif;color:#12263f;margin:0;background:#eee}
.sheet{background:white;width:186mm;min-height:273mm;margin:8mm auto;padding:5mm;break-after:page;page-break-after:always}
.sheet:last-child{break-after:auto;page-break-after:auto}header{border-bottom:2px solid #e8871e;margin-bottom:3mm;padding-bottom:2mm}
header strong{font-size:15pt}small{display:block;font-size:9pt;margin-top:1mm}p{margin:2mm 0;line-height:1.25}
.line{margin:2mm 0;font-size:8.5pt;min-height:9mm}.line span{display:block;border-bottom:1px solid #9aa6b2;min-height:4mm}
table{border-collapse:collapse;width:100%;table-layout:fixed;font-size:8pt}th,td{border:1px solid #9aa6b2;padding:1mm}td{height:7mm}
footer{border-top:1px solid #12263f;margin-top:3mm;font-size:7.5pt;padding-top:2mm}
@media print{body{background:white}.sheet{margin:0;padding:0;width:186mm;min-height:0}a{color:inherit;text-decoration:none}}
</style></head><body>${pages}</body></html>\n`);
  files.set(`${directory}/README.md`, `# BricoHams: plantillas de laboratorio\n\n` +
    `Generadas por [lab-workbook.cjs](../../../scripts/lab-workbook.cjs). **${all.length} ensayos y ${components.length} filas BOM**, todos PENDIENTES.\n\n` +
    `Copiar esta carpeta a un expediente nuevo antes de rellenar. No editar/regenerar sobre resultados reales.\n` +
    `Ver [procedimiento de uso y decision](../09-laboratorio.md), [NanoVNA](../10-nanovna.md), [RF activa](../11-rf-potencia.md) y [calibraciones](../12-calibraciones.md).\n\n` +
    `| Archivo | Uso |\n| --- | --- |\n` +
    `| [cuaderno.html](cuaderno.html) | Imprimir A4, una pagina por ensayo; campos manuscritos, sin guardado interactivo |\n` +
    `| [resultados.csv](resultados.csv) | Cabecera y conclusion por ejecucion; duplicar filas para repeticiones/unidades |\n` +
    `| [lecturas.csv](lecturas.csv) | Valores brutos/corregidos, U/k y condiciones por punto; filas extra para canales de referencia, no autorizacion TX |\n` +
    `| [componentes.csv](componentes.csv) | Seleccion/exclusion de TODAS las filas BOM; expandir por unidad y asignar ensayos revisados |\n` +
    `| [instrumentos.csv](instrumentos.csv) | Equipos/patrones, series, ratings, certificados y vigencia; expandir grupos |\n` +
    `| [calibraciones.csv](calibraciones.csv) | As found/ajuste/as left y verificacion independiente antes/despues |\n` +
    `| [evidencias.csv](evidencias.csv) | Fotos, S1P/S2P, capturas, logs y SHA-256 |\n\n` +
    `Estados: ${statuses.join(', ')}. Un blanco no significa cero, ni aprobado, ni no aplicable.\n\n` +
    `El cuaderno referencia guias relativas a la carpeta original. En una copia externa consultar los procedimientos desde el repositorio y registrar su revision; las fichas incluyen accion/criterio pero no reemplazan los manuales.\n\n` +
    `## Indice de fichas\n\n| ID | Guia / accion |\n| --- | --- |\n` +
    all.map((t) => `| ${t.id} | [${t.guide}](../${t.guide}) · ${t.action.replace(/\|/g,'/')} |`).join('\n') + '\n');
  return files;
}

function writeTemplates(files, base = root, check = false) {
  // Never overwrite a filled or otherwise modified worksheet.
  for (const [file, content] of files) {
    const target = path.join(base, file);
    if (fs.existsSync(target) && fs.readFileSync(target,'utf8') === content) continue;
    if (check || fs.existsSync(target)) throw new Error(`Missing or modified lab template: ${file}. Preserve filled records; generate in a clean checkout.`);
  }
  if (!check) for (const [file, content] of files) {
    const target = path.join(base,file);
    if (!fs.existsSync(target)) {
      fs.mkdirSync(path.dirname(target),{recursive:true});
      fs.writeFileSync(target,content,{flag:'wx'});
    }
  }
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.some((a) => a !== '--check')) throw new Error('Usage: node scripts/lab-workbook.cjs [--check]');
  const check = args.includes('--check');
  writeTemplates(outputs(), root, check);
  console.log(`Lab templates ${check ? 'verified' : 'generated'}: ${tests().length} tests; ${entries().length} BOM rows; no measurements fabricated.`);
}
module.exports = { tests, outputs, statuses, writeTemplates };
