"""Only temporary editor preferences; preserve scene, camera and all user save slots."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV21ExperienceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world() and E.get_editor_world().get_name()=='Dev_TestMap_VisualV2'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
p=D/'OriginalScene.json'
if not p.exists():p.write_text(json.dumps(scene(E.get_editor_world()),indent=2))
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
assert not hasattr(unreal,'_pokemon_ai_v21_settings')
unreal._pokemon_ai_v21_settings={'throttle':s.get_editor_property('bThrottleCPUWhenNotForeground'),'auto':unreal.SystemLibrary.get_console_variable_int_value('pm.Evolution.Auto')}
s.set_editor_property('bThrottleCPUWhenNotForeground',False);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto 0')
