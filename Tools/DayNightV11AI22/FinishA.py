"""Finish already-running A gameplay, then native motion, travel and read-only map checks."""
from pathlib import Path
import json,time,subprocess
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/DayNightV11AI22'
def wait(name,limit=180):
 start=time.monotonic();p=D/name/'Result.json'
 while not p.exists():
  assert time.monotonic()-start<limit,name
  time.sleep(1)
 result=json.loads(p.read_text());assert result['passed'],result.get('error');print(name,'PASS',flush=True)
def job(*args):subprocess.run(['python3','Tools/ProjectMaintenance/ArtControl.py',*args],cwd=R,check=True)
wait('GameplayA01');job('stop_pie');job('start_pie');job('script','Tools/DayNightV11AI22/ShadowMotion.py');wait('ShadowMotionA02');job('stop_pie');job('start_pie');job('script','Tools/DayNightV11AI22/Travel.py');wait('TravelA01');job('stop_pie');job('script','Tools/DayNightV11AI22/MapChecks.py');job('script','Tools/DayNightV11AI22/Restore.py');job('close')
