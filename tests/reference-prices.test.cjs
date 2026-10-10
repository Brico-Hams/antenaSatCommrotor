const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const test = require('node:test');

const csv = fs.readFileSync(path.join(__dirname, '..', 'bom', 'reference-prices.csv'), 'utf8');
const [header, ...lines] = csv.trim().split(/\r?\n/);
const columns = header.split(',');
const rows = lines.map((line) => {
  const values = line.split(',');
  assert.equal(values.length, columns.length, `CSV column count: ${values[0]}`);
  return Object.fromEntries(columns.map((column, index) => [column, values[index]]));
});

test('pricing references distinguish observations and unresolved costs', () => {
  assert.equal(new Set(rows.map((row) => row.id)).size, rows.length);
  for (const row of rows) {
    assert.match(row.price_date, /^\d{4}-\d{2}-\d{2}$/);
    if (row.unit_reference_eur) {
      assert.ok(Number(row.unit_reference_eur) > 0, row.id);
      assert.ok(Number(row.observations) >= 1, row.id);
      assert.match(row.source, /^https:\/\//, row.id);
    } else {
      assert.equal(row.mean_eur, '', row.id);
      assert.equal(row.tax_basis, 'pending', row.id);
      assert.equal(row.observations, '0', row.id);
    }
    if (row.mean_eur) {
      assert.ok(Number(row.observations) >= 2, `${row.id}: a single quote is not a mean`);
    }
    if (row.quantity) assert.ok(Number(row.quantity) > 0, row.id);
  }
});

test('documented electronics subtotal includes two SDRs and three drivers and encoders', () => {
  const basket = { CM5: 1, CM5IO: 1, SDR: 2, DRV: 3, ENC: 3, COMPASS: 1, IMU: 1, GPS: 1 };
  let subtotal = 0;
  for (const [id, quantity] of Object.entries(basket)) {
    const row = rows.find((entry) => entry.id === id);
    assert.ok(row, id);
    assert.equal(Number(row.quantity), quantity, id);
    subtotal += quantity * Number(row.unit_reference_eur);
  }
  assert.equal(subtotal.toFixed(2), '1313.90');
  const asa = rows.find((row) => row.id === 'ASA');
  assert.equal((subtotal + Number(asa.unit_reference_eur)).toFixed(2), '1337.35');
  const battery = rows.find((row) => row.id === 'BAT');
  assert.equal(battery.tax_basis, 'displayed VAT inclusion unknown');
  assert.equal(Number(battery.unit_reference_eur), 99.99);
});
