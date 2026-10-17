"""Open this project explicitly; avoid Project Browser / LaunchServices races."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';(O/'Endpoint.json').write_text(json.dumps({'port':8001}))
with (O/'EditorSession_FinalReview.log').open('w') as f:
 p=subprocess.Popen([exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_EnvironmentPerfV2','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8001','-stdout','-FullStdOutLogOutput'],stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(O/'EditorProcess.json').write_text(json.dumps({'pid':p.pid,'port':8001}));print('Editor',p.pid)
