"""Fresh application reloads only this task's previous native test save."""
import unreal,json,time,traceback,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/WestlandVisualV2IntegrationV1';label=json.loads((D/'Request.json').read_text())['label'];O=D/label;previous=D/'NativeFeatures02';expected=json.loads((previous/'RestartExpected.json').read_text());assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(previous)
W=next(w for w in unreal.ObjectIterator(unreal.World)if w.get_name()=='Dev_WestlandRegion'and unreal.GameplayStatics.get_player_pawn(w,0));P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
def sub(cls,o=GI):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==o)
S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);C=sub(unreal.PokeMonsterWorldClock);assert S.has_save_game();PC.toggle_main_menu();assert S.load_game();start=time.monotonic();busy=False

def tick(dt):
 global busy
 if busy:return
 busy=True
 try:
  if time.monotonic()-start<2 or S.is_load_in_progress():return
  assert time.monotonic()-start<60
  assert [x.export_text()for x in E.get_player_party()]==expected['party'];assert [x.export_text()for x in sub(unreal.PokeMonsterInventorySubsystem).get_stacks()]==expected['inventory'];assert math.dist(P.get_actor_location().to_tuple(),expected['position'])<.1;assert C.get_time().export_text()==expected['clock'];assert sub(unreal.PokeMonsterCreatureCompanionSubsystem,W).get_visual();assert P.third_person_pitch==-12 and P.third_person_distance==350;assert C.get_real_minutes_per_day()==120
  vals={n:unreal.SystemLibrary.get_console_variable_float_value(n)for n in ['r.ScreenPercentage','r.Lumen.HardwareRayTracing','r.Lumen.FinalGatherMethod','r.TemporalAA.Upsampling','r.Shadow.Virtual.SMRT.RayCountDirectional']};assert list(vals.values())==[75,0,0,1,4];assert PC.close_menu();assert not P.is_overworld_input_locked();finish(dict(passed=True,checks=['Fresh application reload restores captured team, AP, inventory, clock, world position, camera and companion'],rendering=vals))
 except Exception:finish(dict(passed=False,error=traceback.format_exc()))
 finally:busy=False
def finish(r):
 (O/'Result.json').write_text(json.dumps(r,indent=2));unreal.unregister_slate_post_tick_callback(unreal._wvi_restart);unreal.SystemLibrary.quit_game(W,PC,unreal.QuitPreference.QUIT,False)
unreal._wvi_restart=unreal.register_slate_post_tick_callback(tick)
