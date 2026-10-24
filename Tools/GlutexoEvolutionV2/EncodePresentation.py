"""Encode verified real Slate frames at original timestamps; no interpolation or synthetic images."""
from pathlib import Path
import csv,json,subprocess,sys,os
R=Path(__file__).resolve().parents[2];label=sys.argv[1];assert label.isalnum();O=R/'Saved/ProjectRefinement/EvolutionPresentationV21'/label;result=json.loads((O/'Result.json').read_text());assert result['passed'];videos=[]
encoder=R/'Saved/BiomeTestV1/EncodeSequence'
if not encoder.exists():
 encoder=O/'EncodeSequence';subprocess.run(['swiftc',str(R/'Tools/MotionRefinementV5/EncodeSequence.swift'),'-o',str(encoder)],check=True)
for target in ['Glutexo','Glurak']:
 source=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('EvolutionV21_'+label+'_'+target);assert(source/'Complete.txt').is_file();assert 'Slate' in(source/'CaptureMethod.txt').read_text();rows=list(csv.DictReader((source/'Frames.csv').open()));assert len(rows)>100;times=[];lines=['index,game_seconds,kind,width,height,file'];d=O/('Verified_'+target);d.mkdir(exist_ok=False)
 for i,row in enumerate(rows):
  p=source/row['file'];b=p.read_bytes();assert b[:2]==b'\xff\xd8'and b[-2:]==b'\xff\xd9';assert int(row['frame'])==i;times.append(float(row['game_seconds']));w,h=int(row['width']),int(row['height']);lines.append(','.join(map(str,[i,row['game_seconds'],target,w,h,os.path.relpath(p,d)])))
 assert all(b>a for a,b in zip(times,times[1:]));assert (len(times)-1)/(times[-1]-times[0])>=24, 'Insufficient actual game-time sampling for movement review';(d/'Frames.csv').write_text('\n'.join(lines)+'\n');video=O/(target+'_FullPIE.mp4');assert not video.exists();run=subprocess.run([str(encoder),str(d),str(video)],check=True,text=True,capture_output=True)
 gaps=sorted(b-a for a,b in zip(times,times[1:]));v=dict(file=str(video.relative_to(R)),actual_frames=len(rows),seconds=times[-1]-times[0],actual_average_hz=(len(rows)-1)/(times[-1]-times[0]),max_interval=max(gaps),p95_interval=gaps[int(len(gaps)*.95)],width=w,height=h,encoder=run.stdout,recording_time_dilation=result['recording_dilation'],method='Actual presented Slate frames, PIE deliberately slowed during recording, encoded at original game timestamps for normal-speed playback; no generated/interpolated frames');videos.append(v);print(json.dumps(v,indent=2),flush=True)
(O/'Videos.json').write_text(json.dumps(videos,indent=2))
