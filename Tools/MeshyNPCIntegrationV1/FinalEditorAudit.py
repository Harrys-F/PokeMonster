import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();I=R/'Art/Characters/NPCs/IntegrationV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();w=E.get_editor_world();assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2'
rows=[]
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if any(x in a.get_class().get_name() for x in ['NPC','Trainer','RestPoint','Quest','Archive','Wild']):
  row={'label':a.get_actor_label(),'name':a.get_name(),'class':a.get_class().get_path_name(),'location':a.get_actor_location().to_tuple(),'rotation':a.get_actor_rotation().to_tuple()}
  for n in ['display_name','dialogue','trainer_profile']:
   try:
    v=a.get_editor_property(n);row[n]=v.get_path_name() if hasattr(v,'get_path_name') else str(v)
   except Exception:pass
  rows.append(row)
saved=[];foreign=[]
for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
 if p.get_path_name().startswith('/Game/Characters/NPCs/'):
  for a in unreal.EditorAssetLibrary.list_assets(p.get_path_name(),False,False):
   if unreal.EditorAssetLibrary.does_asset_exist(a):unreal.EditorAssetLibrary.save_asset(a,False);saved.append(a)
 else:foreign.append(p.get_path_name())
assets=unreal.EditorAssetLibrary.list_assets('/Game/Characters/NPCs',True,False);audit=[]
for path in assets:
 a=unreal.load_asset(path);row={'path':path,'class':a.get_class().get_name()}
 if isinstance(a,unreal.SkeletalMesh):row.update(skeleton=a.skeleton.get_path_name(),slots=len(a.materials),materials=[x.material_interface.get_path_name() if x.material_interface else None for x in a.materials])
 elif isinstance(a,unreal.StaticMesh):row.update(lods=a.get_num_lods(),slots=len(a.static_materials))
 elif isinstance(a,unreal.Texture2D):row.update(size=[a.blueprint_get_size_x(),a.blueprint_get_size_y()],srgb=a.srgb)
 if isinstance(a,unreal.MaterialInstanceConstant):
  row['textures']={n:(unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(a,n).get_path_name() if unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(a,n) else None) for n in ['BaseColor','Normal','MetalRough']}
 audit.append(row)
(I/'FinalEditorAudit.json').write_text(json.dumps({'map':w.get_path_name(),'actors':rows,'assets':audit,'saved_new_assets':saved,'foreign_dirty_content':foreign,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()]},indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');unreal.log('NPC_FINAL_MAP_CHECK_REQUESTED')
