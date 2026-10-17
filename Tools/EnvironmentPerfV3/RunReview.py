from pathlib import Path
import json,time
from Control import job
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3'
request=json.loads((O/'ReviewRequest.json').read_text());job('ReviewShots.py');p=O/'Screenshots'/request['label']/'Review.json';start=time.monotonic()
while not p.exists():
 time.sleep(2)
 assert time.monotonic()-start<900
assert not json.loads(p.read_text())['error'];print('Review complete',request['label'])
