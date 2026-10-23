"""Compare spatial drift only in comparable stable stance intervals. No FPS results."""
import json,math,statistics,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/AnimationCorrectionsV61';labels=sys.argv[1:];assert len(labels)==2;out={}
for label in labels:
 d=json.loads((O/label/'Result.json').read_text());assert d['passed']and d['save_unchanged'];drift=[];z=[];weights=[]
 for a,b in zip(d['samples'],d['samples'][1:]):
  dt=b['time']-a['time'];yaw=abs((b['yaw']-a['yaw']+180)%360-180)
  if not(.005<dt<.085 and a['stage']==b['stage']and a['stage'].startswith(('Walk','Run'))and min(a['walk_alpha'],b['walk_alpha'])>.99 and abs(a['speed']-b['speed'])<3 and yaw/dt<20):continue
  duty=.5-.08*a['run_alpha']
  for i in range(2):
   if all(.06<(r['phase']+i*.5)%1<duty-.06 for r in [a,b]):
    drift.append(math.dist(a['feet'][i][:2],b['feet'][i][:2])/dt);z.append(a['feet'][i][2]);weights.append(a['contact'][i])
 assert len(drift)>60,(label,len(drift))
 out[label]=dict(eligible_stance_intervals=len(drift),median_ankle_drift_cm_s=statistics.median(drift),p95_ankle_drift_cm_s=sorted(drift)[int(len(drift)*.95)],median_ankle_z_cm=statistics.median(z),mean_contact_weight=statistics.mean(weights),max_player_speed_cm_s=max(r['speed']for r in d['samples']))
(O/'FootContactComparison.json').write_text(json.dumps(dict(results=out,scope='Foot bone drift on stable near-straight grounded stance intervals. Excludes transitions, sharp turns, long frame gaps. No claim of perfect vertex-level sole contact or terrain-wide IK acceptance.'),indent=2));print(json.dumps(out,indent=2))
