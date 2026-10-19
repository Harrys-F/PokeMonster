"""Compose only genuine game screenshots; no generated/repainted visual evidence."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtQualityV2/Photos';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V2_2026-10-19');proof=[]
for mode in ['PIE','Standalone']:
 for q in [1,2]:
  for width,height in [(1280,720),(2560,1440)]:
   a=S/f'{mode}_Q{q}_V1_{width}_{height}';b=S/f'{mode}_Q{q}_V2_{width}_{height}';ra=json.loads((a/'Result.json').read_text());rb=json.loads((b/'Result.json').read_text());assert len(ra)==len(rb)==3
   for x,y in zip(ra,rb):
    assert x['name']==y['name'] and x['viewport']==y['viewport']==[width,height] and x['fov']==y['fov']==35 and x['percentage']==y['percentage']==100
    for key in ['player','camera','camera_rotation_rpy']:assert max(abs(u-v) for u,v in zip(x[key],y[key]))<1e-5
    for root in [a,b]:assert Image.open(next(root.glob(x['name']+'*.png'))).size==(width,height)
   proof.append({'mode':mode,'quality':q,'resolution':[width,height],'poses':3,'same_camera_tolerance_cm':1e-5,'original_images':[str(a),str(b)]})
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30)
for name in ['Heilhaus','Vorplatz','Wegsaum']:
 photos=[next((S/f'Standalone_Q1_{v}_2560_1440').glob(name+'*.png')) for v in ['V1','V2']];canvas=Image.new('RGB',(4096,1210),'#17211c');draw=ImageDraw.Draw(canvas)
 for index,(path,label) in enumerate(zip(photos,['A – bisherige Gruppierung (V1)','B – neue Gruppierung und Bodenvariation (V2)'])):
  im=Image.open(path).convert('RGB');im.thumbnail((2048,1152),Image.Resampling.LANCZOS);canvas.paste(im,(index*2048,58));draw.text((index*2048+24,12),label,font=font,fill='white')
 out=O/(name+'_V1_V2_QHD.png');assert not out.exists();canvas.save(out)
(O/'MatchedPhotoProof.json').write_text(json.dumps(proof,indent=2));print('24 matched pose pairs verified; 3 real QHD comparison sheets composed outside Git.')
