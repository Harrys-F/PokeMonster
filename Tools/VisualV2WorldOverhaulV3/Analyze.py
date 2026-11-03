"""Summarize measured CSV timing and matched real screenshots. Never invent absent counters."""
from pathlib import Path
import json,csv,statistics,math,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2WorldOverhaulV3';wanted=['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/SingleLayerWater','GPU/SingleLayerWaterDepthPrepass','GPU/LumenIrradianceFieldGather','GPU/LumenSceneLighting','GPU/TAA'];allrows={}
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
for label in ['NativeBefore01','NativeAfter02']:
 r=json.loads((D/label/'Result.json').read_text());assert r['passed'];groups={};windows=[]
 for row in r['rows']:
  cols=read(D/label/'UserData/Saved/Profiling/CSV'/(row['csv_prefix']+'.csv'));s=stats(cols);windows.append(dict(site=row['site'],repeat=row['repeat'],**s));g=groups.setdefault(row['site'],{})
  for k,values in cols.items():g.setdefault(k,[]).extend(values)
 allrows[label]=dict(windows=windows,sites={k:stats(v)for k,v in groups.items()})
# Capture pipeline and camera transforms, not just equal image dimensions.
pairs=[]
for before,after in [('BeforeAtlas','AfterAtlas03'),('NativeBefore01','NativeAfter02')]:
 b=json.loads((D/before/'Result.json').read_text());a=json.loads((D/after/'Result.json').read_text());assert a['passed']and b['passed']
 for row in b['rows']:
  if row['repeat']!=1:continue
  other=next(x for x in a['rows']if x['repeat']==1 and x['site']==row['site']);deltas={key:max(abs(x-y)for x,y in zip(row[key],other[key]))for key in ['camera','rotation','player']};assert row['viewport']==other['viewport']==[2560,1440]and row['screen_percentage']==other['screen_percentage']==75
  assert deltas['rotation']<.1;assert max(deltas.values())<.1 or row['site']=='Steinplateau',deltas
  for label in [before,after]:
   head=(D/label/(row['site']+'.png')).read_bytes()[:24];assert struct.unpack('>II',head[16:24])==(2560,1440)
  pairs.append(dict(source_pair=[before,after],site=row['site'],deltas_cm_or_degrees=deltas,exact_camera=max(deltas.values())<.1,verified_qhd=True))
allrows['pairs']=pairs
p=D/'NativeGameplay02';r=json.loads((p/'Result.json').read_text());assert r['passed'];allrows['dynamic_tour']=stats(read(p/'UserData/Saved/Profiling/CSV/FAB_NativeGameplay02_Tour.csv'));allrows['dynamic_tour']['method']='Only the 42-waypoint real-input tour before any capture, dialogue, save/load or test-area visit; no video; one full route, not repeated stability certification.'
allrows['map_checks']=json.loads((D/'MapCheckResults.json').read_text());assert len(allrows['map_checks'])==12 and all(x['counts']==['0','0']for x in allrows['map_checks']);(D/'Analysis.json').write_text(json.dumps(allrows,indent=2));print(json.dumps({k:v['sites']for k,v in allrows.items()if k.startswith('Native')},indent=2));print('DYNAMIC',allrows['dynamic_tour'])
