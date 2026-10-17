import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();P=R/'Art/Characters/NPCs/Ranger/Review/V2';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not e.get_game_world();old=json.loads((P/'EditorSettingsBefore.json').read_text());w=e.get_editor_world()
for n,val in old['cvars'].items():unreal.SystemLibrary.execute_console_command(w,n+' '+str(val))
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',old['throttle']);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_set_viewport_realtime(True)
(P/'RestoredSession.json').write_text(json.dumps({'cvars':{n:unreal.SystemLibrary.get_console_variable_float_value(n) for n in old['cvars']},'throttle':old['throttle'],'editor_viewport_realtime':True,'dirty_maps':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'dirty_content':[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]},indent=2))
if hasattr(unreal,'_rv2_queue'):unreal.unregister_slate_post_tick_callback(unreal._rv2_queue);del unreal._rv2_queue
