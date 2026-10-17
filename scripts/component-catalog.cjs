const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const output = 'docs/assembly/components';
const sources = [
  { key: 'electrical', file: 'bom/electrical.csv', title: 'Control ESP32 (no CM5)', id: 'id', name: 'component', quantity: 'quantity', detail: 'selection_constraint', note: 'notes' },
  { key: 'mechanical', file: 'bom/mechanical.csv', title: 'Mecanica BASE y LEGACY: no sumar alternativas', id: 'id', name: 'description', quantity: 'qty', detail: 'material', note: 'notes' },
  { key: 'portable', file: 'bom/antenna-portable.csv', title: 'Antena PF-01 portable: alternativa candidata, no sumar a la antena anterior', id: 'id', name: 'component', quantity: 'quantity', detail: 'specification', note: 'notes' },
  { key: 'eggbeater', file: 'bom/antenna-eggbeater.csv', title: 'Eggbeater TX/RX: dos bandas separadas, no sumar a PF-01', id: 'id', name: 'component', quantity: 'quantity', detail: 'specification', note: 'notes' },
  { key: 'qfh', file: 'bom/antenna-qfh.csv', title: 'QFH TX/RX: dos bandas separadas, no sumar a Eggbeater', id: 'id', name: 'component', quantity: 'quantity', detail: 'specification', note: 'notes' },
  { key: 'preamps', file: 'bom/antenna-preamps.csv', title: 'Previo RX y bypass TX: 25 W pendiente de cualificacion', id: 'id', name: 'component', quantity: 'quantity', detail: 'specification', note: 'notes' },
  { key: 'multimode', file: 'bom/multimode-assembly.csv', title: 'Conjunto CM5 multimodo: diseno en revision', id: 'item_id', name: 'component_or_material', quantity: 'quantity', detail: 'selection_or_interface', note: 'status' },
  { key: 'pcb', file: 'bom/pcb.csv', title: 'PCB ESP32: HOLD de fabricacion', id: 'Reference', name: 'Value', quantity: 'Quantity', detail: 'Manufacturer_part', note: 'Notes' },
  { key: 'polarization', file: 'bom/polarization.csv', title: 'POL, sensores y redes RF: concepto no cualificado', id: 'ID', name: 'Component', quantity: 'Quantity', detail: 'Material or specification', note: 'Status and notes' },
  { key: 'rf', file: 'bom/rf.csv', title: 'RF: referencias, alternativas y herramientas', id: 'id', name: 'valor_o_modelo', quantity: 'cantidad', detail: 'banda_o_limite', note: 'estado' },
  { key: 'cm5', file: 'hardware/cm5/fabrication/NOT_FOR_MANUFACTURE/JLCPCB-BOM-REVIEW.csv', title: 'Auxiliar CM5: NO FABRICAR / NO ENERGIZAR', id: 'Designator', name: 'Comment', quantity: 'Quantity', detail: 'Manufacturer Part', note: 'Footprint' },
  { key: 'lite', file: 'PortableSatLite/bom/bom.csv', title: 'PortableSatLite independiente: no mezclar con BASE', name: 'item', quantity: 'qty', detail: 'spec', note: 'notes' }
];

function parseCsv(text) {
  const rows = [];
  let row = [], value = '', quoted = false, closed = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { value += '"'; i++; }
      else if (c === '"') { quoted = false; closed = true; }
      else value += c;
    } else if (c === '"' && !value && !closed) {
      quoted = true;
    } else if (c === ',' || c === '\n' || c === '\r') {
      row.push(value); value = ''; closed = false;
      if (c !== ',') {
        if (row.some((field) => field !== '')) rows.push(row);
        row = [];
        if (c === '\r' && text[i + 1] === '\n') i++;
      }
    } else {
      if (closed || c === '"') throw new Error(`Invalid CSV quoting at character ${i}`);
      value += c;
    }
  }
  if (quoted) throw new Error('Unclosed CSV field');
  if (value || row.length || closed) { row.push(value); rows.push(row); }
  const header = rows.shift();
  if (!header || new Set(header).size !== header.length) throw new Error('Invalid CSV header');
  return rows.map((fields, i) => {
    if (fields.length !== header.length) throw new Error(`CSV row ${i + 2}: expected ${header.length} columns, got ${fields.length}`);
    return Object.fromEntries(header.map((name, index) => [name, fields[index]]));
  });
}

