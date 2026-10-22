import time,json,sys,shutil,hashlib,subprocess
from pathlib import Path
from Control import R,O,init,job,call
subprocess.run([sys.executable,str(R/'Tools/VisualV2EnvironmentQualityV1/RunMotionReview.py')],check=True)
init();assert not (O/'FootTest/FootTest.json').exists();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';b={'existed':slot.exists()}
if slot.exists():
 b['sha256']=hashlib.sha256(slot.read_bytes()).hexdigest();backup=O/'DevSaveOriginal.sav';assert not backup.exists();shutil.copy2(slot,backup)
(O/'SaveBefore.json').write_text(json.dumps(b,indent=2));(O/'Request.json').write_text(json.dumps({'label':'VEQ1_Foot','config':[2560,1440,2,75]}));job('Preset.py');time.sleep(15);call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':2}});time.sleep(3);job('StartFoot.py');print('FOOT START',flush=True);start=time.monotonic();last=None
while not (O/'FootTest/FootTest.json').exists():
 time.sleep(3);f=O/'FootTest/FootProgress.json'
 if f.exists():
  steps=json.loads(f.read_text());n=steps[-1]['name'] if steps else None
  if n!=last:print('FOOT',len(steps),n,flush=True);last=n
 if time.monotonic()-start>1200:raise TimeoutError('Foot session retained for investigation')
result=json.loads((O/'FootTest/FootTest.json').read_text());print('FOOT RESULT',result['passed'],result['error'],flush=True);call('EditorToolset.EditorAppToolset','StopPIE',{});job('AfterFoot.py')
if slot.exists():
 actual=hashlib.sha256(slot.read_bytes()).hexdigest();assert actual==result['save_after_sha256'],'Concurrent save change: do not overwrite'
 if b['existed']:
  shutil.copy2(slot,O/'DevSaveTestResult.sav');shutil.copy2(O/'DevSaveOriginal.sav',slot);assert hashlib.sha256(slot.read_bytes()).hexdigest()==b['sha256']
 else:
  dest=O/'DevSaveTestResult.sav';assert not dest.exists();slot.rename(dest)
(O/'SaveRestored.json').write_text(json.dumps({'initial':b,'restored':(slot.exists() and hashlib.sha256(slot.read_bytes()).hexdigest()==b.get('sha256')) if b['existed'] else not slot.exists(),'test_save_preserved':str(O/'DevSaveTestResult.sav')},indent=2))
assert result['passed'],result['error']
