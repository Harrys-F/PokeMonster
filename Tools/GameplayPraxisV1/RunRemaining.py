"""Finish independent existing-PIE checks after the serial suite has stopped its last session."""
from pathlib import Path
import json,subprocess,sys,time
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GameplayPraxisV1';start=time.monotonic()
while True:
 p=D/'Suite.json';rows=json.loads(p.read_text())if p.exists()else[]
 if len(rows)==10:break
 assert time.monotonic()-start<1000;time.sleep(1)
results=[]
for case in [['movement','Movement01'],['npc','NPC01'],['e2e','Journey07']]:
 log=D/(case[1]+'_Runner.log');assert not log.exists();print('START',case[1],flush=True)
 with log.open('x')as f:code=subprocess.run([sys.executable,str(R/'Tools/GameplayPraxisV1/Run.py'),*case],cwd=R,stdout=f,stderr=subprocess.STDOUT).returncode
 results.append({'case':case,'runner_exit':code,'log':str(log.relative_to(R))});(D/'Remaining.json').write_text(json.dumps(results,indent=2));print('END',case[1],'EXIT',code,flush=True)
 if case[0]=='movement'and code==0:subprocess.run([sys.executable,str(R/'Tools/GameplayPraxisV1/EncodeMovement.py')],cwd=R,check=True)
assert all(r['runner_exit']==0 for r in results),results
