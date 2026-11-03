"""Encode reviewed frontal concepts and save their measured eye landmarks.

Optional maintenance command; Pillow and OpenCV are not build dependencies.
Source PNGs and the YuNet model live outside the published repository.
"""
from pathlib import Path
import json
import cv2
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'output/agent-frontals'
DEST=ROOT/'dist/cn/assets/agent-portraits'
DEST.mkdir(parents=True,exist_ok=True)
det=cv2.FaceDetectorYN.create(str(ROOT.parent/'output/face_detection_yunet_2023mar.onnx'),'',(320,320),.6,.3,5000)
# Masks and a robot have no human eye landmarks. These visible lens / visor
# anchors were reviewed on the native 1024 x 1536 artwork.
manual={
 'omen':([330,450,365,410],[440,620,584,620]),
 'kayo':([340,210,355,510],[433,400,590,400]),
 'cypher':([335,385,350,380],[430,475,598,475]),
}
# Pupil centers reviewed on a magnified contact sheet. Face-detector eye
# estimates are unreliable for stylized irises, glasses and covered faces.
irises={
 'breach':[434,413,596,413], 'fade':[407,561,603,562],
 'jett':[432,620,589,619], 'killjoy':[417,545,611,545],
 'neon':[422,635,605,634], 'raze':[421,474,611,471],
 'skye':[426,503,604,503], 'sova':[430,507,607,506],
 'viper':[429,524,615,522], 'yoru':[433,527,597,525],
}
portraits={}
for source in sorted(SOURCE.glob('*.png')):
    agent=source.stem
    im=Image.open(source).convert('RGBA');w,h=im.size
    assert (w,h)==(1024,1536),source
    assert im.getpixel((0,0))[3]==0,source
    im.save(DEST/(agent+'.webp'),format='WEBP',lossless=True,method=6)
    if agent in manual:
        face,eyes=manual[agent];method='reviewed-visor-anchors'
    else:
        pixels=cv2.imread(str(source));det.setInputSize((w,h))
        _,faces=det.detect(pixels)
        assert faces is not None,agent
        a=max(faces,key=lambda a:a[2]*a[3])
        face=[float(n) for n in a[:4]]
        eyes=irises[agent];method='reviewed-iris-anchors'
    portraits[agent]={
      'image':'assets/agent-portraits/'+agent+'.webp','size':[w,h],
      'face':[round(n/d,6) for n,d in zip(face,[w,h,w,h])],
      'eyes':[round(n/d,6) for n,d in zip(eyes,[w,h,w,h])],
      'landmarkMethod':method,'reference':'assets/agents/'+agent+'.webp',
      'kind':'ai-frontal-concept',
    }
assert len(portraits)==13
record={
 'created':'2026-11-03','generator':'OpenAI imagegen',
 'description':'Transparent frontal concepts based on the official agent art. Used for aligned hero reveals and paired portraits. Player photographs are real, restored at native resolution, and are not generated.',
 'portraits':portraits,
}
(ROOT/'data/vctcn-agent-portraits.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PREPARED',len(portraits),'lossless frontal concepts and eye landmarks')
