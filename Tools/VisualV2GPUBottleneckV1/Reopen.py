"""Open only the slim VisualV2; establish a guarded editor job queue without saving."""
import json,runpy,traceback
from pathlib import Path
import unreal
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/VisualV2GPUBottleneckV1'
O.mkdir(parents=True,exist_ok=True)
assert R==Path('/Users/harry/Documents/Codex/PokeMonster_GitSicherung_V5_2026-10-16/Worktree')
e=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
def dirty():return {'maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not e.get_game_world() and not any(dirty().values()),dirty()
# A fresh checkout has no local review evidence: establish a new read-only source signature.
if not (O/'SourceScene.json').exists():
 import sys
 sys.path.insert(0,str(R/'Tools/VisualV2QualityV2'))
 from AuditScene import scene
 assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2')
 (O/'SourceScene.json').write_text(json.dumps(scene(e.get_editor_world()),indent=2))
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2GPUBottleneckV1')
w=e.get_editor_world();pp=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PostProcessVolume):
 s=a.get_editor_property('settings');pp.append({'name':a.get_name(),'label':a.get_actor_label(),'unbound':a.get_editor_property('unbound'),'priority':a.get_editor_property('priority'),'blend_weight':a.get_editor_property('blend_weight'),'blend_radius':a.get_editor_property('blend_radius'),'location':a.get_actor_location().to_tuple(),'bounds':[v.to_tuple() for v in a.get_actor_bounds(False)],'motion_blur_amount':s.motion_blur_amount,'override_motion_blur_amount':s.override_motion_blur_amount,'bloom_intensity':s.bloom_intensity,'override_bloom_intensity':s.override_bloom_intensity,'settings_text':s.export_text()})
(O/'InitialMap.json').write_text(json.dumps({'project':str(R),'world':w.get_path_name(),'dirty':dirty(),'volumes':pp},indent=2))
s=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));(O/'EditorSettingsBefore.json').write_text(json.dumps({'throttle':s.get_editor_property('bThrottleCPUWhenNotForeground')}));s.set_editor_property('bThrottleCPUWhenNotForeground',False)
last=json.loads((O/'Job.json').read_text())['id'] if (O/'Job.json').exists() else 0;busy=False
if hasattr(unreal,'_visualenv_queue'):unreal.unregister_slate_post_tick_callback(unreal._visualenv_queue)
def poll(dt):
 global last,busy
 f=O/'Job.json'
 if busy or not f.exists():return
 j=json.loads(f.read_text())
 if j['id']==last:return
 last=j['id'];busy=True
 try:
  p=(R/j['path']).resolve();assert p.is_relative_to(R/'Tools/VisualV2GPUBottleneckV1');runpy.run_path(str(p),run_name='__main__');a={'id':last,'ok':True}
 except Exception:a={'id':last,'ok':False,'error':traceback.format_exc()};unreal.log_error(a['error'])
 finally:busy=False
 (O/'Ack.json').write_text(json.dumps(a,indent=2))
unreal._visualenv_queue=unreal.register_slate_post_tick_callback(poll)
unreal.log('VGB1_READY')
