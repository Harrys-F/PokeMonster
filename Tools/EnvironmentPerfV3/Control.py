"""Local Unreal MCP orchestration. Never closes floating PIE windows."""
import json,time,sys
from pathlib import Path
from MCPClient import rpc
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3'
def job(path):
 n=time.time_ns();(O/'Job.json').write_text(json.dumps({'id':n,'path':'Tools/EnvironmentPerfV3/'+path}));start=time.monotonic()
 while time.monotonic()-start<70:
  try:a=json.loads((O/'Ack.json').read_text())
  except (FileNotFoundError,json.JSONDecodeError):a={}
  if a.get('id')==n:
   assert a['ok'],a;return a
  time.sleep(.4)
 raise TimeoutError(path)
def call(toolset,tool,args):return rpc('tools/call',{'name':'call_tool','arguments':{'toolset_name':toolset,'tool_name':tool,'arguments':args}})
if __name__=='__main__':
 if sys.argv[1]=='job':print(job(sys.argv[2]))
 elif sys.argv[1]=='plans':
  for label in sys.argv[2:]:
   (O/'Request.json').write_text(json.dumps({'plan':label}));job('StartProbe.py');print('START',label,flush=True);start=time.monotonic();d=O/(label+'_Done.txt')
   while not d.exists():
    time.sleep(2)
    if time.monotonic()-start>1800:raise TimeoutError(label)
   assert d.read_text()=='Complete',d.read_text();print('DONE',label,flush=True)
