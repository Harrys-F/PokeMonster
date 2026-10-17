import json,statistics,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';d=json.loads((O/'Measurements.json').read_text());results=[];lines=['| Modus | Ausgabe / Qualität / SP | Ort | FPS A → B | Median ms A → B | P95 ms A → B | GPU ms A → B | Game ms A → B | Render ms A → B | Δms B−A, drei Paare |','|---|---|---|---|---|---|---|---|---|---|']
med=lambda x:statistics.median(x)
def counter(rs,n):
 v=[r['csv'][n]['median'] for r in rs if n in r.get('csv',{}) and not r['csv'][n]['all_zero']]
 return med(v) if len(v)==len(rs) else None
fmt=lambda x:'n/v' if x is None else f'{x:.2f}'
for prefix,mode in [('NativeMatrix','Standalone'),('PIEMatrix','PIE')]:
 for i in range(1,7):
  label=prefix+str(i)
  if not (O/(label+'_Done.txt')).exists() or label not in d:continue
  rs=d[label]
  for site in ['Dorf','Wald','Weg']:
   a=[r for r in rs if r['site']==site and r['condition']=='Control'];b=[r for r in rs if r['site']==site and r['condition']=='TreeMinLOD1'];assert len(a)==len(b)==3
   a.sort(key=lambda x:x['repeat']);b.sort(key=lambda x:x['repeat']);delta=[y['median_ms']-x['median_ms'] for x,y in zip(a,b)];row={'mode':mode,'label':label,'site':site,'configuration':{k:a[0][k] for k in ['quality','percentage','extent','fractions']},'paired_delta_ms':delta,'median_paired_delta_ms':med(delta),'state':{}}
   for state,values in [('A_V2',a),('B_TreeMinLOD1',b)]:
    row['state'][state]={'median_fps':1000/med([r['median_ms'] for r in values]),'median_ms':med([r['median_ms'] for r in values]),'p95_ms':med([r['p95_ms'] for r in values]),'run_fps':[r['median_fps'] for r in values],'run_ms':[r['median_ms'] for r in values],'min_fps':min(r['median_fps'] for r in values),'max_fps':max(r['median_fps'] for r in values),'GPU_ms':counter(values,'GPUTime'),'Game_ms':counter(values,'GameThreadTime'),'Render_ms':counter(values,'RenderThreadTime') if mode=='Standalone' else None,'gpu_stages_ms':{k:counter(values,k) for k in values[0].get('csv',{}) if k.startswith('GPU/')}}
   x,y=row['state'].values();w,h=a[0]['extent'][0][:2];config=f"{w}×{h} / {'Medium' if a[0]['quality']=='1' else 'High'} / {a[0]['percentage']} %"
   pair=lambda n:fmt(x[n])+' → '+fmt(y[n])
   lines.append('| '+' | '.join([mode,config,site,*[pair(n) for n in ['median_fps','median_ms','p95_ms','GPU_ms','Game_ms','Render_ms']],', '.join(f'{x:+.2f}' for x in delta)])+' |');results.append(row)
(O/'PairedMetrics.json').write_text(json.dumps(results,indent=2));(O/'MetricTables.md').write_text('\n'.join(lines)+'\n')
for r in results:
 if r['configuration']['extent'][0][0]==2560:
  x,y=r['state'].values();print(r['label'],r['site'],fmt(x['median_fps']),fmt(y['median_fps']),'Δ',fmt(r['median_paired_delta_ms']))
