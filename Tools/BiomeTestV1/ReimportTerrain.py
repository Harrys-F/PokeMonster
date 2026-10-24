"""Reimport only the two newly authored sandbox meshes after the measured FBX-axis correction."""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_BiomeTestMap_V1'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
D='/Game/Environment/BiomeTestV1';unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'Interchange.FeatureFlags.Import.FBX 0');tasks=[]
for name in ['SM_BiomeTerrain','SM_BiomeWater']:
 ui=unreal.FbxImportUI()
 for k,v in dict(import_mesh=True,import_materials=False,import_textures=False,import_as_skeletal=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():ui.set_editor_property(k,v)
 for k,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,convert_scene=True,convert_scene_unit=True,import_uniform_scale=1.,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE,generate_lightmap_u_vs=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS).items():ui.static_mesh_import_data.set_editor_property(k,v)
 t=unreal.AssetImportTask()
 for k,v in dict(filename=str(R/'Art/World/BiomeTestV1/Exports'/(name+'.fbx')),destination_path=D+'/Meshes',destination_name=name,automated=True,save=False,replace_existing=True,replace_existing_settings=True,options=ui).items():t.set_editor_property(k,v)
 tasks.append(t)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for name,mat in [('SM_BiomeTerrain','M_BiomeGround'),('SM_BiomeWater','M_BiomeWater')]:
 sm=unreal.load_asset(D+'/Meshes/'+name);sm.set_material(0,unreal.load_asset(D+'/Materials/'+mat))
 if name=='SM_BiomeTerrain':sm.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
 assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
assert all(p.get_path_name()=='/Game/Maps/Dev_BiomeTestMap_V1'for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),'/Game/Maps/Dev_BiomeTestMap_V1')
(R/'Saved/BiomeTestV1/TerrainAxisCorrection.json').write_text(json.dumps({'only_new_assets':True,'precompensation':'Blender Y reflected before FBX export; verified through Unreal line traces','meshes':['SM_BiomeTerrain','SM_BiomeWater']},indent=2))
