"""Summarize measured CSV timing and matched real screenshots. Never invent absent counters."""
from pathlib import Path
import json,csv,statistics,math,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';wanted=['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/SingleLayerWater','GPU/SingleLayerWaterDepthPrepass','GPU/LumenIrradianceFieldGather','GPU/LumenSceneLighting','GPU/TAA'];allrows={}
def read(p):
 raw=list(csv.reader(p.open()));headers=next((r for r in reversed(raw)if r and r[0]=='EVENTS'),raw[0]);cols={k:[]for k in headers}
 for line in raw[1:]:
  if not line or line[0]=='EVENTS'or line[0].startswith('[HasHeaderRowAtEnd]'):continue
  values=dict(zip(headers,line))
  try:frame=float(values['FrameTime'])
  except(ValueError,TypeError,KeyError):continue
  if not math.isfinite(frame)or frame<=0:continue
  for k,v in values.items():
   try:x=float(v)
   except(ValueError,TypeError):continue
   if math.isfinite(x)and x>=0:cols[k].append(x)
 return cols
def stats(cols):
 ts=sorted(x for x in cols['FrameTime']if x>0);return dict(frames=len(ts),fps=1000/statistics.mean(ts),p95_ms=ts[min(len(ts)-1,int(len(ts)*.95))],one_percent_low_fps=1000/statistics.mean(ts[-max(1,math.ceil(len(ts)*.01)):]),max_frame_ms=max(ts),counters={k:statistics.mean(cols[k])if cols.get(k)else None for k in wanted})
for label in ['NativeBefore01','NativeAfter02','PairedMaterials01','SceneCostPair02']:
 r=json.loads((D/label/'Result.json').read_text());assert r['passed'];groups={};windows=[]
 for row in r['rows']:
  cols=read(D/label/'UserData/Saved/Profiling/CSV'/(row['csv_prefix']+'.csv'));summary=stats(cols);windows.append(dict(site=row['site'],repeat=row['repeat'],**summary));g=groups.setdefault(row['site'],{})
  for k,values in cols.items():g.setdefault(k,[]).extend(values)
 allrows[label]=dict(windows=windows,sites={k:stats(v)for k,v in groups.items()})
pairs=[]
for before,after in [('BeforeAtlas','AfterAtlas07'),('BeforeExtra','AfterExtra02'),('NativeBefore01','NativeAfter02')]:
 b=json.loads((D/before/'Result.json').read_text());a=json.loads((D/after/'Result.json').read_text());assert a['passed']and b['passed']
 for row in b['rows']:
  if row['repeat']!=1:continue
  other=next(x for x in a['rows']if x['repeat']==1 and x['site']==row['site']);delta={key:[y-x for x,y in zip(row[key],other[key])]for key in ['camera','rotation','player']};assert row['viewport']==other['viewport']==[2560,1440]and row['screen_percentage']==other['screen_percentage']==75
  assert max(abs(x)for x in delta['rotation'])<.1
  for label in [before,after]:
   head=(D/label/(row['site']+'.png')).read_bytes()[:24];assert struct.unpack('>II',head[16:24])==(2560,1440)
  pairs.append(dict(source_pair=[before,after],site=row['site'],delta_cm_or_degrees=delta,exact_world_camera=max(abs(x)for x in delta['camera'])<.1,verified_qhd=True,note='Same XY/yaw/pitch/zoom fixture; actual ground/collision height may intentionally change the following camera. No claim of exact world-space camera equality when height changed.'))
allrows['pairs']=pairs
p=D/'NativeGameplay02';r=json.loads((p/'Result.json').read_text());assert r['passed'];allrows['dynamic_tour']=stats(read(p/'UserData/Saved/Profiling/CSV/FAB_NativeGameplay02_Tour.csv'));allrows['dynamic_tour']['method']='Only continuous 42-waypoint real-input tour before screenshots, menus, battle, save/load or test-area visits. Active clock, AI and companion; no video. One whole route, not repeated long-term stability certification.'
log=(D/'Editor03/Engine.log').read_text(errors='replace');import re
checks=[]
for m in re.finditer(r'VISUALV2_FAB_V1_MAPCHECK_BEGIN ([^\r\n]+)(.*?)VISUALV2_FAB_V1_MAPCHECK_END',log,re.S):
 counts=re.findall(r'Kartenprüfung abgeschlossen: (\d+) Fehler, (\d+) Warnung',m[2]);assert len(counts)==1,m[1];checks.append(dict(map=m[1],counts=list(counts[0])))
assert len(checks)==12 and all(x['counts']==['0','0']for x in checks);allrows['map_checks']=checks;(D/'MapCheckResults.json').write_text(json.dumps(checks,indent=2))
(D/'Analysis.json').write_text(json.dumps(allrows,indent=2));print(json.dumps({k:v['sites']for k,v in allrows.items()if k.startswith(('Native','Paired'))},indent=2));print('DYNAMIC',allrows['dynamic_tour'])
