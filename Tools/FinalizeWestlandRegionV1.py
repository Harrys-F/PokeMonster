"""Owned region corrections proven by walking review; run outside PIE.
Rebuilds only the Ufer path overlay, copies ground flora without ceramic pots,
and aligns the new map's spawn with the existing player presentation convention.
"""
import unreal,runpy,sys,json,math
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(ROOT/'Tools'));import WestlandRegionLayout as L;import importlib;importlib.reload(L)
B=runpy.run_path(str(ROOT/'Tools/BuildWestlandRegionV1.py'),run_name='region_library');A=B['A'];E=B['E'];assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion';by={a.get_actor_label():a for a in A.get_all_level_actors()};audit={}
def update(sm,vs,tri,uv):
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=[unreal.Vector(*v) for v in vs];buf.triangles=[unreal.IntVector(t[0],t[2],t[1]) for t in tri];buf.uv0=[unreal.Vector2D(*p) for p in uv];d=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,buf);opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,sm,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;unreal.EditorAssetLibrary.save_loaded_asset(sm,False)
def job():
 # Spawn rotation inherited from the rotated source world was inappropriate for
 # Paper2D's constructor-relative facing plane. This is map configuration only.
 start=by['WR_RegionPlayerStart'];audit['start_rotation_before']=str(start.get_actor_rotation());start.set_actor_rotation(unreal.Rotator(),False);audit['start_rotation_after']=str(start.get_actor_rotation());yield 'spawn yaw'
 name,points,width=L.PATHS[5];pts=L.sample(points,spacing=.5);vs=[];uv=[];tri=[]
 for i,p in enumerate(pts):
  q=pts[max(0,i-1)];r=pts[min(len(pts)-1,i+1)];dx=r[0]-q[0];dy=r[1]-q[1];length=max(.01,math.hypot(dx,dy))
  for j in range(9):
   s=j/8*2-1;e=p[0]-dy/length*width/2*s;n=p[1]+dx/length*width/2*s;vs.append(L.world(e,n,B['surface'](e,n)+.135));uv.append((i/(len(pts)-1),j/8))
   if i and j:a=(i-1)*9+j-1;b=a+9;tri.extend([(a,a+1,b+1),(a,b+1,b)])
 update(unreal.load_asset(L.ASSETS+'/Meshes/SM_WR_Path_'+name),vs,tri,uv);e,n=L.PLACES['Uferfund'];by['WR_RestBench_Uferfund'].set_actor_location(unreal.Vector(*L.world(e-3,n+2,B['surface'](e-3,n+2)+.42)),False,False);audit['uferfund_m']=[e,n];yield 'river bank overlay'
 for name in ['FlowerPlant','LeafPlant','BroadHerb','NarrowHerb']:
  target=L.ASSETS+'/Meshes/SM_WR_Ground_'+name;sm=unreal.load_asset(target)
  if not sm:
   source='/Game/Environment/HealingHouse/QualityV3/Meshes/SM_HH_Q3_'+name;assert unreal.EditorAssetLibrary.duplicate_asset(source,target);sm=unreal.load_asset(target);d=unreal.DynamicMesh();d,res=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(sm,d,unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS
   _,deleted=unreal.GeometryScript_Materials.delete_triangles_by_material_id(d,0);assert deleted>0
   # Pot starts below the foliage; sink the retained stems by 18 cm into the ground.
   unreal.GeometryScript_MeshTransforms.translate_mesh(d,unreal.Vector(0,0,-18));opt=unreal.GeometryScriptCopyMeshToAssetOptions();_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,sm,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;unreal.EditorAssetLibrary.save_loaded_asset(sm,False);audit['ground_'+name]={'ceramic_triangles_removed':deleted}
  c=by['WR_Garden_'+name].get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);c.set_static_mesh(sm);yield name+' ground form'
 (OUT/'FinalCorrections.json').write_text(json.dumps(audit,indent=2));yield 'finish'
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wr_final);del unreal._wr_final;unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
 except Exception as ex:unreal.unregister_slate_post_tick_callback(unreal._wr_final);del unreal._wr_final;unreal.log_error('REGION_FINAL_FAILED '+repr(ex))
 busy=False
unreal._wr_final=unreal.register_slate_post_tick_callback(tick)
