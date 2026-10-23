"""Spatial contact audit through real Enhanced Input, without screenshot/recorder readback hitches."""
import unreal,json,time,math,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/AnimationCorrectionsV61';q=json.loads((O/'FootProbeRequest.json').read_text());D=O/q['label'];D.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;g=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==w);assert g.visit(0)and g.set_mode('idle');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);m=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);cm=p.get_component_by_class(unreal.CharacterMovementComponent);a=m.get_anim_instance();steps=[];rows=[];index=0;due=0;stage='setup';start=time.monotonic();save=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(save.read_bytes()).hexdigest();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(s):unreal.SystemLibrary.execute_console_command(w,s,pc)
def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
def action(n,f,d):steps.append((n,f,d))
action('enable',lambda:cmd('pm.PlayerFootIK '+str(int(q['enabled']))),1)
for run in [False,True]:
 if run:action('sprint',lambda:cmd('pm.Input.Key LeftShift down'),.2)
 for i in range(8):
  angle=i*math.pi/4;action(('Run'if run else'Walk')+str(i),lambda angle=angle:axis(math.cos(angle),math.sin(angle)),1.5)
 action('Stop',lambda:axis(0,0),.7)
 if run:action('walk',lambda:cmd('pm.Input.Key LeftShift up'),.2)
for i,(x,y)in enumerate([(1,0),(0,-1),(-1,0),(1,1),(0,0)]):action('Tight'+str(i),lambda x=x,y=y:axis(x,y),.4)
action('StopFinal',lambda:axis(0,0),1)
def finish(error=None):
 axis(0,0);cmd('pm.Input.Key LeftShift up');cmd('pm.PlayerFootIK 1');settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._v61_probe);(D/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,enabled=q['enabled'],samples=rows,save_unchanged=hashlib.sha256(save.read_bytes()).hexdigest()==sha,scope='spatial animation/contact measurement, not an FPS benchmark or physical controller test'),indent=2))
def tick(dt):
 global index,due,stage
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);assert time.monotonic()-start<150
  rows.append(dict(time=now,stage=stage,root=p.get_actor_location().to_tuple(),visual=m.get_world_location().to_tuple(),yaw=m.get_world_rotation().yaw,speed=p.get_velocity().length(),phase=a.get_editor_property('walk_time')/m.walk_animation.get_play_length(),run_alpha=a.get_editor_property('run_alpha'),walk_alpha=a.get_editor_property('walk_alpha'),contact=[a.get_editor_property('foot_contact_left'),a.get_editor_property('foot_contact_right')],feet=[m.get_socket_location('foot_'+side).to_tuple()for side in ['l','r']],grounded=cm.movement_mode==unreal.MovementMode.MOVE_WALKING))
  if now<due:return
  if index==len(steps):finish();return
  stage,f,d=steps[index];f();index+=1;due=now+d
 except Exception:finish(traceback.format_exc())
unreal._v61_probe=unreal.register_slate_post_tick_callback(tick)
