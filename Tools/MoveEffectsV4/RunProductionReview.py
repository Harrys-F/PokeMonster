"""Starts/stops normal PIE; verifies all 49 production moves and ten WorldBattle species paths."""
from pathlib import Path
import json,time,sys,struct
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/MoveEffectsV4'/label;assert not O.exists();(O.parent/'ProductionReviewRequest.json').write_text(json.dumps(dict(label=label)))
job('start_pie');time.sleep(3);job('script','Tools/MoveEffectsV4/ProductionReview.py');start=time.monotonic()
while not(O/'Result.json').exists():
 time.sleep(2);assert time.monotonic()-start<1650,'Preserve editor for inspection on timeout'
r=json.loads((O/'Result.json').read_text());job('stop_pie');assert r['passed'],r['error'];assert len(r['rows'])==59 and all(x['returned']for x in r['rows'])
sizes={p:struct.unpack('>II',Path(p).read_bytes()[16:24])for p in r['shots']};(O/'CaptureValidation.json').write_text(json.dumps(dict(native_sizes=sizes,resized=False,logical_viewport=[2560,1440]),indent=2));print('CRYSTAL_PRODUCTION_PIE_PASS',len(r['rows']),'cases',len(sizes),'native captures')
