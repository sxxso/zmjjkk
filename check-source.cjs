const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const root = __dirname;
const scope = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'dist/agent-data.js'), 'utf8'), scope);
const displayed = scope.window.KK_AGENT_DATA;
const source = JSON.parse(fs.readFileSync(path.join(root, 'agent-source.json'), 'utf8'));
assert.equal(displayed.retrieved, source.retrieved);
assert.equal(displayed.agents.length, 4);
for (const a of displayed.agents) {
  const cells = source.rows.find(row => row.agent === a.id).cells;
  assert.equal(a.maps, Number(cells[1].match(/\((\d+)\)/)[1]));
  assert.equal(a.use, cells[1].split(' ').at(-1));
  assert.equal(a.acs, cells[4]);
  assert.equal(a.kd, cells[5]);
  assert.equal(a.kills, Number(cells[11]));
  assert.equal(a.firstKills, Number(cells[14]));
  assert.ok(fs.existsSync(path.join(root, `dist/assets/${a.id}.webp`)));
}
const html = fs.readFileSync(path.join(root, 'dist/index.html'), 'utf8');
for (const match of html.matchAll(/(?:src|href|data-photo)="([^"#]+)"/g)) {
  const url = match[1];
  if (/^https?:/.test(url)) continue;
  assert.ok(fs.existsSync(path.join(root, 'dist', url.split(/[?#]/)[0])), `Missing ${url}`);
}
const photos = JSON.parse(fs.readFileSync(path.join(root, 'photo-sources-v4.json'), 'utf8'));
const photoResearch = JSON.parse(fs.readFileSync(path.join(root, 'photo-research-v4.json'), 'utf8'));
const shots = [...html.matchAll(/<button class="shot [^>]+>/g)].map(match => match[0]);
assert.equal(shots.length, photos.length);
for (const photo of photos) {
  const shot = shots.find(tag => tag.includes(`data-photo="assets/${photo.file}"`));
  assert.ok(shot, `Missing gallery photo ${photo.file}`);
  assert.ok(shot.includes(`data-year="${photo.year}"`));
  assert.ok(shot.includes(`data-source="${photo.page}"`));
  if (photo.year >= 2025) {
    const original = photoResearch.find(item => item.page === photo.page);
    assert.ok(original, `Missing original caption for ${photo.file}`);
    assert.match(original.description, /ZmjjKK/);
    assert.ok(original.description.includes(String(photo.year)));
    assert.equal(original.local, photo.file);
  }
}
assert.equal(photos.filter(photo => photo.year === 2025).length, 3);
assert.equal(photos.filter(photo => photo.year === 2026).length, 3);
// Follow the actual HTML/CSS/JS asset graph, including SVG images and font URLs.
const dist = path.join(root, 'dist');
const seen = new Set();
const pending = [path.join(dist, 'index.html')];
while (pending.length) {
  const file = pending.pop();
  if (seen.has(file)) continue;
  assert.ok(file.startsWith(dist + path.sep), `Asset escapes dist: ${file}`);
  assert.ok(fs.existsSync(file), `Missing asset ${file}`);
  seen.add(file);
  if (!/\.(html|css|js)$/.test(file)) continue;
  const content = fs.readFileSync(file, 'utf8');
  const refs = [];
  if (file.endsWith('.html')) {
    for (const m of content.matchAll(/(?:src|href|data-photo)="([^"#]+)"/g)) refs.push(m[1]);
  }
  for (const m of content.matchAll(/['"](assets\/[^'"]+)['"]/g)) refs.push(m[1]);
  for (const m of content.matchAll(/url\(['"]?([^)'"#]+)['"]?\)/g)) refs.push(m[1]);
  for (const ref of refs) {
    if (/^(https?:|data:|#)/.test(ref)) continue;
    pending.push(path.resolve(path.dirname(file), ref.split(/[?#]/)[0]));
  }
}
console.log(`PASS: agent values, 10 gallery sources/year labels, and ${seen.size} reachable local files.`);
