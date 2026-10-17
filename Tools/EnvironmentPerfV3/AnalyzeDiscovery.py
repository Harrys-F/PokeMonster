import json,statistics
from pathlib import Path
from Summarize import summarize
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';d=summarize().get('DiscoveryQHD',[]);out={}
for i in range(0,len(d)-1,2):
 a,b=d[i:i+2];c=a if a['condition']=='Control' else b;x=b if a['condition']=='Control' else a
 if c['condition']!='Control':continue
 row={'repeat':x['repeat'],'before_ms':c['median_ms'],'after_ms':x['median_ms'],'delta_ms':x['median_ms']-c['median_ms'],'control_p95':c['p95_ms'],'factor_p95':x['p95_ms']}
 for k in ['GPUTime','GameThreadTime','RenderThreadTime','GPU/Basepass','GPU/ShadowDepths','GPU/ShadowProjection','GPU/LumenIrradianceFieldGather']:
  if k in c.get('csv',{}) and k in x.get('csv',{}):row[k]={'before':c['csv'][k]['median'],'after':x['csv'][k]['median'],'delta':x['csv'][k]['median']-c['csv'][k]['median']}
 out.setdefault(x['condition'],[]).append(row)
(O/'DiscoveryPairs.json').write_text(json.dumps(out,indent=2))
for factor,rows in out.items():print(factor,'n',len(rows),'delta_ms',round(statistics.median(r['delta_ms'] for r in rows),3),'runs',[round(r['delta_ms'],3) for r in rows])
