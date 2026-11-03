from pathlib import Path
import subprocess,json,time,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
start=time.monotonic()
while not(D/'NativeAfter01/ProcessExit.json').exists():assert time.monotonic()-start<2400;time.sleep(.5)
assert json.loads((D/'NativeAfter01/Result.json').read_text())['passed']
pid=int(subprocess.check_output([sys.executable,str(R/'Tools/VisualV2InteriorPokemonTeleportV6/LaunchEditor.py'),'EditorRelease04'],cwd=R,text=True).strip())
while json.loads((R/'Saved/ProjectRefinement/Ready.json').read_text())['pid']!=pid:assert time.monotonic()-start<2600;time.sleep(.5)
for label,script in [('PIEImports03','ImportReview.py'),('PIEInterior02','InteriorReview.py')]:
 (D/'GameplayRequest.json').write_text(json.dumps(dict(label=label,travel=False)));print(label,flush=True);job('start_pie');time.sleep(3);job('script','Tools/VisualV2InteriorPokemonTeleportV6/'+script);p=D/label/'Result.json';at=time.monotonic()
 while not p.exists():assert time.monotonic()-at<1000;time.sleep(.5)
 x=json.loads(p.read_text());print(label,x['passed'],x.get('error'),flush=True);assert x['passed'];time.sleep(2)
job('script','Tools/VisualV2InteriorPokemonTeleportV6/MapChecks.py',300);job('close');at=time.monotonic()
while any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()):assert time.monotonic()-at<90;time.sleep(.5)
assert subprocess.call([sys.executable,str(R/'Tools/VisualV2InteriorPokemonTeleportV6/RunNative.py'),'FreshFinal01','FreshVerify.py'],cwd=R)==0
assert json.loads((D/'FreshFinal01/Result.json').read_text())['passed']
assert subprocess.call([sys.executable,str(R/'Tools/VisualV2InteriorPokemonTeleportV6/RunAutomation.py'),'FullAutomationRelease','PokeMonster'],cwd=R)==0
