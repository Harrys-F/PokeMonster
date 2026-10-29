"""Run one isolated native acceptance request; never terminates a timed-out Unreal process."""
from pathlib import Path
import subprocess,json,shutil,time,sys,re,os
R=Path.cwd().resolve();assert R==Path('/Users/harry/Developer/PokeMonster')
D=R/'Saved/ProjectRefinement/InventoryV2';f=Path(sys.argv[1]).resolve();assert f.is_relative_to(D)
q=json.loads(f.read_text());assert re.fullmatch('[A-Za-z0-9_]+',q['label']);O=D/q['label'];assert not O.exists()
assert not any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()),'Existing sessions remain untouched'
fixture=Path(q['fixture']).resolve();assert fixture.is_file()and fixture.is_relative_to(R/'Saved')
script=(D/q['script']).resolve();assert script.is_file()and script.parent==D
O.mkdir();slot=O/'UserData/Saved/SaveGames/PokeMonster_Dev.sav';slot.parent.mkdir(parents=True);shutil.copyfile(fixture,slot);shutil.copyfile(script,O/'RuntimeUsed.py');(D/'Active.json').write_text(json.dumps(q,indent=2))
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-NoSplash','-NoLiveCoding','-nosound','-nowrite','-NoAssetRegistryCacheWrite','-UserDir='+str(O/'UserData'),'-ABSLOG='+str(O/'Engine.log'),'-ExecCmds=py '+str(O/'RuntimeUsed.py')]
if q.get('gpu_csv_diagnostic'):args.append('-csvGpuStats')
with(O/'Console.log').open('x')as out:p=subprocess.Popen(args,cwd=R,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
(O/'Launch.json').write_text(json.dumps({'pid':p.pid,'args':args},indent=2));print('Owned native PID',p.pid,flush=True)
start=time.monotonic();last=-99
while p.poll()is None:
 assert time.monotonic()-start<q.get('timeout',750)+90,f'Observation timeout; PID {p.pid} was NOT terminated'
 if time.monotonic()-last>10:
  last=time.monotonic()
  if(O/'Progress.json').exists():print((O/'Progress.json').read_text(),flush=True)
 time.sleep(1)
x=json.loads((O/'Result.json').read_text());print('Exit',p.returncode,'passed',x['passed'],'cases',len(x['cases']),flush=True);assert p.returncode==0 and x['passed'],x.get('error')
