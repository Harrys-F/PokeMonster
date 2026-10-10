"""Natural steep backdrop at the far edge of the additional 100 m scenery.
Core 800 x 600 m and all walked routes remain unchanged. No invisible border wall.
"""
import unreal,runpy,sys,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();OLD=runpy.run_path(str(R/'Art/World/WestlandRegion/Source/LayoutBeforeMill.py'),run_name='old_ground');O=R/'Saved/WestlandRegion';sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'Tools'));import WestlandRegionLayout as L;import importlib;importlib.reload(L)
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);assert not E.get_game_world();assert E.get_editor_world().get_name()=='Dev_WestlandRegion';actors=A.get_all_level_actors();assert not any(a.get_actor_label()=='WR_BoundaryComplete' for a in actors);audit={'tiles':[],'shifted_instances':0}
def job():
 for tx in range(10):
  for ty in range(8):
   e0=-500+tx*100;n0=-400+ty*100;vs=[];uv=[];tri=[]
   for i in range(51):
    for j in range(51):e=e0+i*2;n=n0+j*2;vs.append(L.world(e,n,L.height(e,n)));uv.append((e/2,n/2))
   for i in range(50):
    for j in range(50):a=i*51+j;b=a+51;c=b+1;d=a+1;tri.extend([(a,d,c),(a,c,b)])
   sm=unreal.load_asset(L.ASSETS+'/Meshes/SM_WR_Terrain_%02d_%02d'%(tx,ty));buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=[unreal.Vector(*v) for v in vs];buf.triangles=[unreal.IntVector(t[0],t[2],t[1]) for t in tri];buf.uv0=[unreal.Vector2D(*v) for v in uv];dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf);opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;_,res=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,sm,opt,unreal.GeometryScriptMeshWriteLOD());assert res==unreal.GeometryScriptOutcomePins.SUCCESS;unreal.EditorAssetLibrary.save_loaded_asset(sm,False);audit['tiles'].append([tx,ty]);yield 'boundary tile'
 for a in actors:
  for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent):
   changed=False
   for i in range(c.get_instance_count()):
    t=c.get_instance_transform(i,True);q=t.translation;e,n=L.en(q.x,q.y);ridge=L.height(e,n)-(OLD['height'](e,n)-OLD['backdrop_ridge'](e,n))
    if abs(ridge)>.001:t.translation=unreal.Vector(q.x,q.y,q.z+ridge*100);c.update_instance_transform(i,t,True,False,True);changed=True;audit['shifted_instances']+=1
   if changed:c.update_instance_transform(i,c.get_instance_transform(i,True),True,True,True)
  yield a.get_actor_label()
 actor=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());actor.set_actor_label('WR_BoundaryComplete');actor.tags=[L.TAG];actor.set_folder_path('WestlandRegion/Metadata');(O/'Boundary.json').write_text(json.dumps(audit,indent=2));yield 'finished'
gen=job();busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:next(gen)
 except StopIteration:unreal.unregister_slate_post_tick_callback(unreal._wr_bound);del unreal._wr_bound;unreal.EditorLoadingAndSavingUtils.save_map(E.get_editor_world(),L.MAP)
 except Exception as ex:unreal.unregister_slate_post_tick_callback(unreal._wr_bound);del unreal._wr_bound;unreal.log_error('REGION_BOUNDARY_FAILED '+repr(ex))
 busy=False
unreal._wr_bound=unreal.register_slate_post_tick_callback(tick)
