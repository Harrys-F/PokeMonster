"""Summarize only observed frame samples / complete CSV records. Diagnostic GPU captures remain separate."""
from pathlib import Path
import json,csv,statistics,math,sys
R=Path.cwd();D=R/'Saved/ProjectRefinement/InventoryV2';labels=sys.argv[1:]or['Native03','Native04','Native05','Native06','PIE05'];output=[]
def stats(a):
 a=sorted(a);n=len(a)
 return {'frames':n,'mean_ms':statistics.mean(a),'fps':1000/statistics.mean(a),'p95_ms':a[min(n-1,math.ceil(n*.95)-1)],'max_ms':max(a),'over_33_333_ms':sum(x>1000/30 for x in a)}
for label in labels:
 O=D/label;p=O/'Result.json'
 if not p.exists():continue
 result=json.loads(p.read_text())
 for row in result.get('performance',[]):
  vals=[x for x in row['frames']if 0<x<10000];entry={'run':label,'scenario':row['name'],'source':'Slate post-tick dt; active world, no video','frame':stats(vals),'seconds':row['seconds']}
  cp=O/('Perf_'+row['name']+'.csv');columns={}
  if cp.exists():
   records=[r for r in csv.DictReader(cp.open())if not str(r.get('EVENTS','')).startswith('[')and r.get('EVENTS')!='EVENTS']
   for name in ['FrameTime','GameThreadTime','RenderThreadTime','GPUTime']:
    values=[]
    for rec in records:
     try:v=float(rec.get(name,''))
     except(ValueError,TypeError):continue
     if math.isfinite(v)and 0<v<10000:values.append(v)
    if values:columns[name]=stats(values)
  entry['csv']=columns;entry['preferred_frame']=columns.get('FrameTime',entry['frame']);entry['gpu_csv_diagnostic']=label=='Native04';output.append(entry)
(D/'PerformanceSummary.json').write_text(json.dumps(output,indent=2))
for x in output:
 print(x['run'],x['scenario'],'fps',round(x['frame']['fps'],2),'frame',round(x['frame']['mean_ms'],2),'p95',round(x['frame']['p95_ms'],2),'CSV',','.join(k+':'+str(round(v['mean_ms'],2))for k,v in x['csv'].items()),'GPU diagnostic'if x['gpu_csv_diagnostic']else'')
