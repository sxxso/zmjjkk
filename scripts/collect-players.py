"""Build per-player facts and download shared, attributed presentation assets.

Requires beautifulsoup4 and Pillow for the maintenance pipeline only.
No dependencies are loaded by the published website.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import runpy, json, re, sys, hashlib

base=runpy.run_path(str(Path(__file__).with_name('collect-vctcn.py')))
fetch,ROOT,DATA,CACHE=[base[k] for k in ('fetch','ROOT','DATA','CACHE')]
sys.stdout.reconfigure(encoding='utf8')
ASSETS=ROOT/'dist/cn/assets'
for name in ['players','teams','agents','photos']:(ASSETS/name).mkdir(parents=True,exist_ok=True)
snapshot=json.loads((DATA/'vctcn-rosters.json').read_text(encoding='utf8'))
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
def source_url(s):return 'https:'+s if s.startswith('//') else 'https://www.vlr.gg'+s if s.startswith('/') else s
def collect_player(pair):
 team,p=pair;checkpoint=CACHE/f'facts-{p["id"]}.json'
 if checkpoint.exists():facts=json.loads(checkpoint.read_text(encoding='utf8'))
 else:
  url=p['vlr'].rstrip('/')+'/?timespan=all'
  soup=BeautifulSoup(fetch(url,f'player-{p["id"]}.html'),'html.parser')
  name=soup.select_one('.player-real-name')
  rows=[]
  for row in soup.select('#st-table tbody tr'):
   cells=[t.get_text(' ',strip=True) for t in row.select('td')];img=row.select_one('img')
   if len(cells)<16 or not img:continue
   use=re.search(r'\((\d+)\)\s*(\d+%)',cells[1])
   if not use:continue
   rows.append({'id':img['alt'],'maps':int(use[1]),'use':use[2],'rounds':int(cells[2] or 0),
     'rating':cells[3] or None,'acs':cells[4] or None,'kd':cells[5] or None,'kast':cells[6] or None,
     'adr':cells[7] or None,'kills':int(cells[11] or 0),'deaths':int(cells[12] or 0),
     'assists':int(cells[13] or 0),'firstKills':int(cells[14] or 0),'cells':cells})
  rows.sort(key=lambda a:a['maps'],reverse=True)
  matches=[]
  for a in soup.select('a.m-item')[:6]:
   tags=[e.get_text(' ',strip=True) for e in a.select('.m-item-team-tag')]
   names=[e.get_text(' ',strip=True) for e in a.select('.m-item-team-name')]
   event=a.select_one('.m-item-event');date=a.select_one('.m-item-date>div');result=a.select_one('.m-item-result')
   if not result or len(tags)<2:continue
   score=[x.get_text(strip=True) for x in result.select('span')]
   games=a.find_next_sibling('div');maps=[]
   if games:
    for m in games.select('a.m-item-games-item'):
     mapname=m.select_one('.map');gameagent=m.select_one('img[alt]')
     if mapname:maps.append({'map':mapname.get_text(strip=True),'agent':gameagent['alt'] if gameagent else None,'url':'https://www.vlr.gg'+m.get('href',''),'stats':m.get_text(' ',strip=True)})
   matches.append({'event':event.get_text(' ',strip=True) if event else '', 'date':date.get_text(strip=True).replace('/','-') if date else '',
      'teams':tags,'teamNames':names,'score':score,'won':'mod-win' in result.get('class',[]),'url':'https://www.vlr.gg'+a['href'],'maps':maps})
  portrait=soup.select_one('.player-header img')
  facts={'realName':name.get_text(' ',strip=True) if name else p['realName'],'agents':rows,'matches':matches,'source':url,
    'vlrPortrait':source_url(portrait['src']) if portrait else p['portraitSource']}
  checkpoint.write_text(json.dumps(facts,ensure_ascii=False,indent=2),encoding='utf8')
 match=next((a for a in team['officialRoster'] if norm(a['handle'])==norm(p['handle'])),None)
 if not match and p['handle']=='Knight':match=next((a for a in team['officialRoster'] if a['handle']=='Knightt'),None)
 namecn=re.search(r'\(([^)]+)\)',facts['realName'])
 return {**p,**facts,'slug':p['id']+'-'+re.sub('[^a-z0-9]+','-',p['handle'].lower()).strip('-'),
   'team':team['code'],'teamName':team['name'],'color':team['color'],'paper':team['paper'],
   'name':namecn[1] if namecn else facts['realName'],'official':team['official'],
   'portraitSource':match['portrait'] if match else source_url(facts['vlrPortrait']),
   'portraitProxy':match['imageProxy'] if match else source_url(facts['vlrPortrait']),
   'portraitMissing':not match and '/ph/' in facts['vlrPortrait'],
   'portraitCredit':'Riot Games / VALORANT Esports' if match else 'VLR.gg player profile',
   'maps':sum(a['maps'] for a in facts['agents']),'kills':sum(a['kills'] for a in facts['agents']),
   'deaths':sum(a['deaths'] for a in facts['agents']), 'portrait':'assets/players/'+p['id']+'.webp','photos':[]}

def save_image(remote,path,cache_name,maxsize):
 dest=ASSETS/path
 if dest.exists():return
 raw=fetch(remote,cache_name,binary=True)
 im=Image.open(BytesIO(raw));im.thumbnail(maxsize,Image.Resampling.LANCZOS)
 im.save(dest,'WEBP',quality=85,method=5)

def portrait(p):
 try:save_image(p['portraitSource'],Path('players')/(p['id']+'.webp'),'portrait-'+p['id'],(1000,1400))
 except Exception:save_image(p['portraitProxy'],Path('players')/(p['id']+'.webp'),'portrait-proxy-'+p['id'],(1000,1400))
 im=Image.open(ASSETS/'players'/(p['id']+'.webp'));p['portraitSize']=list(im.size)
 return p

def photos(p):
 # Public Flickr search constrained to Riot's verified official photo account.
 aliases={'77even':'KovaQ','Knight':'Knight','SpiritZ1':'SpiritZ1','WsLeo':'WsLeo','NoMan':'NoMan'}
 handle=aliases.get(p['handle'],p['handle'])
 try:
  url='https://www.flickr.com/search/?user_id=192820496%40N05&text='+quote(handle)+'&sort=date-taken-desc'
  s=fetch(url,'flickr-'+p['id']+'.html')
  pos=s.index('modelExport: ')+13;obj,_=json.JSONDecoder().raw_decode(s[pos:])
  entries=obj['main']['search-photos-lite-models'][0]['data']['photos']['data']['_data']
  for item in entries:
   d=item['data'];desc=d.get('description','')
   if d.get('ownerNsid')!='192820496@N05' or not re.search(r'(?<!\w)'+re.escape(handle)+r'(?!\w)',desc,re.I):continue
   sizes=d.get('sizes',{}).get('data',{});size=next((sizes[k]['data'] for k in ['l','c','z','m'] if k in sizes),None)
   if not size:continue
   remote=source_url(size['url']);pid=str(d['id']);filename='photos/'+pid+'.webp'
   save_image(remote,Path(filename),'flickr-photo-'+pid,(1280,1000))
   year=re.search(r'20(?:2[0-6])',desc)
   p['photos'].append({'file':'assets/'+filename,'source':'https://www.flickr.com/photos/valorantesports/'+pid+'/',
     'remote':remote,'title':d.get('title',''),'description':BeautifulSoup(desc,'html.parser').get_text(' ',strip=True),
     'year':int(year[0]) if year else None,'credit':'Riot Games / VALORANT Champions Tour Photos'})
   if len(p['photos'])>=3:break
 except Exception as e:p['photoNote']=str(e)
 return p

if __name__=='__main__':
 pairs=[(t,p) for t in snapshot['teams'] for p in t['players']]
 players=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  for f in as_completed([pool.submit(collect_player,pair) for pair in pairs]):
   p=f.result();players.append(p);print('FACTS',p['handle'],len(p['agents']),'agents',len(p['matches']),'matches',flush=True)
 players.sort(key=lambda p:([t['code'] for t in snapshot['teams']].index(p['team']),p['id']))
 with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(portrait,players))
 (DATA/'vctcn-players.json').write_text(json.dumps({'date':snapshot['date'],'players':players},ensure_ascii=False,indent=2),encoding='utf8')
 print('PORTRAITS ready',len(players),flush=True)
 with ThreadPoolExecutor(max_workers=3) as pool:
  for p in pool.map(photos,players):print('PHOTOS',p['handle'],len(p['photos']),flush=True)
 (DATA/'vctcn-players.json').write_text(json.dumps({'date':snapshot['date'],'players':players},ensure_ascii=False,indent=2),encoding='utf8')
 used={a['id'] for p in players for a in p['agents'][:4]}
 chars=json.loads(fetch('https://valorant-api.com/v1/agents?isPlayableCharacter=true&language=en-US','agents-en.json'))['data']
 zh=json.loads(fetch('https://valorant-api.com/v1/agents?isPlayableCharacter=true&language=zh-CN','agents-zh.json'))['data']
 localized={a['uuid']:a for a in zh};agents={}
 for a in chars:
  key=norm(a['displayName']);key='kayo' if key=='kayo' else key
  if key not in used:continue
  z=localized[a['uuid']]
  save_image(a['fullPortrait'],Path('agents')/(key+'.webp'),'agent-'+key,(1800,1800))
  agents[key]={'id':key,'name':z['displayName'],'en':a['displayName'],'role':z['role']['displayName'],'image':'assets/agents/'+key+'.webp','source':a['fullPortrait']}
 for t in snapshot['teams']:
  if t['logoSource']:save_image(t['logoSource'],Path('teams')/(t['code'].lower()+'.webp'),'team-logo-'+t['code'],(160,160))
 assert used.issubset(agents),used-set(agents)
 (DATA/'vctcn-agents.json').write_text(json.dumps(agents,ensure_ascii=False,indent=2),encoding='utf8')
 print('COMPLETE',len(players),'players,',sum(len(p['photos']) for p in players),'photos,',len(agents),'agents',flush=True)
