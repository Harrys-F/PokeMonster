"""Start only when no editor exists. Absolute project path; preserve all configs."""
from pathlib import Path
import json,subprocess,sys,time
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';label=sys.argv[1];assert label.isalnum();P=D/(label+'-Launch.json');assert not P.exists()
rows=subprocess.check_output(['ps','-axo','pid=,comm='],text=True);assert not any(r.strip().endswith('/Contents/MacOS/UnrealEditor')for r in rows.splitlines())
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-NoSplash','-NoLiveCoding','-nowrite','-NoAssetRegistryCacheWrite','-ABSLOG='+str(D/(label+'.log')),'-ExecCmds=py '+str(R/'Tools/VisualV2StabilityV1/Startup.py')]
with (D/(label+'.console.log')).open('x')as f:p=subprocess.Popen(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
P.write_text(json.dumps({'pid':p.pid,'args':args,'started':time.time()},indent=2));print(p.pid,flush=True)
