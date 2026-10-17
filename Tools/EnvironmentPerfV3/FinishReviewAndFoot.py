"""Only after all measurements. Regular embedded PIE stop; no Save All or asset overwrite."""
from pathlib import Path
import subprocess,time,json
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';T=R/'Tools/EnvironmentPerfV3'
start=time.monotonic()
while 'DONE PIEMatrix6' not in (O/'PIEMatrixOrchestration.log').read_text():
 text=(O/'PIEMatrixOrchestration.log').read_text();assert 'Traceback' not in text,text[-2000:]
 time.sleep(2);assert time.monotonic()-start<1800
# The orchestrator writes DONE only after StopPIE completes.
time.sleep(3)
def run(script,args,log):
 print('START',script,*args,flush=True)
 with (O/log).open('x') as f:result=subprocess.run(['/usr/bin/python3',str(T/script),*args],cwd=R,stdout=f,stderr=subprocess.STDOUT)
 assert result.returncode==0,(script,result.returncode,log)
 print('DONE',script,flush=True)
run('ValidateMeasurements.py',[],'CompleteValidation.txt');run('MetricTables.py',[],'CompleteMetricTables.txt')
from MCPClient import rpc
from Control import call,job
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'EnvironmentPerfV3','version':'1'}})
job('PersistControl.py');job('FinalMapAudit.py');print('PERSISTED CONTROL; rejected MinLOD candidate',flush=True)
run('RunBaselineReviews.py',[],'BaselineReviewsOrchestration.log')
job('BeforeFoot.py')
call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3)
job('SetupFootViewport.py');job('AuditRuntimeMaterials.py');job('FootTest.py');print('FOOT START',flush=True);start=time.monotonic();f=O/'FootTest/FootTest.json'
while not f.exists():
 time.sleep(2);assert time.monotonic()-start<900
foot=json.loads(f.read_text());print('FOOT RESULT',foot['passed'],foot['error'],flush=True)
call('EditorToolset.EditorAppToolset','StopPIE',{});assert foot['passed'],foot['error'];job('AfterFoot.py')
run('RestoreDevSave.py',[],'RestoreDevSave.log');job('FinalMapAudit.py')
(O/'ReviewAndFootDone.txt').write_text('Complete');print('REVIEW AND FOOT COMPLETE',flush=True)
