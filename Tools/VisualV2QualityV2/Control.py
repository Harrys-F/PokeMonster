import json,time,sys
from pathlib import Path
from MCPClient import rpc
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2QualityV2'
def init():rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'VisualV2QualityV2','version':'1'}})
def call(ts,name,args):
 r=rpc('tools/call',{'name':'call_tool','arguments':{'toolset_name':ts,'tool_name':name,'arguments':args}})
 assert 'error' not in r and not r.get('result',{}).get('isError'),r
 return r
def job(name):
 n=time.time_ns();(O/'Job.json').write_text(json.dumps({'id':n,'path':'Tools/VisualV2QualityV2/'+name}));start=time.monotonic()
 while time.monotonic()-start<90:
  try:a=json.loads((O/'Ack.json').read_text())
  except (FileNotFoundError,json.JSONDecodeError):a={}
  if a.get('id')==n:assert a['ok'],a;return a
  time.sleep(.4)
 raise TimeoutError(name)
if __name__=='__main__':init();print(job(sys.argv[1]))
