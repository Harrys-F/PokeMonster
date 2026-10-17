from pathlib import Path
import time,json,subprocess
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';start=time.monotonic()
while 'DONE Baseline_EnvironmentPerfV3_QHD' not in (O/'BaselineReviewsOrchestration.log').read_text():
 text=(O/'BaselineReviewsOrchestration.log').read_text();assert 'Traceback' not in text,text[-2000:]
 time.sleep(2);assert time.monotonic()-start<600
from MCPClient import rpc
from Control import job,call
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'EnvironmentPerfV3','version':'1'}})
job('BeforeFoot.py');call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3)
job('SetupFootViewport.py');job('AuditRuntimeMaterials.py');job('FootTest.py');print('FOOT START',flush=True);start=time.monotonic();f=O/'FootTest/FootTest.json'
while not f.exists():
 time.sleep(2);assert time.monotonic()-start<900
foot=json.loads(f.read_text());print('FOOT RESULT',foot['passed'],foot['error'],flush=True);call('EditorToolset.EditorAppToolset','StopPIE',{});assert foot['passed'],foot['error'];job('AfterFoot.py')
result=subprocess.run(['/usr/bin/python3',str(R/'Tools/EnvironmentPerfV3/RestoreDevSave.py')],cwd=R);assert result.returncode==0
job('FinalMapAudit.py');(O/'ReviewAndFootDone.txt').write_text('Complete');print('REVIEW AND FOOT COMPLETE',flush=True)
