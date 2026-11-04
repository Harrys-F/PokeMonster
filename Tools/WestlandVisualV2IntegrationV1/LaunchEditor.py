from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';O=D/sys.argv[1];O.mkdir(exist_ok=False)
assert not any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines())
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-NoSplash','-NoLiveCoding','-nosound','-nowrite','-NoAssetRegistryCacheWrite','-UserDir='+str(O/'UserData'),'-ABSLOG='+str(O/'Engine.log'),'-ExecCmds=py '+str(R/'Tools/ProjectMaintenance/ArtSession.py')]
f=(O/'Console.log').open('x');p=subprocess.Popen(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,start_new_session=True);(O/'Launch.json').write_text(json.dumps(dict(pid=p.pid,args=args),indent=2));print(p.pid)
