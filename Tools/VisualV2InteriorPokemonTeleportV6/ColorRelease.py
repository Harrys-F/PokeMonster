from pathlib import Path
import json,subprocess,time,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
start=time.monotonic()
while not(D/'NativeColorFinal01/ProcessExit.json').exists():assert time.monotonic()-start<180;time.sleep(.5)
assert json.loads((D/'NativeColorFinal01/Result.json').read_text())['passed'];pid=int(subprocess.check_output([sys.executable,str(R/'Tools/VisualV2InteriorPokemonTeleportV6/LaunchEditor.py'),'EditorColorFinal06'],cwd=R,text=True).strip())
while json.loads((R/'Saved/ProjectRefinement/Ready.json').read_text())['pid']!=pid:assert time.monotonic()-start<360;time.sleep(.5)
(D/'GameplayRequest.json').write_text(json.dumps(dict(label='PIEColorFinal02')));job('start_pie');time.sleep(3);job('script','Tools/VisualV2InteriorPokemonTeleportV6/ColorReview.py');p=D/'PIEColorFinal02/Result.json'
while not p.exists():assert time.monotonic()-start<500;time.sleep(.5)
assert json.loads(p.read_text())['passed'];time.sleep(2);job('script','Tools/VisualV2InteriorPokemonTeleportV6/MapChecks.py',240);job('close');at=time.monotonic()
while any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()):assert time.monotonic()-at<90;time.sleep(.5)
assert subprocess.call([sys.executable,str(R/'Tools/VisualV2InteriorPokemonTeleportV6/RunAutomation.py'),'FullAutomationRelease02','PokeMonster'],cwd=R)==0
