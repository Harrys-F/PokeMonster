"""Real PIE contact/challenge -> existing battle -> distinct outcome/escape. No package/save writes.
Runtime placement and party are explicit fixtures. Movement into contact uses Enhanced Input.
"""
import unreal,json,time,math,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();req=json.loads((R/'Saved/WildEncountersV2/Request.json').read_text());O=R/'Saved/WildEncountersV2'/req['label'];assert O.exists()and not(O/'Result.json').exists();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);c=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w)
wild=list(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));a=next(x for x in wild if req['species'] in str(x.visual_species) and '_Group_'not in str(x.encounter_id));m=a.overworld_movement;body=a.get_component_by_class(unreal.CapsuleComponent);offset=body.get_scaled_capsule_half_height();ground=a.get_actor_location()-unreal.Vector(0,0,offset)
for x in wild:x.overworld_movement.set_movement_paused(True)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
T=unreal.PokeMonsterOverworldTemperament;cfg=unreal.PokeMonsterCreatureBehaviorProfile();cfg.temperament=getattr(T,req['temperament']);m.set_editor_property('override_behavior',True);m.set_editor_property('behavior_override',cfg);m.configure(a.visual_species,offset,body.get_scaled_capsule_radius(),offset,None,a.seed);m.set_movement_paused(req['temperament']=='AGGRESSIVE')
move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='MoveAction');inp=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if x.get_world()==w)
interact=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==p and x.get_name()=='InteractAction')
def inject(x,y):inp.inject_input_vector_for_action(move,unreal.Vector(x,y,0),[],[])
def cmd(x):unreal.SystemLibrary.execute_console_command(w,x,pc)
cmd('pm.StarterReview.Party '+{'Zunderlauf':'Schiggy Bisasam Zunderlauf','Schiggy':'Bisasam Zunderlauf Schiggy','Bisasam':'Zunderlauf Schiggy Bisasam'}[req['species']]);cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');cmd('r.SecondaryScreenPercentage.GameViewport 100')
if req.get('outcome')=='Captured':
 inv=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterInventorySubsystem)if x.get_outer()==gi);assert inv.add_item(unreal.load_asset('/Game/Data/Items/DA_TestCaptureItem'),30)
# Collision-free start, then actual movement into the encounter capsule. No teleport after encounter.
radius=body.get_scaled_capsule_radius()+p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_radius()
p.set_actor_location(ground+unreal.Vector(-140 if req.get('approach_side')=='west' else 140,0,p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+.15),False,True);p.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
s={'phase':'near','seconds':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[],'frames':[],'start_count':0,'last_battle':False,'last_sample':0.,'last_shot':-1.,'warning_seen':False,'radius_sum':radius,'request':req,'fixture':'Runtime party/position/profile; actual Enhanced Input movement, native animation and battle outcomes','viewport':None}
def phase(x):s.update(phase=x,seconds=0.,last_shot=-1.)
def shot(label):
 cmd('Shot filename="'+str(O/(str(len(s['frames'])).zfill(4)+'_'+label+'.png'))+'"');s['frames'].append({'time':unreal.GameplayStatics.get_time_seconds(w),'phase':s['phase'],'label':label,'wild':a.get_actor_location().to_tuple(),'player':p.get_actor_location().to_tuple(),'life':str(a.life_state),'outside':a.is_outside_player_view()})
