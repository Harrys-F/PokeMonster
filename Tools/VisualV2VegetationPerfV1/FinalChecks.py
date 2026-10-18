"""Final source/log terminology consistency after all timed runs and real footroutes."""
from pathlib import Path
import subprocess,json,time,os
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2VegetationPerfV1';O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_VegetationPerf_V1_2026-10-18');start=time.monotonic()
while not (S/'PipelineComplete.json').exists():time.sleep(3);assert time.monotonic()-start<900
assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
p=R/'Source/PokeMonster/Development/PokeMonsterEnvironmentPerformanceProbeV2.cpp';text=p.read_text();old='shadow_and_geometry_flags_unchanged=1';new='shadow_cast_flags_unchanged=1 source_mesh_assets_unchanged=1';assert text.count(old)==1 and new not in text;p.write_text(text.replace(old,new));(S/'LogTerminologyCorrection.json').write_text(json.dumps({'old':old,'new':new,'runtime_or_timed_work_changed':False,'measurement_binary':'Build1','final_binary':'Build2','reason':'Forced LOD differs intentionally; source mesh assets and shadow cast flags do not.'},indent=2))
log=O/'Build2.log';assert not log.exists()
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/Build.sh','PokeMonsterEditor','Mac','Development',str(R/'PokeMonster.uproject'),'-WaitMutex','-NoHotReloadFromIDE']
print('START final build',flush=True)
with log.open('w') as f:r=subprocess.run(args,cwd=R,stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0 and 'Result: Succeeded' in log.read_text(errors='replace');print('FINAL BUILD PASS',flush=True)
r=subprocess.run(['python3',str(R/'Tools/VisualV2VegetationPerfV1/RunQAFinal.py'),'Automation'],cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));assert r.returncode==0
(S/'FinalChecks.json').write_text(json.dumps({'final_build_passed':True,'final_automation_passed':True,'only_post_measurement_change':'Log terminology, no render or time-window operation changed'},indent=2));print('FINAL CHECKS PASS',flush=True)
