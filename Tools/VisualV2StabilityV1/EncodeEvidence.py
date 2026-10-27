"""Use the existing native encoder. Longest contiguous stable-size run; source files stay untouched."""
from pathlib import Path
import csv,json,os,subprocess,sys,itertools
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';V=D/'Videos';V.mkdir(exist_ok=True);encoder=R/'Saved/BiomeTestV1/EncodeSequence';assert encoder.is_file();verify=D/'VerifyVideo';assert verify.is_file()
for name in sys.argv[1:]:
 assert all(c.isalnum()or c=='_'for c in name);src=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/name;assert(src/'Complete.txt').exists();raw=list(csv.DictReader((src/'Frames.csv').open()));runs=[list(g)for k,g in itertools.groupby(raw,key=lambda r:(r['width'],r['height']))];rows=max(runs,key=len);assert len(rows)>3;dst=V/name;dst.mkdir(exist_ok=True);first=float(rows[0]['game_seconds']);lines=['index,game_seconds,kind,width,height,file']
 for i,r in enumerate(rows):
  p=(src/r['file']).resolve();assert p.is_relative_to(R/'Saved');assert p.is_file();lines.append(','.join(map(str,[i,float(r['game_seconds'])-first,name,r['width'],r['height'],os.path.relpath(p,dst)])))
 inputs=dst/'Frames.csv';text='\n'.join(lines)+'\n'
 if inputs.exists():assert inputs.read_text()==text,'Preserve differing prior source selection'
 else:inputs.write_text(text)
 out=V/(name+'.mp4');
 if not out.exists():
  result=subprocess.run([str(encoder),str(dst),str(out)],check=True,text=True,capture_output=True);(dst/'Encode.log').write_text(result.stdout+result.stderr)
 result=subprocess.run([str(verify),str(out),str(inputs),str(dst/'VerifiedFinal.json')],check=True,text=True,capture_output=True);verified=json.loads((dst/'VerifiedFinal.json').read_text());assert verified['passed'],verified
 (dst/'SourceFinal.json').write_text(json.dumps({'source':str(src.relative_to(R)),'raw_frames':len(raw),'encoded_frames':len(rows),'omitted_resolution_transition_frames':len(raw)-len(rows),'first_original_game_seconds':first,'first_original_frame':int(rows[0]['frame']),'last_original_frame':int(rows[-1]['frame']),'encoder_spatial_adjustment':'Existing H264 encoder may round odd native viewport dimensions down by one pixel; decoded dimensions are in Verified.json','constant_time_offset_only':True,'original_sources_untouched':True,'movie':str(out.relative_to(R))},indent=2));print(name,result.stdout.strip(),flush=True)
