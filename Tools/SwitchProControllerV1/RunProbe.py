"""Run once after editor startup; preserve the real developer save byte-for-byte."""
from pathlib import Path
import sys,time,json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
O=R/'Saved/ProjectRefinement'
label=sys.argv[1]if len(sys.argv)>1 else'SwitchProPIE02';assert label.isalnum();ready=json.loads((O/'Ready.json').read_text())
os_pid=ready['pid'];assert subprocess.check_output(['ps','-p',str(os_pid),'-o','comm='],text=True).strip().endswith('/Contents/MacOS/UnrealEditor')
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';held=slot.with_name('PokeMonster_Dev.switch-pro-held.sav');assert not held.exists();assert not(O/(label+'.json')).exists()
initial=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
if slot.exists():slot.rename(held)
(O/(label+'_SaveBefore.json')).write_text(json.dumps({'sha256':initial,'held':str(held)}))
(O/'SwitchProRequest.json').write_text(json.dumps({'label':label}));job('start_pie');time.sleep(3)
try:job('script','Tools/SwitchProControllerV1/Probe.py')
except Exception as error:
 job('stop_pie');time.sleep(1)
 if not slot.exists()and held.exists():
  assert hashlib.sha256(held.read_bytes()).hexdigest()==initial;held.rename(slot)
 (O/(label+'_InitFailure.json')).write_text(json.dumps({'error':str(error),'original_save_restored':not held.exists()}))
 raise
start=time.monotonic();last=None
while not(O/(label+'.json')).exists():
 time.sleep(2)
 if(O/(label+'_Progress.json')).exists():
  step=json.loads((O/(label+'_Progress.json')).read_text())['step']
  if step!=last:print(step,flush=True);last=step
 assert time.monotonic()-start<240,'Timeout: held original remains intact; inspect before proceeding'
result=json.loads((O/(label+'.json')).read_text());job('stop_pie');time.sleep(1)
if slot.exists():
 assert hashlib.sha256(slot.read_bytes()).hexdigest()==result['save_after_sha256'],'Concurrent save change; do not overwrite'
 dest=O/(label+'_TestResult.sav');assert not dest.exists();slot.rename(dest)
if held.exists():held.rename(slot)
assert(hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None)==initial
(O/(label+'_SaveRestored.json')).write_text(json.dumps({'restored':True,'sha256':initial}))
assert result['passed'],result['error'];print('SIMULATED_INPUT_PIE_PASS',len(result['checks']),flush=True)
