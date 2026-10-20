"""Run guarded runtime UI tests in the existing map, without save/package changes."""
from pathlib import Path
import json,sys,time
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/BattleSystemV3'/label;assert not O.exists();(O.parent/'ReviewRequest.json').write_text(json.dumps({'label':label,'mode':'PIE'}));job('start_pie');time.sleep(3);job('script','Tools/BattleSystemV3/Review.py');start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(2);assert time.monotonic()-start<950,'Timeout: preserve session for inspection'
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(2);assert r['passed'],r['error'];print('BATTLE_V3_PIE_PASS',len(r['rows']),flush=True)
