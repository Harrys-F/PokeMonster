import unreal,json,time,os
from pathlib import Path
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages();D=Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/VisualV2StabilityV1';(D/'Idle.json').write_text(json.dumps({'pid':os.getpid(),'wall':time.time(),'editor_responding':True,'no_game_world':True,'dirty':[]}))
