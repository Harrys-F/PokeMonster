"""Read baseline without saving, require the existing test map to match apart from AA."""
import unreal,json,runpy,copy
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2VegetationPerfV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
scene=runpy.run_path(str(R/'Tools/VisualV2QualityV2/AuditScene.py'))['scene'];test=scene(e.get_editor_world());assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');central=scene(e.get_editor_world());(O/'CentralScene.json').write_text(json.dumps(central,indent=2));diff=[]
for name in sorted(set(test['actors'])|set(central['actors'])):
 a=test['actors'].get(name);b=central['actors'].get(name)
 if a!=b:diff.append({'actor':name,'test':a,'central':b})
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1');assert scene(e.get_editor_world())==test
(O/'MapComparison.json').write_text(json.dumps({'differences':diff,'test_actors':len(test['actors']),'central_actors':len(central['actors']),'world_settings_equal':test['world_settings']==central['world_settings']},indent=2))
