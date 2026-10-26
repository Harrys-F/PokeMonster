"""Exact existing editor scene and original-file verification; no map saves."""
import unreal,json,sys,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/SaveSystemV2';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
assert scene(E.get_editor_world())==json.loads((D/'OriginalScene.json').read_text())
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
(D/'SceneUnchanged_A.json').write_text(json.dumps({'passed':True,'editor_scene_unchanged':True,'no_dirty_packages':True},indent=2))
