import unreal,json,time,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/IntegrationV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);s=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if x.get_world()==w);a=next(x for x in unreal.ObjectIterator(unreal.InputAction) if x.get_outer()==p and x.get_name()=='MoveAction')
v=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));c=v.visual;old=(c.get_skeletal_mesh_asset(),v.idle_animation,v.conversation_animation,v.get_actor_rotation());ids=['Ranger','WhiteHairedWarrior','ElvenArcher','DwarfWarrior'];i=-1;stage=time.monotonic();active=False;record=[]
def inject(x,y):s.inject_input_vector_for_action(a,unreal.Vector(x,y,0),[],[])
def finish(error=None):
 inject(0,0);c.set_skeletal_mesh_asset(old[0]);c.set_material(0,unreal.load_asset('/Game/Characters/NPCs/Ranger/Materials/MI_Ranger_V1'));v.idle_animation=old[1];v.conversation_animation=old[2];v.set_actor_rotation(old[3],True);unreal.unregister_slate_post_tick_callback(unreal._npc_review);del unreal._npc_review;(O/'ValidatedGameCameraReviews.json').write_text(json.dumps({'renders':record,'error':error,'method':'Walk from PlayerStart to existing Wanderer; temporary mesh swap at unchanged visual position, existing camera, disposable PIE.'},indent=2))
def tick(dt):
 global i,stage,active
 try:
  now=time.monotonic()
  if i<0:
   q=p.get_actor_location();dx=-820-q.x;dy=-1170-q.y
   if math.hypot(dx,dy)<24:inject(0,0);i=0;return
   yaw=math.radians(p.get_movement_basis_yaw());sx=-math.sin(yaw)*dx+math.cos(yaw)*dy;sy=math.cos(yaw)*dx+math.sin(yaw)*dy;ang=round(math.atan2(sx,sy)/(math.pi/4))*math.pi/4;inject(math.sin(ang),math.cos(ang));assert now-stage<15;return
  if i>=len(ids):finish();return
  id=ids[i]
  if not active:
   c.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/'+id+'/Meshes/SK_'+id+'_NPC_V1'));c.set_material(0,unreal.load_asset('/Game/Characters/NPCs/'+id+'/Materials/MI_'+id+'_V1'));v.idle_animation=unreal.load_asset('/Game/Characters/NPCs/'+id+'/Animations/A_'+id+'_Idle_V1');v.conversation_animation=unreal.load_asset('/Game/Characters/NPCs/'+id+'/Animations/A_'+id+'_Talk_V1');c.set_anim_instance_class(unreal.PokeMonsterNPCAnimInstance);v.refresh_presentation();v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=135,roll=0),True);stage=now;active=True;return
  if now-stage<4:return
  path=R/'Art/Characters/NPCs'/id/'Previews/Unreal_Validated_GameCamera.png';unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);record.append({'id':id,'file_request':str(path),'actor_position':v.get_actor_location().to_tuple(),'component_position':c.get_world_location().to_tuple(),'visible':c.is_visible(),'material':c.get_material(0).get_path_name(),'animation':c.get_anim_instance().get_class().get_name(),'player':p.get_actor_location().to_tuple()});i+=1;active=False
 except Exception as e:finish(str(e))
unreal._npc_review=unreal.register_slate_post_tick_callback(tick)
