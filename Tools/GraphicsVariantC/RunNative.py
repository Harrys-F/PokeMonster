"""Editor must be cleanly closed. No terminate/kill, bounded observation only."""
from pathlib import Path
import subprocess,json,sys,time,shutil,hashlib,ctypes,os
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/GraphicsVariantC';q=json.loads(Path(sys.argv[1]).read_text());q['mode']='Native';assert q['label'].isalnum();O=D/q['label'];assert not O.exists()
closing=time.monotonic()
while any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()):
 assert time.monotonic()-closing<45,'Editor remains open; no termination or discard'
 time.sleep(.5)
fixture=R/json.loads((D/'NativeFixture.json').read_text())['source'];assert fixture.name=='PokeMonster_SaveV2_Test_PerfGraphicsC01.sav';target=O/'UserData/Saved/SaveGames/PokeMonster_Dev.sav';target.parent.mkdir(parents=True,exist_ok=False);shutil.copyfile(fixture,target);assert hashlib.sha256(fixture.read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest()
(D/'NativeRequest.json').write_text(json.dumps(q))
# Benchmark creates O itself. Launch metadata intentionally lives alongside it.
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-NoSplash','-NoLiveCoding','-nowrite','-NoAssetRegistryCacheWrite','-UserDir='+str(O/'UserData'),'-ABSLOG='+str(D/(q['label']+'-Engine.log')),'-ExecCmds=py '+str(R/'Tools/GraphicsVariantC/NativeStartup.py')]
with(D/(q['label']+'-Console.log')).open('x')as f:p=subprocess.Popen(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(D/(q['label']+'-Launch.json')).write_text(json.dumps({'pid':p.pid,'args':args,'not_shipping':True},indent=2));print('Native PID',p.pid,flush=True);begin=time.monotonic()
ctypes.CDLL('/System/Library/Frameworks/Foundation.framework/Foundation');lib=ctypes.CDLL('/usr/lib/libobjc.A.dylib');lib.objc_getClass.argtypes=[ctypes.c_char_p];lib.objc_getClass.restype=ctypes.c_void_p;lib.sel_registerName.argtypes=[ctypes.c_char_p];lib.sel_registerName.restype=ctypes.c_void_p
send=ctypes.CFUNCTYPE(ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p)(('objc_msgSend',lib));scalar=ctypes.CFUNCTYPE(ctypes.c_long,ctypes.c_void_p,ctypes.c_void_p)(('objc_msgSend',lib));info=send(lib.objc_getClass(b'NSProcessInfo'),lib.sel_registerName(b'processInfo'));last_thermal=-100.;last_progress=None

while p.poll()is None:
 assert time.monotonic()-begin<q.get('timeout',1800)+90,'Observe process; no termination is authorized'
 if time.monotonic()-last_thermal>=5:
  state=int(scalar(info,lib.sel_registerName(b'thermalState')))
  with(D/(q['label']+'-Thermal.jsonl')).open('a')as log:log.write(json.dumps({'utc_epoch':time.time(),'elapsed':time.monotonic()-begin,'thermal_state':state,'label':['nominal','fair','serious','critical'][state]if 0<=state<4 else'unknown','loadavg':os.getloadavg()})+'\n')
  last_thermal=time.monotonic()
 if(O/'Progress.json').exists():
  progress=(O/'Progress.json').read_text()
  if progress!=last_progress:print(json.loads(progress)['name'],flush=True);last_progress=progress
 time.sleep(1)
assert p.returncode==0,p.returncode;out=json.loads((O/'Result.json').read_text());assert out['passed'];print('Native complete',len(out['cases']),'cases',flush=True)
