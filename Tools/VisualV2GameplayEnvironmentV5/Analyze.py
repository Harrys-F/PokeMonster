"""Measured CSV summaries; zero/unavailable counters remain explicitly unavailable."""
from pathlib import Path
import json,csv,statistics,math,struct,re
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5';wanted=['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/LumenIrradianceFieldGather','GPU/LumenSceneLighting','GPU/TAA'];results={}
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
 ts=sorted(x for x in cols['FrameTime']if x>0);return dict(frames=len(ts),fps=1000/statistics.mean(ts),p95_ms=ts[min(len(ts)-1,int(len(ts)*.95))],one_percent_low_fps=1000/statistics.mean(ts[-max(1,math.ceil(len(ts)*.01)):]),max_frame_ms=max(ts),counters={k:statistics.mean(cols[k])if cols.get(k)and any(cols[k])else None for k in wanted})
for label in ['NativeBefore01','NativeAfter02']:
 data=json.loads((D/label/'Result.json').read_text());assert data['passed'];groups={};windows=[]
 for r in data['rows']:
  cols=read(D/label/'UserData/Saved/Profiling/CSV'/(r['csv_prefix']+'.csv'));windows.append(dict(site=r['site'],repeat=r['repeat'],**stats(cols)));g=groups.setdefault(r['site'],{})
  for k,v in cols.items():g.setdefault(k,[]).extend(v)
 results[label]=dict(windows=windows,sites={k:stats(v)for k,v in groups.items()})
results['matched_images']=[]
b=json.loads((D/'BeforeAtlas/Result.json').read_text());a=json.loads((D/'AfterAtlas03/Result.json').read_text());assert a['passed']and b['passed']
for row in b['rows']:
 other=next(x for x in a['rows']if x['site']==row['site']);diff={k:[y-x for x,y in zip(row[k],other[k])]for k in ['camera','rotation','player']};assert row['viewport']==other['viewport']==[2560,1440]and row['screen_percentage']==other['screen_percentage']==75
 assert max(abs(v)for v in diff['rotation'])<.1
 for folder in ['BeforeAtlas','AfterAtlas03']:assert struct.unpack('>II',(D/folder/(row['site']+'.png')).read_bytes()[16:24])==(2560,1440)
 results['matched_images'].append(dict(site=row['site'],delta_cm_degrees=diff,identical_camera=max(abs(v)for v in diff['camera'])<.1,actual_qhd=True))
p=D/'NativeGameplay02';x=json.loads((p/'Result.json').read_text());assert x['passed'];results['native_dynamic_tour']=stats(read(p/'UserData/Saved/Profiling/CSV/FAB_NativeGameplay02_Tour.csv'));results['native_dynamic_tour']['method']='One complete continuous existing-road tour before captures, battle, dialogue, save/load or travel. Active clock/AI/companion, real Enhanced Input and physical player collision; no in-route positioning teleports and no video. Not a long-term stability certification.'
log=(D/'Editor03/Engine.log').read_text(errors='replace');checks=[]
for m in re.finditer(r'VISUALV2_FAB_V1_MAPCHECK_BEGIN ([^\r\n]+)(.*?)VISUALV2_FAB_V1_MAPCHECK_END',log,re.S):
 counts=re.findall(r'Kartenprüfung abgeschlossen: (\d+) Fehler, (\d+) Warnung',m[2]);assert len(counts)==1,m[1];checks.append(dict(map=m[1],errors=int(counts[0][0]),warnings=int(counts[0][1])))
assert len(checks)==12 and all(r['errors']==r['warnings']==0 for r in checks);results['map_checks']=checks;(D/'MapCheckResults.json').write_text(json.dumps(checks,indent=2));(D/'Analysis.json').write_text(json.dumps(results,indent=2))
for label in ['NativeBefore01','NativeAfter02']:
 print(label,{k:{n:round(v[n],2)for n in ['fps','p95_ms','one_percent_low_fps']}for k,v in results[label]['sites'].items()})
print('Dynamic',results['native_dynamic_tour'])
