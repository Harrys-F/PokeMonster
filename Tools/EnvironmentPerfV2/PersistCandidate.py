import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/EnvironmentPerfV2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();w=e.get_editor_world();assert w.get_name()=='Dev_TestMap_EnvironmentPerfV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterEnvironmentRenderProfileV2)
a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_class(unreal.PokeMonsterEnvironmentRenderProfileV2,unreal.Vector());a.set_actor_label('EnvironmentPerfV2_RenderOnly');chosen=json.loads((O/'SelectedCandidate.json').read_text());a.set_editor_property('renderer_overrides',chosen['renderer_overrides']);assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(O/'PersistedCandidate.json').write_text(json.dumps({'map':w.get_path_name(),'profile':a.get_path_name(),'overrides':chosen['renderer_overrides'],'baseline_saved':False,'vegetation_materials_geometry_changed':False},indent=2))
