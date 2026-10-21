"""Independent group roaming and directional shared-action target selection in actual PIE.
Target ranking uses an explicit close-range placement fixture after natural roaming is recorded.
"""
import unreal,json,time,math,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/WildEncountersV2/Request.json').read_text())['label'];O=R/'Saved/WildEncountersV2'/label;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w);wild=list(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));group=sorted([a for a in wild if 'Dev_Bisasam_Wild_01'in str(a.encounter_id)],key=lambda a:str(a.encounter_id));assert len(group)==3
inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');interact=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='InteractAction')
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def inject(x=0,y=0):inp.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[])
def face(a):
 d=a.get_actor_location()-p.get_actor_location();theta=math.radians(p.get_movement_basis_yaw());l=max(1,math.hypot(d.x,d.y));inject(.2*(-d.x*math.sin(theta)+d.y*math.cos(theta))/l,.2*(d.x*math.cos(theta)+d.y*math.sin(theta))/l)
def shot(name):cmd('Shot filename="'+str(O/(name+'.png'))+'"')
cmd('pm.StarterReview.Party Schiggy Bisasam Zunderlauf');cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');p.set_actor_location(unreal.Vector(-300,900,50.15),False,True)
s={'phase':'observe','seconds':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'last_sample':0.,'rows':[],'ids':[str(a.encounter_id)for a in group],'seeds':[a.seed for a in group],'initial':{str(a.encounter_id):a.get_actor_location().to_tuple()for a in group},'idle_offsets':[next(v for v in a.get_attached_actors()if isinstance(v,unreal.PokeMonsterCreatureVisualActor)).idle_phase_offset for a in group]};assert len(set(s['seeds']))==3 and len(set(s['idle_offsets']))==3
for a in group:
 m=a.overworld_movement;b=a.get_component_by_class(unreal.CapsuleComponent);cfg=unreal.PokeMonsterCreatureBehaviorProfile();cfg.temperament=unreal.PokeMonsterOverworldTemperament.CALM;m.set_editor_property('override_behavior',True);m.set_editor_property('behavior_override',cfg);m.configure(a.visual_species,b.get_scaled_capsule_half_height(),b.get_scaled_capsule_radius(),b.get_scaled_capsule_half_height(),None,a.seed)
def phase(x):s.update(phase=x,seconds=0.)
def finish(error=None):
 inject();inp.inject_input_vector_for_action(interact,unreal.Vector(0,0,0),[],[]);unreal.unregister_slate_post_tick_callback(unreal._wild_group_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);s.update(passed=error is None,error=error,save_after_sha256=__import__('hashlib').sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest());(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('WILD_GROUP_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['seconds']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<150
  if now-s['last_sample']>.25:
   s['last_sample']=now;s['rows'].append({'time':now,'phase':s['phase'],'actors':[{'id':str(a.encounter_id),'position':a.get_actor_location().to_tuple(),'goal':a.overworld_movement.current_goal.to_tuple(),'state':str(a.overworld_movement.behavior_state),'distance':a.overworld_movement.distance_travelled,'speed':a.overworld_movement.current_speed}for a in group]})
  if s['phase']=='observe':
   assert not e.is_encounter_active();inject()
   if s['seconds']>4 and not s.get('shot'):shot('IndependentGroup');s['shot']=True
   if s['seconds']>22:
    s['distances']=[a.overworld_movement.distance_travelled for a in group];assert min(s['distances'])>35,s['distances'];assert len({a.overworld_movement.current_goal.to_tuple()for a in group})==3
    for a in wild:a.overworld_movement.set_movement_paused(True)
    for a in group[:2]:a.set_actor_location(unreal.Vector(*s['initial'][str(a.encounter_id)]),False,True)
    aa,bb=group[:2];av=aa.get_actor_location();bv=bb.get_actor_location();mid=(av+bv)*.5;d=bv-av;length=max(1,math.hypot(d.x,d.y));v=unreal.Vector(d.x/length,d.y/length,0);g=None
    for side in [90,-90,60,-60,110,-110]:
     q=mid+unreal.Vector(-v.y,v.x,0)*side;q.z=0;g=aa.overworld_movement.project_walkable(q)
     if g:break
    assert g,'No safe target-selection player point';p.set_actor_location(g+unreal.Vector(0,0,50.15),False,True);s['target_fixture']='Two members restored to their own spawn positions; player point selected by actual walkability';phase('face_a')
  elif s['phase']=='face_a':
   face(group[0]);assert not e.is_encounter_active()
   if s['seconds']>.4:
    inject();target=p.find_interactable_in_range();assert target==group[0],('Target A',str(target));s['selected_a']=str(target.encounter_id);shot('SelectedMemberA');phase('face_b')
  elif s['phase']=='face_b':
   face(group[1]);assert not e.is_encounter_active()
   if s['seconds']>.4:
    inject();target=p.find_interactable_in_range();assert target==group[1],('Target B',str(target));s['selected_b']=str(target.encounter_id);shot('SelectedMemberB');s['positions_before_battle']={str(a.encounter_id):a.get_actor_location().to_tuple()for a in wild};inp.inject_input_vector_for_action(interact,unreal.Vector(1,0,0),[],[]);phase('challenge')
  elif s['phase']=='challenge':
   inp.inject_input_vector_for_action(interact,unreal.Vector(0,0,0),[],[])
   if e.is_encounter_active():phase('battle')
   else:assert s['seconds']<3,'Shared interaction did not start battle'
  elif s['phase']=='battle':
   assert e.is_encounter_active();assert comp.get_visual()and comp.get_visual().get_editor_property('hidden')
   assert all(a.get_actor_location().distance(unreal.Vector(*s['positions_before_battle'][str(a.encounter_id)]))<.01 for a in wild)
   if s['seconds']>3:s['all_other_members_paused_without_joining']=True;phase('flee')
  elif s['phase']=='flee':
   if e.is_encounter_active():
    pr=e.get_presenter();v=pr.get_view()
    if not v.busy and not v.finished:assert pr.try_select_flee();assert pr.resolve_selection()
   else:
    assert e.get_last_result().source_actor==group[1];assert e.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.FLED;assert all(a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE for a in group);phase('returned')
  elif s['phase']=='returned'and s['seconds']>2:
   assert not e.is_encounter_active();assert comp.get_visual()and not comp.get_visual().get_editor_property('hidden');assert len([v for v in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterCreatureVisualActor)if 'CreaturePartyCompanion'in[str(t)for t in v.tags]])==1;s['one_companion_restored']=True;finish()
 except Exception:finish(traceback.format_exc())
unreal._wild_group_review=unreal.register_slate_post_tick_callback(tick)
