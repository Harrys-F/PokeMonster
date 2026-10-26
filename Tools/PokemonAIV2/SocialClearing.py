"""Clearly labeled PIE-only visibility fixture: two existing Bisasam moved to an
existing open meadow; original map and saved encounter positions are never written.
The native roaming component chooses, approaches, observes and releases its peer.
"""
import unreal,json,time,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/PokemonAIV2';label=json.loads((D/'ReviewRequest.json').read_text())['label'];O=D/label;O.mkdir(exist_ok=False)
W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W;P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W);PC=unreal.GameplayStatics.get_player_controller(W,0)
S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);assert S.use_isolated_pie_test_slot('PokeMonster_SaveV2_Test_PokemonAI'+label);user=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(user.read_bytes()).hexdigest()
actors=list(unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor));group=[a for a in actors if str(a.visual_species.get_internal_id())=='Bisasam' and '_Group_' in str(a.encounter_id)][:2];assert len(group)==2
result={'fixture':'Two existing Bisasam, transient relocated positions on existing open VisualV2 meadow, social-only profile, native AI and camera. No permanent actor or map changes.','originals':[a.get_actor_transform().export_text()for a in group],'samples':[],'shots':[]};s={'time':0.,'last':unreal.GameplayStatics.get_time_seconds(W),'wall':time.monotonic(),'sample':0.,'shot':False,'done':None}
def cmd(t):unreal.SystemLibrary.execute_console_command(W,t,PC)
for i,a in enumerate(group):
 m=a.overworld_movement;m.set_movement_paused(True);a.set_actor_location(unreal.Vector(-450+400*i,2100,38),False,True)
 cfg=m.activities;cfg.wander_weight=.001;cfg.observe_weight=cfg.rest_weight=cfg.sleep_weight=cfg.forage_weight=0;cfg.social_weight=100;m.set_editor_property('override_activities',True);m.set_editor_property('activity_override',cfg)
 b=m.get_behavior_profile();b.temperament=unreal.PokeMonsterOverworldTemperament.CALM;m.set_editor_property('override_behavior',True);m.set_editor_property('behavior_override',b)
 a.set_actor_rotation(unreal.Rotator(yaw=0 if i==0 else 180),False);body=a.get_component_by_class(unreal.CapsuleComponent);m.set_editor_property('habitat_radius_override',650.);m.configure(a.visual_species,38,body.get_scaled_capsule_radius(),38,None,4831+137*i);m.set_movement_paused(True)
P.set_actor_location(unreal.Vector(-250,2600,50.15),False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();cmd('pm.EnvPerf2.Viewport 2560 1440');clip=R/'Saved/VisualV2TAAIntegrationV1/Recordings'/('PokemonAIV2'+label);assert not clip.exists();cmd('pm.TAAReview.CaptureStart '+str(clip))
def shot(n):cmd('HighResShot 2560x1440 filename="'+str(O/(n+'.png'))+'"');result['shots'].append(n)
def finish(error=None):
 cmd('pm.TAAReview.CaptureStop');unreal.unregister_slate_post_tick_callback(unreal._pokemon_ai_social_clear);result.update(passed=error is None,error=error,user_save_unchanged=hashlib.sha256(user.read_bytes()).hexdigest()==before,clip=str(clip.relative_to(R)));assert result['user_save_unchanged'];(O/'Result.json').write_text(json.dumps(result,indent=2));unreal.log('POKEMON_AI_SOCIAL_CLEAR_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(W);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<100 and s['time']<50
  if s['time']<2:return
  if not s.get('armed'):
   for a in group:a.overworld_movement.set_movement_paused(False)
   s['armed']=True;return
  if now-s['sample']>.2:
   s['sample']=now;result['samples'].append({'time':now,'actors':[{'last_social':str(a.overworld_movement.last_social_decision),'queries':a.overworld_movement.peer_queries,'traces':a.overworld_movement.perception_traces,'enabled':a.overworld_movement.activities_enabled,'decisions':a.overworld_movement.activity_decisions,'plans':a.overworld_movement.successful_plans,'profile':a.overworld_movement.activities.export_text(),'position':a.get_actor_location().to_tuple(),'state':str(a.overworld_movement.behavior_state),'partner':a.overworld_movement.social_partner.get_owner().get_name()if a.overworld_movement.social_partner else None,'completed':a.overworld_movement.social_completed,'speed':a.overworld_movement.current_speed}for a in group]})
  if any(a.overworld_movement.social_partner for a in group)and not s['shot']:shot('SocialApproach');s['shot']=True
  if s['shot']and not any(a.overworld_movement.is_activity_travelling()for a in group)and not s.get('dwell'):shot('SocialObserve');s['dwell']=True
  if any(a.overworld_movement.social_completed for a in group)and s['done']is None:shot('SocialCompleted');s['done']=s['time']
  if s['done']is not None and s['time']-s['done']>3:finish()
 except Exception:finish(traceback.format_exc());raise
unreal._pokemon_ai_social_clear=unreal.register_slate_post_tick_callback(tick)
