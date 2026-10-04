"""Refine only the existing Healing House occluder list; never rebuild actors.

Run with PIE stopped in Dev_HealingHouseTestMap. The explicit legacy side
entries are retained as actors, with their existing visibility and collision.
Evidence goes to ignored Saved/HealingCutaway; only the map is saved.
"""
import json
from pathlib import Path
import unreal

LEGACY_SIDE_OCCLUDERS = frozenset({
    'CameraSideWall',
    'HH_Walls_CameraSide', 'HH_Timber_CameraSide',
    'HH_WindowFrames_CameraSide', 'HH_Glass_CameraSide',
    'HH_V2_Walls_CameraSide', 'HH_V2_Glass_CameraSide',
    'HH_V2_Windows_CameraSide', 'HH_V2_Timber_CameraSide',
    'HH_V2_Stone_CameraSide', 'HH_V2_InteriorBeams_CameraSide',
})
EXPANDED_FRONT_OCCLUDERS = frozenset({
    'HH_Expanded_FrontWall_-1', 'HH_Expanded_FrontWall_1',
    'HH_Expanded_DoorPost_-1', 'HH_Expanded_DoorPost_1',
    'HH_Expanded_DoorLintel', 'HH_Expanded_DoorBeam',
})


def without_legacy_side_occluders(actors):
    """Keep order and references; exclude only these audited building parts."""
    return [a for a in actors if a.get_actor_label() not in LEGACY_SIDE_OCCLUDERS]


def configure():
    editor = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    assert not editor.get_game_world(), 'Stop PIE before configuration'
    world = editor.get_editor_world()
    assert world.get_name() == 'Dev_HealingHouseTestMap'
    actors = list(unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors())
    cut = next(a for a in actors if a.get_actor_label() == 'HouseCutaway')
    assert cut.get_editor_property('use_relocated_interior'), 'Existing expanded prototype required'
    before = list(cut.get_editor_property('occluding_actors'))
    after = without_legacy_side_occluders(before)
    labels = {a.get_actor_label() for a in after}
    assert EXPANDED_FRONT_OCCLUDERS <= labels
    assert not any(a.get_actor_label().startswith(('HH_Expanded_Side', 'HH_Expanded_Rear')) for a in after)
    # Setting the reference list does not unhide retained, obsolete V1/blockout actors.
    cut.set_editor_property('occluding_actors', after)
    assert unreal.EditorLoadingAndSavingUtils.save_map(world, '/Game/Maps/Dev_HealingHouseTestMap')
    out = Path(unreal.Paths.project_dir()).resolve() / 'Saved/HealingCutaway'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'Occluders.json').write_text(json.dumps({
        'before': [a.get_actor_label() for a in before],
        'after': [a.get_actor_label() for a in after],
        'removed': [a.get_actor_label() for a in before if a not in after],
    }, indent=2))
    unreal.log('HH_EXPANDED_CUTAWAY_CONFIGURED')


if __name__ == '__main__':
    configure()
