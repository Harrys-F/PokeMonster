"""Explicit, editor-closed QA. Targeted Mac cook is not a packaged-game acceptance."""
from pathlib import Path
import subprocess,json,sys,time
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2AASoftShadowsV1';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
mode=sys.argv[1];assert mode in ['Automation','Cook']
dest=O/mode;assert not dest.exists(),'Keep completed evidence; use a new output label';dest.mkdir()
common=[exe,str(R/'PokeMonster.uproject'),'-unattended','-nosplash','-NoLiveCoding','-stdout','-FullStdOutLogOutput','-ABSLOG='+str(dest/'Engine.log')]
if mode=='Automation':
 args=common+['-NullRHI','-nosound','-ExecCmds=Automation RunTests PokeMonster','-TestExit=Automation Test Queue Empty','-ReportExportPath='+str(dest/'Report')]
else:
 args=common+['-run=Cook','-TargetPlatform=Mac','-CookDir='+str(R/'Content/Development/VisualV2AASoftShadowsV1'),'-NoDefaultMaps','-NoGameAlwaysCook','-SkipSoftReferences','-OutputDir='+str(dest/'Output')]
with (dest/'Console.log').open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200)
result={'exit':p.returncode,'argv':args,'is_packaged_shipping_test':False}
(dest/'Result.json').write_text(json.dumps(result,indent=2));assert p.returncode==0,(mode,p.returncode)
if mode=='Automation':
 a=json.loads((dest/'Report/index.json').read_text(encoding='utf-8-sig'));result['summary']={k:a[k] for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']};assert a['succeeded']>=48 and all(a[k]==0 for k in ['succeededWithWarnings','failed','notRun','inProcess'])
(dest/'Result.json').write_text(json.dumps(result,indent=2));print(mode,'SUCCESS',result.get('summary'),flush=True)
