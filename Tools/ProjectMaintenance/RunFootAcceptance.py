"""Existing full Enhanced-Input gameplay route, with exact real save-slot restoration."""
from pathlib import Path
import json,hashlib,shutil,time
from ArtControl import job
R=Path(__file__).resolve().parents[2];S=R/'Saved/ProjectRefinement';O=S/'Acceptance/Final';O.mkdir(parents=True,exist_ok=False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';initial={'existed':slot.exists()}
if slot.exists():initial['sha256']=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,O/'DevSaveOriginal.sav')
(O/'SaveBefore.json').write_text(json.dumps(initial));(S/'AcceptanceRequest.json').write_text(json.dumps({'label':'Final','width':2560,'height':1440,'quality':2,'percentage':100,'mode':'PIE'}))
wrapper=S/'StartFoot.py';wrapper.write_text("from pathlib import Path\nimport unreal\nR=Path(unreal.Paths.project_dir()).resolve()\nsource=(R/'Tools/VisualV2QualityV2/FootTest.py').read_text().replace('Saved/VisualV2QualityV2','Saved/ProjectRefinement')\nexec(compile(source,'existing_complete_gameplay_route','exec'),globals())\n")
job('start_pie');time.sleep(3);job('script','Saved/ProjectRefinement/StartFoot.py');t=time.monotonic();last=None
while not (O/'FootTest.json').exists():
 time.sleep(3)
 if (O/'FootProgress.json').exists():
  steps=json.loads((O/'FootProgress.json').read_text());n=steps[-1]['name'] if steps else None
  if n!=last:print(len(steps),n,flush=True);last=n
 assert time.monotonic()-t<1100,'Timeout: keep process/save for inspection'
r=json.loads((O/'FootTest.json').read_text());time.sleep(2);job('stop_pie');time.sleep(2)
assert slot.exists() and hashlib.sha256(slot.read_bytes()).hexdigest()==r['save_after_sha256'],'Concurrent dev-slot write: do not overwrite'
if initial['existed']:shutil.copy2(slot,O/'DevSaveTestResult.sav');shutil.copy2(O/'DevSaveOriginal.sav',slot);assert hashlib.sha256(slot.read_bytes()).hexdigest()==initial['sha256']
else:slot.rename(O/'DevSaveTestResult.sav')
(O/'SaveRestored.json').write_text(json.dumps({'restored':True,'initial':initial}));assert r['passed'],r['error'];print('FULL_FOOT_PASS',r['distance_m'],r['max_speed_cm_s'],flush=True)
