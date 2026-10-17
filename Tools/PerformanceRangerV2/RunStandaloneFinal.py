"""Serial native standalone processes, same options as BeforeC. Each probe quits its own game through the console, never by closing a floating PIE window."""
import subprocess,sys
from pathlib import Path
R=Path('/Users/harry/Developer/PokeMonster/Game/PokeMonster');O=R/'Art/Characters/NPCs/Ranger/Review/V2';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
for label in ['FinalAfterC','VillageC']:
 assert not (R/'Saved/PerformanceRangerV2'/(label+'_Done.txt')).exists()
 args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-ResX=1280','-ResY=740','-ForceRes','-NoVSync','-NoSound','-NoSplash','-NoLiveCoding','-ExecCmds=r.Editor.Viewport.OverridePIEScreenPercentage 0,r.SecondaryScreenPercentage.GameViewport 100,pm.Perf.Run '+str(R/'Tools/PerformanceRangerV2/Plans'/(label+'.tsv'))]
 print('START',label,flush=True)
 with (O/('Standalone_'+label+'.log')).open('w') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=900)
 assert r.returncode==0,(label,r.returncode);assert (R/'Saved/PerformanceRangerV2'/(label+'_Done.txt')).read_text()=='Complete';print('DONE',label,flush=True)
