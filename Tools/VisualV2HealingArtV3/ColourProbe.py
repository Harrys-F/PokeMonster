import unreal,json
from pathlib import Path
S=Path(unreal.Paths.project_dir())/'Saved/VisualV2HealingArtV3';out={}
for cls in [unreal.GeometryScript_ListUtilityFunctions] if hasattr(unreal,'GeometryScript_ListUtilityFunctions') else []:out['list_api']={n:str(getattr(cls,n).__doc__) for n in dir(cls) if 'color' in n}
mesh=unreal.load_asset('/Game/Environment/VisualV2HealingArtV3/Meshes/SM_HA3_BroadHerb');dm=unreal.DynamicMesh();lod=unreal.GeometryScriptMeshReadLOD();lod.lod_index=0;lod.lod_type=unreal.GeometryScriptLODType.RENDER_DATA;dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),lod);_,colors,valid,gaps=unreal.GeometryScript_VertexColors.get_mesh_per_vertex_colors(dm);out.update(valid=valid,gaps=gaps,color_list=colors.export_text(),classes=[x for x in dir(unreal) if 'GeometryScript' in x and 'List' in x])
from collections import Counter
array=unreal.GeometryScript_List.convert_color_list_to_array(colors);out['palette']=Counter(tuple(round(v,4) for v in [c.r,c.g,c.b]) for c in array).most_common(12);out['bounds']=[[min(getattr(c,k) for c in array),max(getattr(c,k) for c in array)] for k in ['r','g','b']];(S/'ColourProbe.json').write_text(json.dumps(out,indent=2))
