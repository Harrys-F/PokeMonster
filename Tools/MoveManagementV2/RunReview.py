"""Existing real PIE master review, now with isolated slots. Never move or copy user saves."""
from pathlib import Path
import sys,time,json,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label=sys.argv[1];assert label.isalnum();O=R/'Saved/MoveManagementV2';D=O/label;assert not D.exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
originals={str(p):sha(p)for p in(R/'Saved/SaveGames').glob('*.sav')};auto=R/'Saved/SaveGames/PokeMonster_Recovery.sav';auto_existed=auto.exists()
O.mkdir(exist_ok=True);(O/'ReviewRequest.json').write_text(json.dumps({'label':label,'isolated_transport':True}));job('start_pie');time.sleep(2)
try:job('script','Tools/MoveManagementV2/Review.py')
except Exception:job('stop_pie');raise
start=time.monotonic()
while not(D/'Result.json').exists():time.sleep(1);assert time.monotonic()-start<180
result=json.loads((D/'Result.json').read_text());job('stop_pie')
assert all(Path(p).exists()and sha(Path(p))==value for p,value in originals.items())
assert auto.exists()==auto_existed
(D/'ProtectedSlots.json').write_text(json.dumps({'passed':True,'original_slots_byte_identical':len(originals),'user_saves_never_moved_copied_overwritten':True},indent=2))
assert result['passed'],result['error'];print('MOVE_MASTER_ISOLATED_PIE_PASS',len(result['checks']))
