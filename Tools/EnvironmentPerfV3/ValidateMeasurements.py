import json,collections,math
from pathlib import Path
from Summarize import summarize
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';d=summarize();out={}
for prefix in ['PIEMatrix','NativeMatrix']:
 for i in range(1,7):
  label=prefix+str(i)
  if not (O/(label+'_Done.txt')).exists():continue
  rows=d[label];assert len(rows)==18,(label,len(rows));g=collections.defaultdict(list)
  for r in rows:
   assert r['samples']>50,(label,r['segment'],r['samples'])
   assert all(math.isfinite(r[n]) and r[n]>0 for n in ['median_fps','median_ms','p95_ms'])
   assert len(r['extent'])==len(r['fractions'])==len(r['window'])==1
   w,h,tw,th,vw,vh,iw,ih=r['extent'][0];f=float(r['percentage'])/100
   assert (w,h)==(tw,th)==(vw,vh)
   assert tuple(r['fractions'][0])==(f,1.0)
   assert (iw,ih)==(math.ceil(w*f),math.ceil(h*f))
   assert r['camera']['pitch']==[-50.,-50.] and r['camera']['yaw']==[-45.,-45.] and r['camera']['fov']==[35.,35.]
   assert all(v[0]==v[1] for v in r['camera'].values()),(label,r['segment'],'camera moved')
   assert r['active_window_fraction']==1.,(label,r['segment'],'inactive window',r['active_window_fraction'])
   g[(w,h,r['quality'],r['percentage'],r['site'],r['condition'])].append(r)
  assert all(sorted(x['repeat'] for x in rs)==['1','2','3'] for rs in g.values())
  for key,rs in g.items():
   other=g[key[:-1]+(('TreeMinLOD1' if key[-1]=='Control' else 'Control'),)]
   for a in rs:
    b=next(b for b in other if b['repeat']==a['repeat']);assert a['camera']==b['camera'];assert a['window']==b['window']
  out[label]={'segments':len(rows),'three_repetitions_each_site_state':True,'actual_extents_camera_and_active_window_verified':True,'all_segment_csv_present':all('csv' in r for r in rows)}
(O/'MatrixValidation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
