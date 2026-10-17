import sys,json
from pathlib import Path
from MCPClient import rpc
r=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');p=(r/sys.argv[1]).resolve();assert p.is_relative_to(r/'Tools/MeshyNPCIntegrationV1')
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'NPCIntegrationV1','version':'1'}})
a=rpc('tools/call',{'name':'call_tool','arguments':{'toolset_name':'SlateInspectorToolset.SlateInspectorToolset','tool_name':'Type','arguments':{'ref':'tb1','text':"exec(open("+repr(str(p))+").read())",'submit':True}}});print(json.dumps(a))
