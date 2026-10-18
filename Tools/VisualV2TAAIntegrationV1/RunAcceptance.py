"""Full existing Enhanced-Input route, real dev-slot preservation, no test teleports."""
import time,json,sys,hashlib,shutil,subprocess
from pathlib import Path
from Control import R,O,job
mode,label,width,height,sp=sys.argv[1:];width,height,sp=map(int,[width,height,sp]);assert mode in ['PIE','Standalone'];dest=O/'Acceptance'/label;dest.mkdir(parents=True,exist_ok=False);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before={'existed':slot.exists()}
if slot.exists():before['sha256']=hashlib.sha256(slot.read_bytes()).hexdigest();shutil.copy2(slot,dest/'DevSaveOriginal.sav')
(dest/'SaveBefore.json').write_text(json.dumps(before));request={'label':label,'width':width,'height':height,'quality':1,'percentage':sp,'mode':mode};(O/'AcceptanceRequest.json').write_text(json.dumps(request));(O/'Request.json').write_text(json.dumps({'label':label,'config':[width,height,1,sp]}));process=None
if mode=='PIE':job('Preset.py');time.sleep(8);job('StartPIE.py');time.sleep(4);job('StartAcceptance.py')
else:
 assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
 args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed',f'-ResX={width}',f'-ResY={height}','-ForceRes','-NoVSync','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8016','-ExecCmds='+','.join(['sg.'+n+'Quality 1' for n in ['ViewDistance','AntiAliasing','Shadow','GlobalIllumination','Reflection','PostProcess','Texture','Effects','Foliage','Shading']]+['py '+str(R/'Tools/VisualV2TAAIntegrationV1/NativeAcceptance.py')]),'-ABSLOG='+str(dest/'Engine.log')];f=(dest/'Console.log').open('w');process=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
start=time.monotonic();last=None
while not (dest/'FootTest.json').exists():
 time.sleep(3);p=dest/'FootProgress.json'
 if p.exists():
  steps=json.loads(p.read_text());n=steps[-1]['name'] if steps else None
  if n!=last:print(label,len(steps),n,flush=True);last=n
 if process and process.poll() is not None and not (dest/'FootTest.json').exists():raise RuntimeError('Unexpected game exit, preserve test slot for inspection')
 assert time.monotonic()-start<1100,'Timeout; preserve process and save for inspection'
r=json.loads((dest/'FootTest.json').read_text());time.sleep(3)
if mode=='PIE':job('StopPIE.py')
else:assert process.wait(timeout=45)==0;f.close()
if slot.exists():
 assert hashlib.sha256(slot.read_bytes()).hexdigest()==r['save_after_sha256'],'Concurrent save write'
 if before['existed']:shutil.copy2(slot,dest/'DevSaveTestResult.sav');shutil.copy2(dest/'DevSaveOriginal.sav',slot);assert hashlib.sha256(slot.read_bytes()).hexdigest()==before['sha256']
 else:slot.rename(dest/'DevSaveTestResult.sav')
(dest/'SaveRestored.json').write_text(json.dumps({'restored':slot.exists()==before['existed'],'initial':before}));assert r['passed'],r['error'];print(label,'PASS',r['distance_m'],r['max_speed_cm_s'],flush=True)
