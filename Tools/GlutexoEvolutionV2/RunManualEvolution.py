"""Drive a normal editor Play/Stop review. Never copies, restores, deletes or writes a SaveGame."""
from pathlib import Path
import sys,time,json,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();D=R/'Saved/GlutexoEvolutionV2'/label;D.mkdir(exist_ok=False)
(D.parent/'ManualReviewRequest.json').write_text(json.dumps({'label':label}))
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()
job('start_pie');job('script','Tools/GlutexoEvolutionV2/ReviewManualEvolution.py');start=time.monotonic();last=None
while not(D/'Result.json').exists():
 time.sleep(2);assert time.monotonic()-start<300
 if (D/'Progress.json').exists():
  p=json.loads((D/'Progress.json').read_text())
  if p['last']!=last:print(p,flush=True);last=p['last']
r=json.loads((D/'Result.json').read_text());job('stop_pie');time.sleep(2)
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before,'Save changed: stop without overwrite'
assert r['passed'],r['error']
# Separate ordinary PIE restart; verify no memory save or selected fixture leaks to the next GameInstance.
job('start_pie');job('script','Tools/GlutexoEvolutionV2/ReviewManualRestart.py');job('stop_pie');time.sleep(1)
restarted=json.loads((D/'Restart.json').read_text());expected=[{k:x[k]for k in ['id','species','level','xp']}for x in r['original_party']];assert restarted==expected
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
(D/'SaveUnchanged.json').write_text(json.dumps({'sha256':before,'no_restore_or_copy_performed':True,'restart_original_party':True},indent=2))
print('MANUAL_EVOLUTION_PIE_PASS',len(r['checks']),len(r['screenshots']),flush=True)
