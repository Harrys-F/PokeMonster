"""Real normal-PIE test-ground review. Does not spawn, save, or alter authored assets."""
import unreal,json,time,math,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/AnimationCorrectionsV61';q=json.loads((O/'ReviewRequest.json').read_text());D=O/q['label'];D.mkdir(exist_ok=False);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w;g=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureTestGround)if x.get_outer()==w);assert len(g.specimens)==10;assert g.visit(0),'Test-ground access blocked; no review may continue';p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);cm=p.get_component_by_class(unreal.CharacterMovementComponent);mesh=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);save=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=lambda:hashlib.sha256(save.read_bytes()).hexdigest();before=sha();rows=[];shots=[];steps=[];index=0;due=0;sample_due=0;stage='setup';start=time.monotonic();record=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/q['label'];assert not record.exists();settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
original_clips={role:mesh.get_editor_property(role+'_animation')for role in ['idle','walk','run']}
if q.get('integrated'):assert all('/AnimationV6/'in a.get_path_name()for a in original_clips.values()),'Native player defaults were not adopted'
if q.get('baseline'):
 mesh.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2'))
 assert g.specimens[9].set_presentation(unreal.load_asset('/Game/Characters/Creatures/Glurak/AnimationV6/DA_Glurak_Presentation_V6'))
if q.get('after'):assert '/AnimationV61/'in mesh.get_skeletal_mesh_asset().get_path_name()

def cmd(s):unreal.SystemLibrary.execute_console_command(w,s,pc)
def action(name,fn,wait=.5):steps.append((name,fn,wait))
def shot(name):
 assert pc.get_viewport_size()==(2560,1440);dest=D/(name+'.png');cmd('Shot filename='+str(dest));shots.append(dict(name=name,path=str(dest.with_name(dest.stem+'00000.png')),camera=pc.player_camera_manager.get_camera_location().to_tuple(),rotation=pc.player_camera_manager.get_camera_rotation().to_tuple(),player=p.get_actor_location().to_tuple()))
def visit(i):
 assert g.visit(i),'Visit failed; stop instead of capturing the wrong scene'
def face(i,yaw):
 v=g.specimens[i-1];v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=yaw,roll=0),False);assert abs(v.get_actor_rotation().pitch)<.01 and abs(v.get_actor_rotation().roll)<.01
action('contact mode',lambda:cmd('pm.PlayerFootIK '+('0'if q.get('baseline')else'1')));action('qhd',lambda:cmd('pm.EnvPerf2.Viewport 2560 1440'),2);action('screen100',lambda:cmd('r.ScreenPercentage 100'));action('visit',lambda:visit(0),2);action('record',lambda:cmd('pm.TAAReview.CaptureStart '+str(record)));action('idle',lambda:g.set_mode('idle'))
for i,name in [(1,'Glumanda'),(2,'Schiggy'),(3,'Bisasam'),(4,'Pikachu'),(5,'Myrapla'),(6,'Enton'),(7,'Machomei'),(8,'Nebulak'),(9,'Gengar'),(10,'Glurak')]:
 if q.get('targets')and name not in q['targets']:continue
 action(name+' visit',lambda i=i:visit(i),1)
 for view,yaw in ([('Direction'+str(j),j*45)for j in range(8)]if q.get('eight_views')else[('Front',135),('Side',45),('Rear',-45)]):
  action(name+view,lambda i=i,yaw=yaw:face(i,yaw),1.5);action(name+view+' shot',lambda name=name,view=view:shot(name+view),.3)
 action(name+' walk',lambda:g.set_mode('walk'),5 if i!=10 else q.get('glurak_seconds',14));action(name+' walk shot',lambda name=name:shot(name+'Walk'),.5);action(name+' run',lambda:g.set_mode('run'),4);action(name+' run shot',lambda name=name:shot(name+'Run'),.5);action(name+' idle',lambda:g.set_mode('idle'),1)
 if i in [7,10]:action(name+' attack',lambda:g.react('attack'),1.5)
