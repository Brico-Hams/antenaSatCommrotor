const fs = require('node:fs');
const zlib = require('node:zlib');
const assert = require('node:assert/strict');

module.exports = function validateRenderedPng(file, width = 1200, height = 800) {
  const png = fs.readFileSync(file);
  assert.equal(png.subarray(0, 8).toString('hex'), '89504e470d0a1a0a', file);
  assert.equal(png.readUInt32BE(16), width, file);
  assert.equal(png.readUInt32BE(20), height, file);
  assert.equal(png[24], 8, 'Expected 8-bit render');
  assert.ok([2, 6].includes(png[25]), 'Expected RGB or RGBA');
  assert.equal(png[28], 0, 'Expected non-interlaced render');
  const channels = png[25] === 6 ? 4 : 3;
  const chunks = [];
  let ended = false;
  for (let offset = 8; offset < png.length;) {
    const length = png.readUInt32BE(offset);
    const type = png.toString('ascii', offset + 4, offset + 8);
    assert.ok(offset + length + 12 <= png.length, 'Truncated PNG');
    if (type === 'IDAT') chunks.push(png.subarray(offset + 8, offset + 8 + length));
    if (type === 'IEND') ended = true;
    offset += length + 12;
  }
  assert.ok(ended && chunks.length > 0, file);
  const raw = zlib.inflateSync(Buffer.concat(chunks));
  const stride = width * channels;
  assert.equal(raw.length, (stride + 1) * height, file);
  const pixels = Buffer.alloc(stride * height);
  const paeth = (a,b,c) => {
    const p = a + b - c, pa = Math.abs(p-a), pb = Math.abs(p-b), pc = Math.abs(p-c);
    return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
  };
  for (let y = 0; y < height; y++) {
    const filter = raw[y * (stride + 1)];
    assert.ok(filter <= 4, 'Invalid PNG filter');
    for (let x = 0; x < stride; x++) {
      const left = x >= channels ? pixels[y * stride + x - channels] : 0;
      const above = y > 0 ? pixels[(y-1) * stride + x] : 0;
      const upperLeft = y > 0 && x >= channels ? pixels[(y-1)*stride+x-channels] : 0;
      const predict = [0, left, above, Math.floor((left+above)/2), paeth(left,above,upperLeft)][filter];
      pixels[y*stride+x] = (raw[y*(stride+1)+x+1] + predict) & 255;
    }
  }
  let foregroundPixels = 0;
  for (let i = 0; i < pixels.length; i += channels) {
    if (pixels[i] !== pixels[0] || pixels[i+1] !== pixels[1] || pixels[i+2] !== pixels[2]) foregroundPixels++;
  }
  assert.ok(foregroundPixels > 500, `${file}: empty or near-empty rendered geometry`);
  return { width, height, foregroundPixels };
};
