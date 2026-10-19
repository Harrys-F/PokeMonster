"""Open this project explicitly; avoid Project Browser / LaunchServices races."""

# Historical map prerequisites; explicit unavailable result, never an implicit new map.
from pathlib import Path as _MLPath
import sys as _MLSys
_MLSys.dont_write_bytecode = True
_MLSys.path.insert(0, str(next(p for p in _MLPath(__file__).resolve().parents if (p / 'PokeMonster.uproject').is_file()) / 'Tools/ProjectMaintenance'))
from MapLifecycle import require_historical_maps as _require_historical_maps
_require_historical_maps(__file__)

from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV1';exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor';(O/'Endpoint.json').write_text(json.dumps({'port':8001}))
with (O/'EditorSession_FinalReview.log').open('w') as f:
 p=subprocess.Popen([exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_EnvironmentPerfV1','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8001','-stdout','-FullStdOutLogOutput'],stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(O/'EditorProcess.json').write_text(json.dumps({'pid':p.pid,'port':8001}));print('Editor',p.pid)
