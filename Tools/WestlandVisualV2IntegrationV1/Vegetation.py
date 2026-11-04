"""Reuse a subset of the same flower placements for approved Fab variety; preserve total count."""
import unreal,runpy,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandVisualV2IntegrationV1/Common.py')));assert not(D/'Vegetation.json').exists();src=[a for n,a in actors.items()if n.startswith('WEP_Wildflowers_')];before=sum(a.get_component_by_class(unreal.InstancedStaticMeshComponent).get_instance_count()for a in src);plants=[];changes=[];root='/Game/StyleHex_Studio/Free_Packs/FREE_Stylized_Grass_Flowers_Foliage/Meshes/'
for i in range(4):plants.append(group('FlowerVariety_'+str(i+1),root+'SM_Fol_Flower_Clump_'+str(i+1),[ROOT+'/Materials/MI_WI_FabFlowers'],False,7000))
for a in src:
 c=a.get_component_by_class(unreal.InstancedStaticMeshComponent);box=c.static_mesh.get_bounding_box();old=[]
 for i in range(c.get_instance_count()):
  if i%4:continue
  t=c.get_instance_transform(i,True);center=unreal.MathLibrary.transform_location(t,unreal.Vector((box.min.x+box.max.x)*.5,(box.min.y+box.max.y)*.5,box.min.z));target=plants[(i//4+len(changes))%4];b=target.static_mesh.get_bounding_box();scale=(box.max.z-box.min.z)*t.scale3d.z/(b.max.z-b.min.z);rt=unreal.Transform(rotation=t.rotation.rotator(),scale=unreal.Vector(scale,scale,scale));offset=unreal.MathLibrary.transform_location(rt,unreal.Vector((b.min.x+b.max.x)*.5,(b.min.y+b.max.y)*.5,b.min.z));rt.translation=center-offset;target.add_instance(rt,True);old.append(i)
 a.modify()
 for i in reversed(old):assert c.remove_instance(i)
 changes.append(dict(source=a.get_actor_label(),retained=c.get_instance_count(),varied=len(old)))
after=sum(a.get_component_by_class(unreal.InstancedStaticMeshComponent).get_instance_count()for a in src)+sum(c.get_instance_count()for c in plants);assert before==after==12369;finish('Vegetation.json',dict(changes=changes,total_before=before,total_after=after,new_groups=[dict(mesh=c.static_mesh.get_path_name(),instances=c.get_instance_count())for c in plants],original_trees_grasses_understory_unchanged=True,quality_requires_real_comparison=True))
