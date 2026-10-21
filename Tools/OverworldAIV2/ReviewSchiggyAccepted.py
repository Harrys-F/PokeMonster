"""Paired QHD world-camera images using the actual game AnimInstance, never SingleNode poses."""
import unreal,json,math,time
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/OverworldAIV2/SchiggyNativeQHD';O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w);inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');original=p.get_actor_location();old=unreal.load_asset('/Game/Characters/Creatures/Schiggy/MeshyV1/DA_Schiggy_Presentation');new=unreal.load_asset('/Game/Characters/Creatures/Schiggy/SurfaceV2/DA_Schiggy_Presentation');state={'phase':'walk','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'i':0,'posed':False,'shot':False,'rows':[]}
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True)
for c in ['pm.StarterReview.Party Schiggy Bisasam Zunderlauf','pm.EnvPerf2.Viewport 2560 1440','r.ScreenPercentage 100']:unreal.SystemLibrary.execute_console_command(w,c)
def inject(dx=0,dy=0):
 yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;n=max(120,math.hypot(sx,sy));inp.inject_input_vector_for_action(move,unreal.Vector(sx/n,sy/n,0),[],[])
def finish(error=None):
 inject();v=comp.get_visual()
 if v:v.set_presentation(new);comp.get_movement().set_component_tick_enabled(True)
 p.set_actor_location(original,False,True);unreal.unregister_slate_post_tick_callback(unreal._ai_schiggy_native);state.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(state,indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);state['time']+=now-state['last'];state['last']=now;assert time.monotonic()-state['wall']<90;v=comp.get_visual()
  if not v:return
  if state['phase']=='walk':
   q=p.get_actor_location();dx=-760-q.x;dy=-820-q.y
   if math.hypot(dx,dy)>18:inject(dx,dy);return
   inject();state.update(phase='follow',time=0.);return
  if state['phase']=='follow':
   if v.get_actor_location().distance(p.get_actor_location())>220 or state['time']<2:return
   comp.get_movement().set_component_tick_enabled(False);state.update(phase='photos',time=0.)
  label,profile=[('Before',old),('After',new)][state['i']]
  if not state['posed']:assert v.set_presentation(profile);state['posed']=True
  if state['time']>5 and not state['shot']:
   assert isinstance(v.mesh.get_anim_instance(),unreal.PokeMonsterCreatureAnimInstance);assert pc.get_viewport_size()==(2560,1440);unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(O/(label+'.png'))+'"',pc);state['rows'].append({'label':label,'actor':v.get_actor_location().to_tuple(),'scale':v.get_actor_scale3d().to_tuple(),'camera':pc.player_camera_manager.get_camera_location().to_tuple(),'viewport':list(pc.get_viewport_size()),'anim_instance':v.mesh.get_anim_instance().get_class().get_name(),'pose':'actual native Idle, breathing continues'});state['shot']=True
  if state['time']>6:
   if state['i']==0:state.update(i=1,time=0.,posed=False,shot=False)
   else:finish()
 except Exception as ex:finish(str(ex));raise
unreal._ai_schiggy_native=unreal.register_slate_post_tick_callback(tick)
