"""Serial real-PIE regressions using existing services; each case has its own RAM save guard."""
from pathlib import Path
import json,subprocess,sys,time
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GameplayPraxisV1';prior=D/(sys.argv[1]if len(sys.argv)>1 else'Journey06')/'Run.json';start=time.monotonic()
while not prior.exists():
 assert time.monotonic()-start<650,'Connected route not finished';time.sleep(1)
assert 'passed'in json.loads(prior.read_text()),'Previous runner must have completed ordinary PIE teardown; independent checks do not require that unrelated case to pass'
cases=[['progression','Progression01'],['themes','Themes01'],['evolution','Evolution01'],['wild','Aggressive01','Zunderlauf','AGGRESSIVE','Fled'],['wild','Territorial01','Zunderlauf','TERRITORIAL','Victory'],['wild','Shy01','Schiggy','SHY','Fled'],['wild','Curious01','Bisasam','CURIOUS','Fled'],['wild','Capture01','Bisasam','CALM','Captured'],['group','Group01'],['collision','Collision01']];rows=[]
for case in cases:
 log=D/(case[1]+'_Runner.log');assert not log.exists();print('START',case[1],flush=True)
 with log.open('x')as f:code=subprocess.run([sys.executable,str(R/'Tools/GameplayPraxisV1/Run.py'),*case],cwd=R,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'case':case,'runner_exit':code,'log':str(log.relative_to(R))});(D/'Suite.json').write_text(json.dumps(rows,indent=2));print('END',case[1],'EXIT',code,flush=True)
 # A failed isolated fixture is kept, but other independent checks may proceed only after ordinary PIE teardown.
 if code:
  print('CHECK_FAILED see retained log; no success claimed',case[1],flush=True)
assert all(r['runner_exit']==0 for r in rows),rows
