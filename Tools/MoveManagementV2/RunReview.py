"""Guarded real PIE review. Original developer save is held and restored byte-for-byte."""
from pathlib import Path
import sys,time,json,hashlib,struct
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/MoveManagementV2';D=O/label;assert not D.exists()
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';held=slot.with_name('PokeMonster_Dev.moves-v2-held.sav');assert not held.exists();before=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
if slot.exists():slot.rename(held)
(O/'ReviewRequest.json').write_text(json.dumps({'label':label,'original_save_sha256':before}));job('start_pie');time.sleep(3)
try:job('script','Tools/MoveManagementV2/Review.py')
except Exception:
 job('stop_pie');time.sleep(1)
 if not slot.exists()and held.exists():
  assert hashlib.sha256(held.read_bytes()).hexdigest()==before;held.rename(slot)
 raise
start=time.monotonic();last=None
while not(D/'Result.json').exists():
 time.sleep(2);assert time.monotonic()-start<240,'Timeout: preserve held original and inspect session'
 if(D/'Progress.json').exists():
  step=json.loads((D/'Progress.json').read_text())['step']
  if step!=last:print(step,flush=True);last=step
result=json.loads((D/'Result.json').read_text());job('stop_pie');time.sleep(1)
if slot.exists():
 assert hashlib.sha256(slot.read_bytes()).hexdigest()==result['save_after_sha256'],'Concurrent save write: do not overwrite'
 slot.rename(D/'TestResult.sav')
if held.exists():
 assert hashlib.sha256(held.read_bytes()).hexdigest()==before;held.rename(slot)
assert(hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None)==before
(D/'SaveRestored.json').write_text(json.dumps({'restored':True,'sha256':before},indent=2))
assert result['passed'],result['error']
sizes={p:struct.unpack('>II',Path(p).read_bytes()[16:24])for p in result['shots']};(D/'CaptureValidation.json').write_text(json.dumps({'native_slate_sizes':sizes,'resized':False,'logical_viewport':[2560,1440]},indent=2))
print('MOVE_MANAGEMENT_PIE_PASS',len(result['checks']),'checks',len(sizes),'actual UI captures')
