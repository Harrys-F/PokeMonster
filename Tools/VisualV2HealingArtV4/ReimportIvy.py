import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV4';A=R/'Art/World/VisualV2HealingArtV4';D='/Game/Environment/VisualV2HealingArtV4';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();AT=unreal.AssetToolsHelpers.get_asset_tools()
for name in ['IvySprigA','IvySprigB']:
 path=D+'/Meshes/SM_HA4_'+name;assert unreal.EditorAssetLibrary.does_asset_exist(path);ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for key,val in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(key,val)
 ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
 t=unreal.AssetImportTask();t.filename=str(A/'Exports'/('SM_HA4_'+name+'.fbx'));t.destination_path=D+'/Meshes';t.destination_name='SM_HA4_'+name;t.options=ui;t.automated=True;t.save=False;t.replace_existing=True;t.replace_existing_settings=True;AT.import_asset_tasks([t]);m=unreal.load_asset(path);assert m.get_num_triangles(0)==180;m.set_material(0,unreal.load_asset(D+'/Materials/M_HA4_Ivy'));assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).get_simple_collision_count(m)==0;assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
import sys
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
current=scene(E.get_editor_world());expected=json.loads((S/'CandidateScene.json').read_text())
for value in [current,expected]:
 for row in value['actors'].values():row['components'].sort(key=lambda c:c['name'])
assert current==expected;(S/'IvyReimport.json').write_text(json.dumps({'owned_meshes':2,'triangles_each':180,'scene_signature_unchanged':True}));unreal.log('HA4_IVY_PLACEMENT_REIMPORTED')
