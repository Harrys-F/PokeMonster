import re,json,time
from pathlib import Path
from MCPClient import rpc
from Control import call
R=Path(__file__).resolve().parents[2]
for attempt in range(60):
 try:
  rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'NPCMotionV2','version':'1'}});call('SlateInspectorToolset.SlateInspectorToolset','Observe',{'ref':'','maxDepth':20})
  response=call('SlateInspectorToolset.SlateInspectorToolset','Snapshot',{'ref':'','maxDepth':35});text=json.loads(response['result']['content'][0]['text'])['returnValue']
  match=re.search(r'textbox .*?\[ref=(tb\d+)\]',text)
  if match:
   assert '"Python"' in text,'Expected existing Python selector';p=R/'Tools/RangerAnimationV2/InspectEditor.py';print(call('SlateInspectorToolset.SlateInspectorToolset','Type',{'ref':match.group(1),'text':'exec(open('+repr(str(p))+').read())','submit':True}));break
  match=re.search(r'button "Output-Log"[^\n]*\[ref=(b\d+)\]',text)
  if match:call('SlateInspectorToolset.SlateInspectorToolset','Click',{'ref':match.group(1)})
 except Exception as e:
  if attempt==59:raise
 time.sleep(1)
else:raise TimeoutError('No Python console found')
