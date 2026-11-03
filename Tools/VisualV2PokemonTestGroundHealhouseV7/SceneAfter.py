import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PokemonTestGroundHealhouseV7';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert W.get_name()=='Dev_TestMap_VisualV2';sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
(D/'SceneAfter.json').write_text(json.dumps(scene(W),indent=2));assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
