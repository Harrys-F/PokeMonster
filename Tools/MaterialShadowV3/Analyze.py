"""Validate render dimensions on every measured frame; aggregate separate timings."""
from pathlib import Path
import csv,json,statistics as st,math,sys,collections
D=Path(__file__).resolve().parents[2]/'Saved/ProjectRefinement/MaterialShadowV3'
batch=sys.argv[1];O=D/batch;d=json.loads((O/'Result.json').read_text());assert d['passed'],d.get('error');DATA=Path(d['isolated_data']);out=[];pools={}
def avg(xs):return st.mean(xs)
def stats(xs):return dict(n=len(xs),mean=avg(xs),p95=sorted(xs)[math.ceil(.95*len(xs))-1],min=min(xs),max=max(xs))
for c in d['cases']:
 f=list(csv.DictReader((DATA/'EnvironmentPerfV2'/(c['label']+'_Frames.csv')).open()));assert len(f)>=60
 for row in f:
  for k,v in dict(viewport_w=2560,viewport_h=1440,target_w=2560,target_h=1440,view_w=2560,view_h=1440,internal_w=1920,internal_h=1080,actual_aa_method=2,actual_upscale_method=1,screen_percentage_showflag=1,percentage=75,quality=2,window_active=1).items():assert int(row[k])==v,(c['name'],k,row[k])
  assert float(row['primary_fraction'])==.75 and float(row['secondary_fraction'])==1
 raw=list(csv.DictReader((DATA/'Profiling/CSV'/('ENV2_'+c['label']+'_000.csv')).open()));vals={}
 for row in raw:
  for k,v in row.items():
   if not k or not(k.endswith('Time')or k.startswith('GPU/')):continue
   try:x=float(v)
   except(ValueError,TypeError):continue
   if math.isfinite(x)and x>=0:vals.setdefault(k,[]).append(x)
 pools.setdefault((c['site'],c['hour'],c.get('variant','Control')),[]).extend(float(x['frame_ms'])for x in f)
 ft=stats([float(x['frame_ms'])for x in f]);out.append({**c,'fps':1000/ft['mean'],'frame':ft,'camera':{k:[min(float(x[k])for x in f),max(float(x[k])for x in f)]for k in ['camera_x','camera_y','camera_z','pitch','yaw','fov']},'stats':{k:stats(v)for k,v in vals.items()}})
rows=[]
for site,h,v in dict.fromkeys((c['site'],c['hour'],c.get('variant','Control'))for c in out):
 a=[c for c in out if(c['site'],c['hour'],c.get('variant','Control'))==(site,h,v)]
 rows.append(dict(site=site,hour=h,variant=v,runs=len(a),fps=avg(c['fps']for c in a),fps_range=[min(c['fps']for c in a),max(c['fps']for c in a)],frame_ms=avg(c['frame']['mean']for c in a),p95_ms=stats(pools[(site,h,v)])['p95'],gpu_ms=avg(c['stats']['GPUTime']['mean']for c in a),game_ms=avg(c['stats']['GameThreadTime']['mean']for c in a),render_ms=avg(c['stats']['RenderThreadTime']['mean']for c in a),gpu_scopes_ms={k:avg(c['stats'][k]['mean']for c in a)for k in a[0]['stats']if k.startswith('GPU/')and all(k in c['stats']for c in a)}))
(O/'Measurements.json').write_text(json.dumps(dict(windows=len(out),renderer_per_frame_validated=True,segments=out,rows=rows),indent=2))
for x in rows:
 scopes=x['gpu_scopes_ms'];print(x['site'],x['hour'],x['variant'],x['runs'],*[round(x[k],3)for k in ['fps','gpu_ms','frame_ms','p95_ms','game_ms','render_ms']],{k:round(v,3)for k,v in scopes.items()if any(n in k for n in ['BasePass','ShadowDepth','ShadowProjection','ScreenProbeGather'])})
