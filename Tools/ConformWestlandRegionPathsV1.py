"""Final ground-exact road surface pass; visual meshes only, no collision changes."""
import unreal,sys,json,runpy
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();O=ROOT/'Saved/WestlandRegion';sys.path.insert(0,str(ROOT/'Tools'));sys.dont_write_bytecode=True;import WestlandRegionLayout as L;import importlib;importlib.reload(L);from WestlandRegionPathMesh import build
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion'
paths=[{'name':n,'points_m':p,'width_m':w} for n,p,w in L.PATHS]+json.loads((ROOT/'Art/World/WestlandRegion/WestlandRegion_Access.json').read_text());audit=[]
def job():
 for p in paths:
  vs,tri,uv=build(p['points_m'],p['width_m']);sm=unreal.load_asset(L.ASSETS+'/Meshes/SM_WR_Path_'+p['name']);buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=[unreal.Vector(*v) for v in vs];buf.triangles=[unreal.IntVector(t[0],t[2],t[1]) for t in tri];buf.uv0=[unreal.Vector2D(*v) for v in uv];d=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,buf);opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,sm,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;unreal.EditorAssetLibrary.save_loaded_asset(sm,False);audit.append({'path':p['name'],'triangles':len(tri),'normal_surface_offset_cm':1.2});yield p['name']
 (O/'ConformedPaths.json').write_text(json.dumps(audit,indent=2));yield 'finished'
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wr_conform);del unreal._wr_conform;unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
 except Exception as ex:unreal.unregister_slate_post_tick_callback(unreal._wr_conform);del unreal._wr_conform;unreal.log_error('REGION_CONFORM_FAILED '+repr(ex))
 busy=False
unreal._wr_conform=unreal.register_slate_post_tick_callback(tick)
