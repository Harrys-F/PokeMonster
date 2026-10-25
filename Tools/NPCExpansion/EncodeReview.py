"""Encode native, timestamped Unreal captures; no generated/interpolated frames."""
from pathlib import Path
import csv,json,subprocess,os,sys
R=Path(__file__).resolve().parents[2];label=sys.argv[1];assert label.isalnum();O=R/'Saved/ProjectRefinement/NPCExpansion'/label;result=json.loads((O/'Result.json').read_text());assert result['passed'];encoder=R/'Saved/BiomeTestV1/EncodeSequence';videos=[]
if not encoder.exists():
 encoder=O/'EncodeSequence';subprocess.run(['swiftc',str(R/'Tools/MotionRefinementV5/EncodeSequence.swift'),'-o',str(encoder)],check=True)
for a in json.loads((R/'Tools/NPCExpansion/Library.json').read_text()):
 id=a['id'];source=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('NPCLibrary_'+label+'_'+id);assert (source/'Complete.txt').is_file();rows=list(csv.DictReader((source/'Frames.csv').open()));assert len(rows)>80;times=[];lines=['index,game_seconds,kind,width,height,file'];d=O/('Verified_'+id);d.mkdir(exist_ok=False)
 for i,row in enumerate(rows):
  p=source/row['file'];b=p.read_bytes();assert b[:2]==b'\xff\xd8' and b[-2:]==b'\xff\xd9';assert int(row['frame'])==i;times.append(float(row['game_seconds']));w,h=int(row['width']),int(row['height']);lines.append(','.join(map(str,[i,row['game_seconds'],id,w,h,os.path.relpath(p,d)])))
 assert all(b>a for a,b in zip(times,times[1:]));hz=(len(times)-1)/(times[-1]-times[0]);assert hz>=24,('Capture too sparse for final motion assessment',id,hz);(d/'Frames.csv').write_text('\n'.join(lines)+'\n');video=O/(id+'_Gameplay.mp4');assert not video.exists();run=subprocess.run([str(encoder),str(d),str(video)],check=True,text=True,capture_output=True);gaps=sorted(b-a for a,b in zip(times,times[1:]));videos.append({'id':id,'file':str(video.relative_to(R)),'frames':len(rows),'seconds':times[-1]-times[0],'game_time_sample_hz':hz,'max_interval':max(gaps),'width':w,'height':h,'method':result['video_method'],'encoder':run.stdout});print(id,hz,flush=True)
(O/'Videos.json').write_text(json.dumps(videos,indent=2))
