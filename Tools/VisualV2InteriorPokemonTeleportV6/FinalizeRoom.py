import unreal
root='/Game/Environment/VisualV2InteriorV6/'
for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
 assert p.get_path_name().startswith(root),p.get_path_name()
 m=unreal.load_asset(p.get_path_name());m.set_editor_property('used_with_instanced_static_meshes',True);unreal.MaterialEditingLibrary.recompile_material(m);assert unreal.EditorAssetLibrary.save_loaded_asset(m,False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
