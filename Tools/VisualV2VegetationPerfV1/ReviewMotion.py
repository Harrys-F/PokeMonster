"""Chronological genuine frames at original pixel scale; no synthesized game images."""
from pathlib import Path
import json,csv,statistics
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18/ImageReview');O.mkdir(exist_ok=True);inventory=[]
for w,h,q,sp in [(1280,720,1,75),(2560,1440,2,100)]:
 labels=[f'MotionR2_{w}_{h}_Q{q}_SP{sp}_{v}' for v in ['Control','FullyRough']];stages=['WalkForest','SprintForest','StopSprint','DiagonalWalk','Talk'];im=Image.new('RGB',(1600,600),(24,24,24));draw=ImageDraw.Draw(im)
 for ri,label in enumerate(labels):
  result=json.loads((S/'Motion'/label/'Result.json').read_text());assert result['error'] is None;assert {r['aa_cvar'] for r in result['records']}=={2};assert {tuple(r['viewport']) for r in result['records']}=={(w,h)}
  probe=list(csv.DictReader((R/'Saved/EnvironmentPerfV2'/(result['request']['probe_label']+'_Frames.csv')).open()));assert probe and {int(x['actual_aa_method']) for x in probe}=={2}
  rows=list(csv.DictReader((Path(result['recording'])/'Frames.csv').open()));assert (Path(result['recording'])/'Complete.txt').exists();ts=[float(r['game_seconds']) for r in rows];assert ts==sorted(ts) and len(rows)>50
  for r in rows:assert (Path(result['recording'])/r['file']).is_file()
  t0=next(x['t'] for x in result['records'] if x['stage']=='IdleForest');inventory.append({'label':label,'frames':len(rows),'first_seconds':ts[0],'last_seconds':ts[-1],'mean_capture_fps':(len(rows)-1)/(ts[-1]-ts[0]),'median_interval_seconds':statistics.median(b-a for a,b in zip(ts,ts[1:])),'error':None,'explicit_setup_repositions':result['initial_profiling_teleports']})
  for ci,stage in enumerate(stages):
   t=next(x['t'] for x in result['records'] if x['stage']==stage)-t0+.7;f=min(rows,key=lambda f:abs(float(f['game_seconds'])-t));source=Image.open(Path(result['recording'])/f['file']);assert source.size==(w,h);im.paste(source.crop((w//2-160,h//2-125,w//2+160,h//2+150)),(ci*320,ri*300+25));draw.text((ci*320+3,ri*300+3),f"{'Control' if ri==0 else 'FullyRough'} {stage}",fill='white')
 im.save(O/f'Motion_{w}_Q{q}_SP{sp}_Player.png')
 # Six sequential captures in a fixed patch, same stage in each real run. No interpolation.
 for stage in ['WalkForest','SprintForest','StopSprint']:
  sheet=Image.new('RGB',(6*320,2*345),(24,24,24));draw=ImageDraw.Draw(sheet)
  for ri,label in enumerate(labels):
   result=json.loads((S/'Motion'/label/'Result.json').read_text());rows=list(csv.DictReader((Path(result['recording'])/'Frames.csv').open()));t0=next(x['t'] for x in result['records'] if x['stage']=='IdleForest');start=next(x['t'] for x in result['records'] if x['stage']==stage)-t0+.3;first=min(range(len(rows)),key=lambda i:abs(float(rows[i]['game_seconds'])-start))
   for ci,f in enumerate(rows[first:first+6]):
    source=Image.open(Path(result['recording'])/f['file']);patch=source.crop((int(w*.2)-160,max(160,int(h*.17))-160,int(w*.2)+160,max(160,int(h*.17))+160));sheet.paste(patch,(ci*320,ri*345+25));draw.text((ci*320+2,ri*345+3),f"{'Control' if ri==0 else 'FullyRough'} t={float(f['game_seconds']):.3f}s",fill='white')
  sheet.save(O/f'Motion_{w}_Q{q}_SP{sp}_{stage}_Leaves.png')
(S/'MotionInventory.json').write_text(json.dumps(inventory,indent=2));print('Verified',len(inventory),'sequences',sum(x['frames'] for x in inventory),'real frames')
