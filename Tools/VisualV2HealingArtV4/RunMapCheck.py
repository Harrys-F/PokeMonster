from ProcessGuard import editor_pids
"""Fresh-editor reload/Map Check of the saved central map. No save operation."""
from pathlib import Path
import subprocess,json,re,sys
R=Path(__file__).resolve().parents[2];O=R/('Saved/VisualV2HealingArtV4/'+(sys.argv[1] if len(sys.argv)>1 else 'MapChecks'));O.mkdir(exist_ok=False);assert not editor_pids()
(R/'Saved/VisualV2HealingArtV4/MapCheckRequest.json').write_text(json.dumps({'output':str(O)}))
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';name='Dev_TestMap_VisualV2';log=O/(name+'_Engine.log');args=[exe,str(R/'PokeMonster.uproject'),'/Game/Maps/'+name,'-NoSplash','-NoLiveCoding','-unattended','-ExecutePythonScript='+str(R/'Tools/VisualV2HealingArtV4/CheckCurrentMap.py'),'-ABSLOG='+str(log)]
with (O/'Console.log').open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=300)
s=log.read_text(errors='replace');assert p.returncode==0 and re.search(r'MapCheck:.*0 Fehler, 0 Warnung',s);assert not re.search(r'LogPython: Error|appError called|Fatal error:',s);d=json.loads((O/(name+'.json')).read_text());assert not d['dirty_maps'] and not d['dirty_content'];print('MAP CHECK PASS / saved scene matches exactly / 0 errors, 0 warnings',flush=True)
