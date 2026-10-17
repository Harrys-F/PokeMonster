import json,statistics,collections
from pathlib import Path
from Summarize import summarize
from ResolveMeasurements import resolve
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2';data=resolve(summarize());tables=[]
CAND=json.loads((O/'SelectedCandidate.json').read_text())['condition']
def med(a):return statistics.median(a)
def metric(r,n):
 v=r.get('csv',{}).get(n)
 if n in ['RenderThreadTime','RenderThreadTime_CriticalPath'] and r.get('window',[[0,0,0]])[0][2]==2.0:return None
 return v['median'] if v and not (v['all_zero'] and n in ['RenderThreadTime','RHI/DrawCalls','RHI/PrimitivesDrawn']) else None
def col(rs,n):
 vals=[v for r in rs if (v:=metric(r,n)) is not None];return f'{med(vals):.3f}' if vals else 'n/v'
def config(r):return (r['extent'][0][0],r['extent'][0][1],r['quality'],r['percentage'],r['site'])
groups=collections.defaultdict(list)
for r in data.get('BaselinePIE',[]):groups[config(r)].append(r)
tables+=['## Baseline: eingebettetes PIE','', '| Ausgabe | Qualität | SP | Ort | FPS je Lauf | Median FPS | Frame ms | P95 ms je Lauf | Game ms | Render ms | GPU ms |','|---|---|---|---|---|---:|---:|---|---:|---:|---:|']
for (w,h,q,p,s),rs in groups.items():tables.append(f"| {w}×{h} | {'Medium' if q=='1' else 'High'} | {p}% | {s} | "+', '.join(f'{r["median_fps"]:.2f}' for r in rs)+f' | {med(r["median_fps"] for r in rs):.2f} | {med(r["median_ms"] for r in rs):.3f} | '+', '.join(f'{r["p95_ms"]:.3f}' for r in rs)+f' | {col(rs,"GameThreadTime")} | {col(rs,"RenderThreadTime")} | {col(rs,"GPUTime")} |')
tables+=['','## Einzelfaktor-Paare','','Negative Differenzen bedeuten kürzere Framezeit. Drei benachbarte Paare, umgekehrte Reihenfolge in Wiederholung 2. QHD/High/100%.','', '| Serie/Ort | Faktor | Δ Frame ms je Paar | Median Δ Frame ms | Median Δ GPU ms |','|---|---|---|---:|---:|']
pairs=[]
for label in ['FactorsQHD','FactorsFollowup']:
 rows=data.get(label,[]);g=collections.defaultdict(list)
 for a,b in zip(rows[::2],rows[1::2]):
  if a['condition']!='Control' and b['condition']!='Control':continue
  c,v=(a,b) if a['condition']=='Control' else (b,a);g[(v['site'],v['condition'])].append((c,v))
 for (site,f),ps in g.items():
  ds=[v['median_ms']-c['median_ms'] for c,v in ps];gpu=[metric(v,'GPUTime')-metric(c,'GPUTime') for c,v in ps if metric(v,'GPUTime') is not None and metric(c,'GPUTime') is not None]
  tables.append(f'| {label}/{site} | {f} | '+', '.join(f'{v:+.3f}' for v in ds)+f' | {med(ds):+.3f} | '+(f'{med(gpu):+.3f}' if gpu else 'n/v')+' |')
  pairs.append({'label':label,'site':site,'factor':f,'frame_deltas_ms':ds,'gpu_deltas_ms':gpu})
for mode,labels in [('PIE',['FinalPairedPIE']),('Standalone',['StandalonePair'+str(i) for i in range(1,7)])]:
 tables+=['',f'## Finale Paare: {mode}','','| Ausgabe | Qualität | SP | Ort | Kontrolle FPS | Kandidat FPS | Kontrolle Frame ms | Kandidat Frame ms | Δ ms je Paar | Median Δ ms | Kontrolle/Kandidat P95 ms | Kontrolle/Kandidat Game ms | Kontrolle/Kandidat Render ms | Kontrolle/Kandidat Render CriticalPath ms | Kontrolle/Kandidat GPU ms |','|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|---|'];g=collections.defaultdict(list)
 for label in labels:
  rows=data.get(label,[])
  for a,b in zip(rows[::2],rows[1::2]):
   if {a['condition'],b['condition']}!={'Control',CAND}:continue
   c,v=(a,b) if a['condition']=='Control' else (b,a);g[config(c)].append((c,v))
 for (w,h,q,p,s),ps in g.items():
  cs=[x[0] for x in ps];vs=[x[1] for x in ps];ds=[v['median_ms']-c['median_ms'] for c,v in ps]
  tables.append(f"| {w}×{h} | {'Medium' if q=='1' else 'High'} | {p}% | {s} | {med(r['median_fps'] for r in cs):.2f} | {med(r['median_fps'] for r in vs):.2f} | {med(r['median_ms'] for r in cs):.3f} | {med(r['median_ms'] for r in vs):.3f} | "+', '.join(f'{v:+.3f}' for v in ds)+f" | {med(ds):+.3f} | {med(r['p95_ms'] for r in cs):.3f}/{med(r['p95_ms'] for r in vs):.3f} | {col(cs,'GameThreadTime')}/{col(vs,'GameThreadTime')} | {col(cs,'RenderThreadTime')}/{col(vs,'RenderThreadTime')} | {col(cs,'RenderThreadTime_CriticalPath')}/{col(vs,'RenderThreadTime_CriticalPath')} | {col(cs,'GPUTime')}/{col(vs,'GPUTime')} |")
(O/'MetricTables.md').write_text('\n'.join(tables)+'\n');(O/'FactorPairs.json').write_text(json.dumps(pairs,indent=2))
validation={}
for label,rows in data.items():
 validation[label]={'segments':len(rows),'extents':sorted({tuple(e) for r in rows for e in r['extent']}),'fractions':sorted({tuple(e) for r in rows for e in r['fractions']}),'windows':sorted({tuple(e) for r in rows for e in r['window']}),'active_window_fraction_range':[min(r.get('active_window_fraction',-1) for r in rows),max(r.get('active_window_fraction',-1) for r in rows)] if rows else []}
(O/'MeasurementValidation.json').write_text(json.dumps(validation,indent=2))
print('Wrote metric tables and per-segment validation')
