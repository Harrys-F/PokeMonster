from pathlib import Path
import json,time,subprocess
from MCPClient import rpc
from Control import call,job
R=Path(__file__).resolve().parents[2];O=R/'Saved/RangerAnimationV2';A=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data'
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'NPCMotionV2','version':'1'}})
job('BeforeFoot.py');time.sleep(20)
call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3);job('CaptureMotionSequence.py');print('SEQUENCE START',flush=True)
start=time.monotonic()
while not (A/'Sequence.json').exists():time.sleep(1);assert time.monotonic()-start<180
assert not json.loads((A/'Sequence.json').read_text())['error'];call('EditorToolset.EditorAppToolset','StopPIE',{});time.sleep(2)
call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3);job('SetupFootViewport.py');job('FootTest.py');print('FOOT START',flush=True);start=time.monotonic();f=O/'FootTest/FootTest.json'
while not f.exists():time.sleep(2);assert time.monotonic()-start<1000
foot=json.loads(f.read_text());print('FOOT RESULT',foot['passed'],foot['error'],flush=True);call('EditorToolset.EditorAppToolset','StopPIE',{});job('AfterFoot.py')
if foot['passed']:
 result=subprocess.run(['/usr/bin/python3',str(R/'Tools/RangerAnimationV2/RestoreDevSave.py')],cwd=R);assert result.returncode==0
assert foot['passed'],foot['error']
