"""Own guarded editor session. No asset save or project quality override."""
import unreal,runpy,json,sys,os
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GraphicsVariantC'
assert R==Path('/Users/harry/Developer/PokeMonster')
runpy.run_path(str(R/'Tools/ProjectMaintenance/ArtSession.py'),run_name='__main__')
E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'));from AuditScene import scene
p=D/'OriginalScene.json'
if not p.exists():p.write_text(json.dumps(scene(E.get_editor_world()),indent=2))
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
unreal._perf1_preferences={'throttle':s.get_editor_property('bThrottleCPUWhenNotForeground'),'auto':unreal.SystemLibrary.get_console_variable_int_value('pm.Evolution.Auto')}
s.set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.SystemLibrary.execute_console_command(E.get_editor_world(),'pm.Evolution.Auto 0')
(D/('Session-'+str(os.getpid())+'.json')).write_text(json.dumps({'pid':os.getpid(),'preferences':unreal._perf1_preferences}))
unreal.log('PERFORMANCE_V1_READY')
