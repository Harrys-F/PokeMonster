import json,re,time
from pathlib import Path
from MCPClient import rpc
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');P=R/'Art/Characters/NPCs/Ranger/Review/V2'
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'RangerV2','version':'1'}})
def call(name,args):
 r=rpc('tools/call',{'name':'call_tool','arguments':{'toolset_name':'SlateInspectorToolset.SlateInspectorToolset','tool_name':name,'arguments':args}});return json.loads(r['result']['content'][0]['text'])['returnValue']
call('Observe',{'ref':'','maxDepth':30});s=call('Snapshot',{'ref':'','maxDepth':30});(P/'ResumeSlate.json').write_text(s);match=re.search(r'button [^\n]*Output-Log[^\n]*?\[ref=(b\d+)\]',s.replace('\\n','\n'));assert match,s[-2000:];call('Click',{'ref':match.group(1)});s=call('Snapshot',{'ref':'','maxDepth':30});lines=s.replace('\\n','\n').splitlines();textboxes=[re.search(r'\[ref=(tb\d+)\]',l).group(1) for l in lines if 'textbox [focused]' in l];assert len(textboxes)==1,lines[-30:];(P/'Job.json').write_text(json.dumps({'id':0,'path':'Tools/PerformanceRangerV2/AuditLODs.py'}));print(call('Type',{'ref':textboxes[0],'text':"exec(open("+repr(str(R/'Tools/PerformanceRangerV2/PrepareEditor.py'))+").read())",'submit':True}))
