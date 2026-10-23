"""Run the explicit fixture in ordinary existing-map PIE, then end PIE. No save writes."""
from pathlib import Path
import json,time,sys,struct
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/MoveEffectsV4'/label;assert not O.exists();(O.parent/'ReviewRequest.json').write_text(json.dumps(dict(label=label)))
job('start_pie');time.sleep(3);job('script','Tools/MoveEffectsV4/Review.py');start=time.monotonic()
while not(O/'Result.json').exists():
 time.sleep(2);assert time.monotonic()-start<750,'Timeout: preserve editor for inspection'
r=json.loads((O/'Result.json').read_text());job('stop_pie');assert r['passed'],r['error'];assert len(r['rows'])==20
sizes={p:struct.unpack('>II',Path(p).read_bytes()[16:24])for p in r['shots']};(O/'CaptureValidation.json').write_text(json.dumps(dict(native_sizes=sizes,resized=False,logical_viewport=[2560,1440]),indent=2));print('MOVE_EFFECTS_V4_PIE_PASS',len(r['rows']),'cases',len(sizes),'native UI captures')
