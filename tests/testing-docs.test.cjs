const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const dirs = { es: "docs/testing", en: "docs/en/testing", hu: "docs/hu/testing" };
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");
const ids = (dir) => {
  const found = [];
  for (const f of fs.readdirSync(path.join(root, dir)).filter((n) => n.endsWith(".md")).sort())
    for (const m of read(`${dir}/${f}`).matchAll(/^### ([A-Z]{2,3}-\d{2})$/gm)) found.push(m[1]);
  return found;
};

test("testing section exists in es/en/hu with identical test ids", () => {
  const es = ids(dirs.es);
  assert.ok(es.length >= 70, `expected >= 70 tests, got ${es.length}`);
  assert.equal(new Set(es).size, es.length, "duplicate test ids");
  for (const lang of ["en", "hu"]) assert.deepEqual(ids(dirs[lang]), es, `${lang} ids differ`);
});

test("every test has action, expected behaviour, criterion and a pending record line", () => {
  for (const [lang, dir] of Object.entries(dirs)) {
    for (const f of fs.readdirSync(path.join(root, dir)).filter((n) => /^0[2-8]-/.test(n))) {
      const text = read(`${dir}/${f}`);
      const blocks = text.split(/^### /m).slice(1);
      for (const block of blocks) {
        assert.match(block, /- \[ \] \*\*[^*]+:\*\* .{15,}/, `${lang}/${f}: action`);
        assert.equal((block.match(/^- \*\*/gm) || []).length, 2, `${lang}/${f}: expected + criterion`);
        assert.match(block, /^- _.+_$/m, `${lang}/${f}: record line`);
      }
    }
  }
});

test("register CSV lists every test as PENDING", () => {
  const rows = read(`${dirs.es}/registro-pruebas.csv`).trim().split("\n").slice(1);
  const es = ids(dirs.es);
  assert.equal(rows.length, es.length);
  for (const r of rows) assert.ok(r.includes("PENDIENTE"), "no test may start approved");
  for (const lang of ["en", "hu"]) assert.equal(read(`${dirs[lang]}/registro-pruebas.csv`), read(`${dirs.es}/registro-pruebas.csv`));
});

test("links and figures in the testing docs resolve and carry the BricoHams branding", () => {
  for (const dir of Object.values(dirs)) {
    for (const f of fs.readdirSync(path.join(root, dir)).filter((n) => n.endsWith(".md"))) {
      for (const m of read(`${dir}/${f}`).matchAll(/\]\(([^)#\s]+)\)/g)) {
        if (/^https?:/.test(m[1])) continue;
        assert.ok(fs.existsSync(path.join(root, dir, m[1])), `${dir}/${f}: broken link ${m[1]}`);
      }
    }
  }
  for (const n of ["T1-banco-pruebas", "T2-comprobador-gpio", "T3-fixture-mecanico"])
    for (const suffix of ["", ".en", ".hu"]) {
      const svg = read(`docs/testing/fig/${n}${suffix}.svg`);
      assert.match(svg, /Anatol EA5KAO · Diego EA5JEF · Pedro Roca Molina/);
      assert.match(svg, /bricohams\.org/);
      assert.match(svg, /<image [^>]*data:image\/png;base64/, "logo embedded");
    }
});

test("GPIO tester figure lists every signal of the CM5 interface contract", () => {
  const gpio = JSON.parse(read("hardware/cm5/interface.json")).gpio;
  const svg = read("docs/testing/fig/T2-comprobador-gpio.svg");
  for (const g of gpio) assert.ok(svg.includes(g.signal), `missing ${g.signal}`);
  assert.match(read(`${dirs.es}/01-banco-de-pruebas.md`), new RegExp(`las ${gpio.length} señales`));
});

test("honest status wording and safety stops are present in all languages", () => {
  for (const dir of Object.values(dirs)) {
    const readme = read(`${dir}/README.md`);
    assert.match(readme, /PENDIENTE|PENDING|FÜGGŐ/);
    assert.match(read(`${dir}/02-electronica.md`), /ESTOP_AUX_N/);
    assert.match(read(`${dir}/07-app-android.md`), /CelesTrak/);
    assert.match(read(`${dir}/07-app-android.md`), /PE0SAT/);
  }
});
