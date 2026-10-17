from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV3';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';(O/'Endpoint.json').write_text(json.dumps({'port':8004}))
with (O/'EditorSession.log').open('a') as f:
 p=subprocess.Popen([exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_EnvironmentPerfV3','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8004','-stdout','-FullStdOutLogOutput'],stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(O/'EditorProcess.json').write_text(json.dumps({'pid':p.pid,'port':8004}));print('Editor',p.pid)
