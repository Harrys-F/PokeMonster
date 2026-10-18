from pathlib import Path
import json,re,statistics
from collections import defaultdict
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2AASoftShadowsV1';src=(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py').read_text()
old="r'VGB1_Final_(PIE|Standalone)_(Base_[1-8]|FactorsWald|FactorsPost|FactorsAA|Confirm)_Frames'";src=src.replace(old,"r'VGB1_AASoftShadows_FinalFollow_(PIE|Standalone)_Frames'").replace('Saved/VisualV2GPUBottleneckV1/Measurements.json','Saved/VisualV2AASoftShadowsV1/FinalFollowMeasurements.json');ns={'__name__':'follow_decoder','__file__':str(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py')};exec(compile(src,'tracked_decoder_adapter','exec'),ns);data=ns['summarize']();assert len(data)==2
summary=[]
for label,rows in data.items():
 assert (R/'Saved/EnvironmentPerfV2'/(label+'_Done.txt')).read_text()=='Complete';assert len(rows)==17
 groups=defaultdict(list)
 for r in rows:
  if int(r['repeat'])>=90:continue
  assert r['extent']==[(2560,1440,2560,1440,2560,1440,2560,1440)] and r['fractions']==[(1.,1.)] and r['samples']>=20 and r['resolution_samples_increment']>0
  groups[r['condition'].split(':')[1]].append(r)
 for v,rs in groups.items():
  assert len(rs)==3
  ms=statistics.median(r['median_ms'] for r in rs)
  summary.append({'mode':label.rsplit('_',1)[1],'variant':v,'fps':1000/ms,'median_ms':ms,'gpu_ms':statistics.median(r['csv']['GPUTime']['median'] for r in rs),'p95_ms':statistics.median(r['p95_ms'] for r in rs)})
 review=json.loads((S/(label+'_Review.json')).read_text());assert not review['error'] and len(review['captures'])==4
 base=review['captures'][0];clean=lambda v:re.sub(r'0x[0-9a-fA-F]+','<address>',json.dumps(v,sort_keys=True))
 for p in review['captures']:
  assert p['aa']==(2 if p['variant'].endswith(('B','D')) else 4)
  assert clean(p['lights'])==clean(base['lights']) and p['pp']==base['pp']
  assert max(abs(x-y) for x,y in zip(p['camera'],base['camera']))<.001
  assert len(p['decals'])==(50 if p['variant'].endswith(('C','D')) else 0)
(S/'FinalFollowSummary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
