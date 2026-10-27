"""Use owned isolated slots and the existing guarded editor queue. Never kill processes."""
from pathlib import Path
import json,time,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
summary=[]
def wait_result(path,seconds):
 start=time.monotonic()
 while not path.exists():
  assert time.monotonic()-start<seconds,('Observe editor, no termination authorized',str(path))
  time.sleep(.5)
 result=json.loads(path.read_text());assert result['passed'],result;return result

def start(slot):
 (D/'PrepareRequest.json').write_text(json.dumps({'slot':slot,'disable_contacts':False}));before=time.time();job('script','Tools/VisualV2PerformanceV1/PrepareGameplay.py');job('start_pie');start=time.monotonic()
 while True:
  p=D/'EarlyPIE.json'
  if p.exists()and p.stat().st_mtime>before:break
  assert time.monotonic()-start<60
  time.sleep(.3)

def stop(name,result):
 begin=time.monotonic();job('stop_pie',timeout=90);summary.append({'case':name,'stop_seconds':time.monotonic()-begin,'result':result});(D/'RegressionStops.json').write_text(json.dumps(summary,indent=2));print(name,'PASS; regular PIE stop',round(summary[-1]['stop_seconds'],3),flush=True)
# Caller has ended any benchmark PIE explicitly.
start('PokeMonster_SaveV2_Test_PerfGameplay02');(D/'ReviewRequest.json').write_text(json.dumps({'label':'Gameplay01'}));job('script','Tools/VisualV2PerformanceV1/Gameplay.py');stop('Gameplay',wait_result(D/'Gameplay01/Result.json',350))
start('PokeMonster_SaveV2_Test_PerfRhythm01');(D/'ReviewRequest.json').write_text(json.dumps({'label':'Rhythm01','joint':False}));job('script','Tools/VisualV2PerformanceV1/RhythmReview.py');stop('Rhythm',wait_result(D/'Rhythm01/Result.json',250))
(D/'Cycles01').mkdir(exist_ok=False)
for i,mode in enumerate(['normal','pokemon','movement','phase','save','battle','interior']):
 label='%02d'%i+mode;start('PokeMonster_SaveV2_Test_PerfCycle'+str(i));(D/'CycleRequest.json').write_text(json.dumps({'label':label,'mode':mode}));job('script','Tools/VisualV2PerformanceV1/Cycle.py');stop(mode,wait_result(D/'Cycles01'/label/'Result.json',150))
start('PokeMonster_SaveV2_Test_PerfTravel01');job('script','Tools/VisualV2PerformanceV1/Travel.py');stop('Travel',wait_result(D/'Travel01/Result.json',200));print('All regression sessions finished',flush=True)
