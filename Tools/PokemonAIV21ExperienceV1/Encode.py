"""Encode authentic recorded frames with original game timestamps, no interpolation.
Only ignored evidence is written. No frame, capture or old video is replaced.
"""
from pathlib import Path
import csv,json,subprocess,os,sys
from collections import Counter
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/PokemonAIV21ExperienceV1';O=D/'Videos';O.mkdir(exist_ok=True);encoder=R/'Saved/BiomeTestV1/EncodeSequence';assert encoder.is_file();videos=[]
for name in (sys.argv[1:] or ['AIV21SpontaneousSocial01','AIV21SpontaneousSocial02']):
 assert name.isalnum()
 if (O/(name+'.mp4')).exists():
  print('Preserved existing video',name,flush=True);continue
 source=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/name;assert(source/'Complete.txt').exists();raw=list(csv.DictReader((source/'Frames.csv').open()));assert len(raw)>2
 assert all(int(row['frame'])==i for i,row in enumerate(raw))
 resolution=Counter((int(row['width']),int(row['height']))for row in raw).most_common(1)[0][0]
 rows=[row for row in raw if (int(row['width']),int(row['height']))==resolution]
 times=[];lines=['index,game_seconds,kind,width,height,file'];d=O/name;d.mkdir(exist_ok=False)
 for i,row in enumerate(rows):
  p=source/row['file'];b=p.read_bytes();assert b[:2]==b'\xff\xd8'and b[-2:]==b'\xff\xd9'
  times.append(float(row['game_seconds']));w,h=int(row['width']),int(row['height']);lines.append(','.join(map(str,[i,row['game_seconds'],name,w,h,os.path.relpath(p,d)])))
 assert all(b>a for a,b in zip(times,times[1:]));(d/'Frames.csv').write_text('\n'.join(lines)+'\n');video=O/(name+'.mp4');assert not video.exists();run=subprocess.run([str(encoder),str(d),str(video)],check=True,text=True,capture_output=True);hz=(len(times)-1)/(times[-1]-times[0]);videos.append({'name':name,'file':str(video.relative_to(R)),'frames':len(rows),'source_frames':len(raw),'omitted_resolution_transition_frames':len(raw)-len(rows),'game_seconds':times[-1]-times[0],'sample_hz':hz,'width':w,'height':h,'method':'Actual native Unreal framebuffer, real timestamps, no generated or interpolated frames; actual PIE footage; unmodified species profiles for AI, explicit party/victory fixture for XP; observer/clearing setup disclosed in matching review metadata','encoder':run.stdout});print(name,round(hz,2),flush=True)

if videos:
 manifest=O/(videos[-1]['name']+'_Videos.json');assert not manifest.exists();manifest.write_text(json.dumps(videos,indent=2))
