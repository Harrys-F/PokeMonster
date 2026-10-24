"""Encode actual Unreal frames at recorded times; split discontinuous scenes, never synthesize frames."""
from pathlib import Path
import json,sys,struct,os,subprocess
R=Path(__file__).resolve().parents[2];label=sys.argv[1];assert label.isalnum();D=R/'Saved/BiomeTestV11'/label
v=json.loads((D/'Result.json').read_text());assert v['passed'];segments=[]
for f in v['frames']:
 if not segments or f['game_time']-segments[-1][-1]['game_time']>1:segments.append([])
 segments[-1].append(f)
rows=[]
for n,frames in enumerate(segments):
 if len(frames)<3:continue
 O=D/('Sequence'+str(n));O.mkdir(exist_ok=False);lines=['index,game_seconds,kind,width,height,file'];times=[]
 for i,f in enumerate(frames):
  path=R/f['path'];data=path.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',data[16:24]);assert(width,height)==(1280,720)
  lines.append(','.join(map(str,[i,f['game_time'],'Water',width,height,os.path.relpath(path,O)])));times.append(f['game_time'])
 (O/'Frames.csv').write_text('\n'.join(lines)+'\n');target=D/('Water_ActualPIE_'+str(n)+'.mp4')
 run=subprocess.run([str(R/'Saved/BiomeTestV1/EncodeSequence'),str(O),str(target)],check=True,text=True,capture_output=True)
 rows.append(dict(file=str(target.relative_to(R)),frames=len(frames),game_seconds=times[-1]-times[0],largest_interval=max(b-a for a,b in zip(times,times[1:])),method='Actual timestamped Unreal game-camera frames, no generated or interpolated images',encoder=run.stdout))
(D/'Sequences.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
