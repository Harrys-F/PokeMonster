"""Send one guarded task to our existing editor session; never starts another editor."""
from pathlib import Path
import json,time,sys
R=Path(__file__).resolve().parents[2];S=R/'Saved/ProjectRefinement'
def job(action,path=None,timeout=120):
 assert (S/'Ready.json').exists(),'No authorized editor session'
 n=time.time_ns();v={'id':n,'action':action}
 if path:v['path']=path
 q=S/'Job.tmp';q.write_text(json.dumps(v));q.replace(S/'Job.json');start=time.monotonic()
 while time.monotonic()-start<timeout:
  try:a=json.loads((S/'Ack.json').read_text())
  except (FileNotFoundError,json.JSONDecodeError):a={}
  if a.get('id')==n:
   if not a['ok']:raise RuntimeError(a['error'])
   return a
  time.sleep(.2)
 raise TimeoutError(v)
if __name__=='__main__':print(job(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None))
