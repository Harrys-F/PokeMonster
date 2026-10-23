"""Run one existing-map PIE review, retaining the original developer save bytes in memory."""
from pathlib import Path
import sys,time,json,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();D=R/'Saved/GlutexoEvolutionV2'/label;D.mkdir(exist_ok=False);(D.parent/'EvolutionReviewRequest.json').write_text(json.dumps({'label':label}))
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';original=slot.read_bytes();before=hashlib.sha256(original).hexdigest()
job('start_pie');time.sleep(2);job('script',sys.argv[2] if len(sys.argv)>2 else 'Tools/GlutexoEvolutionV2/ReviewEvolution.py');start=time.monotonic()
while not(D/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<280
result=json.loads((D/'Result.json').read_text());job('stop_pie');time.sleep(1)
assert hashlib.sha256(slot.read_bytes()).hexdigest()==result['save_after_sha256'],'Concurrent save write; preserve and inspect'
slot.write_bytes(original);assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
(D/'SaveRestored.json').write_text(json.dumps({'sha256':before,'restored':True}));assert result['passed'],result['error'];print('EVOLUTION_PIE_PASS',len(result['checks']),len(result['shots']),len(result['frames']))
