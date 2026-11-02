"""Collect a dated, source-attributed roster snapshot; keep raw cache outside Git."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import json, re, time, sys

sys.stdout.reconfigure(encoding='utf8')
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT.parent / 'output/vctcn-cache'
DATA = ROOT / 'data'
CACHE.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)
TEAMS = [
 ('EDG','EDward Gaming','edward-gaming',1120,'#e94250','#f2f3ef'),
 ('AG','All Gamers','all-gamers',1119,'#df344c','#f4f3ec'),
 ('BLG','Bilibili Gaming','bilibili-gaming',12010,'#79cfe6','#eef6f7'),
 ('DRG','Dragon Ranger Gaming','dragon-ranger-gaming',11981,'#d8e949','#f1f3ec'),
 ('FPX','FunPlus Phoenix','funplus-phoenix',11328,'#f56045','#f4eee6'),
 ('JDG','JD Gaming','jdg-esports',13576,'#e94f6b','#f5edf0'),
 ('NOVA','Nova Esports','nova-esports',12064,'#b99ae8','#f1eef6'),
 ('TEC','Titan Esports Club','titan-esports-club',14137,'#b8dd3a','#f0f3e9'),
 ('TE','Trace Esports','trace-esports',12685,'#76aefa','#ecf1f6'),
 ('TYL','TYLOO','tyloo-gaming',731,'#e75145','#f3eee8'),
 ('WOL','Wolves Esports','wolves-esports',13790,'#f1c54a','#f4f1e7'),
 ('XLG','Xi Lai Gaming','xilai-gaming',13581,'#cbef50','#f1f4e8'),
]

def fetch(url, name, binary=False):
 p = CACHE / name
 if p.exists(): return p.read_bytes() if binary else p.read_text(encoding='utf8')
 for attempt in range(3):
  try:
   raw = urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
   p.write_bytes(raw)
   return raw if binary else raw.decode('utf8')
  except Exception:
   if attempt==2: raise
   time.sleep(1+attempt)

def collect_team(spec):
 code,name,slug,vid,color,paper=spec
 source=f'https://www.vlr.gg/team/{vid}'
 v = BeautifulSoup(fetch(source,f'team-{code}.html'),'html.parser')
 members=[]
 for box in v.select('.team-roster-item'):
  a=box.select_one('a[href^="/player/"]')
  if not a:continue
  alias=box.select_one('.team-roster-item-name-alias')
  if not alias:continue
  role=box.get_text(' ',strip=True)
  if re.search(r'coach|manager|analyst|owner|staff',role,re.I):continue
  real=box.select_one('.team-roster-item-name-real')
  status=box.select_one('.team-roster-item-name-role')
  img=box.select_one('img')
  members.append({'handle':alias.get_text(' ',strip=True),'realName':real.get_text(' ',strip=True) if real else '',
   'vlr':'https://www.vlr.gg'+a['href'],'id':a['href'].split('/')[2],
   'rosterStatus':'非活跃' if re.search('inactive',role,re.I) else '替补' if re.search(r'\bsub\b',role,re.I) else '阵容选手',
   'portraitSource':('https:'+img['src']) if img and img.get('src','').startswith('//') else None})
 official=None; roster=[]; official_error=None
 for candidate in [slug]+(['xi-lai-gaming','xlg-esports','xi-lai'] if code=='XLG' else ['tec-esports'] if code=='TEC' else []):
  try:
   url='https://valorantesports.com/en-US/teams/'+candidate
   s=BeautifulSoup(fetch(url,f'official-{candidate}.html'),'html.parser')
   for li in s.select('li'):
    h=li.select_one('h3');img=li.select_one('img')
    if not h or not img:continue
    alias=h.get_text(' ',strip=True)
    if re.search(r'coach',li.get_text(' ',strip=True),re.I):continue
    src=img.get('src','');remote=parse_qs(urlparse(src).query).get('f',[''])[0]
    if '/players/' in remote:roster.append({'handle':alias,'portrait':remote.replace('http:','https:'),'imageProxy':src.replace('resize=3840:','resize=1080:')})
   if roster:official=url;break
  except Exception as e:official_error=str(e)
 logo=v.select_one('.team-header-logo img') or v.select_one('img[alt$="team logo"]')
 return {'code':code,'name':name,'slug':code.lower(),'color':color,'paper':paper,'vlr':source,'official':official,'rosterSource':source,
  'logoSource':('https:'+logo['src']) if logo and logo['src'].startswith('//') else None,'players':members,'officialRoster':roster,'officialError':official_error}

if __name__=='__main__':
 teams=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(collect_team,t):t[0] for t in TEAMS}
  for job in as_completed(jobs):
   try:
    team=job.result();teams.append(team)
    print(team['code'],len(team['players']),'VLR players,',len(team['officialRoster']),'official portraits',flush=True)
   except Exception as e:print('ERROR',jobs[job],repr(e),flush=True);raise
 teams.sort(key=lambda t:[s[0] for s in TEAMS].index(t['code']))
 snapshot={'date':'2026-11-02','season':2026,'rosterScope':'2026 VCT CN参赛战队的VLR公开阵容快照；替补单独标注','teams':teams}
 (DATA/'vctcn-rosters.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf8')
 print('SAVED',sum(len(t['players']) for t in teams),'players')
