const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=__dirname,dist=path.join(root,'dist'),cn=path.join(dist,'cn');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const roster=read('data/vctcn-rosters.json'),players=read('data/vctcn-players.json').players,agents=read('data/vctcn-agents.json');
assert.equal(roster.teams.length,12);assert.equal(players.length,roster.teams.reduce((n,t)=>n+t.players.length,0));assert.equal(new Set(players.map(p=>p.id)).size,players.length);
const ctx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(cn,'catalog.js'),'utf8'),ctx);assert.equal(ctx.window.VCT_CATALOG.players.length,players.length);
const files=[];function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else files.push(p)}}walk(cn);
for(const file of files){if(!/\.(html|css)$/.test(file))continue;const text=fs.readFileSync(file,'utf8');
 const refs=[...text.matchAll(/(?:src|href)="([^"#]+)"/g),...text.matchAll(/url\(['"]?([^)'";\s]+)['"]?\)/g),...text.matchAll(/@import\s+['"]([^'"]+)['"]/g)].map(m=>m[1]);
 for(const ref of refs){if(/^(https?:|data:)/.test(ref))continue;const resolved=path.resolve(path.dirname(file),ref.split(/[?#]/)[0]);assert.ok(resolved.startsWith(dist+path.sep));assert.ok(fs.existsSync(resolved),`Missing ${ref} in ${file}`)}
 if(file.endsWith('.html'))for(const m of text.matchAll(/href="#([^"#]+)"/g))assert.ok(text.includes(`id="${m[1]}"`),`Dead anchor #${m[1]} in ${file}`);
}
let maps=0,photos=0;for(const p of players){const file=path.join(cn,'players',p.slug,'index.html');assert.ok(fs.existsSync(file));const html=fs.readFileSync(file,'utf8');assert.ok(html.includes(p.handle));const data=html.match(/window\.VCT_PROFILE=([\s\S]+?);<\/script>/);assert.ok(data,`Missing profile data: ${p.handle}`);const config=JSON.parse(data[1]);assert.equal(config.id,p.id);assert.equal(config.maps,p.maps);
 assert.ok(fs.existsSync(path.resolve(path.dirname(file),config.portrait)));if(config.agentImage)assert.ok(fs.existsSync(path.resolve(path.dirname(file),config.agentImage)));
 for(const key of ['face','agentFace']){assert.equal(config[key].length,4);assert.ok(config[key].every(n=>Number.isFinite(n)&&n>=0&&n<=1),`Invalid framing: ${p.handle}`)}
 for(const a of p.agents){const c=a.cells;assert.equal(a.maps,Number(c[1].match(/\((\d+)\)/)[1]));assert.equal(a.acs,c[4]||null);assert.equal(a.kd,c[5]||null);assert.equal(a.kills,Number(c[11]||0));assert.equal(a.firstKills,Number(c[14]||0));maps+=a.maps}
 assert.equal(p.maps,p.agents.reduce((n,a)=>n+a.maps,0));assert.equal(p.kills,p.agents.reduce((n,a)=>n+a.kills,0));assert.equal(config.agents.length,Math.min(4,p.agents.length));
 for(const a of config.agents){assert.ok(agents[a.id]);assert.ok(fs.existsSync(path.resolve(path.dirname(file),a.image)))}
 for(const photo of config.photos){assert.ok(fs.existsSync(path.resolve(path.dirname(file),photo.file)));assert.ok(photo.source.startsWith('https://www.flickr.com/photos/valorantesports/'));assert.ok(photo.description.toLowerCase().includes(p.handle.toLowerCase()+' of'),`Wrong player caption: ${p.handle}`);photos++}
}
console.log(`PASS: ${roster.teams.length} teams, ${players.length} unique player pages, source-derived agent rows, ${photos} photos, all static links and assets.`);
