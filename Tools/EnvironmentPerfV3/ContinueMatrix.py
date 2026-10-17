"""Sequential own-test orchestration. Stops on errors; never saves/discards editor packages."""
from pathlib import Path
import subprocess,time,json,re,socket
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';T=R/'Tools/EnvironmentPerfV3'
start=time.monotonic()
while 'DONE NativeMatrix6' not in (O/'StandaloneOrchestration.log').read_text():
 text=(O/'StandaloneOrchestration.log').read_text();assert 'Traceback' not in text,text[-2000:]
 time.sleep(2);assert time.monotonic()-start<2200
# Native runner prints completion only after process exit and CSV flush.
time.sleep(3)
def run(script,args,log):
 print('START',script,*args,flush=True)
 with (O/log).open('x') as f:result=subprocess.run(['/usr/bin/python3',str(T/script),*args],cwd=R,stdout=f,stderr=subprocess.STDOUT)
 assert result.returncode==0,(script,result.returncode,log)
 print('DONE',script,flush=True)
run('RunStandalone.py',['NativeCulling'],'NativeCullingOrchestration.log')
run('RunAutomation.py',[],'AutomationOrchestration.log')
run('ReopenEditor.py',[],'ReopenOrchestration.log')
for _ in range(90):
 s=socket.socket();s.settimeout(.2);ready=s.connect_ex(('127.0.0.1',8004))==0;s.close()
 if ready:break
 time.sleep(1)
assert ready
# Match the actual observed console reference; no coordinate guesses.
from MCPClient import rpc
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'EnvironmentPerfV3','version':'1'}})
def call(name,args):return rpc('tools/call',{'name':'call_tool','arguments':{'toolset_name':'SlateInspectorToolset.SlateInspectorToolset','tool_name':name,'arguments':args}})
call('Observe',{'ref':'','maxDepth':35})
for attempt in range(45):
 snap=call('Snapshot',{'ref':'','maxDepth':35});text=json.loads(snap['result']['content'][0]['text'])['returnValue'];refs=re.findall(r'textbox[^\n]*\[ref=(tb\d+)\]',text)
 if len(refs)==1:break
 time.sleep(1)
assert len(refs)==1,refs
run('RunInEditor.py',['Tools/EnvironmentPerfV3/PrepareEditor.py',refs[0]],'PrepareAfterStandalone.log')
run('RunPIEPlans.py',['PIEMatrix'+str(i) for i in range(1,7)],'PIEMatrixOrchestration.log')
(O/'AllMatricesDone.txt').write_text('Complete');print('ALL MATRICES DONE',flush=True)
