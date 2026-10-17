import unreal,json
from pathlib import Path
rows=[]
for asset,strip in [('/Game/Environment/WestlandAssetLibrary/QualityV3/Meshes/Trees/SM_WLA_OakAncient_V3',True),('/Game/Environment/TreeShadowProxyV1/SM_TSP_OakAncient_Bark',False)]:
 dm=unreal.DynamicMesh();dm,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(unreal.load_asset(asset),dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 if strip:unreal.GeometryScript_Materials.delete_triangles_by_material_id(dm,1)
 _,vs,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);rows.append([v.to_tuple() for v in unreal.GeometryScript_List.convert_vector_list_to_array(vs)])
(Path(unreal.Paths.project_dir())/'Saved/TreeShadowProxyV1/BarkCoordinates.json').write_text(json.dumps(rows))
