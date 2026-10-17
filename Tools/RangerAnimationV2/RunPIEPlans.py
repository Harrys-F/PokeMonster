import time,json,sys
from pathlib import Path
from MCPClient import rpc
from Control import job,call
R=Path(__file__).resolve().parents[2];O=R/'Saved/RangerAnimationV2'
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'RangerAnimationV2','version':'1'}})
for label in sys.argv[1:]:
 lines=(R/'Tools/RangerAnimationV2/Plans'/(label+'.tsv')).read_text().splitlines();row=lines[1].split('\t');config=list(map(int,row[3:]));assert not (O/(label+'_Done.txt')).exists()
 assert all(l.split('\t')[5:]==row[5:] for l in lines[1:] if l),'Never switch scalability inside PIE'
 (O/'BenchmarkRequest.json').write_text(json.dumps({'label':label,'config':config}));job('PresetBeforePIE.py');time.sleep(20)
 call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3)
 (O/'Request.json').write_text(json.dumps({'plan':label}));job('StartProbe.py');print('START',label,config,flush=True);start=time.monotonic()
 while not (O/(label+'_Done.txt')).exists():
  time.sleep(2)
  if time.monotonic()-start>1800:raise TimeoutError(label)
 assert (O/(label+'_Done.txt')).read_text()=='Complete'
 time.sleep(6);call('EditorToolset.EditorAppToolset','StopPIE',{});print('DONE',label,flush=True);time.sleep(3)
