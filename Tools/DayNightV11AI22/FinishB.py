"""Independent B gate: existing live observation, short CPU comparison and twelve map checks."""
from pathlib import Path
import json,time,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/DayNightV11AI22'
def wait(name,limit=200):
 start=time.monotonic();p=D/name/'Result.json'
 while not p.exists():
  assert time.monotonic()-start<limit,name
  time.sleep(1)
 data=json.loads(p.read_text());assert data['passed'],data.get('error');print(name,'PASS',flush=True)
def job(*args):subprocess.run(['python3','Tools/ProjectMaintenance/ArtControl.py',*args],cwd=R,check=True)
wait('RhythmB02');job('stop_pie');job('start_pie');(D/'ReviewRequest.json').write_text(json.dumps({'label':'AICPU01'}));job('script','Tools/DayNightV11AI22/AIPerformance.py');wait('AICPU01');job('stop_pie');job('script','Tools/DayNightV11AI22/MapChecks.py');job('script','Tools/DayNightV11AI22/Restore.py')
