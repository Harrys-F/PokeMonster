from pathlib import Path
import subprocess,json
from ProcessGuard import editor_pids
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2ShadowQualityV8';assert not editor_pids() and not (S/'NativeABC_Done.json').exists();exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-ResX=2560','-ResY=1440','-ForceRes','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8016','-ExecCmds='+','.join(['sg.'+n+'Quality 1' for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]+['py '+str(R/'Tools/VisualV2ShadowQualityV8/NativeABC.py')]),'-ABSLOG='+str(S/'NativeABC_Engine.log')]
with (S/'NativeABC_Console.log').open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=400)
assert p.returncode==0 and (S/'NativeABC_Done.json').exists();(S/'NativeABC_Result.json').write_text(json.dumps({'exit':p.returncode,'args':args},indent=2));print('NATIVE A/B/C COMPLETE',flush=True)
