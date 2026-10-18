"""Validate matching output/renderer fractions and produce measured A/B/C/D comparisons."""
from pathlib import Path
import csv,json,re,statistics,struct,sys
from collections import defaultdict
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2AASoftShadowsV1';P=R/'Saved/EnvironmentPerfV2'
source=(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py').read_text()
old="r'VGB1_Final_(PIE|Standalone)_(Base_[1-8]|FactorsWald|FactorsPost|FactorsAA|Confirm)_Frames'";assert old in source
source=source.replace(old,"r'VGB1_AASoftShadows_(PIE|Standalone)_C[1-8]_Frames'").replace('Saved/VisualV2GPUBottleneckV1/Measurements.json','Saved/VisualV2AASoftShadowsV1/Measurements.json')
ns={'__file__':str(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py'),'__name__':'aa_shadow_csv_decoder'};exec(compile(source,'tracked_decoder_adapter','exec'),ns);data=ns['summarize']();partial='--partial' in sys.argv
if not partial:assert len(data)==16
valid=[];groups=defaultdict(list);photos=[];errors=[]
for label,rows in data.items():
 if not (P/(label+'_Done.txt')).exists():continue
 assert (P/(label+'_Done.txt')).read_text()=='Complete'
 m=re.fullmatch(r'VGB1_AASoftShadows_(PIE|Standalone)_C([1-8])',label);assert m
 plan=[x.split('\t') for x in (R/'Tools/VisualV2AASoftShadowsV1/Plans'/(label+'.tsv')).read_text().splitlines()[1:]]
 assert len(rows)==len(plan),(label,len(rows),len(plan));assert len({tuple(x[3:]) for x in plan})==1
 blocks=(P/(label+'_Settings.txt')).read_text().split('segment=')[1:]
 for block in blocks:
  i=int(block.split()[0]);q=int(plan[i][5]);v=plan[i][1].split(':')[1]
  expected={'r.AntiAliasingMethod':2 if v in ['B','D'] else 4,'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4 if q==1 else 8,'r.Lumen.FinalGatherMethod':0 if q==1 else 1,'r.Lumen.Reflections.Allow':0 if q==1 else 1,'r.VSync':0,'t.MaxFPS':0,'r.DynamicRes.OperationMode':0}
  for n,value in expected.items():
   mm=re.search(r'^'+re.escape(n)+r'=([^ ]+)',block,re.M);assert mm and float(mm[1])==value,(label,i,n,mm[1] if mm else None)
 for row in rows:
  if int(row['repeat'])>=90:continue
  e=plan[row['segment']];w,h,q,sp=map(int,e[3:]);expected=[w,h,w,h,w,h,(w*sp+99)//100,(h*sp+99)//100]
  assert row['extent']==[tuple(expected)],(label,row['segment'],row['extent'],expected)
  assert row['fractions']==[(sp/100,1.0)] and row['resolution_samples_increment']>0 and row['samples']>=20
  assert row.get('csv',{}).get('GPUTime',{}).get('median',0)>0
  for n,value in [('pitch',-50),('yaw',-45),('fov',35)]:assert max(abs(x-value) for x in row['camera'][n])<.001
  variant=row['condition'].split(':')[1];row.update(label=label,variant=variant,mode=m[1],width=w,height=h,config=int(m[2]));valid.append(row);groups[(variant,m[1],w,h,q,sp,row['site'])].append(row)
 review_file=S/(label+'_Review.json')
 if review_file.exists():review=json.loads(review_file.read_text())
 else:
  assert m[2] not in ['1','8'],'Missing required photograph manifest'
  review={'captures':[],'error':None,'source':'No photographs requested in this completed timing-only plan'}
 assert not review['error']
 assert len(review['captures'])==(16 if m[2] in ['1','8'] else 0),(label,len(review['captures']))
 for p in review['captures']:
  files=list(Path(p['requested_file']).parent.glob(Path(p['requested_file']).stem+'*.png'));assert len(files)==1,(label,files);f=files[0]
  dims=struct.unpack('>II',f.read_bytes()[16:24]);assert list(dims)==p['viewport']==p['config'][:2]
  assert sum(b['instances'] for b in p['bushes'])==58
  p.update(file=str(f),label=label,mode=m[1],config_id=int(m[2]));photos.append(p)
 # Each scene's camera, all light parameters and complete postprocess structs must match.
 for site in set(p['site'] for p in review['captures']):
  records=[p for p in review['captures'] if p['site']==site];base=next(p for p in records if p['variant']=='SoftAA:A')
  for p in records:
   for key in ['camera','rotation','fov','lights','pp']:
    if key=='camera':assert max(abs(a-b) for a,b in zip(p[key],base[key]))<.001,(label,site,key)
    else:
     clean=lambda v:re.sub(r'0x[0-9a-fA-F]+','<address>',json.dumps(v,sort_keys=True))
     assert clean(p[key])==clean(base[key]),(label,site,key)
summary=[]
for key,rows in sorted(groups.items()):
 assert len(rows)==3,(key,len(rows));variant,mode,w,h,q,sp,site=key;ms=statistics.median(r['median_ms'] for r in rows)
 summary.append({'variant':variant,'mode':mode,'width':w,'height':h,'quality':q,'percentage':sp,'site':site,'fps':1000/ms,'median_ms':ms,'p95_ms':statistics.median(r['p95_ms'] for r in rows),'individual_ms':[r['median_ms'] for r in rows],'individual_gpu':[r['csv']['GPUTime']['median'] for r in rows],'csv':{n:statistics.median(r['csv'][n]['median'] for r in rows if n in r['csv']) for n in set().union(*(r['csv'] for r in rows))},'camera':rows[0]['camera']})
lookup={(r['variant'],r['mode'],r['width'],r['height'],r['quality'],r['percentage'],r['site']):r for r in summary};comparisons=[]
for row in summary:
 if row['variant']=='A':continue
 base=lookup[('A',row['mode'],row['width'],row['height'],row['quality'],row['percentage'],row['site'])]
 for n in ['camera_x','camera_y','camera_z']:assert max(abs(a-b) for a,b in zip(base['camera'][n],row['camera'][n]))<.01
 comparisons.append({k:row[k] for k in ['variant','mode','width','height','quality','percentage','site']}|{'baseline_fps':base['fps'],'candidate_fps':row['fps'],'baseline_ms':base['median_ms'],'candidate_ms':row['median_ms'],'delta_ms':row['median_ms']-base['median_ms'],'baseline_gpu':base['csv']['GPUTime'],'candidate_gpu':row['csv']['GPUTime'],'delta_gpu':row['csv']['GPUTime']-base['csv']['GPUTime'],'baseline_p95':base['p95_ms'],'candidate_p95':row['p95_ms']})
if not partial:assert len(valid)==576 and len(summary)==192 and len(photos)==64
for name,d in [('Validation.json',{'regular_segments':len(valid),'photos':len(photos),'rows':valid}),('Summary.json',summary),('Comparison.json',comparisons),('Photos.json',photos)]: (S/name).write_text(json.dumps(d,indent=2))
if comparisons:
 with (S/'Comparison.csv').open('w') as f:
  writer=csv.DictWriter(f,fieldnames=list(comparisons[0]));writer.writeheader();writer.writerows(comparisons)
print('VALIDATED',len(valid),'segments;',len(summary),'three-run summaries;',len(photos),'photos')
