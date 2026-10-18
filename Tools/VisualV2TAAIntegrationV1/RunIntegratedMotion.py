import json,time,sys
from pathlib import Path
from Control import R,O,job
w,h,q,sp=map(int,sys.argv[1:5]);label=f'IntegratedMotion_{w}_{h}_Q{q}_SP{sp}';assert not (O/'Motion'/label).exists();(O/'Request.json').write_text(json.dumps({'label':label,'config':[w,h,q,sp]}));(O/'MotionRequest.json').write_text(json.dumps({'label':label,'width':w,'height':h,'quality':q,'percentage':sp,'aa':'from_saved_map'}));job('Preset.py');time.sleep(5);job('StartPIE.py');time.sleep(3);job('StartIntegratedMotion.py');start=time.monotonic()
while not (O/'Motion'/label/'Result.json').exists():time.sleep(2);assert time.monotonic()-start<180
r=json.loads((O/'Motion'/label/'Result.json').read_text());assert r['error'] is None,r['error'];assert {x['aa_cvar'] for x in r['records']}=={4},'Expected unchanged global TSR default'
while not (O/'Recordings'/label/'Complete.txt').exists():time.sleep(1);assert time.monotonic()-start<210
job('StopPIE.py');print('INTEGRATED_MOTION_COMPLETE',label,'frames',(O/'Recordings'/label/'Complete.txt').read_text(),flush=True)
