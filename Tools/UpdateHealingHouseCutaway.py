"""Apply only the doorway geometry and dither mask to the existing V1 test house.

Run with UnrealEditor-Cmd PokeMonster.uproject -run=pythonscript -script=<this file>.
Never rebuilds the map, changes collision, or writes Dev_TestMap.
"""
import json
from pathlib import Path
import unreal

MAP = '/Game/Maps/Dev_HealingHouseTestMap'
MATERIAL_ROOT = '/Game/Environment/HealingHouse/Materials'
NAMES = ('Plaster', 'Wood', 'Timber', 'Stone', 'Roof', 'Metal', 'Glass')
world = unreal.EditorLoadingAndSavingUtils.load_map(MAP)
if not world:
    raise RuntimeError('Existing healing-house map is required')
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
cutaways = [a for a in actors.get_all_level_actors()
            if a.get_class().get_name() == 'PokeMonsterBuildingCutaway']
if len(cutaways) != 1:
    raise RuntimeError('Expected exactly one existing house cutaway')
cutaway = cutaways[0]
threshold = cutaway.get_editor_property('door_threshold')
if not threshold:
    raise RuntimeError('Restart with the compiled doorway component before applying')

# Record all real blockers and actor placements; the visual patch must preserve them.
def world_signature():
    return {a.get_path_name(): {
        'location': [a.get_actor_location().x, a.get_actor_location().y, a.get_actor_location().z],
        'rotation': [a.get_actor_rotation().pitch, a.get_actor_rotation().yaw, a.get_actor_rotation().roll],
        'scale': [a.get_actor_scale3d().x, a.get_actor_scale3d().y, a.get_actor_scale3d().z],
        'collision': [(c.get_name(), str(c.get_collision_enabled()),
                       str(c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)),
                       str(c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)))
                      for c in a.get_components_by_class(unreal.PrimitiveComponent)]}
        for a in actors.get_all_level_actors() if a != cutaway}

before = world_signature()
occluders = list(cutaway.get_editor_property('occluding_actors'))
function = unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/DitherTemporalAA')
if not function:
    raise RuntimeError('Engine dither function is unavailable')
report = {'map': MAP, 'materials': [], 'collision_and_placements_unchanged': False}
library = unreal.MaterialEditingLibrary
for name in NAMES:
    material = unreal.load_asset(MATERIAL_ROOT + '/M_HH_' + name)
    if not isinstance(material, unreal.Material):
        raise RuntimeError('Missing original house material: ' + name)
    if 'HouseCutaway' not in [str(p) for p in library.get_scalar_parameter_names(material)]:
        fade = library.create_material_expression(material, unreal.MaterialExpressionScalarParameter, -600, 420)
        fade.set_editor_property('parameter_name', 'HouseCutaway')
        fade.set_editor_property('default_value', 0.0)
        fade.set_editor_property('use_custom_primitive_data', True)
        fade.set_editor_property('primitive_data_index', 0)
        visible = library.create_material_expression(material, unreal.MaterialExpressionOneMinus, -360, 420)
        dither = library.create_material_expression(material, unreal.MaterialExpressionMaterialFunctionCall, -140, 420)
        dither.set_editor_property('material_function', function)
        names = library.get_material_expression_input_names(dither)
        alpha = next((str(n) for n in names if 'alpha' in str(n).lower()), None)
        if not alpha:
            raise RuntimeError('Dither function did not expose its alpha input: ' + str(names))
        inverse_inputs = library.get_material_expression_input_names(visible)
        if not inverse_inputs or not library.connect_material_expressions(fade, '', visible, str(inverse_inputs[0])):
            raise RuntimeError('Could not connect fade inversion')
        if not library.connect_material_expressions(visible, '', dither, alpha):
            raise RuntimeError('Could not connect dither alpha')
        if not library.connect_material_property(dither, '', unreal.MaterialProperty.MP_OPACITY_MASK):
            raise RuntimeError('Could not connect opacity mask')
    material.set_editor_property('blend_mode', unreal.BlendMode.BLEND_MASKED)
    library.recompile_material(material)
    if not unreal.EditorAssetLibrary.save_loaded_asset(material):
        raise RuntimeError('Could not save ' + material.get_path_name())
    report['materials'].append(material.get_path_name())

cutaway.get_editor_property('interior_area').set_box_extent(unreal.Vector(490, 500, 250), False)
threshold.set_relative_location(unreal.Vector(-410, 0, -35), False, False)
threshold.set_box_extent(unreal.Vector(20, 120, 115), False)
cutaway.set_editor_property('fade_duration', 0.4)
cutaway.set_editor_property('threshold_hysteresis', 4.0)
after = world_signature()
if before != after or occluders != list(cutaway.get_editor_property('occluding_actors')):
    Path('/private/tmp/HealingHouseThresholdUnexpectedChanges.json').write_text(json.dumps({'before': before, 'after': after}, indent=2))
    raise RuntimeError('Patch unexpectedly changed world placements, collision or occluders')
if not unreal.EditorLoadingAndSavingUtils.save_map(world, MAP):
    raise RuntimeError('Could not save the targeted healing-house map')
report['collision_and_placements_unchanged'] = True
report['threshold_world_cm'] = str(threshold.get_world_location())
report['threshold_half_extent_cm'] = str(threshold.get_unscaled_box_extent())
Path('/private/tmp/HealingHouseThresholdAssetReport.json').write_text(json.dumps(report, indent=2))
unreal.log('Healing-house doorway/dither patch completed; no gameplay actors changed')
