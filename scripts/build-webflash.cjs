'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const root = path.resolve(__dirname, '..');
const sha256 = data => crypto.createHash('sha256').update(data).digest('hex');
const readJSON = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const upstreamHashes = {
  'ARDUINO-ESP32-LGPL-2.1.md': '994ce1902a23c74519b5d118c6bbb657edabce91dd6b7cc825d86bb8f5c9780f',
  'ESP-IDF-APACHE-2.0.txt': 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30',
  'arduino-esp32-2.0.17.tar.gz': 'fb4024408494d6c45701dc8e1c595f84af543e66e06b00a21435a632d577fa61',
  'esp-idf-v4.4.7.tar.gz': 'ffa2081fa5d38426a861d060cdfac95477d54df29d42457d57030a44472f367f'
};

function validateNpmIsolation() {
  const manifest = readJSON(path.join(root, 'webflash', 'package.json'));
  const lock = readJSON(path.join(root, 'webflash', 'package-lock.json'));
  if (Object.keys(manifest.dependencies).join() !== 'esp-web-tools' ||
      manifest.dependencies['esp-web-tools'] !== '10.1.0')
    throw Error('Webflash may install only pinned registry ESP Web Tools');
  for (const [name, item] of Object.entries(lock.packages)) {
    if (name === '') continue;
    if (!name.startsWith('node_modules/') || item.link ||
        !item.resolved?.startsWith('https://registry.npmjs.org/'))
      throw Error(`Non-registry/local dependency prohibited: ${name}`);
  }
}

function sourceTree() {
  const files = [];
  function walk(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const full = path.join(directory, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile()) files.push(full);
    }
  }
  for (const directory of ['firmware/src', 'firmware/include', 'web'])
    walk(path.join(root, directory));
  files.push(path.join(root, 'firmware', 'platformio.ini'));
  const entries = files.map(file => ({
    path: path.relative(root, file).split(path.sep).join('/'),
    sha256: sha256(fs.readFileSync(file))
  })).sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
  return { sha256: sha256(entries.map(file => `${file.sha256}  ${file.path}\n`).join('')), files: entries };
}

