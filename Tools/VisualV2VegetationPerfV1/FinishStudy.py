"""Guarded sequential completion after the active PIE matrix; stop at every failure."""
from pathlib import Path
import time,subprocess,os,json
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(name,*args):
 p=S/('Pipeline_'+name+'.log');assert not p.exists();print('START',name,flush=True)
 with p.open('w') as f:r=subprocess.run(['python3',str(R/'Tools/VisualV2VegetationPerfV1'/args[0]),*args[1:]],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=env)
 (S/'PipelineState.json').write_text(json.dumps({'last_step':name,'exit':r.returncode,'log':str(p)},indent=2))
 if r.returncode:print(p.read_text()[-4000:],flush=True);raise SystemExit(r.returncode)
 print('COMPLETE',name,flush=True)
start=time.monotonic();last=S/'Runner_PIE_C8.log'
while not (last.exists() and 'PHASE_COMPLETE VGB1_Vegetation_PIE_C8' in last.read_text()):
 time.sleep(5);assert time.monotonic()-start<3600,'PIE matrix not complete; preserve editor'
time.sleep(4)
run('PIE_Recheck1','RunPhase.py','PIE','Recheck1')
for config in [(1280,720,1,75),(2560,1440,2,100)]:
 for variant in ['Control','FullyRough']:run('Motion_'+str(config[0])+'_'+variant,'RunMotion.py',*map(str,config),variant)
# Debug views are qualitative, not timing evidence. Existing cheat-manager only.
from Control import job
(S/'Request.json').write_text(json.dumps({'label':'DebugViews','config':[2560,1440,2,100]}));job('Preset.py');time.sleep(5);job('StartPIE.py');time.sleep(3);job('DebugViews.py');start=time.monotonic()
while not (S/'DebugViews/Result.json').exists():time.sleep(2);assert time.monotonic()-start<120
assert 'error' not in json.loads((S/'DebugViews/Result.json').read_text());time.sleep(2);job('StopPIE.py');time.sleep(3)
run('Foot_PIE_QHD','RunAcceptance.py','PIE','Foot_PIE_QHD','2560','1440','100')
job('CloseEditor.py');time.sleep(15)
run('Automation','RunQA.py','Automation');run('MapChecks','RunMapChecks.py')
run('NativeMatrix','RunMatrix.py','Standalone')
run('Foot_Standalone_720p','RunAcceptance.py','Standalone','Foot_Standalone_720p','1280','720','75')
run('Foot_Standalone_QHD','RunAcceptance.py','Standalone','Foot_Standalone_QHD','2560','1440','100')
(S/'StopThermal.txt').write_text('Measurement complete\n');(S/'PipelineComplete.json').write_text(json.dumps({'complete':True,'time_utc':time.time()},indent=2));print('ALL_PHASES_COMPLETE',flush=True)
