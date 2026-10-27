from pathlib import Path
import json,time,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1'
def job(*args):subprocess.run(['python3','-B',str(R/'Tools/ProjectMaintenance/ArtControl.py'),*args],cwd=R,check=True)
def wait(p,limit=150):
 start=time.monotonic()
 while not p.exists():
  assert time.monotonic()-start<limit,str(p)
  time.sleep(.5)
 q=json.loads(p.read_text());assert q['passed'],q.get('error');print(str(p.parent.name),'PASS',flush=True)
wait(D/'Rhythm01/Result.json');job('stop_pie');job('script','Tools/VisualV2StabilityV1/PreparePIE.py');job('start_pie');time.sleep(.6);(D/'CycleRequest.json').write_text(json.dumps({'label':'11_continuous','mode':'movement','recording_name':'GameplayContinuous01'}));job('script','Tools/VisualV2StabilityV1/Cycle.py');wait(D/'Cycles01/11_continuous/Result.json');job('script','Tools/VisualV2StabilityV1/ViewSites.py');wait(D/'ViewSites01/Result.json');print('FINAL_VISUAL_READY',flush=True)
