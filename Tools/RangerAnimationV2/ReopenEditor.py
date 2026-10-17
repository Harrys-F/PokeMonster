from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];O=R/'Saved/RangerAnimationV2';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';(O/'Endpoint.json').write_text(json.dumps({'port':8005}))
with (O/'EditorSession.log').open('a') as f:
 p=subprocess.Popen([exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_NPCMotionV2','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8005','-stdout','-FullStdOutLogOutput'],stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(O/'EditorProcess.json').write_text(json.dumps({'pid':p.pid,'port':8005}));print('Editor',p.pid)
