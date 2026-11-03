"""Deterministic static generation: one directory and a complete page per player."""
from pathlib import Path
import json,html,re,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/cn';DATA=ROOT/'data'
sys.stdout.reconfigure(encoding='utf8')
snapshot=json.loads((DATA/'vctcn-rosters.json').read_text(encoding='utf8'))
players=json.loads((DATA/'vctcn-players.json').read_text(encoding='utf8'))['players']
agents=json.loads((DATA/'vctcn-agents.json').read_text(encoding='utf8'))
teams=snapshot['teams'];E=lambda s:html.escape(str(s),quote=True)
from atlas_styles import build_styles
build_styles(ROOT,OUT)
def js(o):return json.dumps(o,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def img(src,alt='',cls='',loading='lazy'):return f'<img src="{E(src)}" alt="{E(alt)}" class="{cls}" loading="{loading}" decoding="async">'
def num(n):return f'{n:,}'
asset_versions={}
def versioned(s):
 local=re.sub(r'^(?:\.\./)+','',s)
 if local not in asset_versions:asset_versions[local]=hashlib.sha256((OUT/local).read_bytes()).hexdigest()[:10]
 return s+'?v='+asset_versions[local]
def head(title,css,level=''):
 return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#eef1ef"><meta name="description" content="VCT CN 选手个人站合集。真实人物肖像、英雄池、赛场影像和比赛记录。非官方粉丝作品。"><title>{E(title)}</title><link rel="icon" href="{level}../assets/icon.svg"><link rel="stylesheet" href="{versioned(css)}"><script defer src="{level}../assets/gsap.min.js"></script><script defer src="{level}../assets/ScrollTrigger.min.js"></script>'
catalog=[]
for p in players:
 a=agents.get(p['agents'][0]['id']) if p['agents'] else None
 catalog.append({k:p[k] for k in ['id','slug','handle','name','realName','team','teamName','color','paper','portrait','portraitMissing','rosterStatus','maps','kills']}|{'portrait':versioned(p['portrait']),'url':'../index.html' if p['id']=='3520' else 'players/'+p['slug']+'/index.html','agentName':a['name'] if a else '', 'role':a['role'] if a else '', 'agentImage':a['image'] if a else ''})
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
<main><section class="atlas-hero" aria-label="中国赛场的每一位主角"><div class="hero-copy"><p>中国赛场，每个人都是主角。</p><h1><span>EVERY</span><span><em>PLAYER.</em></span></h1><p class="hero-intro">从站上赛场，到成为焦点。<br>走进每一位选手的世界。</p>'''+f'<div class="hero-stats"><b>12<small>支参赛战队</small></b><b>{count}<small>个独立选手站</small></b><b>2026<small>VCT CN 赛季</small></b></div></div><div class="portrait-stack"><div class="cast-ring"></div>{stack}</div><div class="cast-label"><button class="round-button" data-cast="-1" aria-label="上一位焦点选手">←</button><a id="featured-link" href="{featured[0]["url"]}"><small id="featured-team">{E(featured[0]["team"])} / {E(featured[0]["name"])}</small><b id="featured-name">{E(featured[0]["handle"])} ↗</b></a><button class="round-button" data-cast="1" aria-label="下一位焦点选手">→</button></div><div class="atlas-hero-bottom"><a href="#directory">向下探索 ↓</a><span>非官方粉丝选手档案 / 2026.11.02</span></div><p class="sr-only" id="cast-announcement" aria-live="polite"></p></section><div class="ticker" aria-hidden="true"><div>{tick}</div></div>'+'''
<section class="directory" id="directory" aria-labelledby="directory-title"><div class="directory-heading"><h2 id="directory-title">找到你的<br><em>赛场主角。</em></h2><p>按战队、名字或英雄定位探索。<br>每个名字背后，都有一个完整的个人站。</p></div><div class="filter-panel"><div class="filter-top"><label class="search-wrap"><span aria-hidden="true">⌕</span><input id="player-search" type="search" placeholder="搜索选手 ID、姓名或战队" aria-label="搜索选手"><button id="clear-search" type="button" aria-label="清除搜索">×</button></label><select id="role-filter" aria-label="按主要英雄定位筛选"><option value="all">全部英雄定位</option>'''+options+'''</select><select id="sort-order" aria-label="选手排序"><option value="team">按战队排列</option><option value="name">按选手 ID</option><option value="maps">出场地图最多</option><option value="kills">总击杀最多</option></select><div class="view-options" aria-label="展示方式"><button data-view="grid" aria-pressed="true">画廊</button><button data-view="list" aria-pressed="false">列表</button></div></div><div class="team-filters" aria-label="按战队筛选"><button data-team="all" aria-pressed="true">全部战队</button>'''+teamfilters+'''</div></div><div class="directory-meta"><span id="result-count" aria-live="polite"></span><label><input type="checkbox" id="include-bench" checked>含替补与非活跃选手</label></div><div class="player-grid" id="player-grid"></div><div class="empty-state" id="empty-state" hidden><h3>没有找到符合条件的选手</h3><p>试试其他名字，或放宽战队与定位筛选。</p><button id="reset-filters">重置筛选</button></div><noscript><p>请启用 JavaScript 使用筛选；仍可直接访问选手网站。</p>'''+''.join(f'<p><a href="{p["url"]}">{E(p["team"])} / {E(p["handle"])}</a></p>' for p in catalog)+'''</noscript></section></main>
<footer class="atlas-footer"><h2>ALL IN.<br>EVERY PLAYER.</h2><div class="footer-row"><p>2026 VCT CN 的 12 支参赛战队。阵容与全时期职业数据为 2026-11-02 公开快照，非实时转会名单；替补与非活跃状态以 VLR 阵容标记为准。人物肖像优先来自 Riot 官方选手页。照片、角色及商标归各自权利人所有。</p><nav><a href="../index.html">康康原版</a><a href="https://github.com/sxxso/zmjjkk" target="_blank" rel="noopener">项目源码</a><a href="https://valorantesports.com/en-US/season/115571062868511862/handbook" target="_blank" rel="noopener">官方赛区</a></nav></div></footer><button id="back-to-top" class="back-to-top" aria-label="回到顶部">↑</button></body></html>'''
hub=hub.replace('src="catalog.js"','src="'+versioned('catalog.js')+'"').replace('src="atlas.js"','src="'+versioned('atlas.js')+'"')
(OUT/'index.html').write_text(hub,encoding='utf8')

from atlas_profile import render
framing=json.loads((DATA/'vctcn-framing.json').read_text(encoding='utf8'))
agent_portraits=json.loads((DATA/'vctcn-agent-portraits.json').read_text(encoding='utf8'))['portraits']
for p in players:
 dest=OUT/'players'/p['slug'];dest.mkdir(parents=True,exist_ok=True)
 (dest/'index.html').write_text(render(p,players,agents,teams,head,versioned,framing,agent_portraits),encoding='utf8')
print('GENERATED',count,'player pages and the directory')
