import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P=R/'Art/Characters/NPCs/Ranger/Review/V2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=e.get_editor_world();assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
if w.get_path_name()!='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2':
 unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2');w=e.get_editor_world()
assert w.get_path_name()=='/Game/Maps/Dev_TestMap_VisualV2.Dev_TestMap_VisualV2';assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old={'throttle':settings.get_editor_property('bThrottleCPUWhenNotForeground'),'cvars':{}}
for n,val in [('r.Editor.Viewport.OverridePIEScreenPercentage',0),('r.SecondaryScreenPercentage.GameViewport',100)]:
 old['cvars'][n]=unreal.SystemLibrary.get_console_variable_float_value(n);unreal.SystemLibrary.execute_console_command(w,n+' '+str(val))
settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
if not (P/'EditorSettingsBefore.json').exists():(P/'EditorSettingsBefore.json').write_text(json.dumps(old,indent=2))
exec((R/'Tools/PerformanceRangerV2/Queue.py').read_text())
