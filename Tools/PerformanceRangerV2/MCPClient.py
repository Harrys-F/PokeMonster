import json,urllib.request,sys
URL='http://127.0.0.1:8000/mcp'
SESSION=None
def rpc(method,params):
 global SESSION
 req=urllib.request.Request(URL,data=json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode(),headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream'})
 if SESSION:req.add_header('Mcp-Session-Id',SESSION)
 with urllib.request.urlopen(req,timeout=50) as r:
  SESSION=r.headers.get('Mcp-Session-Id') or SESSION
  s=r.read().decode();return json.loads(s) if s.lstrip().startswith('{') else [json.loads(l[6:]) for l in s.splitlines() if l.startswith('data: ')][-1]
if __name__=='__main__':
 rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'PokeMonsterNPCIntegration','version':'1'}})
 print(json.dumps(rpc('tools/call',{'name':sys.argv[1],'arguments':json.loads(sys.argv[2]) if len(sys.argv)>2 else {}}),ensure_ascii=False))
