"""Unforced standard-profile social observation in ordinary VisualV2 PIE.
Two existing Bisasam are moved to a clear visual area during PIE. No spawn, profile or state override.
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
P.set_actor_location(unreal.Vector(-250,2750,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
# Clear visual fixture: two already existing generated group members, standard species profiles.
# Configure updates their runtime habitat only. Nothing is spawned or persisted into the map.
visual=[a for a in actors if str(a.visual_species.get_internal_id())=='Bisasam'and '_Group_'in str(a.encounter_id)];assert len(visual)==2
for i,a in enumerate(visual):
 m=a.overworld_movement;m.set_movement_paused(True);a.set_actor_location(unreal.Vector(-360+i*220,2100,38),False,True)
 body=a.get_component_by_class(unreal.CapsuleComponent)
 assert not m.get_editor_property('override_activities') and not m.get_editor_property('override_behavior')
 m.set_editor_property('habitat_radius_override',180.)
 m.configure(a.visual_species,body.get_scaled_capsule_half_height(),body.get_scaled_capsule_radius(),body.get_scaled_capsule_half_height(),None,4831+i*137)
cmd('pm.EnvPerf2.Viewport 2560 1440')
s={'last':unreal.GameplayStatics.get_time_seconds(W),'t':0.,'sample':0.,'wall':time.monotonic(),'recording':False,'observed':False,'post':0.,'viewwait':0.}
result={'ordinary_pie':True,'profiles':'unmodified species defaults','diagnostic_player_position':[-250,2750,50.15],'creature_positions_modified':True,'visual_fixture':'Only two existing generated Bisasam relocated to an existing clearing during PIE; 180 cm runtime visual habitat, no profile/state forcing, no saved map changes','samples':[]}
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
