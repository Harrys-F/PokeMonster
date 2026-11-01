"""Comparable existing actor/component/instance audit, without exporting licensed geometry."""
import unreal,json,hashlib

def snapshot(actors):
 def t(v):return [list(v.translation.to_tuple()),[getattr(v.rotation,k)for k in ['x','y','z','w']],list(v.scale3d.to_tuple())]
 rows={}
 for a in actors:
  cs=[]
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   row={'name':c.get_name(),'mesh':c.static_mesh.get_path_name()if c.static_mesh else None,'materials':[c.get_material(i).get_path_name()if c.get_material(i)else None for i in range(c.get_num_materials())],'transform':t(c.get_world_transform()),'collision':str(c.get_collision_profile_name())}
   if isinstance(c,unreal.InstancedStaticMeshComponent):row['instances_sha256']=hashlib.sha256(json.dumps([t(c.get_instance_transform(i,True))for i in range(c.get_instance_count())]).encode()).hexdigest();row['count']=c.get_instance_count()
   cs.append(row)
  rows[a.get_name()]={'label':a.get_actor_label(),'class':a.get_class().get_path_name(),'transform':t(a.get_actor_transform()),'tags':[str(x)for x in a.tags],'components':cs}
 return rows
