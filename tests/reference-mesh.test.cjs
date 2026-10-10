const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { inspectMesh } = require('../scripts/inspect-reference-mesh.cjs');

test('OBJ metadata preserves unit uncertainty and does not change input', () => {
  const folder = fs.mkdtempSync(path.join(os.tmpdir(), 'sat-mesh-test-'));
  const filename = path.join(folder, 'fixture.obj');
  const source = 'o triangle\nv 0 0 0\nv 3 0 0\nv 0 4 2\nf 1 2 3\n';
  try {
    fs.writeFileSync(filename, source);
    const info = inspectMesh(filename);
    assert.deepEqual(info.boundingBox.spans, [3, 4, 2]);
    assert.equal(info.faceCount, 1);
    assert.equal(info.objectCount, 1);
    assert.equal(info.units, 'unspecified-by-format');
    assert.equal(fs.readFileSync(filename, 'utf8'), source);
  } finally {
    fs.unlinkSync(filename);
    fs.rmdirSync(folder);
  }
});

test('binary STL reads actual float coordinates, not text heuristics', () => {
  const folder = fs.mkdtempSync(path.join(os.tmpdir(), 'sat-mesh-test-'));
  const filename = path.join(folder, 'fixture.stl');
  try {
    const data = Buffer.alloc(134);
    data.write('solid misleading-binary-header');
    data.writeUInt32LE(1, 80);
    [[0, 0, 0], [3, 0, 0], [0, 4, 2]].flat().forEach((value, index) => {
      data.writeFloatLE(value, 96 + index * 4);
    });
    fs.writeFileSync(filename, data);
    const info = inspectMesh(filename);
    assert.equal(info.format, 'STL-binary');
    assert.equal(info.faceCount, 1);
    assert.equal(info.vertexCount, 3);
    assert.deepEqual(info.boundingBox.spans, [3, 4, 2]);
  } finally {
    fs.unlinkSync(filename);
    fs.rmdirSync(folder);
  }
});
