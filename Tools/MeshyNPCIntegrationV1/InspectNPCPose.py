import unreal,json
from pathlib import Path
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world();v=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor));c=v.visual;o={'mesh':c.get_skeletal_mesh_asset().get_path_name(),'idle':v.idle_animation.get_path_name(),'rotation':v.get_actor_rotation().to_tuple(),'scale':v.get_actor_scale3d().to_tuple(),'bounds':str(v.get_actor_bounds(False)),'anim_alpha':c.get_anim_instance().conversation_alpha,'bones':{},'functions':[n for n in dir(c) if 'bone' in n or 'animation' in n]}
for b in ['root','pelvis','chest','head','ankle_L','foot_l']:
 try:o['bones'][b]=c.get_socket_location(b).to_tuple()
 except Exception as e:o['bones'][b]=str(e)
Path(unreal.Paths.project_dir(),'Art/Characters/NPCs/IntegrationV1/PoseDebug.json').write_text(json.dumps(o,indent=2))
