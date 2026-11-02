"""Reshape derivatives of existing terrain/river meshes; originals, topology, UVs and gameplay actors retained."""
import unreal,json,sys,time,traceback,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';ROOT='/Game/Environment/WestlandEnvironmentPolishV2';sys.path.insert(0,str(R/'Tools/WestlandEnvironmentPolishV2'));import Shapes as S
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert W.get_name()=='Dev_WestlandRegion'and not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert not(D/'Terrain.json').exists();actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()};rows=[];before=json.loads((D/'Inventory.json').read_text());todo=[r for r in before['Dev_WestlandRegion']if r['label'].startswith('WR_Terrain_')or r['label']=='WR_WindingRiver'];assert len(todo)==81;start=time.monotonic()
def job():
 for row in todo:
  a=actors[row['label']];c=a.get_component_by_class(unreal.StaticMeshComponent);src=unreal.load_asset(row['mesh']);q=ROOT+'/Meshes/'+src.get_name().replace('SM_WR_','SM_WEP_');assert not unreal.EditorAssetLibrary.does_asset_exist(q);out=unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name(),q);assert out;dm=unreal.DynamicMesh();dm,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(src,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert result==unreal.GeometryScriptOutcomePins.SUCCESS;_,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);assert not gaps;old=list(unreal.GeometryScript_List.convert_vector_list_to_array(vs));new=[];deltas=[]
  for p in old:
   e,n=S.L.en(p.x,p.y)
   if row['label']=='WR_WindingRiver':
    relative=e-S.L.river(n);width=(7+.9*math.sin(n/19))*.5;e=S.center(n)+relative/width*S.halfwidth(n);x,y,_=S.L.world(e,n);v=unreal.Vector(x,y,p.z);deltas.append(math.hypot(x-p.x,y-p.y))
   else:
    dz=S.delta(e,n,p.z/100)*100;v=unreal.Vector(p.x,p.y,p.z+dz);deltas.append(abs(dz))
   new.append(v)
  unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(new));unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions());opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,result=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,out,opt,unreal.GeometryScriptMeshWriteLOD());assert result==unreal.GeometryScriptOutcomePins.SUCCESS;assert out.get_num_triangles(0)==src.get_num_triangles(0);assert unreal.EditorAssetLibrary.save_loaded_asset(out,False);a.modify();c.set_static_mesh(out);rows.append(dict(actor=row['label'],source=src.get_path_name(),derived=out.get_path_name(),vertices=len(old),triangles=out.get_num_triangles(0),max_vertex_change_cm=max(deltas),protected_routes_pads_and_water_reaches=True));(D/'TerrainProgress.json').write_text(json.dumps(rows,indent=2));yield
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'Terrain.json').write_text(json.dumps(dict(passed=True,rows=rows,seconds=time.monotonic()-start),indent=2))
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wep_terrain)
 except Exception:
  (D/'TerrainFailure.json').write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._wep_terrain);unreal.log_error(traceback.format_exc())
 busy=False
unreal._wep_terrain=unreal.register_slate_post_tick_callback(tick)
