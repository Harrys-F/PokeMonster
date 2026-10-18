"""Validate actual per-view AA, dimensions, unchanged illumination and paired timings."""
from pathlib import Path
import csv,json,re,statistics,sys,struct
from collections import defaultdict
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2TAAIntegrationV1';P=R/'Saved/EnvironmentPerfV2';source=(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py').read_text();old="r'VGB1_Final_(PIE|Standalone)_(Base_[1-8]|FactorsWald|FactorsPost|FactorsAA|Confirm)_Frames'";assert old in source;source=source.replace(old,"r'VGB1_TAAIntegration_(PIE|Standalone)_C([1-6]|Recheck[2-5])_Frames'").replace('Saved/VisualV2GPUBottleneckV1/Measurements.json','Saved/VisualV2TAAIntegrationV1/Measurements.json');ns={'__file__':str(R/'Tools/VisualV2GPUBottleneckV1/Summarize.py'),'__name__':'verified_existing_csv_decoder'};exec(compile(source,'existing_csv_decoder','exec'),ns);data=ns['summarize']();partial='--partial' in sys.argv;groups=defaultdict(list);validated=[];photos=[]
for label,rows in data.items():
 if not (P/(label+'_Done.txt')).exists():continue
 assert (P/(label+'_Done.txt')).read_text()=='Complete';plan=[x.split('\t') for x in (R/'Tools/VisualV2TAAIntegrationV1/Plans'/(label+'.tsv')).read_text().splitlines()[1:]];m=re.fullmatch('VGB1_TAAIntegration_(PIE|Standalone)_C([1-6]|Recheck[2-5])',label);assert m and len(plan)==len(rows)
 raw=list(csv.DictReader((P/(label+'_Frames.csv')).open()))
 for row in rows:
  if m[1]=='Standalone' and m[2] in ['2','3','4','5'] and row['site']=='Weg' and int(row['repeat'])<90:continue # Whole paired groups replaced by independently complete rechecks.
  e=plan[row['segment']];w,h,q,sp=map(int,e[3:]);wanted=4 if e[1]=='MapTAA:TSR' else 2;rs=[x for x in raw if int(x['segment'])==row['segment']]
  if label=='VGB1_TAAIntegration_PIE_C1' and int(row['repeat'])>=90:continue # Diagnosed invalid initial photographs; preserve and replace separately.
  assert {int(x['actual_aa_method']) for x in rs}=={wanted},(label,row['segment'],'Actual renderer AA mismatch')
  assert row['extent']==[(w,h,w,h,w,h,(w*sp+99)//100,(h*sp+99)//100)],(label,row['segment'],row['extent']);assert row['fractions']==[(sp/100,1.)] and row['resolution_samples_increment']>0
  if int(row['repeat'])>=90:continue
  assert row['samples']>=20 and row['csv']['GPUTime']['median']>0 and row['csv']['GPUTime']['samples']>=20
  for n,v in [('pitch',-50),('yaw',-45),('fov',35)]:assert max(abs(x-v) for x in row['camera'][n])<.001
  row.update(label=label,mode=m[1],width=w,height=h,config=int(m[2].removeprefix('Recheck')),actual_aa=wanted);validated.append(row);groups[(m[1],w,h,q,sp,row['site'],e[1])].append(row)
 blocks=(P/(label+'_Settings.txt')).read_text().split('segment=')[1:]
 for block in blocks:
  i=int(block.split()[0]);q=int(plan[i][5]);expected={'r.AntiAliasingMethod':4,'r.Lumen.ScreenProbeGather.IntegrateDownsampleFactor':1,'r.Shadow.Virtual.SMRT.RayCountDirectional':4 if q==1 else 8,'r.Lumen.FinalGatherMethod':0 if q==1 else 1,'r.Lumen.Reflections.Allow':0 if q==1 else 1,'r.VSync':0,'t.MaxFPS':0,'r.DynamicRes.OperationMode':0}
  for n,v in expected.items():
   match=re.search(r'^'+re.escape(n)+r'=([^ ]+)',block,re.M);assert match and float(match[1])==v,(label,i,n)
 review_label='VGB1_TAAIntegration_PIE_CPhotoC1' if label=='VGB1_TAAIntegration_PIE_C1' else label
 if partial and not (S/(review_label+'_Review.json')).exists():review={'captures':[],'error':None}
 else:review=json.loads((S/(review_label+'_Review.json')).read_text())
 if label=='VGB1_TAAIntegration_PIE_C1' and (S/(review_label+'_Review.json')).exists():
  rr=list(csv.DictReader((P/(review_label+'_Frames.csv')).open()))
  assert all(tuple(int(r[k]) for k in ['viewport_w','viewport_h','target_w','target_h','view_w','view_h','internal_w','internal_h'])==(1280,720,1280,720,1280,720,960,540) and float(r['primary_fraction'])==.75 and float(r['secondary_fraction'])==1 for r in rr)
  for factor in ['MapTAA:TSR','MapTAA:Native']:
   assert {int(r['actual_aa_method']) for r in rr if r['condition']==factor}=={4 if factor.endswith('TSR') else 2}
 assert not review['error'];assert (partial and label=='VGB1_TAAIntegration_PIE_C1' and not review['captures']) or len(review['captures'])==(8 if m[2] in ['1','6'] else 0)
 clean=lambda x:re.sub('0x[0-9a-fA-F]+','<address>',json.dumps(x,sort_keys=True))
 for p in review['captures']:
  fs=list(Path(p['file_request']).parent.glob(Path(p['file_request']).stem+'*.png'));assert len(fs)==1;f=fs[0];assert list(struct.unpack('>II',f.read_bytes()[16:24]))==p['viewport']==p['config'][:2];p.update(file=str(f),label=label,mode=m[1]);photos.append(p)
 for site in {x['site'] for x in review['captures']}:
  a,b=[x for x in review['captures'] if x['site']==site]
  for key in ['camera','rotation']:assert max(abs(x-y) for x,y in zip(a[key],b[key]))<.001,(label,site,key)
  assert abs(a['fov']-b['fov'])<.0001
  for key in ['lights','shadows']:assert clean(a[key])==clean(b[key]),(label,site,key)
  for av,bv in zip(a['pp'],b['pp']):assert av['name']==bv['name'] and av['without_blendables']==bv['without_blendables'],(label,site,'non-AA postprocess')
summary=[]
for key,rs in sorted(groups.items()):
 assert len(rs)==3;mode,w,h,q,sp,site,condition=key;ms=statistics.median(x['median_ms'] for x in rs);summary.append({'mode':mode,'width':w,'height':h,'quality':q,'percentage':sp,'site':site,'condition':condition,'actual_aa':rs[0]['actual_aa'],'fps':1000/ms,'median_ms':ms,'p95_ms':statistics.median(x['p95_ms'] for x in rs),'individual_ms':[x['median_ms'] for x in rs],'individual_gpu':[x['csv']['GPUTime']['median'] for x in rs],'csv':{n:statistics.median(x['csv'][n]['median'] for x in rs if n in x['csv']) for n in set().union(*(x['csv'] for x in rs))},'camera':rs[0]['camera']})
if not partial:assert len(validated)==216 and len(summary)==72 and len(photos)==32
for name,value in [('Summary.json',summary),('Validation.json',{'recorded_regular_segments':sum(int(r['repeat'])<90 for rs in data.values() for r in rs),'excluded_original_regular_segments':24,'replacement_groups':['Standalone C2 Weg','Standalone C3 Weg','Standalone C4 Weg','Standalone C5 Weg'],'segments':len(validated),'summaries':len(summary),'photos':len(photos),'actual_renderer_aa_verified':True,'rows':validated}),('Photos.json',photos)]: (S/name).write_text(json.dumps(value,indent=2))
print('VALIDATED',len(validated),'segments',len(summary),'three-run groups',len(photos),'photos')
