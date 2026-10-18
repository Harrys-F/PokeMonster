"""Explicit, editor-closed QA. Full project automation; optional local evidence is not a build dependency."""
from pathlib import Path
import subprocess,json,sys,time
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2VegetationPerfV1';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
mode=sys.argv[1];assert mode=='Automation'
dest=O/(mode+"Final");assert not dest.exists(),'Keep completed evidence; use a new output label';dest.mkdir()
common=[exe,str(R/'PokeMonster.uproject'),'-unattended','-nosplash','-NoLiveCoding','-stdout','-FullStdOutLogOutput','-ABSLOG='+str(dest/'Engine.log')]
args=common+['-NullRHI','-nosound','-ExecCmds=Automation RunTests PokeMonster','-TestExit=Automation Test Queue Empty','-ReportExportPath='+str(dest/'Report')]
with (dest/'Console.log').open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200)
result={'exit':p.returncode,'argv':args,'is_packaged_shipping_test':False}
(dest/'Result.json').write_text(json.dumps(result,indent=2));assert p.returncode==0,(mode,p.returncode)
if mode=='Automation':
 a=json.loads((dest/'Report/index.json').read_text(encoding='utf-8-sig'));result['summary']={k:a[k] for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']};(dest/'Result.json').write_text(json.dumps(result,indent=2));assert a['succeeded']>=49 and all(a[k]==0 for k in ['succeededWithWarnings','failed','notRun','inProcess'])
(dest/'Result.json').write_text(json.dumps(result,indent=2));print(mode,'SUCCESS',result.get('summary'),flush=True)
