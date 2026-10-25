"""Encode existing native frames with their actual game timestamps, without interpolation."""
from pathlib import Path
import csv,json,subprocess,os
R=Path(__file__).resolve().parents[2];O=R/'Saved/ProjectRefinement/EnvironmentV3/MotionFinal';result=json.loads((O/'Result.json').read_text());assert result['passed'];encoder=R/'Saved/BiomeTestV1/EncodeSequence';videos=[]
if not encoder.is_file():
 encoder=O/'EncodeSequence';subprocess.run(['swiftc',str(R/'Tools/MotionRefinementV5/EncodeSequence.swift'),'-o',str(encoder)],check=True)
for clip in result['rows']:
 source=Path(clip['source']);assert(source/'Complete.txt').exists();rows=list(csv.DictReader((source/'Frames.csv').open()));assert len(rows)>30;times=[];lines=['index,game_seconds,kind,width,height,file'];d=O/('Verified_'+clip['name']);d.mkdir(exist_ok=False)
 for i,row in enumerate(rows):
  p=source/row['file'];b=p.read_bytes();assert b[:2]==b'\xff\xd8'and b[-2:]==b'\xff\xd9';assert int(row['frame'])==i;times.append(float(row['game_seconds']));w,h=int(row['width']),int(row['height']);lines.append(','.join(map(str,[i,row['game_seconds'],clip['name'],w,h,os.path.relpath(p,d)])))
 assert all(b>a for a,b in zip(times,times[1:]));hz=(len(times)-1)/(times[-1]-times[0]);(d/'Frames.csv').write_text('\n'.join(lines)+'\n');video=O/(clip['name']+'.mp4');assert not video.exists();run=subprocess.run([str(encoder),str(d),str(video)],check=True,text=True,capture_output=True);videos.append({'name':clip['name'],'file':str(video.relative_to(R)),'frames':len(rows),'game_seconds':times[-1]-times[0],'game_time_sample_hz':hz,'width':w,'height':h,'method':result['method'],'encoder':run.stdout});print(clip['name'],hz,flush=True)
(O/'Videos.json').write_text(json.dumps(videos,indent=2))
