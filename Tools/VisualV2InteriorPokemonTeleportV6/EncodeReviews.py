"""Existing AVFoundation encoder; genuine QHD frames with original game timestamps, no interpolation."""
from pathlib import Path
import csv,json,subprocess,os
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';V=D/'Videos';V.mkdir(exist_ok=True);encoder=R/'Saved/BiomeTestV1/EncodeSequence';verifier=R/'Saved/ProjectRefinement/VisualV2StabilityV1/VerifyVideo';assert encoder.is_file()and verifier.is_file();summary=[]
for label,clip in [('NativeTeleport04','Motion_Pikachu'),('NativeTeleport04','Motion_Karpador'),('NativeWild02','WildMotion_Pikachu'),('NativeWild02','WildMotion_Karpador')]:
 src=D/label/clip;assert(src/'Complete.txt').exists();rows=list(csv.DictReader((src/'Frames.csv').open()));out=V/clip;out.mkdir(exist_ok=False);lines=['index,game_seconds,kind,width,height,file'];first=float(rows[0]['game_seconds'])
 for i,x in enumerate(rows):
  p=src/x['file'];assert p.is_file()and(x['width'],x['height'])==('2560','1440');lines.append(','.join(map(str,[i,float(x['game_seconds'])-first,clip,x['width'],x['height'],os.path.relpath(p,out)])))
 source=out/'Frames.csv';source.write_text('\n'.join(lines)+'\n');movie=V/(clip+'.mp4');log=subprocess.check_output([str(encoder),str(out),str(movie)],text=True);(out/'Encode.log').write_text(log)
 subprocess.run([str(verifier),str(movie),str(source),str(out/'Verified.json')],check=True,capture_output=True,text=True);v=json.loads((out/'Verified.json').read_text());assert v['passed'];summary.append(dict(movie=str(movie.relative_to(R)),**v));print(clip,v['decoded_frames'],v['actual_interval_fps'])
(D/'VideoResults.json').write_text(json.dumps(summary,indent=2))
