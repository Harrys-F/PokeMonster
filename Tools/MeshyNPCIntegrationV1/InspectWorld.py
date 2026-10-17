import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P=R/'Art/Characters/NPCs/IntegrationV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
rows=[]
for o in a.get_all_level_actors():
 if any(k in o.get_class().get_name() for k in ['NPC','Trainer','RestPoint','Quest','Archive','Wild']):
  row={'label':o.get_actor_label(),'name':o.get_name(),'class':o.get_class().get_path_name(),'location':o.get_actor_location().to_tuple(),'rotation':str(o.get_actor_rotation()),'components':[]}
  for prop in ['display_name','dialogue','trainer_profile']:
   try:row[prop]=str(o.get_editor_property(prop))
   except Exception:pass
  for c in o.get_components_by_class(unreal.SceneComponent):
   row['components'].append({'name':c.get_name(),'class':c.get_class().get_name(),'location':c.get_world_location().to_tuple(),'scale':c.get_world_scale().to_tuple(),'visible':c.is_visible()})
  rows.append(row)
x={'map':w.get_path_name(),'pie_running':bool(e.get_game_world()),'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'actors':rows}
(P/'WorldBefore.json').write_text(json.dumps(x,indent=2));unreal.log('NPC_WORLD_AUDIT_DONE')
