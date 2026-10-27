import unreal,json,sys
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not E.get_game_world();sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
now=scene(E.get_editor_world());expected=json.loads((D/'AfterScene.json').read_text());assert now==expected,'Editor scene changed beyond final checked material assignments'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
v=unreal._stability_preferences;s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));s.set_editor_property('bThrottleCPUWhenNotForeground',v['throttle']);unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto '+str(v['auto']));unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.TAAReview.ReadbackSlots 3');(D/'SceneRestored.json').write_text(json.dumps({'passed':True,'matches_checked_final_scene':True,'dirty':[]}))
