from pathlib import Path
import subprocess,json,time,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';start=time.monotonic()
while not(D/'EditorBuild05/Result.json').exists():assert time.monotonic()-start<300;time.sleep(.5)
for label,script in [('NativeWild02','WildMotionReview.py'),('NativeGameplay01','GameplayReview.py'),('NativeAfter01','CaptureBenchmark.py')]:
 print(label,flush=True);code=subprocess.call([sys.executable,str(R/'Tools/VisualV2InteriorPokemonTeleportV6/RunNative.py'),label,script],cwd=R);assert code==0,(label,code);p=D/label/'Result.json';assert p.exists(),str(p);x=json.loads(p.read_text());print(label,x['passed'],x.get('error'),flush=True);assert x['passed']
