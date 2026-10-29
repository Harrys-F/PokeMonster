"""Owned native review launcher. Copies only explicitly chosen QA fixture; never terminates a timed-out process."""
from pathlib import Path
import subprocess,json,shutil,time,sys,re,os
R=Path.cwd().resolve();f=Path(sys.argv[1]).resolve();D=f.parent;assert D in [R/'Saved/ProjectRefinement/ModelsV4',R/'Saved/ProjectRefinement/RaichuMeshyCorrection'];q=json.loads(f.read_text());assert re.fullmatch('[A-Za-z0-9_]+',q['label']);O=D/q['label'];assert not O.exists()
assert not any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()),'Existing sessions remain untouched'
fixture=Path(q['fixture']).resolve();assert fixture.is_file()and fixture.is_relative_to(R/'Saved');script=(R/q.get('script','Tools/ModelsV4/Gameplay.py')).resolve();assert script.is_file()and (script.is_relative_to(R/'Tools/ModelsV4')or script.is_relative_to(D));O.mkdir();slot=O/'UserData/Saved/SaveGames/PokeMonster_Dev.sav';slot.parent.mkdir(parents=True);shutil.copyfile(fixture,slot);(D/'Active.json').write_text(json.dumps(q,indent=2));shutil.copyfile(script,O/'RuntimeUsed.py')
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-NoSplash','-NoLiveCoding','-nosound','-nowrite','-NoAssetRegistryCacheWrite','-UserDir='+str(O/'UserData'),'-ABSLOG='+str(O/'Engine.log'),'-ExecCmds=py '+str(O/'RuntimeUsed.py')]
with(O/'Console.log').open('x')as out:p=subprocess.Popen(args,cwd=R,stdout=out,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'PM_REVIEW_ROOT':D.name})
(O/'Launch.json').write_text(json.dumps({'pid':p.pid,'args':args},indent=2));print('Owned native PID',p.pid,flush=True);start=time.monotonic();last=0
while p.poll()is None:
 assert time.monotonic()-start<q.get('timeout',850)+90,f'Observation timeout; PID {p.pid} was NOT terminated'
 if time.monotonic()-last>15:
  last=time.monotonic()
  if(O/'Progress.json').exists():print((O/'Progress.json').read_text(),flush=True)
 time.sleep(1)
(O/'ProcessExit.json').write_text(json.dumps({'returncode':p.returncode,'seconds':time.monotonic()-start,'has_test_result':(O/'Result.json').exists()},indent=2))
assert (O/'Result.json').exists(),f'Process {p.pid} exited {p.returncode} without a test result; inspect its Engine.log. No pass claimed.'
x=json.loads((O/'Result.json').read_text());print('Exit',p.returncode,'passed',x['passed'],'checks',len(x['checks']),flush=True);assert p.returncode==0 and x['passed'],x.get('error')
