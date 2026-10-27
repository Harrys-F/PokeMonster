from pathlib import Path
import json,time,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1'
def job(*args):subprocess.run(['python3','-B',str(R/'Tools/ProjectMaintenance/ArtControl.py'),*args],cwd=R,check=True)
def wait(label,limit=400):
 p=D/label/'Result.json';start=time.monotonic()
 while not p.exists():
  assert time.monotonic()-start<limit,label
  time.sleep(.5)
 q=json.loads(p.read_text());assert q['passed'],q.get('error');print(label,'PASS',flush=True)
wait('MotionPerformance01');job('script','Tools/VisualV2StabilityV1/GroupPerformance.py');wait('GroupPerformance01');job('stop_pie');job('script','Tools/VisualV2StabilityV1/PreparePIE.py');job('start_pie');time.sleep(.6);(D/'ReviewRequest.json').write_text(json.dumps({'label':'Rhythm01','joint':False}));job('script','Tools/VisualV2StabilityV1/RhythmReview.py');wait('Rhythm01');print('REST_COMPLETE',flush=True)
