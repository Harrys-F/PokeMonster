"""Real Unreal frame sequence in VisualV2. Runtime-only test actor; no new map or camera settings."""
import unreal,json,math,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/MeshyGlumandaV1/RuntimeReviewCandidateFinal';O.mkdir(exist_ok=True);assert not (O/'Result.json').exists()
w=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
unreal.SystemLibrary.execute_console_command(w,'pm.EnvPerf2.Viewport 2560 1440');unreal.SystemLibrary.execute_console_command(w,'r.ScreenPercentage 100');unreal.SystemLibrary.execute_console_command(w,'r.SecondaryScreenPercentage.GameViewport 100')
prefs=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=prefs.get_editor_property('bThrottleCPUWhenNotForeground');prefs.set_editor_property('bThrottleCPUWhenNotForeground',False)
wild=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));wild.set_actor_tick_enabled(False)
center=unreal.Vector(-810,-1520,0)
actor=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor));original=actor.get_actor_transform()
assert actor.set_presentation(unreal.load_asset('/Game/Characters/Creatures/Zunderlauf/MeshyV1/DA_Glumanda_Presentation'))
mesh=actor.mesh;flame=actor.effect_components[0];data=unreal.load_asset('/Game/Characters/Creatures/Zunderlauf/MeshyV1/DA_Glumanda_Presentation');assert mesh.get_skeletal_mesh_asset()==data.mesh
hit=unreal.SystemLibrary.line_trace_single(w,center+unreal.Vector(0,0,150),center-unreal.Vector(0,0,200),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[p,wild,actor],unreal.DrawDebugTrace.NONE,True);assert hit and hit.to_tuple()[0];center.z=hit.to_tuple()[5].z-data.ground_offset_cm
phases=[('Idle',4.5),('Walk',2.),('Run',1.6),('NativeRun',2.6),('Attack',1.2),('Hit',1.),('Faint',1.5),('Happy',1.4)]+[('Direction_'+str(a),1.4)for a in range(0,360,45)]
state={'i':0,'t':0.,'wall':time.monotonic(),'started':False,'nextshot':.35,'rows':[],'shots':0,'last_game_time':unreal.GameplayStatics.get_time_seconds(w),'native_run_max_blend':0.};samples=(O/'Frames.jsonl').open('w')
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._zunderlauf_review);samples.close();prefs.set_editor_property('bThrottleCPUWhenNotForeground',throttle);actor.set_species(unreal.load_asset('/Game/Data/Creatures/DA_Zunderlauf'));actor.set_actor_transform(original,False,True);state['passed']=error is None;state['error']=error;(O/'Result.json').write_text(json.dumps(state,indent=2))
def tick(dt):
 try:
  i=state['i'];now=unreal.GameplayStatics.get_time_seconds(w);dt=now-state['last_game_time'];state['last_game_time']=now
  if dt<=0:return
  if i==len(phases):finish();return
  name,duration=phases[i];state['t']+=dt;t=state['t']
  if not state['started']:
   state['started']=True;actor.set_actor_location(center,False,True);actor.set_actor_rotation(unreal.Rotator(yaw=135),True)
   if name.startswith('Direction_') or name=='NativeRun':mesh.set_animation_mode(unreal.AnimationMode.ANIMATION_BLUEPRINT);mesh.set_anim_instance_class(unreal.PokeMonsterCreatureAnimInstance.static_class())
   else:mesh.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE);mesh.play_animation(data.get_editor_property('clips')[getattr(unreal.PokeMonsterCreatureClip,name.upper())],name in ['Idle','Walk','Run'])
  if name.startswith('Direction_') or name=='NativeRun':
   yaw=135. if name=='NativeRun' else float(name.split('_')[1]);rad=math.radians(yaw);actor.set_actor_rotation(unreal.Rotator(yaw=yaw),True);actor.set_actor_location(actor.get_actor_location()+unreal.Vector(math.cos(rad),math.sin(rad),0)*(36 if name=='NativeRun' else 22)*dt,False,True)
  if (name.startswith('Direction_') or name=='NativeRun') and t>.6:
   anim=mesh.get_anim_instance();assert anim.walk_blend>.9 and anim.reaction_blend<.01,(name,anim.walk_blend,anim.reaction_blend)
   if name=='NativeRun':state['native_run_max_blend']=max(state['native_run_max_blend'],anim.run_blend)
  distance=(flame.get_world_location()-mesh.get_socket_location('tail_socket')).length();assert distance<.02,distance
  assert max(abs(v)for v in flame.get_world_scale().to_tuple())<1.01,'FBX socket scale must not inflate the effect'
  assert flame.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and mesh.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
  samples.write(json.dumps({'phase':name,'phase_time':t,'game_time':unreal.GameplayStatics.get_time_seconds(w),'wall_time':time.monotonic()-state['wall'],'actor':actor.get_actor_location().to_tuple(),'native_speed_cm_s':actor.motion_speed,'left_foot':mesh.get_socket_location('foot_L').to_tuple(),'right_foot':mesh.get_socket_location('foot_R').to_tuple(),'flame':flame.get_world_location().to_tuple(),'tail_socket_error_cm':distance,'viewport':list(pc.get_viewport_size())})+'\n')
  if t>=state['nextshot']:
   filename=name+'_'+str(state['shots']).zfill(3)+'.png';unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/filename)+'"',pc);state['rows'].append({'file':filename,'phase':name,'time':t,'viewport':list(pc.get_viewport_size()),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'rotation':pc.player_camera_manager.get_camera_rotation().to_tuple()});state['shots']+=1;state['nextshot']+=.25
  if name=='NativeRun' and t>=duration:assert state['native_run_max_blend']>.95,state['native_run_max_blend']
  if t>=duration:state.update(i=i+1,t=0.,started=False,nextshot=.35)
 except Exception:
  import traceback
  finish(traceback.format_exc());raise
unreal._zunderlauf_review=unreal.register_slate_post_tick_callback(tick)
