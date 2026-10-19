"""Read-only verification of built plant geometry, materials, collision and map scope."""
from pathlib import Path
import unreal,json,hashlib
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtV5';catalog=json.loads((R/'Art/World/VisualV2WorldArtV5/Details.json').read_text());SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);rows=[]
for family,row in catalog.items():
 mesh=unreal.load_asset('/Game/Environment/VisualV2WorldArtV5/Meshes/SM_WA5_'+family);assert mesh;tri=mesh.get_num_triangles(0);assert tri==row['triangles'];bounds=mesh.get_bounding_box();dims=bounds.max-bounds.min;actual=list(dims.to_tuple());assert max(abs(a-b*100) for a,b in zip(actual,row['dimensions_m']))<.05
 assert SM.get_simple_collision_count(mesh)==0;materials=[slot.material_interface for slot in mesh.static_materials];assert all(materials)
 assert all(m.get_path_name().startswith('/Game/Environment/VisualV2WorldArtV5/Materials/') for m in materials)
 rows.append({'family':family,'triangles':tri,'vertices_unreal':SM.get_number_verts(mesh,0),'sections':mesh.get_num_sections(0),'material_slots':len(mesh.static_materials),'dimensions_cm':actual,'collision_shapes':0,'materials':[m.get_path_name() for m in materials]})
textures=[]
for name in ['T_WA5_ForestFloor','T_WA5_WetBank']:
 t=unreal.load_asset('/Game/Environment/VisualV2WorldArtV5/Textures/'+name);assert t;textures.append({'path':t.get_path_name(),'srgb':t.get_editor_property('srgb'),'max_texture_size':t.get_editor_property('max_texture_size'),'power_of_two_mode':str(t.get_editor_property('power_of_two_mode'))})
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert [p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()] in [[],['/Game/Maps/Dev_TestMap_VisualV2']];(S/'AssetVerification.json').write_text(json.dumps({'meshes':rows,'textures':textures},indent=2));unreal.log('WA5_ASSET_VERIFICATION_PASS')
