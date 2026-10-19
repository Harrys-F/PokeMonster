import csv,json,statistics,math
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster');P=R/'Saved/PerformanceRangerV2';O=R/'Art/Characters/NPCs/Ranger/Review/V2';out={}
def pct(a,p):
 s=sorted(a);x=(len(s)-1)*p;lo=int(x);return s[lo]+(s[min(lo+1,len(s)-1)]-s[lo])*(x-lo)
for f in P.glob('*_Frames.csv'):
 rows=list(csv.DictReader(f.open()));groups={};result=[]
 for row in rows:groups.setdefault(row['segment'],[]).append(row)
 for seg,rs in groups.items():
  ms=[float(r['frame_ms']) for r in rs];a=rs[0];x={'segment':int(seg),'site':a['site'],'condition':a['condition'],'repeat':int(a['repeat']),'samples':len(ms),'median_fps':1000/statistics.median(ms),'median_ms':statistics.median(ms),'p95_ms':pct(ms,.95),'extent':sorted(set((int(r['viewport_w']),int(r['viewport_h']),int(r['target_w']),int(r['target_h'])) for r in rs)),'percentage':sorted(set(float(r['screen_percentage']) for r in rs)),'lods':sorted(set(int(r['predicted_lod']) for r in rs)),'camera':{k:[min(float(r[k]) for r in rs),max(float(r[k]) for r in rs)] for k in ['camera_x','camera_y','camera_z','pitch','yaw','fov']},'utc':[a['utc'],rs[-1]['utc']]}
  label=f.stem.removesuffix('_Frames');c=R/'Saved/Profiling/CSV'/('RV2_'+label+'_'+str(int(seg)).zfill(3)+'.csv')
  if c.exists():
   rr=list(csv.reader(c.open(encoding='utf-8-sig')));end=max(i for i,v in enumerate(rr) if v and v[0]=='EVENTS');h=rr[end];d=rr[1:end];times={}
   for n in list(dict.fromkeys([n for n in h if n.startswith(('GPU/','DrawCall/'))]+['MemoryFreeMB','RenderThreadTime_CriticalPath','RHIThreadTime','RHI/PrimitivesDrawn','FrameTime','GameThreadTime','RenderThreadTime','GPUTime','RHI/DrawCalls','RHI/Triangles','GPU/ShadowDepths','GPU/ShadowProjection','GPU/Basepass','GPU/PostProcessing','GPU/Translucency','GPU/RenderDeferredLighting','Exclusive/GameThread/Animation'])):
    if n not in h:continue
    j=h.index(n);v=[]
    for row in d:
     try:v.append(float(row[j]))
     except (ValueError,IndexError):pass
    if v:times[n]={'median':statistics.median(v),'p95':pct(v,.95),'samples':len(v),'all_zero':all(z==0 for z in v)}
   x['csv']=times
  result.append(x)
 out[f.stem.removesuffix('_Frames')]=result
(O/'Measurements.json').write_text(json.dumps(out,indent=2))
for name,rs in out.items():
 print(name,[(r['site'],r['condition'],r['repeat'],round(r['median_fps'],2),round(r['p95_ms'],2),r['extent']) for r in rs])