function validateBrowserBundle(dir) {
  const web = path.join(dir, 'vendor', 'esp-web-tools', 'web');
  if (!fs.existsSync(path.join(web, 'install-button.js'))) throw Error('Browser-ready ESP Web Tools entry missing');
  for (const filename of fs.readdirSync(web).filter(n => n.endsWith('.js'))) {
    const js = fs.readFileSync(path.join(web, filename), 'utf8');
    const patterns = [
      /\bimport\s*\(\s*["']([^"']+)["']/g,
      /\b(?:import|export)\s+(?:[^"']*?\bfrom\s*)?["']([^"']+)["']/g
    ];
    for (const pattern of patterns) for (const match of js.matchAll(pattern)) {
      if (!/^\.\/[a-zA-Z0-9_.-]+\.js$/.test(match[1]) ||
          !fs.existsSync(path.join(web, match[1])))
        throw Error(`Missing/nonlocal browser import: ${match[1]}`);
    }
  }
}

function validateBundle(dir) {
  const manifest = readJSON(path.join(dir, 'manifest.json'));
  const metadata = readJSON(path.join(dir, 'build-info.json'));
  if (manifest.builds.length !== 1 || manifest.builds[0].chipFamily !== 'ESP32')
    throw Error('Only classic ESP32 is supported');
  // In ESP Web Tools 10.1.0 FALSE erases non-Improv devices by default.
  // TRUE presents an unchecked erase checkbox before installation.
  if (manifest.new_install_prompt_erase !== true) throw Error('Automatic erase prohibited: explicit prompt required');
  const parts = manifest.builds[0].parts;
  if (parts.length < 4 || parts.length > 5) throw Error('Expected four firmware images and optional filesystem');
  const expected = [4096, 32768, 57344, 65536];
  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (!Number.isInteger(part.offset) || part.offset < 0 ||
        (i < 4 && part.offset !== expected[i])) throw Error('Unexpected upload offset');
    if (!/^firmware\/[a-z0-9_.-]+\.bin$/.test(part.path)) throw Error('Unsafe asset path');
    const data = fs.readFileSync(path.join(dir, part.path));
    if (!data.length || ((i === 0 || i === 3) &&
        (data.length < 24 || data[0] !== 0xe9 || data.readUInt16LE(12) !== 0)))
      throw Error('Missing or invalid ESP32 image');
    if (i === 2 && (data.length !== 8192 || data.readUInt32LE(0) !== 1))
      throw Error('Invalid boot_app0 OTA data image');
    const asset = metadata.assets.find(a => a.path === part.path);
    if (!asset || asset.offset !== part.offset || asset.bytes !== data.length ||
        asset.sha256 !== sha256(data)) throw Error('Asset integrity mismatch');
  }
  // NVS occupies 0x9000..0xdfff in the captured default partition table.
  for (const part of parts) {
    const bytes = fs.statSync(path.join(dir, part.path)).size;
    if (part.offset < 0xe000 && part.offset + Math.ceil(bytes / 4096) * 4096 > 0x9000)
      throw Error('Image would erase NVS');
  }
  for (let i = 0; i < parts.length - 1; i++) {
    const bytes = fs.statSync(path.join(dir, parts[i].path)).size;
    if (parts[i].offset + Math.ceil(bytes / 4096) * 4096 > parts[i + 1].offset)
      throw Error('Flash images overlap');
  }
  const partitions = fs.readFileSync(path.join(dir, parts[1].path));
  let nvs = false;
  const ranges = [];
  for (let i = 0; i + 32 <= partitions.length && partitions.readUInt16LE(i) === 0x50aa; i += 32) {
    const label = partitions.subarray(i + 12, i + 28).toString().replace(/\0.*$/, '');
    const offset = partitions.readUInt32LE(i + 4), size = partitions.readUInt32LE(i + 8);
    ranges.push({ label, offset, size });
    if (label === 'nvs') nvs = offset === 0x9000 && size === 0x5000;
  }
  if (!nvs) throw Error('Unexpected NVS partition layout');
  const app = ranges.find(p => p.label === 'app0');
  if (!app || app.offset !== parts[3].offset ||
      metadata.assets.find(a => a.path === parts[3].path).bytes > app.size)
    throw Error('Application exceeds partition');
  if (parts.length === 5) {
    const partition = ranges.find(p => ['spiffs', 'littlefs'].includes(p.label));
    if (!partition || partition.offset !== parts[4].offset ||
        partition.size !== metadata.assets.find(a => a.path === parts[4].path).bytes)
      throw Error('Filesystem does not match actual partition table');
  }
  return metadata;
}

function assertPublicConfiguration() {
  for (const name of [path.join('include', 'secrets.h'), 'secrets.ini']) {
    if (fs.existsSync(path.resolve(root, 'firmware', name)))
      throw Error('Private provisioning files must not be present in public build');
  }
  const config = fs.readFileSync(path.join(root, 'firmware', 'include', 'board_config.h'), 'utf8');
  for (const field of ['apPassword', 'apiToken', 'staSsid', 'staPassword']) {
    if (!new RegExp(`\\b${field}\\s*=\\s*""\\s*;`).test(config))
      throw Error(`Public build requires empty ${field}; provision privately`);
  }
  if (!/carrierVerified\s*=\s*false/.test(config)) throw Error('Public prototype must remain hardware-locked');
}

function buildBundle({ buildDir, outDir, version, sourceSha }) {
  validateNpmIsolation();
  assertPublicConfiguration();
  if (sourceSha !== null && !/^[0-9a-f]{40}$/.test(sourceSha)) throw Error('A full source commit SHA is required');
  if (process.env.GITHUB_ACTIONS === 'true' && sourceSha === null) throw Error('CI requires a real source commit');
  if (!/^[A-Za-z0-9_.+-]{1,100}$/.test(version)) throw Error('Unsafe version label');
  const proof = readJSON(path.join(buildDir, 'webflash-upload.json'));
  const tree = sourceTree();
  if (!proof.sourceTree || proof.sourceTree.sha256 !== tree.sha256)
    throw Error('Firmware/UI/header/config sources changed since upload proof; rebuild before packaging');
  if (proof.board !== 'esp32dev' || proof.mcu !== 'esp32' || proof.platform !== 'espressif32@6.10.0' ||
      !proof.command.includes('write_flash') || !proof.command.includes('--chip esp32') ||
      proof.command.includes('erase_flash')) throw Error('Not the verified classic ESP32 upload recipe');
  for (const [name, version] of Object.entries({
    'framework-arduinoespressif32': '3.20017.241212',
    'toolchain-xtensa-esp32': '8.4.0+2021r2-patch5',
    'tool-esptoolpy': '1.40501.0', 'tool-mklittlefs': '1.203.210628'
  })) {
    const installed = proof.packages.find(item => item.name === name)?.version;
    if (!installed || !(installed === version || installed.startsWith(`${version}+sha.`)))
      throw Error(`Unexpected build dependency: ${name}`);
  }
  fs.mkdirSync(path.join(outDir, 'firmware'), { recursive: true });
  const images = proof.images.sort((a, b) => a.offset - b.offset);
  if (images.length !== 4) throw Error('Unexpected base upload images');
  const assets = images.map(image => {
    const source = path.resolve(image.source);
    const hexadecimal = `0x${image.offset.toString(16)}`;
    if (!proof.command.includes(path.basename(source)) ||
        !new RegExp(`(?:^|\\s)(?:${hexadecimal}|${image.offset})(?:\\s|$)`, 'i').test(proof.command))
      throw Error('Image/offset absent from actual upload command');
    const data = fs.readFileSync(source);
    const destination = `firmware/${path.basename(source)}`;
    fs.writeFileSync(path.join(outDir, destination), data);
    return { path: destination, offset: image.offset, bytes: data.length, sha256: sha256(data) };
  });
  // Existing controller serves its web UI from LittleFS; never omit a required uploadfs image.
  const main = fs.readFileSync(path.join(root, 'firmware', 'src', 'main.cpp'), 'utf8');
  if (/LittleFS\.open\("\/index\.html"/.test(main)) {
    const partitions = fs.readFileSync(path.join(buildDir, 'partitions.bin'));
    let partition;
    for (let i = 0; i + 32 <= partitions.length && partitions.readUInt16LE(i) === 0x50aa; i += 32) {
      const label = partitions.subarray(i + 12, i + 28).toString().replace(/\0.*$/, '');
      if (['spiffs', 'littlefs'].includes(label))
        partition = { offset: partitions.readUInt32LE(i + 4), bytes: partitions.readUInt32LE(i + 8) };
    }
    if (!partition) throw Error('Required filesystem partition missing');
    const data = fs.readFileSync(path.join(buildDir, 'littlefs.bin'));
    fs.writeFileSync(path.join(outDir, 'firmware', 'littlefs.bin'), data);
    assets.push({ path: 'firmware/littlefs.bin', ...partition, sha256: sha256(data) });
  }
  const manifest = {
    name: 'PortableSatStation — PROTOTYPE ONLY',
    version: `${version}+${sourceSha ? sourceSha.slice(0, 12) : 'uncommitted'}`,
    new_install_prompt_erase: true,
    builds: [{ chipFamily: 'ESP32', parts: assets.map(({ path, offset }) => ({ path, offset })) }]
  };
  const metadata = {
    version, sourceSha, sourceState: sourceSha ? 'commit' : 'local-uncommitted',
    sourceTree: tree,
    generatedAt: new Date().toISOString(), assets,
    uploadCommand: proof.command,
    platformioCore: '6.1.18',
    platformioConfig: fs.readFileSync(path.join(root, 'firmware', 'platformio.ini'), 'utf8'),
    packages: proof.packages,
    espWebTools: { version: '10.1.0', license: 'Apache-2.0',
      lockSha256: sha256(fs.readFileSync(path.join(root, 'webflash', 'package-lock.json'))) },
    provisioning: 'No embedded WiFi password/API token. Fresh NVS: USB JSON setup required, AP off, carrier unverified. Existing NVS retained; boots DISARMED.'
  };
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
  fs.writeFileSync(path.join(outDir, 'build-info.json'), JSON.stringify(metadata, null, 2));
  fs.writeFileSync(path.join(outDir, 'SHA256SUMS'), assets.map(a => `${a.sha256}  ${a.path}`).join('\n') + '\n');
  for (const file of ['index.html', 'flash.js', 'style.css'])
    fs.copyFileSync(path.join(root, 'webflash', file), path.join(outDir, file));
  for (const file of ['AUTHORS.md', 'ACKNOWLEDGEMENTS.md', 'DISCLAIMER.md'])
    fs.copyFileSync(path.join(root, file), path.join(outDir, file));
  fs.mkdirSync(path.join(outDir, 'docs'), { recursive: true });
  for (const file of ['WEBFLASH.md', 'CONTROL.md', 'SOURCES.md'])
    fs.copyFileSync(path.join(root, 'docs', file), path.join(outDir, 'docs', file));
  const vendor = path.join(root, 'webflash', 'node_modules', 'esp-web-tools');
  if (readJSON(path.join(vendor, 'package.json')).version !== '10.1.0') throw Error('ESP Web Tools version mismatch');
  const installerSource = fs.readFileSync(path.join(vendor, 'dist', 'install-dialog.js'), 'utf8');
  if (!installerSource.includes('else if (this._manifest.new_install_prompt_erase)') ||
      !installerSource.includes('this._startInstall(checkbox.checked)') ||
      !installerSource.includes('<ew-checkbox touch-target="wrapper" class="danger"></ew-checkbox>'))
    throw Error('Pinned installer erase confirmation behavior changed; review before publishing');
  fs.cpSync(path.join(vendor, 'dist'), path.join(outDir, 'vendor', 'esp-web-tools'), { recursive: true });
  validateBrowserBundle(outDir);
  fs.mkdirSync(path.join(outDir, 'licenses'), { recursive: true });
  fs.copyFileSync(path.join(vendor, 'LICENSE'), path.join(outDir, 'licenses', 'ESP-WEB-TOOLS-APACHE-2.0.txt'));
  fs.copyFileSync(path.join(root, 'LICENSES', 'MIT.txt'), path.join(outDir, 'licenses', 'ORIGINAL-MIT.txt'));
  fs.copyFileSync(path.join(root, 'webflash', 'THIRD-PARTY-NOTICES.txt'), path.join(outDir, 'THIRD-PARTY-NOTICES.txt'));
  fs.copyFileSync(path.join(root, 'webflash', 'package-lock.json'), path.join(outDir, 'dependencies-lock.json'));
  fs.copyFileSync(path.join(root, 'NOTICE.md'), path.join(outDir, 'licenses', 'PROJECT-NOTICE.md'));
  // Preserve installed dependency license texts rather than relabel the linked binary as MIT.
  const dependencyRoot = path.resolve(proof.libdeps);
  for (const dep of ['Sgp4', 'ArduinoJson', 'NimBLE-Arduino']) {
    const dir = path.join(dependencyRoot, dep);
    const license = fs.readdirSync(dir).find(n => /^(license|copying)(\.|$)/i.test(n));
    if (!license) throw Error(`Missing license for ${dep}`);
    fs.copyFileSync(path.join(dir, license), path.join(outDir, 'licenses', `${dep}-${license}`));
  }
  // TinyGPSPlus registry archive omits LICENSE; its source header states LGPL 2.1+.
  const tinyHeader = path.join(dependencyRoot, 'TinyGPSPlus', 'src', 'TinyGPS++.h');
  const tinyLicense = fs.readFileSync(tinyHeader, 'utf8').match(/^\/\*[\s\S]*?\*\//)?.[0];
  if (!tinyLicense || !tinyLicense.includes('Lesser General Public')) throw Error('Missing TinyGPSPlus copyright/license');
  fs.writeFileSync(path.join(outDir, 'licenses', 'TinyGPSPlus-copyright.txt'), tinyLicense);
  const frameworkDir = path.resolve(proof.framework);
  const upstream = path.join(root, 'build', 'webflash-upstream');
  metadata.upstream = [];
  for (const [file, expectedHash] of Object.entries(upstreamHashes)) {
    const source = path.join(upstream, file);
    if (!fs.existsSync(source)) throw Error('Run upstream license/source preservation step before packaging');
    if (sha256(fs.readFileSync(source)) !== expectedHash) throw Error(`Pinned upstream source integrity failed: ${file}`);
    fs.copyFileSync(source, path.join(outDir, file.endsWith('.gz') ? '' : 'licenses', file));
    metadata.upstream.push({ file, sha256: expectedHash, bytes: fs.statSync(source).size });
  }
  cp.execFileSync('tar', ['-czf', path.join(outDir, 'arduino-framework-source.tar.gz'),
    '-C', frameworkDir, '.'], { cwd: root });
  const nodeModules = path.join(root, 'webflash', 'node_modules');
  function preserveLicenseTexts(directory, destinationRoot, relative = '') {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (entry.name === '.bin') continue;
      const full = path.join(directory, entry.name);
      const next = path.join(relative, entry.name);
      if (fs.lstatSync(full).isSymbolicLink())
        throw Error(`Refusing to traverse dependency symlink/junction: ${next}`);
      if (entry.isDirectory()) preserveLicenseTexts(full, destinationRoot, next);
      else if (/^(license|copying|notice)(\.|$)/i.test(entry.name)) {
        const destination = path.join(destinationRoot, next);
        fs.mkdirSync(path.dirname(destination), { recursive: true });
        fs.copyFileSync(full, destination);
      }
    }
  }
  preserveLicenseTexts(nodeModules, path.join(outDir, 'licenses', 'npm'));
  preserveLicenseTexts(dependencyRoot, path.join(outDir, 'licenses', 'firmware-libraries'));
  fs.cpSync(path.join(path.resolve(proof.toolchain), 'share', 'licenses'),
    path.join(outDir, 'licenses', 'toolchain-runtime'), { recursive: true });
  fs.copyFileSync(path.join(buildDir, 'firmware.elf'), path.join(outDir, 'firmware.elf'));
  // Source + relocatable objects allow upstream-license review and private relinking.
  cp.execFileSync('tar', ['-czf', path.join(outDir, 'firmware-link-objects.tar.gz'),
    '-C', buildDir, '.'], { cwd: root });
  cp.execFileSync('tar', ['-czf', path.join(outDir, 'controller-source.tar.gz'),
    '--exclude=.pio', '--exclude=.tools', '--exclude=secrets.h', '--exclude=secrets.ini',
    '-C', root, 'firmware', 'web', 'scripts', 'LICENSES', 'NOTICE.md'], { cwd: root });
  cp.execFileSync('tar', ['-czf', path.join(outDir, 'firmware-library-source.tar.gz'),
    '-C', dependencyRoot, 'Sgp4', 'ArduinoJson', 'TinyGPSPlus', 'NimBLE-Arduino'], { cwd: root });
  metadata.sourceArchives = fs.readdirSync(outDir).filter(file => file.endsWith('.tar.gz')).map(file => ({
    file, sha256: sha256(fs.readFileSync(path.join(outDir, file))), bytes: fs.statSync(path.join(outDir, file)).size
  }));
  fs.writeFileSync(path.join(outDir, 'build-info.json'), JSON.stringify(metadata, null, 2));
  fs.appendFileSync(path.join(outDir, 'SHA256SUMS'),
    metadata.sourceArchives.map(asset => `${asset.sha256}  ${asset.file}`).join('\n') + '\n' +
    `${metadata.espWebTools.lockSha256}  dependencies-lock.json\n`);
  validateBundle(outDir);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === '--validate') {
    validateBundle(path.resolve(args[1]));
    validateBrowserBundle(path.resolve(args[1]));
    console.log('Webflash manifest, binary headers, partition boundaries and SHA256 verified.');
  } else {
    let sourceSha = process.env.GITHUB_SHA || null;
    if (!sourceSha) {
      try {
        sourceSha = cp.execFileSync('git', ['rev-parse', 'HEAD'], {
          cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore']
        }).trim();
        if (cp.execFileSync('git', ['status', '--porcelain'], { cwd: root, encoding: 'utf8' }).trim())
          sourceSha = null;
      } catch { /* An initialized repository need not have its first commit yet. */ }
    }
    buildBundle({
      buildDir: path.resolve(args[0] || path.join(root, 'firmware', '.pio', 'build', 'esp32')),
      outDir: path.resolve(args[1] || path.join(root, 'build', 'webflash')),
      version: process.env.WEBFLASH_VERSION || (sourceSha ? `prototype-${sourceSha.slice(0, 12)}` : 'local-prototype'), sourceSha
    });
    console.log('Generated and validated webflash bundle from real PlatformIO build outputs.');
  }
}
module.exports = { validateBundle, validateBrowserBundle, validateNpmIsolation, sourceTree, buildBundle, assertPublicConfiguration };
