from pathlib import Path
import subprocess,json,re
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2VegetationPerfV1/MapChecks';O.mkdir(exist_ok=True)
assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
for name in ['Dev_TestMap_VisualV2','Dev_TestMap_VisualV2GPUBottleneckV1','Dev_WestlandAssetLibrary']:
 log=O/(name+'_Engine.log');assert not log.exists()
 args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/'+name,'-NoSplash','-NoLiveCoding','-unattended','-ExecutePythonScript='+str(R/'Tools/VisualV2VegetationPerfV1/CheckCurrentMap.py'),'-ABSLOG='+str(log)]
 with (O/(name+'_Console.log')).open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=240)
 assert p.returncode==0,(name,p.returncode)
 s=log.read_text(errors='replace');assert 'MapCheck:' in s and re.search(r'MapCheck:.*0 Fehler, 0 Warnung',s),name
 assert not re.search(r'LogPython: Error|appError called|Fatal error:',s),name
 assert json.loads((O/(name+'.json')).read_text())['map'].startswith('/Game/Maps/'+name)
 print('MAP CHECK PASS',name,flush=True)
