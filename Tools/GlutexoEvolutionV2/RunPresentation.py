"""Complete real PIE reviews. Existing user save is hash-checked, never copied/restored."""
from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();Q=R/'Saved/ProjectRefinement/EvolutionPresentationV21';Q.mkdir(exist_ok=True);O=Q/label;O.mkdir(exist_ok=False)
(Q/'Request.json').write_text(json.dumps({'label':label,'slate':True}))
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
job('start_pie');job('script','Tools/GlutexoEvolutionV2/ReviewPresentation.py');start=time.monotonic();last=None
while not(O/'Result.json').exists():
 time.sleep(1);assert time.monotonic()-start<270
 if(O/'Progress.json').exists():
  p=json.loads((O/'Progress.json').read_text());v=(p['route'],p['step'],p['phase'])
  if v!=last:print(p,flush=True);last=v
r=json.loads((O/'Result.json').read_text());job('stop_pie');assert hashlib.sha256(slot.read_bytes()).hexdigest()==before,'Save changed: preserve, do not overwrite'
assert r['passed'],r['error'];print('COMPLETE_EVOLUTION_PRESENTATION_PASS',len(r['checks']),flush=True)
