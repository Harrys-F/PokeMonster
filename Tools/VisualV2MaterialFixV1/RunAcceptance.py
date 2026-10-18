"""PIE gameplay acceptance with per-run lossless save-slot protection."""
import time,json,sys,hashlib,shutil
from pathlib import Path
from Control import R,O,job
label,width,height=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]);dest=O/'Acceptance'/label;dest.mkdir(parents=True,exist_ok=False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before={'existed':slot.exists()}
if slot.exists():before['sha256']=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,dest/'DevSaveOriginal.sav')
(dest/'SaveBefore.json').write_text(json.dumps(before));(O/'AcceptanceRequest.json').write_text(json.dumps({'label':label,'width':width,'height':height,'quality':1,'percentage':75,'mode':'PIE'}));(O/'Request.json').write_text(json.dumps({'label':label,'config':[width,height,1,75]}));job('Preset.py');time.sleep(10);job('StartPIE.py');time.sleep(3);job('StartAcceptance.py');start=time.monotonic();last=None
while not (dest/'FootTest.json').exists():
 time.sleep(3);f=dest/'FootProgress.json'
 if f.exists():
  steps=json.loads(f.read_text());n=steps[-1]['name'] if steps else None
  if n!=last:print(label,len(steps),n,flush=True);last=n
 if time.monotonic()-start>1100:raise TimeoutError('PIE remains open for inspection')
d=json.loads((dest/'FootTest.json').read_text());time.sleep(3);job('StopPIE.py')
if slot.exists():
 assert hashlib.sha256(slot.read_bytes()).hexdigest()==d['save_after_sha256'],'Concurrent save change'
 if before['existed']:shutil.copy2(slot,dest/'DevSaveTestResult.sav');shutil.copy2(dest/'DevSaveOriginal.sav',slot);assert hashlib.sha256(slot.read_bytes()).hexdigest()==before['sha256']
 else:slot.rename(dest/'DevSaveTestResult.sav')
(dest/'SaveRestored.json').write_text(json.dumps({'restored':slot.exists()==before['existed'],'initial':before}));assert d['passed'],d['error'];print(label,'PASS',d['distance_m'],d['max_speed_cm_s'],flush=True)
