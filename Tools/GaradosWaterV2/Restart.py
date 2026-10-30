"""Fresh native load of the exact isolated evolved team; no fixture creation or save write."""
import unreal,time,json,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GaradosWaterV2';q=json.loads((D/'Active.json').read_text());O=D/q['label'];s={'start':time.monotonic(),'loaded':False,'done':False,'phase':'load'};r={'checks':[]};W=PC=S=E=C=None
assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(O/'UserData')
def finish(error=None):
 if s['done']:return
 s['done']=True;r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(O/'Result.json').write_text(json.dumps(r,indent=2));unreal.unregister_slate_post_tick_callback(unreal._garados_restart)
 if W:unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
def tick(dt):
 global W,PC,S,E,C
 try:
  now=time.monotonic();assert now-s['start']<90
  if not s['loaded']:
   if now-s['start']<12:return
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_TestMap_VisualV2'and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
   def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
   S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);C=sub(unreal.PokeMonsterWorldClock);assert S.load_game();s.update(loaded=True,at=now);return
  if S.is_load_in_progress()or now-s['at']<5:return
  expected_world={'other':'Dev_TestMap','return':'Dev_TestMap_VisualV2'}.get(s['phase'])
  if expected_world:
   worlds=[w for w in unreal.ObjectIterator(unreal.World)if w.get_name()==expected_world and unreal.GameplayStatics.get_player_pawn(w,0)]
   if not worlds:return
   W=worlds[0];PC=unreal.GameplayStatics.get_player_controller(W,0)
  expected=json.loads(Path(q['expected']).read_text());p=list(E.get_player_party());assert[x.export_text()for x in p]==expected['party'];assert str(p[0].species.get_internal_id())=='Garados';r['checks'].append('Fresh process restores exact evolved/captured party including identities, experience, HP, AP, repertoire and order')
  B=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==W);v=B.get_visual();assert v and v.mesh.get_skeletal_mesh_asset()==p[0].species.get_visuals().presentation.mesh and not v.using_swim_mesh;r['checks'].append('Active Garados land companion restores original model and skeleton')
  if s['phase']=='load':
   r['checks'].append('Opening existing Dev_TestMap without saving maps or user storage');s.update(phase='other',at=now);unreal.GameplayStatics.open_level(W,unreal.Name('/Game/Maps/Dev_TestMap'));return
  if s['phase']=='other':
   r['checks'].append('Exact evolved team and original Garados buddy survive actual map change');s.update(phase='return',at=now);unreal.GameplayStatics.open_level(W,unreal.Name('/Game/Maps/Dev_TestMap_VisualV2'));return
  r['checks'].append('Return to VisualV2 preserves evolved team and buddy')
  r['rendering']={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.ScreenPercentage','r.TemporalAA.Upsampling','r.Shadow.Virtual.Enable','r.Shadow.Virtual.SMRT.RayCountDirectional']};assert list(r['rendering'].values())==[0.,0.,75.,1.,1.,4.];assert C.get_real_minutes_per_day()==120;r['checks'].append('Fresh standard C remains Software-Lumen/IFG TAAU75 VSM4 and 120-minute world clock');finish()
 except Exception:finish(traceback.format_exc())
unreal._garados_restart=unreal.register_slate_post_tick_callback(tick)
