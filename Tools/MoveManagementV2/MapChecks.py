"""Read-only existing map checks and world-site inventory; never saves a level."""
import unreal,json,re
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/MoveManagementV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world();rows=[]
for p in sorted((R/'Content/Maps').glob('*.umap')):
 assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
 name='/Game/Maps/'+p.stem;assert unreal.EditorLoadingAndSavingUtils.load_map(name)
 actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
 rows.append({'map':name,'actors':[{'label':a.get_actor_label(),'class':a.get_class().get_name(),'position':a.get_actor_location().to_tuple(),'tags':[str(t)for t in a.tags]}for a in actors]})
 unreal.log('MOVE_MANAGEMENT_V2_MAPCHECK_BEGIN '+name);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'MAP CHECK');unreal.log('MOVE_MANAGEMENT_V2_MAPCHECK_END '+name)
assert len(rows)==11
assets=unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path('/Game',recursive=True)
keywords=re.compile(r'bruchtal|rivendell|hidden.?valley|knowledge.?valley|wissenstal|gelehrten|erinnerung',re.I)
matches=[str(a.package_name)for a in assets if keywords.search(str(a.package_name))]
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2')
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(O/'WorldInventory.json').write_text(json.dumps({'maps':rows,'named_valley_asset_matches':matches,'note':'Names are evidence, not proof that an unnamed area has no art assets. No documented playable knowledge valley or access route is identified.'},indent=2))
