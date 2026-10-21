"""Numeric existing-map safety snapshot; no saves, loading or mutations."""
import unreal,json,hashlib
def transform(t):return {'translation':t.translation.to_tuple(),'rotation':[t.rotation.x,t.rotation.y,t.rotation.z,t.rotation.w],'scale':t.scale3d.to_tuple()}
def snapshot(A):
 result={}
 for a in A.get_all_level_actors():
  components=[]
  for c in a.get_components_by_class(unreal.SceneComponent):
   row={'name':c.get_name(),'class':c.get_class().get_name(),'transform':transform(c.get_world_transform())}
   if isinstance(c,unreal.PrimitiveComponent):row.update(collision=str(c.get_collision_enabled()),profile=str(c.get_collision_profile_name()),shadow=c.cast_shadow)
   if isinstance(c,unreal.MeshComponent):row['materials']=[m.get_path_name()if m else None for m in c.get_materials()]
   if isinstance(c,unreal.StaticMeshComponent):row['mesh']=c.static_mesh.get_path_name()if c.static_mesh else None
   if isinstance(c,unreal.InstancedStaticMeshComponent):row['instances_sha256']=hashlib.sha256(json.dumps([transform(c.get_instance_transform(i,True))for i in range(c.get_instance_count())],sort_keys=True).encode()).hexdigest()
   if isinstance(c,unreal.LightComponent):row.update(intensity=c.intensity,color=str(c.light_color))
   components.append(row)
  result[a.get_path_name()]={'name':a.get_actor_label(),'class':a.get_class().get_name(),'transform':transform(a.get_actor_transform()),'tags':[str(t)for t in a.tags],'components':components}
 return result
