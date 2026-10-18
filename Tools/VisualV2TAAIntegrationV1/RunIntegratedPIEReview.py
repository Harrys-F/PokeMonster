"""Fresh editor: verify saved map, replace invalid photos, move, then full gameplay."""
from pathlib import Path
import json,time,subprocess,os,sys
from Control import R,O,job
pid=int(sys.argv[1]);start=time.monotonic()
while True:
 try:d=json.loads((O/'Ready.json').read_text())
 except Exception:d={}
 if d.get('pid')==pid:break
 assert time.monotonic()-start<240,'Fresh editor did not become ready';time.sleep(2)
job('VerifyMap.py')
def run(script,*args):subprocess.run(['python3',str(R/'Tools/VisualV2TAAIntegrationV1'/script),*map(str,args)],check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
run('RunPhase.py','PIE','PhotoC1')
for c in [(1280,720,1,75),(1280,720,1,100),(2560,1440,1,75),(2560,1440,1,100)]:run('RunIntegratedMotion.py',*c)
run('RunAcceptance.py','PIE','Integrated_PIE_QHD_Medium100',2560,1440,100)
for c in [(2560,1440,2,75),(2560,1440,2,100)]:run('RunIntegratedMotion.py',*c)
job('CloseEditor.py');print('FINAL_PIE_REVIEW_COMPLETE',flush=True)
