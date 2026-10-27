"""Validate real per-view AA and paired 75% timing without mixing historical samples."""
from pathlib import Path
import csv,json,statistics as st,math
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/TSRComparisonC75';out=[]
def stats(xs):
 return {'mean':st.mean(xs),'median':st.median(xs),'p95':sorted(xs)[min(len(xs)-1,math.ceil(len(xs)*.95)-1)],'min':min(xs),'max':max(xs),'n':len(xs)}
for p in sorted(D.glob('*/Result.json')):
 q=json.loads(p.read_text())
 if 'cases'not in q:continue
 assert q['passed'],q
 DATA=Path(q['data_root'])
 for case in q['cases']:
  label=case['label'];frames=list(csv.DictReader((DATA/'EnvironmentPerfV2'/(label+'_Frames.csv')).open()));assert len(frames)>15
  wanted=4 if case['aa']=='TSR'else 2
  for f in frames:
   for k,v in {'viewport_w':2560,'viewport_h':1440,'target_w':2560,'target_h':1440,'view_w':2560,'view_h':1440,'internal_w':1920,'internal_h':1080,'actual_aa_method':wanted,'actual_upscale_method':1,'screen_percentage_showflag':1,'percentage':75,'quality':2,'window_active':1}.items():assert int(f[k])==v,(label,k,f[k])
   assert float(f['primary_fraction'])==.75 and float(f['secondary_fraction'])==1
  camera={k:[min(float(f[k])for f in frames),max(float(f[k])for f in frames)]for k in ['camera_x','camera_y','camera_z','pitch','yaw','fov']}
  for k,v in [('pitch',-50),('yaw',-45),('fov',35)]:assert max(abs(x-v)for x in camera[k])<.001
  raw=list(csv.DictReader((DATA/'Profiling/CSV'/('ENV2_'+label+'_000.csv')).open()));gpu={}
  for k in raw[0]:
   if not k or not(k.endswith('Time')or k.startswith('GPU/')):continue
   xs=[]
   for r in raw:
    try:x=float(r[k])
    except(ValueError,TypeError):continue
    if math.isfinite(x)and x>=0:xs.append(x)
   if xs:gpu[k]=stats(xs)
  frame=stats([float(f['frame_ms'])for f in frames]);out.append({'batch':p.parent.name,'mode':q['mode'],'case':case,'label':label,'aa':case['aa'],'site':case['site'],'camera':camera,'frame_ms':frame,'fps':1000/frame['mean'],'stats':gpu})
summary=[]
for mode,site,aa in dict.fromkeys((r['mode'],r['site'],r['aa'])for r in out):
 a=[r for r in out if(r['mode'],r['site'],r['aa'])==(mode,site,aa)];assert len(a)==3
 summary.append({'mode':mode,'site':site,'aa':aa,'fps':st.mean(r['fps']for r in a),'fps_range':[min(r['fps']for r in a),max(r['fps']for r in a)],'frame_ms':st.mean(r['frame_ms']['mean']for r in a),'p95_ms':st.mean(r['frame_ms']['p95']for r in a),'gpu_ms':st.mean(r['stats']['GPUTime']['mean']for r in a),'game_ms':st.mean(r['stats']['GameThreadTime']['mean']for r in a),'render_ms':st.mean(r['stats']['RenderThreadTime']['mean']for r in a),'frames':sum(r['frame_ms']['n']for r in a)})
for batch,pair in dict.fromkeys((r['batch'],r['case']['pair'])for r in out):
 a=[r for r in out if r['batch']==batch and r['case']['pair']==pair];assert len(a)==2 and {r['aa']for r in a}=={'TSR','TAAU'}
 for k in a[0]['camera']:assert abs(st.mean(a[0]['camera'][k])-st.mean(a[1]['camera'][k]))<.1,(batch,pair,k)
(D/'Measurements.json').write_text(json.dumps({'segments':out},indent=2));(D/'Summary.json').write_text(json.dumps({'rows':summary,'segments':len(out),'renderer_aa_verified':True},indent=2))
for r in summary:print(r['mode'],r['site'],r['aa'],'FPS',round(r['fps'],2),'GPU',round(r['gpu_ms'],2),'frame',round(r['frame_ms'],2),'range',r['fps_range'])
