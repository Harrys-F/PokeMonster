"""Strictly sequential phases. Stop on any failed driver; never terminate a foreign editor."""
from pathlib import Path
import subprocess,sys,json,time,os
from Control import R,O,job
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');phases=[('RunMatrix.py',['PIE','2']),('close_editor',[]),('RunStudy.py',['Standalone','1']),('RunStudy.py',['Standalone','2']),('RunMatrix.py',['Standalone','1']),('RunMatrix.py',['Standalone','2']),('RunNativeReview.py',['1']),('RunNativeReview.py',['2'])]
resume=int(sys.argv[1]) if len(sys.argv)>1 else 0
assert resume in [0,3,4]
if resume==3:assert (R/'Saved/EnvironmentPerfV2/VGB1_WAQ2_Cost_Standalone_Q1_Done.txt').read_text()=='Complete'
for index,(tool,args) in enumerate(phases):
 if index<resume:continue
 (O/'RemainingDriver.json').write_text(json.dumps({'phase':index,'tool':tool,'args':args,'status':'running','utc':time.time()}));print('BEGIN',tool,args,flush=True)
 if tool=='close_editor':
  job('CloseEditor.py');start=time.monotonic()
  while 'Contents/MacOS/UnrealEditor ' in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout:time.sleep(.5);assert time.monotonic()-start<45
 else:
  p=subprocess.run([sys.executable,str(R/'Tools/VisualV2WorldArtQualityV2'/tool),*args],cwd=R,env=env)
  if p.returncode!=0:
   (O/'RemainingDriver.json').write_text(json.dumps({'phase':index,'tool':tool,'args':args,'status':'FAILED','exit':p.returncode}));raise RuntimeError('Stop; preserve project and logs')
 (O/'RemainingDriver.json').write_text(json.dumps({'phase':index,'tool':tool,'args':args,'status':'complete','utc':time.time()}))
print('ALL REMAINING TIMING STUDIES COMPLETE',flush=True)
