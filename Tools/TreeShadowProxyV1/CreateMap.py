import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/TreeShadowProxyV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
source='/Game/Maps/Dev_TestMap_VisualV2';target='/Game/Maps/Dev_TestMap_TreeShadowProxyV1'
assert not unreal.EditorAssetLibrary.does_asset_exist(target)
assert unreal.EditorLoadingAndSavingUtils.load_map(source)
assert unreal.EditorLoadingAndSavingUtils.save_map(e.get_editor_world(),target)
assert unreal.EditorLoadingAndSavingUtils.load_map(target)
(O/'MapCopy.json').write_text(json.dumps({'source':source,'target':target,'method':'Editor save_map/load_map; original never saved','trees':['V2_ForestOak_0','V2_ForestOak_1','V2_ForestOak_2']},indent=2))
