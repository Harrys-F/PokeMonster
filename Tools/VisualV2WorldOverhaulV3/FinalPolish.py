"""Refine own surfaces and remove only doorway/paving vegetation intersections."""
import runpy
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/VisualV2WorldOverhaulV3/Common.py')));assert not(D/'FinalPolish.json').exists()
m=unreal.load_asset(ROOT+'/Materials/M_WOV_Cobbles')
for n in ML.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom):
  n.set_editor_property('code','float2 q=P.xy/29;float row=floor(q.y);q.x+=fmod(row,2)*.47+.13*sin(row*3.1);float2 id=floor(q);float v=frac(sin(dot(id,float2(12.9898,78.233)))*43758.5453);float2 f=frac(q)-.5;float d=pow(abs(f.x)*2,4)+pow(abs(f.y)*2,4);float edge=1-smoothstep(.61,.88,d+sin(f.x*18+v*5)*.035);float grain=.95+.05*sin(P.x*.31+sin(P.y*.27));return lerp(float3(.045,.038,.026),lerp(float3(.14,.12,.085),float3(.22,.205,.16),v)*grain,edge);')
ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
m=unreal.load_asset(ROOT+'/Materials/M_WOV_Ground')
for n in ML.get_material_expressions(m):
 if isinstance(n,unreal.MaterialExpressionCustom)and'float variation='in n.get_editor_property('code'):n.set_editor_property('code',n.get_editor_property('code').replace('G*float3(.82,1.0,.70)*variation','lerp(G*float3(.82,1.0,.70),dot(G,float3(.299,.587,.114))*float3(.55,.86,.32),.55)*variation'))
ML.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
def clear(x,y):return(-4260<x<-3570 and 190<y<810)or(-3430<x<-2980 and abs(y+1020)<110)
removed=[];moved=[]
for a in actors.values():
 label=a.get_actor_label()
 if not label.startswith(('V2_Bush_','EQ3_','FAT_','EP2_','ArtV','Refined_','WOV3_','WA')):continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if not c.static_mesh or not c.is_visible()or c.get_editor_property('hidden_in_game'):continue
  mesh=c.static_mesh.get_path_name().lower()
  if not any(k in mesh for k in ['grass','fern','flower','clover','bush','shrub','moss','pratia']):continue
  if isinstance(c,unreal.InstancedStaticMeshComponent):
   ids=[i for i in range(c.get_instance_count())if clear(c.get_instance_transform(i,True).translation.x,c.get_instance_transform(i,True).translation.y)]
   if ids:a.modify();c.modify();assert c.remove_instances(ids);removed.append(dict(label=label,count=len(ids)))
  else:
   p=a.get_actor_location()
   if clear(p.x,p.y):
    a.modify();a.set_actor_location(unreal.Vector(p.x,p.y-310 if p.y<0 else p.y+470,p.z),False,False);moved.append(dict(label=label,before=p.to_tuple(),after=a.get_actor_location().to_tuple()))
save('FinalPolish.json',dict(removed_intruding_instances=removed,moved_decorative_shrubs=moved))
