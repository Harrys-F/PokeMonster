import time,json
from pathlib import Path
from MCPClient import rpc
from Control import call,job
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3'
start=time.monotonic()
while 'DONE DiscoveryQHD' not in (O/'DiscoveryOrchestration.log').read_text():
 time.sleep(2);assert time.monotonic()-start<1200
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'EnvironmentPerfV3','version':'1'}})
call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3)
job('ReviewShots.py');start=time.monotonic()
f=O/'Screenshots/CandidatesQHD/Review.json'
while not f.exists():
 time.sleep(2);assert time.monotonic()-start<900
assert not json.loads(f.read_text())['error'];time.sleep(4);call('EditorToolset.EditorAppToolset','StopPIE',{});print('Candidate review complete')
