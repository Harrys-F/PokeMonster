"""Strict post-run validation and aggregation. Run after GPU timings finish."""
import json,statistics,csv,re
from collections import defaultdict
from pathlib import Path
from Summarize import summarize
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2GPUBottleneckV1';P=R/'Saved/EnvironmentPerfV2';data=summarize();groups=defaultdict(list);valid=[];pairs=[]
for label,rows in data.items():
 assert (P/(label+'_Done.txt')).read_text()=='Complete',label
 plan=(R/'Tools/VisualV2GPUBottleneckV1/Plans'/(label+'.tsv')).read_text().splitlines()
 expected=[x.split('\t') for x in plan[1:] if x]
 regular=[r for r in rows if r['site']!='CSVDrain']
 settings=(P/(label+'_Settings.txt')).read_text()
 blocks=settings.split('segment=')[1:]
 for block in blocks:
  index=int(block.split()[0]);e=expected[index]
  if e[0]=='CSVDrain':continue
  if e[1]=='Control':
   wanted={'r.AntiAliasingMethod':4,'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4 if int(e[5])==1 else 8,'r.Lumen.FinalGatherMethod':0 if int(e[5])==1 else 1,'r.Lumen.Reflections.Allow':0 if int(e[5])==1 else 1}
   for name,value in wanted.items():
    match=re.search(r'^'+re.escape(name)+r'=([^ ]+)',block,re.M);assert match and float(match[1])==value,(label,index,name,match[1] if match else None)
  if e[1].startswith('CV:'):
   name,value=e[1][3:].split('=');match=re.search(r'^factor_verified '+re.escape(name)+r'=([^ ]+)',block,re.M)
   assert match and float(match[1])==float(value),(label,index,e[1],'CVar not applied')

 assert len(regular)==sum(x[0]!='CSVDrain' for x in expected),(label,len(regular))
 for r in regular:
  e=expected[r['segment']];width,height,q,sp=map(int,e[3:]);assert r['quality']==str(q) and r['percentage']==str(sp)
  assert r['extent']==[(width,height,width,height,width,height,(width*sp+99)//100,(height*sp+99)//100)],(label,r['segment'],r['extent'])
  assert r['fractions']==[(sp/100,1.0)]
  assert r['resolution_samples_increment']>0,(label,r['segment'],'stale renderer resolution observation')
  assert r['csv'],(label,r['segment'],'missing CSV counters')
  if r['condition']!='CV:r.GPUCsvStatsEnabled=0':assert r['csv'].get('GPUTime',{}).get('median',0)>0,(label,r['segment'],'missing GPU timing')
  else:r['csv']={n:v for n,v in r['csv'].items() if not n.startswith('GPU/') and n!='GPUTime'}
  for n,v in [('pitch',-50),('yaw',-45),('fov',35)]:assert max(abs(x-v) for x in r['camera'][n])<.001
  r['label']=label;r['mode']='PIE' if '_PIE_' in label else 'Standalone';r['width']=width;r['height']=height
  valid.append({k:r[k] for k in ['label','segment','site','condition','repeat','extent','fractions','camera','samples']})
  groups[(r['mode'],width,height,q,sp,r['site'],r['condition'])].append(r)
 if 'Factors' in label or 'Confirm' in label:
  for i in range(0,len(regular),2):
   a,b=regular[i:i+2]
   control,test=(a,b) if a['condition']=='Control' else (b,a)
   assert control['condition']=='Control' and test['condition']!='Control' and control['site']==test['site'] and control['repeat']==test['repeat']
   def med(r,n):return r['csv'].get(n,{}).get('median')
   pairs.append({'label':label,'mode':control['mode'],'site':control['site'],'condition':test['condition'],'repeat':control['repeat'],'control_ms':control['median_ms'],'test_ms':test['median_ms'],'delta_ms':test['median_ms']-control['median_ms'],'control_p95':control['p95_ms'],'test_p95':test['p95_ms'],'control_gpu':med(control,'GPUTime'),'test_gpu':med(test,'GPUTime'),'delta_gpu':(med(test,'GPUTime')-med(control,'GPUTime')) if med(test,'GPUTime') is not None and med(control,'GPUTime') is not None else None,'control_game':med(control,'GameThreadTime'),'test_game':med(test,'GameThreadTime'),'control_counters':{n:v['median'] for n,v in control['csv'].items()},'test_counters':{n:v['median'] for n,v in test['csv'].items()}})
summary=[]
for key,rs in groups.items():
 mode,width,height,q,sp,site,condition=key
 if condition=='Control' and any('Base_' not in r['label'] for r in rs):rs=[r for r in rs if 'Base_' in r['label']]
 if not rs:continue
 assert len(rs)==3,(key,len(rs))
 ms=statistics.median(r['median_ms'] for r in rs)
 summary.append({'mode':mode,'width':width,'height':height,'quality':q,'percentage':sp,'site':site,'condition':condition,'fps':1000/ms,'median_ms':ms,'p95_ms':statistics.median(r['p95_ms'] for r in rs),'individual_ms':[r['median_ms'] for r in rs],'csv':{n:statistics.median(r['csv'][n]['median'] for r in rs if n in r['csv']) for n in set().union(*(r['csv'] for r in rs))}})
pg=defaultdict(list)
for p in pairs:pg[(p['mode'],p['site'],p['condition'])].append(p)
ps=[]
for key,rs in pg.items():
 assert len(rs)==3,(key,len(rs));ps.append({'mode':key[0],'site':key[1],'condition':key[2],'delta_ms':statistics.median(r['delta_ms'] for r in rs),'delta_gpu':statistics.median([r['delta_gpu'] for r in rs if r['delta_gpu'] is not None]) if any(r['delta_gpu'] is not None for r in rs) else None,'individual_delta_ms':[r['delta_ms'] for r in rs],'individual_delta_gpu':[r['delta_gpu'] for r in rs],'pairs':rs})
(O/'Validation.json').write_text(json.dumps({'regular_segments':len(valid),'rows':valid},indent=2));(O/'Summary.json').write_text(json.dumps(summary,indent=2));(O/'Pairs.json').write_text(json.dumps(ps,indent=2))
with (O/'Summary.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=['mode','width','height','quality','percentage','site','condition','fps','median_ms','p95_ms','game_ms','render_ms','gpu_ms']);writer.writeheader()
 for r in summary:writer.writerow({**{k:r[k] for k in writer.fieldnames if k in r},'game_ms':r['csv'].get('GameThreadTime'),'render_ms':r['csv'].get('RenderThreadTime'),'gpu_ms':r['csv'].get('GPUTime')})
print('Validated regular segments',len(valid),'summaries',len(summary),'paired conditions',len(ps))
for p in ps:print(p['mode'],p['site'],p['condition'],'delta frame',round(p['delta_ms'],3),'delta GPU',round(p['delta_gpu'],3) if p['delta_gpu'] is not None else None,'individual',[round(x,3) for x in p['individual_delta_ms']])
