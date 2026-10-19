"""Only runtime camera blendables; persistent world, lights, TAA and gameplay are read-only."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir());S=R/'Saved/VisualV2ShadowQualityV8';j=json.loads((S/'VariantRequest.json').read_text());E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=next(w for w in unreal.ObjectIterator(unreal.World) if w.get_name()=='Dev_TestMap_VisualV2' and unreal.GameplayStatics.get_player_pawn(w,0));assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);cam=p.get_component_by_class(unreal.CameraComponent);volume=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume) if a.get_actor_label()=='V2_OutdoorExposure')
if not hasattr(unreal,'_sv8_mid'):
 parent=unreal.load_asset('/Game/Environment/VisualV2ShadowQualityV8/Materials/M_SV8_ShadowLift_Experimental');unreal._sv8_mid=unreal.MaterialLibrary.create_dynamic_material_instance(w,parent)
 volume.add_or_update_blendable(unreal._sv8_mid,1);assert volume.get_editor_property('blend_weight')==1
 others=[]
 for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
  if isinstance(a,unreal.PokeMonsterNPCVisualActor):others.append({'actor':a.source_actor,'radius':35});continue
  c=a.get_component_by_class(unreal.StaticMeshComponent)
  if not c or not c.static_mesh or a.get_editor_property('hidden') or not c.get_editor_property('visible') or c.get_editor_property('hidden_in_game'):continue
  tree=any(k in c.static_mesh.get_name() for k in ['Oak','Birch'])
  if tree:
   ts=[c.get_instance_transform(i,True).translation for i in range(c.get_instance_count())] if isinstance(c,unreal.InstancedStaticMeshComponent) else [c.get_world_location()]
   others.extend({'position':v,'radius':45} for v in ts)
  else:
   center,extent=a.get_actor_bounds(False)
   if c.cast_shadow and 15<max(extent.x,extent.y)<125 and extent.z>20 and center.z-extent.z<20:others.append({'position':center,'radius':25})
 def position(entry):return entry['actor'].get_actor_location() if 'actor' in entry else entry['position']
 def contacts(dt):
  mid=unreal._sv8_mid;q=p.get_actor_location();points=[(q.x,q.y,35)]
  for entry in sorted(others,key=lambda entry:(position(entry)-q).length())[:15]:
   pos=position(entry);points.append((pos.x,pos.y,entry['radius']))
  for i in range(16):
   x,y,r=points[i] if i<len(points) else (100000,100000,1);mid.set_vector_parameter_value('Contact'+str(i),unreal.LinearColor(x,y,0,r))
 unreal._sv8_contact_callback=unreal.register_slate_post_tick_callback(contacts)
mid=unreal._sv8_mid
for key,value in [('Gain',j.get('gain',0)),('Low',j.get('low',.40)),('High',j.get('high',1.20)),('Debug',j.get('debug',0))]:mid.set_scalar_parameter_value(key,float(value))
volume.add_or_update_blendable(mid,0 if j['variant']=='A' else 1)
(S/'RuntimeVariant.json').write_text(json.dumps({**j,'camera_blend_weight':cam.get_editor_property('post_process_blend_weight'),'world':w.get_path_name(),'original_map_modified':False},indent=2));unreal.log('SV8_RUNTIME_VARIANT '+j['variant'])
