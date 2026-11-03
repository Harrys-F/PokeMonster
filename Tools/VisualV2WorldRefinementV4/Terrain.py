"""Derived actual ground + visual-only distant land; protect roads, pads and gameplay actors."""
import unreal,runpy,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldRefinementV4/Common.py')));assert not(D/'Terrain.json').exists();src=actors['V2_Ground'].static_mesh_component.static_mesh;dm,_=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(src,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,ps,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);ps=unreal.GeometryScript_List.convert_vector_list_to_array(ps);old={};new={};coords=[]
for p in ps:
 if p.z>-500:
  key=(round(p.x),round(p.y));old[key]=max(old.get(key,-99999),p.z);z=bed(p.x,p.y,p.z);new[key]=max(new.get(key,-99999),z)
 else:z=p.z
 coords.append(unreal.Vector(p.x,p.y,z))
unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(coords));opt=unreal.GeometryScriptCopyMeshToAssetOptions();opt.enable_recompute_normals=True;m=unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name(),ROOT+'/Meshes/SM_WR4_Ground');assert m;unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,m,opt,unreal.GeometryScriptMeshWriteLOD());m.get_editor_property('body_setup').set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);m.set_material(0,material('Ground'));assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);a=actors['V2_Ground'];a.modify();a.static_mesh_component.set_static_mesh(m);a.static_mesh_component.set_material(0,material('Ground'))
def sample(table,x,y):
 x=min(3000,max(-6000,x));y=min(3250,max(-3250,y));xx=math.floor(x/50)*50;yy=math.floor(y/50)*50;t=(x-xx)/50;u=(y-yy)/50
 def get(a,b):return table.get((min(3000,a),min(3250,b)),0)
 return(1-u)*((1-t)*get(xx,yy)+t*get(xx+50,yy))+u*((1-t)*get(xx,yy+50)+t*get(xx+50,yy+50))
# Four adjoining rectangles outside the existing ground; no playable collision extension.
bg=unreal.DynamicMesh()
for xmin,ymin,xmax,ymax in [(-10000,-7250,-6000,7250),(3000,-7250,7000,7250),(-6000,3250,3000,7250),(-6000,-7250,3000,-3250)]:
 unreal.GeometryScript_Primitives.append_rectangle_xy(bg,unreal.GeometryScriptPrimitiveOptions(),unreal.Transform(location=unreal.Vector((xmin+xmax)/2,(ymin+ymax)/2,0)),xmax-xmin,ymax-ymin,max(2,round((xmax-xmin)/200)),max(2,round((ymax-ymin)/200)))
_,vs,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(bg,True);vs=unreal.GeometryScript_List.convert_vector_list_to_array(vs);out=[]
for p in vs:
 x,y=p.x,p.y;bx=min(3000,max(-6000,x));by=min(3250,max(-3250,y));dist=math.hypot(x-bx,y-by);t=smooth(dist/1500);ridge=370+140*math.sin(x*.00061+y*.00073)+100*math.sin(x*.0011-y*.00041);z=sample(new,bx,by)*(1-t)+t*ridge;out.append(unreal.Vector(x,y,z))
unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(bg,unreal.GeometryScript_List.convert_array_to_vector_list(out));m=unreal.EditorAssetLibrary.duplicate_asset('/Engine/BasicShapes/Plane',ROOT+'/Meshes/SM_WR4_DistantLand');unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(bg,m,opt,unreal.GeometryScriptMeshWriteLOD());m.set_material(0,material('Backdrop'));assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);a=A.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());a.set_actor_label('WR4_DistantLand');a.tags=['VisualV2WorldRefinementV4'];c=a.static_mesh_component;c.set_static_mesh(m);c.set_material(0,material('Backdrop'));c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_editor_property('affect_distance_field_lighting',False)
# Reground existing visual scenery and its old static collision proxies, not functional actors.
rebased=[]
for a in actors.values():
 label=a.get_actor_label()
 if not label.startswith(('V2_Tree','V2_Birch','V2_ForestOak','V2_Stone','V2_Bush','V2_Instanced','WA','EQ3','ArtV','Refined_','FAT_','EP2_','WOV3_','VS_')):continue
 if any(k in label for k in ['Bridge','WaterBlock','Ground','Floor','House','Cottage','Hill_Step','Lookout']):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh:continue
  b=c.static_mesh.get_bounding_box()
  if b.max.x-b.min.x>1800 or b.max.y-b.min.y>1800:continue
  ts=[(i,c.get_instance_transform(i,True))for i in range(c.get_instance_count())]if isinstance(c,unreal.InstancedStaticMeshComponent)else[(None,c.get_world_transform())];n=0
  for i,t in ts:
   p=t.translation
   if not(-5900<p.x<2900 and-3150<p.y<3150):continue
   oz=sample(old,p.x,p.y);nz=sample(new,p.x,p.y);dz=nz-oz
   if c.is_visible()and not c.get_editor_property('hidden_in_game')and any(k in c.static_mesh.get_name().lower()for k in ['grass','flower','fern','stone','rock','pratia','clover','moss']):
    base=p.z+b.min.z*t.scale3d.z;gap=base-oz
    if -25<gap<35:dz-=max(0,gap)+.5
   if abs(dz)<.15:continue
   a.modify();c.modify();t.translation=unreal.Vector(p.x,p.y,p.z+dz)
   if i is None:c.set_world_transform(t,False,False)
   else:c.update_instance_transform(i,t,True,False,True)
   n+=1
  if n:
   if isinstance(c,unreal.InstancedStaticMeshComponent)and c.get_instance_count():c.update_instance_transform(0,c.get_instance_transform(0,True),True,True,True)
   rebased.append(dict(label=label,count=n))
# Match the actual single pond surface to the new non-circular bank.
a=actors['P2D_Surface_Pond_Water'];src=a.static_mesh_component.static_mesh;dm,_=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(src,unreal.DynamicMesh(),unreal.GeometryScriptCopyMeshFromAssetOptions(),unreal.GeometryScriptMeshReadLOD());_,vs,_=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(dm,True);vs=unreal.GeometryScript_List.convert_vector_list_to_array(vs);out=[]
for p in vs:
 dx,dy=(p.x-720)/900,(p.y+1800)/650;r=math.hypot(dx,dy)
 if r>.5:q=shore(math.atan2(dy,dx));p=unreal.Vector(720+(p.x-720)*q,-1800+(p.y+1800)*q,p.z)
 out.append(p)
unreal.GeometryScript_MeshEdits.set_all_mesh_vertex_positions(dm,unreal.GeometryScript_List.convert_array_to_vector_list(out));m=unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name(),ROOT+'/Meshes/SM_WR4_PondWater');unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm,m,opt,unreal.GeometryScriptMeshWriteLOD());assert unreal.EditorAssetLibrary.save_loaded_asset(m,False);a.modify();a.static_mesh_component.set_static_mesh(m)
(D/'GroundHeightGrid.json').write_text(json.dumps(dict(old=[[x,y,z]for(x,y),z in old.items()],new=[[x,y,z]for(x,y),z in new.items()])));save('Terrain.json',dict(rebased=rebased,ground_source='/Game/Environment/VisualV2WorldOverhaulV3/Meshes/SM_WOV_Ground',playable_extents_unchanged=True,distant_land_collision=False,pond_deep_core_cm=420))
