"""One normal PIE session with explicitly selected isolated disk transport."""
from pathlib import Path
import sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
label,kind=sys.argv[1:];assert label.isalnum()and kind in ['learning','production'];D=R/'Saved/ProjectRefinement/LearnMovesV1';O=D/label;O.mkdir(exist_ok=False);(D/'Request.json').write_text(json.dumps(dict(label=label,kind=kind)));original=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(original.read_bytes()).hexdigest();job('script','Tools/SaveSystemV2/Prepare.py');job('start_pie');time.sleep(2)
try:job('script','Tools/LearnMovesV1/Review.py'if kind=='learning'else'Tools/LearnMovesV1/ProductionReview.py')
except Exception:job('stop_pie');raise
start=time.monotonic();last=''
while not(O/'Result.json').exists():
 assert time.monotonic()-start<1000
 time.sleep(2)
 if(O/'Progress.json').exists():
  now=(O/'Progress.json').read_text()
  if now!=last:print(now,flush=True);last=now
r=json.loads((O/'Result.json').read_text());job('stop_pie');assert hashlib.sha256(original.read_bytes()).hexdigest()==sha;assert r['passed'],r['error'];print('LEARN_MOVES_REAL_PIE_PASS',label,len(r['cases']))
