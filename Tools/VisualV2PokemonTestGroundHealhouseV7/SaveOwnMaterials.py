import unreal
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
 assert p.get_path_name().startswith('/Game/Environment/VisualV2InteriorV7/Materials/'),p
 assert unreal.EditorAssetLibrary.save_asset(p.get_path_name(),False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