def finish(error=None):
 inject(0,0);unreal.unregister_slate_post_tick_callback(unreal._wild_encounter_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);s.update(passed=error is None,error=error,elapsed_wall=time.monotonic()-s['wall'],save_after_sha256=__import__('hashlib').sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest());(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('WILD_ENCOUNTER_V2_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);delta=now-s['last'];s['last']=now;s['seconds']+=delta;assert time.monotonic()-s['wall']<210,'Runtime review timeout'
  battle=e.is_encounter_active()
  if battle and not s['last_battle']:s['start_count']+=1
  s['last_battle']=battle
  if now-s['last_sample']>.15:
   s['last_sample']=now;s['rows'].append({'time':now,'phase':s['phase'],'life':str(a.life_state),'state':str(m.behavior_state),'wild':a.get_actor_location().to_tuple(),'player':p.get_actor_location().to_tuple(),'speed':m.current_speed,'plans':m.successful_plans,'blocked':m.blocked_steps,'encounter':battle,'touch':a.is_touching_player(p),'outside':a.is_outside_player_view(),'hidden':a.get_editor_property('hidden'),'cooldown':m.cooldown_remaining,'companion_hidden':c.get_visual().get_editor_property('hidden') if c.get_visual() else None})
  if s['phase']=='near':
   assert not battle,'Proximity incorrectly started battle';s['warning_seen']|=m.behavior_state==unreal.PokeMonsterOverworldState.WARNING
   if s['seconds']>1 and not s.get('initial_shot'):shot('Proximity_NoBattle');s['initial_shot']=True
   if s['seconds']>4:
    s['no_proximity_battle']=True;s['viewport']=list(pc.get_viewport_size());assert s['viewport']==[2560,1440];m.set_movement_paused(True);phase('contact')
  elif s['phase']=='contact':
   if not battle and s['seconds']-s['last_shot']>.2 and s.get('contact_shots',0)<8:shot('Approach_Contact');s['last_shot']=s['seconds'];s['contact_shots']=s.get('contact_shots',0)+1
   # Approach the current wild position along world XY using the actual camera-relative action.
   d=a.get_actor_location()-p.get_actor_location();length=math.hypot(d.x,d.y);theta=math.radians(p.get_movement_basis_yaw())
   if not battle and not a.is_touching_player(p):inject((-d.x*math.sin(theta)+d.y*math.cos(theta))/max(length,1), (d.x*math.cos(theta)+d.y*math.sin(theta))/max(length,1))
   else:inject(0,0)
   if battle:
    assert req['temperament'] in ['TERRITORIAL','AGGRESSIVE'],'Peaceful contact auto-started';s['contact_started']=True;phase('battle');return
   if a.is_touching_player(p) and s['seconds']>1:
    if req['temperament'] in ['TERRITORIAL','AGGRESSIVE']:assert s['seconds']<5,'Actual contact did not start';return
    s['contact_did_not_start']=True;shot('Peaceful_Contact_NoBattle');phase('challenge');return
   assert s['seconds']<14,('Could not reach contact',length,d.to_tuple())
  elif s['phase']=='challenge':
   inject(0,0);assert not battle
   if s['seconds']<.5:return
   target=p.find_interactable_in_range();s['selected_target']=target.get_name()if target else None;s['expected_target']=a.get_name();assert target==a,('Wrong directed target',s['selected_target'],s['expected_target'])
   if req.get('outcome')=='Captured':
    own,reserve,target_creature=e.get_player_party();target_creature.current_hp=1
    data=unreal.PokeMonsterEncounterStartData(presentation_mode=unreal.PokeMonsterBattlePresentationMode.CLASSIC_BATTLE,encounter_id=a.encounter_id,kind=unreal.PokeMonsterEncounterKind.WILD,source=unreal.PokeMonsterEncounterSource.VISIBLE_CREATURE,player_team=[own,reserve],opponent_team=[target_creature],random_seed=51,allow_flee=True,source_actor=a)
    s['capture_runtime_fixture']='One-HP opponent, seed 51; same source actor and existing battle/capture flow';assert e.start_encounter(data,p);phase('battle')
   else:inp.inject_input_vector_for_action(interact,unreal.Vector(1,0,0),[],[]);phase('challenge_input')
  elif s['phase']=='challenge_input':
   inp.inject_input_vector_for_action(interact,unreal.Vector(0,0,0),[],[])
   if battle:s['shared_interaction_action_verified']=True;phase('battle')
   else:assert s['seconds']<3,'Shared interaction action failed'
  elif s['phase']=='battle':
   inject(0,0)
   if not battle:
    s['outcome']=str(e.get_last_result().outcome);assert s['start_count']==1;phase('after');return
   assert p.is_overworld_input_locked();assert not c.get_visual() or c.get_visual().get_editor_property('hidden');pr=e.get_presenter();v=pr.get_view()
   if not s.get('battle_shot') and s['seconds']>1:cmd('pm.CreatureReview.CaptureLiveUI Wild_'+req['label']);s['battle_shot']=True
   if not v.busy and not v.finished:
    if v.must_switch:assert pr.try_select_switch(next(i for i,x in enumerate(v.player_team)if x.can_switch))
    elif req.get('outcome')=='Fled':assert pr.try_select_flee()
    elif req.get('outcome')=='Captured':assert pr.try_select_capture()
    else:
     names=[str(x.name)for x in v.moves];preferred={'Zunderlauf':'Aquaknarre','Schiggy':'Rankenhieb','Bisasam':'Glut'}[req['species']];i=names.index(preferred)if preferred in names else 0;assert pr.try_select_move(i)
    assert pr.resolve_selection()
   assert s['seconds']<100,'Battle did not finish'
  elif s['phase']=='after':
   inject(0,0);assert not battle,'Repeated encounter after result';assert s['outcome'].endswith(req.get('outcome','Victory').upper()+': '+{'Victory':'0','Fled':'2','Captured':'4'}[req.get('outcome','Victory')]+'>') or req.get('outcome','Victory').upper() in s['outcome'],s['outcome']
   if req.get('outcome')=='Fled':
    assert a.life_state==unreal.PokeMonsterWildLifeState.ACTIVE and not a.get_editor_property('hidden');assert not a.can_interact(p);assert not p.try_interact()
    if s['seconds']>3:s['flee_cooldown_verified']=True;finish()
    return
   if req.get('outcome')=='Captured':
    assert a.life_state==unreal.PokeMonsterWildLifeState.REMOVED and a.get_editor_property('hidden');s['capture_removed_without_escape']=not m.escaping_defeat;finish();return
   assert not a.can_interact(p),'Defeated fleeing creature can be challenged';assert e.is_encounter_completed(a.encounter_id),'Defeat not persisted'
   if s['seconds']-s['last_shot']>.8 and len(s['frames'])<65:shot('Recovery_Escape');s['last_shot']=s['seconds']
   if a.life_state==unreal.PokeMonsterWildLifeState.REMOVED:
    assert a.is_outside_player_view(),'Visible defeated creature popped away';assert m.distance_travelled>150;s['escape_distance_cm']=m.distance_travelled;s['escape_seconds']=s['seconds'];s['completed_no_respawn']=True;finish()
   elif s['seconds']>70:
    assert a.life_state==unreal.PokeMonsterWildLifeState.WAITING_FOR_EXIT and not a.get_editor_property('hidden');s['safe_blocked_fallback']=True;finish('Safe fallback reached but visible escape acceptance is still open')
 except Exception:finish(traceback.format_exc())
unreal._wild_encounter_review=unreal.register_slate_post_tick_callback(tick)
