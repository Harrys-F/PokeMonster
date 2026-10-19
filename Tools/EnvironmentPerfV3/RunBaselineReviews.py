
# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

import time,json
from pathlib import Path
from MCPClient import rpc
from Control import call,job
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3'
rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'EnvironmentPerfV3','version':'1'}})
for name,condition in [
 ('VisualV2','CV:r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor=1|r.Shadow.Virtual.SMRT.RayCountDirectional=8|r.Lumen.FinalGatherMethod=1|r.Lumen.HardwareRayTracing=1'),
 ('EnvironmentPerfV1','CV:r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor=2|r.Shadow.Virtual.SMRT.RayCountDirectional=2|r.Lumen.FinalGatherMethod=1|r.Lumen.HardwareRayTracing=1'),
 ('EnvironmentPerfV2','Control'),
 ('EnvironmentPerfV3','Control')]:
 map='/Game/Maps/Dev_TestMap_'+name;label='Baseline_'+name+'_QHD'
 (O/'LoadReviewRequest.json').write_text(json.dumps({'map':map}));job('LoadReviewMap.py')
 (O/'BenchmarkRequest.json').write_text(json.dumps({'label':label,'config':[2560,1440,2,100]}));job('PresetBeforePIE.py');time.sleep(15)
 call('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':1}});time.sleep(3)
 rows=[{'site':s,'tag':name,'condition':condition,'position':p} for s,p in [('Dorf',[-4100,450,50.15]),('Wald',[-4300,1550,50.15]),('Weg',[-36.6,-47.1,50.15])]]
 if name=='EnvironmentPerfV3':rows += [{'site':'NPCWald','tag':name,'condition':condition,'position':[-760,-1410,50.15]},{'site':'Crown','tag':name,'condition':condition,'position':[-1900,530,50.15]}]
 (O/'ReviewRequest.json').write_text(json.dumps({'label':label,'quality':2,'percentage':100,'rows':rows},indent=2));job('ReviewShots.py');start=time.monotonic();f=O/'Screenshots'/label/'Review.json'
 while not f.exists():
  time.sleep(2);assert time.monotonic()-start<300
 assert not json.loads(f.read_text())['error'];time.sleep(4);call('EditorToolset.EditorAppToolset','StopPIE',{});print('DONE',label,flush=True)
