"""One real PIE review using its own named disk slot; never rename/copy/restore a user save."""
from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
D=R/'Saved/ProjectRefinement/SaveSystemV2';label=sys.argv[1];assert label.isalnum();O=D/label;O.mkdir(exist_ok=False)
mode=sys.argv[2]if len(sys.argv)>2 else'main';source=sys.argv[3]if mode=='restart'else label;slot='PokeMonster_SaveV2_Test_'+source
if mode=='main':assert not(R/'Saved/SaveGames'/(slot+'.sav')).exists()
(D/'Request.json').write_text(json.dumps({'label':label,'mode':mode,'source_label':source,'slot':slot,'case':sys.argv[3]if mode=='edge'else None},indent=2));user=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(user.read_bytes()).hexdigest()
job('script','Tools/SaveSystemV2/Prepare.py');job('start_pie');time.sleep(1.5)
try:job('script','Tools/SaveSystemV2/Edges.py'if mode=='edge'else'Tools/SaveSystemV2/Evolution.py'if mode=='evolution'else'Tools/SaveSystemV2/Review.py')
except Exception as error:
 (O/'InitializationFailure.json').write_text(json.dumps({'passed':False,'error':str(error)},indent=2));job('stop_pie');assert hashlib.sha256(user.read_bytes()).hexdigest()==before;raise
started=time.monotonic();last=''
while not(O/'Result.json').exists():
 assert time.monotonic()-started<600
 time.sleep(2)
 if(O/'Progress.json').exists():
  now=(O/'Progress.json').read_text()
  if now!=last:print(now,flush=True);last=now
result=json.loads((O/'Result.json').read_text());job('stop_pie');assert hashlib.sha256(user.read_bytes()).hexdigest()==before
assert result['passed'],result['error'];print('SAVE_V2_REAL_PIE_PASS',label,len(result['checks']),flush=True)
