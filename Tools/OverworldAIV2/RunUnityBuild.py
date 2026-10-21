"""Exercise the committed-code unity compilation path, not only adaptive exclusions."""
import subprocess,time,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];label=sys.argv[1];assert label.isalnum();O=R/'Saved/OverworldAIV2'/label;O.mkdir(exist_ok=False)
rows=subprocess.check_output(['ps','-axo','comm='],text=True).splitlines();assert not any(x.endswith('/Contents/MacOS/UnrealEditor')for x in rows),'Close the clean editor first'
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/Build.sh','PokeMonsterEditor','Mac','Development',str(R/'PokeMonster.uproject'),'-WaitMutex','-NoHotReloadFromIDE','-ForceUnity','-DisableAdaptiveUnity'];start=time.monotonic()
with (O/'Console.log').open('x')as out:code=subprocess.run(args,cwd=R,stdout=out,stderr=subprocess.STDOUT,timeout=1200).returncode
result={'exit':code,'seconds':time.monotonic()-start,'forced_unity':True,'adaptive_unity_disabled':True};(O/'Result.json').write_text(json.dumps(result,indent=2));assert code==0,result;print('FORCED_UNITY_BUILD_PASS',result,flush=True)
