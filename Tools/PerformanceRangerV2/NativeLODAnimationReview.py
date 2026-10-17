import unreal,time,json
from pathlib import Path
P=Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/Ranger/Review/V2/NativeAnim');P.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));c=v.visual;p.set_actor_location(unreal.Vector(-835,-1080,50.15),False,True);v.set_actor_rotation(unreal.Rotator(pitch=0,yaw=135,roll=0),True);old=(c.get_skeletal_mesh_asset(),c.get_animation_mode(),c.get_forced_lod());c.set_anim_instance_class(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterNPCAnimInstance'));c.set_editor_property('pause_anims',False);rows=[('V1',0),('V2',1),('V2LOD1',2)];i=0;stage=0;active=False;shots=[]
def finish(error=None):
 c.set_skeletal_mesh_asset(old[0]);c.set_forced_lod(0);unreal.unregister_slate_post_tick_callback(unreal._rv2_native);del unreal._rv2_native;(P/'NativeAnimation.json').write_text(json.dumps({'shots':shots,'error':error},indent=2))
def tick(dt):
 global i,stage,active
 try:
  t=time.monotonic()
  if i>=len(rows):finish();return
  name,lod=rows[i]
  if not active:
   c.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1' if name=='V1' else '/Game/Characters/NPCs/RangerV2/Meshes/SK_Ranger_NPC_V2'));c.set_anim_instance_class(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterNPCAnimInstance'));c.set_forced_lod(lod);stage=t;active=True;return
  if t-stage>=3.:
   f=P/(name+'.png');unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+str(f)+'"',pc);shots.append({'file_request':str(f),'lod':c.get_predicted_lod_level(),'anim_class':c.get_anim_instance().get_class().get_path_name()});i+=1;active=False
 except Exception as e:finish(str(e))
unreal._rv2_native=unreal.register_slate_post_tick_callback(tick)
