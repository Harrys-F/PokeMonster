"""Prepare instances for the existing birch mesh; no master, mesh or map edits."""
import json
from pathlib import Path
import unreal

R = Path(unreal.Paths.project_dir()).resolve()
O = R / 'Saved/TreeReveal_20261013'
O.mkdir(parents=True, exist_ok=True)
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
L = unreal.MaterialEditingLibrary
D = '/Game/Environment/DevTestMapVisualV2/Materials'
W = '/Game/Environment/WestlandAssetLibrary/Materials'
parent = unreal.load_asset(D + '/M_V2_BarkRevealBase')
assert parent
rows = []
for suffix in ['Birch', 'LeafBirch', 'LeafDark', 'LeafLight']:
    original = unreal.load_asset(W + '/MI_WLA_' + suffix)
    assert original
    root = original
    while isinstance(root, unreal.MaterialInstanceConstant):
        root = root.get_editor_property('parent')
    path = D + '/MI_V2_' + suffix + 'Reveal'
    instance = unreal.load_asset(path)
    if not instance:
        instance = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            path.rsplit('/', 1)[1], D, unreal.MaterialInstanceConstant,
            unreal.MaterialInstanceConstantFactoryNew())
    assert instance
    # The existing painted bark reveal already exposes all original paint/Tint/PBR
    # parameters. Birch leaves are opaque geometry, so no new alpha graph is needed.
    L.set_material_instance_parent(instance, parent)
    for name in L.get_texture_parameter_names(root):
        value = L.get_material_instance_texture_parameter_value(original, name)
        L.set_material_instance_texture_parameter_value(instance, name, value)
    for name in L.get_vector_parameter_names(root):
        value = L.get_material_instance_vector_parameter_value(original, name)
        L.set_material_instance_vector_parameter_value(instance, name, value)
    for name in L.get_scalar_parameter_names(root):
        value = L.get_material_instance_scalar_parameter_value(original, name)
        L.set_material_instance_scalar_parameter_value(instance, name, value)
    overrides = unreal.MaterialInstanceBasePropertyOverrides()
    overrides.set_editor_property('override_two_sided', True)
    overrides.set_editor_property('two_sided', root.get_editor_property('two_sided'))
    instance.set_editor_property('base_property_overrides', overrides)
    L.set_material_instance_scalar_parameter_value(instance, 'PlayerRevealStrength', 0.0)
    L.update_material_instance(instance)
    assert unreal.EditorAssetLibrary.save_loaded_asset(instance, False)
    rows.append({'original': original.get_path_name(), 'reveal': instance.get_path_name(),
                 'parent': parent.get_path_name(), 'two_sided': root.get_editor_property('two_sided')})
(O / 'FamilyMaterials.json').write_text(json.dumps(rows, indent=2))
