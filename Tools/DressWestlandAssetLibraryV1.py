"""Additive landscape review route in the independent library map, no gameplay alterations."""
import unreal,math,json
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibrary';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);w=E.get_editor_world();assert not E.get_game_world() and w.get_name()=='Dev_WestlandAssetLibrary';D='/Game/Environment/WestlandAssetLibrary'
# Smooth closed loop through forest edge, rocks, village yard, farm and ruin garden.
pts=[(-14,-9),(-14,4),(-10,8),(-3,7),(5,5),(8,-4),(20,-4),(20,8),(11,12),(7,14),(4,7),(6,-9)]
vs=[];uv=[];tri=[];samples=[]
for i in range(len(pts)):
 p0,p1,p2,p3=[pts[j%len(pts)] for j in (i-1,i,i+1,i+2)]
 for j in range(14):
  t=j/14;e=.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t*t+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t**3);n=.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t*t+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t**3);samples.append((e,n))
samples.append(samples[0]);N=len(samples)
for i,(e,n) in enumerate(samples):
 prev=samples[max(0,i-1)];nxt=samples[min(N-1,i+1)];dx,dy=nxt[0]-prev[0],nxt[1]-prev[1];l=math.hypot(dx,dy);width=2.4*(1+.12*math.sin(i*.17))
 for j in range(7):
  v=j/6;ee=e-dy/l*(v*2-1)*width/2;nn=n+dx/l*(v*2-1)*width/2;vs.append(unreal.Vector((ee+nn)*math.sqrt(.5)*100,(ee-nn)*math.sqrt(.5)*100,1.4));uv.append(unreal.Vector2D(i/(N-1),v))
  if i and j:
   a=(i-1)*7+j-1;b=i*7+j-1;tri.extend([unreal.IntVector(a,b,b+1),unreal.IntVector(a,b+1,a+1)])
p=D+'/Meshes/Review/SM_WLA_ReviewLoop';m=unreal.load_asset(p)
if not m:
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=vs;buf.triangles=tri;buf.uv0=uv;dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf);unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions());_,normal,_,_,valid=unreal.GeometryScript_MeshQueries.get_triangle_normals(dm,0)
 if normal.z<0:unreal.GeometryScript_Normals.flip_normals(dm)
 opt=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();opt.enable_collision=False;opt.enable_nanite=False;opt.enable_recompute_normals=True;m,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,p,opt);assert m;m.set_material(0,unreal.load_asset('/Game/Environment/Westland/NaturalGroundV1/Materials/M_WL_NG_PathBlend'));assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
a=next((a for a in A.get_all_level_actors() if a.get_actor_label()=='WLA_ReviewLoop'),None)
if not a:a=A.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());a.set_actor_label('WLA_ReviewLoop');a.set_folder_path('WestlandAssetLibrary/Ground');a.tags=['WLA_V1']
a.static_mesh_component.set_static_mesh(m);a.static_mesh_component.set_collision_profile_name('NoCollision');a.static_mesh_component.set_cast_shadow(False)
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_WestlandAssetLibrary');(O/'LandscapeReviewLayout.json').write_text(json.dumps({'path_points_E_N_m':pts,'path_width_m':2.4,'collision':'ground only','shared_ground_materials_read_only':True},indent=2)+'\n');unreal.log('WLA_LANDSCAPE_REVIEW_READY')
