"""Serial visual validation, performance matrix, native automation. Never saves/discards foreign packages."""
import json,time,subprocess,sys
from pathlib import Path
from MCPClient import rpc
from Control import call,job
R=Path(__file__).resolve().parents[2];O=R/'Saved/RangerAnimationV2';D=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data'
def run(name,*args):
 p=subprocess.run(['/usr/bin/python3',str(R/'Tools/RangerAnimationV2'/name),*args],cwd=R);assert p.returncode==0,(name,p.returncode)
start=time.monotonic()
while 'FINAL VISUALS COMPLETE' not in (O/'FinalVisualsControlled.log').read_text():
 text=(O/'FinalVisualsControlled.log').read_text();assert 'Traceback' not in text,text[-3000:];time.sleep(2);assert time.monotonic()-start<400
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'NPCMotionV2','version':'1'}})
call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3);job('MotionValidation.py');print('NO-SCREENSHOT MOTION VALIDATION START',flush=True);start=time.monotonic()
while not (D/'MotionValidation.json').exists():time.sleep(2);assert time.monotonic()-start<200
assert json.loads((D/'MotionValidation.json').read_text())['passed_technical_sequence'];call('EditorToolset.EditorAppToolset','StopPIE',{});job('FinalMapAudit.py');print('MAP AUDIT COMPLETE',flush=True)
monitorlog=(O/'ThermalMonitor.log').open('a');monitor=subprocess.Popen(['/usr/bin/python3',str(R/'Tools/RangerAnimationV2/ThermalMonitor.py')],cwd=R,stdout=monitorlog,stderr=subprocess.STDOUT)
try:
 run('RunPIEPlans.py',*[f'PIEMatrix{i}' for i in range(1,7)]);print('PIE MATRIX COMPLETE',flush=True)
 job('CloseForBuild.py');pid=json.loads((O/'EditorProcess.json').read_text())['pid'];start=time.monotonic()
 while True:
  try:
   import os;os.kill(pid,0)
  except ProcessLookupError:break
  time.sleep(1);assert time.monotonic()-start<120,'Editor did not exit normally'
 run('RunAutomation.py');print('AUTOMATION COMPLETE',flush=True)
 run('RunStandalone.py',*[f'NativeMatrix{i}' for i in range(1,7)]);print('NATIVE MATRIX COMPLETE',flush=True)
finally:
 (O/'StopThermal.txt').write_text('Complete');monitor.wait(timeout=20);monitorlog.close()
(O/'QAComplete.txt').write_text('Complete');print('QA COMPLETE',flush=True)
