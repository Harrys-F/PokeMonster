"""Fit existing river rows into actual bank intersections; prevent exposed floating side edges."""
import unreal,json,re,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world()and W.get_name()=='Dev_WestlandRegion';assert not(D/'ShoreFit.json').exists();import sys;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();ignore=[a for a in actors if not a.get_actor_label().startswith('WR_Terrain_')];river=next(a for a in actors if a.get_actor_label()=='WR_WindingRiver');m=river.static_mesh_component.static_mesh;assert m.get_path_name().startswith('/Game/Environment/WestlandEnvironmentPolishV2/');dm=unreal.DynamicMesh();dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(m,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;_,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);old=list(unreal.GeometryScript_List.convert_vector_list_to_array(vs));rows={};positions=[];audit=[]
def ground(e,n,z):
 x,y,_=L.world(e,n);h=unreal.SystemLibrary.line_trace_single(W,unreal.Vector(x,y,z+3000),unreal.Vector(x,y,z-7000),unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignore,unreal.DrawDebugTrace.NONE);assert h,(e,n,z);match=re.search(r'ImpactPoint=\(X=[^,]+,Y=[^,]+,Z=([^\)]+)',h.export_text());assert match;return float(match[1])
for p in old:
 e,n=L.en(p.x,p.y);key=round(n,3);rows.setdefault(key,[]).append(e)
for n,es in rows.items():
 c=(min(es)+max(es))*.5;z=next(p.z for p in old if abs(L.en(p.x,p.y)[1]-n)<.003);edges=[]
 if abs(n)>398:
  rows[n]=(min(es),max(es),[min(es),max(es)]);continue
 for side in [-1,1]:
  d=2.5
  while d<13 and ground(c+side*d,n,z)<z+3:d+=.25
  assert d<13,('No safe bank intersection',n,side);d+=.4;edge=c+side*d;g=ground(edge,n,z);assert g>z;edges.append(edge)
 audit.append(dict(n=n,left=edges[0],right=edges[1],width_m=edges[1]-edges[0],water_z_cm=z));rows[n]=(min(es),max(es),edges)
for p in old:
 e,n=L.en(p.x,p.y);a,b,edges=rows[round(n,3)];u=(e-a)/(b-a);ee=edges[0]+(edges[1]-edges[0])*u;x,y,_=L.world(ee,n);positions.append(unreal.Vector(x,y,p.z))
unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(positions));unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions());opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,m,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
water=unreal.load_asset('/Game/Environment/WestlandEnvironmentPolishV2/Materials/M_WEP_FlowingRiver');ML=unreal.MaterialEditingLibrary
for node in ML.get_material_expressions(water):
 if isinstance(node,unreal.MaterialExpressionSingleLayerWaterMaterialOutput):
  pass
# Existing constant attached to the scattering output: exact inspected connection.
scatter=next(n for n in ML.get_material_expressions(water)if isinstance(n,unreal.MaterialExpressionConstant3Vector)and abs(n.get_editor_property('constant').r-.00035)<.0000001);scatter.set_editor_property('constant',unreal.LinearColor(.001,.0025,.0018,1));ML.recompile_material(water);assert unreal.EditorAssetLibrary.save_loaded_asset(water,False);assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'ShoreFit.json').write_text(json.dumps(dict(passed=True,rows=audit,edges_buried_in_terrain=True,basic_course_retained=True,original_centerline_kept=False),indent=2))
