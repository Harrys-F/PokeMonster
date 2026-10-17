import unreal,json
from pathlib import Path
p=Path(unreal.Paths.project_dir())/'Saved/EnvironmentPerfV3/FinalEditorState.json';d=json.loads(p.read_text());assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
unreal.unregister_slate_post_tick_callback(unreal._envperf3_queue);del unreal._envperf3_queue;d['automation_queue_removed']=True;p.write_text(json.dumps(d,indent=2))
