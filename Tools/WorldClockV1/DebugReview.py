"""Fresh ordinary PIE: developer commands reuse existing RAM save protection."""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/WorldClockV1/Debug01';O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
C=sub(unreal.PokeMonsterWorldClock);S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem)
def hashes():return{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in(R/'Saved/SaveGames').glob('*')if p.is_file()}
before=hashes();route=[];state={};result={'checks':[],'normal_storage_context':True,'no_isolated_disk_slot_created':True};s={'i':0,'wall':time.monotonic(),'last':time.monotonic()}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock '+t,PC)
def act(n,f,d=.45):route.append((n,f,d))
def check(n,p):
 def f():assert p(),n;result['checks'].append(n)
 act(n,f)
P.set_actor_location(unreal.Vector(-200,-100,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
act('Remember initial personal data',lambda:state.update(party=[x.export_text()for x in E.get_player_party()],time=C.get_time().export_text()))
act('Show time day phase and speed',lambda:cmd('show'))
def pause():state['time']=C.get_time().export_text();cmd('pause')
act('Begin protected RAM preview via developer pause',pause)
act('Set explicit day/time',lambda:cmd('set 22 18 0'));check('Exact requested day time phase',lambda:C.get_day()==22 and C.get_hour()==18 and C.get_phase()==unreal.PokeMonsterDayPhase.DUSK)
act('Reject invalid target',lambda:cmd('set 0 99 -1'));check('Invalid target preserves time',lambda:C.get_time().export_text()=='(Day=22,SecondsOfDay=64800.000000)')
for speed in [5,10,60,.5]:
 act('Set debug speed '+str(speed),lambda v=speed:cmd('speed '+str(v)));check('Exact temporary multiplier '+str(speed),lambda v=speed:C.get_debug_speed()==v)
act('Save using existing normal UI service',lambda:state.update(saved=S.save_current_game(),message=S.get_last_storage_message()))
check('Normal save is redirected to existing RAM preview',lambda:state['saved']and'RAM'in state['message']and hashes()==before)
act('Reset speed and debug pause only',lambda:cmd('reset'));check('Reset releases only debug control at 1x',lambda:C.get_debug_speed()==1 and not C.is_clock_paused())
act('End existing RAM preview',lambda:cmd('end'),1.)
check('End restores initial clock and party with normal speed',lambda:C.get_time().day==1 and C.get_hour()==9 and[x.export_text()for x in E.get_player_party()]==state['party']and C.get_debug_speed()==1 and not C.is_clock_paused())
check('All pre-existing save files byte-identical and no new file',lambda:hashes()==before)
def tick(dt):
 try:
  now=time.monotonic();assert now-s['wall']<90
  n,f,d=route[s['i']]
  if now-s['last']<d:return
  f();s['last']=time.monotonic();s['i']+=1
  if s['i']==len(route):finish()
 except Exception:finish(traceback.format_exc())
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._clock_debug);result.update(passed=error is None,error=error,save_files_unchanged=hashes()==before);(O/'Result.json').write_text(json.dumps(result,indent=2))
unreal._clock_debug=unreal.register_slate_post_tick_callback(tick)
