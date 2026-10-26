import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV21ExperienceV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not E.get_game_world()
if hasattr(unreal,'_pokemon_ai_v21_settings'):
 v=unreal._pokemon_ai_v21_settings;s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));s.set_editor_property('bThrottleCPUWhenNotForeground',v['throttle']);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto '+str(v['auto']));del unreal._pokemon_ai_v21_settings
sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
now=scene(E.get_editor_world());assert now==json.loads((D/'OriginalScene.json').read_text()),'Scene changed'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(D/'ScenePreserved.json').write_text(json.dumps({'identical':True,'dirty_packages':[]}))
