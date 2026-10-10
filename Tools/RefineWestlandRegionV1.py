"""Correct only owned upward surfaces; shared assets and gameplay remain untouched."""
import unreal,json,time
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/WestlandRegion'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world()
paths=[p for p in unreal.EditorAssetLibrary.list_assets('/Game/Environment/WestlandRegion/Meshes',True,False) if any(s in p for s in ['SM_WR_Terrain_','SM_WR_Path_','SM_WR_River.'])];audit=[];i=0;busy=False
def tick(dt):
 global i,busy
 if busy:return
 busy=True
 try:
  p=paths[i];m=unreal.load_asset(p);d=unreal.DynamicMesh();d,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(m,d,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS
  _,n1,n2,n3,valid=unreal.GeometryScript_MeshQueries.get_triangle_normals(d,0);assert valid
  before=n1.z
  if before<0:
   unreal.GeometryScript_Normals.flip_normals(d);opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True
   d,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,m,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS
   unreal.EditorAssetLibrary.save_loaded_asset(m,False)
  d=unreal.DynamicMesh();d,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(m,d,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,nn,_,_,valid=unreal.GeometryScript_MeshQueries.get_triangle_normals(d,0);assert valid and nn.z>.5,(p,nn)
  audit.append({'asset':p,'normal_z_before':before,'normal_z_after':nn.z,'triangles':m.get_num_triangles(0)});i+=1
  (OUT/'NormalAudit.json').write_text(json.dumps({'completed':i==len(paths),'meshes':audit},indent=2))
  if i==len(paths):unreal.unregister_slate_post_tick_callback(unreal._wr_refine);del unreal._wr_refine;unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),'/Game/Maps/Dev_WestlandRegion')
 except Exception as ex:
  unreal.unregister_slate_post_tick_callback(unreal._wr_refine);del unreal._wr_refine;unreal.log_error('REGION_NORMAL_FIX_FAILED '+repr(ex))
 busy=False
unreal._wr_refine=unreal.register_slate_post_tick_callback(tick)
