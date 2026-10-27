"""Create only our named isolated PIE fixture through existing public functions."""
import unreal,json,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2PerformanceV1';W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and unreal._perf1_isolated;GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI)
name='PokeMonster_SaveV2_Test_PerfOptimization01';path=R/'Saved/SaveGames'/(name+'.sav');assert not path.exists();assert unreal._perf1_isolated
for cmd in ['pm.WorldClock pause','pm.WorldClock set 1 12 0']:unreal.SystemLibrary.execute_console_command(W,cmd,PC)
assert C.get_hour()==12 and C.get_minute()==0 and C.get_real_minutes_per_day()==120;assert S.save_current_game();assert path.exists();(D/'NativeFixture.json').write_text(json.dumps({'source':str(path.relative_to(R)),'slot':name,'time':C.get_time().export_text(),'existing_save_system':True,'user_slot_changed':False},indent=2));unreal.log('PERF1_NATIVE_FIXTURE_READY')
