"""Summarize recorded CSVs, camera pairs and the actual scoped QA result."""
from pathlib import Path
import json,csv,statistics,math,re,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';allrows={};core=json.loads((R/'Tools/VisualV2EnvironmentPolishV2/Sites.json').read_text());sites=[s[0]for s in core]
def mean(xs):return statistics.mean(xs)if xs else None
for label in ['NativeBefore01','NativeFinal01']:
 r=json.loads((D/label/'Result.json').read_text());assert r['passed'];data=[]
 for row in r['rows']:
  p=D/label/'UserData/Saved/Profiling/CSV'/(row['csv_prefix']+'.csv');assert p.is_file(),p
  raw=list(csv.reader(p.open()));headers=next((r for r in reversed(raw)if r and r[0]=='EVENTS'),raw[0]);cols={k:[]for k in headers}
  for line in raw[1:]:
   if not line or line[0]=='EVENTS' or line[0].startswith('[HasHeaderRowAtEnd]'):continue
   values=dict(zip(headers,line))
   try:frame=float(values['FrameTime'])
   except(ValueError,TypeError,KeyError):continue
   if not math.isfinite(frame)or frame<=0:continue
   for k,v in values.items():
    try:x=float(v)
    except(ValueError,TypeError):continue
    if math.isfinite(x)and x>=0:cols[k].append(x)
  wanted=['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/SingleLayerWater','GPU/SingleLayerWaterDepthPrepass','GPU/LumenScreenProbeGather','GPU/LumenSceneLighting','GPU/LumenIrradianceFieldGather','GPU/TAA']
  row=dict(row);row['csv_means_ms']={k:mean(cols.get(k,[]))for k in wanted};times=[x for x in cols.get('FrameTime',[])if x>0];row['csv_fps']=1000/mean(times);row['csv_p95_ms']=sorted(times)[int(len(times)*.95)];data.append(row)
 summary={}
 for s in sites:
  rows=[x for x in data if x['site']==s];assert len(rows)==3
  summary[s]=dict(fps=mean([x['csv_fps']for x in rows]),fps_min=min(x['csv_fps']for x in rows),fps_max=max(x['csv_fps']for x in rows),frame_p95_ms=mean([x['csv_p95_ms']for x in rows]),counters={k:mean([x['csv_means_ms'][k]for x in rows if x['csv_means_ms'][k]is not None])for k in wanted},population=[x['active_population']for x in rows])
 allrows[label]=dict(rows=data,summary=summary)
pairs=[]
for b in allrows['NativeBefore01']['rows']:
 if b['repeat']!=1:continue
 a=next(x for x in allrows['NativeFinal01']['rows']if x['repeat']==1 and x['site']==b['site']);deltas={key:max(abs(x-y)for x,y in zip(a[key],b[key]))for key in ['camera','rotation','player']};assert max(deltas.values())<.1,(b['site'],deltas);assert a['viewport']==b['viewport']==[2560,1440]and a['screen_percentage']==b['screen_percentage']==75
 for label in allrows:
  p=D/label/(b['site']+'.png');head=p.read_bytes()[:24];assert head[:8]==b'\x89PNG\r\n\x1a\n';assert struct.unpack('>II',head[16:24])==(2560,1440)
 pairs.append(dict(site=b['site'],camera_deltas_cm_or_degrees=deltas,verified_qhd=True))
text=(D/'Editor01/Engine.log').read_text(errors='replace');checks=[]
for name in json.loads((D/'MapChecks.json').read_text()):
 part=text.split('VISUALV2_FAB_V1_MAPCHECK_BEGIN '+name,1)[1].split('VISUALV2_FAB_V1_MAPCHECK_END '+name,1)[0];match=re.search(r'(\d+) (?:Fehler|Errors?).*?(\d+) (?:Warnung|Warnings?)',part);assert match and match.groups()==('0','0'),(name,part);checks.append(dict(map=name,errors=0,warnings=0))
assert len(checks)==12;allrows['pairs']=pairs;allrows['map_checks']=checks;(D/'Analysis.json').write_text(json.dumps(allrows,indent=2));print(json.dumps({k:v['summary']for k,v in allrows.items()if k.startswith('Native')},indent=2))
