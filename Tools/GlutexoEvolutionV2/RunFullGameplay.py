"""Run the existing full Enhanced Input route, then restore the exact original developer save."""
from pathlib import Path
import json,hashlib,shutil,time,sys
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1] if len(sys.argv)>1 else 'FinalV11';assert label.isalnum();S=R/'Saved/GlumandaV11';O=S/'Acceptance'/label;O.mkdir(parents=True,exist_ok=False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';initial={'existed':slot.exists()}
if slot.exists():initial['sha256']=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,O/'DevSaveOriginal.sav')
(O/'SaveBefore.json').write_text(json.dumps(initial));(S/'AcceptanceRequest.json').write_text(json.dumps({'label':label,'width':2560,'height':1440,'quality':2,'percentage':100,'mode':'PIE','battle_review_only':label.startswith('Battle')}))
job('start_pie');time.sleep(3);job('script','Tools/GlutexoEvolutionV2/StartFullGameplay.py');start=time.monotonic();last=None
while not (O/'FootTest.json').exists():
 time.sleep(3)
 if (O/'FootProgress.json').exists():
  steps=json.loads((O/'FootProgress.json').read_text());name=steps[-1]['name'] if steps else None
  if name!=last:print(len(steps),name,flush=True);last=name
 assert time.monotonic()-start<1100,'Timeout: preserve session/save for inspection'
r=json.loads((O/'FootTest.json').read_text());time.sleep(2);job('stop_pie');time.sleep(2)
assert slot.exists() and hashlib.sha256(slot.read_bytes()).hexdigest()==r['save_after_sha256'],'Concurrent save write: do not overwrite'
if initial['existed']:shutil.copy2(slot,O/'DevSaveTestResult.sav');shutil.copy2(O/'DevSaveOriginal.sav',slot);assert hashlib.sha256(slot.read_bytes()).hexdigest()==initial['sha256']
else:slot.rename(O/'DevSaveTestResult.sav')
(O/'SaveRestored.json').write_text(json.dumps({'restored':True,'initial':initial}));assert r['passed'],r['error'];print('FULL_FOOT_PASS',r['distance_m'],r['max_speed_cm_s'],flush=True)

companion=json.loads((O/'CompanionResult.json').read_text());assert not companion['issues'],companion;print('COMPANION_FULL_ROUTE_PASS',companion,flush=True)
