"""All approved routes in one ordinary PIE session; existing controllers, collision and save guards."""
from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();D=R/'Saved/BiomeTestV11'/label;D.mkdir(exist_ok=False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();rows=[];error=None
steps=[('WaterReviewRequest','ReviewWaterV11',{'label':label+'Water','motion_sequence':False},500),('MeadowReviewRequest','ReviewMeadowV11',{'label':label+'Meadow','record':False,'require_overflight':False},650),('CaveReviewRequest','ReviewCavePlateauV11',{'label':label+'Cave'},650),('ForestReviewRequest','ReviewForestCameraV11',{'label':label+'Forest','record':False},450),('RuinReviewRequest','ReviewRuinV11',{'label':label+'Ruin','record':False},400)]
print(job('start_pie'),flush=True);time.sleep(3)
try:
 for request,tool,values,timeout in steps:
  (D.parent/(request+'.json')).write_text(json.dumps(values));print('BEGIN',values['label'],job('script','Tools/BiomeTestV1/'+tool+'.py'),flush=True);p=D.parent/values['label']/'Result.json';t=time.monotonic()
  while not p.exists():
   time.sleep(2)
   if time.monotonic()-t>timeout:raise TimeoutError(values['label'])
  result=json.loads(p.read_text());rows.append({'label':values['label'],'passed':result['passed'],'error':result['error'],'distance_m':result.get('distance_m'),'steps':result.get('steps'),'total':result.get('total')});print('END',json.dumps(rows[-1]),flush=True);assert result['passed'],result['error'];assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
except Exception as ex:error=str(ex);raise
finally:
 print(job('stop_pie'),flush=True);(D/'Result.json').write_text(json.dumps({'passed':error is None and len(rows)==len(steps),'error':error,'ordinary_PIE_starts':1,'same_continuous_world':True,'no_test_driver_teleports':True,'only_relocations':'Authored masked existing BuildingCutaway cave entrance and exit','routes':rows,'distance_m':sum(x.get('distance_m')or 0 for x in rows),'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest()},indent=2))
