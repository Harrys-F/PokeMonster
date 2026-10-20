"""Measure world-space ankle slip only during sampled flat stance, never infer it from source formulas."""
from pathlib import Path
import json,math,statistics
R=Path(__file__).resolve().parents[2];D=R/'Saved/ZunderlaufV1/RuntimeReviewFinal03';j=json.loads((D/'Result.json').read_text());assert j['passed'],j['error'];rows=[json.loads(x)for x in (D/'Frames.jsonl').read_text().splitlines()];result={}
for phase in ['Direction_'+str(a)for a in range(0,360,45)]+['NativeRun']:
 samples=[r for r in rows if r['phase']==phase];slip=[]
 for side in ['left_foot','right_foot']:
  bottom=min(r[side][2]for r in samples)
  for a,b in zip(samples,samples[1:]):
   if a['phase_time']<.6 or any(abs(r[side][2]-bottom)>.03 for r in [a,b]):continue
   dt=b['game_time']-a['game_time']
   if not 0<dt<.15:continue
   slip.append(math.hypot(b[side][0]-a[side][0],b[side][1]-a[side][1]))
 result[phase]={'sampled_flat_stance_pairs':len(slip),'median_world_ankle_slip_cm':statistics.median(slip)if slip else None,'max_world_ankle_slip_cm':max(slip)if slip else None,'native_speed_min_cm_s':min(r['native_speed_cm_s']for r in samples),'native_speed_max_cm_s':max(r['native_speed_cm_s']for r in samples)}
(R/'Saved/ZunderlaufV1/MeasuredWorldContacts.json').write_text(json.dumps({'criteria':'After .6s blend, adjacent samples <.15s, both ankle heights within .03cm of their sampled phase minimum. Numerical measurement, not complete foot/terrain validation.','phases':result},indent=2));print(json.dumps(result,indent=2))
