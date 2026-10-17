import json,statistics,math
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2/Data';a=json.loads((O/'MotionReview.json').read_text());out={'stages':{},'automatic_lod_switches':a['automatic_lod_switches'],'limitations':['Screenshot-induced stalls are part of the captured sequence, not performance data.','Transform preview is not AI navigation.','No guaranteed physical foot locking during arbitrary acceleration or on uneven terrain.']}
for stage in dict.fromkeys(x['stage'] for x in a['frames']):
 rows=[x for x in a['frames'] if x['stage']==stage];steady=[x for x in rows if x['local_t']>.7 and x['rendered']];q={'samples':len(rows),'visible_samples':len(steady),'lods':sorted(set(x['lod'] for x in rows))}
 for key in ['speed','rate','walk_alpha','turn_alpha','cape_pitch','cape_swing','bag_swing']:
  v=[x[key] for x in steady];q[key]={'median':statistics.median(v),'range':[min(v),max(v)]} if v else None
 out['stages'][stage]=q
(O/'MotionSummary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
