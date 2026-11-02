"""Contain the existing raised upstream river; fix only owned terrain derivatives."""
import unreal,json,sys,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandEnvironmentPolishV2';sys.path.insert(0,str(R/'Tools/WestlandEnvironmentPolishV2'));import Shapes as S;import importlib;importlib.reload(S)
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world();assert not(D/'BankGuard.json').exists();actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()};todo=[a for label,a in actors.items()if label.startswith('WR_Terrain_')];rows=[]
def job():
 for a in todo:
  out=a.static_mesh_component.static_mesh;assert out.get_path_name().startswith('/Game/Environment/WestlandEnvironmentPolishV2/');src=unreal.load_asset('/Game/Environment/WestlandRegion/Meshes/'+out.get_name().replace('SM_WEP_','SM_WR_'));assert src;dm=unreal.DynamicMesh();dm,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(src,dm,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;_,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);new=[];deltas=[]
  for p in unreal.GeometryScript_List.convert_vector_list_to_array(vs):
   e,n=S.L.en(p.x,p.y);base=p.z/100+S.delta(e,n,p.z/100);z=S.bank_height(e,n,base)*100;new.append(unreal.Vector(p.x,p.y,z));deltas.append(z-base*100)
  if max(deltas)>.001:
   unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(new));unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions());opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,out,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;assert unreal.EditorAssetLibrary.save_loaded_asset(out,False);rows.append(dict(tile=a.get_actor_label(),raised_vertices=sum(d>.001 for d in deltas),max_raise_cm=max(deltas)))
  yield
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();assert unreal.EditorLoadingAndSavingUtils.save_map(W,'/Game/Maps/Dev_WestlandRegion');(D/'BankGuard.json').write_text(json.dumps(dict(passed=True,rows=rows),indent=2))
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wep_bank)
 except Exception:(D/'BankGuardFailure.txt').write_text(traceback.format_exc());unreal.unregister_slate_post_tick_callback(unreal._wep_bank)
 busy=False
unreal._wep_bank=unreal.register_slate_post_tick_callback(tick)
