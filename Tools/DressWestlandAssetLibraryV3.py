"""Additive V2/V3 forest comparisons on the existing independent library map.
No previous actor/asset changes; exactly one V3 oak and two V3 bush instances.
"""
import unreal,math,json,random
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibraryV3';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and w.get_name()=='Dev_WestlandAssetLibrary';D='/Game/Environment/WestlandAssetLibrary';V=D+'/QualityV3';old={a.get_actor_label():a for a in A.get_all_level_actors()};manifest=[]
def pos(e,n,z=0):return unreal.Vector((e+n)*math.sqrt(.5)*100,(e-n)*math.sqrt(.5)*100,z*100)
def mesh_actor(label,path,e,n,collision=False,yaw=45,scale=1):
 a=old.get(label)
 if not a:a=A.spawn_actor_from_class(unreal.StaticMeshActor,pos(e,n));a.set_actor_label(label)
 a.set_actor_location(pos(e,n),False,False);a.set_actor_rotation(unreal.Rotator(pitch=0,yaw=yaw,roll=0),False);a.set_actor_scale3d(unreal.Vector(scale,scale,scale));a.set_folder_path('WestlandAssetLibrary/ArtQualityV3');a.tags=['WLA_ArtV3'];c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset(path));assert c.static_mesh
 c.set_collision_profile_name('BlockAll' if collision else 'NoCollision');c.set_cast_shadow(True);c.set_editor_property('ld_max_draw_distance',10000);manifest.append({'label':label,'mesh':path,'E_N_m':[e,n],'scale':scale,'collision':collision});return a
pairs=[('Oak',-4,-11,10,-13,'Trees/SM_WLA_OakAncient_A','Trees/SM_WLA_OakAncient_V3',True),('BushA',-7.5,-14,6.5,-16,'Vegetation/SM_WLA_Bush_A','Vegetation/SM_WLA_WildBush_V3_A',False),('BushB',0,-14.5,14,-16.5,'Vegetation/SM_WLA_Bush_B','Vegetation/SM_WLA_WildBush_V3_B',False)]
for key,ea,na,eb,nb,v2,v3,coll in pairs:
 mesh_actor('V3_Compare_V2_'+key,D+'/Meshes/'+v2,ea,na,coll);mesh_actor('V3_Forest_'+key,V+'/Meshes/'+v3,eb,nb,coll)
for i,(e,n,sc) in enumerate([(7,-5.8,.7),(15.2,-12,.58),(-1,-7,.5)]):mesh_actor('V3_Forest_Rock_'+str(i),D+'/Meshes/Landscape/SM_WLA_Boulder_A',e,n,True,45+i*50,sc)
for i,(e,n) in enumerate([(4.7,-14.9),(12.7,-10.2),(15.7,-16.5)]):mesh_actor('V3_Forest_Stones_'+str(i),D+'/Meshes/Landscape/SM_WLA_SmallStones_A',e,n,False,30+i*60,.85)
# Curving 2.4-m forest loop linked to the earlier route; soft edge uses existing blend material.
pts=[(-14,-9),(-10,-11),(-4,-15.5),(3,-19),(10,-17),(13,-13),(10,-8),(6,-9),(-3,-9)]
samples=[]
for i in range(len(pts)):
 p0,p1,p2,p3=[pts[j%len(pts)] for j in (i-1,i,i+1,i+2)]
 for j in range(14):
  t=j/14;samples.append(tuple(.5*(2*p1[k]+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t**3) for k in (0,1)))
samples.append(samples[0]);vs=[];uv=[];tri=[]
for i,(e,n) in enumerate(samples):
 prev=samples[max(0,i-1)];nxt=samples[min(len(samples)-1,i+1)];dx=nxt[0]-prev[0];dy=nxt[1]-prev[1];length=math.hypot(dx,dy);width=2.4*(1+.08*math.sin(i*.21))
 for j in range(7):
  v=j/6;vs.append(pos(e-dy/length*(v*2-1)*width/2,n+dx/length*(v*2-1)*width/2,.014));uv.append(unreal.Vector2D(i/(len(samples)-1),v))
  if i and j:a=(i-1)*7+j-1;b=i*7+j-1;tri.extend([unreal.IntVector(a,b,b+1),unreal.IntVector(a,b+1,a+1)])
path=V+'/Meshes/Review/SM_WLA_V3_ForestPath';m=unreal.load_asset(path)
# Tight spline bends can reverse individual band triangles. Orient EACH face
# upward instead of averaging opposing corner normals (the initial warning cause).
tri=[t if (vs[t.y]-vs[t.x]).cross(vs[t.z]-vs[t.x]).z>0 else unreal.IntVector(t.x,t.z,t.y) for t in tri]
assert all((vs[t.y]-vs[t.x]).cross(vs[t.z]-vs[t.x]).z>.01 for t in tri)
buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=vs;buf.triangles=tri;buf.uv0=uv;buf.normals=[unreal.Vector(0,0,1) for _ in vs];dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf)
if not m:
 opts=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();opts.enable_collision=False;opts.enable_nanite=False;opts.enable_recompute_normals=False;opts.enable_recompute_tangents=True;m,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,path,opts);assert m
else:
 opts=unreal.GeometryScriptCopyMeshToAssetOptions();opts.enable_recompute_normals=False;opts.enable_recompute_tangents=True;opts.enable_remove_degenerates=True
 unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,m,opts,unreal.GeometryScriptMeshWriteLOD())
m.set_material(0,unreal.load_asset('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend'));assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)

pathactor=mesh_actor('V3_Forest_Path',path,0,0,False,0);pathactor.static_mesh_component.set_cast_shadow(False)
rng=random.Random(88419)
for key,num in [('Grass',35),('Wildflowers',20),('Herb',12)]:
 label='V3_Forest_Instanced_'+key;a=old.get(label)
 if not a:a=A.spawn_actor_from_class(unreal.Actor,unreal.Vector());a.set_actor_label(label)
 c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
 if not c:
  sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);root=sub.k2_gather_subobject_data_for_instance(a)[0];params=unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.HierarchicalInstancedStaticMeshComponent,skip_mark_blueprint_modified=True);handle,reason=sub.add_new_subobject(params);c=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle));assert c,reason
 c.set_static_mesh(unreal.load_asset(D+'/Meshes/Vegetation/SM_WLA_'+key+'_A'));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_cull_distances(6000,8000);a.set_folder_path('WestlandAssetLibrary/ArtQualityV3');a.tags=['WLA_ArtV3'];c.clear_instances();count=0
 for _ in range(num*8):
  e=rng.uniform(3,17);n=rng.uniform(-19,-7)
  if min(math.hypot(e-x,n-y) for x,y in samples)<1.7 or math.hypot(e-10,n+13)<1.8:continue
  sc=rng.uniform(.65,1.2);c.add_instance(unreal.Transform(location=pos(e,n),rotation=unreal.Rotator(pitch=0,yaw=rng.uniform(0,360),roll=0),scale=unreal.Vector(sc,sc,sc)),True);count+=1
  if count==num:break
 assert count==num;manifest.append({'label':label,'instances':count,'collision':False,'cast_shadow':False,'cull_cm':[6000,8000]})
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_WestlandAssetLibrary');(O/'MapLayout.json').write_text(json.dumps({'actors':manifest,'forest_path_E_N_m':pts,'path_width_m':2.4,'original_actors_not_modified':True},indent=2));unreal.log('WLA_V3_FOREST_READY')
