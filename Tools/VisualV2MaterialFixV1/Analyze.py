"""Validate current measurements, excluding all photograph and drain rows.
Before/after is sequential, not interleaved; native image content intentionally differs.
"""
from pathlib import Path
import csv,json,re,statistics,struct
from collections import defaultdict
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2MaterialFixV1';P=R/'Saved/EnvironmentPerfV2'
# Use the tracked CSV decoder without creating dependencies on old local reviews.
source=(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py').read_text()
old="r'VGB1_Final_(PIE|Standalone)_(Base_[1-8]|FactorsWald|FactorsPost|FactorsAA|Confirm)_Frames'"
assert old in source
source=source.replace(old,"r'VGB1_MaterialFix_(Before|After)_(PIE|Standalone)_C[1-8]_Frames'")
source=source.replace("Saved/VisualV2GPUBottleneckV1/Measurements.json","Saved/VisualV2MaterialFixV1/Measurements.json")
ns={'__file__':str(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py'),'__name__':'vmf_csv_decoder'};exec(compile(source,'tracked_Summarize_adapter','exec'),ns);data=ns['summarize']();assert len(data)==32
valid=[];groups=defaultdict(list);photos=[]
for label,rows in data.items():
 m=re.fullmatch(r'VGB1_MaterialFix_(Before|After)_(PIE|Standalone)_C([1-8])',label);assert m
 assert (P/(label+'_Done.txt')).read_text()=='Complete'
 plan=[x.split('\t') for x in (R/'Tools/VisualV2MaterialFixV1/Plans'/(label+'.tsv')).read_text().splitlines()[1:]]
 assert len(rows)==len(plan),(label,len(rows),len(plan));assert len({tuple(x[3:]) for x in plan})==1,'No live scalability switches'
 settings=(P/(label+'_Settings.txt')).read_text();blocks=settings.split('segment=')[1:]
 for block in blocks:
  i=int(block.split()[0]);q=int(plan[i][5]);expected={'r.AntiAliasingMethod':4,'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4 if q==1 else 8,'r.Lumen.FinalGatherMethod':0 if q==1 else 1,'r.Lumen.Reflections.Allow':0 if q==1 else 1,'r.VSync':0,'t.MaxFPS':0,'r.DynamicRes.OperationMode':0}
  for n,v in expected.items():
   match=re.search(r'^'+re.escape(n)+r'=([^ ]+)',block,re.M);assert match and float(match[1])==v,(label,i,n,match[1] if match else None)
 for row in rows:
  if int(row['repeat'])>=90:continue
  e=plan[row['segment']];w,h,q,sp=map(int,e[3:]);expected=[w,h,w,h,w,h,(w*sp+99)//100,(h*sp+99)//100]
  assert row['extent']==[tuple(expected)],(label,row['extent']);assert row['fractions']==[(sp/100,1.0)]
  assert row['resolution_samples_increment']>0 and row['samples']>=20
  assert row.get('csv',{}).get('GPUTime',{}).get('median',0)>0,(label,row['segment'],'GPU unavailable')
  for n,v in [('pitch',-50),('yaw',-45),('fov',35)]:assert max(abs(x-v) for x in row['camera'][n])<.001
  row.update(label=label,phase=m[1],mode=m[2],width=w,height=h,config=int(m[3]));valid.append(row);groups[(m[1],m[2],w,h,q,sp,row['site'])].append(row)
 review=json.loads((S/(label+'_Review.json')).read_text());assert not review['error'];assert len(review['captures'])==(3 if m[3]=='8' else 1)
 for p in review['captures']:
  files=list(Path(p['requested_file']).parent.glob(Path(p['requested_file']).stem+'*.png'));assert len(files)==1,(label,files);f=files[0];head=f.read_bytes()[:24];dims=struct.unpack('>II',head[16:24]);assert list(dims)==p['viewport']==p['config'][:2];assert sum(b['instances'] for b in p['bushes'])==58
  p.update(file=str(f),label=label,phase=m[1],mode=m[2],config_id=int(m[3]));photos.append(p)
assert len(valid)==288 and len(photos)==40
summary=[]
for key,rows in sorted(groups.items()):
 assert len(rows)==3,(key,len(rows));phase,mode,w,h,q,sp,site=key;ms=statistics.median(r['median_ms'] for r in rows)
 summary.append({'phase':phase,'mode':mode,'width':w,'height':h,'quality':q,'percentage':sp,'site':site,'fps':1000/ms,'median_ms':ms,'p95_ms':statistics.median(r['p95_ms'] for r in rows),'individual_ms':[r['median_ms'] for r in rows],'csv':{n:statistics.median(r['csv'][n]['median'] for r in rows if n in r['csv']) for n in set().union(*(r['csv'] for r in rows))},'camera':rows[0]['camera']})
lookup={(r['phase'],r['mode'],r['width'],r['height'],r['quality'],r['percentage'],r['site']):r for r in summary};comparisons=[]
for row in summary:
 if row['phase']!='After':continue
 before=lookup[('Before',row['mode'],row['width'],row['height'],row['quality'],row['percentage'],row['site'])]
 for name in ['camera_x','camera_y','camera_z']:
  assert max(abs(a-b) for a,b in zip(before['camera'][name],row['camera'][name]))<.05,(row,name,before['camera'][name],row['camera'][name])
 comparisons.append({'mode':row['mode'],'width':row['width'],'height':row['height'],'quality':row['quality'],'percentage':row['percentage'],'site':row['site'],'before_fps':before['fps'],'after_fps':row['fps'],'before_ms':before['median_ms'],'after_ms':row['median_ms'],'delta_ms':row['median_ms']-before['median_ms'],'before_p95':before['p95_ms'],'after_p95':row['p95_ms'],'before_gpu':before['csv']['GPUTime'],'after_gpu':row['csv']['GPUTime'],'delta_gpu':row['csv']['GPUTime']-before['csv']['GPUTime'],'before_game':before['csv'].get('GameThreadTime'),'after_game':row['csv'].get('GameThreadTime'),'before_render':before['csv'].get('RenderThreadTime'),'after_render':row['csv'].get('RenderThreadTime')})
for name,content in [('Validation.json',{'regular_segments':len(valid),'photo_frames':len(photos),'static_configs':32,'rows':valid}),('Summary.json',summary),('Comparison.json',comparisons),('Photos.json',photos)]: (S/name).write_text(json.dumps(content,indent=2))
with (S/'Comparison.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=list(comparisons[0]));writer.writeheader();writer.writerows(comparisons)
print('VALIDATED',len(valid),'regular segments,',len(summary),'three-run summaries,',len(photos),'actual screenshots')
