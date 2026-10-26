"""Unforced standard-profile social observation in ordinary VisualV2 PIE.
Only the player is moved to an observer position. No creature spawn, profile or state override.
"""
import unreal,json,time,traceback,math
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV21ExperienceV1'
label=json.loads((D/'ReviewRequest.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI)
E=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI)
assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_AIV21'+label)
assert not E.is_encounter_active()
actors=[a for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor)if a.overworld_movement.activities_enabled]
assert len(actors)==8
P.set_actor_location(unreal.Vector(-100,-100,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
cmd('pm.EnvPerf2.Viewport 2560 1440')
s={'last':unreal.GameplayStatics.get_time_seconds(W),'t':0.,'sample':0.,'wall':time.monotonic(),'recording':False,'observed':False,'post':0.,'viewwait':0.}
result={'ordinary_pie':True,'profiles':'unmodified species defaults','diagnostic_player_position':[-100,-100,50.15],'creature_positions_modified':False,'samples':[]}
clip=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('AIV21'+label)
def finish(error=None):
 cmd('pm.TAAReview.CaptureStop');unreal.unregister_slate_post_tick_callback(unreal._aiv21_social)
 result.update(passed=error is None,error=error,game_seconds=s['t'],clip=str(clip))
 (O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('AIV21_SOCIAL_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);delta=now-s['last'];s['last']=now;s['t']+=delta
  assert time.monotonic()-s['wall']<500,'Wall timeout'
  assert not E.is_encounter_active(),'No diagnostic distance-based battle expected'
  if s['t']-s['sample']>.5:
   s['sample']=s['t'];rows=[]
   for a in actors:
    m=a.overworld_movement;peer=m.social_partner
    if peer:assert peer.social_partner==m,'Nonreciprocal reservation'
    rows.append({'name':a.get_name(),'species':str(a.visual_species.get_internal_id()),'state':str(m.behavior_state),'position':a.get_actor_location().to_tuple(),'partner':peer.get_owner().get_name()if peer else None,'travelling':m.is_activity_travelling(),'requests':m.social_requests,'declined':m.social_declined,'completed':m.social_completed,'interrupted':m.social_interrupted,'last_decision':str(m.last_social_decision),'plans':m.successful_plans,'blocked':m.blocked_steps})
   result['samples'].append({'time':s['t'],'actors':rows});(O/'Progress.json').write_text(json.dumps(result['samples'][-1],indent=2))
   pairs=[a for a in actors if a.overworld_movement.social_partner]
   if pairs and not s['recording']:
    # Observer framing only. Non-target territorial species are paused so they cannot chase
    # the observer while the six target species keep their unmodified profiles and states.
    paused=[]
    for other in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):
     m=other.overworld_movement
     if not m.activities_enabled and m.get_behavior_profile().temperament in [unreal.PokeMonsterOverworldTemperament.TERRITORIAL,unreal.PokeMonsterOverworldTemperament.AGGRESSIVE]:
      m.set_movement_paused(True);paused.append(str(other.visual_species.get_internal_id()))
    mid=(pairs[0].get_actor_location()+pairs[0].overworld_movement.social_partner.get_owner().get_actor_location())*.5
    q=unreal.Vector(mid.x-650,mid.y+650,50.15)
    P.set_actor_location(q,False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
    result['observer_framing']={'time':s['t'],'player':q.to_tuple(),'paused_non_target_species':paused}
    s['viewwait']=s['t']+2
    cmd('pm.TAAReview.CaptureStart '+str(clip));s['recording']=True
    cmd('HighResShot 2560x1440 filename="'+str(O/'SocialApproach.png')+'"')
   if any(not a.overworld_movement.is_activity_travelling()and not a.overworld_movement.social_partner.is_activity_travelling()for a in pairs)and not s['observed'] and s['t']>s['viewwait']:
    s['observed']=True;cmd('HighResShot 2560x1440 filename="'+str(O/'SocialObserve.png')+'"')
   if sum(a.overworld_movement.social_completed for a in actors)>0:
    s['post']+=.5
    if s['post']>8:
     cmd('HighResShot 2560x1440 filename="'+str(O/'SocialAfter.png')+'"');finish();return
  if s['t']>180:raise AssertionError('No spontaneous completed visit within 180 game seconds')
 except Exception:finish(traceback.format_exc());raise
unreal._aiv21_social=unreal.register_slate_post_tick_callback(tick)
