import unreal,json,time,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/IntegrationV1';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
if hasattr(unreal,'_npc_review'):unreal.unregister_slate_post_tick_callback(unreal._npc_review);del unreal._npc_review
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);q=p.get_actor_location();yaw=math.radians(p.get_movement_basis_yaw());right=unreal.Vector(-math.sin(yaw),math.cos(yaw),0);forward=unreal.Vector(math.cos(yaw),math.sin(yaw),0)
v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Script/PokeMonster.PokeMonsterNPCVisualActor')));c=v.get_component_by_class(unreal.SkeletalMeshComponent);old=(v.get_actor_transform(),c.get_skeletal_mesh_asset(),v.idle_animation,v.conversation_animation)
ids=['Ranger','WhiteHairedWarrior','ElvenArcher','DwarfWarrior'];i=0;stage=0;active=False;record=[]
def finish(error=None):
 c.set_skeletal_mesh_asset(old[1]);v.idle_animation=old[2];v.conversation_animation=old[3];v.set_actor_transform(old[0],False,True)
 unreal.unregister_slate_post_tick_callback(unreal._npc_review);del unreal._npc_review;(O/'GameCameraReviews.json').write_text(json.dumps({'renders':record,'error':error,'preview_only':True,'static_six':'No game-camera review; technical static references not placed.'},indent=2))
def tick(dt):
 global i,stage,active
 try:
  now=time.monotonic()
  if i>=len(ids):finish();return
  id=ids[i]
  if not active:
   v.set_actor_location(q+right*160+forward*80-unreal.Vector(0,0,47.15),False,True);v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=135,roll=0),True);c.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/'+id+'/Meshes/SK_'+id+'_NPC_V1'));v.idle_animation=unreal.load_asset('/Game/Characters/NPCs/'+id+'/Animations/A_'+id+'_Idle_V1');v.conversation_animation=unreal.load_asset('/Game/Characters/NPCs/'+id+'/Animations/A_'+id+'_Talk_V1');stage=now;active=True;return
  if now-stage<4:return
  path=R/'Art/Characters/NPCs'/id/'Previews/Unreal_GameCamera.png';unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(path)+'"',pc);record.append({'id':id,'file_request':str(path),'mode':'Temporary visual swap on own presentation actor during disposable PIE, no NPC identity/map data changed','location':v.get_actor_location().to_tuple(),'viewport':list(pc.get_viewport_size())});i+=1;active=False
 except Exception as error:finish(str(error))
unreal._npc_review=unreal.register_slate_post_tick_callback(tick)
