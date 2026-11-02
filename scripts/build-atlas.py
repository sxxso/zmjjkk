"""Deterministic static generation: one directory and a complete page per player."""
from pathlib import Path
import json,html,re,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/cn';DATA=ROOT/'data'
sys.stdout.reconfigure(encoding='utf8')
snapshot=json.loads((DATA/'vctcn-rosters.json').read_text(encoding='utf8'))
players=json.loads((DATA/'vctcn-players.json').read_text(encoding='utf8'))['players']
agents=json.loads((DATA/'vctcn-agents.json').read_text(encoding='utf8'))
teams=snapshot['teams'];E=lambda s:html.escape(str(s),quote=True)
def js(o):return json.dumps(o,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def img(src,alt='',cls='',loading='lazy'):return f'<img src="{E(src)}" alt="{E(alt)}" class="{cls}" loading="{loading}" decoding="async">'
def num(n):return f'{n:,}'
def versioned(s):return s+'?v='+hashlib.sha256((OUT/Path(s).name).read_bytes()).hexdigest()[:10]
def head(title,css,level=''):
 return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#eef1ef"><meta name="description" content="VCT CN 选手个人站合集。真实人物肖像、英雄池、赛场影像和比赛记录。非官方粉丝作品。"><title>{E(title)}</title><link rel="icon" href="{level}../assets/icon.svg"><link rel="stylesheet" href="{versioned(css)}"><script defer src="{level}../assets/gsap.min.js"></script><script defer src="{level}../assets/ScrollTrigger.min.js"></script>'
catalog=[]
for p in players:
 a=agents.get(p['agents'][0]['id']) if p['agents'] else None
 catalog.append({k:p[k] for k in ['id','slug','handle','name','realName','team','teamName','color','paper','portrait','portraitMissing','rosterStatus','maps','kills']}|{'agentName':a['name'] if a else '', 'role':a['role'] if a else '', 'agentImage':a['image'] if a else ''})
featured=['ZmjjKK','whzy','Life','Rarga','BerLIN','yosemite']
featured=[p for handle in featured for p in catalog if p['handle']==handle][:6]
if len(featured)<3:featured=catalog[:4]
teamdata=[{k:t[k] for k in ['code','name','color','paper','official','vlr']} for t in teams]
(OUT/'catalog.js').write_text('window.VCT_CATALOG='+js({'date':snapshot['date'],'players':catalog,'teams':teamdata,'featured':[p['id'] for p in featured]})+';',encoding='utf8')
count=len(players)
teamfilters=''.join(f'<button data-team="{t["code"]}" aria-pressed="false">{img("assets/teams/"+t["code"].lower()+".webp","")}{t["code"]}</button>' for t in teams)
roles=sorted(set(a['role'] for a in agents.values()))
options=''.join(f'<option value="{E(r)}">{E(r)}</option>' for r in roles)
stack=''.join(img(p['portrait'],p['handle'],'stack-portrait '+cls,'eager' if cls=='front' else 'lazy') for p,cls in zip([featured[-1],featured[0],featured[1]],['back-left','front','back-right']))
tick=''.join(f'<span>✦</span>{t["code"]}' for t in teams)*2
hub=head('VCT CN — 每个人，都是主角。','atlas.css')+'''<script defer src="catalog.js"></script><script defer src="atlas.js"></script></head><body>
<header class="atlas-header"><a class="atlas-brand" href="index.html" aria-label="VCT CN 选手合集首页"><svg viewBox="0 0 54 50" aria-hidden="true"><path d="M7 3h10l-7 25h12l7-25h10l-6 21L47 3h7L34 32h-9l-4 15H11l3-10H0zm29 31h11L35 49H24z"/></svg><span>VCT CN<br>Player Atlas</span></a><nav><a href="../index.html">康康原版</a><a href="#directory" class="go-directory">探索选手</a></nav></header>
<main><section class="atlas-hero" aria-label="中国赛场的每一位主角"><div class="hero-copy"><p>中国赛场，每个人都是主角。</p><h1><span>EVERY</span><span><em>PLAYER.</em></span></h1><p class="hero-intro">从站上赛场，到成为焦点。<br>走进每一位选手的世界。</p>'''+f'<div class="hero-stats"><b>12<small>支参赛战队</small></b><b>{count}<small>个独立选手站</small></b><b>2026<small>VCT CN 赛季</small></b></div></div><div class="portrait-stack"><div class="cast-ring"></div>{stack}</div><div class="cast-label"><button class="round-button" data-cast="-1" aria-label="上一位焦点选手">←</button><a id="featured-link" href="players/{featured[0]["slug"]}/index.html"><small id="featured-team">{E(featured[0]["team"])} / {E(featured[0]["name"])}</small><b id="featured-name">{E(featured[0]["handle"])} ↗</b></a><button class="round-button" data-cast="1" aria-label="下一位焦点选手">→</button></div><div class="atlas-hero-bottom"><a href="#directory">向下探索 ↓</a><span>非官方粉丝选手档案 / 2026.11.02</span></div><p class="sr-only" id="cast-announcement" aria-live="polite"></p></section><div class="ticker" aria-hidden="true"><div>{tick}</div></div>'+'''
<section class="directory" id="directory" aria-labelledby="directory-title"><div class="directory-heading"><h2 id="directory-title">找到你的<br><em>赛场主角。</em></h2><p>按战队、名字或英雄定位探索。<br>每个名字背后，都有一个完整的个人站。</p></div><div class="filter-panel"><div class="filter-top"><label class="search-wrap"><span aria-hidden="true">⌕</span><input id="player-search" type="search" placeholder="搜索选手 ID、姓名或战队" aria-label="搜索选手"><button id="clear-search" type="button" aria-label="清除搜索">×</button></label><select id="role-filter" aria-label="按主要英雄定位筛选"><option value="all">全部英雄定位</option>'''+options+'''</select><select id="sort-order" aria-label="选手排序"><option value="team">按战队排列</option><option value="name">按选手 ID</option><option value="maps">出场地图最多</option><option value="kills">总击杀最多</option></select><div class="view-options" aria-label="展示方式"><button data-view="grid" aria-pressed="true">画廊</button><button data-view="list" aria-pressed="false">列表</button></div></div><div class="team-filters" aria-label="按战队筛选"><button data-team="all" aria-pressed="true">全部战队</button>'''+teamfilters+'''</div></div><div class="directory-meta"><span id="result-count" aria-live="polite"></span><label><input type="checkbox" id="include-bench" checked>含替补与非活跃选手</label></div><div class="player-grid" id="player-grid"></div><div class="empty-state" id="empty-state" hidden><h3>没有找到符合条件的选手</h3><p>试试其他名字，或放宽战队与定位筛选。</p><button id="reset-filters">重置筛选</button></div><noscript><p>请启用 JavaScript 使用筛选；仍可直接访问选手网站。</p>'''+''.join(f'<p><a href="players/{p["slug"]}/index.html">{E(p["team"])} / {E(p["handle"])}</a></p>' for p in players)+'''</noscript></section></main>
<footer class="atlas-footer"><h2>ALL IN.<br>EVERY PLAYER.</h2><div class="footer-row"><p>2026 VCT CN 的 12 支参赛战队。阵容与全时期职业数据为 2026-11-02 公开快照，非实时转会名单；替补与非活跃状态以 VLR 阵容标记为准。人物肖像优先来自 Riot 官方选手页。照片、角色及商标归各自权利人所有。</p><nav><a href="../index.html">康康原版</a><a href="https://github.com/sxxso/zmjjkk-player-site" target="_blank" rel="noopener">项目源码</a><a href="https://valorantesports.com/en-US/season/115571062868511862/handbook" target="_blank" rel="noopener">官方赛区</a></nav></div></footer><button id="back-to-top" class="back-to-top" aria-label="回到顶部">↑</button></body></html>'''
hub=hub.replace('src="catalog.js"','src="'+versioned('catalog.js')+'"').replace('src="atlas.js"','src="'+versioned('atlas.js')+'"')
(OUT/'index.html').write_text(hub,encoding='utf8')

for index,p in enumerate(players):
 dest=OUT/'players'/p['slug'];dest.mkdir(parents=True,exist_ok=True)
 A=lambda s:'../../'+s
 pool=[dict(a,**agents[a['id']]) for a in p['agents'][:4]]
 mainagent=pool[0] if pool else None
 agentimage=A(mainagent['image']) if mainagent else ''
 photos=[dict(photo,file=A(photo['file'])) for photo in p['photos']]
 profile={k:p[k] for k in ['id','handle','name','team','maps','kills','portraitMissing']}
 profile.update({'portrait':A(p['portrait']),'agentImage':agentimage,'agentName':mainagent['name'] if mainagent else '',
  'agents':[dict(a,image=A(a['image'])) for a in pool],'photos':photos})
 title=p['handle']+' — '+p['team']+' / VCT CN'
 page=head(title,'../../profile.css','../../')+f'<script>window.VCT_PROFILE={js(profile)};</script><script defer src="../../profile.js"></script></head><body class="profile" style="--accent:{p["color"]};--paper:{p["paper"]}">'
 page+=f'''<header class="p-header"><a href="../../index.html">VCT CN<span>Player Atlas</span></a><nav><a href="../../index.html#team={p['team']}">{p['team']} 阵容</a><button class="p-menu-trigger" aria-label="打开选手导航" aria-haspopup="dialog">☰</button></nav></header><main><section class="p-hero-shell" id="home"><div class="p-hero"><div class="p-marquee" aria-hidden="true"><div>{E(p['handle'])}. {E(p['team'])}. EVERY ROUND. {E(p['handle'])}.</div><div>ALL IN. EVERY PLAYER. ALL IN. EVERY PLAYER.</div></div><div class="p-frame">{img(A('assets/teams/'+p['team'].lower()+'.webp'),'','p-team-watermark')}{img(A(p['portrait']),p['handle'],'p-portrait-fallback','eager')}<canvas class="p-canvas" role="img" aria-label="{E(p['handle'])}与主要英雄的交互肖像"></canvas><div class="p-frame-tag"><b>{E(p['team'])}</b>{E(p['teamName'])}<br>{E(p['rosterStatus'])}</div><div class="p-frame-tag right">{E(p['handle'])}<br>{E(p['name'])}</div><div class="p-hero-tools"><span id="p-hero-hint">{'尚无公开选手肖像' if p['portraitMissing'] else '移动鼠标，发现另一个自己'}</span><button id="p-hero-toggle" aria-pressed="false">{E(p['handle'])} / {E(mainagent['en']) if mainagent else '暂无英雄统计'}</button><button id="p-motion-resume" hidden>开启动效</button></div><div class="p-hero-bottom"><span>VCT CN / 2026</span><a href="#identity">向下探索 ↓</a></div></div><div class="p-wordmark"><p>{E(p['teamName'])} / {E(p['name'])}</p><h1>{E(p['handle'])}.</h1><span>ALL IN. EVERY ROUND.</span></div></div></section>'''
 page+=f'''<section class="p-dual" id="identity">{('<div class="p-dual-agent">'+img(agentimage,'Riot 官方英雄立绘')+'</div>') if mainagent else ''}{img(A(p['portrait']),p['handle'],'p-dual-player')}<div class="p-dual-copy"><a href="#agents"><h2><em>IN</em><br>GAME</h2><p>{E(mainagent['name']+' / '+mainagent['role']) if mainagent else '职业英雄数据'}<br>走进英雄池。</p><span>↗</span></a><a href="#{'moments' if photos or p['matches'] else 'results'}"><h2><em>ON</em><br>STAGE</h2><p>{E(p['handle'])} / {E(p['team'])}<br>看见每个赛场瞬间。</p><span>↗</span></a></div><div class="p-dual-label"><span>{E(mainagent['en']) if mainagent else 'VALORANT'}</span><span>{E(p['handle'])} / {E(p['name'])}</span></div></section>'''
 if photos:
  shots=''.join(f'<button class="p-shot" data-photo="{i}" aria-label="放大第{i+1}张赛场照片"><span>{photo["year"] or ""} / {E(p["handle"])}</span>{img(photo["file"],photo["description"])}<i aria-hidden="true">+</i></button>' for i,photo in enumerate(photos))
  page+=f'''<section class="p-photo-section" id="moments"><div class="p-photo-stage"><div class="p-photo-title"><span>{E(p['handle'])} / 赛场影像</span><h2>MOMENTS<br>THAT MATTER.</h2></div><div class="p-photo-window"><div class="p-photo-track">{shots}</div></div><div class="p-photo-controls"><span>Riot Games / 官方赛场照片 · 点击放大</span><div><button data-photo-step="-1" aria-label="向前浏览照片">←</button><button data-photo-step="1" aria-label="向后浏览照片">→</button></div></div></div></section>'''
 elif p['matches']:
  posters=[]
  for mi,m in enumerate(p['matches'][:4]):
   g=m['maps'][0] if m['maps'] else None
   gameagent=agents.get(g['agent']) if g else mainagent
   art=A(gameagent['image']) if gameagent else agentimage
   posters.append(f'<a class="p-reel-poster" href="{E(m["url"])}" target="_blank" rel="noopener" style="--poster-index:{mi}"><span class="reel-date">{E(m["date"])} / {E(p["handle"])}</span><div class="reel-image">{img(A(p["portrait"]),p["handle"],"reel-player")}{img(art,"","reel-agent") if art else ""}<span class="reel-score">{E(" : ".join(m["score"]))}</span></div><div class="reel-caption"><h3>{E(" / ".join(m["teams"]))}</h3><span>↗</span><p>{E(m["event"])}</p><small>{E(g["stats"]) if g else "打开比赛记录"}</small></div></a>')
  page+=f'<section class="p-photo-section" id="moments"><div class="p-photo-stage"><div class="p-photo-title"><span>{E(p["handle"])} / 赛场档案</span><h2>IN EVERY<br>ROUND.</h2></div><div class="p-photo-window"><div class="p-photo-track p-reel-track">{"".join(posters)}</div></div><div class="p-photo-controls"><span>人物 × 比赛数据海报 · 点击打开原始记录</span><div><button data-photo-step="-1" aria-label="向前浏览档案">←</button><button data-photo-step="1" aria-label="向后浏览档案">→</button></div></div></div></section>'
 page+='''<section class="p-agent-section" id="agents"><div class="p-section-title"><p>英雄池 / 按职业出场地图排序</p><h2>HEROES<br><em>ON DUTY.</em></h2><span>每一次选下英雄，都是另一种表达。</span></div>'''
 if pool:
  cards=''.join(f'<button class="p-agent-card" id="agent-tab-{a["id"]}" data-agent="{a["id"]}" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="p-agent-panel" tabindex="{0 if i==0 else -1}">{img(A(a["image"]),a["name"])}<span><b>{E(a["name"])}</b><em>{a["maps"]} <small>张</small></em></span></button>' for i,a in enumerate(pool))
  a=pool[0]; metrics=[('maps',a['maps'],'出场地图'),('acs',a['acs'] or '—','平均战斗评分'),('kd',a['kd'] or '—','击杀 / 死亡'),('kills',num(a['kills']),'总击杀'),('firstKills',num(a['firstKills']),'首杀')]
  detail=''.join(f'<div class="p-agent-metric"><strong data-metric="{k}">{v}</strong><span>{label}</span></div>' for k,v,label in metrics)
  page+=f'<div class="p-agent-cards" role="tablist" aria-label="选择英雄">{cards}</div><div class="p-agent-detail" id="p-agent-panel" role="tabpanel" aria-labelledby="agent-tab-{a["id"]}"><div><h3 id="p-agent-en">{E(a["en"])}.</h3><p class="agent-subname" id="p-agent-use">{E(a["name"])} / {a["use"]} 使用占比</p></div>{detail}</div><p id="p-agent-announcement" class="sr-only" aria-live="polite"></p>'
 else:page+='<p class="p-empty-data">该选手暂未在 VLR 收录职业英雄统计。新增数据可在下次更新时纳入。</p>'
 page+=f'<p class="p-data-note">VLR 全时期已收录职业数据 · 2026-11-02 快照 · 出场单位为地图，使用占比不是胜率。<a href="{E(p["source"])}" target="_blank" rel="noopener">查看该选手原始统计</a></p></section>'
 deaths=p['deaths'];kd=f'{p["kills"]/deaths:.2f}' if deaths else '—'
 page+=f'<section class="p-record" id="results"><div class="p-record-head"><h2>EVERY<br><em>ROUND.</em></h2><div class="p-career"><div><strong>{num(p["maps"]) if p["maps"] else "—"}</strong>职业地图</div><div><strong>{num(p["kills"]) if p["maps"] else "—"}</strong>总击杀</div><div><strong>{kd}</strong>全英雄 K/D</div></div></div>'
 for m in p['matches']:
  event=m['event'];maps=''.join(f'<a href="{E(g["url"])}" target="_blank" rel="noopener">{E(g["map"])}<br>{E(g["stats"])}</a>' for g in m['maps'])
  page+=f'<details class="p-result"><summary><time>{E(m["date"])}</time><h3>{E(event)}</h3><span class="match-teams">{E(" / ".join(m["teams"]))}</span><strong class="match-score">{E(" : ".join(m["score"]))}</strong><i aria-hidden="true">+</i></summary><div class="p-map-list">{maps}<p><a href="{E(m["url"])}" target="_blank" rel="noopener">打开原始比赛记录 ↗</a></p></div></details>'
 if not p['matches']:page+='<p class="p-empty-data" style="color:var(--ink)">暂未收录比赛记录。以原始选手资料页为准。</p>'
 page+='<p class="p-match-source">最近已收录系列赛；日期和比分沿用 VLR 公开记录。上方生涯总计由全英雄表求和，K/D 为总击杀除以总死亡。</p></section>'
 teamplayers=[q for q in players if q['team']==p['team']];nextp=teamplayers[(teamplayers.index(p)+1)%len(teamplayers)]
 page+=f'<section class="p-next"><div><p>下一位 / {p["team"]} 阵容</p><h2><a href="../{nextp["slug"]}/index.html">{E(nextp["handle"])}.</a></h2></div><a href="../{nextp["slug"]}/index.html" aria-label="探索下一位选手 {E(nextp["handle"])}">↗</a></section></main><footer class="p-footer"><p>{E(p["handle"])} 非官方粉丝个人站。阵容与数据为 2026-11-02 快照，选手字标为排版设计。人物肖像、赛事照片、英雄与商标归各自权利人所有。</p><nav><a href="../../index.html">全部选手</a><button data-dialog="p-credits" class="p-motion">素材来源</button><button id="p-motion-toggle" class="p-motion" aria-pressed="false">减少动态</button></nav></footer>'
 page+='''<dialog id="p-menu" class="p-dialog p-menu"><button class="p-dialog-close" aria-label="关闭导航">关闭 ×</button><nav><a href="#home">Home<small>首页</small></a><a href="#identity">Player × Agent<small>选手与英雄</small></a>'''+('<a href="#moments">Moments<small>赛场档案</small></a>' if photos or p['matches'] else '')+'''<a href="#agents">Agents<small>英雄池</small></a><a href="#results">Results<small>比赛记录</small></a><a href="../../index.html">Player Atlas<small>全部选手</small></a></nav></dialog>'''
 page+=f'<dialog id="p-credits" class="p-dialog"><button class="p-dialog-close" aria-label="关闭来源">关闭 ×</button><h2>资料与素材</h2><ul><li><a href="{E(p["vlr"])}" target="_blank" rel="noopener">{E(p["handle"])} 的人物资料与全时期英雄统计：VLR.gg</a></li><li><a href="{E(next(t["vlr"] for t in teams if t["code"]==p["team"]))}" target="_blank" rel="noopener">阵容及替补 / 非活跃状态：VLR 战队页面，2026-11-02 快照</a></li><li><a href="{E(p["official"] or p["vlr"])}" target="_blank" rel="noopener">人物肖像：{E(p["portraitCredit"])}</a></li><li>英雄原画：Riot Games，经 Valorant-API 提供。每位选手展示其生涯出场最多的四位英雄。</li><li>赛场照片来自 Riot 官方 Flickr 账号；放大照片可打开对应原始页面，完整摄影说明一并保留。</li><li>选手 ID 字标为排版设计；未制作或模仿本人签名。</li></ul></dialog>'
 if photos:page+='<dialog id="p-photo-dialog" class="p-dialog p-photo-dialog"><button class="p-dialog-close" aria-label="关闭照片">关闭 ×</button><img alt=""><p></p><div class="p-photo-nav"><a id="p-photo-source" href="#" target="_blank" rel="noopener">原始照片与摄影说明 ↗</a><div><button id="p-photo-prev" aria-label="上一张照片">←</button><button id="p-photo-next" aria-label="下一张照片">→</button></div></div></dialog>'
 page+='</body></html>'
 page=page.replace('src="../../profile.js"','src="'+versioned('../../profile.js')+'"')
 (dest/'index.html').write_text(page,encoding='utf8')
print('GENERATED',count,'player pages and the directory')
