"""Import only new mesh packages; reuse the EXACT existing skeletons, clips and materials."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();T=unreal.AssetToolsHelpers.get_asset_tools();created=[];rows=[]
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 for name in ['Player','Glurak']:
  A=R/('Art/Characters/YoungTrainer'if name=='Player'else'Art/Characters/Creatures/Glurak');P=('/Game/Characters/YoungTrainer'if name=='Player'else'/Game/Characters/Creatures/Glurak')+'/AnimationV61';assert not unreal.EditorAssetLibrary.does_directory_exist(P);audit=json.loads((A/'AnimationCorrectionsV61_Audit.json').read_text());source=R/audit['export'];assert hashlib.sha256(source.read_bytes()).hexdigest()==audit['export_sha256'];original=unreal.load_asset('/Game/Characters/YoungTrainer/MeshyV2/Meshes/SK_Player_Meshy_V2'if name=='Player'else'/Game/Characters/Creatures/Glurak/AnimationV6/SK_Glurak_V6');ui=unreal.FbxImportUI()
  for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False,skeleton=original.skeleton).items():ui.set_editor_property(k,v)
  for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
  task=unreal.AssetImportTask()
  for k,v in dict(filename=str(source),destination_path=P,destination_name='SK_'+name+'_V61',automated=True,save=False,replace_existing=False,options=ui).items():task.set_editor_property(k,v)
  T.import_asset_tasks([task]);mesh=next(x for x in task.get_objects()if isinstance(x,unreal.SkeletalMesh));assert mesh.skeleton==original.skeleton;assert unreal.PokeMonsterCreaturePolishLibrary.have_matching_reference_skeleton(mesh,original);slots=list(mesh.materials);assert len(slots)==len(original.materials)
  for i,slot in enumerate(slots):slot.material_interface=original.materials[i].material_interface
  mesh.set_editor_property('materials',slots);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);created.append(mesh.get_path_name())
  if name=='Glurak':
   before=unreal.load_asset('/Game/Characters/Creatures/Glurak/AnimationV6/DA_Glurak_Presentation_V6');profile=unreal.EditorAssetLibrary.duplicate_asset(before.get_path_name(),P+'/DA_Glurak_Presentation_V61');profile.set_editor_property('mesh',mesh);assert not profile.get_validation_errors(),profile.get_validation_errors();assert unreal.EditorAssetLibrary.save_loaded_asset(profile,False);created.append(profile.get_path_name())
  rows.append(dict(name=name,mesh=mesh.get_path_name(),skeleton=mesh.skeleton.get_path_name(),height=mesh.get_bounds().box_extent.z*2,old_materials_exact=True,clips_not_imported=True))
finally:unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
dirty=[p.get_path_name()for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()];assert not dirty,dirty;assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();(R/'Saved/AnimationCorrectionsV61/Import.json').write_text(json.dumps(dict(models=rows,created=created),indent=2));unreal.log('V61_MESHES_IMPORTED_WITHOUT_ANIMATION_OR_SKELETON_CHANGES')
