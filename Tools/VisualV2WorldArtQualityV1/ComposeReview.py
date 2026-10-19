"""Label/copy actual Unreal screenshots. No generated imagery or geometric image edits."""
from pathlib import Path
import json,shutil,hashlib,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtQualityV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_WorldArtQuality_V1_2026-10-19');D=O/'Vergleich';D.mkdir(exist_ok=True);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',28);records=[]
a=json.loads((S/'Photos/Before/Result.json').read_text());b=json.loads((S/'Photos/FinalMatched/Result.json').read_text())
for before,after in zip(a,b):
 assert before['name']==after['name'] and before['viewport']==after['viewport']==[2560,1440] and before['percentage']==after['percentage']==100 and before['fov']==after['fov']==35
 delta=max(abs(x-y) for x,y in zip(before['camera'],after['camera']));assert delta<.05,(before['name'],delta);assert max(abs(x-y) for x,y in zip(before['camera_rotation_rpy'],after['camera_rotation_rpy']))<.001
 canvas=Image.new('RGB',(2560,770),(25,28,25));draw=ImageDraw.Draw(canvas);row={'name':before['name'],'camera_delta_cm':delta,'camera':before['camera'],'fov':35,'raw_dimensions':[2560,1440],'before':{},'after':{}}
 for i,(phase,source) in enumerate([('Vorher','Before'),('Nachher','FinalMatched')]):
  p=S/'Photos'/source/(before['name']+'00000.png');dest=D/(before['name']+'_'+phase+'.png');assert Image.open(p).size==(2560,1440);shutil.copy2(p,dest);sha=hashlib.sha256(p.read_bytes()).hexdigest();assert hashlib.sha256(dest.read_bytes()).hexdigest()==sha;canvas.paste(Image.open(p).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS),(i*1280,50));draw.text((i*1280+22,10),phase+' – '+before['name'],font=font,fill=(237,231,211));row['before' if i==0 else 'after']={'file':str(dest),'sha256':sha}
 file=D/(before['name']+'_Vergleich.png');canvas.save(file);row['comparison']=str(file);records.append(row)
(O/'MatchedPhotoProof.json').write_text(json.dumps(records,indent=2));print('Three matched real-camera pairs copied and verified')