const xml = (value) => String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[c]);
const md = (value) => String(value).replace(/\|/g, '\\|').replace(/[\r\n]+/g, ' ').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function wrap(value, width) {
  const words = String(value).match(new RegExp(`\\S{1,${width}}`, 'g')) || [];
  const lines = [];
  for (const word of words) {
    if (!lines.length || lines[lines.length - 1].length + word.length + 1 > width) lines.push(word);
    else lines[lines.length - 1] += ` ${word}`;
  }
  return lines;
}

function symbol(text) {
  if (/motor|nema|stepper/i.test(text)) return ['Motor', '<rect x="52" y="42" width="136" height="136" rx="12"/><circle cx="120" cy="110" r="40"/><path d="M120 110v-65M80 178v28m80-28v28"/>'];
  if (/bearing|rodamiento|608|6000/i.test(text)) return ['Rodamiento / apoyo', '<circle cx="120" cy="120" r="85"/><circle cx="120" cy="120" r="44"/><circle cx="120" cy="56" r="12"/><circle cx="184" cy="120" r="12"/><circle cx="120" cy="184" r="12"/><circle cx="56" cy="120" r="12"/>'];
  if (/belt|correa|pulley|polea|gt2/i.test(text)) return ['Transmision', '<path d="M65 55h100a65 65 0 0 1 0 130H65a65 65 0 0 1 0-130Z"/><circle cx="65" cy="120" r="38"/><circle cx="165" cy="120" r="48"/><path d="M65 105v30m100-30v30"/>'];
  if (/shaft|eje|tube|tubo|boom|mastil|varilla|rod /i.test(text)) return ['Elemento longitudinal', '<path d="M40 65l155 80v35L40 100Z"/><ellipse cx="40" cy="82" rx="18" ry="24"/><path d="M55 65l155 80"/>'];
  if (/battery|bateria|lifepo|dc supply/i.test(text)) return ['Energia', '<rect x="35" y="60" width="170" height="145" rx="10"/><path d="M60 60V40h28v20m64 0V40h28v20M60 105h35m-18-18v36m70-18h35"/>'];
  if (/antenna|antena|reflector|driven|elementos|balun|hibrido|hybrid|diplex|coax|sma|bnc|rf|lime|sdr|load|vna/i.test(text)) return ['Radiofrecuencia', '<path d="M120 205V45M50 65h140M65 105h110M80 145h80M95 185h50"/><path d="M30 35q-40 85 0 170m180-170q40 85 0 170"/>'];
  if (/screw|tornill|fasten|tuerca|insert|perno|pasador|clamp/i.test(text)) return ['Fijacion', '<path d="M85 30h70v35H85Zm15 35h40v145h-40Zm0 25 40 20m-40 10 40 20m-40 10 40 20m-40 10 40 20"/>'];
  if (/case|caja|enclosure|tapa|cuna|cradle|shield/i.test(text)) return ['Carcasa / soporte', '<path d="M35 80l100-45 75 45-100 45Zm0 0v100l75 40 100-40V80m-100 45v95"/><path d="m55 57 80-37 55 32"/>'];
  if (/resistor|resistencia|^r\d|10k|4k7|4\.7k|^1[mk]$/i.test(text)) return ['Resistencia', '<path d="M15 120h50m110 0h50"/><rect x="65" y="90" width="110" height="60"/><path d="M92 90v60m25-60v60m35-60v60"/>'];
  if (/capacitor|^c\d|^100n|^1u|^220u/i.test(text)) return ['Condensador', '<path d="M20 120h75m50 0h75M95 65v110m50-110v110"/>'];
  if (/sensor|encoder|as5600|gps|gnss|imu|compass|magnet|iman/i.test(text)) return ['Sensor / referencia', '<rect x="45" y="45" width="150" height="150" rx="12"/><circle cx="120" cy="120" r="50"/><path d="m120 70-22 70 22-12 22 12Z"/>'];
  if (/connector|conector|header|socket|terminal|jst|phoenix|samtec/i.test(text)) return ['Conexion', '<rect x="35" y="60" width="170" height="110" rx="8"/><path d="M65 170v40m55-40v40m55-40v40"/><circle cx="65" cy="110" r="12"/><circle cx="120" cy="110" r="12"/><circle cx="175" cy="110" r="12"/>'];
  if (/audio|speaker|mic|altavoz|k1/i.test(text)) return ['Audio', '<path d="M40 95h45l65-45v140l-65-45H40Z"/><path d="M175 85q35 35 0 70m20-95q60 60 0 120"/>'];
  return ['Pieza / modulo: simbolo funcional', '<rect x="40" y="50" width="160" height="140" rx="10"/><path d="M70 85h100m-100 35h100m-100 35h60"/><circle cx="55" cy="65" r="4"/><circle cx="185" cy="175" r="4"/>'];
}

