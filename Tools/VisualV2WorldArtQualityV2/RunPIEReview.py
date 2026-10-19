"""Matched V1/V2 photos at both output sizes, one scalability quality per embedded PIE session."""
import json,time,sys
from Control import R,O,job
q=int(sys.argv[1]);assert q in [1,2];(O/'Request.json').write_text(json.dumps({'label':'PhotoPIE_Q'+str(q),'config':[1280,720,q,100]}));job('Preset.py');time.sleep(5);job('StartPIE.py');time.sleep(4)
for width,height in [(1280,720),(2560,1440)]:
 for mode in ['V1','V2']:
  label=f'PIE_Q{q}_{mode}_{width}_{height}';assert not (O/'Photos'/label).exists();(O/'ReviewVariant.json').write_text(json.dumps({'mode':mode}));job('SetReviewVariant.py');(O/'PhotoRequest.json').write_text(json.dumps({'label':label,'width':width,'height':height,'percentage':100,'quality':q,'mode':'PIE'}));job('Photos.py');start=time.monotonic()
  while not (O/'Photos'/label/'Result.json').exists():
   time.sleep(1);assert time.monotonic()-start<70
  print('MATCHED PIE PHOTO',label,flush=True)
job('StopPIE.py');time.sleep(3);print('PIE REVIEW COMPLETE',q,flush=True)
