"""Reimport only our private botanical variants after a diagnosed UV correction.
Verify identical rendered triangle positions and restore private material bindings.
"""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2HealingArtV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();D='/Game/Environment/VisualV2HealingArtV3';AT=unreal.AssetToolsHelpers.get_asset_tools();rows=[]
import sys,copy
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
def canon(x):
 x=copy.deepcopy(x)
 for a in x['actors'].values():a['components'].sort(key=lambda c:c['name'])
 return x
expected=canon(json.loads((S/'AfterScene.json').read_text()));assert canon(scene(E.get_editor_world()))==expected
assert all(p.get_path_name().startswith(D+'/Meshes/') for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages())
assert all(p.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2' for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
def geometry(mesh):
 dm=unreal.DynamicMesh();lod=unreal.GeometryScriptMeshReadLOD();lod.lod_index=0;lod.lod_type=unreal.GeometryScriptLODType.RENDER_DATA;dm,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),lod);assert 'SUCCESS' in str(result);tri=[]
 for i in range(mesh.get_num_triangles(0)):
  valid,*p=unreal.GeometryScript_MeshQueries.get_triangle_positions(dm,i);assert valid;tri.append(tuple(sorted(tuple(round(x,5) for x in v.to_tuple()) for v in p)))
 return hashlib.sha256(repr(sorted(tri)).encode()).hexdigest()
for family in ['BroadHerb','NarrowHerb','LeafPlant','FlowerPlant','TrailingHerb']:
 name='SM_HA3_'+family;path=D+'/Meshes/'+name;mesh=unreal.load_asset(path);before=geometry(mesh)
 ui=unreal.FbxImportUI();ui.import_mesh=True;ui.import_materials=False;ui.import_textures=False;ui.import_as_skeletal=False;ui.automated_import_should_detect_type=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 for key,value in {'combine_meshes':True,'auto_generate_collision':False,'convert_scene':True,'convert_scene_unit':True,'transform_vertex_to_absolute':True,'import_uniform_scale':1}.items():ui.static_mesh_import_data.set_editor_property(key,value)
 ui.static_mesh_import_data.set_editor_property('vertex_color_import_option',unreal.VertexColorImportOption.REPLACE)
 task=unreal.AssetImportTask();task.filename=str(R/'Art/World/VisualV2HealingArtV3/Exports'/(name+'.fbx'));task.destination_path=D+'/Meshes';task.destination_name=name;task.options=ui;task.automated=True;task.save=False;task.replace_existing=True;AT.import_asset_tasks([task]);mesh=unreal.load_asset(path)
 for i,slot in enumerate(mesh.static_materials):
  key=str(slot.get_editor_property('imported_material_slot_name')).split('_')[-1];m=unreal.load_asset(D+'/Materials/M_HA3_'+key);assert m;mesh.set_material(i,m)
 after=geometry(mesh);assert before==after,(family,before,after);assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False);rows.append({'family':family,'triangle_position_hash':after,'geometry_identical_to_1e5_cm':True})
assert canon(scene(E.get_editor_world()))==expected,'Reimport altered map bindings or any protected scene properties'
if unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages():assert unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),'/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(S/'UVReimport.json').write_text(json.dumps(rows,indent=2));unreal.log('HA3_UV_REIMPORT_GEOMETRY_IDENTICAL')
