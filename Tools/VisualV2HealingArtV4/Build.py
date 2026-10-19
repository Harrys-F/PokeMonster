from ProcessGuard import editor_pids
from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parents[2];O=R/('Saved/VisualV2HealingArtV4/'+(sys.argv[1] if len(sys.argv)>1 else 'Build'));O.mkdir(exist_ok=True);assert not (O/'Build.log').exists();assert not editor_pids()
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/Build.sh','PokeMonsterEditor','Mac','Development',str(R/'PokeMonster.uproject'),'-WaitMutex','-NoHotReloadFromIDE']
with (O/'Build.log').open('w') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=1200)
(O/'Result.json').write_text(json.dumps({'exit':p.returncode,'argv':args},indent=2));assert p.returncode==0;print('Development Editor build passed',flush=True)
