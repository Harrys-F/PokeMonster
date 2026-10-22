"""Observe existing native PIE specimens and exercise public dev commands + real Enhanced Input.
No spawning, party fixtures, asset writes or save writes. Screenshots remain under Saved.
"""
import unreal,json,time,traceback,hashlib,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/TestGroundV1';request=json.loads((O/'AcceptanceRequest.json').read_text());label=request['label'];assert label.isalnum();D=O/label
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w
proof_label=request.get('observation','OrdinaryPIEBeforeAnyReview');assert proof_label.isalnum();proof=json.loads((O/(proof_label+'.json')).read_text());assert proof['world']==w.get_path_name(),'Prove this ordinary PIE world first'
g=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==w)
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
f=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=lambda:hashlib.sha256(f.read_bytes()).hexdigest()if f.exists()else None
D.mkdir(exist_ok=False)
before=sha();party=lambda:[(c.instance_id.to_string(),c.current_hp,c.experience)for c in e.get_player_party()];initial_party=party();original=p.get_actor_location();assert len(g.specimens)==10
wild=lambda:sorted(x.get_path_name()for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor))
original_wild=wild();route=[];result=dict(checks=[],screenshots=[],samples=[],simulated_input_not_physical_hardware=True,ordinary_pie_no_spawn_fixture=True);index=0;next_game=0;started=time.monotonic();walk_start=None
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(s):unreal.SystemLibrary.execute_console_command(w,s,pc)
def action(n,fn,wait=.3):route.append((n,fn,wait))
def check(n,fn):
 def run():
  assert fn(),n
  result['checks'].append(n)
 action(n,run)
def shot(name):
 assert pc.get_viewport_size()==(2560,1440),pc.get_viewport_size()
 dest=D/(name+'.png');cmd('Shot filename='+str(dest));result['screenshots'].append(dict(name=name,file=str(dest.with_name(dest.stem+'00000'+dest.suffix)),viewport=[2560,1440],camera=pc.player_camera_manager.get_camera_location().to_tuple(),rotation=pc.player_camera_manager.get_camera_rotation().to_tuple(),player=p.get_actor_location().to_tuple()))
def axis(v):cmd('pm.Input.Axis Gamepad_LeftY '+str(v))
def save_walk():
 global walk_start
 walk_start=p.get_actor_location()
action('QHD actual framebuffer',lambda:cmd('pm.EnvPerf2.Viewport 2560 1440'),2)
action('go command',lambda:cmd('pm.TestGround.Go'),2)
check('Return anchor stored',lambda:g.has_return_position())
check('Native center reached',lambda:abs(p.get_actor_location().x+7500)<5 and abs(p.get_actor_location().y+4000)<5)
action('center game camera',lambda:shot('Center'),1)
action('walk baseline',save_walk)
action('ordinary Enhanced Input walking',lambda:axis(.75),1.7)
action('stop walking',lambda:axis(0),.4)
check('Actual player moved across collidable floor',lambda:(p.get_actor_location()-walk_start).length()>70 and abs(p.get_actor_location().z-original.z)<200)
action('B interact on test specimens is harmless',lambda:cmd('pm.Input.Key Gamepad_FaceButton_Right down'),.2)
action('release B',lambda:cmd('pm.Input.Key Gamepad_FaceButton_Right up'),.5)
for i in range(1,11):
 action('visit '+str(i),lambda i=i:cmd('pm.TestGround.Go '+str(i)),1)
 action('run '+str(i),lambda:cmd('pm.TestGround.Mode run'),8)
 action('refresh current specimen position '+str(i),lambda i=i:cmd('pm.TestGround.Go '+str(i)),.4)
 action('capture station '+str(i),lambda i=i:shot('Station'+str(i).zfill(2)),.5)
check('Every specimen used real bounded movement',lambda:all(m.distance_travelled>2 for m in g.movements))
check('All specimens stay in their own regions',lambda:all(math.hypot(v.get_actor_location().x-m.habitat_origin.x,v.get_actor_location().y-m.habitat_origin.y)<=435 for v,m in zip(g.specimens,g.movements)))
action('idle',lambda:cmd('pm.TestGround.Mode idle'),1)
check('Idle stops translation',lambda:all(m.current_speed<.01 for m in g.movements))
for role in ['attack','hit','faint','happy']:
 action(role,lambda role=role:cmd('pm.TestGround.React '+role),.45)
 action('capture '+role,lambda role=role:shot(role.title()),3)
action('auto',lambda:cmd('pm.TestGround.Mode auto'),1)
action('return',lambda:cmd('pm.TestGround.Return'),1)
check('Return restores original position',lambda:(p.get_actor_location()-original).length()<3 and not g.has_return_position())
check('Party identity HP and XP unchanged',lambda:party()==initial_party)
check('Wild actor population unchanged',lambda:wild()==original_wild)
check('No encounter or capture caused',lambda:not e.is_encounter_active())
check('Save file byte-for-byte unchanged',lambda:sha()==before)
def finish(error=None):
 axis(0);cmd('pm.EnvPerf2.Viewport 0 0');settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
 unreal.unregister_slate_post_tick_callback(unreal._permanent_ground_acceptance);delattr(unreal,'_permanent_ground_acceptance')
 result.update(passed=error is None,error=error,save_before=before,save_after=sha(),party_unchanged=party()==initial_party,wild_unchanged=wild()==original_wild,elapsed_wall_seconds=time.monotonic()-started)
 (D/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('TESTGROUND_ACCEPTANCE_DONE '+str(error))
def tick(dt):
 global index,next_game
 try:
  now=unreal.GameplayStatics.get_time_seconds(w)
  if time.monotonic()-started>900:raise TimeoutError('PIE acceptance exceeded 15 minutes')
  result['samples'].append(dict(time=now,movement=[m.distance_travelled for m in g.movements],hover=g.specimens[-1].get_ground_hover_state(),height=g.specimens[-1].get_ground_hover_height()))
  if now<next_game:return
  if index==len(route):finish();return
  name,fn,delay=route[index];fn();index+=1;next_game=now+delay
  (D/'Progress.json').write_text(json.dumps(dict(step=index,name=name,time=now)))
 except Exception:finish(traceback.format_exc())
assert not hasattr(unreal,'_permanent_ground_acceptance');unreal._permanent_ground_acceptance=unreal.register_slate_post_tick_callback(tick)
