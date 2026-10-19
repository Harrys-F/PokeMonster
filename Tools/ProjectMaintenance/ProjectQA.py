"""Explicit editor-closed build/automation runner with preserved local evidence."""
from pathlib import Path
import subprocess,json,time,sys
R=Path(__file__).resolve().parents[2];label,mode=sys.argv[1:];O=R/'Saved/ProjectRefinement'/label;start=time.time()
while True:
 rows=subprocess.check_output(['ps','-axo','pid=,comm='],text=True).splitlines()
 if not any(x.strip().split(None,1)[-1].endswith('/Contents/MacOS/UnrealEditor') for x in rows):break
 assert time.time()-start<45,'Editor still open; no termination or discard'
 time.sleep(.5)
O.mkdir(exist_ok=False)
if mode=='Build':args=['/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/Build.sh','PokeMonsterEditor','Mac','Development',str(R/'PokeMonster.uproject'),'-WaitMutex','-NoHotReloadFromIDE']
else:
 assert mode=='Automation';args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'-NoSplash','-NoLiveCoding','-unattended','-NullRHI','-nosound','-stdout','-FullStdOutLogOutput','-ABSLOG='+str(O/'Engine.log'),'-ExecCmds=Automation RunTests PokeMonster','-TestExit=Automation Test Queue Empty','-ReportExportPath='+str(O/'Report')]
with (O/'Console.log').open('x') as f:code=subprocess.run(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,timeout=1200).returncode
r={'mode':mode,'exit':code,'seconds':time.time()-start};assert code==0,r
if mode=='Automation':
 d=json.loads((O/'Report/index.json').read_text(encoding='utf-8-sig'));r['summary']={k:d[k] for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']};assert d['succeeded']>=49 and all(d[k]==0 for k in ['succeededWithWarnings','failed','notRun','inProcess']),r
(O/'Result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r),flush=True)
