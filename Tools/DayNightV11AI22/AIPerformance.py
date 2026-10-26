"""Short, optional native component CPU sample in actual PIE. No GPU benchmark.
1/3/8 existing wild instances, V2.1/V2.2 rhythm mode, identical initial transforms.
Does not persist any actor transform or profile; restart PIE after this technical test.
"""
import unreal,json,time,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/DayNightV11AI22';label=json.loads((D/'ReviewRequest.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_Rhythm'+label)
actors=list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor));subjects=[a for a in actors if a.overworld_movement.activities_enabled];assert len(subjects)==8
C=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterWorldClock)if x.get_outer()==GI);E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI);Config=unreal.get_default_object(unreal.load_class(None,'/Script/PokeMonster.PokeMonsterCreatureRhythmSettings'));original_enabled=Config.get_editor_property('bEnableRhythms');encounter_profiles=[(a,a.get_editor_property('profile'))for a in actors]
for a,p in encounter_profiles:a.set_editor_property('profile',None)
unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock reset')
orig={a.get_name():a.get_actor_transform()for a in actors};profiles={a.get_name():a.overworld_movement.activities for a in subjects};cases=[(n,new,False)for n in [1,3,8]for new in [False,True]]+[(8,True,True)];s={'i':-1,'time':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic(),'deltas':[]};rows=[]
def setup():
 s['i']+=1
 if s['i']==len(cases):finish();return
 n,new,far=cases[s['i']];Config.set_editor_property('bEnableRhythms',new);unreal.SystemLibrary.execute_console_command(W,'pm.WorldClock set 1 9 0')
 for a in actors:
  m=a.overworld_movement;m.set_movement_paused(True);a.set_actor_transform(orig[a.get_name()],False,True)
  body=a.get_component_by_class(unreal.CapsuleComponent)
  if a in subjects:
   cfg=profiles[a.get_name()];m.set_editor_property('override_activities',True);m.set_editor_property('activity_override',cfg)
  m.configure(a.visual_species,body.get_scaled_capsule_half_height(),body.get_scaled_capsule_radius(),body.get_scaled_capsule_half_height(),None,3817+actors.index(a));m.set_editor_property('measure_activity_cost',False);m.set_movement_paused(True)
 P.set_actor_location(unreal.Vector(-4500,-3500,50.15)if far else unreal.Vector(0,0,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
 for a in subjects[:n]:
  m=a.overworld_movement;m.set_editor_property('measure_activity_cost',True);m.set_movement_paused(False)
 s.update(time=0.,deltas=[],base_us=sum(a.overworld_movement.tick_work_microseconds for a in subjects[:n]),base_ticks=sum(a.overworld_movement.measured_ticks for a in subjects[:n]))
 (O/'Progress.json').write_text(json.dumps({'count':n,'rhythms':new,'far':far}))
def finish(error=None):
 Config.set_editor_property('bEnableRhythms',original_enabled)
 for a,p in encounter_profiles:a.set_editor_property('profile',p)
 for a in actors:a.overworld_movement.set_editor_property('measure_activity_cost',False)
 unreal.unregister_slate_post_tick_callback(unreal._pokemon_ai_perf);(O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'cases':rows,'method':'native per-component wall-clock CPU scope inside real game Tick; development measurement flag; no GPU profiling','seconds_per_case':8,'lighting':'same V1.1 enabled for both; actual 1x clock','synthetic_count':0},indent=2));unreal.log('POKEMON_AI_PERF_DONE '+str(error))
 for n in ['W','P','PC','GI','S','C','E','actors','subjects','profiles','encounter_profiles','a','p']:globals().pop(n,None)
def tick(dt):
 try:
  assert not E.is_encounter_active()and not C.is_clock_paused(),'Unexpected paused/battle benchmark'
  now=unreal.GameplayStatics.get_time_seconds(W);delta=now-s['last'];s['last']=now;s['time']+=delta
  assert time.monotonic()-s['wall']<250
  if s['i']<0:setup();return
  if delta>0:s['deltas'].append(delta)
  if s['time']>=8:
   n,new,far=cases[s['i']];ms=[a.overworld_movement for a in subjects[:n]];frames=max(1,len(s['deltas']));rows.append({'count':n,'rhythms':new,'far':far,'component_cpu_ms_per_frame_sum':(sum(m.tick_work_microseconds for m in ms)-s['base_us'])/frames/1000,'mean_frame_ms':sum(s['deltas'])/frames*1000,'measured_ticks':sum(m.measured_ticks for m in ms)-s['base_ticks'],'decisions':sum(m.activity_decisions for m in ms),'peer_queries':sum(m.peer_queries for m in ms),'traces':sum(m.perception_traces for m in ms),'distant_count':sum(m.activity_distant for m in ms),'plans':sum(m.successful_plans for m in ms),'rhythm_refreshes':sum(m.rhythm_refreshes for m in ms),'enabled_count':sum(m.rhythm_enabled for m in ms)});setup()
 except Exception as e:finish(str(e));raise
unreal._pokemon_ai_perf=unreal.register_slate_post_tick_callback(tick)
