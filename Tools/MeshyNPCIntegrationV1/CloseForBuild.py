import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir()).resolve()/'Art/Characters/NPCs/IntegrationV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world()
x={'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]};(P/'BeforeBuild.json').write_text(json.dumps(x,indent=2))
assert not x['dirty_maps'], 'Do not discard map changes'
for package in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages():
 assert package.get_path_name().startswith('/Game/Characters/NPCs/'), 'Foreign dirty package'
 assert unreal.EditorLoadingAndSavingUtils.save_packages([package],False)
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
if hasattr(unreal,'_npcintegration_queue'):
 unreal.unregister_slate_post_tick_callback(unreal._npcintegration_queue);del unreal._npcintegration_queue
unreal.SystemLibrary.quit_editor()
