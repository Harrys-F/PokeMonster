"""Run one no-save PIE review, assert completion, stop PIE, verify unchanged developer save."""
import sys,time,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
script,result=sys.argv[1:];target=R/result;assert not target.exists();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
job('start_pie');time.sleep(2);job('script',script);start=time.monotonic()
while not target.exists():time.sleep(1);assert time.monotonic()-start<300,'Review timeout; preserve live state for inspection'
r=json.loads(target.read_text());job('stop_pie');time.sleep(1);assert(hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None)==before,'Unexpected save mutation; stop'
if isinstance(r,dict):assert r.get('passed',False),r.get('error')
print('PIE_REVIEW_PASS',script,'save_unchanged',before,flush=True)
