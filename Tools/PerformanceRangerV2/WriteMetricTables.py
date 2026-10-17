"""Derived tables, never substitutes for raw observations. Run after measurements, not alongside profiling."""
import json,statistics,csv
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');O=R/'Art/Characters/NPCs/Ranger/Review/V2';m=json.loads((O/'Measurements.json').read_text());lines=[]
def med(xs):return statistics.median(xs)
def metric(rows,n):
 vals=[r.get('csv',{}).get(n,{}).get('median') for r in rows];vals=[v for v in vals if v is not None];return f'{med(vals):.3f}' if vals else 'nicht erfasst'
lines+=['## Baseline und Wiederholung','', '| Reihe | Standort | FPS der 3 Läufe | Median FPS | Median ms | Median P95 ms | Game ms | Render ms | GPU ms |','|---|---|---|---:|---:|---:|---:|---:|---:|']
for name in ['BeforeA','AfterA','BeforeB','AfterB','BeforeC','AfterC']:
 for site in ['Dorf','Wald','Weg','DorfBauten']:
  rs=[r for r in m.get(name,[]) if r['site']==site]
  if not rs:continue
  lines.append('| '+ ' | '.join([name,site,', '.join(f"{r['median_fps']:.2f}" for r in rs),f"{med([r['median_fps'] for r in rs]):.2f}",f"{med([r['median_ms'] for r in rs]):.3f}",f"{med([r['p95_ms'] for r in rs]):.3f}",metric(rs,'GameThreadTime'),metric(rs,'RenderThreadTime'),metric(rs,'GPUTime')])+' |')
lines+=['','## Zeitlich verschachtelte V1/V2-Paare','','| Reihe | Standort | V1 ms | V2 ms | Differenz ms V2−V1 je Paar | Median Differenz ms |','|---|---|---:|---:|---|---:|']
for name in ['PairedA','PairedB','VillageA','VillageB','VillageC']:
 for site in ['Dorf','Wald','Weg','DorfBauten']:
  a=[r for r in m.get(name,[]) if r['site']==site and r['condition']=='V1'];b=[r for r in m.get(name,[]) if r['site']==site and r['condition']=='V2']
  if len(a)!=3 or len(b)!=3:continue
  diffs=[next(r['median_ms'] for r in b if r['repeat']==i)-next(r['median_ms'] for r in a if r['repeat']==i) for i in [1,2,3]]
  lines.append(f"| {name} | {site} | {med([r['median_ms'] for r in a]):.3f} | {med([r['median_ms'] for r in b]):.3f} | "+', '.join(f'{x:+.3f}' for x in diffs)+f' | {med(diffs):+.3f} |')
lines+=['','## Isolierte Faktoren','','Je Variante zwei direkte Kontroll-/Variantenpaare; zweite Runde in umgekehrter Faktor-Reihenfolge. Negative Differenz = schneller. Keine statistische Signifikanzbehauptung.','','| Standort | Faktor | Kontroll-ms | Varianten-ms | Median Δ ms | Δ der beiden Paare | GPU Δ ms |','|---|---|---:|---:|---:|---|---:|']
for site in ['Dorf','Wald','Weg','DorfBauten']:
 rs=m.get('Factors_'+('Village' if site=='DorfBauten' else site),[])
 for cond in dict.fromkeys(r['condition'] for r in rs if r['condition']!='V1'):
  pairs=[(next(x for x in rs if x['segment']==r['segment']-1),r) for r in rs if r['condition']==cond];diff=[b['median_ms']-a['median_ms'] for a,b in pairs];gpu=[b['csv']['GPUTime']['median']-a['csv']['GPUTime']['median'] for a,b in pairs if 'GPUTime' in b.get('csv',{}) and 'GPUTime' in a.get('csv',{})]
  lines.append(f'| {site} | {cond} | {med([a["median_ms"] for a,b in pairs]):.3f} | {med([b["median_ms"] for a,b in pairs]):.3f} | {med(diff):+.3f} | '+', '.join(f'{x:+.3f}' for x in diff)+' | '+(f'{med(gpu):+.3f}' if gpu else 'offen')+' |')
(O/'MetricTables.md').write_text('\n'.join(lines)+'\n')
