"""Import the three reusable V2 window assets. No map is loaded or saved."""
import json
from pathlib import Path
import unreal

ROOT=Path(unreal.Paths.project_dir()).resolve()
ART=ROOT/'Art/HealingHouse'
DEST='/Game/Environment/HealingHouse'
report=json.loads((ART/'Review/V2/WindowLibraryAudit.json').read_text())
for m in report['modules']:
    if unreal.EditorAssetLibrary.does_asset_exist(DEST+'/Meshes/SM_'+m['name']):
        raise RuntimeError('Preserve already imported window library')
ui=unreal.FbxImportUI()
for prop,value in {'import_mesh':True,'import_materials':False,'import_textures':False,
                   'import_as_skeletal':False,'automated_import_should_detect_type':False,
                   'mesh_type_to_import':unreal.FBXImportType.FBXIT_STATIC_MESH}.items():
    ui.set_editor_property(prop,value)
for prop,value in {'combine_meshes':False,'auto_generate_collision':False,
                  'transform_vertex_to_absolute':True,'bake_pivot_in_vertex':False,
                  'convert_scene':True,'convert_scene_unit':True,
                  'force_front_x_axis':False,'import_uniform_scale':1}.items():
    ui.static_mesh_import_data.set_editor_property(prop,value)
task=unreal.AssetImportTask()
for prop,value in {'filename':str(ART/'Exports/HealingHouse_V2_WindowModules.fbx'),
                   'destination_path':DEST+'/Meshes','automated':True,'save':True,
                   'replace_existing':False,'options':ui}.items(): task.set_editor_property(prop,value)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
loaded=[]
for path in task.get_editor_property('imported_object_paths'):
    mesh=unreal.load_asset(path)
    if not isinstance(mesh,unreal.StaticMesh): continue
    entry=next(m for m in report['modules'] if mesh.get_name().endswith(m['name']))
    dest=DEST+'/Meshes/SM_'+entry['name']
    if mesh.get_path_name().split('.')[0]!=dest:
        assert unreal.EditorAssetLibrary.rename_asset(mesh.get_path_name(),dest)
    bounds=mesh.get_bounding_box()
    for i,value in enumerate((bounds.min.x,bounds.min.y,bounds.min.z)):
        assert abs(value-100*entry['unreal_bounds_min_m'][i])<.3
    for i,value in enumerate((bounds.max.x,bounds.max.y,bounds.max.z)):
        assert abs(value-100*entry['unreal_bounds_max_m'][i])<.3
    for i,slot in enumerate(mesh.get_editor_property('static_materials')):
        name=str(slot.get_editor_property('imported_material_slot_name')).removeprefix('HH_V2_')
        material=unreal.load_asset(DEST+'/Materials/M_HH_V2_'+name)
        assert material
        mesh.set_material(i,material)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    loaded.append(dest)
assert len(loaded)==3
(ART/'Review/V2/WindowLibraryImport.json').write_text(json.dumps({'assets':loaded,'map_changed':False},indent=2)+'\n')
unreal.log('HH_V2_WINDOW_LIBRARY_SUCCESS count=3; no map changes')
