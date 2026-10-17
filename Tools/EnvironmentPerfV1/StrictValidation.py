"""Validate complete paired runs and actual extents/poses, without inventing missing data."""
from pathlib import Path
import json,collections
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV1';d=json.loads((O/'Measurements.json').read_text());out={}
for label in ['FinalPairedPIE']+['StandalonePair'+str(i) for i in range(1,7)]:
 rows=d[label];assert len(rows)==(108 if label=='FinalPairedPIE' else 18),(label,len(rows));g=collections.defaultdict(list)
 for r in rows:
  assert r['samples']>50,(label,r['segment'])
  assert len(r['extent'])==1 and len(r['fractions'])==1 and len(r['window'])==1
  w,h,tw,th,vw,vh,iw,ih=r['extent'][0];f=float(r['percentage'])/100
  assert (w,h)==(tw,th)==(vw,vh)
  assert r['fractions'][0]==[f,1.0]
  assert (iw,ih)==({(1280,740,.75):(960,555),(1280,740,1.):(1280,740),(2560,1440,.75):(1920,1080),(2560,1440,1.):(2560,1440)}[(w,h,f)])
  assert r['camera']['pitch']==[-50.,-50.] and r['camera']['yaw']==[-45.,-45.] and r['camera']['fov']==[35.,35.]
  assert all(v[0]==v[1] for v in r['camera'].values())
  assert r['active_window_fraction']==1.0,(label,r['segment'],'inactive window')
  g[(w,h,r['quality'],r['percentage'],r['site'],r['condition'])].append(r)
 assert all(sorted(x['repeat'] for x in rs)==['1','2','3'] for rs in g.values()),label
 for key,rs in g.items():
  other=g[key[:-1]+(('MapCandidate' if key[-1]=='Control' else 'Control'),)]
  for a in rs:
   b=next(b for b in other if b['repeat']==a['repeat']);assert a['camera']==b['camera']
 out[label]={'segments':len(rows),'groups':len(g),'three_repetitions_each':True,'actual_extents_and_camera_verified':True,'window_active_all_frames':True}
(O/'StrictValidation.json').write_text(json.dumps(out,indent=2));print('All final paired extents, repetitions, camera and foreground state validated')
