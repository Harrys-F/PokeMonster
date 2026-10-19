"""Same triangles, normals and UVs; replace constant-colour sections with per-corner vertex colours.
Private candidate assets only. No source mesh, scene actor or texture mutation.
"""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();S=R/'Saved/VisualV2WorldArtQualityV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();D='/Game/Environment/VisualV2WorldArtV2';T=unreal.AssetToolsHelpers.get_asset_tools();L=unreal.MaterialEditingLibrary;out=[];mp=D+'/Materials/M_WAQ2_PlantVertexColour';assert not (S/'GrassCandidate.json').exists()
m=unreal.load_asset(mp) if unreal.EditorAssetLibrary.does_asset_exist(mp) else T.create_asset('M_WAQ2_PlantVertexColour',D+'/Materials',unreal.Material,unreal.MaterialFactoryNew());L.delete_all_material_expressions(m);m.set_editor_property('two_sided',True);m.set_editor_property('used_with_instanced_static_meshes',True);vc=L.create_material_expression(m,unreal.MaterialExpressionVertexColor);assert L.connect_material_property(vc,'',unreal.MaterialProperty.MP_BASE_COLOR)
for value,prop in [(.88,unreal.MaterialProperty.MP_ROUGHNESS),(.12,unreal.MaterialProperty.MP_SPECULAR)]:
 n=L.create_material_expression(m,unreal.MaterialExpressionConstant);n.set_editor_property('r',value);assert L.connect_material_property(n,'',prop)
L.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
for key in ['GrassSmall','GrassMedium','MeadowHerbs']:
 src=unreal.load_asset('/Game/Environment/Westland/NaturalGroundV1/Meshes/SM_WL_NG_'+key);dst=D+'/Meshes/SM_WAQ2_'+key;assert not unreal.EditorAssetLibrary.does_asset_exist(dst);dm=unreal.DynamicMesh();lod=unreal.GeometryScriptMeshReadLOD();lod.set_editor_property('lod_index',0);lod.set_editor_property('lod_type',unreal.GeometryScriptLODType.RENDER_DATA);dm,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(src,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),lod);assert 'SUCCESS' in str(result),result
 colors=[]
 for sm in src.static_materials:
  mat=sm.material_interface;const=next(x for x in unreal.ObjectIterator(unreal.MaterialExpressionConstant3Vector) if x.get_outer()==mat);colors.append(const.get_editor_property('constant'))
 vs=[];ns=[];uvs=[];cs=[];tris=[];by=[];reuse={}
 for i in range(src.get_num_triangles(0)):
  valid,a,b,c=unreal.GeometryScript_MeshQueries.get_triangle_positions(dm,i);assert valid
  _,na,nb,nc,validn=unreal.GeometryScript_MeshQueries.get_triangle_normals(dm,i);assert validn
  ua,ub,uc,validuv=unreal.GeometryScript_MeshQueries.get_triangle_u_vs(dm,0,i);assert validuv
  matid,validmat=unreal.GeometryScript_Materials.get_triangle_material_id(dm,i);assert validmat and matid<len(colors)
  ids=[]
  for p,n,uv in zip([a,b,c],[na,nb,nc],[ua,ub,uc]):
   keyv=(p.to_tuple(),n.to_tuple(),uv.to_tuple(),matid)
   if keyv not in reuse:reuse[keyv]=len(vs);vs.append(p);ns.append(n);uvs.append(uv);cs.append(colors[matid])
   ids.append(reuse[keyv])
  tris.append(unreal.IntVector(*ids));by.append(matid)
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=vs;buf.normals=ns;buf.uv0=uvs;buf.vertex_colors=cs;buf.triangles=tris;target=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(target,buf);options=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();options.enable_collision=False;options.enable_nanite=False;options.enable_recompute_normals=False;options.enable_recompute_tangents=True;mesh,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(target,dst,options);assert mesh;mesh.set_material(0,m);assert mesh.get_num_triangles(0)==src.get_num_triangles(0) and mesh.get_num_sections(0)==1;assert unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
 # Re-read built triangles: compare the triangle-position multiset; face ordering may change.
 check=unreal.DynamicMesh();check,_=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,check,unreal.GeometryScriptCopyMeshFromAssetOptions(),lod)
 def positions(d,count):
  out=[]
  for i in range(count):
   valid,*p=unreal.GeometryScript_MeshQueries.get_triangle_positions(d,i);assert valid;out.append(tuple(sorted(tuple(round(v,5) for v in x.to_tuple()) for x in p)))
  return sorted(out)
 assert positions(dm,len(tris))==positions(check,len(tris)),'Silhouette or triangles changed'
 out.append({'key':key,'source':src.get_path_name(),'candidate':mesh.get_path_name(),'triangles':len(tris),'sections_before':src.get_num_sections(0),'sections_after':mesh.get_num_sections(0),'material_slots_before':len(src.static_materials),'material_slots_after':len(mesh.static_materials),'positions_exact_to_1e5_cm':True,'uvs_and_corner_normals_copied':True,'vertex_colour_palette':[x.export_text() for x in colors]})
(S/'GrassCandidate.json').write_text(json.dumps(out,indent=2));unreal.log('WAQ2_GRASS_CANDIDATES_BUILT')
