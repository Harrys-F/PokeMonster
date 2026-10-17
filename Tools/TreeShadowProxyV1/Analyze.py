"""Measured values only; refuses wrong resolution/pose, missing segments and GPU counters."""
import csv,json,statistics,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/TreeShadowProxyV1';N=R/'Saved/EnvironmentPerfV2';D=R/'Art/World/TreeShadowProxyV1/Review'
def pct(v,p):
 a=sorted(v);x=(len(a)-1)*p;i=int(x);return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)
def counters(p):
 a=list(csv.reader(p.open(encoding='utf-8-sig')));end=max(i for i,row in enumerate(a) if row and row[0]=='EVENTS');h=a[end];d=a[1:end];out={}
 for n in ['FrameTime','GameThreadTime','RenderThreadTime','GPUTime','GPU/ShadowDepths','GPU/ShadowProjection','GPU/SlateUI','GPU/Basepass','GPU/LumenScreenProbeGather','GPU/PostProcessing']:
  if n not in h:continue
  j=h.index(n);v=[]
  for row in d:
   try:v.append(float(row[j]))
   except (ValueError,IndexError):pass
  if v:out[n]={'median_ms':statistics.median(v),'p95_ms':pct(v,.95),'samples':len(v),'all_zero':all(x==0 for x in v)}
 return out
segments=[];table=[]
for i in range(1,7):
 label='TreeShadowProxyV1_C'+str(i);assert (N/(label+'_Done.txt')).read_text()=='Complete';control=json.loads((O/(label+'_Control.json')).read_text());assert not control['error'];meta=json.loads((O/(label+'_Rows.json')).read_text());data=list(csv.DictReader((N/(label+'_Frames.csv')).open()));rows=[]
 for seg,m in enumerate(meta):
  a=[x for x in data if int(x['segment'])==seg];assert len(a)>50,(label,seg,len(a));ext=set(tuple(int(r[k]) for k in ['viewport_w','viewport_h','target_w','target_h','view_w','view_h','internal_w','internal_h']) for r in a);w,h=m['width'],m['height'];f=m['percentage']/100
  assert ext=={(w,h,w,h,w,h,math.ceil(w*f),math.ceil(h*f))},ext
  assert set((r['primary_fraction'],r['secondary_fraction']) for r in a)=={(f'{f:.5f}','1.00000')};assert all(r['window_active']=='1' for r in a),'Unreal not foreground'
  camera=set(tuple(float(r[k]) for k in ['camera_x','camera_y','camera_z','pitch','yaw','fov']) for r in a);assert len(camera)==1 and next(iter(camera))[-3:]==(-50.,-45.,35.),camera
  ms=[float(r['frame_ms']) for r in a];x={'label':label,'segment':seg,**m,'frames':len(a),'median_frame_ms':statistics.median(ms),'p95_frame_ms':pct(ms,.95),'median_fps':1000/statistics.median(ms),'camera':list(next(iter(camera))),'actual_extents':list(next(iter(ext))),'window':sorted(set((r['window_slate_w'],r['window_slate_h'],r['window_dpi']) for r in a)),'counters':counters(R/'Saved/Profiling/CSV'/('ENV2_'+label+'_'+str(seg).zfill(3)+'.csv'))};rows.append(x);segments.append(x)
 assert len(rows)==6
 summary={k:meta[0][k] for k in ['width','height','quality','percentage']}
 for state in ['A','B']:
  rs=[x for x in rows if x['state']==state];assert sorted(x['repeat'] for x in rs)==[1,2,3];summary[state]={k:statistics.median(x[k] for x in rs) for k in ['median_frame_ms','p95_frame_ms','median_fps']}
  summary[state]['range_median_frame_ms']=[min(x['median_frame_ms'] for x in rs),max(x['median_frame_ms'] for x in rs)]
  for n in ['GPUTime','GameThreadTime','RenderThreadTime','GPU/ShadowDepths','GPU/ShadowProjection','GPU/SlateUI']:
   vals=[x['counters'][n]['median_ms'] for x in rs if n in x['counters'] and not x['counters'][n]['all_zero']];summary[state][n]=statistics.median(vals) if len(vals)==3 else None
 summary['paired_frame_delta_B_minus_A_ms']=[next(x for x in rows if x['repeat']==r and x['state']=='B')['median_frame_ms']-next(x for x in rows if x['repeat']==r and x['state']=='A')['median_frame_ms'] for r in [1,2,3]];table.append(summary)
D.mkdir(parents=True,exist_ok=True);(D/'Measurements.json').write_text(json.dumps({'segments':segments,'summary':table,'validation':'36 segments, three AB/BA pairs per configuration, native extents and fixed pose validated','internal_size':'Derived with ceil from native renderer resolution fractions; not allocation readback','mode':'Editor embedded PIE; no standalone measurement in this bounded group experiment','site':'Wald: Player (-4300,1550,50.15) cm'},indent=2))
for r in table:print(r['width'],r['height'],r['quality'],r['percentage'],'A/B ms',round(r['A']['median_frame_ms'],3),round(r['B']['median_frame_ms'],3),'GPU',r['A']['GPUTime'],r['B']['GPUTime'],'shadow',r['A']['GPU/ShadowDepths'],r['B']['GPU/ShadowDepths'],'paired delta',r['paired_frame_delta_B_minus_A_ms'])
