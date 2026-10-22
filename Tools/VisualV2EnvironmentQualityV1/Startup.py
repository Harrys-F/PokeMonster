"""Explicit isolated test setup. Never saves an existing map or shared asset."""
import unreal,json,runpy,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2EnvironmentQualityV1';e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert R==Path('/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree')
assert not e.get_game_world()
def dirty():return {"maps":[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],"content":[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not any(dirty().values()),dirty()
source='/Game/Maps/Dev_TestMap_VisualV2';target='/Game/Maps/Dev_TestMap_VisualV2EnvironmentQualityV1'
if not unreal.EditorAssetLibrary.does_asset_exist(target):
 assert unreal.EditorLoadingAndSavingUtils.load_map(source)
 assert unreal.EditorLoadingAndSavingUtils.save_map(e.get_editor_world(),target)
assert unreal.EditorLoadingAndSavingUtils.load_map(target)
assert not any(dirty().values()),dirty()
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));before={'throttle':s.get_editor_property('bThrottleCPUWhenNotForeground')};s.set_editor_property('bThrottleCPUWhenNotForeground',False)
(O/'Startup.json').write_text(json.dumps({'project':str(R),'source':source,'target':e.get_editor_world().get_path_name(),'dirty':dirty(),'editor_settings_before':before},indent=2))
last=0;busy=False
if hasattr(unreal,'_visualenv_queue'):unreal.unregister_slate_post_tick_callback(unreal._visualenv_queue)
def poll(dt):
 global last,busy
 f=O/'Job.json'
 if busy or not f.exists():return
 j=json.loads(f.read_text())
 if j['id']==last:return
 last=j['id'];busy=True
 try:
  p=(R/j['path']).resolve();assert p.is_relative_to(R/'Tools/VisualV2EnvironmentQualityV1');runpy.run_path(str(p),run_name='__main__');a={'id':last,'ok':True}
 except Exception:a={'id':last,'ok':False,'error':traceback.format_exc()};unreal.log_error(a['error'])
 finally:busy=False
 (O/'Ack.json').write_text(json.dumps(a,indent=2))
unreal._visualenv_queue=unreal.register_slate_post_tick_callback(poll)
unreal.log('VISUAL_ENV_READY')
