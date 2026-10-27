"""Bounded QHD High matrix using the existing native CSV profiler. No recording."""
import unreal,json,time,traceback,gc
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/VisualV2StabilityV1';q=json.loads((D/'PerformanceRequest.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
C=sub(unreal.PokeMonsterWorldClock);E=sub(unreal.PokeMonsterEncounterSubsystem);assert unreal._stability_isolated and not E.is_encounter_active()
actors=[a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.Actor)if isinstance(a,(unreal.PokeMonsterCreatureVisualActor,unreal.PokeMonsterVisibleWildCreatureActor))];flags=[]
for a in actors:
 cs=[(c,c.is_component_tick_enabled(),c.is_visible()if isinstance(c,unreal.SceneComponent)else None)for c in a.get_components_by_class(unreal.ActorComponent)];flags.append((a,a.is_actor_tick_enabled(),cs))
def population(enabled):
 for a,t,cs in flags:
  a.set_actor_tick_enabled(t if enabled else False)
  for c,t,v in cs:
   c.set_component_tick_enabled(t if enabled else False)
   if isinstance(c,unreal.SceneComponent):c.set_visibility(v if enabled else False,False)
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
cases=q['cases'];result={'cases':[],'actor_count':len(actors),'wild_count':len(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)),'without_definition':'All Pokemon actor/component ticks and SceneComponent rendering suspended transiently; no destruction or saved settings'};s={'i':0,'start':True,'wall':time.monotonic()}
def finish(error=None):
 cmd('pm.EnvPerf2.Stop');population(True);unreal.unregister_slate_post_tick_callback(unreal._stability_perf);result.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(result,indent=2))
 for n in ['W','GI','PC','C','E','actors','flags','a','cs','c']:globals().pop(n,None)
 gc.collect()
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<650
  if s['i']==len(cases):finish();return
  case=cases[s['i']];label='VGB1_'+q['label']+'_'+case['name']
  if s['start']:
   population(case.get('pokemon',True));cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 '+str(case['hour'])+' 0');cmd('pm.WorldClock speed 1');cmd('pm.WorldClock resume');plan=O/(case['name']+'.tsv');rows=[label+'\tPIE\t2\t4']
   for rep in [1,2,3]:
    for site in case.get('sites',['Wald']):rows.append(site+'\tControl\t'+str(rep)+'\t2560\t1440\t2\t100')
   plan.write_text('\n'.join(rows)+'\n');s.update(start=False,time=time.monotonic(),before=C.get_time().seconds_of_day);cmd('pm.EnvPerf2.Run '+str(plan));return
  assert not E.is_encounter_active()and not C.is_clock_paused(),'Unexpected battle/pause invalidates timing'
  done=R/'Saved/EnvironmentPerfV2'/(label+'_Done.txt')
  if not done.exists():return
  assert done.read_text()=='Complete';result['cases'].append({'label':label,**case,'clock_before':s['before'],'clock_after':C.get_time().seconds_of_day,'wall_seconds':time.monotonic()-s['time']});s.update(i=s['i']+1,start=True);(O/'Progress.json').write_text(json.dumps(result['cases'][-1]))
 except Exception:finish(traceback.format_exc())
unreal._stability_perf=unreal.register_slate_post_tick_callback(tick)
