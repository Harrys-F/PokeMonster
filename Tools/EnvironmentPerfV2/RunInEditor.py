import sys,json
from pathlib import Path
from MCPClient import rpc
R=Path(__file__).resolve().parents[2]
p=(R/sys.argv[1]).resolve();assert p.is_relative_to(R/'Tools/EnvironmentPerfV2')
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'EnvironmentPerfV2','version':'1'}})
print(json.dumps(rpc('tools/call',{'name':'call_tool','arguments':{'toolset_name':'SlateInspectorToolset.SlateInspectorToolset','tool_name':'Type','arguments':{'ref':sys.argv[2] if len(sys.argv)>2 else 'tb4','text':'exec(open('+repr(str(p))+').read())','submit':True}}})))
