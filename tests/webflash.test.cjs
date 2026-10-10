'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { validateBundle, validateBrowserBundle, validateNpmIsolation, assertPublicConfiguration } = require('../scripts/build-webflash.cjs');
const root = path.resolve(__dirname, '..');

function fixture(t) {
  const base = path.join(root, 'build');
  fs.mkdirSync(base, { recursive: true });
  const dir = fs.mkdtempSync(path.join(base, 'webflash-test-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  fs.mkdirSync(path.join(dir, 'firmware'));
  const offsets = [4096, 32768, 57344, 65536];
  const names = ['bootloader', 'partitions', 'boot_app0', 'firmware'];
  const assets = names.map((name, i) => {
    // Synthetic staged test data ONLY; never copied to a distributable CI artifact.
    const data = Buffer.alloc(i === 1 ? 3072 : i === 2 ? 8192 : 256, 0xff);
    data[0] = 0xe9;
    if (i === 0 || i === 3) data.writeUInt16LE(0, 12);
    if (i === 2) data.writeUInt32LE(1, 0);
    if (i === 1) {
      for (const [n, label, offset, size] of [[0, 'nvs', 0x9000, 0x5000],
        [1, 'app0', 0x10000, 0x140000], [2, 'spiffs', 0x290000, 0x160000]]) {
        const start = n * 32;
        data.writeUInt16LE(0x50aa, start);
        data.writeUInt32LE(offset, start + 4);
        data.writeUInt32LE(size, start + 8);
        data.fill(0, start + 12, start + 28);
        data.write(label, start + 12);
      }
    }
    const asset = { path: `firmware/${name}.bin`, offset: offsets[i], bytes: data.length,
      sha256: crypto.createHash('sha256').update(data).digest('hex') };
    fs.writeFileSync(path.join(dir, asset.path), data);
    return asset;
  });
  const manifest = { new_install_prompt_erase: true,
    builds: [{ chipFamily: 'ESP32', parts: assets.map(({ path, offset }) => ({ path, offset })) }] };
  const metadata = { assets };
  const save = () => {
    fs.writeFileSync(path.join(dir, 'manifest.json'), JSON.stringify(manifest));
    fs.writeFileSync(path.join(dir, 'build-info.json'), JSON.stringify(metadata));
  };
  save();
  return { dir, manifest, metadata, save };
}

test('valid staged manifest preserves default NVS and uses actual ESP32 offsets', t => {
  const f = fixture(t);
  assert.equal(validateBundle(f.dir).assets.length, 4);
});
test('wrong chip and guessed offset rejected', t => {
  const f = fixture(t);
  f.manifest.builds[0].chipFamily = 'ESP32-C3'; f.save();
  assert.throws(() => validateBundle(f.dir), /classic ESP32/);
  f.manifest.builds[0].chipFamily = 'ESP32';
  f.manifest.builds[0].parts[0].offset = 0; f.save();
  assert.throws(() => validateBundle(f.dir), /offset/);
});
test('erase, traversal and corrupted binaries rejected', t => {
  const f = fixture(t);
  f.manifest.new_install_prompt_erase = false; f.save();
  assert.throws(() => validateBundle(f.dir), /erase/);
  f.manifest.new_install_prompt_erase = true;
  f.manifest.builds[0].parts[0].path = '../private.bin'; f.save();
  assert.throws(() => validateBundle(f.dir), /Unsafe/);
  f.manifest.builds[0].parts[0].path = 'firmware/bootloader.bin'; f.save();
  fs.appendFileSync(path.join(f.dir, 'firmware', 'bootloader.bin'), 'damage');
  assert.throws(() => validateBundle(f.dir), /integrity/);
});
test('missing assets fail rather than pretending CI compiled', t => {
  const f = fixture(t);
  fs.unlinkSync(path.join(f.dir, 'firmware', 'firmware.bin'));
  assert.throws(() => validateBundle(f.dir), /ENOENT/);
});
test('oversize bootloader cannot reach NVS', t => {
  const f = fixture(t);
  const header = fs.readFileSync(path.join(f.dir, 'firmware', 'bootloader.bin')).subarray(0, 24);
  const data = Buffer.alloc(0x9000, 0xff);
  header.copy(data);
  fs.writeFileSync(path.join(f.dir, 'firmware', 'bootloader.bin'), data);
  f.metadata.assets[0].bytes = data.length;
  f.metadata.assets[0].sha256 = crypto.createHash('sha256').update(data).digest('hex');
  f.save();
  assert.throws(() => validateBundle(f.dir), /Image would erase NVS/);
});
test('public credentials and motor hardware lock remain fail closed', () => {
  assert.doesNotThrow(assertPublicConfiguration);
});
test('Pages deploy has narrow permissions and no privileged PR trigger', () => {
  const workflow = fs.readFileSync(path.join(root, '.github', 'workflows', 'webflash.yml'), 'utf8');
  assert.match(workflow, /github\.ref == 'refs\/heads\/main'/);
  assert.match(workflow, /name: webflash-pages/);
  assert.doesNotMatch(workflow, /pull_request_target|secrets\./);
  assert.match(workflow, /platformio==6\.1\.18/);
  assert.match(workflow, /npm ci --ignore-scripts/);
});
test('install UI is acknowledgement-gated and pinned locally', () => {
  assert.doesNotThrow(validateNpmIsolation);
  const html = fs.readFileSync(path.join(root, 'webflash', 'index.html'), 'utf8');
  const js = fs.readFileSync(path.join(root, 'webflash', 'flash.js'), 'utf8');
  assert.match(html, /id="installer" hidden/);
  assert.match(html, /id="acknowledge"/);
  assert.match(html, /motores\/actuadores desconectados/);
  assert.match(js, /vendor\/esp-web-tools\/web\/install-button\.js/);
  assert.doesNotMatch(js, /unpkg|jsdelivr|requestPort/);
  assert.equal(require('../webflash/package.json').dependencies['esp-web-tools'], '10.1.0');
});
if (process.env.WEBFLASH_VALIDATE_COMPILED === 'true') {
  test('CI validates its actual compiled bundle, not only synthetic fixtures', () => {
    assert.doesNotThrow(() => validateBundle(path.join(root, 'build', 'webflash')));
    assert.doesNotThrow(() => validateBrowserBundle(path.join(root, 'build', 'webflash')));
  });
}
