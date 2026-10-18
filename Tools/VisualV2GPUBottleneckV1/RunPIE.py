import time,json,sys,csv
from pathlib import Path
from Control import R,O,init,job,call
init()
for label in sys.argv[1:]:
 plan=R/'Tools/VisualV2GPUBottleneckV1/Plans'/(label+'.tsv');lines=plan.read_text().splitlines();row=lines[1].split('\t');config=list(map(int,row[3:]));out=R/'Saved/EnvironmentPerfV2';assert not (out/(label+'_Done.txt')).exists()
 assert all(l.split('\t')[5:]==row[5:] for l in lines[1:] if l),'Never switch scalability inside PIE'
 (O/'Request.json').write_text(json.dumps({'label':label,'config':config}));job('Preset.py');time.sleep(15)
 call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':2}});time.sleep(3);job('StartProbe.py');print('START',label,config,flush=True);start=time.monotonic();previous=-1
 while not (out/(label+'_Done.txt')).exists():
  time.sleep(4)
  f=out/(label+'_Segments.csv');count=len(list(csv.DictReader(f.open()))) if f.exists() else 0
  if count!=previous:print(label,count,'/',len(lines)-1,flush=True);previous=count
  if time.monotonic()-start>1600:raise TimeoutError(label)
 assert (out/(label+'_Done.txt')).read_text()=='Complete'
 time.sleep(5);call('EditorToolset.EditorAppToolset','StopPIE',{});print('DONE',label,flush=True);time.sleep(3)
