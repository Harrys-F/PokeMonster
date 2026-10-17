"""Matched V2/V3 measurements, no capture/build/Blender work during sampling."""
import subprocess,time,json,os
from pathlib import Path
from MCPClient import rpc
from Control import call,job
R=Path(__file__).resolve().parents[2];S=R/'Saved/RangerAnimationV3'
assert (S/'CaptureReviewed.txt').exists(),'Inspect the genuine capture before timing'
def run(name,*args):
 subprocess.run(['/usr/bin/python3',str(R/'Tools/RangerAnimationV3'/name),*args],cwd=R,check=True)
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'NPCMotionV3','version':'1'}})
job('FinalMapAudit.py')
with (S/'ThermalMonitor.log').open('w') as f:
 monitor=subprocess.Popen(['/usr/bin/python3',str(R/'Tools/RangerAnimationV3/ThermalMonitor.py')],cwd=R,stdout=f,stderr=subprocess.STDOUT)
 try:
  run('RunPIEPlans.py',*[f'PIEMatrix{i}' for i in range(1,6)]);print('PIE MATRIX COMPLETE',flush=True)
  job('CloseForBuild.py');pid=json.loads((S/'EditorProcess.json').read_text())['pid'];start=time.monotonic()
  while True:
   try:os.kill(pid,0)
   except ProcessLookupError:break
   time.sleep(1);assert time.monotonic()-start<120
  run('RunAutomation.py','AutomationFinal');print('FINAL AUTOMATION COMPLETE',flush=True)
  run('RunStandalone.py',*[f'NativeMatrix{i}' for i in range(1,6)]);print('NATIVE MATRIX COMPLETE',flush=True)
 finally:
  (S/'StopThermal.txt').write_text('Complete');monitor.wait(timeout=20)
run('Summarize.py');run('ValidateMeasurements.py');run('ReopenEditor.py');run('Bootstrap.py');job('FinalMapAudit.py')
(S/'PerformanceComplete.txt').write_text('Complete');print('PERFORMANCE QA COMPLETE',flush=True)
