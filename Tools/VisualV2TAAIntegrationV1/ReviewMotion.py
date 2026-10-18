"""Contact sheets of actual successive framebuffer pixels, never synthesis/interpolation."""
from pathlib import Path
import json,csv,statistics
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_TAAIntegration_V1_2026-10-18/ImageReview');O.mkdir(exist_ok=True)
summary=[]
for result in sorted((S/'Motion').glob('*/Result.json')):
 d=json.loads(result.read_text());assert d['error'] is None;label=result.parent.name;D=S/'Recordings'/label;rows=list(csv.DictReader((D/'Frames.csv').open()));assert len(rows)==int((D/'Complete.txt').read_text());assert all((D/r['file']).exists() for r in rows)
 times=[float(r['game_seconds']) for r in rows];intervals=[b-a for a,b in zip(times,times[1:])];assert all(t>0 for t in intervals)
 summary.append({'label':label,'frames':len(rows),'duration':times[-1],'median_interval':statistics.median(intervals),'max_interval':max(intervals),'dimensions':sorted({(int(r['width']),int(r['height'])) for r in rows}),'recording':str(D)})
(S/'MotionInventory.json').write_text(json.dumps(summary,indent=2))
for w,h,q,sp in [(1280,720,1,75),(1280,720,1,100),(2560,1440,1,75),(2560,1440,1,100),(2560,1440,2,75),(2560,1440,2,100)]:
 labels=[f'PreMotion_{w}_{h}_Q{q}_SP{sp}_{n}' for n in ['A','B']]
 if not all((S/'Motion'/label/'Result.json').exists() and (S/'Recordings'/label/'Complete.txt').exists() for label in labels):continue
 for stage,t0 in [('SprintForest',.8),('WalkForest',1.2),('DiagonalWalk',.5),('StopSprint',.08),('Talk',1.5)]:
  image=Image.new('RGB',(6*320,2*300),(24,24,24));draw=ImageDraw.Draw(image)
  for row,label in enumerate(labels):
   d=json.loads((S/'Motion'/label/'Result.json').read_text());records=d['records'];first=next(x['t'] for x in records if x['stage']=='IdleForest');start=next(x['t'] for x in records if x['stage']==stage);frames=list(csv.DictReader((S/'Recordings'/label/'Frames.csv').open()));index=min(range(len(frames)),key=lambda i:abs(float(frames[i]['game_seconds'])-(start-first+t0)))
   for col,f in enumerate(frames[index:index+6]):
    im=Image.open(S/'Recordings'/label/f['file']);ww,hh=im.size
    # 1:1 original pixels around the actual camera's player focus. Talk source is near player.
    box=(ww//2-160,hh//2-125,ww//2+160,hh//2+150);image.paste(im.crop(box),(col*320,row*300+25));draw.text((col*320+4,row*300+4),f"{label[-1]} {stage} t={float(f['game_seconds']):.3f}",fill='white')
  image.save(O/f'{w}_{h}_Q{q}_SP{sp}_{stage}_Consecutive.png')
 print('REVIEW_SHEETS',w,h,q,sp)
print('ACTUAL_MOTION_CLIPS',len(summary),'FRAMES',sum(x['frames'] for x in summary))
