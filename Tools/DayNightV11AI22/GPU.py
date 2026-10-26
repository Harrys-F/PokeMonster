"""Existing native profiler. V1 reference or threshold-only ablation, live unpaused 1x clock."""
import unreal,json,time,traceback,gc
from pathlib import Path
gc.collect();R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV11AI22';q=json.loads((D/'Request.json').read_text());O=D/q['label'];O.mkdir(exist_ok=False);W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
L=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDayNightSubsystem)if x.get_outer()==W);C=sub(unreal.PokeMonsterWorldClock);E=sub(unreal.PokeMonsterEncounterSubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);assert not E.is_encounter_active();assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_'+q['label'])
profiles=[(a,a.get_editor_property('profile'))for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)]
for a,p in profiles:a.set_editor_property('profile',None)
Config=unreal.get_default_object(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterDayNightSettings'));has_threshold=hasattr(Config,'get_editor_property')
try:original=Config.get_editor_property('RotationThresholdDegrees')
except Exception:has_threshold=False;original=None
cases=q.get('cases',[{'name':'V1Moving','threshold':None,'paused':False}]);r={'cases':[]};s={'i':0,'start':True,'wall':time.monotonic()}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._lighting11gpu)
 for a,p in profiles:a.set_editor_property('profile',p)
 if has_threshold:Config.set_editor_property('RotationThresholdDegrees',original)
 r.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(r,indent=2))
 for n in ['W','GI','PC','C','E','S','L','profiles','a','p']:globals().pop(n,None)
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<600
  if s['i']==len(cases):finish();return
  case=cases[s['i']];label='VGB1_'+q['label']+'_'+case['name']
  if s['start']:
   if case['threshold']is not None:assert has_threshold;Config.set_editor_property('RotationThresholdDegrees',case['threshold'])
   cmd('pm.WorldClock pause');cmd('pm.WorldClock set 1 12 0');cmd('pm.WorldClock speed 1')
   if not case['paused']:cmd('pm.WorldClock resume')
   plan=O/(case['name']+'.tsv');rows=[label+'\tPIE\t3\t5']
   for rep in [1,2,3]:
    for site in ['Dorf','Wald']:rows.append(site+'\tControl\t'+str(rep)+'\t2560\t1440\t2\t100')
   plan.write_text('\n'.join(rows)+'\n');s['counts']=[L.get_editor_property(n)for n in ['LightingEvaluations','RotationApplications']]if has_threshold else None;s.update(start=False,time=time.monotonic(),before=C.get_time().seconds_of_day);cmd('pm.EnvPerf2.Run '+str(plan));return
  assert not E.is_encounter_active()and C.is_clock_paused()==case['paused'],'Unexpected pause/battle'
  done=R/'Saved/EnvironmentPerfV2'/(label+'_Done.txt')
  if not done.exists():return
  assert done.read_text()=='Complete'
  if not case['paused']:assert C.get_time().seconds_of_day>s['before']+300
  r['cases'].append({'label':label,**case,'clock_before':s['before'],'clock_after':C.get_time().seconds_of_day,'elapsed':time.monotonic()-s['time'],'counter_before':s['counts'],'counter_after':[L.get_editor_property(n)for n in ['LightingEvaluations','RotationApplications']]if has_threshold else None});s.update(i=s['i']+1,start=True);(O/'Progress.json').write_text(json.dumps(r['cases'][-1]))
 except Exception:finish(traceback.format_exc())
unreal._lighting11gpu=unreal.register_slate_post_tick_callback(tick)
