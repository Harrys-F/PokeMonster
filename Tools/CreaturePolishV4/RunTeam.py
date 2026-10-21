"""Keep original developer save in memory only; restore after exact test-write ownership check."""
from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/CreaturePolishV4'/label;O.mkdir(exist_ok=False);(O.parent/'TeamRequest.json').write_text(json.dumps(dict(label=label)));slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';original=slot.read_bytes();before=hashlib.sha256(original).hexdigest();job('start_pie');time.sleep(2);job('script','Tools/CreaturePolishV4/ReviewTeam.py');start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<200
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(2);assert hashlib.sha256(slot.read_bytes()).hexdigest()==r['save_after_sha256'],'Unexpected concurrent save write: do not overwrite'
if slot.read_bytes()!=original:slot.write_bytes(original)
assert hashlib.sha256(slot.read_bytes()).hexdigest()==before;(O/'SaveRestored.json').write_text(json.dumps(dict(restored=True,sha256=before,method='original bytes kept in memory, no additional backup')));assert r['passed'],r['error'];print('TEAM_PIE_PASS',r['checks'],flush=True)
