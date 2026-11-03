"""Owned Development-game launch, fresh save directory, no automatic process termination."""
from pathlib import Path
import subprocess,time,json,sys,re
R=Path(__file__).resolve().parents[2];D=R/'Saved/ProjectRefinement/VisualV2WorldRefinementV4';label,script=sys.argv[1:3];resume=False;assert len(sys.argv)==3;assert re.fullmatch('[A-Za-z0-9_]+',label)
source=(R/'Tools/VisualV2WorldRefinementV4'/script).resolve();assert source.is_relative_to(R/'Tools/VisualV2WorldRefinementV4')and source.is_file()
assert not any(x.strip().endswith('/Contents/MacOS/UnrealEditor')for x in subprocess.check_output(['ps','-axo','comm='],text=True).splitlines()),'Existing editor/game remains untouched'
O=D/label;O.mkdir(exist_ok=False);storage=D/'NativeTour03/UserData'if resume else O/'UserData'
if resume:assert json.loads((D/'NativeTour03/Tour_review.json').read_text())['passed']and(storage/'Saved/SaveGames/PokeMonster_Dev.sav').is_file()
(D/'Request.json').write_text(json.dumps({'label':label}));(D/'GameplayRequest.json').write_text(json.dumps({'label':label,'travel':True}));(D/'ActiveNative.json').write_text(json.dumps({'label':label,'script':script,'storage':str(storage)}));(O/'RuntimeUsed.py').write_text(source.read_text())
startup='''import unreal,runpy,time,sys,traceback,json
from pathlib import Path
sys.dont_write_bytecode=True
O=Path(%r);start=time.monotonic()
def wait(dt):
 if time.monotonic()-start<12:return
 W=next((w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)),None)
 if not W:return
 unreal.unregister_slate_post_tick_callback(unreal._westland_native_start)
 try:runpy.run_path(str(O/'RuntimeUsed.py'),run_name='__main__')
 except Exception:
  (O/'StartupFailure.json').write_text(json.dumps({'error':traceback.format_exc()}));unreal.SystemLibrary.quit_game(W,unreal.GameplayStatics.get_player_controller(W,0),unreal.QuitPreference.QUIT,False)
unreal._westland_native_start=unreal.register_slate_post_tick_callback(wait)
'''%str(O)
(O/'Startup.py').write_text(startup)
# Explicit target-map argument; leave the existing GameDefaultMap unchanged.
args=['/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor',str(R/'PokeMonster.uproject'),'/Game/Maps/Dev_TestMap_VisualV2','-game','-windowed','-NoSplash','-NoLiveCoding','-nosound','-nowrite','-NoAssetRegistryCacheWrite','-UserDir='+str(storage),'-ABSLOG='+str(O/'Engine.log'),'-ExecCmds=py '+str(O/'Startup.py')]
start=time.monotonic()
with(O/'Console.log').open('x')as f:p=subprocess.Popen(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
(O/'Launch.json').write_text(json.dumps({'pid':p.pid,'args':args},indent=2));print('Owned native PID',p.pid,flush=True)
while p.poll()is None:
 assert time.monotonic()-start<3000,f'Observation timeout; PID {p.pid} was NOT terminated'
 time.sleep(.5)
r={'returncode':p.returncode,'seconds':time.monotonic()-start};(O/'ProcessExit.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
