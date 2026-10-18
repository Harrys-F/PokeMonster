import json,time,sys
from pathlib import Path
from Control import R,O,job
w,h,q,sp=map(int,sys.argv[1:5]);n=sys.argv[5];assert n in ['A','B'];label=f'PreMotion_{w}_{h}_Q{q}_SP{sp}_{n}';assert not (O/'Motion'/label).exists();(O/'Request.json').write_text(json.dumps({'label':label,'config':[w,h,q,sp]}));(O/'MotionRequest.json').write_text(json.dumps({'label':label,'width':w,'height':h,'quality':q,'percentage':sp,'aa':4 if n=='A' else 2}));job('Preset.py');time.sleep(5);job('StartPIE.py');time.sleep(3);job('StartMotion.py');start=time.monotonic()
while not (O/'Motion'/label/'Result.json').exists():
 time.sleep(2);assert time.monotonic()-start<160,'Motion timeout, preserve editor'
r=json.loads((O/'Motion'/label/'Result.json').read_text());assert r['error'] is None,r['error']
while not (O/'Recordings'/label/'Complete.txt').exists():time.sleep(1);assert time.monotonic()-start<190
job('StopPIE.py');print('MOTION_COMPLETE',label,'frames', (O/'Recordings'/label/'Complete.txt').read_text(),flush=True)
