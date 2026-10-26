"""Summarize native profiler evidence; never substitutes invented timings."""
from pathlib import Path
import csv,json,statistics as st,math
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/DayNightV1';out=[]
def summary(a):
 a=sorted(a)
 return {'n':len(a),'median':st.median(a),'p95':a[min(len(a)-1,math.ceil(.95*len(a))-1)],'min':a[0],'max':a[-1]}
labels=['Original01','NoonB7502','OriginalControl02','NoonC8502','Dawn02','Dusk02','Night02','MovingNoonB7502']
for label in labels:
 stem='VGB1_DayNight_'+label;done=R/'Saved/EnvironmentPerfV2'/(stem+'_Done.txt')
 assert done.read_text()=='Complete',stem
 frames=list(csv.DictReader((R/'Saved/EnvironmentPerfV2'/(stem+'_Frames.csv')).open()))
 segments=list(csv.DictReader((R/'Saved/EnvironmentPerfV2'/(stem+'_Segments.csv')).open()))
 assert len(segments)==6
 for seg in segments:
  i=int(seg['segment']);ff=[r for r in frames if int(r['segment'])==i];assert ff
  for f in ff:
   assert all(int(f[k])==v for k,v in [('viewport_w',2560),('viewport_h',1440),('internal_w',2560),('internal_h',1440),('quality',2),('actual_aa_method',2)])
   assert abs(float(f['pitch'])+50)<.01 and abs(float(f['yaw'])+45)<.01 and abs(float(f['fov'])-35)<.01
  p=R/'Saved/Profiling/CSV'/('ENV2_'+stem+'_%03d.csv'%i)
  raw=list(csv.DictReader(p.open()));gpu={}
  for k in ['GPUTime','GPU/ShadowDepths','GPU/ShadowProjection','GPU/DistanceFieldShadows']:
   a=[]
   for r in raw:
    try:v=float(r[k])
    except (ValueError,TypeError,KeyError):continue
    if math.isfinite(v)and v>=0:a.append(v)
   assert a,(label,k);gpu[k]=summary(a)
  out.append({'label':label,'site':seg['site'],'repeat':int(seg['repeat']),'frames':summary([float(x['frame_ms'])for x in ff]),'gpu':gpu})
rows=[]
for label in labels:
 for site in ['Dorf','Wald']:
  a=[r for r in out if r['label']==label and r['site']==site];med=[x['frames']['median']for x in a];g=[x['gpu']['GPUTime']['median']for x in a];shadow=[sum(x['gpu'][k]['median']for k in ['GPU/ShadowDepths','GPU/ShadowProjection','GPU/DistanceFieldShadows'])for x in a]
  rows.append({'condition':label,'site':site,'repeats':3,'frame_median_ms':st.median(med),'frame_repeat_range_ms':[min(med),max(med)],'fps_from_frame_median':1000/st.median(med),'frame_p95_ms':st.median([x['frames']['p95']for x in a]),'gpu_median_ms':st.median(g),'gpu_repeat_range_ms':[min(g),max(g)],'shadow_sum_medians_ms':st.median(shadow)})
v={'method':'Two identical QHD High/TAA2 normal-camera sites, three 5-second samples each after 3-second warmup. Median of repetition medians. Shadow total is sum of recorded GPU scope medians, not exclusive frame budget. Uncontrolled OS/thermal/AI variation retained.','segments':out,'conditions':rows};(D/'PerformanceSummary.json').write_text(json.dumps(v,indent=2))
for x in rows:print(x)
