from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[2];O=Path('/Users/harry/Documents/Codex/PokeMonster_VisualV2_AASoftShadows_V1_2026-10-18');label=sys.argv[1]
assert not (O/(label+'.log')).exists()
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
with (O/(label+'_Console.log')).open('w') as f:
 p=subprocess.Popen([exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1','-NoSplash','-NoLiveCoding','-ExecCmds=py '+str(R/'Tools/VisualV2AASoftShadowsV1/Startup.py'),'-ABSLOG='+str(O/(label+'.log'))],stdout=f,stderr=subprocess.STDOUT,cwd=R)
 print('Editor PID',p.pid,flush=True);print('Editor exit',p.wait(),flush=True)
