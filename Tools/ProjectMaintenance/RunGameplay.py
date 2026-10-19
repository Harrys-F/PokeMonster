"""Use the existing complete input route, preserving the user save by rename only."""
import json,time,hashlib,os
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/ProjectMigration'
def job(action):
 n=time.time_ns();(O/'EditorJob.json').write_text(json.dumps({'id':n,'action':action}));t=time.monotonic()
 while time.monotonic()-t<90:
  try:a=json.loads((O/'EditorAck.json').read_text())
  except (FileNotFoundError,json.JSONDecodeError):a={}
  if a.get('id')==n:assert a['ok'],a;return a
  time.sleep(.25)
 raise TimeoutError(action)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
 label='RelocatedRoot';dest=O/'Acceptance'/label;dest.mkdir(parents=True,exist_ok=False)
 slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';held=O/'PokeMonster_Dev.migration-held.sav';assert not held.exists()
 original={'existed':slot.exists(),'method':'Original temporarily renamed, no additional backup copy.'}
 if slot.exists():original['sha256']=sha(slot);os.rename(slot,held)
 (dest/'UserSave.json').write_text(json.dumps(original,indent=2));(dest/'SaveBefore.json').write_text(json.dumps({'existed':False}))
 (O/'AcceptanceRequest.json').write_text(json.dumps({'label':label,'width':1280,'height':720,'mode':'PIE'}))
 passed=False;playing=False
 try:
  job('start_pie');playing=True;time.sleep(5);job('start_route');start=time.monotonic();last=None
  while not (dest/'FootTest.json').exists():
   time.sleep(2)
   if (dest/'FootProgress.json').exists():
    steps=json.loads((dest/'FootProgress.json').read_text());name=steps[-1]['name'] if steps else None
    if name!=last:print(len(steps),name,flush=True);last=name
   assert time.monotonic()-start<1100,'Route timeout; original user save remains safely held'
  result=json.loads((dest/'FootTest.json').read_text());passed=result['passed'];print('Route result',passed,result.get('error'),flush=True)
 finally:
  if playing:job('stop_pie');time.sleep(3)
  if slot.exists():
   test=dest/'TestGeneratedSave.sav';assert not test.exists();os.rename(slot,test)
  if original['existed']:
   assert sha(held)==original['sha256'] and not slot.exists();os.rename(held,slot);assert sha(slot)==original['sha256']
  (dest/'SaveRestored.json').write_text(json.dumps({'restored':slot.exists()==original['existed'],'sha256':sha(slot) if slot.exists() else None,'original':original},indent=2))
 assert passed,'Gameplay route failed; see FootTest.json, original save already restored'
 print('Full gameplay route passed; original user save restored byte-for-byte.',flush=True)
