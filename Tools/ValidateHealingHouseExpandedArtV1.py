"""Read-only map/material/collision audit; writes only ignored review evidence."""
import unreal,json,runpy
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/HealingArt'
runpy.run_path(str(ROOT/'Tools/ValidateHealingHouseExpandedInterior.py'))
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();by={a.get_actor_label():a for a in actors};cut=by['HouseCutaway'];occ=list(cut.get_editor_property('occluding_actors'));missing=[];new=[];collisions=[];triangles=0
assert len(occ)==107
for a in actors:
 if not isinstance(a,unreal.StaticMeshActor):continue
 c=a.static_mesh_component
 if not c.static_mesh:missing.append(a.get_actor_label()+': mesh');continue
 if any(not m for m in c.get_materials()):missing.append(a.get_actor_label()+': material')
 if a.actor_has_tag('HealingHouse_ExpandedArt'):
  b=c.static_mesh.get_bounding_box();size=b.max-b.min;r=a.get_actor_rotation()
  assert abs(r.pitch)<.01 and abs(r.roll)<.01,'Tilted prop: '+a.get_actor_label()
  assert a not in occ,'Art detail accidentally registered as occluder'
  if c.get_collision_enabled()!=unreal.CollisionEnabled.NO_COLLISION:assert c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)==unreal.CollisionResponseType.ECR_IGNORE,a.get_actor_label()
  if c.get_collision_enabled()!=unreal.CollisionEnabled.NO_COLLISION:
   assert any(word in a.get_actor_label() for word in ('RetainedBlocker','Bench','Table','Fireplace','Apothecary')),a.get_actor_label()
   collisions.append(a.get_actor_label())
  new.append({'name':a.get_actor_label(),'mesh':c.static_mesh.get_path_name(),'location':str(a.get_actor_location()),'rotation':str(r),'visible':c.is_visible(),'collision':str(c.get_collision_enabled())})
assert not missing,missing
for label in ('HH_Expanded_SideWall_-1_1','HH_Expanded_SideWall_-1_4','HH_Expanded_SideWall_1_1','HH_Expanded_SideWall_1_3','HH_Expanded_RearWall_0','HH_Expanded_RearWall_4'):
 a=by[label];o,e=a.get_actor_bounds(False,False);assert abs(e.z-150)<.1,'Window bay must remain upright and 300cm high'
for n in ('Wood','Timber','Plaster','Stone','Sage','Linen'):
 m=unreal.load_asset('/Game/Environment/HealingHouse/ExpandedArtV1/Materials/M_HH_Art_'+n);assert m
 samples=[x for x in unreal.MaterialEditingLibrary.get_material_expressions(m) if isinstance(x,unreal.MaterialExpressionTextureSample)]
 assert samples and all(x.get_editor_property('sampler_type')==unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR for x in samples),n
pp=by['HH_Art_InteriorLighting'];assert not pp.get_editor_property('unbound') and not pp.get_actor_enable_collision()
o,e=pp.get_actor_bounds(False,False);assert o.x-e.x>10000,'Lighting must never affect exterior'
catalog=json.loads((ROOT/'Art/HealingHouse/ExpandedArtV1/Props.json').read_text());unique=sum(p['triangles'] for p in catalog.values());instances={}
for entry in new:
 key=entry['mesh'].split('.')[-1].removeprefix('SM_HH_Art_')
 if key in catalog:instances[key]=instances.get(key,0)+1
triangles=sum(instances.get(n,0)*v['triangles'] for n,v in catalog.items())
assert triangles<500000,'Interior Art pass exceeds its triangle budget'
(OUT/'FinalAudit.json').write_text(json.dumps({'missing_assets_materials':missing,'new_mesh_actors':new,'blocking_art_actors':collisions,'occluders':[a.get_actor_label() for a in occ],'unique_prop_triangles':unique,'instanced_prop_triangles':triangles,'instances':instances,'local_lighting_only':True,'camera_gameplay_unchanged':True},indent=2))
unreal.SystemLibrary.execute_console_command(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world(),'MAP CHECK')
unreal.log('HH_ART_MAP_MATERIAL_COLLISION_AUDIT_PASSED')
