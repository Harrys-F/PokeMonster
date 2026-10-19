"""Sequential final acceptance. A failure stops the sequence and leaves evidence/state for inspection."""
from pathlib import Path
import subprocess,sys,os,time,json
from Control import R,O,job
stages=[('RunPIEReview.py',['2']),('RunAcceptance.py',['PIE','ArtV2FinalFoot','1280','720','100']),('control',['ValidateArt.py']),('close',[]),('Build.py',[]),('RunQA.py',['Automation']),('RunMapCheck.py',['FinalMapCheck'])]
for index,(tool,args) in enumerate(stages):
 (O/'FinalQADriver.json').write_text(json.dumps({'stage':index,'tool':tool,'status':'running'}));print('QA BEGIN',tool,args,flush=True)
 if tool=='control':job(args[0])
 elif tool=='close':
  pid=json.loads((O/'Ready.json').read_text())['pid'];job('CloseEditor.py');start=time.monotonic()
  while True:
   try:os.kill(pid,0)
   except ProcessLookupError:break
   time.sleep(.5);assert time.monotonic()-start<45,'Wait for own editor normal exit; never force quit'
 else:
  p=subprocess.run([sys.executable,str(R/'Tools/VisualV2WorldArtQualityV2'/tool),*args],cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  assert p.returncode==0,('Stop after failed acceptance stage',tool,p.returncode)
 (O/'FinalQADriver.json').write_text(json.dumps({'stage':index,'tool':tool,'status':'complete'}))
print('FINAL BUILD/AUTOMATION/MAP/GAMEPLAY QA COMPLETE',flush=True)
