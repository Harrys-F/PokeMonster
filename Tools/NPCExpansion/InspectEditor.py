import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/ProjectRefinement/NPCExpansion'
u=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=u.get_editor_world();a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();rows=[]
for x in a:
 if isinstance(x,unreal.PokeMonsterNPC) or isinstance(x,unreal.PokeMonsterNPCVisualActor):
  v={'label':x.get_actor_label(),'class':x.get_class().get_name(),'location':str(x.get_actor_location()),'rotation':str(x.get_actor_rotation()),'path':x.get_path_name()}
  for k in ['display_name','dialogue','source_actor','idle_animation','walk_animation','conversation_animation','b_enable_motion_presentation']:
   try:v[k]=str(x.get_editor_property(k))
   except Exception:pass
  if isinstance(x,unreal.PokeMonsterNPCVisualActor):v['mesh']=str(x.visual.skeletal_mesh)
  rows.append(v)
(O/'EditorInventory.json').write_text(json.dumps({'world':w.get_path_name(),'pie':str(u.get_game_world()),'dirty_maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'npcs':rows},indent=2))
