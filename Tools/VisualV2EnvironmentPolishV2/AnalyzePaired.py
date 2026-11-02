"""Read the final paired CSV windows; keep ordering and sample spread explicit."""
from pathlib import Path
import json,csv,math,statistics,struct
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2EnvironmentPolishV2';O=D/'NativePaired06';result=json.loads((O/'Result.json').read_text());assert result['passed']and json.loads((O/'ProcessExit.json').read_text())['returncode']==0;rows=[]
keys=['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/LumenIrradianceFieldGather','GPU/TAA']
for row in result['rows']:
 raw=list(csv.reader((O/'UserData/Saved/Profiling/CSV'/(row['csv_prefix']+'.csv')).open()));header=next(r for r in reversed(raw)if r and r[0]=='EVENTS');cols={k:[]for k in keys}
 for line in raw[1:]:
  if not line or line[0]=='EVENTS'or line[0].startswith('[HasHeaderRowAtEnd]'):continue
  v=dict(zip(header,line))
  try:frame=float(v['FrameTime'])
  except(KeyError,ValueError):continue
  if not math.isfinite(frame)or frame<=0:continue
  for k in keys:
   try:x=float(v[k])
   except(KeyError,ValueError):continue
   if math.isfinite(x)and x>=0:cols[k].append(x)
 site,variant=row['site'].split('__');times=sorted(cols['FrameTime']);assert times;rows.append(dict(site=site,variant=variant,repeat=row['repeat'],fps=1000/statistics.mean(times),p95=times[int(len(times)*.95)],counters={k:statistics.mean(v)if v else None for k,v in cols.items()},camera=row['camera'],rotation=row['rotation'],player=row['player'],population=row['active_population']))
summary={};pairs=[]
for site in ['Blumenwiese','Waldrand','Dorf']:
 summary[site]={}
 for variant in ['Before','After']:
  rs=[r for r in rows if r['site']==site and r['variant']==variant];assert len(rs)==3;summary[site][variant]=dict(fps=statistics.mean(r['fps']for r in rs),fps_min=min(r['fps']for r in rs),fps_max=max(r['fps']for r in rs),p95=statistics.mean(r['p95']for r in rs),counters={k:statistics.mean(r['counters'][k]for r in rs if r['counters'][k]is not None)for k in keys})
 for rep in range(1,4):
  a=next(r for r in rows if r['site']==site and r['repeat']==rep and r['variant']=='After');b=next(r for r in rows if r['site']==site and r['repeat']==rep and r['variant']=='Before');assert all(max(abs(x-y)for x,y in zip(a[k],b[k]))<.1 for k in ['camera','rotation','player']);assert a['population']==b['population'];pairs.append(dict(site=site,repeat=rep,gpu_after_minus_before=a['counters']['GPUTime']-b['counters']['GPUTime'],fps_before=b['fps'],fps_after=a['fps']))
 for variant in ['Before','After']:
  p=O/(site+'__'+variant+'.png');assert struct.unpack('>II',p.read_bytes()[16:24])==(2560,1440)
s=(O/'Engine.log').read_text(errors='replace');assert 'Mobility of 'not in s;assert 'Failed to compile Material'not in s;out=dict(rows=rows,summary=summary,pairs=pairs,method='Three paired static noon windows/site; ordering After-Before, Before-After, After-Before. Original map visuals reconstructed in RAM, including stationary old bank clones. No disk map writes. Not regular moving gameplay FPS.');(D/'PairedAnalysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(summary,indent=2))
