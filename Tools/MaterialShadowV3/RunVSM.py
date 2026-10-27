"""Explicit isolated native benchmark. Never ends an existing editor or writes user saves."""
from pathlib import Path
import argparse,json,re,subprocess,shutil,time,ctypes,os
R=Path(__file__).resolve().parents[2];assert R==Path('/Users/harry/Developer/PokeMonster');D=R/'Saved/ProjectRefinement/MaterialShadowV3'
a=argparse.ArgumentParser();a.add_argument('label');a.add_argument('--fixture',required=True);a.add_argument('--mode',choices=['matrix','smoke','production'],default='matrix');a.add_argument('--expected-rays',type=int,choices=[4,8]);args=a.parse_args();assert re.fullmatch('[A-Za-z0-9_]+',args.label)
rows=subprocess.check_output(['ps','-axo','comm='],text=True).splitlines();assert not any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in rows),'Existing editor/game remains untouched'
fixture=(R/args.fixture).resolve();assert fixture.is_relative_to(R/'Saved/SaveGames')and fixture.name.startswith('PokeMonster_SaveV2_Test_')and fixture.is_file()
O=D/args.label;assert not O.exists();(O/'UserData/Saved/SaveGames').mkdir(parents=True);shutil.copyfile(fixture,O/'UserData/Saved/SaveGames/PokeMonster_Dev.sav')
sites=[('Dorf',[-4100,450,50.15]),('Wiese',[-300,2100,50.15]),('Waldweg',[-2600,950,50.15]),('Wald',[-4300,1550,50.15]),('Innenraum',[17050,500,50.15])];cases=[]
for repeat in range(1,4 if args.mode!='smoke'else 2):
 for hi,hour in enumerate([6,12,19,22]if args.mode=='matrix'else[12]):
  for si,(site,pos)in enumerate((sites if repeat!=2 else list(reversed(sites)))if args.mode=='matrix'else[sites[0],sites[3]]):
   variants=['Production']if args.mode=='production'else(['Control','VSM4']if(repeat+hi+si)%2 else['VSM4','Control'])
   for variant in variants:
    row=dict(name=f'{site}H{hour}R{repeat}{variant}',site=site,position=pos,hour=hour,repeat=repeat,variant=variant)
    if variant!='Production':row['vsm_rays']=8 if variant=='Control'else 4
    cases.append(row)
q=dict(label=args.label,cases=cases,warmup=4,duration=5,timeout=1500,expected_production_rays=args.expected_rays if args.mode=='production'else None);(D/'VSMRequest.json').write_text(json.dumps(q,indent=2))
for name,cmd in [('Power',['pmset','-g','custom']),('Battery',['pmset','-g','batt']),('Host',['sysctl','hw.model','hw.memsize','machdep.cpu.brand_string'])]:
 x=subprocess.run(cmd,capture_output=True,text=True);(O/(name+'.txt')).write_text(x.stdout+x.stderr)
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';cmd=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-NoSplash','-NoLiveCoding','-nowrite','-NoAssetRegistryCacheWrite','-UserDir='+str(O/'UserData'),'-ABSLOG='+str(O/'Engine.log'),'-ExecCmds=py '+str(R/'Tools/MaterialShadowV3/VSMRuntime.py')]
with(O/'Console.log').open('x')as f:p=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(O/'Launch.json').write_text(json.dumps({'pid':p.pid,'args':cmd},indent=2));print('Native PID',p.pid,flush=True)
ctypes.CDLL('/System/Library/Frameworks/Foundation.framework/Foundation');lib=ctypes.CDLL('/usr/lib/libobjc.A.dylib');lib.objc_getClass.argtypes=[ctypes.c_char_p];lib.objc_getClass.restype=ctypes.c_void_p;lib.sel_registerName.argtypes=[ctypes.c_char_p];lib.sel_registerName.restype=ctypes.c_void_p
send=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p)(('objc_msgSend',lib));scalar=ctypes.CFUNCTYPE(ctypes.c_long,ctypes.c_void_p,ctypes.c_void_p)(('objc_msgSend',lib));info=send(lib.objc_getClass(b'NSProcessInfo'),lib.sel_registerName(b'processInfo'));start=time.monotonic();last=-99;seen=None
while p.poll()is None:
 if time.monotonic()-start>q['timeout']+90:raise TimeoutError(f'Observation timed out; PID {p.pid} was NOT terminated')
 if time.monotonic()-last>=5:
  with(O/'Thermal.jsonl').open('a')as f:f.write(json.dumps({'elapsed':time.monotonic()-start,'thermal_state':int(scalar(info,lib.sel_registerName(b'thermalState'))),'loadavg':os.getloadavg()})+'\n')
  last=time.monotonic()
 if(O/'Progress.json').exists():
  item=(O/'Progress.json').read_text()
  if item!=seen:print(json.loads(item)['name'],flush=True);seen=item
 time.sleep(1)
assert p.returncode==0,p.returncode;result=json.loads((O/'Result.json').read_text());assert result['passed'],result.get('error');print('Passed',len(result['cases']),'windows; render dimensions still require Analyze.py',flush=True)
