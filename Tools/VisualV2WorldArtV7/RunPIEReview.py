"""Actual matched camera captures, no performance instrumentation."""
import json,time,sys
from Control import O,job
q=int(sys.argv[1]);phase=sys.argv[2];assert q in [1,2] and phase in ['Before','ArtOnly','After','ShadowTest','Restored','BeforeFinal','ShadowHalf','ShadowZero']
(O/'Request.json').write_text(json.dumps({'label':phase+'_Q'+str(q),'config':[1280,720,q,100]}));job('Preset.py');time.sleep(5);job('StartPIE.py');time.sleep(4)
for width,height in [(2560,1440)]:
 label=f'PIE_Q{q}_{phase}_{width}_{height}';assert not (O/'Photos'/label).exists();(O/'PhotoRequest.json').write_text(json.dumps({'label':label,'width':width,'height':height,'percentage':100,'quality':q,'mode':'PIE'}));job('Photos.py');start=time.monotonic()
 while not (O/'Photos'/label/'Result.json').exists():
  time.sleep(1);assert time.monotonic()-start<200
 print('PHOTO',label,flush=True)
job('StopPIE.py');time.sleep(3)
