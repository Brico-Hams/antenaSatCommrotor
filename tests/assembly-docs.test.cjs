const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const test = require('node:test');
const { parseCsv, entries, artifacts, sources } = require('../scripts/component-catalog.cjs');

const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
// Checkout may convert line endings (core.autocrlf); compare content only.
const lf = (text) => text.replace(/\r\n/g, '\n');

test('component CSV parser preserves commas, escaped quotes, CRLF and multiline fields', () => {
  assert.deepEqual(parseCsv('id,note\r\nA,"one, two"\r\nB,"say ""hello""\nnext"\r\n'), [
    { id: 'A', note: 'one, two' }, { id: 'B', note: 'say "hello"\nnext' }
  ]);
  assert.deepEqual(parseCsv('id,note\nA,'), [{ id: 'A', note: '' }]);
  for (const input of ['id,note\nA,B,C', 'id,note\nA,"open', 'id,note\nA,"closed"x', 'id,id\nA,B']) {
    assert.throws(() => parseCsv(input), /CSV/);
  }
});

test('all component BOMs have exact columns and uniquely identified catalog rows', () => {
  assert.equal(sources.length, 12);
  const all = entries();
  assert.equal(new Set(all.map((entry) => entry.key)).size, all.length);
  for (const source of sources) {
    const rows = parseCsv(read(source.file));
    assert.ok(rows.length > 0, source.file);
    assert.equal(all.filter((entry) => entry.source === source.file).length, rows.length);
  }
  const sdr = all.find((entry) => entry.id === 'MMA-017');
  assert.equal(sdr.quantity, '2');
  assert.match(sdr.detail, /TX-capable, with hardware safety/);
  const sensor = all.find((entry) => entry.id === 'SEN-10');
  assert.equal(sensor.detail, 'AZ/EL/POL encoders, remote compass/IMU, GPS receiver/antenna');
  assert.match(sensor.note, /^Include the full operational harness/);
});

test('every component image and catalog index exactly match their current BOM sources', () => {
  const expected = artifacts();
  for (const [file, content] of expected) assert.equal(lf(read(file)), lf(content), `Regenerate ${file}`);
  const images = fs.readdirSync(path.join(root, 'docs/assembly/components')).filter((name) => name.endsWith('.svg'));
  assert.equal(images.length, entries().length, 'stale or missing images');
});

test('component illustrations carry source identity, branding, accessibility and honest status', () => {
  for (const [file, svg] of artifacts()) {
    if (!file.endsWith('.svg')) continue;
    assert.match(svg, /role="img" aria-labelledby="title desc"/, file);
    assert.match(svg, /bricohams\.org/, file);
    assert.match(svg, /Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina/, file);
    assert.match(svg, /PICTOGRAMA NO A ESCALA/, file);
    assert.match(svg, /NO FABRICAR NI CABLEAR/, file);
    assert.match(svg, /Fuente: .* \| fila \d+/, file);
    for (const match of svg.matchAll(/<image href="([^"]+)"/g)) {
      assert.ok(fs.existsSync(path.resolve(root, path.dirname(file), match[1])), file);
    }
  }
});

function markdownFiles(directory) {
  return fs.readdirSync(path.join(root, directory), { withFileTypes: true }).flatMap((item) => {
    const file = path.join(directory, item.name);
    return item.isDirectory() ? markdownFiles(file) : item.name.endsWith('.md') ? [file] : [];
  });
}

test('assembly guides and catalog resolve all local links in every existing language', () => {
  for (const directory of ['docs/assembly', 'docs/en/assembly', 'docs/hu/assembly']) {
    for (const file of markdownFiles(directory)) {
      for (const match of read(file).matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
        const target = match[1].replace(/^<|>$/g, '').split('#')[0];
        if (!target || /^[a-z][a-z\d+.-]*:/i.test(target)) continue;
        assert.ok(fs.existsSync(path.resolve(root, path.dirname(file), decodeURIComponent(target))), `${file}: ${target}`);
      }
    }
  }
});

test('installation keeps variants, PCB holds and published OS password policy explicit', () => {
  const guide = read('docs/assembly/06-instalacion.md');
  for (const term of ['rotor-only', 'radio-only', 'integrated', 'ESP32', 'PortableSatLite', 'passwd', 'SHA-256']) {
    assert.ok(guide.includes(term), term);
  }
  assert.match(guide, /contrasena publica/);
  assert.match(guide, /no habilita automaticamente el servicio/);
  assert.match(read('docs/assembly/04-electronica.md'), /NO FABRICAR \/ NO ENERGIZAR/);
  assert.match(read('docs/assembly/01-rotor.md'), /no son recorridos fisicamente aprobados/);
});
