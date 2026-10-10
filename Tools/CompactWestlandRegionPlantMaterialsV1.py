"""Remove only unused pot-material sections from owned ground-flora mesh copies.
All visible triangles, vertex positions, UVs and used material identities are retained.
"""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();audit=[]
for name in ['FlowerPlant','LeafPlant','BroadHerb','NarrowHerb']:
 sm=unreal.load_asset('/Game/Environment/WestlandRegion/Meshes/SM_WR_Ground_'+name);before=sm.get_num_triangles(0);bounds=sm.get_bounding_box();old=[s.material_interface for s in sm.get_editor_property('static_materials')];d=unreal.DynamicMesh();d,out=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(sm,d,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert out==unreal.GeometryScriptOutcomePins.SUCCESS;d,materials=unreal.GeometryScript_Materials.compact_material_i_ds(d,old,False);opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.replace_materials=True;opt.new_materials=materials;d,out=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,sm,opt,unreal.GeometryScriptMeshWriteLOD());assert out==unreal.GeometryScriptOutcomePins.SUCCESS;assert sm.get_num_triangles(0)==before;after=sm.get_bounding_box();assert after.min==bounds.min and after.max==bounds.max;assert unreal.EditorAssetLibrary.save_loaded_asset(sm,False);audit.append({'mesh':name,'triangles_unchanged':before,'bounds_unchanged':True,'material_slots_before':len(old),'material_slots_after':len(materials)})
(R/'Saved/WestlandRegion/PlantMaterialSections.json').write_text(json.dumps(audit,indent=2));unreal.log('REGION_PLANT_SECTIONS_DONE')
