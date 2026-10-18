"""Strict actual-AA/resolution/CSV checks. No missing GPU value is estimated."""
from pathlib import Path
import json,csv,re,statistics,sys
from collections import defaultdict
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';P=R/'Saved/EnvironmentPerfV2'
src=(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py').read_text();src=src.replace("r'VGB1_Final_(PIE|Standalone)_(Base_[1-8]|FactorsWald|FactorsPost|FactorsAA|Confirm)_Frames'","r'VGB1_Vegetation_(PIE|Standalone)_C(Scout|Recheck1|[1-8])_Frames'").replace('Saved/VisualV2GPUBottleneckV1/Measurements.json','Saved/VisualV2VegetationPerfV1/Measurements.json');ns={'__file__':str(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py'),'__name__':'decoder'};exec(compile(src,'existing_csv_decoder','exec'),ns);data=ns['summarize']();groups=defaultdict(list);allrows=[];photoproofs=[]
for label,rows in data.items():
 done=P/(label+'_Done.txt')
 if not done.exists():continue
 assert done.read_text()=='Complete'
 if label=='VGB1_Vegetation_PIE_C1':continue # Entire group remeasured after concurrent source-atlas CPU analysis.
 plan=list(csv.reader((R/'Tools/VisualV2VegetationPerfV1/Plans'/(label+'.tsv')).open(),delimiter='\t'))[1:];assert len(rows)==len(plan),(label,len(rows),len(plan))
 raw=list(csv.DictReader((P/(label+'_Frames.csv')).open()))
 for x in rows:
  row=plan[x['segment']];w,h,q,sp=map(int,row[3:]);rs=[a for a in raw if int(a['segment'])==x['segment']]
  assert {int(a['actual_aa_method']) for a in rs}=={2},(label,x['segment'],'AA')
  assert x['extent']==[(w,h,w,h,w,h,(w*sp+99)//100,(h*sp+99)//100)],(label,x['segment'],x['extent'])
  assert x['fractions']==[(sp/100,1.)] and x['resolution_samples_increment']>0
  if int(x['repeat'])>=90:continue
  assert x.get('active_window_fraction')==1,(label,x['segment'],'Inactive measurement window')
  assert x['samples']>=20 and x.get('csv',{}).get('GPUTime',{}).get('median',0)>0,(label,x['segment'],'CSV GPU')
  for n,v in [('pitch',-50),('yaw',-45),('fov',35)]:assert max(abs(a-v) for a in x['camera'][n])<.001
  x.update(label=label,mode='PIE' if '_PIE_' in label else 'Standalone',width=w,height=h)
  allrows.append(x)
  if 'Scout' not in label:groups[(x['mode'],w,h,q,sp,x['site'],x['condition'])].append(x)
 settings=(P/(label+'_Settings.txt')).read_text();slot_counts=list(map(int,re.findall(r'vegetation_candidate_slots=(\d+)',settings)));assert len(slot_counts)==len(plan);blocks=settings.split('segment=')[1:]
 for block in blocks:
  i=int(block.split()[0]);q=int(plan[i][5]);expected={'r.AntiAliasingMethod':2,'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4 if q==1 else 8,'r.Lumen.FinalGatherMethod':0 if q==1 else 1,'r.Lumen.Reflections.Allow':0 if q==1 else 1,'r.VSync':0,'t.MaxFPS':0,'r.DynamicRes.OperationMode':0}
  for n,v in expected.items():
   match=re.search(r'^'+re.escape(n)+r'=([^ ]+)',block,re.M);assert match and float(match[1])==v,(label,i,n)
  if plan[i][1]=='VegPerf:FullyRough':
   assert slot_counts[i]==87,(label,i,'Expected 41 crown + 46 bush components')
 review=json.loads((S/(label+'_Review.json')).read_text());assert not review['error']
 for p in review['captures']:
  fs=list(Path(p['file_request']).parent.glob(Path(p['file_request']).stem+'*.png'));assert len(fs)==1;p['file']=str(fs[0]);p['label']=label;photoproofs.append(p)
 for site in {x['site'] for x in review['captures']}:
  ps=[p for p in review['captures'] if p['site']==site];a=ps[0]
  for b in ps[1:]:
   for key in ['camera','rotation']:assert max(abs(u-v) for u,v in zip(a[key],b[key]))<.001
   assert a['fov']==b['fov'];assert a['lights']==b['lights'] and a['shadows']==b['shadows']
   assert a['pp']==b['pp'],'Non-AA postprocess changed'
summary=[]
for key,rs in sorted(groups.items()):
 assert len(rs)==3,(key,len(rs));mode,w,h,q,sp,site,condition=key;ms=statistics.median(x['median_ms'] for x in rs)
 summary.append({'mode':mode,'width':w,'height':h,'quality':q,'percentage':sp,'site':site,'condition':condition,'fps':1000/ms,'median_ms':ms,'p95_ms':statistics.median(x['p95_ms'] for x in rs),'individual_ms':[x['median_ms'] for x in rs],'individual_gpu':[x['csv']['GPUTime']['median'] for x in rs],'csv':{n:statistics.median(x['csv'][n]['median'] for x in rs if n in x['csv']) for n in set().union(*(x['csv'] for x in rs))}})
scout=[]
for label,rs in data.items():
 if 'Scout' not in label or not (P/(label+'_Done.txt')).exists():continue
 for i in range(0,18,2):
  pair=rs[i:i+2];a=next(x for x in pair if x['condition']=='VegPerf:Control');b=next(x for x in pair if x!=a);scout.append({'candidate':b['condition'],'repeat':b['repeat'],'control_ms':a['median_ms'],'candidate_ms':b['median_ms'],'delta_ms':b['median_ms']-a['median_ms'],'control_gpu':a['csv']['GPUTime']['median'],'candidate_gpu':b['csv']['GPUTime']['median'],'delta_gpu':b['csv']['GPUTime']['median']-a['csv']['GPUTime']['median']})
if '--final' in sys.argv:assert len(summary)==96 and len(allrows)==306,(len(summary),len(allrows))
for name,value in [('Summary.json',summary),('Validation.json',{'regular_segments':len(allrows),'three_run_groups':len(summary),'rows':allrows,'all_completed':len(summary)==96}),('Scout.json',scout),('Photos.json',photoproofs)]: (S/name).write_text(json.dumps(value,indent=2))
print('Validated',len(allrows),'segments',len(summary),'three-run groups',len(photoproofs),'photos')
for factor in sorted({x['candidate'] for x in scout}):
 rr=[x for x in scout if x['candidate']==factor];print(factor,'GPU deltas',[round(x['delta_gpu'],3) for x in rr],'median',round(statistics.median(x['delta_gpu'] for x in rr),3))
