"""Host waits on one guarded in-editor benchmark; no process termination."""
from pathlib import Path
import sys,json,time
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GraphicsVariantC';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
q=json.loads(Path(sys.argv[1]).read_text());assert q['label'].isalnum();p=D/q['label'];assert not p.exists();(D/'Request.json').write_text(json.dumps(q));job('script','Tools/GraphicsVariantC/Benchmark.py');start=time.monotonic();last=None
while not(p/'Result.json').exists():
 assert time.monotonic()-start<q.get('timeout',1800)+20
 if(p/'Progress.json').exists():
  v=(p/'Progress.json').read_text()
  if v!=last:print(json.loads(v)['name'],flush=True);last=v
 time.sleep(1)
res=json.loads((p/'Result.json').read_text());print('Completed',len(res['cases']),'cases',flush=True);assert res['passed']
