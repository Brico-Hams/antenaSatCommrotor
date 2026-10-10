const fs = require('node:fs');
const crypto = require('node:crypto');

function inspectMesh(filename) {
  const data = fs.readFileSync(filename);
  const sha256 = crypto.createHash('sha256').update(data).digest('hex');
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  let vertexCount = 0;
  let faceCount = 0;
  let objectCount = 0;
  let format;
  function vertex(coords) {
    if (!coords.every(Number.isFinite)) throw new Error('Non-finite mesh coordinates');
    coords.forEach((value, axis) => {
      min[axis] = Math.min(min[axis], value);
      max[axis] = Math.max(max[axis], value);
    });
    vertexCount++;
  }
  if (/\.obj$/i.test(filename)) {
    format = 'OBJ';
    for (const line of data.toString('utf8').split(/\r?\n/)) {
      if (/^v\s/.test(line)) vertex(line.trim().split(/\s+/).slice(1, 4).map(Number));
      else if (/^f\s/.test(line)) faceCount++;
      else if (/^o\s/.test(line)) objectCount++;
    }
  } else if (/\.stl$/i.test(filename)) {
    const binaryCount = data.length >= 84 ? data.readUInt32LE(80) : 0;
    if (data.length === 84 + binaryCount * 50) {
      format = 'STL-binary';
      faceCount = binaryCount;
      for (let triangle = 0; triangle < binaryCount; triangle++) {
        const start = 84 + triangle * 50 + 12;
        for (let corner = 0; corner < 3; corner++) {
          vertex([0, 1, 2].map((axis) => data.readFloatLE(start + corner * 12 + axis * 4)));
        }
      }
    } else {
      format = 'STL-ascii';
      for (const line of data.toString('utf8').split(/\r?\n/)) {
        const parts = line.trim().split(/\s+/);
        if (parts[0] === 'vertex') vertex(parts.slice(1, 4).map(Number));
        else if (parts[0] === 'facet') faceCount++;
      }
    }
  } else {
    throw new Error('Expected OBJ or STL');
  }
  if (!vertexCount || !faceCount) throw new Error('Mesh has no readable vertices/faces');
  return {
    filename, bytes: data.length, sha256, format, vertexCount, faceCount,
    objectCount: format === 'OBJ' ? objectCount : null,
    boundingBox: { min, max, spans: max.map((value, axis) => value - min[axis]) },
    units: 'unspecified-by-format',
    limitations: 'Read-only metadata, not a license, manifold, assembly or RF validation.'
  };
}

if (require.main === module) {
  const filenames = process.argv.slice(2);
  if (!filenames.length) throw new Error('Provide one or more local OBJ/STL paths');
  process.stdout.write(JSON.stringify(filenames.map(inspectMesh), null, 2) + '\n');
}
module.exports = { inspectMesh };
