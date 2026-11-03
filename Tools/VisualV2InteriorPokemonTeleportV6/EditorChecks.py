"""Owned editor start, real PIE review and twelve read-only map checks; guarded clean close."""
from pathlib import Path
import subprocess,json,time,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2InteriorPokemonTeleportV6';sys.path.insert(0,str(R/'Tools/ProjectMaintenance'));from ArtControl import job
start=time.monotonic();done=D/'FullAutomation01/Result.json'
while not done.exists():assert time.monotonic()-start<900;time.sleep(.5)
assert json.loads(done.read_text())['strict_wrapper_exit']==0,done.read_text()
pid=int(subprocess.check_output([sys.executable,str(R/'Tools/VisualV2InteriorPokemonTeleportV6/LaunchEditor.py'),'EditorChecks03'],cwd=R,text=True).strip())
while json.loads((R/'Saved/ProjectRefinement/Ready.json').read_text())['pid']!=pid:assert time.monotonic()-start<1000;time.sleep(.5)
for label,script in [('PIERoomPreview01','RoomPreview.py'),('PIETeleport01','TeleportReview.py'),('PIEInterior01','InteriorReview.py')]:
 (D/'GameplayRequest.json').write_text(json.dumps(dict(label=label,travel=False)));print(label,flush=True);job('start_pie');time.sleep(3);job('script','Tools/VisualV2InteriorPokemonTeleportV6/'+script);p=D/label/'Result.json';at=time.monotonic()
 while not p.exists():assert time.monotonic()-at<1200;time.sleep(.5)
 result=json.loads(p.read_text());print(label,result['passed'],result.get('error'),flush=True);assert result['passed'];time.sleep(2)
print('Map checks',flush=True);job('script','Tools/VisualV2InteriorPokemonTeleportV6/MapChecks.py',300);job('close');print('Editor checks complete',flush=True)
