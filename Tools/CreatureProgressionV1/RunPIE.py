"""Normal PIE start plus explicit progression fixture; no map or developer save writes."""
import json,sys,time,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/CreatureProgressionV1'/label;assert not O.exists();(O.parent/'ReviewRequest.json').write_text(json.dumps({'label':label}))
job('start_pie');time.sleep(3);job('script','Tools/CreatureProgressionV1/Review.py');start=time.monotonic()
while not(O/'Result.json').exists():
 time.sleep(2);assert time.monotonic()-start<550,'Timeout: preserve session for inspection'
r=json.loads((O/'Result.json').read_text());job('stop_pie');assert r['passed'],r['error']
shots=[Path(p)for p in r['shots']];assert shots and all(p.is_file()for p in shots)
sizes={str(p):struct.unpack('>II',p.read_bytes()[16:24])for p in shots};assert all(w>=1280 and h>=720 for w,h in sizes.values());(O/'CaptureValidation.json').write_text(json.dumps({'native_slate_sizes':sizes,'resized':False,'logical_game_viewport':[2560,1440]},indent=2))
print('PROGRESSION_PIE_PASS',len(r['rows']),'cases',len(shots),'native UI screenshots (actual dimensions in CaptureValidation.json)')