function entries() {
  return sources.flatMap((source) => parseCsv(fs.readFileSync(path.join(root, source.file), 'utf8')).map((row, index) => {
    for (const key of [source.name, source.quantity, source.detail, source.note, source.id].filter(Boolean)) {
      if (!(key in row)) throw new Error(`${source.file}: missing column ${key}`);
    }
    const id = source.id ? row[source.id] : `LITE-${String(index + 1).padStart(3, '0')}`;
    return {
      key: `${source.key}-${String(index + 1).padStart(3, '0')}`,
      source: source.file, row: index + 2, id, name: row[source.name],
      quantity: row[source.quantity], detail: row[source.detail], note: row[source.note]
    };
  }));
}

function figure(entry) {
  const [kind, drawing] = symbol(`${entry.name} ${entry.detail}`);
  const lines = [
    ...wrap(entry.name, 57),
    '',
    ...wrap(`Referencia: ${entry.id}`, 57),
    ...wrap(`Cantidad de la fila: ${entry.quantity}`, 57),
    ...wrap(entry.detail || 'Especificacion no definida en la BOM', 57),
    '',
    ...wrap(entry.note || 'Sin nota adicional en la BOM', 57)
  ];
  const height = Math.max(570, 160 + lines.length * 23 + 130);
  return `<svg xmlns="http://www.w3.org/2000/svg" lang="es" role="img" aria-labelledby="title desc" viewBox="0 0 1000 ${height}" font-family="Arial, sans-serif">
<title id="title">${xml(entry.id)} - ${xml(entry.name)} - BricoHams</title>
<desc id="desc">Ficha conceptual, no plano ni fotografia. ${xml(kind)}. Fuente ${xml(entry.source)}, fila ${entry.row}. No validado fisicamente.</desc>
<rect width="1000" height="${height}" fill="#fff"/>
<rect x="8" y="8" width="984" height="${height - 16}" fill="none" stroke="#12263f" stroke-width="2"/>
<rect x="10" y="10" width="980" height="94" fill="#f4f7fa"/>
<image href="../../../branding/bricohams_horizontal.png" x="24" y="24" width="218" height="56"/>
<text x="270" y="50" font-size="25" fill="#12263f" font-weight="bold">BricoHams | Componentes</text>
<text x="270" y="79" font-size="17" fill="#5b6b7b">${xml(entry.key)}</text>
<path d="M10 105H990" stroke="#e8871e" stroke-width="5"/>
<g transform="translate(35 160)" fill="none" stroke="#12263f" stroke-width="5" stroke-linejoin="round">${drawing}</g>
<text x="35" y="435" font-size="15" fill="#5b6b7b">PICTOGRAMA NO A ESCALA</text>
${lines.map((line, i) => `<text x="310" y="${150 + i * 23}" font-size="17" fill="#12263f">${xml(line)}</text>`).join('\n')}
<rect x="20" y="${height - 112}" width="960" height="36" fill="#fff0db"/>
<text x="32" y="${height - 88}" font-size="16" fill="#12263f">PROTOTIPO / NO FABRICAR NI CABLEAR DESDE ESTA FICHA</text>
<text x="24" y="${height - 53}" font-size="14" fill="#12263f">Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina | bricohams.org</text>
<text x="24" y="${height - 29}" font-size="13" fill="#5b6b7b">Fuente: ${xml(entry.source)} | fila ${entry.row} | Ver NOTICE y LICENSES</text>
</svg>
`;
}

