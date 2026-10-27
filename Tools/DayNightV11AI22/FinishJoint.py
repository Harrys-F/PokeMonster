"""Finish the already-running final GPU session, real travel and twelve read-only checks.
Run after GPU.py with Request.label=GPUJoint01 in a fresh authorized editor.
Every dependent step requires the previous result; no process signals or saving maps.
"""
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
wait('GPUJoint01')
if not(D/'TravelJoint04').exists():job('script','Tools/DayNightV11AI22/TravelJoint.py')
wait('TravelJoint04');job('stop_pie');job('script','Tools/DayNightV11AI22/MapChecks.py');job('script','Tools/DayNightV11AI22/Restore.py');job('close')
