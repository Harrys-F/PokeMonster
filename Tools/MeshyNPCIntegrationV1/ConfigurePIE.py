import unreal,json
from pathlib import Path
P=Path(unreal.Paths.project_dir()).resolve()/'Art/Characters/NPCs/IntegrationV1';o=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'));values={}
for n in ['new_window_width','new_window_height','new_viewport_resolution','new_window_position','center_new_window','last_executed_play_mode_type']:
 try:values[n]=str(o.get_editor_property(n))
 except Exception:pass
(P/'PIESettingsBefore.json').write_text(json.dumps(values,indent=2))
for n,v in [('new_window_width',1280),('new_window_height',720)]:
 try:o.set_editor_property(n,v)
 except Exception:pass
unreal.SystemLibrary.execute_console_command(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world(),'MAP CHECK')
