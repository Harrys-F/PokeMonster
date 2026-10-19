"""Only arrange actual engine screenshots; no retouching, relighting or synthetic images."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,math,shutil
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtV7';O=Path('/Users/harry/Documents/Codex/PokeMonster_WorldArt_V7_2026-10-19');D=O/'Comparisons';D.mkdir(exist_ok=True);rows=[]
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',25)
for mode in ['PIE','Standalone']:
 left=S/'Photos'/f'{mode}_Q1_BeforeFinal_2560_1440';right=S/'Photos'/(f'{mode}_Q1_'+('ArtOnly_2560_1440' if mode=='PIE' else 'After_2560_1440'))
 if not (right/'Result.json').exists():continue
 l={r['name']:r for r in json.loads((left/'Result.json').read_text())};r={r['name']:r for r in json.loads((right/'Result.json').read_text())}
 for name in l:
  for k in ['player','camera','camera_rotation_rpy']:
   assert max(abs(a-b) for a,b in zip(l[name][k],r[name][k]))<.02,(mode,name,k)
  assert l[name]['viewport']==r[name]['viewport']==[2560,1440]
  for v in [l[name],r[name]]:assert v['fov']==35 and v['percentage']==v['screen_percentage_cvar']==v['secondary_percentage_cvar']==100 and v['dynamic_resolution_mode']==0 and v['shadow_amount']==1
  a=next(left.glob(name+'*.png'));b=next(right.glob(name+'*.png'));ia=Image.open(a).convert('RGB');ib=Image.open(b).convert('RGB');assert ia.size==ib.size==(2560,1440)
  board=Image.new('RGB',(2560,766),(23,25,22));draw=ImageDraw.Draw(board);draw.text((20,12),'VORHER – V6 | '+name+' | '+mode,fill='white',font=font);draw.text((1300,12),'NACHHER – V7 | Originalschatten',fill='white',font=font)
  board.paste(ia.resize((1280,720),Image.Resampling.LANCZOS),(0,46));board.paste(ib.resize((1280,720),Image.Resampling.LANCZOS),(1280,46));dest=D/(mode+'_'+name+'_V6_V7.jpg');board.save(dest,quality=95)
  rows.append({'name':name,'mode':mode,'before':str(a),'after':str(b),'comparison':str(dest),'original_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in [a,b]]})
# Isolated shadow comparison uses the same unchanged V6 world, not the landscape-after capture.
left=S/'Photos/PIE_Q1_BeforeFinal_2560_1440';right=S/'Photos/PIE_Q1_ShadowHalf_2560_1440'
for name in ['Westwald','Heilhaus','Suedwiese','Uferabzweig','Innenraum']:
 a=Image.open(next(left.glob(name+'*.png'))).convert('RGB');b=Image.open(next(right.glob(name+'*.png'))).convert('RGB');board=Image.new('RGB',(2560,766),(23,25,22));draw=ImageDraw.Draw(board);draw.text((20,12),'ORIGINAL | '+name,fill='white',font=font);draw.text((1300,12),'DIAGNOSE Shadow Amount 0,5 – nicht übernommen',fill='white',font=font);board.paste(a.resize((1280,720),Image.Resampling.LANCZOS),(0,46));board.paste(b.resize((1280,720),Image.Resampling.LANCZOS),(1280,46));board.save(D/('ShadowProbe_'+name+'.jpg'),quality=95)
(D/'Manifest.json').write_text(json.dumps(rows,indent=2));print('Verified matching view pairs',len(rows))