def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
if not q.get('skip_player'):
 action('player center',lambda:visit(0),1)
 action('player idle',lambda:shot('PlayerIdle'),.5)
 def axis(x,y):cmd('pm.Input.Axis Gamepad_LeftX '+str(x));cmd('pm.Input.Axis Gamepad_LeftY '+str(y))
 for sprint in [False,True]:
  if sprint:action('sprint press',lambda:cmd('pm.Input.Key LeftShift down'),.2)
  for i in range(8):
   a=i*math.pi/4;action(('Sprint'if sprint else'Walk')+str(i),lambda a=a:axis(math.cos(a),math.sin(a)),1.1);action('player shot '+str(i),lambda i=i,sprint=sprint:shot(('PlayerSprint'if sprint else'PlayerWalk')+str(i)),.1)
  action('stop',lambda:axis(0,0),1)
  if sprint:action('sprint release',lambda:cmd('pm.Input.Key LeftShift up'),.3)
if not q.get('skip_player'):
 for i,(x,y)in enumerate([(1,0),(0,-1),(-1,0),(1,1),(0,0)]):
  action('tight turn '+str(i),lambda x=x,y=y:axis(x,y),.4)
 action('stop after tight',lambda:axis(0,0),.6)
 action('restart',lambda:axis(1,0),.5)
 action('accelerate',lambda:cmd('pm.Input.Key LeftShift down'),.7)
 action('decelerate',lambda:cmd('pm.Input.Key LeftShift up'),.7)
 action('final stop',lambda:axis(0,0),1)
action('return',lambda:g.return_to_world(),1)
def finish(error=None):
 axis(0,0);cmd('pm.Input.Key LeftShift up');cmd('pm.TAAReview.CaptureStop');cmd('pm.PlayerFootIK 1');
 for role,clip in original_clips.items():mesh.set_editor_property(role+'_animation',clip)
 cmd('pm.EnvPerf2.Viewport 0 0');settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);unreal.unregister_slate_post_tick_callback(unreal._v6_review);delattr(unreal,'_v6_review');(D/'Result.json').write_text(json.dumps(dict(passed=error is None,error=error,save_unchanged=sha()==before,shots=shots,samples=rows,recording=str(record),ordinary_pie_native_test_ground=True,simulated_input_not_hardware=True,player_clips={k:v.get_path_name()for k,v in original_clips.items()}),indent=2));unreal.log('V6_REVIEW_DONE '+str(error))
def tick(dt):
 global index,due,sample_due,stage
 try:
  now=unreal.GameplayStatics.get_time_seconds(w)
  assert time.monotonic()-start<720
  if now>=sample_due:
   sample_due=now+.1;rows.append(dict(time=now,stage=stage,player=p.get_actor_location().to_tuple(),player_speed=p.get_velocity().length(),player_grounded=cm.movement_mode==unreal.MovementMode.MOVE_WALKING,visual_origin=mesh.get_world_location().to_tuple(),feet={side:mesh.get_socket_location('foot_'+side).to_tuple()for side in ['l','r']},visual_yaw=mesh.get_world_rotation().yaw,gait_time=mesh.get_anim_instance().get_editor_property('walk_time'),specimens=[dict(position=v.get_actor_location().to_tuple(),speed=m.current_speed,hover=v.get_ground_hover_height(),hover_state=v.get_ground_hover_state())for v,m in zip(g.specimens,g.movements)]))
  if now<due:return
  if index==len(steps):finish();return
  stage,fn,delay=steps[index];fn();index+=1;due=now+delay;(D/'Progress.json').write_text(json.dumps(dict(step=index,total=len(steps),stage=stage)))
 except Exception:finish(traceback.format_exc())
unreal._v6_review=unreal.register_slate_post_tick_callback(tick)
