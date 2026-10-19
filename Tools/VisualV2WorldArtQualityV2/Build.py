from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];O=R/'Saved/VisualV2WorldArtQualityV2/Build';O.mkdir(exist_ok=True);assert not (O/'Build.log').exists();assert 'Contents/MacOS/UnrealEditor ' not in subprocess.run(['pgrep','-alf','UnrealEditor'],text=True,capture_output=True).stdout
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/Build.sh','PokeMonsterEditor','Mac','Development',str(R/'PokeMonster.uproject'),'-WaitMutex','-NoHotReloadFromIDE']
with (O/'Build.log').open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200)
(O/'Result.json').write_text(json.dumps({'exit':p.returncode,'argv':args},indent=2));assert p.returncode==0;print('Development Editor build passed',flush=True)
