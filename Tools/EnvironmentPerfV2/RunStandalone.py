"""Serial native -game processes, not floating PIE or a packaged Shipping build.
Run after closing the editor safely. Each resolution starts its own correctly sized window.
"""
import subprocess,json,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
labels=sys.argv[1:] or ['StandalonePair'+str(i) for i in range(1,7)]
for label in labels:
 plan=R/'Tools/EnvironmentPerfV2/Plans'/(label+'.tsv');lines=plan.read_text().splitlines();row=lines[1].split('\t');width,height=row[3:5]
 assert all(l.split('\t')[3:5]==[width,height] for l in lines[1:] if l),'One window extent per native process'
 assert not (O/(label+'_Done.txt')).exists(),'Preserve existing measurements; choose a new label'
 args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_EnvironmentPerfV1','-game',('-fullscreen' if label=='PacingFullscreen' else '-windowed'),'-ResX='+width,'-ResY='+height,'-ForceRes','-NoVSync','-NoSplash','-NoLiveCoding','-stdout','-FullStdOutLogOutput','-ExecCmds=getall Engine bSmoothFrameRate,getall Engine bUseFixedFrameRate,getall GameUserSettings FrameRateLimit,getall GameUserSettings bUseVSync,getall GameUserSettings FullscreenMode,r.Editor.Viewport.OverridePIEScreenPercentage 0,r.SecondaryScreenPercentage.GameViewport 100,pm.EnvPerf2.Run '+str(plan)]
 (O/(label+'_Launch.json')).write_text(json.dumps({'argv':args,'mode':'Native Development -game using editor binary; not packaged Shipping'},indent=2));print('START',label,flush=True)
 with (O/(label+'.log')).open('w') as f:result=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200)
 assert result.returncode==0,(label,result.returncode)
 assert (O/(label+'_Done.txt')).read_text()=='Complete',label
 print('DONE',label,flush=True)
