from ProcessGuard import editor_pids
"""Open an existing map in a fresh supervised editor. Never creates/saves a map."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[2];S=R/'Saved/VisualV2WorldArtV6';O=Path('/Users/harry/Documents/Codex/PokeMonster_WorldArt_V6_2026-10-19')
label=sys.argv[1];name=sys.argv[2] if len(sys.argv)>2 else 'Dev_TestMap_VisualV2'
assert name in ['Dev_TestMap_VisualV2'];assert not (O/(label+'.log')).exists();assert not editor_pids()
(S/'LaunchRequest.json').write_text(json.dumps({'map':name}));exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
with (O/(label+'_Console.log')).open('w') as f:
 p=subprocess.Popen([exe,str(R/'PokeMonster.uproject'),'/Game/Maps/'+name,'-NoSplash','-NoLiveCoding','-ExecCmds=py '+str(R/'Tools/VisualV2WorldArtV6/Startup.py'),'-ABSLOG='+str(O/(label+'.log'))],stdout=f,stderr=subprocess.STDOUT,cwd=R);print('Editor PID',p.pid,flush=True);print('Editor exit',p.wait(),flush=True)
