"""Optional local asset preparation. CI only consumes the saved assets/coordinates.

Requires Pillow + MediaPipe. Download face_landmarker.task from the official
MediaPipe Face Landmarker guide to ../output before running.
Never regenerates a player face. Only saved eye coordinates ship with the site.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, urllib.request, math, sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
local_tools=ROOT.parent/'output/face-tools'
if local_tools.exists():sys.path.insert(0,str(local_tools))
import mediapipe as mp
import numpy as np
CACHE=ROOT.parent/'output/vctcn-cache'
players=json.loads((ROOT/'data/vctcn-players.json').read_text(encoding='utf8'))['players']
framing=json.loads((ROOT/'data/vctcn-framing.json').read_text(encoding='utf8'))

def native(p):
    if p['portraitMissing']:return None
    cached=CACHE/('native-portrait-'+p['id'])
    try:
        if not cached.exists():
            req=urllib.request.Request(p['portraitSource'],headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=25) as r:cached.write_bytes(r.read())
        src=Image.open(cached).convert('RGBA')
        target=ROOT/'dist/cn'/p['portrait']
        old=Image.open(target)
        if src.width<old.width or src.height<old.height:raise ValueError('native source smaller than existing portrait')
        src.save(target,format='WEBP',lossless=True,method=6)
        return p['id']
    except Exception as e:
        print('RETAIN',p['id'],type(e).__name__,str(e)[:100],flush=True)
        return None

with ThreadPoolExecutor(max_workers=6) as pool:
    restored=sum(bool(result) for result in pool.map(native,players))
print('RESTORED',restored,'native player images losslessly',flush=True)

model=ROOT.parent/'output/face_landmarker.task'
options=mp.tasks.vision.FaceLandmarkerOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(model)),num_faces=1)
with mp.tasks.vision.FaceLandmarker.create_from_options(options) as detector:
 for p in players:
    f=framing[p['id']]
    im=Image.open(ROOT/'dist/cn'/p['portrait']).convert('RGBA');w,h=im.size
    # Transparent RGB can contain arbitrary pixels. Detect against a real matte.
    rgb=Image.new('RGB',im.size,'white');rgb.paste(im,mask=im.getchannel('A'))
    result=detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.asarray(rgb))) if not p['portraitMissing'] else None
    if result and result.face_landmarks:
        lm=result.face_landmarks[0]
        eyes=sorted([[lm[i].x,lm[i].y] for i in [468,473]])
        angle=abs(math.atan2((eyes[1][1]-eyes[0][1])*h,(eyes[1][0]-eyes[0][0])*w))
        if angle<.3:
            f.pop('landmarkConfidence',None)
            f.update(eyes=[round(n,6) for eye in eyes for n in eye],landmarkMethod='mediapipe-iris')
            continue
    if not p['portraitMissing']:raise ValueError('Review missing / tilted iris landmarks: '+p['handle'])
    # Explicit geometric estimate for the three labelled placeholder posters.
    x,y,bw,bh=f['face']
    f.update(eyes=[round(n,6) for n in [x+bw*.3,y+bh*.4,x+bw*.7,y+bh*.4]],landmarkMethod='face-box-estimate')
(ROOT/'data/vctcn-framing.json').write_text(json.dumps(framing,indent=2)+'\n',encoding='utf8')
print('MEASURED IRISES',sum(a['landmarkMethod']=='mediapipe-iris' for a in framing.values()),'of',len(framing))
