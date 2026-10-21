"""Real PIE state/path/encounter acceptance on an existing wild actor. No map/save writes."""
import unreal,json,time,math,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/OverworldAIV2/BehaviorRearmFinal';O.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);wild=list(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));a=next(x for x in wild if 'Glumanda'in x.get_actor_label()or'Zunderlauf'in str(x.visual_species));m=a.overworld_movement;body=a.get_component_by_class(unreal.CapsuleComponent);offset=body.get_scaled_capsule_half_height();origin=m.habitat_origin;original_override=m.override_behavior;original_profile=m.behavior_override
for actor in wild:
 actor.overworld_movement.set_movement_paused(True)
 for c in actor.get_components_by_class(unreal.SphereComponent):c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
a.set_editor_property('deactivate_after_victory',False)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));oldthrottle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
cmd('pm.StarterReview.Party Schiggy Bisasam Zunderlauf');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100')
T=unreal.PokeMonsterOverworldTemperament;S=unreal.PokeMonsterOverworldState;cases=[('Shy',T.SHY,350),('Curious',T.CURIOUS,400),('Calm',T.CALM,400),('Territorial',T.TERRITORIAL,140)];s={'i':0,'phase':'setup','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'frames':[],'rows':[],'last_sample':0.,'flee_attempts':0}
def place_player(d):
 for angle in range(0,360,30):
  q=origin+unreal.Vector(math.cos(math.radians(angle))*d,math.sin(math.radians(angle))*d,0);res=m.project_walkable(q)
  if res and m.can_traverse(origin,q):
   p.set_actor_location(unreal.Vector(q.x,q.y,origin.z+50.15),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();return
 raise RuntimeError('No collision-clear player fixture at '+str(d))
def phase(x):s.update(phase=x,time=0.)
def shot(label):cmd('Shot filename="'+str(O/(label+'.png'))+'"')
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._ai_behavior);settings.set_editor_property('bThrottleCPUWhenNotForeground',oldthrottle);s.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('OVERWORLD_AI_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['time']+=delta;assert time.monotonic()-s['wall']<240
  if now-s['last_sample']>.2:
   s['last_sample']=now;loc=a.get_actor_location();s['frames'].append({'time':now,'case':s['i'],'phase':s['phase'],'state':str(m.behavior_state),'npc':loc.to_tuple(),'player':p.get_actor_location().to_tuple(),'distance':loc.distance(p.get_actor_location()),'plans':m.successful_plans,'blocked':m.blocked_steps,'cooldown':m.cooldown_remaining,'encounter':e.is_encounter_active()});assert m.is_inside_habitat(loc-unreal.Vector(0,0,offset)),'Left habitat'
  if s['phase']=='setup':
   n,kind,d=cases[s['i']];a.set_actor_location(origin+unreal.Vector(0,0,offset),False,True);m.set_editor_property('override_behavior',True);cfg=unreal.PokeMonsterCreatureBehaviorProfile();cfg.temperament=kind;m.set_editor_property('behavior_override',cfg);m.configure(a.visual_species,offset,body.get_scaled_capsule_radius(),offset,None,461);place_player(d);s['start_distance']=a.get_actor_location().distance(p.get_actor_location());s['start_position']=a.get_actor_location().to_tuple();phase('observe');return
  if s['phase']=='observe':
   name=cases[s['i']][0]
   if s['time']>3 and not s.get('shot_'+name):shot(name);s['shot_'+name]=True
   if name=='Territorial' and e.is_encounter_active():s['rows'].append({'territorial_triggered':True,'warning_seconds':s['time']});phase('flee');return
   if name=='Territorial':assert s['time']<12,'Territory did not start encounter';return
   assert not e.is_encounter_active(),'Unexpected automatic encounter'
   if s['time']>14:
    distance=a.get_actor_location().distance(p.get_actor_location());gain=distance-s['start_distance'];s['rows'].append({'case':name,'distance_delta_cm':gain,'distance_travelled':m.distance_travelled,'plans':m.successful_plans,'state':str(m.behavior_state)})
    if name=='Shy':assert gain>70,'Shy failed to retreat'
    if name=='Curious':assert gain<-65,'Curious failed to approach'
    if name=='Calm':assert m.distance_travelled>50,'Calm did not wander'
    s['i']+=1;phase('setup')
  elif s['phase']=='flee':
   if not e.is_encounter_active():phase('cooldown');return
   pr=e.get_presenter();v=pr.get_view()
   if not v.busy and not v.finished:assert pr.try_select_flee();assert pr.resolve_selection();s['flee_attempts']+=1
   elif v.finished:pass
  elif s['phase']=='cooldown':
   assert not e.is_encounter_active(),'Immediate repeated territorial battle'
   if s['time']>33:
    assert m.cooldown_remaining==0,'Cooldown did not expire';s['rows'].append({'post_battle_no_repeat_after_cooldown_expired':True,'cooldown':m.cooldown_remaining});finish()
 except Exception as ex:finish(str(ex));raise
unreal._ai_behavior=unreal.register_slate_post_tick_callback(tick)
