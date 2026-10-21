"""One species' real PIE presentation review; guarded original developer save."""
from pathlib import Path
import sys,json,time,hashlib,shutil
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
name,label=sys.argv[1:];assert name.isalnum()and label.isalnum();O=R/'Saved/CreatureExpansionV3'/label;O.mkdir(exist_ok=False);(O.parent/'ReviewRequest.json').write_text(json.dumps(dict(species=name,label=label)));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,O/'DevSaveOriginal.sav');job('start_pie');time.sleep(3);job('script','Tools/CreatureExpansionV3/ReviewOne.py');start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<240,'No forced shutdown; inspect active review'
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(1);after=hashlib.sha256(slot.read_bytes()).hexdigest();assert after==r['save_after_sha256'],'Concurrent save write; stop'
if after!=before:shutil.copy2(slot,O/'AcceptanceSave.sav');shutil.copy2(O/'DevSaveOriginal.sav',slot)
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;(O/'SaveRestored.json').write_text(json.dumps(dict(restored=True,sha256=before)));assert r['passed'],r['error'];print('CREATURE_REVIEW_PASS',name,label)
