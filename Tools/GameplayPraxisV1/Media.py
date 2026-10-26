"""Index only fresh actual Unreal images/video; never synthesize scene pixels or upload evidence."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GameplayPraxisV1';since=(D/'Baseline.json').stat().st_mtime;paths=set()
for root in ['Journey07','Collision01','NPC01','Follower01','wild','group']:
 paths.update((D/root).rglob('*.png'))
for root,patterns in [('Saved/BattleSystemV3/LiveUI',['BattleV3_Battle01_*']),('Saved/BattleViewV2/LiveUI',['BattleV2_*_Themes01']),('Saved/GlumandaV11/LiveUI',['PraxisController01*','Progression01_*','Evolution01*','Wild_Aggressive01','Wild_Territorial01','Wild_Shy01','Wild_Curious01','Wild_Capture01','PraxisRepertoire01*'])]:
 for pattern in patterns:
  for folder in (R/root).glob(pattern):
   p=folder/'ActualSlateViewport.png'
   if p.exists():paths.add(p)
rows=[]
for p in sorted(paths):
 assert p.stat().st_mtime>=since,('Historical image excluded',p)
 with Image.open(p)as im:size=list(im.size);im.verify()
 rows.append({'path':str(p.relative_to(R)),'pixels':size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fresh_this_task':True,'kind':'native Slate viewport'if p.name=='ActualSlateViewport.png'else'Unreal game camera capture'})
# Four original frames from the genuine territorial encounter sequence; only resize for an overview.
seq=D/'wild/Territorial01';files=sorted(seq.glob('*.png'));selected=[files[0],files[3],files[len(files)//2],files[-1]];canvas=Image.new('RGB',(1600,940),(22,22,22));draw=ImageDraw.Draw(canvas)
for i,p in enumerate(selected):
 image=Image.open(p).convert('RGB').resize((800,450));x=(i%2)*800;y=(i//2)*470;canvas.paste(image,(x,y+20));draw.text((x+8,y+4),p.name,fill='white')
canvas.save(D/'ContactAndEscape_Overview.jpg',quality=95)
(D/'Media.json').write_text(json.dumps({'actual_unreal_images':rows,'count':len(rows),'overview_originals':[str(p.relative_to(R))for p in selected],'overview_resized_only_no_scene_edits':True,'video':json.loads((D/'Movement01/Motion/Videos.json').read_text()),'not_committed_or_uploaded':True},indent=2));print('FRESH_NATIVE_IMAGES',len(rows))
