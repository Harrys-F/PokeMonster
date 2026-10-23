"""Make short videos solely from genuine framebuffer frames with original timestamps.
Symlinks reference existing local frames; no synthetic frames, copied projects, or uploaded media.
"""
from pathlib import Path
import csv,json,subprocess,sys
R=Path(__file__).resolve().parents[2];O=R/'Saved/AnimationCorrectionsV61';encoder=R/'Saved/MotionRefinementV5/EncodeSequence'
if not encoder.exists():
 print('VIDEO_NOT_EXECUTED: optional local AVFoundation encoder absent; genuine timestamped frame sequences remain available.')
 raise SystemExit(2)
assert len(sys.argv)in [3,4],'Usage: EncodeReviews.py Before|After REVIEW_LABEL [--player-only|--glurak-only]'
names=(["Player"]if sys.argv[-1]=='--player-only'else["Glurak"]if sys.argv[-1]=='--glurak-only'else["Glurak","Player"])
cases=[(sys.argv[1],sys.argv[2],n)for n in names]
for side,label,name in cases:
 result=json.loads((O/label/'Result.json').read_text());assert result['passed']and result['save_unchanged'];samples=result['samples'];record=Path(result['recording']);rows=list(csv.DictReader((record/'Frames.csv').open()));assert rows and all(int(x['width'])==2560 and int(x['height'])==1440 for x in rows)
 record_start=next(x['time']for x in samples if x['stage']=='record')
 start=next(x['time']for x in samples if x['stage']==('player center'if name=='Player'else name+' visit'))
 end=next((x['time']for x in samples if x['time']>start and ((x['stage'].endswith(' visit')and not x['stage'].startswith(name))or x['stage']=='return'or(name!='Player'and x['stage']=='player center'))),samples[-1]['time']+.1)
 chosen=[x for x in rows if start-record_start<=float(x['game_seconds'])<=end-record_start];assert len(chosen)>=10,(label,name,len(chosen));dest=O/'Media'/(side+name)
 if (dest/'Motion.mp4').exists():
  assert list(csv.DictReader((dest/'Frames.csv').open()))==chosen,'Preserve different existing recording';print('VERIFIED_EXISTING_VIDEO',side,name,flush=True);continue
 dest.mkdir(parents=True,exist_ok=False)
 for row in chosen:(dest/row['file']).symlink_to(record/row['file'])
 with (dest/'Frames.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=list(chosen[0]));w.writeheader();w.writerows(chosen)
 subprocess.run([str(encoder),str(dest),str(dest/'Motion.mp4')],check=True);print('REAL_VIDEO',side,name,len(chosen),flush=True)
