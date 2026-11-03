"""Record portrait framing coordinates; does not modify source images."""
from pathlib import Path
import json,cv2
ROOT=Path(__file__).resolve().parents[1]
players=json.loads((ROOT/'data/vctcn-players.json').read_text(encoding='utf8'))['players']
detector=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
framing={}
for p in players:
 im=cv2.imread(str(ROOT/'dist/cn'/p['portrait']));h,w=im.shape[:2]
 faces=detector.detectMultiScale(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),scaleFactor=1.06,minNeighbors=5,minSize=(50,50))
 faces=[list(map(int,f)) for f in faces if f[1]<h*.45]
 box=max(faces,key=lambda f:f[2]*f[3]) if faces else [int(w*.35),int(h*.10),int(w*.30),int(h*.36)]
 framing[p['id']]={'face':[round(box[0]/w,4),round(box[1]/h,4),round(box[2]/w,4),round(box[3]/h,4)],'measured':bool(faces)}
(ROOT/'data/vctcn-framing.json').write_text(json.dumps(framing,indent=2),encoding='utf8')
print('Measured',sum(v['measured'] for v in framing.values()),'of',len(framing),'portraits')
for key in ['jett','viper','neon','killjoy','omen']:
 im=cv2.imread(str(ROOT/'dist/cn/assets/agents'/f'{key}.webp'));h,w=im.shape[:2]
 faces=detector.detectMultiScale(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),scaleFactor=1.06,minNeighbors=3,minSize=(50,50))
 print(key,faces)
