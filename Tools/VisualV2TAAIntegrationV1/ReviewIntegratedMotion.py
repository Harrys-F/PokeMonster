"""Inspect saved-map TAA against preflight TAA at original-pixel scale."""
from pathlib import Path
import json,csv
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/ImageReview');O.mkdir(exist_ok=True)
for w,h,q,sp in [(1280,720,1,75),(1280,720,1,100),(2560,1440,1,75),(2560,1440,1,100),(2560,1440,2,75),(2560,1440,2,100)]:
 labels=[f'PreMotion_{w}_{h}_Q{q}_SP{sp}_B',f'IntegratedMotion_{w}_{h}_Q{q}_SP{sp}'];stages=['WalkForest','SprintForest','StopSprint','DiagonalWalk','Talk'];im=Image.new('RGB',(320*5,600),(24,24,24));draw=ImageDraw.Draw(im)
 for ri,label in enumerate(labels):
  d=json.loads((S/'Motion'/label/'Result.json').read_text());fs=list(csv.DictReader((S/'Recordings'/label/'Frames.csv').open()));t0=next(x['t'] for x in d['records'] if x['stage']=='IdleForest')
  for ci,stage in enumerate(stages):
   t=next(x['t'] for x in d['records'] if x['stage']==stage)-t0+.7;f=min(fs,key=lambda f:abs(float(f['game_seconds'])-t));source=Image.open(S/'Recordings'/label/f['file']);ww,hh=source.size;im.paste(source.crop((ww//2-160,hh//2-125,ww//2+160,hh//2+150)),(ci*320,ri*300+25));draw.text((ci*320+3,ri*300+3),f"{'Preflight B' if ri==0 else 'Saved map'} {stage}",fill='white')
 im.save(O/f'Integrated_{w}_{h}_Q{q}_SP{sp}.png')
for p in (S/'Acceptance').glob('*/DoorRecording.json'):
 d=json.loads(p.read_text());D=Path(d['recording']);fs=list(csv.DictReader((D/'Frames.csv').open()));im=Image.new('RGB',(4*480,3*295),(24,24,24));draw=ImageDraw.Draw(im)
 for i in range(12):
  f=fs[round((len(fs)-1)*i/11)];source=Image.open(D/f['file']);source.thumbnail((480,270));x=i%4*480;y=i//4*295;im.paste(source,(x,y+25));draw.text((x+3,y+3),f"Real door sequence t={float(f['game_seconds']):.3f}s",fill='white')
 im.save(O/(p.parent.name+'_Door.png'))
print('Integrated motion and door sheets complete')
