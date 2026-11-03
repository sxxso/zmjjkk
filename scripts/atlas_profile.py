"""The shared player experience, using the original site's visual sequence."""
import html,json
E=lambda s:html.escape(str(s),quote=True)
def js(o):return json.dumps(o,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def img(src,alt='',cls='',loading='lazy'):return f'<img src="{E(src)}" alt="{E(alt)}" class="{cls}" loading="{loading}" decoding="async">'
def num(n):return f'{n:,}'
FACE={'jett': [0.48, 0.169, 0.08, 0.102], 'neon': [0.44, 0.185, 0.1, 0.125], 'raze': [0.423, 0.165, 0.09, 0.12], 'chamber': [0.416, 0.16, 0.09, 0.115], 'viper': [0.445, 0.15, 0.09, 0.14], 'killjoy': [0.425, 0.155, 0.09, 0.13], 'cypher': [0.425, 0.17, 0.09, 0.12], 'sova': [0.453, 0.125, 0.095, 0.115], 'omen': [0.43, 0.15, 0.14, 0.16], 'fade': [0.41, 0.2, 0.085, 0.12], 'gekko': [0.43, 0.135, 0.09, 0.12], 'breach': [0.392, 0.13, 0.1, 0.15], 'tejo': [0.434, 0.13, 0.09, 0.13], 'kayo': [0.419, 0.12, 0.11, 0.14], 'skye': [0.413, 0.15, 0.105, 0.13], 'harbor': [0.432, 0.12, 0.09, 0.12], 'vyse': [0.431, 0.13, 0.12, 0.14], 'phoenix': [0.402, 0.13, 0.09, 0.12], 'astra': [0.442, 0.16, 0.1, 0.12], 'brimstone': [0.441, 0.11, 0.11, 0.15], 'yoru': [0.43, 0.125, 0.105, 0.15], 'waylay': [0.4, 0.16, 0.1, 0.14], 'sage': [0.41, 0.15, 0.09, 0.13]}

def render(p,players,agents,teams,head,versioned,framing,agent_portraits):
 A=lambda s:'../../'+s
 pool=[dict(a,**agents[a['id']]) for a in p['agents'][:4]]
 main=pool[0] if pool else None
 portrait=versioned(A(p['portrait']));art=A(main['image']) if main else ''
 measured=framing[p['id']]
 face=measured['face'];aface=FACE.get(main['id'],[.47,.14,.11,.15]) if main else face
 frontal=agent_portraits.get(main['id']) if main else None
 photos=[dict(q,file=A(q['file'])) for q in p['photos']]
 config={k:p[k] for k in ['id','handle','name','team','maps','kills','portraitMissing']}
 config.update({'portrait':portrait,'agentImage':versioned(A(frontal['image'])) if frontal else art,'agentName':main['name'] if main else '',
  'face':face,'agentFace':frontal['face'] if frontal else aface,
  'playerEyes':measured.get('eyes'),'agentEyes':frontal['eyes'] if frontal else None,
  'portraitSize':p['portraitSize'],'agentPortraitSize':frontal['size'] if frontal else None,
  'agentPortraitKind':'ai-frontal-concept' if frontal else 'official-art',
  'agents':[dict(a,image=A(a['image'])) for a in pool],'photos':photos})
 teamlogo=A('assets/teams/'+p['team'].lower()+'.webp')
 # Wordmark is typographic. No player autograph is invented.
 name=p['handle'];split=max(2,len(name)//2)
 brand=f'<span>{E(name[:split])}</span><b>{E(name[split:])}.</b>'
 style=f'--accent:{p["color"]};--paper:{p["paper"]};--name-size:{min(25,144/max(4,len(name))):.2f}vw'
 canonical='<link rel="canonical" href="../../../index.html"><script>location.replace("../../../index.html"+location.hash)</script>' if p['id']=='3520' else ''
 page=head(name+' — '+p['team']+' / VCT CN','../../profile.css','../../')+canonical+f'<script>window.VCT_PROFILE={js(config)};</script><script defer src="{versioned("../../profile.js")}"></script></head><body class="profile" style="{style}">'
 page+=f'''<header class="p-header"><a class="p-brand" href="#home" aria-label="{E(name)} 首页">{brand}</a><a class="p-emblem" href="../../index.html#team={p['team']}" aria-label="{p['team']} 阵容">{img(teamlogo,'')}</a><nav><a class="p-atlas-link" href="../../index.html">选手合集 ↗</a><a class="p-highlight-link" href="#moments">赛场时刻</a><button class="p-menu-trigger" aria-label="打开选手导航" aria-haspopup="dialog"><i></i><i></i></button></nav></header><main>
<section class="p-hero-shell" id="home"><div class="p-hero"><div class="p-contours p-back-contours" aria-hidden="true"></div><div class="p-marquee" aria-hidden="true"><div>EVERY ROUND. {E(name)}. EVERY ROUND.</div><div>ALL IN. {E(p['team'])}. ALL IN. {E(p['team'])}.</div></div><div class="p-frame"><div class="p-contours p-hero-contours" aria-hidden="true"></div>{img(portrait,name,'p-portrait-fallback','eager')}<canvas class="p-canvas" role="img" aria-label="{E(name)}与{E(main['name']) if main else '英雄'}的交互肖像"></canvas><div class="p-portrait-caption"><b>{E(name)}</b><span>{E(p['name'])} / {p['team']}</span></div><a class="p-team-badge" href="../../index.html#team={p['team']}"><small>VCT CN / 2026</small>{img(teamlogo,p['team'])}<b>{p['team']}</b><span>{E(p['rosterStatus'])}</span></a><div class="p-hero-tools"><span id="p-hero-hint">{'尚无公开选手肖像' if p['portraitMissing'] else '划过人物，发现另一个自己'}</span><button id="p-hero-toggle" aria-pressed="false"><span>{E(name)}</span><i aria-hidden="true"></i><span>{E(main['en']) if main else '暂无统计'}</span></button><button id="p-motion-resume" hidden>开启动效</button></div><a class="p-scroll-cue" href="#identity"><span>向下探索</span><b>↓</b></a></div><div class="p-wordmark"><p>{E(p['teamName'])} / {E(p['name'])}</p><h1><span>{E(name[:split])}</span>{E(name[split:])}<b>.</b></h1><span>ALL IN. EVERY ROUND.</span></div></div></section>
<section class="p-dual" id="identity"><div class="p-contours" aria-hidden="true"></div>'''
 if main:page+=f'<div class="p-dual-portrait p-dual-agent"><canvas aria-hidden="true"></canvas></div>'
 page+='<div class="p-dual-portrait p-dual-player"><canvas aria-hidden="true"></canvas></div>'
 page+=f'''<div class="p-dual-copy"><a href="#agents"><h2><em>IN</em><br>GAME.</h2><p>{E(main['name']+' / '+main['role']) if main else '职业英雄数据'}<br>走进英雄池。</p><span>↗</span></a><a href="#moments"><h2><em>ON</em><br>STAGE.</h2><p>{E(name)} / {p['team']}<br>走进赛场时刻。</p><span>↗</span></a></div><div class="p-dual-label"><span>{E(main['en']) if main else 'VALORANT'}</span><span>{E(name)} / {E(p['name'])}</span></div></section>
<section class="p-manifesto"><div class="p-contours" aria-hidden="true"></div><p>{E(name)} / {p['team']}</p><h2><span>ONE NAME.</span><span>EVERY ROUND.</span><span><em>ALL IN.</em></span></h2><div><p>{E(p['name'])}，{E(p['teamName'])}。<br>从每次选下英雄，到每次站上赛场。</p><a href="#moments">继续探索 <b>↘</b></a></div></section>'''
 # An absolute-positioned photo field restores the original staggered long scroll.
 shots=[]
 if photos:
  for i,q in enumerate(photos):
   shots.append(f'<button class="p-shot p-shot-{i%8}" data-depth="{[.03,-.06,.05,-.04,.02,-.05,.04,-.02][i%8]}" data-photo-index="{i}" data-year="{q["year"] or ""}" aria-label="放大 {E(name)} 第{i+1}张赛场照片"><span>{q["year"] or ""} / {E(name)}</span>{img(q["file"],q["description"])}<i aria-hidden="true">放大 ↗</i></button>')
  years=sorted({q['year'] for q in photos if q['year']},reverse=True)
  controls=''.join(f'<button data-photo-year="{y}" aria-current="false">{y}</button>' for y in years)
  gallerynote='Riot Games / 官方赛场影像'
 else:
  # Varied source-backed visual chapters instead of four copies of a portrait poster.
  shots.append(f'<a class="p-shot p-shot-0 p-editorial-portrait" href="{E(p["official"] or p["vlr"])}" target="_blank" rel="noopener" data-depth=".03"><span>PORTRAIT / {E(name)}</span><div>{img(portrait,name)}<b>{E(name)}.</b></div></a>')
  if main:shots.append(f'<a class="p-shot p-shot-1 p-editorial-agent" href="#agents" data-depth="-.06"><span>{E(main["en"])} / {main["maps"]} 张地图</span>{img(art,main["name"])}</a>')
  for i,m in enumerate(p['matches'][:2]):
   shots.append(f'<a class="p-shot p-shot-{i+2} p-editorial-match" href="{E(m["url"])}" target="_blank" rel="noopener" data-depth=".04"><span>{E(m["date"])} / 比赛档案</span><div><small>{E(m["event"])}</small><h3>{E(" / ".join(m["teams"]))}</h3><strong>{E(" : ".join(m["score"]))}</strong><b>查看原始比赛 ↗</b></div></a>')
  controls='';gallerynote='官方肖像 / 英雄原画 / 比赛档案'
 gallerycount=len(shots);gallerywidth=max(120,42*gallerycount+12);mobilewidth=max(200,82*gallerycount+12)
 page+=f'''<section class="p-photo-section" id="moments"><div class="p-photo-stage"><div class="p-contours" aria-hidden="true"></div><div class="p-photo-title"><span>{E(name)} / {'赛场影像' if photos else '人物与赛场档案'}</span><h2>MOMENTS<br>THAT MATTER.</h2></div><div class="p-photo-window"><div class="p-photo-track" style="--gallery-width:{gallerywidth}vw;--gallery-mobile-width:{mobilewidth}vw" tabindex="0" aria-label="{'赛场照片' if photos else '人物档案'}长卷">{''.join(shots)}<div class="p-photo-quote"><em>{E(name)}.</em><p>{E(p['teamName'])}<br>{'每一瞬间，都是比赛的一部分。' if photos else '人物肖像与英雄原画；未收录本人赛场照片。'}</p></div></div></div><div class="p-photo-controls"><span>{gallerynote}</span><div class="p-photo-years">{controls}</div><div class="p-photo-progress" aria-hidden="true"><i></i></div><div><button data-photo-step="-1" aria-label="向前浏览长卷">←</button><button data-photo-step="1" aria-label="向后浏览长卷">→</button></div></div></div></section>
<section class="p-agent-section" id="agents"><div class="p-section-title"><p>{E(name)} / 职业英雄池</p><h2>DIFFERENT AGENTS.<br><em>SAME PLAYER.</em></h2><span>从最熟悉的英雄，看到每一种打法。</span></div>'''
 if pool:
  cards=''.join(f'<button class="p-agent-card" id="agent-tab-{a["id"]}" data-agent="{a["id"]}" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="p-agent-panel" tabindex="{0 if i==0 else -1}"><span class="p-agent-letter" aria-hidden="true">{E(a["en"][0])}</span>{img(A(a["image"]),a["name"])}<span class="p-agent-label"><b>{E(a["en"])} / {E(a["name"])}</b><em>{a["maps"]} <small>张</small></em></span><span class="p-agent-explore">探索战绩 ↗</span></button>' for i,a in enumerate(pool))
  a=pool[0];metrics=[('maps',a['maps'],'职业出场地图'),('acs',a['acs'] or '—','平均战斗评分 ACS'),('kd',a['kd'] or '—','击杀 / 死亡 K:D'),('kills',num(a['kills']),'总击杀'),('firstKills',num(a['firstKills']),'首杀')]
  detail=''.join(f'<div class="p-agent-metric"><strong data-metric="{k}">{v}</strong><span>{label}</span></div>' for k,v,label in metrics)
  page+=f'<div class="p-agent-cards" style="--agent-count:{len(pool)}" role="tablist" aria-label="选择英雄">{cards}</div><div class="p-agent-detail" id="p-agent-panel" role="tabpanel" aria-labelledby="agent-tab-{a["id"]}"><div><span id="p-agent-cn">{E(a["name"])}</span><h3 id="p-agent-en">{E(a["en"])}.</h3><p id="p-agent-use">{a["use"]} 全英雄使用占比</p></div>{detail}</div><p id="p-agent-announcement" class="sr-only" aria-live="polite"></p>'
 else:page+='<p class="p-empty-data">该选手暂未在 VLR 收录职业英雄统计。</p>'
 page+=f'<p class="p-data-note">VLR 全时期职业数据 · 2026-11-02 快照 · 出场单位为地图，使用占比不是胜率。<a href="{E(p["source"])}" target="_blank" rel="noopener">查看原始统计 ↗</a></p></section>'
 if photos:
  q=photos[0]
  page+=f'<section class="p-feature"><div class="p-feature-frame">{img(q["file"],q["description"])}<div><span>{q["year"] or ""} / {E(name)}</span><h2>ON STAGE.<br><em>IN THE MOMENT.</em></h2><a href="{E(q["source"])}" target="_blank" rel="noopener">查看原始影像 ↗</a></div></div></section>'
 kd=f'{p["kills"]/p["deaths"]:.2f}' if p['deaths'] else '—'
 page+=f'<section class="p-record" id="results"><div class="p-record-head"><div><span>{E(name)} / 比赛记录</span><h2>ONE PLAYER.<br><em>EVERY ROUND.</em></h2></div><div class="p-career"><div><strong>{num(p["maps"]) if p["maps"] else "—"}</strong>职业地图</div><div><strong>{num(p["kills"]) if p["maps"] else "—"}</strong>总击杀</div><div><strong>{kd}</strong>全英雄 K/D</div></div></div>'
 for m in p['matches']:
  maps=''.join(f'<a href="{E(g["url"])}" target="_blank" rel="noopener">{E(g["map"])}<br>{E(g["stats"])}</a>' for g in m['maps'])
  page+=f'<details class="p-result"><summary><time>{E(m["date"])}</time><h3>{E(m["event"])}</h3><span class="match-teams">{E(" / ".join(m["teams"]))}</span><strong class="match-score">{E(" : ".join(m["score"]))}</strong><i aria-hidden="true">+</i></summary><div class="p-map-list">{maps}<p><a href="{E(m["url"])}" target="_blank" rel="noopener">原始比赛记录 ↗</a></p></div></details>'
 if not p['matches']:page+='<p class="p-empty-data">暂未收录比赛记录。</p>'
 page+='<p class="p-match-source">最近已收录系列赛；生涯总计由全英雄表求和，K/D 为总击杀除以总死亡。</p></section>'
 teammates=[q for q in players if q['team']==p['team']];nxt=teammates[(teammates.index(p)+1)%len(teammates)]
 nexturl='../../../index.html' if nxt['id']=='3520' else '../'+nxt['slug']+'/index.html'
 page+=f'''<section class="p-next"><div class="p-contours" aria-hidden="true"></div>{img(versioned(A(nxt['portrait'])),'','p-next-portrait')}<a href="{nexturl}"><p>下一位 / {p['team']} 阵容</p><h2>KEEP<br><em>EXPLORING.</em></h2><span>{E(nxt['handle'])} <b>↗</b></span></a></section></main><footer class="p-footer"><a class="p-brand" href="#home">{brand}</a><a class="p-footer-word" href="../../index.html">ALL IN.<br><em>EVERY PLAYER.</em><span>↗</span></a><div><p>{E(name)} / 非官方粉丝作品<br>阵容与数据为 2026-11-02 快照。字标为排版设计。素材归各自权利人所有。</p><nav><a href="../../index.html">全部选手</a><button data-dialog="p-credits">资料与影像来源</button><button id="p-motion-toggle" aria-pressed="false">减少动态</button><a href="#home">回到顶部 ↑</a></nav></div></footer>
<dialog id="p-menu" class="p-dialog p-menu"><button class="p-dialog-close" aria-label="关闭导航">关闭 ×</button>{img(portrait,'','p-menu-portrait')}<div><p>{E(name)} / {p['team']}</p><nav><a href="#home">Home<small>首页</small></a><a href="#identity">Player × Agent<small>选手与英雄</small></a><a href="#moments">Moments<small>赛场时刻</small></a><a href="#agents">Agents<small>英雄池</small></a><a href="#results">Results<small>比赛记录</small></a><a href="../../index.html">Player Atlas<small>全部选手</small></a></nav></div></dialog>'''
 team=next(t for t in teams if t['code']==p['team'])
 page+=f'<dialog id="p-credits" class="p-dialog"><button class="p-dialog-close" aria-label="关闭来源">关闭 ×</button><h2>资料与影像</h2><ul><li><a href="{E(p["vlr"])}" target="_blank" rel="noopener">{E(name)} 的人物与英雄统计：VLR.gg</a></li><li><a href="{E(team["vlr"])}" target="_blank" rel="noopener">阵容状态：VLR 战队页，2026-11-02 快照</a></li><li><a href="{E(p["official"] or p["vlr"])}" target="_blank" rel="noopener">官方人物肖像：{E(p["portraitCredit"])}</a></li><li>英雄池立绘：Riot Games，经 Valorant-API 提供。首屏与双人画面的正面特工头像为基于原画制作的 AI 概念立绘；选手使用真实肖像。</li><li>{"赛事照片来自 Riot 官方 Flickr；逐张放大可查看摄影说明与原始页面。" if photos else "本页暂无已核实的本人赛场照片，长卷展示官方肖像、英雄原画和比赛档案。"}</li><li>选手字标为排版设计，未制作或模仿本人签名。</li></ul></dialog>'
 if photos:page+='<dialog id="p-photo-dialog" class="p-dialog p-photo-dialog"><button class="p-dialog-close" aria-label="关闭照片">关闭 ×</button><img alt=""><p></p><div class="p-photo-nav"><a id="p-photo-source" href="#" target="_blank" rel="noopener">原始照片与摄影说明 ↗</a><div><button id="p-photo-prev" aria-label="上一张照片">←</button><button id="p-photo-next" aria-label="下一张照片">→</button></div></div></dialog>'
 return page+'</body></html>'
