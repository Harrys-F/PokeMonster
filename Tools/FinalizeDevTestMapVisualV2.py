"""Correct winding of new ground ribbons and clear the retained gameplay test stations."""
import unreal,math,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/DevTestMapVisualV2';D='/Game/Environment/DevTestMapVisualV2';G='/Game/Environment/Westland/NaturalGroundV1'
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_editor_world();assert w.get_name()=='Dev_TestMap_VisualV2' and not E.get_game_world();A=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=list(A.get_all_level_actors());by={a.get_actor_label():a for a in actors};record={'paths':[]}
m=unreal.load_asset(D+'/Materials/M_V2_PathBlend');m.set_editor_property('two_sided',False);unreal.MaterialEditingLibrary.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,False)
paths={
 'Main':[(-760,-1410),(-760,-1110),(-780,-850),(-700,-640),(-440,-540),(-350,-480),(-350,-150),(-20,-40),(240,170),(470,360),(730,600),(760,850)],
 'Wild':[(-760,-1370),(-880,-1410),(-1000,-1430)],
 'VillageLoop':[(-760,-1410),(-1150,-1920),(-2100,-2060),(-3350,-1700),(-4150,-700),(-4100,450),(-3600,500)],
 'NorthLoop':[(-4100,450),(-4300,1550),(-3300,2050),(-2150,2000),(-1700,1220),(-1550,650),(-1580,-100),(-1560,-860),(-1520,-1830),(-1150,-1920)]}
paths['Cottage']=[(-3350,-1700),(-3310,-1290),(-3150,-1020),(-3020,-1020)]
route_samples=[]
def pathmesh(name,points,width):
 pts=[]
 for i in range(len(points)-1):
  p0,p1,p2,p3=[points[max(0,min(len(points)-1,j))] for j in (i-1,i,i+1,i+2)]
  for j in range(16):
   t=j/16;pts.append(tuple(.5*(2*p1[k]+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t**3) for k in (0,1)))
 pts.append(points[-1]);route_samples.extend(pts);vs=[];uv=[];tris=[]
 for i,(x,y) in enumerate(pts):
  prev=pts[max(0,i-1)];nxt=pts[min(len(pts)-1,i+1)];dx=nxt[0]-prev[0];dy=nxt[1]-prev[1];length=max(.1,math.hypot(dx,dy));bw=width*(1+.07*math.sin(i*.42))
  for j in range(7):
   v=j/6;vs.append(unreal.Vector(x-dy/length*(2*v-1)*bw/2,y+dx/length*(2*v-1)*bw/2,1.35));uv.append(unreal.Vector2D(i/(len(pts)-1),v))
   if i and j:
    a=(i-1)*7+j-1;b=i*7+j-1
    for t in [unreal.IntVector(a,b,b+1),unreal.IntVector(a,b+1,a+1)]:
     if (vs[t.y]-vs[t.x]).cross(vs[t.z]-vs[t.x]).z>0:t=unreal.IntVector(t.x,t.z,t.y)
     if (vs[t.y]-vs[t.x]).cross(vs[t.z]-vs[t.x]).length()>.01:tris.append(t)
 buf=unreal.GeometryScriptSimpleMeshBuffers();buf.vertices=vs;buf.triangles=tris;buf.uv0=uv;dm=unreal.DynamicMesh();unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dm,buf);unreal.GeometryScript_Normals.recompute_normals(dm,unreal.GeometryScriptCalculateNormalsOptions())
 mesh=unreal.load_asset(D+'/Meshes/SM_V2_Path_'+name)
 options=unreal.GeometryScriptCopyMeshToAssetOptions();options.enable_recompute_normals=True;options.enable_recompute_tangents=True
 if mesh:dm,result=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,mesh,options,unreal.GeometryScriptMeshWriteLOD())
 else:
  opts=unreal.GeometryScriptCreateNewStaticMeshAssetOptions();opts.enable_collision=False;opts.enable_nanite=False;opts.enable_recompute_normals=True;mesh,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dm,D+'/Meshes/SM_V2_Path_'+name,opts)
 assert mesh;mesh.set_material(0,m);unreal.EditorAssetLibrary.save_loaded_asset(mesh,False)
 if name=='Cottage' and 'V2_Path_Cottage' not in by:
  actor=A.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());actor.set_actor_label('V2_Path_Cottage');actor.static_mesh_component.set_static_mesh(mesh);actor.static_mesh_component.set_collision_profile_name('NoCollision');actor.static_mesh_component.set_cast_shadow(False);actor.set_folder_path('VisualV2/Environment')
 else:actor=by['V2_Path_'+name]
 actor.static_mesh_component.set_material(0,m)
 record['paths'].append({'name':name,'points_cm':points,'width_cm':width,'triangles':len(tris)})
for name,points in paths.items():pathmesh(name,points,270 if name!='Wild' else 140)

# Move only the newly assembled cottage so original isolated test actors remain outside.
shift=unreal.Vector(-500,-90,0) if abs(by['V2_Cottage_Cutaway'].get_actor_location().x+2250)<1 else unreal.Vector()
for a in actors:
 n=a.get_actor_label()
 if n.startswith('V2_Cottage_'):
  if isinstance(a,unreal.PokeMonsterBuildingCutaway):a.set_actor_location(a.get_actor_location()+shift,False,False)
  else:
   c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
   for i in range(c.get_instance_count()):
    t=c.get_instance_transform(i,True);t.translation=t.translation+shift;c.update_instance_transform(i,t,True,True,True)
 if n.startswith('V2_Instanced_'):
  c=a.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
  for i in reversed(range(c.get_instance_count())):
   p=c.get_instance_transform(i,True).translation
   if abs(p.x+2750)<360 and abs(p.y+1020)<360:c.remove_instance(i)
 if n.startswith(('V2_Bush_','V2_Stone_')):
  p=a.get_actor_location()
  if -1780<p.x<1650 and -430<p.y<-210:
   a.set_actor_location(unreal.Vector(p.x,-490 if p.y<-320 else -145,0),False,False)
assert unreal.EditorLoadingAndSavingUtils.save_map(w,'/Game/Maps/Dev_TestMap_VisualV2');(O/'PathFix.json').write_text(json.dumps(record,indent=2));unreal.SystemLibrary.execute_console_command(w,'MAP CHECK')
