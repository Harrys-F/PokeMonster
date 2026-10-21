"""Actual Enhanced Input player sequence on the existing transient review ground."""
import unreal,json,time,math,hashlib,traceback,csv
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/MotionRefinementV5';q=json.loads((O/'PlayerRequest.json').read_text());D=O/q['label'];D.mkdir(exist_ok=False);E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();assert w and 'Dev_TestMap_VisualV2'in w.get_name();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);mesh=p.get_component_by_class(unreal.PokeMonsterMeshyVisualComponent);cm=p.get_component_by_class(unreal.CharacterMovementComponent);original=p.get_actor_transform();original_walk=cm.max_walk_speed;slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();gi=unreal.GameplayStatics.get_game_instance(w);enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);assert not enc.is_encounter_active();comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w);comp.set_enabled(False)
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):a.set_actor_tick_enabled(False);a.set_actor_enable_collision(False);a.overworld_movement.set_movement_paused(True)
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterWildEncounterZone):a.set_actor_enable_collision(False)
inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);actions={x.get_name():x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p};move=actions['MoveAction'];sprint=actions['SprintHoldAction']
original_clips={role:mesh.get_editor_property(role+'_animation')for role in ['idle','walk','run']}
assert all('/MotionV3/'in x.get_path_name()for x in original_clips.values()),'Actual player must use the reviewed current clips'
if q.get('original_clips'):
 for role,name in [('idle','A_Player_Meshy_Idle_V2'),('walk','A_Player_Meshy_Walk_V2'),('run','A_Player_Meshy_Run_V1')]:
  clip=unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV2/Animations/'+name);assert clip and clip.get_editor_property('skeleton')==mesh.get_skeletal_mesh_asset().skeleton;mesh.set_editor_property(role+'_animation',clip)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def inject(dx=0,dy=0,run=False):
 yaw=math.radians(p.get_movement_basis_yaw());inp.inject_input_vector_for_action(move,unreal.Vector(-math.sin(yaw)*dx+math.cos(yaw)*dy,math.cos(yaw)*dx+math.sin(yaw)*dy,0),[],[]);inp.inject_input_vector_for_action(sprint,unreal.Vector(1 if run else 0,0,0),[],[])
surface=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.StaticMeshActor)if a.get_actor_label()=='V2_Ground');origin,extent=surface.get_actor_bounds(False);start=unreal.Vector(-4300,-2300,origin.z+extent.z+p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+.15);assert origin.x-extent.x+30<start.x-1250 and start.x+1100<origin.x+extent.x-30;assert origin.y-extent.y+30<start.y-50 and start.y+2150<origin.y+extent.y-30;p.set_actor_location(start,False,True);cm.stop_movement_immediately();cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');s=dict(recording=[],t=0.,last=unreal.GameplayStatics.get_time_seconds(w),wall=time.monotonic(),rows=[],shots=[],fixture='Explicit existing review ground placement, real Enhanced Input, unchanged player physics; no save writes');last_sample=-1.;stamps=[3,5,7,9.2,10.5,12,14,16.2,17.5]+[19+i*4 for i in range(8)]
s['ground_surface']=dict(actor=surface.get_actor_label(),origin=origin.to_tuple(),extent=extent.to_tuple());s['clip_references']={role:mesh.get_editor_property(role+'_animation').get_path_name()for role in ['idle','walk','run']};s['comparison_scope']='Original V2/V1 clips on current steering/blend layer'if q.get('original_clips')else'Current MotionV3 clips and current steering/blend layer';s['expected_capsule_z']=p.get_actor_location().z
def finish(error=None):
 if q.get('native_record'):cmd('pm.TAAReview.CaptureStop')

 if s['recording']:
  with (D/'Frames.csv').open('w')as f:
   writer=csv.writer(f);writer.writerow(['frame','time','stage','width','height','file']);writer.writerows(s['recording'])
 for role,clip in original_clips.items():mesh.set_editor_property(role+'_animation',clip)
 inject();cm.stop_movement_immediately();p.set_actor_transform(original,False,True);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);unreal.unregister_slate_post_tick_callback(unreal._motion_player);s.update(passed=error is None,error=error,save_unchanged=hashlib.sha256(slot.read_bytes()).hexdigest()==before,initial_walk_speed=original_walk,final_walk_speed=cm.max_walk_speed);(D/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('MOTION_PLAYER_DONE '+str(error))
def tick(dt):
 global last_sample
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;t=s['t'];assert time.monotonic()-s['wall']<180;assert not enc.is_encounter_active()
  if t>.6:
   assert cm.movement_mode==unreal.MovementMode.MOVE_WALKING,('Review left walkable ground',t,p.get_actor_location().to_tuple(),str(cm.movement_mode))
   z=p.get_actor_location().z;s.setdefault('settled_ground_z',z);assert abs(z-s['settled_ground_z'])<1.,('Unexpected floor height',t,p.get_actor_location().to_tuple());gap=z-p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()-(origin.z+extent.z);assert -.1<=gap<=4.,('Capsule left actual flat ground surface',gap)
  if t<4:inject();stage='idle'
  elif t<9:inject(1,0);stage='walk'
  elif t<11:inject();stage='stop'
  elif t<16:inject(-1,0,True);stage='sprint'
  elif t<18:inject();stage='stop'
  elif t<50:
   i=int((t-18)//4);a=i*math.pi/4;inject(math.cos(a),math.sin(a));stage='direction_'+str(i)
  else:inject();stage='final_stop'
  if q.get('native_record')and t>=3 and not s.get('native_recording'):
   cmd('pm.TAAReview.CaptureStart '+q['native_record']);s['native_recording']=q['native_record']
  if t-last_sample>=.033:
   last_sample=t;a=mesh.get_anim_instance();s['rows'].append(dict(t=t,stage=stage,grounded=cm.movement_mode==unreal.MovementMode.MOVE_WALKING,speed=math.hypot(p.get_velocity().x,p.get_velocity().y),player=p.get_actor_location().to_tuple(),visual_yaw=mesh.get_world_rotation().yaw,walk_alpha=a.walk_alpha,run_alpha=a.run_alpha,walk_phase=a.walk_time,feet={n:mesh.get_socket_location(n).to_tuple()for n in ['foot_l','foot_r']},camera=pc.player_camera_manager.get_camera_location().to_tuple()))
  if q.get('record')and t>=3 and (not s['recording']or t-s['recording'][-1][1]>=.18):
   idx=len(s['recording']);stem='Sequence'+str(idx).zfill(5);assert pc.get_viewport_size()==(2560,1440);cmd('Shot filename='+str(D/(stem+'.png')));s['recording'].append([idx,t,stage,2560,1440,stem+'00000.png'])
  for stamp in ([] if q.get('record')else stamps):
   if t>=stamp and stamp not in s['shots']:
    assert pc.get_viewport_size()==(2560,1440);cmd('Shot filename='+str(D/('Time'+str(stamp)+'_QHD.png')));s['shots'].append(stamp);break
  if t>53:
   assert max(x['speed']for x in s['rows'])>310
   for i in range(8):
    rows=[x for x in s['rows']if x['stage']=='direction_'+str(i)];assert len(rows)>=3 and all(x['grounded']for x in rows),i
   s['eight_directions_grounded']=True;finish()
 except Exception:finish(traceback.format_exc())
unreal._motion_player=unreal.register_slate_post_tick_callback(tick)
