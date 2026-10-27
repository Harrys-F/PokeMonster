"""Regular start/stop only; on timeout leave process intact and retain diagnostics."""
from pathlib import Path
import json,time,subprocess,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';O=D/'Cycles01';O.mkdir(exist_ok=False);rows=[]
def job(*args):
 start=time.monotonic();subprocess.run(['python3','-B',str(R/'Tools/ProjectMaintenance/ArtControl.py'),*args],cwd=R,check=True);return time.monotonic()-start
for i,mode in enumerate(['normal','pokemon','phase','interior','save','battle','movement','record','normal','normal']):
 label=f'{i+1:02d}_{mode}';(D/'CycleRequest.json').write_text(json.dumps({'label':label,'mode':mode}));job('script','Tools/VisualV2StabilityV1/PreparePIE.py');job('start_pie');time.sleep(.5);job('script','Tools/VisualV2StabilityV1/Cycle.py');p=O/label/'Result.json';start=time.monotonic()
 while not p.exists():
  assert time.monotonic()-start<120,label
  time.sleep(.5)
 result=json.loads(p.read_text());assert result['passed'],result.get('error');elapsed=job('stop_pie');idle=job('script','Tools/VisualV2StabilityV1/Idle.py');row={'label':label,'mode':mode,'passed':True,'stop_request_seconds':elapsed,'idle_check_seconds':idle,'idle':json.loads((D/'Idle.json').read_text())}
 if mode=='record':
  capture=Path(result['capture']);wait=time.monotonic()
  while not(capture/'Complete.txt').exists():
   assert time.monotonic()-wait<30,'Recorder failed to close automatically after PIE end'
   time.sleep(.25)
  row['automatic_capture_drain_seconds']=time.monotonic()-wait;row['capture_metrics']=json.loads((capture/'Metrics.json').read_text())
 rows.append(row);(O/'Progress.json').write_text(json.dumps(rows,indent=2));print(label,'PASS',flush=True)
(O/'Result.json').write_text(json.dumps({'passed':True,'cycles':rows,'forced_termination':False},indent=2));print('TEN_CYCLES_COMPLETE',flush=True)
