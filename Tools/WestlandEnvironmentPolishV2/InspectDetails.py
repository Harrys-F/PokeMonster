import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';out={}
for path in ['/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_FlowerBlue','/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_FlowerCream','/Game/Environment/WestlandAssetLibrary/Materials/MI_WLA_MossStone']:
 a=unreal.load_asset(path);out[path]=dict(parent=a.parent.get_path_name(),vectors=str(a.vector_parameter_values),scalars=str(a.scalar_parameter_values),vector_names=[str(x)for x in unreal.MaterialEditingLibrary.get_vector_parameter_names(a)])
for key in ['A','B']:
 m=unreal.load_asset('/Game/Environment/WestlandAssetLibrary/Meshes/Landscape/SM_WLA_Boulder_'+key);S=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);out[key]=dict(simple=S.get_simple_collision_count(m),convex=S.get_convex_collision_count(m))
for k,c,n in [('positions',unreal.GeometryScript_MeshEdits,'set_all_mesh_vertex_positions'),('vectors',unreal.GeometryScript_List,'convert_array_to_vector_list')]:out[k]=getattr(c,n).__doc__
(D/'AssetDetails.json').write_text(json.dumps(out,indent=2))
