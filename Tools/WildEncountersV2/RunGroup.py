from pathlib import Path
import sys,json,time,hashlib,shutil
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/WildEncountersV2'/label;O.mkdir(parents=True,exist_ok=False);(O.parent/'Request.json').write_text(json.dumps({'label':label}));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,O/'DevSaveOriginal.sav');job('start_pie');time.sleep(3);job('script','Tools/WildEncountersV2/ReviewGroup.py');start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<180
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(1);after=hashlib.sha256(slot.read_bytes()).hexdigest();assert after==r['save_after_sha256'],'Concurrent save write; stop'
if after!=before:shutil.copy2(slot,O/'AcceptanceSave.sav');shutil.copy2(O/'DevSaveOriginal.sav',slot)
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;(O/'SaveRestored.json').write_text(json.dumps({'restored':True,'sha256':before}));assert r['passed'],r['error'];print('GROUP_PIE_PASS',r['ids'],r['distances'],flush=True)
