"""Existing Automation RunTests/strict report contract, with owned isolated storage and no timeout kill."""
from pathlib import Path
import subprocess,sys,time,json,re
R=Path(__file__).resolve().parents[2];label=sys.argv[1];scope=sys.argv[2]if len(sys.argv)>2 else'PokeMonster';assert re.fullmatch('[A-Za-z0-9_]+',label)and scope in ['PokeMonster','PokeMonster.GaradosWater'];D=R/'Saved/ProjectRefinement/GaradosWaterV2'/label;D.mkdir(exist_ok=False)
assert not any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()),'Existing sessions remain untouched'
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'-NoSplash','-NoLiveCoding','-nowrite','-NoAssetRegistryCacheWrite','-UserDir='+str(D/'UserData'),'-unattended','-NullRHI','-nosound','-stdout','-FullStdOutLogOutput','-ABSLOG='+str(D/'Engine.log'),'-ExecCmds=Automation RunTests '+scope,'-TestExit=Automation Test Queue Empty','-ReportExportPath='+str(D/'Report')]
start=time.monotonic()
with(D/'Console.log').open('x')as f:p=subprocess.Popen(args,cwd=R,stdout=f,stderr=subprocess.STDOUT)
(D/'Launch.json').write_text(json.dumps({'pid':p.pid,'args':args},indent=2));print('Owned automation PID',p.pid,flush=True)
while p.poll()is None:
 assert time.monotonic()-start<1200,f'Observation timeout; PID {p.pid} was NOT terminated'
 time.sleep(.5)
r={'engine_exit':p.returncode,'scope':scope,'seconds':time.monotonic()-start};report=D/'Report/index.json';ok=False
if report.exists():
 d=json.loads(report.read_text(encoding='utf-8-sig'));r['summary']={k:d[k]for k in ['succeeded','succeededWithWarnings','failed','notRun','inProcess']};r['functional_pass']=p.returncode==0 and d['succeeded']+d['succeededWithWarnings']>=(314 if scope=='PokeMonster'else 5)and all(d[k]==0 for k in ['failed','notRun','inProcess']);r['warnings']=[{'test':t['fullTestPath'],'entries':t['entries']}for t in d['tests']if t.get('warnings',0)];ok=r['functional_pass']and d['succeededWithWarnings']==0
r['strict_wrapper_exit']=0 if ok else 1;(D/'Result.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));print(json.dumps(r,ensure_ascii=False),flush=True);sys.exit(r['strict_wrapper_exit'])
