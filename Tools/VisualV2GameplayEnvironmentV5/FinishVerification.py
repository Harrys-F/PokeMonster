"""Sequential owned-session final verification. Never kills, reloads dirty content or touches user storage."""
from pathlib import Path
import json,subprocess,time,runpy,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2GameplayEnvironmentV5';expected_pid=int(sys.argv[1]);j=runpy.run_path(str(R/'Tools/ProjectMaintenance/ArtControl.py'))['job'];start=time.monotonic()
def stage(name):
 (D/'FinalPipeline.json').write_text(json.dumps(dict(stage=name,seconds=time.monotonic()-start),indent=2));print(name,flush=True)
while True:
 ready=json.loads((R/'Saved/ProjectRefinement/Ready.json').read_text())
 if ready['pid']==expected_pid:break
 assert time.monotonic()-start<120,'Owned editor not ready; no action attempted';time.sleep(.25)
stage('Final entrance clearance');j('script','Tools/VisualV2GameplayEnvironmentV5/EntranceClearance.py',180);j('script','Tools/VisualV2GameplayEnvironmentV5/Audit.py',180)
stage('Final 21-point photographic atlas');(D/'Request.json').write_text('{"label":"AfterAtlas03"}');j('start_pie');j('script','Tools/VisualV2GameplayEnvironmentV5/Atlas.py',120);p=D/'AfterAtlas03/Result.json';at=time.monotonic()
while not p.exists():assert time.monotonic()-at<450;time.sleep(.5)
assert json.loads(p.read_text())['passed'],p.read_text();time.sleep(1)
stage('Final twelve map checks');j('script','Tools/VisualV2GameplayEnvironmentV5/MapChecks.py',180)
stage('Regular clean editor shutdown');j('close');at=time.monotonic()
while any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()):
 assert time.monotonic()-at<60,'Editor is still open; no termination attempted';time.sleep(.25)
for label,script in [('NativeGameplay02','GameplayReview.py'),('NativeAfter02','CaptureBenchmark.py'),('FreshFinal01','FreshVerify.py')]:
 stage(label);assert subprocess.call([sys.executable,str(R/'Tools/VisualV2GameplayEnvironmentV5/RunNative.py'),label,script],cwd=R)==0;result=D/label/'Result.json';assert result.exists()and json.loads(result.read_text())['passed'],result.read_text()if result.exists()else str(result)
stage('Final editor build');assert subprocess.call([sys.executable,str(R/'Tools/ProjectMaintenance/ProjectQA.py'),'VisualV2GameplayEnvironmentV5/EditorBuild03','Build'],cwd=R)==0
stage('Full strict automation release');assert subprocess.call([sys.executable,str(R/'Tools/VisualV2GameplayEnvironmentV5/RunAutomation.py'),'FullAutomationRelease','PokeMonster'],cwd=R)==0
stage('Verification completed')
