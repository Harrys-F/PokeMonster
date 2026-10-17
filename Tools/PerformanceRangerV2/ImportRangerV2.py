import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/V2';E=R/'Art/Characters/NPCs/Ranger/Exports/V2';P='/Game/Characters/NPCs/RangerV2';editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not editor.get_game_world();T=unreal.AssetToolsHelpers.get_asset_tools();S=unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem);v1=unreal.load_asset('/Game/Characters/NPCs/Ranger/Meshes/SK_Ranger_NPC_V1');skeleton=v1.skeleton
assert not unreal.EditorAssetLibrary.does_asset_exist(P+'/Meshes/SK_Ranger_NPC_V2'),'Do not overwrite existing assets'
old=unreal.SystemLibrary.get_console_variable_int_value('Interchange.FeatureFlags.Import.FBX');unreal.SystemLibrary.execute_console_command(editor.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0')
try:
 ui=unreal.FbxImportUI()
 for k,v in {'import_mesh':True,'import_as_skeletal':True,'import_animations':False,'import_materials':False,'import_textures':False,'automated_import_should_detect_type':False,'mesh_type_to_import':unreal.FBXImportType.FBXIT_SKELETAL_MESH,'create_physics_asset':False,'skeleton':skeleton}.items():ui.set_editor_property(k,v)
 for k,v in {'convert_scene':True,'convert_scene_unit':True,'force_front_x_axis':True,'import_uniform_scale':1.,'normal_import_method':unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,'normal_generation_method':unreal.FBXNormalGenerationMethod.MIKK_T_SPACE}.items():ui.skeletal_mesh_import_data.set_editor_property(k,v)
 task=unreal.AssetImportTask()
 for k,v in {'filename':str(E/'SK_Ranger_NPC_V2_LOD0.fbx'),'destination_path':P+'/Meshes','destination_name':'SK_Ranger_NPC_V2','automated':True,'save':False,'replace_existing':False,'options':ui}.items():task.set_editor_property(k,v)
 T.import_asset_tasks([task]);mesh=unreal.load_asset(P+'/Meshes/SK_Ranger_NPC_V2');assert mesh and mesh.skeleton==skeleton
 for j in [1,2]:assert S.import_lod(mesh,j,str(E/('SK_Ranger_NPC_V2_LOD'+str(j)+'.fbx')))==j
 slots=list(mesh.materials);assert len(slots)==1;slots[0].material_interface=unreal.load_asset('/Game/Characters/NPCs/Ranger/Materials/MI_Ranger_V1');mesh.materials=slots
 assert S.get_lod_count(mesh)==3;unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
 # Material-only diagnostic: same lit/opaque/two-sided family, constant inputs, no texture sampling.
 flat=T.create_asset('M_Ranger_FlatDiagnostic',P+'/Materials',unreal.Material,unreal.MaterialFactoryNew());flat.set_editor_property('two_sided',True);flat.set_editor_property('used_with_skeletal_mesh',True);L=unreal.MaterialEditingLibrary
 col=L.create_material_expression(flat,unreal.MaterialExpressionConstant3Vector,-300,0);col.set_editor_property('constant',unreal.LinearColor(.16,.15,.12,1));rough=L.create_material_expression(flat,unreal.MaterialExpressionConstant,-300,150);rough.set_editor_property('r',.65);L.connect_material_property(col,'',unreal.MaterialProperty.MP_BASE_COLOR);L.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);L.recompile_material(flat);unreal.EditorAssetLibrary.save_loaded_asset(flat,False)
 (O/'UnrealLOD_Import.json').write_text(json.dumps({'mesh':mesh.get_path_name(),'skeleton':mesh.skeleton.get_path_name(),'lod_count':S.get_lod_count(mesh),'shared_original_material':slots[0].material_interface.get_path_name(),'reused_idle':'/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Idle_V1','reused_talk':'/Game/Characters/NPCs/Ranger/Animations/A_Ranger_Talk_V1','textures':'No duplicated textures or changed originals','physics':'No new physics asset/collision','candidate_screen_sizes':[1.,.12,.055]},indent=2))
finally:unreal.SystemLibrary.execute_console_command(editor.get_editor_world(),'Interchange.FeatureFlags.Import.FBX '+str(old))
