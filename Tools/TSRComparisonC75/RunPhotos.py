from pathlib import Path
import sys,time,json
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/TSRComparisonC75';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
out=D/json.loads((D/'PhotoRequest.json').read_text())['label'];assert not out.exists();job('script','Tools/TSRComparisonC75/Photos.py');start=time.monotonic()
while not(out/'Result.json').exists():
 assert time.monotonic()-start<300
 time.sleep(1)
r=json.loads((out/'Result.json').read_text());assert r['passed'],r;print('Actual viewport photos',len(r['shots']))
