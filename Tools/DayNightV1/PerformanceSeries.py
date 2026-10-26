"""Existing native profiler: six requested conditions + ordinary moving-sun overhead.
Each condition: same QHD/High sites, 3 repetitions, 3s warmup + 5s native CSV sampling.
"""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV1';O=D/'PerformanceSeries02';O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0)
Cycle=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==W);Clock=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI)
P=unreal.GameplayStatics.get_player_pawn(W,0);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI)
assert not E.is_encounter_active()and not PC.is_menu_open()and not Clock.is_clock_paused();assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_DayNightPerformance02');assert not P.is_overworld_input_locked()
# Disarm ONLY encounter bindings of these transient PIE actors; roaming/animation stays live.
Profiles=[(a,a.get_editor_property('profile'))for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)]
for a,profile in Profiles:a.set_editor_property('profile',None)
cases=[('NoonB75',12,0,'B',True),('OriginalControl',12,0,'off',True),('NoonC85',12,0,'C',True),('Dawn',6,0,'B',True),('Dusk',19,0,'B',True),('Night',22,0,'B',True),('MovingNoonB75',12,0,'B',False)]
s={'i':0,'stage':'start','wall':time.monotonic(),'time':time.monotonic()};result={'cases':[],'quality':2,'qhd':[2560,1440],'samples_per_case':6,'unchanged_ai':True}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._daynight_perf)
 for a,profile in Profiles:a.set_editor_property('profile',profile)
 result.update(passed=error is None,error=error,temporary_encounter_bindings_restored=True,ai_during_measurements='existing roaming and animation active; player input not locked');(O/'Result.json').write_text(json.dumps(result,indent=2))
 for n in ['W','GI','PC','Cycle','Clock','P','E','S','Profiles','a','profile']:globals().pop(n,None)
def tick(dt):
 try:
  now=time.monotonic();assert now-s['wall']<650,'Profiler timeout'
  if s['i']==len(cases):finish();return
  name,h,m,v,paused=cases[s['i']];label='VGB1_DayNight_'+name+'02'
  if s['stage']=='start':
   cmd('pm.WorldClock pause');cmd('pm.WorldClock speed 1');cmd('pm.WorldClock set 1 '+str(h)+' '+str(m));cmd('pm.DayNight '+v)
   if v!='off':cmd('pm.DayNight on')
   if not paused:cmd('pm.WorldClock resume')
   plan=D/(label+'.tsv');assert not plan.exists();rows=[label+'\tPIE\t3\t5']
   for rep in [1,2,3]:
    for site in ['Dorf','Wald']:rows.append(site+'\tControl\t'+str(rep)+'\t2560\t1440\t2\t100')
   plan.write_text('\n'.join(rows)+'\n');cmd('pm.EnvPerf2.Run '+str(plan));s.update(stage='wait',time=now);s['before']=Clock.get_time().export_text();return
  assert not E.is_encounter_active(),'Unexpected battle invalidates timing';assert Clock.is_clock_paused()==paused,'Unexpected clock hold invalidates timing'
  done=R/'Saved/EnvironmentPerfV2'/(label+'_Done.txt')
  if not done.exists():return
  assert done.read_text()=='Complete'
  if not paused:assert Clock.get_time().seconds_of_day>43200+300,'Actual moving-sun time did not progress'
  result['cases'].append({'label':label,'condition':name,'clock_before':s['before'],'clock_after':Clock.get_time().export_text(),'paused':paused,'variant':v,'elapsed_real_seconds':now-s['time']});s.update(i=s['i']+1,stage='start');(O/'Progress.json').write_text(json.dumps(result['cases'][-1]))
 except Exception:finish(traceback.format_exc())
unreal._daynight_perf=unreal.register_slate_post_tick_callback(tick)
