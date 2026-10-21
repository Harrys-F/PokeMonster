"""Import local surface caps against unchanged skeleton; configure species-only overworld profiles."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()and not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();T=unreal.AssetToolsHelpers.get_asset_tools();w=E.get_editor_world();rows=[];flag=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX 0')
try:
 a=json.loads((R/'Art/Characters/Creatures/Schiggy/SurfaceV2_Audit.json').read_text());assert hashlib.sha256((R/a['original']).read_bytes()).hexdigest()==a['original_sha256'];s=unreal.load_asset('/Game/Data/Creatures/DA_Schiggy');old=s.get_visuals().presentation;sk=old.mesh.skeleton;folder='/Game/Characters/Creatures/Schiggy/SurfaceV2';assetname='SK_Schiggy_Surface';assert unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+assetname)
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_as_skeletal=True,import_animations=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH,create_physics_asset=False,skeleton=sk,override_full_name=True).items():ui.set_editor_property(k,v)
 for k,v in dict(convert_scene=True,convert_scene_unit=True,force_front_x_axis=True,import_uniform_scale=1.,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,update_skeleton_reference_pose=False,use_t0_as_ref_pose=False).items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 task=unreal.AssetImportTask()
 for k,v in dict(filename=str(R/a['export']),destination_path=folder,destination_name=assetname,automated=True,save=False,replace_existing=True,options=ui).items():task.set_editor_property(k,v)
 T.import_asset_tasks([task]);mesh=next(x for x in task.get_objects()if isinstance(x,unreal.SkeletalMesh));assert mesh.skeleton==sk
 if mesh.get_path_name().split('.')[0]!=folder+'/'+assetname:assert unreal.EditorAssetLibrary.rename_asset(mesh.get_path_name().split('.')[0],folder+'/'+assetname);mesh=unreal.load_asset(folder+'/'+assetname)
 cap=unreal.load_asset(folder+'/M_Schiggy_LocalSurfaceCaps')
 if not cap:
  cap=T.create_asset('M_Schiggy_LocalSurfaceCaps',folder,unreal.Material,unreal.MaterialFactoryNew());node=unreal.MaterialEditingLibrary.create_material_expression(cap,unreal.MaterialExpressionVertexColor,0,0);assert unreal.MaterialEditingLibrary.connect_material_property(node,'',unreal.MaterialProperty.MP_BASE_COLOR);assert unreal.MaterialEditingLibrary.connect_material_property(node,'A',unreal.MaterialProperty.MP_ROUGHNESS);unreal.MaterialEditingLibrary.recompile_material(cap);assert unreal.EditorAssetLibrary.save_loaded_asset(cap,False)
 slots=list(mesh.materials);assert len(slots)==2
 slots[0].material_interface=old.mesh.materials[0].material_interface;slots[1].material_interface=cap
 mesh.materials=slots;unreal.MaterialEditingLibrary.set_material_usage(cap,unreal.MaterialUsage.MATUSAGE_SKELETAL_MESH);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);assert unreal.EditorAssetLibrary.save_loaded_asset(cap,False)
 rows.append({'reimported_generated_surface_only':mesh.get_path_name()})
finally:unreal.SystemLibrary.execute_console_command(w,'Interchange.FeatureFlags.Import.FBX '+str(flag))
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(R/'Saved/OverworldAIV2/ReimportSurface.json').write_text(json.dumps(rows,indent=2))
