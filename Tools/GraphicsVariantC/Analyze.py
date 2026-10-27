"""Native per-frame timing validation; never infer an optimization from instruction count."""
from pathlib import Path
import csv,json,statistics as st,math,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GraphicsVariantC';out=[]
def values(rs,k):
 v=[]
 for r in rs:
  try:x=float(r[k])
  except(ValueError,KeyError,TypeError):continue
  if math.isfinite(x)and x>=0:v.append(x)
 return v
def summary(v):return {'mean':st.mean(v),'median':st.median(v),'stdev':st.pstdev(v),'p95':sorted(v)[min(len(v)-1,math.ceil(len(v)*.95)-1)],'min':min(v),'max':max(v),'n':len(v)}if v else None
for p in sorted(D.glob('*/Result.json')):
 q=json.loads(p.read_text())
 if not q.get('passed')or'cases'not in q:continue
 for case in q['cases']:
  label=case['label'];DATA=Path(q.get('data_root',str(R/'Saved')));fs=list(csv.DictReader((DATA/'EnvironmentPerfV2'/(label+'_Frames.csv')).open()));ss=list(csv.DictReader((DATA/'EnvironmentPerfV2'/(label+'_Segments.csv')).open()))
  for seg in ss:
   i=int(seg['segment']);ff=[f for f in fs if int(f['segment'])==i];assert len(ff)>5
   for f in ff:
    for k,v in [('viewport_w',2560),('viewport_h',1440),('quality',case.get('quality',2)),('percentage',case.get('percentage',100))]:assert int(f[k])==v,(label,k,f[k])
    if case.get('condition')!='PostProcessingOff':assert int(f['actual_aa_method'])==2,(label,f['actual_aa_method'])
    assert int(f['screen_percentage_showflag'])==1,(label,'screen percentage disabled')
    assert int(f['actual_upscale_method'])==1,(label,'not temporal upscaling',f)
    assert [int(f['target_w']),int(f['target_h'])]==[2560,1440],(label,'target',f)
    assert abs(float(f['pitch'])+50)<.01 and abs(float(f['yaw'])+45)<.01 and abs(float(f['fov'])-35)<.01
    expected=[math.ceil(2560*case.get('percentage',100)/100),math.ceil(1440*case.get('percentage',100)/100)]
    assert [int(f['internal_w']),int(f['internal_h'])]==expected,(label,f)
   raw=list(csv.DictReader((DATA/'Profiling/CSV'/('ENV2_'+label+'_%03d.csv'%i)).open()));stats={k:summary(values(raw,k))for k in raw[0]if k and (k.endswith('Time')or k.startswith('GPU/')or k.startswith('Exclusive/RenderThread/')or'RHI'in k or'Draw'in k or'Prim'in k or k in ['PhysicalUsedMB','ExtendedUsedMB'])}
   frame=summary(values(ff,'frame_ms'));row={'batch':p.parent.name,'label':label,'case':case,'segment':i,'site':seg['site'],'condition':seg['condition'],'repeat':int(seg['repeat']),'mode':seg['mode'],'frame_ms':frame,'fps':1000/frame['mean'],'stats':stats,'resolution_verified':True,'camera':{k:[min(float(f[k])for f in ff),max(float(f[k])for f in ff)]for k in ['camera_x','camera_y','camera_z','pitch','yaw','fov']},'window_active':all(int(f['window_active'])==1 for f in ff)};out.append(row)
(D/'Measurements.json').write_text(json.dumps({'segments':out},indent=2))
for batch in dict.fromkeys(x['batch']for x in out):
 print(batch)
 for label in dict.fromkeys(x['label']for x in out if x['batch']==batch):
  a=[x for x in out if x['label']==label]
  print(a[0]['site'],a[0]['condition'],'n',len(a),'FPS',round(st.mean(x['fps']for x in a),2),'frame',round(st.mean(x['frame_ms']['mean']for x in a),2),'GPU',round(st.mean(x['stats']['GPUTime']['mean']for x in a),2),'GT',round(st.mean(x['stats']['GameThreadTime']['mean']for x in a),2))

# Keep the matrix and short final proofs distinct; do not mix different sample durations.
aggregates=[]
for batch,mode,site,percentage in dict.fromkeys((r['batch'],r['mode'],r['site'],r['case']['percentage'])for r in out):
 a=[r for r in out if (r['batch'],r['mode'],r['site'],r['case']['percentage'])==(batch,mode,site,percentage)]
 aggregates.append({'batch':batch,'mode':mode,'site':site.removeprefix('S_'),'percentage':percentage,'fps':st.mean(r['fps']for r in a),'fps_min_run':min(r['fps']for r in a),'fps_max_run':max(r['fps']for r in a),'frame_ms':st.mean(r['frame_ms']['mean']for r in a),'frame_p95_ms':st.mean(r['frame_ms']['p95']for r in a),'gpu_ms':st.mean(r['stats']['GPUTime']['mean']for r in a),'game_ms':st.mean(r['stats']['GameThreadTime']['mean']for r in a),'render_ms':st.mean(r['stats']['RenderThreadTime']['mean']for r in a),'frames':sum(r['frame_ms']['n']for r in a),'window_active':all(r['window_active']for r in a)})
(D/'Summary.json').write_text(json.dumps({'rows':aggregates,'samples':len(out)},indent=2))
pairs=[]
for batch,pair in dict.fromkeys((r['batch'],r['case']['pair'])for r in out):
 a=[r for r in out if r['batch']==batch and r['case']['pair']==pair];assert len(a)==2
 d={k:abs(st.mean(a[0]['camera'][k])-st.mean(a[1]['camera'][k]))for k in ['camera_x','camera_y','camera_z','pitch','yaw','fov']}
 assert max(d.values())<.1,(batch,pair,d)
 pairs.append({'batch':batch,'pair':pair,'camera_delta':d})
(D/'PairValidation.json').write_text(json.dumps({'passed':True,'pairs':pairs},indent=2))
