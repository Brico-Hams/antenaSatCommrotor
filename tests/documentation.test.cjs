const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const test = require('node:test');

const root = path.join(__dirname, '..');
const documents = [
  path.join(root, 'README.md'),
  path.join(root, 'NOTICE.md'),
  path.join(root, 'AUTHORS.md'),
  path.join(root, 'ACKNOWLEDGEMENTS.md'),
  path.join(root, 'DISCLAIMER.md'),
  ...fs.readdirSync(path.join(root, 'docs')).filter((name) => name.endsWith('.md'))
    .map((name) => path.join(root, 'docs', name))
];

test('documentation local links resolve to persistent deliverables', () => {
  const missing = [];
  for (const filename of documents) {
    const text = fs.readFileSync(filename, 'utf8');
    for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
      const target = match[1].replace(/^<|>$/g, '').split('#')[0];
      if (!target || /^[a-z][a-z\d+.-]*:/i.test(target)) continue;
      const resolved = path.resolve(path.dirname(filename), decodeURIComponent(target));
      if (!fs.existsSync(resolved)) {
        missing.push(`${path.relative(root, filename)}: ${target}`);
      }
    }
  }
  assert.deepEqual(missing, []);
});
