import time,json
from pathlib import Path
from MCPClient import rpc
from Control import job,call
R=Path(__file__).resolve().parents[2];O=R/'Saved/TreeShadowProxyV1';N=R/'Saved/EnvironmentPerfV2'
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'TreeShadowProxyV1','version':'1'}})
configs=[(1280,740,1,75),(1280,740,1,100),(2560,1440,1,75),(2560,1440,1,100),(2560,1440,2,75),(2560,1440,2,100)]
for i,config in enumerate(configs):
 label='TreeShadowProxyV1_C'+str(i+1);assert not (N/(label+'_Done.txt')).exists()
 (O/'BenchmarkRequest.json').write_text(json.dumps({'label':label,'config':config}));job('PresetBeforePIE.py');time.sleep(20)
 call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3);job('Benchmark.py');print('START',label,config,flush=True);start=time.monotonic()
 while not (N/(label+'_Done.txt')).exists():
  time.sleep(2)
  if time.monotonic()-start>240:raise TimeoutError(label+'; investigate editor log, do not fabricate results')
 assert (N/(label+'_Done.txt')).read_text()=='Complete'
 d=json.loads((O/(label+'_Control.json')).read_text());assert not d['error'] and len(d['events'])==6,d
 time.sleep(3);call('EditorToolset.EditorAppToolset','StopPIE',{});print('DONE',label,flush=True);time.sleep(2)
(O/'MatrixDone.txt').write_text('Complete')
