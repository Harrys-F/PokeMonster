"""Guarded in-project editor queue; no map creation, automatic saving or external server."""
import unreal,json,time,traceback,runpy,os,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(unreal.Paths.project_dir()).resolve();assert R==Path('/Users/harry/Developer/PokeMonster');S=R/'Saved/ProjectRefinement';E=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
def dirty():return {'maps':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'content':[x.get_path_name() for x in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
assert not E.get_game_world() and not any(dirty().values()),dirty()
assert unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/Dev_TestMap_VisualV2')
last=json.loads((S/'Job.json').read_text())['id'] if (S/'Job.json').exists() else 0;busy=False
def poll(dt):
 global last,busy
 p=S/'Job.json'
 if busy or not p.exists():return
 j=json.loads(p.read_text())
 if j['id']==last:return
 last=j['id'];busy=True
 try:
  if j['action']=='script':
   q=(R/j['path']).resolve();assert q.is_relative_to(R/'Tools') or q.is_relative_to(S);runpy.run_path(str(q),run_name='__main__')
  elif j['action']=='start_pie':
   assert not E.get_game_world() and not any(dirty().values()),dirty();unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
  elif j['action']=='stop_pie':unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_end_play()
  elif j['action']=='close':
   assert not E.get_game_world() and not any(dirty().values()),dirty();unreal.SystemLibrary.quit_editor()
  else:raise ValueError(j['action'])
  a={'id':last,'ok':True}
 except Exception:a={'id':last,'ok':False,'error':traceback.format_exc()};unreal.log_error(a['error'])
 finally:busy=False
 (S/'Ack.json').write_text(json.dumps(a,indent=2))
unreal._refine_queue=unreal.register_slate_post_tick_callback(poll)
(S/'Ready.json').write_text(json.dumps({'pid':os.getpid(),'time':time.time(),'dirty':dirty()}))
