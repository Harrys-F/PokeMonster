"""Guard one isolated PIE run; never modifies developer save or editor packages."""
from pathlib import Path
import json,sys,time,hashlib,shutil
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label,species,temperament,outcome=sys.argv[1:5];side=sys.argv[5]if len(sys.argv)>5 else'east';assert side in ['east','west'];assert label.isalnum();O=R/'Saved/WildEncountersV2'/label;O.mkdir(parents=True,exist_ok=False);req=dict(label=label,species=species,temperament=temperament,outcome=outcome,approach_side=side);(O.parent/'Request.json').write_text(json.dumps(req));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,O/'DevSaveOriginal.sav');job('start_pie');time.sleep(3);job('script','Tools/WildEncountersV2/ReviewEncounter.py');start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<240,'Review timeout; preserve live state for investigation'
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(1);after=hashlib.sha256(slot.read_bytes()).hexdigest();assert after==r['save_after_sha256'],'Concurrent save write; preserve state for inspection'
if after!=before:shutil.copy2(slot,O/'AcceptanceSave.sav');shutil.copy2(O/'DevSaveOriginal.sav',slot)
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;(O/'SaveRestored.json').write_text(json.dumps({'restored':True,'sha256':before}));assert r['passed'],r['error'];print('ENCOUNTER_PIE_PASS',label,r.get('escape_distance_cm'),r['outcome'],flush=True)
