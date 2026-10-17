import json,statistics
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');O=R/'Art/Characters/NPCs/Ranger/Review/V2';data=json.loads((O/'Measurements.json').read_text());out=[];med=statistics.median
out+=['## Gültige Baselines und finale Messungen','','A: 1280 × 740; B: 2331 × 1346; C: Standalone 1280 × 740. Medium / 75 %, VSync aus / uncapped. „Dorf“ in den Rohdaten bezeichnet den NPC-Vorplatz; die eigentliche Gebäudemessung heißt „DorfBauten“.','','| Reihe | Standort | Mesh | FPS der 3 Läufe | Median FPS | Median ms | Median der 3 P95 ms | Game ms | Render ms | GPU ms |','|---|---|---|---|---:|---:|---:|---:|---:|---:|']
for name in ['BeforeA','FinalPairedA','BeforeB','FinalPairedB','BeforeC','FinalAfterC','VillageA','VillageB','VillageC']:
 rows=data.get(name,[])
 for site in dict.fromkeys(r['site'] for r in rows):
  for condition in dict.fromkeys(r['condition'] for r in rows if r['site']==site):
   a=[r for r in rows if r['site']==site and r['condition']==condition]
   if len(a)!=3:continue
   def counter(n):
    v=[r.get('csv',{}).get(n,{}).get('median') for r in a];v=[x for x in v if x is not None];return ('n/a' if n=='RenderThreadTime' and med(v)==0 else f'{med(v):.3f}') if v else 'offen'
   out.append('| '+' | '.join([name,site,condition,', '.join(f"{r['median_fps']:.2f}" for r in a),f"{med([r['median_fps'] for r in a]):.2f}",f"{med([r['median_ms'] for r in a]):.3f}",f"{med([r['p95_ms'] for r in a]):.3f}",counter('GameThreadTime'),counter('RenderThreadTime'),counter('GPUTime')])+' |')
out+=['','**RenderThreadTime = 0 im PIE ist kein belastbarer Nullkosten-Nachweis; dort nicht interpretieren.** P95 je einzelner Messung steht im Rohdatenaudit `Measurements.json`. Frühere AfterA/AfterB/PairedA/PairedB beziehen sich auf einen verworfenen Import und sind von dieser Auswertung ausgeschlossen.','','## Finale zeitlich verschachtelte Paare','','Negative Differenz = V2 schneller. Drei Paare sind eine begrenzte Stichprobe, keine Signifikanzgarantie.','','| Reihe | Standort | V1 ms | V2 ms | Δ V2−V1 je Paar, ms | Median Δ ms |','|---|---|---:|---:|---|---:|']
for name in ['FinalPairedA','FinalPairedB','VillageA','VillageB','VillageC']:
 rows=data.get(name,[])
 for site in dict.fromkeys(r['site'] for r in rows):
  a=[r for r in rows if r['site']==site and r['condition']=='V1'];b=[r for r in rows if r['site']==site and r['condition']=='V2']
  if len(a)!=3 or len(b)!=3:continue
  diffs=[next(r['median_ms'] for r in b if r['repeat']==i)-next(r['median_ms'] for r in a if r['repeat']==i) for i in [1,2,3]]
  out.append(f'| {name} | {site} | {med([r["median_ms"] for r in a]):.3f} | {med([r["median_ms"] for r in b]):.3f} | '+', '.join(f'{v:+.3f}' for v in diffs)+f' | {med(diffs):+.3f} |')
out+=['','## Einzelfaktoren – V1, jeweils scoped zurückgesetzt','','| Standort | Faktor | Kontroll-ms | Varianten-ms | Median Δ ms | Δ der zwei Paare | GPU Δ ms |','|---|---|---:|---:|---:|---|---:|']
for name in ['Factors_Dorf','Factors_Wald','Factors_Weg','Factors_Village']:
 rows=data.get(name,[])
 for condition in dict.fromkeys(r['condition'] for r in rows if r['condition']!='V1'):
  pairs=[(next(x for x in rows if x['segment']==r['segment']-1),r) for r in rows if r['condition']==condition];diff=[b['median_ms']-a['median_ms'] for a,b in pairs];gpu=[b['csv']['GPUTime']['median']-a['csv']['GPUTime']['median'] for a,b in pairs if 'GPUTime' in b.get('csv',{}) and 'GPUTime' in a.get('csv',{})]
  out.append(f'| {pairs[0][0]["site"]} | {condition} | {med([a["median_ms"] for a,b in pairs]):.3f} | {med([b["median_ms"] for a,b in pairs]):.3f} | {med(diff):+.3f} | '+', '.join(f'{v:+.3f}' for v in diff)+' | '+(f'{med(gpu):+.3f}' if gpu else 'offen')+' |')
(O/'FinalMetricTables.md').write_text('\n'.join(out)+'\n')
