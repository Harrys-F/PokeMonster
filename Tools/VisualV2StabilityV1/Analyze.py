"""Derive timings only from captured native frames/CSV. Keep uncertainty explicit."""
from pathlib import Path
import csv,json,statistics as st,math
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';segments=[];conditions=[]
def nums(rows,k):
 a=[]
 for r in rows:
  try:v=float(r[k])
  except (ValueError,KeyError,TypeError):continue
  if math.isfinite(v)and v>=0:a.append(v)
 return a
for p in sorted(D.glob('*/Result.json')):
 q=json.loads(p.read_text())
 if not q.get('passed')or'cases'not in q:continue
 for case in q['cases']:
  label=case['label'];fs=list(csv.DictReader((R/'Saved/EnvironmentPerfV2'/(label+'_Frames.csv')).open()));ss=list(csv.DictReader((R/'Saved/EnvironmentPerfV2'/(label+'_Segments.csv')).open()));group=[]
  for seg in ss:
   i=int(seg['segment']);ff=[f for f in fs if int(f['segment'])==i];assert ff
   for f in ff:
    assert all(int(f[k])==v for k,v in [('viewport_w',2560),('viewport_h',1440),('internal_w',2560),('internal_h',1440),('quality',2),('percentage',100),('actual_aa_method',2)]),(label,f)
    assert abs(float(f['pitch'])+50)<.01 and abs(float(f['yaw'])+45)<.01 and abs(float(f['fov'])-35)<.01
   raw=list(csv.DictReader((R/'Saved/Profiling/CSV'/('ENV2_'+label+'_%03d.csv'%i)).open()));frame=nums(ff,'frame_ms');row={'label':label,'site':seg['site'],'repeat':int(seg['repeat']),'frame_n':len(frame),'mean_frame_ms':st.mean(frame),'gameplay_fps':1000/st.mean(frame),'median_frame_ms':st.median(frame),'p95_frame_ms':sorted(frame)[min(len(frame)-1,math.ceil(.95*len(frame))-1)],'all_frames_qhd_high100_taa2':True,'all_frames_window_active':all(int(f['window_active'])==1 for f in ff)}
   for k in ['FrameTime','GPUTime','GameThreadTime','RenderThreadTime','RHIThreadTime','GPU/ShadowDepths','GPU/ShadowProjection','GPU/Lights','GPU/Basepass','PhysicalUsedMB','ExtendedUsedMB','Exclusive/RenderThread/RDG']:
    a=nums(raw,k);row[k]={'mean':st.mean(a),'median':st.median(a),'n':len(a)}if a else None
   # The native aggregate RT counter is zero in this engine build, despite measured RT scopes.
   rt=row['RenderThreadTime'];row['render_thread_aggregate_valid']=bool(rt and rt['mean']>.001)
   segments.append(row);group.append(row)
  for site in dict.fromkeys(r['site']for r in group):
   aa=[r for r in group if r['site']==site];row={'label':label,'site':site,'repeats':len(aa),'hour':case.get('hour'),'pokemon':case.get('pokemon',True),'mode':case.get('mode','none'),'frame_ms_mean_of_repeats':st.mean(a['mean_frame_ms']for a in aa),'frame_ms_range':[min(a['mean_frame_ms']for a in aa),max(a['mean_frame_ms']for a in aa)],'gameplay_fps_range':[min(a['gameplay_fps']for a in aa),max(a['gameplay_fps']for a in aa)]}
   for k in ['GPUTime','GameThreadTime','RenderThreadTime','Exclusive/RenderThread/RDG']:
    v=[a[k]['mean']for a in aa if a[k]];row[k+'_mean']=st.mean(v)if v else None;row[k+'_range']=[min(v),max(v)]if v else None
   conditions.append(row)
recordings=[]
for p in sorted((R/'Saved/VisualV2TAAIntegrationV1/Recordings').glob('*')):
 if not p.name.startswith(('CaptureBefore01_','CaptureAfter01_','StabilityStop','MotionPerformance01_','GameplayContinuous01'))or not(p/'Frames.csv').exists():continue
 a=list(csv.DictReader((p/'Frames.csv').open()));assert len(a)>1;game=nums(a,'game_seconds');wall=nums(a,'wall_seconds');assert all(b>a for a,b in zip(game,game[1:]));row={'name':p.name,'frames':len(a),'game_seconds':game[-1]-game[0],'wall_seconds':wall[-1]-wall[0],'capture_game_fps':(len(a)-1)/(game[-1]-game[0]),'capture_wall_fps':(len(a)-1)/(wall[-1]-wall[0]),'native_sizes':sorted(set((int(x['width']),int(x['height']))for x in a)),'original_timestamps':True,'interpolation':False}
 if(p/'Metrics.json').exists():row['metrics']=json.loads((p/'Metrics.json').read_text())
 recordings.append(row)
result={'method':'Standard plans: three 4-second samples after 2-second warmup. Short InterleavedMaterial plans: one 2-second sample after 1-second warmup per row; actual repeat counts retained. Exact rendered QHD/High2/100%/TAA2 asserted per frame. Actual presentation frame intervals, not requested recording rates. Thermal/OS/session differences retained. RenderThreadTime aggregate is unavailable/zero, not a valid claim of 0ms rendering. RDG is a partial CPU scope only.','segments':segments,'conditions':conditions,'recordings':recordings};(D/'MetricsSummary.json').write_text(json.dumps(result,indent=2));print('segments',len(segments),'conditions',len(conditions));print(json.dumps(conditions[:2],indent=2));print(json.dumps(recordings,indent=2))
