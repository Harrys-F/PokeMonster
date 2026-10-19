"""File queue for this explicitly started editor session; no external HTTP required."""
import json,time,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2HealingArtV3'
def job(name):
 n=time.time_ns();(O/'Job.json').write_text(json.dumps({'id':n,'path':'Tools/VisualV2HealingArtV3/'+name}));start=time.monotonic()
 while time.monotonic()-start<90:
  try:a=json.loads((O/'Ack.json').read_text())
  except (FileNotFoundError,json.JSONDecodeError):a={}
  if a.get('id')==n:assert a['ok'],a;return a
  time.sleep(.4)
 raise TimeoutError(name)
if __name__=='__main__':print(job(sys.argv[1]))
