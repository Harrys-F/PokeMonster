"""Dependent review stages in the same project; no signals, no automatic map saves."""
from pathlib import Path
import json,time,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1'
def job(*args):subprocess.run(['python3','-B',str(R/'Tools/ProjectMaintenance/ArtControl.py'),*args],cwd=R,check=True)
def wait(label,limit=300):
 p=D/label/'Result.json';start=time.monotonic()
 while not p.exists():
  assert time.monotonic()-start<limit,label
  time.sleep(.5)
 data=json.loads(p.read_text());assert data['passed'],data.get('error');print(label,'PASS',flush=True)
wait('ReproAfter01');job('script','Tools/VisualV2StabilityV1/Capture.py');wait('CaptureAfter01');job('stop_pie');job('script','Tools/VisualV2StabilityV1/PreparePIE.py');job('start_pie');time.sleep(.6);job('script','Tools/VisualV2StabilityV1/Gameplay.py');wait('Gameplay01');job('script','Tools/VisualV2StabilityV1/Travel.py');wait('Travel01');job('stop_pie');print('AFTER_REVIEW_COMPLETE',flush=True)
