"""Guarded existing-map PIE review. No new map or asset save. Choose a fresh alphanumeric label."""
from pathlib import Path
import json,sys,time
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label,kind=sys.argv[1:];assert label.isalnum()and kind in['Review','Input','World'];O=R/'Saved/BattleViewV2'/label;assert not O.exists();request={'label':label,'mode':'PIE','width':2560,'height':1440};(O.parent/(kind+'Request.json')).write_text(json.dumps(request));script={'Review':'Review.py','Input':'ReviewInput.py','World':'ReviewWorld.py'}[kind];job('start_pie');time.sleep(3);job('script','Tools/BattleViewV2/'+script);start=time.monotonic()
while not(O/'Result.json').exists():time.sleep(2);assert time.monotonic()-start<600,'Timeout: preserve session for inspection'
r=json.loads((O/'Result.json').read_text());job('stop_pie');time.sleep(2);assert r['passed'],r['error'];print('PIE_REVIEW_PASS',kind,label,flush=True)
