"""Summarize actual V7 CSV windows, natural routes and scene protection. No measurements invented."""
from pathlib import Path
import csv,json,math,statistics,re,collections
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def read(p):
 raw=list(csv.reader(p.open()));headers=next((r for r in reversed(raw)if r and r[0]=='EVENTS'),raw[0]);cols={k:[]for k in headers}
 for row in raw[1:]:
  if not row or row[0]=='EVENTS'or row[0].startswith('[HasHeaderRowAtEnd]'):continue
  values=dict(zip(headers,row))
  try:frame=float(values['FrameTime'])
  except(ValueError,TypeError,KeyError):continue
  if not math.isfinite(frame)or frame<=0:continue
  for k,v in values.items():
   try:x=float(v)
   except(ValueError,TypeError):continue
   if math.isfinite(x)and x>=0:cols[k].append(x)
 return cols
def stats(cols):
 ts=sorted(x for x in cols['FrameTime']if x>0);wanted=['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/LumenIrradianceFieldGather'];return dict(frames=len(ts),fps=1000/statistics.mean(ts),p95_ms=ts[min(len(ts)-1,int(len(ts)*.95))],one_percent_low_fps=1000/statistics.mean(ts[-max(1,math.ceil(len(ts)*.01)):]),max_frame_ms=max(ts),counters={k:statistics.mean(cols[k])if cols.get(k)and any(cols[k])else None for k in wanted})

results={}
for label in ['NativeBefore01','NativeAfter01','NativeAfterFinal01']:
 p=D/label/'Result.json'
 if not p.exists():continue
 data=load(p);assert data['passed'],data['error'];groups={};windows=[]
 for row in data['rows']:
  cols=read(D/label/'UserData/Saved/Profiling/CSV'/(row['csv_prefix']+'.csv'));windows.append(dict(site=row['site'],repeat=row['repeat'],**stats(cols)));g=groups.setdefault(row['site'],{})
  for k,v in cols.items():g.setdefault(k,[]).extend(v)
 results[label]=dict(windows=windows,sites={k:stats(v)for k,v in groups.items()})
(D/'Performance.json').write_text(json.dumps(results,indent=2))
for label,r in results.items():print(label,{k:dict(fps=round(v['fps'],2),gpu_ms=v['counters']['GPUTime'],game_ms=v['counters']['GameThreadTime'],render_ms=v['counters']['RenderThreadTime'],p95_ms=round(v['p95_ms'],2))for k,v in r['sites'].items()})
