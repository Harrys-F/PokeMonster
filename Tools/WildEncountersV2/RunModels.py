"""Run real starter acceptance, preserving the exact developer save around intentional test writes."""
from pathlib import Path
import sys,json,time,hashlib,shutil
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/StarterExpansionV1'/label;O.mkdir(exist_ok=False);(O.parent/'ModelReviewRequest.json').write_text(json.dumps({'label':label}));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
if before:shutil.copy2(slot,O/'DevSaveOriginal.sav')
job('start_pie');time.sleep(3);job('script','Tools/WildEncountersV2/ReviewModels.py');start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(2);assert time.monotonic()-start<330
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(2);assert(hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None)==r['save_after_sha256'],'Concurrent save write; stop'
if before:shutil.copy2(slot,O/'AcceptanceSave.sav');shutil.copy2(O/'DevSaveOriginal.sav',slot);assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
elif slot.exists():slot.rename(O/'AcceptanceSave.sav')
(O/'SaveRestored.json').write_text(json.dumps({'restored':True,'sha256':before}));assert r['passed'],r['error'];print('STARTER_MODEL_PIE_PASS',len(r['rows']))
