"""Native wall-frame times plus available Unreal CSV counters. Zero RHI/Draw counters are not assumed valid."""
import csv,json,statistics,re
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV1'
def pct(a,p):
 s=sorted(a);v=(len(s)-1)*p;i=int(v);return s[i]+(s[min(i+1,len(s)-1)]-s[i])*(v-i)
def summarize():
 out={}
 for f in O.glob('VEQ1_*_Frames.csv'):
  if not re.fullmatch(r'VEQ1_(PIE|Standalone)_[1-6]_Frames',f.stem):continue
  rows=list(csv.DictReader(f.open()));groups={}
  for row in rows:groups.setdefault(row['segment'],[]).append(row)
  result=[]
  for seg,rs in groups.items():
   ms=[float(r['frame_ms']) for r in rs];a=rs[0];label=f.stem.removesuffix('_Frames');x={k:a[k] for k in ['site','condition','repeat','quality','percentage']};x.update(segment=int(seg),samples=len(ms),median_fps=1000/statistics.median(ms),median_ms=statistics.median(ms),p95_ms=pct(ms,.95),extent=sorted(set(tuple(int(r[k]) for k in ['viewport_w','viewport_h','target_w','target_h','view_w','view_h','internal_w','internal_h']) for r in rs)),window=sorted(set(tuple(float(r[k]) for k in ['window_slate_w','window_slate_h','window_dpi']) for r in rs)),fractions=sorted(set((float(r['primary_fraction']),float(r['secondary_fraction'])) for r in rs)),utc=[a['utc'],rs[-1]['utc']],camera={k:[min(float(r[k]) for r in rs),max(float(r[k]) for r in rs)] for k in ['camera_x','camera_y','camera_z','pitch','yaw','fov']})
   if 'window_active' in a:x['active_window_fraction']=sum(int(r['window_active']) for r in rs)/len(rs)
   c=R/'Saved/Profiling/CSV'/('ENV1_'+label+'_'+str(int(seg)).zfill(3)+'.csv')
   if c.exists():
    rr=list(csv.reader(c.open(encoding='utf-8-sig')));ends=[i for i,v in enumerate(rr) if v and v[0]=='EVENTS']
    if ends:
     end=max(ends);h=rr[end];d=rr[1:end];times={}
     for n in dict.fromkeys([n for n in h if n.startswith(('GPU/','DrawCall/'))]+['FrameTime','GameThreadTime','RenderThreadTime','RenderThreadTime_CriticalPath','GPUTime','RHIThreadTime','RHI/DrawCalls','RHI/PrimitivesDrawn','RHI/Triangles','MemoryFreeMB','Exclusive/GameThread/Animation']):
      if n not in h:continue
      j=h.index(n);v=[]
      for row in d:
       try:v.append(float(row[j]))
       except (ValueError,IndexError):pass
      if v:times[n]={'median':statistics.median(v),'p95':pct(v,.95),'all_zero':all(y==0 for y in v),'samples':len(v)}
     x['csv']=times
   result.append(x)
  out[label]=result
 (R/'Saved/VisualV2EnvironmentQualityV1/Measurements.json').write_text(json.dumps(out,indent=2));return out
if __name__=='__main__':
 for label,rows in summarize().items():
  print(label,len(rows))
  for r in rows:print(r['site'],r['condition'],r['repeat'],r['quality'],r['percentage'],round(r['median_fps'],2),round(r['p95_ms'],2))
