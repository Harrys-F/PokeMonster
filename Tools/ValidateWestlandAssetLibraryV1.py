"""Editor-only complete import/material/scale/UCX audit and PIE capsule clearance probes."""
import unreal,json,math
from pathlib import Path
R=Path(unreal.Paths.project_dir());O=R/'Saved/WestlandAssetLibrary';data=json.loads((R/'Art/World/WestlandAssetLibrary/Assets.json').read_text());E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=E.get_game_world() or E.get_editor_world();assert 'Dev_WestlandAssetLibrary' in w.get_name();SM=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);game=E.get_game_world();actors=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor) if game else unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();by={a.get_actor_label():a for a in actors};rows=[]
for a in data['assets']:
 actor=by['Library_'+a['id']];c=actor.static_mesh_component;m=c.static_mesh;assert m and c.get_collision_enabled()==(unreal.CollisionEnabled.QUERY_AND_PHYSICS if a['collision_objects'] else unreal.CollisionEnabled.NO_COLLISION)
 assert all(c.get_material(i) for i in range(c.get_num_materials()));b=m.get_bounding_box();d=b.max-b.min
 for v,t in zip((d.x,d.y,d.z),a['dimensions_m']):assert abs(v/100-t)<max(.02,t*.01),(a['id'],v,t)
 assert b.min.z>=-.1,(a['id'],b.min.z)
 row={'id':a['id'],'scale_m':a['dimensions_m'],'triangles':m.get_num_triangles(0),'slots':c.get_num_materials(),'collision':a['collision'],'uv_channels':SM.get_num_uv_channels(m,0) if not game else 'validated in editor'}
 if not game:row['collision_bodies']=SM.get_simple_collision_count(m)+SM.get_convex_collision_count(m);assert row['collision_bodies']==len(a['collision_objects']);row['lods']=SM.get_lod_count(m)
 rows.append(row)
if game:
 p=unreal.GameplayStatics.get_player_pawn(w,0);assert p.get_component_by_class(unreal.CharacterMovementComponent).max_walk_speed==210;boom=p.get_component_by_class(unreal.SpringArmComponent);assert boom.target_arm_length==2500;assert p.get_component_by_class(unreal.CameraComponent).field_of_view==35
 # Sweep each real collider in both horizontal axes. Plant/canopy collision must stay absent.
 probes=[]
 for a in data['assets']:
  actor=by['Library_'+a['id']];center=actor.get_actor_location()+unreal.Vector(0,0,50)
  if a['collision_objects']:
   hits=[]
   for axis in (unreal.Vector(1,0,0),unreal.Vector(0,1,0)):
    hit=unreal.SystemLibrary.capsule_trace_single_for_objects(w,center-axis*400,center+axis*400,28,48,[unreal.ObjectTypeQuery.ECC_WORLD_STATIC],False,[x for x in actors if x!=actor],unreal.DrawDebugTrace.NONE,True);hits.append(bool(hit))
   assert any(hits),(a['id'],'missing blocker');probes.append({'id':a['id'],'blocker_detected':True})
 dataout={'passed':True,'mode':'PIE collision and scale audit','assets':rows,'collision_probes':probes,'camera_and_movement_unchanged':True}
else:
 unreal.SystemLibrary.execute_console_command(w,'MAP CHECK');dataout={'passed':True,'mode':'editor full geometry/material import audit','assets':rows,'total_lod0_triangles':sum(x['triangles'] for x in rows),'material_slots_range':[min(x['slots'] for x in rows),max(x['slots'] for x in rows)],'hism_instances':sum(c.get_instance_count() for a in actors for c in a.get_components_by_class(unreal.HierarchicalInstancedStaticMeshComponent))}
(O/('PIEAudit.json' if game else 'FinalAudit.json')).write_text(json.dumps(dataout,indent=2)+'\n');unreal.log('WLA_VALIDATION_PASSED')
