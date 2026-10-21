"""Use the existing transient showroom; explicit new presentation previews, no species/save/map writes."""
from pathlib import Path
import json,subprocess,sys,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();name=sys.argv[2]if len(sys.argv)>2 else'Glurak';assert name in ['Glurak','Nebulak'];hover='--hover'in sys.argv;seconds=40 if hover else 10.;yaw=float(next((x.split('=',1)[1]for x in sys.argv if x.startswith('--yaw=')),135));q=dict(label=label,seconds=seconds,yaw=yaw,focus=name,profiles={n:'/Game/Characters/Creatures/'+n+'/MotionV5/DA_'+n+'_Presentation'for n in ['Glurak','Nebulak']},mode='hover'if hover else'idle',stamps=[4,7,9]+([12,14,16,18,20,22,24,26,28,30,32,34,36,38]if hover else[]))
if '--record'in sys.argv:q['native_record']=str(R/'Saved/VisualV2TAAIntegrationV1/Recordings'/label)
if '--route-probe'in sys.argv:q['route_probe']=True
if '--ceiling'in sys.argv:q.update(ceiling=True,seconds=18,stamps=[4,10,16])
if '--original'in sys.argv:
 q['profiles']={x['species']:x['previous']for x in json.loads((R/'Saved/MotionRefinementV5/Import.json').read_text())['models']}
if hover:q['ground_hover']=['Glurak']
O=R/'Saved/CreaturePolishV4';assert not(O/label).exists();(O/'ShowcaseRequest.json').write_text(json.dumps(q));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();job('start_pie');time.sleep(2)
try:
 job('script','Tools/CreaturePolishV4/Showcase.py');t=time.monotonic()
 while not(O/label/'Result.json').exists():time.sleep(1);assert time.monotonic()-t<240
 d=json.loads((O/label/'Result.json').read_text());assert d['passed'],d['error'];assert d['save_unchanged'];
 if hover:
  samples=[v for x in d['hover_samples']for v in x['visuals']];states={x['state']for x in samples};
  if '--ceiling'in sys.argv:assert states=={'Grounded'}and not any(x['clearance']for x in samples)
  else:
   assert {'Grounded','Takeoff','Hover','Landing'}<=states,states;assert 50<=max(x['height_cm']for x in samples)<=150;assert samples[-1]['state']=='Grounded',samples[-1]
 if q.get('native_record'):
  start=time.monotonic()
  while not(Path(q['native_record'])/'Complete.txt').exists():time.sleep(.2);assert time.monotonic()-start<45
 if q.get('route_probe'):assert d['route_probe']['ground_after_landing']
 print('TARGET_REVIEW_PASS',label,flush=True)
finally:job('stop_pie')
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
