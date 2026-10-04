"""Read-only authored-map audit. Writes evidence only to ignored Saved/."""
import unreal,json,math
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();OUT=ROOT/'Saved/HealingExpanded';OUT.mkdir(parents=True,exist_ok=True)
editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not editor.get_game_world()
world=editor.get_editor_world();assert world.get_name()=='Dev_HealingHouseTestMap'
objects=list(unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors())
by={a.get_actor_label():a for a in objects};cut=by['HouseCutaway'];door=cut.get_editor_property('door_threshold');inner=cut.get_editor_property('relocated_door_threshold');area=cut.get_editor_property('relocated_interior_area')
assert cut.get_editor_property('use_relocated_interior') and cut.get_editor_property('use_interior_camera')
assert door.get_world_location()==unreal.Vector(-450,0,107.5)
assert inner.get_world_location()==unreal.Vector(19500,0,107.5)
assert door.get_world_rotation()==inner.get_world_rotation()
assert door.get_unscaled_box_extent()==inner.get_unscaled_box_extent()==unreal.Vector(20,75,107.5)
assert abs(cut.get_editor_property('fade_duration')-.4)<1e-6
assert cut.get_editor_property('interior_camera_distance')==2600
assert cut.get_editor_property('relocated_camera_target')==unreal.Vector(-60,0,-70)
for side in (-1,1):
    assert by['HH_Expanded_FrontWall_'+str(side)].get_actor_scale3d().x==.3, 'Inner and outer jamb thickness must both be 30 cm'
assert cut.get_editor_property('interior_camera_pitch')==-50
assert cut.get_editor_property('interior_camera_yaw_offset')==0
assert area.get_world_location()==unreal.Vector(20000,0,150)
healer=by['HouseHealer'];assert healer.get_actor_location()==unreal.Vector(20330,-80,62)
assert healer.get_editor_property('save_after_rest') and healer.get_editor_property('activate_checkpoint')
assert str(healer.get_editor_property('checkpoint_id'))=='Dev_HealingHouse'
missing=[];meshes=[];own=[]
for actor in objects:
    if not isinstance(actor,unreal.StaticMeshActor):continue
    c=actor.static_mesh_component;mesh=c.static_mesh
    if not mesh:missing.append(actor.get_actor_label()+': mesh');continue
    for slot,m in enumerate(c.get_materials()):
        if not m:missing.append(actor.get_actor_label()+': material '+str(slot))
    if actor.actor_has_tag('HealingHouse_Expanded'):
        own.append(actor.get_actor_label())
        meshes.append({'actor':actor.get_actor_label(),'mesh':mesh.get_path_name(),'materials':[m.get_path_name() if m else None for m in c.get_materials()],'collision':str(c.get_collision_enabled()),'rotation':str(actor.get_actor_rotation()),'location':str(actor.get_actor_location())})
        assert not any(math.isnan(x) for x in [actor.get_actor_location().x,actor.get_actor_location().y,actor.get_actor_location().z])
        if actor.get_actor_label().startswith('HH_Expanded_Side'):
            rotation=actor.get_actor_rotation();assert abs(rotation.pitch)<.01 and abs(rotation.yaw+90)<.01
assert not missing,missing
(OUT/'MapAudit.json').write_text(json.dumps({'same_map':world.get_path_name(),'room_cm':[1000,1200],'inner_door':str(inner.get_world_location()),'outer_door':str(door.get_world_location()),'own_actor_count':len(own),'new_assets':[],'missing':missing,'geometry_materials':meshes,'healer_gameplay_settings_preserved':True},indent=2))
unreal.log('HH_EXPANDED_AUDIT_PASSED')
