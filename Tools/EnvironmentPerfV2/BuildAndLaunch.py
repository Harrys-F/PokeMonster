"""Use only after CloseForBuild verified there is no PIE or unsaved package.
Wait for the actual old process to exit; avoid a hot-reload build / HTTP listener bind race.
"""
import subprocess,os,time,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'Saved/EnvironmentPerfV2';old=json.loads((O/'EditorProcess.json').read_text())['pid'];start=time.monotonic()
while True:
 try:os.kill(old,0)
 except ProcessLookupError:break
 assert time.monotonic()-start<40,'Do not build against a still-running editor'
 time.sleep(.5)
with (O/'Build_FinalProfile.log').open('w') as f:
 result=subprocess.run(['/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/Build.sh','PokeMonsterEditor','Mac','Development',str(R/'PokeMonster.uproject'),'-WaitMutex','-NoHotReloadFromIDE'],stdout=f,stderr=subprocess.STDOUT)
assert result.returncode==0,'Build failed; keep files and inspect Build_FinalProfile.log'
(O/'Endpoint.json').write_text(json.dumps({'port':8001,'reason':'Temporary loopback port avoids old listener TIME_WAIT on rapid restart'}))
exe='/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor'
with (O/'EditorSession_FinalProfile.log').open('w') as f:
 p=subprocess.Popen([exe,str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_EnvironmentPerfV2','-NoSplash','-NoLiveCoding','-ModelContextProtocolPort=8001','-stdout','-FullStdOutLogOutput'],stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(O/'EditorProcess.json').write_text(json.dumps({'pid':p.pid,'port':8001}));print('Build succeeded; editor',p.pid,flush=True)
