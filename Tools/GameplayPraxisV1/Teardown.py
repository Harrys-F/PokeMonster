"""Read-only result guard and restore temporary settings; PIE stop discards fixtures."""
import unreal,json,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();g=unreal._praxis_guard;s=unreal._praxis_settings;E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);W=E.get_game_world()or E.get_editor_world();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';assert hashlib.sha256(slot.read_bytes()).hexdigest()==g['sha256'],'User save changed: do not overwrite'
for k,v in s['cvars'].items():unreal.SystemLibrary.execute_console_command(W,k+' '+str(v))
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',s['throttle'])
(g['output']/'Teardown.json').write_text(json.dumps({'disk_save_unchanged':True,'temporary_settings_restored':True,'fixtures_discarded_by_normal_pie_stop':True},indent=2))
