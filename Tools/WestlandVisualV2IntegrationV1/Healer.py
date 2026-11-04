"""Apply the actual V7 room surfaces and map V6 details through existing doorway anchors."""
import runpy,unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();globals().update(runpy.run_path(str(R/'Tools/WestlandVisualV2IntegrationV1/Common.py')));assert not(D/'Healer.json').exists();data=json.loads((D/'MigrationInputs.json').read_text());src=data['source'];target=actors['HouseCutaway'];td=target.relocated_door_threshold;sd=src['door'];sy=sd['rotation']['yaw'];angle=td.get_world_rotation().yaw-sy;rad=math.radians(angle);origin=td.get_world_location();sp=sd['location'];bindings=[];lights=[];unknown=[]
def mapped(p):
 x,y,z=(p[i]-sp[i]for i in range(3));return origin+unreal.Vector(x*math.cos(rad)-y*math.sin(rad),x*math.sin(rad)+y*math.cos(rad),z)
for row in src['room']:
 a=actors.get(row['label'])
 if not a:continue
 if not target.is_viewer_in_relocated_room(a.get_actor_location())and (a.get_actor_location()-target.relocated_interior_area.get_world_location()).length()>1300:continue
 by={c.get_name():c for c in a.get_components_by_class(unreal.StaticMeshComponent)}
 for cr in row['components']:
  c=by.get(cr['name'])
  if not c:continue
  for i,p in enumerate(cr['materials']):
   if not p:continue
   old=c.get_material(i);m=unreal.load_asset(p);assert m,p
   if old!=m:a.modify();c.set_material(i,m);bindings.append(dict(actor=a.get_actor_label(),slot=i,before=old.get_path_name()if old else None,after=p))
  c.set_cast_shadow(cr['shadow'])
for row in src['groups']:
 existing=actors.get('WVI_Healer_'+row['label'])
 if existing:
  assert existing.actor_has_tag('WestlandVisualV2IntegrationV1');c=existing.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent);assert c.static_mesh.get_path_name()==row['mesh'];c.clear_instances();groups['Healer_'+row['label']]=c
 else:c=group('Healer_'+row['label'],row['mesh'],row['materials'],row['shadow'])
 for inst in row['instances']:
  rot=dict(inst['rotation']);rot['yaw']+=angle;c.add_instance(unreal.Transform(location=mapped(inst['location']),rotation=unreal.Rotator(**rot),scale=unreal.Vector(*inst['scale'])),True)
for row in src['lights']:
 a=actors.get(row['label'])or actors.get('WVI_Healer_'+row['label'])
 if not a:
  assert row['label']=='InteriorDiffuse','Never fabricate a missing role'
  reference=unreal.load_asset('/Game/Maps/Dev_TestMap_VisualV2');reference_light=next(l for l in unreal.GameplayStatics.get_all_actors_of_class(reference,unreal.RectLight)if l.get_actor_label()=='V2_House_InteriorDiffuse');original=reference_light.get_component_by_class(unreal.RectLightComponent);a=own('Healer_InteriorDiffuse',unreal.RectLight,location=mapped(reference_light.get_actor_location().to_tuple()));rotation=reference_light.get_actor_rotation();a.set_actor_rotation(unreal.Rotator(pitch=rotation.pitch,yaw=rotation.yaw+angle,roll=rotation.roll),False);local=a.get_component_by_class(unreal.RectLightComponent)
  for key in ['attenuation_radius','source_width','source_height','indirect_lighting_intensity','volumetric_scattering_intensity','intensity_units','use_temperature','temperature']:local.set_editor_property(key,original.get_editor_property(key))
 c=a.get_component_by_class(unreal.LightComponent);assert c;c.set_intensity(row['intensity']);c.set_light_color(unreal.LinearColor(*row['color']),False);c.set_cast_shadows(row['shadow']);c.set_lighting_channels(True,True,False);lights.append(row['label'])
# Interior walls and furniture stay visible. Exterior roof/facade cutaway identity remains intact.
removed=[]
for a in list(target.occluding_actors):
 if a and (a.get_actor_location()-target.relocated_interior_area.get_world_location()).length()<1500:
  removed.append(a);a.set_actor_hidden_in_game(False)
  for c in a.get_components_by_class(unreal.PrimitiveComponent):c.set_visibility(True);c.set_hidden_in_game(False);c.set_custom_primitive_data_float(0,0)
target.occluding_actors=[a for a in target.occluding_actors if a and a not in removed];target.set_editor_property('stable_doorway_transition',True);target.set_editor_property('constrain_third_person_to_room',True);target.set_editor_property('use_shadowless_interior_lighting',True);target.doorway_landing_distance=150.;target.interior_camera_boundary_margin=85.
visual=next(a for a in actors.values()if isinstance(a,unreal.PokeMonsterNPCVisualActor)and a.source_actor==actors['HouseHealer']);visual.set_editor_property('shadowless_interior_presentation',True);visual.refresh_presentation()
before=json.loads((D/'Inventory.json').read_text())['Dev_WestlandRegion'];old={(r['label'],r['component']):r['materials']for r in before};bindings=[]
for row in src['room']:
 a=actors.get(row['label'])
 if not a:continue
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  prior=old.get((a.get_actor_label(),c.get_name()),[])
  for i in range(min(c.get_num_materials(),len(prior))):
   path=c.get_material(i).get_path_name()if c.get_material(i)else None
   if prior[i]!=path:bindings.append(dict(actor=a.get_actor_label(),slot=i,before=prior[i],after=path))
assert len(lights)==13 and len(bindings)>80,(len(lights),len(bindings));finish('Healer.json',dict(bindings=bindings,groups=[dict(name=n,instances=c.get_instance_count())for n,c in groups.items()],lights=lights,removed_remote_occluders=[a.get_actor_label()for a in removed],source_door=sd,target_door=dict(position=origin.to_tuple(),yaw=td.get_world_rotation().yaw),unchanged='Original room geometry, doors, healer identity, furniture positions, original wall collisions'))
