"""All original scene actors/settings unchanged after runtime-only tests and map checks."""
import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_editor_world();assert not E.get_game_world()and W.get_name()=='Dev_TestMap_VisualV2';sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
before=json.loads((D/'OriginalScene.json').read_text());after=scene(W);assert after==before,'Unexpected editor scene modification';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();(D/'SceneUnchanged.json').write_text(json.dumps({'passed':True,'actors':len(before['actors']),'complete_editor_inventory_unchanged':True,'no_dirty_packages':True},indent=2))
