import time,json,subprocess
from pathlib import Path
from MCPClient import rpc
from Control import call,job
R=Path(__file__).resolve().parents[2];f=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data/SharpPoses.json';rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'NPCMotionV2','version':'1'}})
subprocess.run(['/usr/bin/python3',str(R/'Tools/RangerAnimationV2/Bootstrap.py')],cwd=R,check=True);call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3);job('SharpPoseReview.py');start=time.monotonic()
while not f.exists():time.sleep(1);assert time.monotonic()-start<180
r=json.loads(f.read_text());call('EditorToolset.EditorAppToolset','StopPIE',{});assert not r['error'],r['error'];job('FinalMapAudit.py');job('FinalEditorState.py');print('SHARP POSES COMPLETE',flush=True)
