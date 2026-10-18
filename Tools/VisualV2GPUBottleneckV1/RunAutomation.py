"""Fresh native project automation, after graphics benchmarks and with editor closed."""
from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2GPUBottleneckV1';label=sys.argv[1] if len(sys.argv)>1 else 'Automation';assert label in ['Automation','AutomationFinal'];dest=O/label;assert not dest.exists(),'Preserve previous test evidence'
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'-NullRHI','-unattended','-nosound','-nosplash','-NoLiveCoding','-ExecCmds=Automation RunTests PokeMonster','-TestExit=Automation Test Queue Empty','-ReportExportPath='+str(dest),'-stdout','-FullStdOutLogOutput']
with (O/(label+'.log')).open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=900)
(O/(label+'Exit.json')).write_text(json.dumps({'exit_code':p.returncode,'argv':args},indent=2));assert p.returncode==0,p.returncode
print('Automation exit',p.returncode)
