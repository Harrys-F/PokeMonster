import sys,json
from pathlib import Path
from MCPClient import rpc
r=Path('/Users/harry/Developer/PokeMonster');p=(r/sys.argv[1]).resolve();assert p.is_relative_to(r/'Tools/PerformanceRangerV2')
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'RangerV2','version':'1'}})
print(json.dumps(rpc('tools/call',{'name':'call_tool','arguments':{'toolset_name':'SlateInspectorToolset.SlateInspectorToolset','tool_name':'Type','arguments':{'ref':'tb3','text':"exec(open("+repr(str(p))+").read())",'submit':True}}})))
