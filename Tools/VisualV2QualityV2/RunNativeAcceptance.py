"""Protect the dev save before each native run; preserve test outputs outside source control."""
import json,hashlib,shutil,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2QualityV2';label,width,height=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]);dest=O/'Acceptance'/label;dest.mkdir(parents=True,exist_ok=False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before={'existed':slot.exists()}
if slot.exists():before['sha256']=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,dest/'DevSaveOriginal.sav')
(dest/'SaveBefore.json').write_text(json.dumps(before));(O/'AcceptanceRequest.json').write_text(json.dumps({'label':label,'width':width,'height':height,'quality':1,'percentage':75,'mode':'Standalone','battle_review_only':label.endswith('_BattleReview')}))
running=subprocess.check_output(['pgrep','-alf','UnrealEditor'],text=True);assert 'Contents/MacOS/UnrealEditor ' not in running
commands=['sg.'+n+'Quality 1' for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]+['py '+str(R/'Tools/VisualV2QualityV2/NativeAcceptance.py')]
a=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-ForceRes','-ResX='+str(width),'-ResY='+str(height),'-NoVSync','-NoLiveCoding','-ModelContextProtocolPort=8012','-ExecCmds='+','.join(commands),'-ABSLOG='+str(dest/'Native.log'),'-stdout','-FullStdOutLogOutput']
(dest/'Launch.json').write_text(json.dumps(a,indent=2));print('NATIVE START',label,flush=True)
with (dest/'Console.log').open('w') as f:
 p=subprocess.Popen(a,stdout=f,stderr=subprocess.STDOUT);start=time.monotonic();last=None
 while p.poll() is None:
  time.sleep(3)
  if (dest/'NativeFailure.txt').exists():raise RuntimeError((dest/'NativeFailure.txt').read_text())
  if (dest/'FootProgress.json').exists():
   steps=json.loads((dest/'FootProgress.json').read_text());n=steps[-1]['name'] if steps else None
   if n!=last:print(label,len(steps),n,flush=True);last=n
  if time.monotonic()-start>1200:raise TimeoutError('Native game left intact for inspection')
 assert p.returncode==0
result=json.loads((dest/'FootTest.json').read_text())
if slot.exists():
 assert hashlib.sha256(slot.read_bytes()).hexdigest()==result['save_after_sha256'],'Concurrent save change'
 if before['existed']:shutil.copy2(slot,dest/'DevSaveTestResult.sav');shutil.copy2(dest/'DevSaveOriginal.sav',slot);assert hashlib.sha256(slot.read_bytes()).hexdigest()==before['sha256']
 else:slot.rename(dest/'DevSaveTestResult.sav')
(dest/'SaveRestored.json').write_text(json.dumps({'restored':slot.exists()==before['existed'],'initial':before}));assert result['passed'],result['error'];print('NATIVE PASS',label,result['distance_m'],result['max_speed_cm_s'],flush=True)
