"""Three paired runs with exactly the same disabled shadow casters; only decal drawing differs."""
from pathlib import Path
import csv,json,statistics,re,sys
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2AASoftShadowsV1';src=(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py').read_text()
old="r'VGB1_Final_(PIE|Standalone)_(Base_[1-8]|FactorsWald|FactorsPost|FactorsAA|Confirm)_Frames'";src=src.replace(old,"r'VGB1_AASoftShadows_Cost_(PIE|Standalone)_Frames'").replace('Saved/VisualV2GPUBottleneckV1/Measurements.json','Saved/VisualV2AASoftShadowsV1/CostMeasurements.json')
ns={'__file__':str(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py'),'__name__':'cost_decoder'};exec(compile(src,'tracked_cost_decoder','exec'),ns);data=ns['summarize']();result=[]
for label,rows in data.items():
 assert (R/'Saved/EnvironmentPerfV2'/(label+'_Done.txt')).read_text()=='Complete'
 proof=json.loads((O/(label+'_Proof.json')).read_text());assert len(proof)==9
 for p in proof:
  if p['repeat']==99:continue
  assert p['owners']==1,(label,p)
  assert p['hidden']==(10<=p['repeat']<20 or p['repeat']==91)
 groups={False:[],True:[]}
 for r in rows:
  rep=int(r['repeat'])
  if rep>=90:continue
  assert r['fractions']==[(1.,1.)] and r['extent']==[(2560,1440,2560,1440,2560,1440,2560,1440)]
  assert r['samples']>=20 and r['csv']['GPUTime']['median']>0
  groups[rep>=10].append(r)
 assert len(groups[False])==len(groups[True])==3
 gpu={k:statistics.median(r['csv']['GPUTime']['median'] for r in rs) for k,rs in groups.items()};frame={k:statistics.median(r['median_ms'] for r in rs) for k,rs in groups.items()}
 pairs=[]
 for rep in range(3):
  visible=next(r for r in groups[False] if int(r['repeat'])==rep);hidden=next(r for r in groups[True] if int(r['repeat'])==rep+10)
  pairs.append({'repeat':rep,'delta_gpu_ms':visible['csv']['GPUTime']['median']-hidden['csv']['GPUTime']['median'],'delta_frame_ms':visible['median_ms']-hidden['median_ms']})
 result.append({'mode':label.rsplit('_',1)[1],'configuration':'2560x1440 High 100%','visible_gpu_ms':gpu[False],'hidden_gpu_ms':gpu[True],'gpu_difference_ms':gpu[False]-gpu[True],'visible_frame_ms':frame[False],'hidden_frame_ms':frame[True],'frame_difference_ms':frame[False]-frame[True],'pairs':pairs,'cost_interpretation':'Isolated drawing delta includes decal/compositing effects and measurement noise; not a hardware-kernel timer.'})
(O/'CostSummary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
