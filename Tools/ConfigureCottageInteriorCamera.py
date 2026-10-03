"""Apply only the Cottage's occluder mapping and opt-in interior view in its test map."""
import json
from pathlib import Path
import unreal
root = Path(unreal.Paths.project_dir()).resolve()
editor = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not editor.get_game_world(), 'Stop PIE before updating the Cottage configuration.'
world = editor.get_editor_world()
assert world.get_name() == 'Dev_BuildingKitTestMap', world.get_name()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
by_label = {a.get_actor_label(): a for a in actors}
layout = json.loads((root / 'Art/Architecture/Westland/Buildings/WL_Cottage_V1.json').read_text())
cutaway = by_label['WL_Cottage_Cutaway']
assert abs(cutaway.get_editor_property('fade_duration') - .4) < 1e-6
before = [a.get_actor_label() for a in cutaway.get_editor_property('occluding_actors')]
other_buildings = [a for a in actors if a.get_class() == cutaway.get_class() and a != cutaway]
other_configs = [(a, list(a.get_editor_property('occluding_actors')), a.get_editor_property('use_interior_camera')) for a in other_buildings]
cutaway.set_editor_property('occluding_actors', [by_label[p['label']] for p in layout['placements'] if p['cutaway']])
view = layout['interior_camera']
cutaway.set_editor_property('use_interior_camera', view['enabled'])
cutaway.set_editor_property('interior_camera_distance', view['distance_cm'])
cutaway.set_editor_property('interior_camera_pitch', view['pitch_degrees'])
cutaway.set_editor_property('interior_camera_yaw_offset', view['yaw_offset_degrees'])
cutaway.set_editor_property('interior_camera_target', unreal.Vector(*view['target_local_cm']))
after = [a.get_actor_label() for a in cutaway.get_editor_property('occluding_actors')]
for actor, occluders, enabled in other_configs:
    assert list(actor.get_editor_property('occluding_actors')) == occluders
    assert actor.get_editor_property('use_interior_camera') == enabled
assert unreal.EditorLoadingAndSavingUtils.save_map(world, '/Game/Maps/Dev_BuildingKitTestMap')
out = root / 'Saved/WestlandInteriorControls'
out.mkdir(parents=True, exist_ok=True)
(out / 'MapConfiguration.json').write_text(json.dumps({'removed': sorted(set(before)-set(after)), 'added': sorted(set(after)-set(before)), 'interior_camera': view, 'other_buildings_unchanged': True}, indent=2)+'\n')
unreal.log('COTTAGE_INTERIOR_CAMERA_CONFIGURED')
