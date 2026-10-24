"""Verify and encode actual native game-viewport JPEG frames, without invented/interpolated images."""
from pathlib import Path
import csv,json,subprocess,sys,os
R=Path(__file__).resolve().parents[2];label=sys.argv[1];targetname=sys.argv[2];assert label.isalnum()and targetname.isalnum()
source=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('BiomeV11_'+label);assert(source/'Complete.txt').is_file()
O=R/'Saved/BiomeTestV11'/label;O.mkdir(exist_ok=True);d=O/('VerifiedNative_'+targetname);d.mkdir(exist_ok=False);rows=list(csv.DictReader((source/'Frames.csv').open()));assert len(rows)>3;times=[];lines=['index,game_seconds,kind,width,height,file']
for i,row in enumerate(rows):
 p=source/row['file'];b=p.read_bytes();assert b[:2]==b'\xff\xd8'and b[-2:]==b'\xff\xd9';assert int(row['frame'])==i;w,h=int(row['width']),int(row['height']);assert w==1280 and h==720;times.append(float(row['game_seconds']));lines.append(','.join(map(str,[i,row['game_seconds'],targetname,w,h,os.path.relpath(p,d)])))
assert all(b>a for a,b in zip(times,times[1:]));assert len(list(source.glob('Frame_*.jpg')))==len(rows)
(d/'Frames.csv').write_text('\n'.join(lines)+'\n');video=O/(targetname+'_ActualPIE.mp4');assert not video.exists();run=subprocess.run([str(R/'Saved/BiomeTestV1/EncodeSequence'),str(d),str(video)],check=True,text=True,capture_output=True)
v={'file':str(video.relative_to(R)),'actual_frames':len(rows),'span_game_seconds':times[-1]-times[0],'width':w,'height':h,'max_frame_interval_seconds':max(b-a for a,b in zip(times,times[1:])),'method':'Actual Unreal framebuffer sequence with source timestamps; no generated or interpolated frames','encoder':run.stdout};(O/(targetname+'_Sequence.json')).write_text(json.dumps(v,indent=2));print(json.dumps(v,indent=2))
