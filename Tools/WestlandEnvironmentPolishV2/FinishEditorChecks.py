"""Own-editor QA sequence only. No force quit, no overwrite of existing evidence labels."""
from pathlib import Path
import sys,json,time,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));import ArtControl
pid=json.loads((D/'Editor01/Launch.json').read_text())['pid'];assert json.loads((R/'Saved/ProjectRefinement/Ready.json').read_text())['pid']==pid

def run(name):print(name,ArtControl.job('script','Tools/WestlandEnvironmentPolishV2/'+name,240),flush=True)
def wait(path,timeout=360):
 start=time.monotonic()
 while not path.exists():
  assert time.monotonic()-start<timeout,str(path);time.sleep(.3)
 x=json.loads(path.read_text());assert x.get('passed',True),x;time.sleep(.8);return x
assert json.loads((D/'ShoreFit.json').read_text())['passed'];run('RegroundBanks.py');wait(D/'RegroundBanks.json',180)
(D/'PhotoRequest.json').write_text(json.dumps({'label':'AfterFinalBanks'}));print(ArtControl.job('start_pie'),flush=True);run('Photos.py');wait(D/'AfterFinalBanks/Result.json',180)
(D/'PerformanceRequest.json').write_text(json.dumps({'label':'PerfFinal'}));print(ArtControl.job('start_pie'),flush=True);run('Performance.py');wait(D/'PerfFinal/Result.json')
run('Audit.py');(D/'Active.json').write_text(json.dumps({'label':'PIERegressionFinal'}));print(ArtControl.job('start_pie'),flush=True);run('Regression.py');wait(D/'PIERegressionFinal/Result.json',180);print(ArtControl.job('stop_pie'),flush=True);time.sleep(1)
run('MapChecks.py');assert json.loads((R/'Saved/ProjectRefinement/Ready.json').read_text())['pid']==pid;print('Closing own clean editor',ArtControl.job('close'),flush=True)
start=time.monotonic()
while subprocess.run(['ps','-p',str(pid)],stdout=subprocess.DEVNULL).returncode==0:
 assert time.monotonic()-start<120,'Own editor still open; no force quit';time.sleep(.5)
print('Own editor exited normally',flush=True)