function artifacts() {
  const all = entries();
  const files = new Map();
  for (const entry of all) files.set(`${output}/${entry.key}.svg`, figure(entry));
  const index = [
    '# BricoHams: catalogo visual de componentes',
    '',
    'Generado desde las BOM mediante `node scripts/component-catalog.cjs`.',
    `Cobertura: **${all.length} filas de componentes en ${sources.length} listas**. Cada fila tiene una ficha SVG propia; una fila puede agrupar varias unidades o designadores.`,
    '',
    '**Son pictogramas funcionales de identificacion, no fotografias, renders CAD, huellas PCB, planos a escala ni instrucciones de cableado.** Para la geometria disponible, consulte los [despieces CAD y vistas de PCB](../README.md). No se inventan formas de componentes todavia sin seleccionar.',
    '',
    'Las especificaciones y notas se reproducen de cada BOM, incluso si son historicas o provisionales. Los IDs solo son unicos dentro de su lista; los IDs LITE son numeros de fila de este catalogo, no referencias de fabricante. No sumar alternativas, LEGACY, herramientas ni piezas compartidas. Los precios se consultan por separado en [REFERENCE-PRICES](../../REFERENCE-PRICES.md).',
    '',
    'La BOM no equivale a una autorizacion de compra, fabricacion o energizacion. Prevalecen [VALIDATION](../../VALIDATION.md), las fichas de fabricante y la revision liberada. Las filas con cantidad cero se muestran para identificar referencias excluidas, no para comprarlas.',
    '',
    '[Montaje por modulos](../README.md) · [Instalacion de software y conjunto](../06-instalacion.md) · [Cobertura y limites de la revision](../../PROJECT-REVIEW.md)',
    ''
  ];
  for (const source of sources) {
    index.push(`## ${source.title}`, '', `[BOM fuente](../../../${source.file})`, '', '| ID / designadores | Componente | Cantidad | Imagen |', '| --- | --- | --- | --- |');
    for (const entry of all.filter((item) => item.source === source.file)) {
      index.push(`| ${md(entry.id)} | ${md(entry.name)} | ${md(entry.quantity)} | [Ficha visual](${entry.key}.svg) |`);
    }
    index.push('');
  }
  files.set(`${output}/README.md`, `${index.join('\n').trimEnd()}\n`);
  return files;
}

function main(check) {
  const files = artifacts();
  const missing = [];
  for (const [file, content] of files) {
    const target = path.join(root, file);
    if (check) {
      if (!fs.existsSync(target) || fs.readFileSync(target, 'utf8') !== content) missing.push(file);
    } else {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, content);
    }
  }
  if (missing.length) throw new Error(`Stale component catalog; run node scripts/component-catalog.cjs:\n${missing.join('\n')}`);
  console.log(`${files.size - 1} component figures ${check ? 'verified' : 'generated'} from ${sources.length} BOMs.`);
}

if (require.main === module) {
  if (process.argv.slice(2).some((arg) => arg !== '--check')) throw new Error('Usage: node scripts/component-catalog.cjs [--check]');
  main(process.argv.includes('--check'));
}
module.exports = { parseCsv, entries, artifacts, sources };
