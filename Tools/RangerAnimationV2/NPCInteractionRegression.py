"""Real Enhanced Input collision/dialogue/fallback check; source NPC is never moved."""
import unreal,json,math,traceback,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Art/Characters/NPCs/Ranger/Review/AnimationV2';w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name()=='Dev_TestMap_NPCMotionV2'
p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);v=next(x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterNPCVisualActor) if x.source_actor.get_class().get_name()=='PokeMonsterNPC');src=v.source_actor;before=(src.get_actor_location().to_tuple(),src.get_actor_rotation().to_tuple(),src.get_actor_scale3d().to_tuple());caps=src.get_component_by_class(unreal.CapsuleComponent);pr=p.get_component_by_class(unreal.CapsuleComponent);minimum=caps.get_scaled_capsule_radius()+pr.get_scaled_capsule_radius();sprite=src.get_component_by_class(unreal.PaperSpriteComponent)
sub=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem) if x.get_world()==w);move=next(x for x in unreal.ObjectIterator(unreal.InputAction) if x.get_outer()==p and x.get_name()=='MoveAction');gi=unreal.GameplayStatics.get_game_instance(w);dialog=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterDialogueSubsystem) if x.get_outer()==gi)
stage='approach';t=0.;total=0.;data=[];locked_position=None;lastpage=0.;savehash=hashlib.sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest()
unreal.SystemLibrary.execute_console_command(w,'pm.NPCMotion2.Viewport 2560 1440')
def inject(dx,dy):
 yaw=math.radians(p.get_movement_basis_yaw());sub.inject_input_vector_for_action(move,unreal.Vector(-math.sin(yaw)*dx+math.cos(yaw)*dy,math.cos(yaw)*dx+math.sin(yaw)*dy,0),[],[])
def finish(error=None):
 inject(0,0);v.set_editor_property('bUseVisual',True);v.refresh_presentation();unreal.unregister_slate_post_tick_callback(unreal._npcmotion2_interaction);del unreal._npcmotion2_interaction
 (O/'Data/NPCInteractionRegression.json').write_text(json.dumps({'error':error,'passed':error is None,'steps':data,'source_transform_preserved':(src.get_actor_location().to_tuple(),src.get_actor_rotation().to_tuple(),src.get_actor_scale3d().to_tuple())==before,'capsule_radius_sum_cm':minimum,'save_unchanged':hashlib.sha256((R/'Saved/SaveGames/PokeMonster_Dev.sav').read_bytes()).hexdigest()==savehash,'method':'Real Enhanced Input walking/bumping, no test teleports','physical_controller_tested':False},indent=2))
def nextstage(name,extra=None):
 global stage,t
 data.append({'stage':stage,'position':p.get_actor_location().to_tuple(),**(extra or {})});stage=name;t=0.
def tick(dt):
 global t,total,locked_position,lastpage
 try:
  t+=dt;total+=dt;assert total<45;assert (src.get_actor_location().to_tuple(),src.get_actor_rotation().to_tuple(),src.get_actor_scale3d().to_tuple())==before
  q=p.get_actor_location();s=src.get_actor_location();distance=math.hypot(q.x-s.x,q.y-s.y)
  if stage=='approach':
   dx=-835-q.x;dy=-1080-q.y;d=math.hypot(dx,dy)
   if d<12:inject(0,0);nextstage('bump');return
   inject(dx/max(d,1),dy/max(d,1))
  elif stage in ['bump','fallback_bump']:
   inject((s.x-q.x)/max(distance,1),(s.y-q.y)/max(distance,1))
   if t>1.1:
    assert minimum-.8<=distance<minimum+6,(minimum,distance);inject(0,0)
    if stage=='bump':nextstage('interact',{'blocked_distance_cm':distance})
    else:nextstage('restore',{'fallback_collision_still_blocks_cm':distance})
  elif stage=='interact':
   inject(0,0)
   if t>.3:assert p.try_interact();assert dialog.is_dialogue_active();locked_position=q;nextstage('talk')
  elif stage=='talk':
   inject(-1,0);assert p.is_overworld_input_locked();assert (q-locked_position).length()<1
   if t>.8:
    an=v.visual.get_anim_instance();assert an.conversation_alpha>.95 and v.is_conversing();unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+str(O/'Unreal/Final_Conversation.png')+'"',pc);inject(0,0);nextstage('advance',{'talk_alpha':an.conversation_alpha,'input_lock_blocks_movement':True})
  elif stage=='advance':
   inject(0,0)
   if not dialog.is_dialogue_active():nextstage('idle');return
   if t-lastpage>.65:dialog.advance_dialogue();lastpage=t
  elif stage=='idle':
   if t>.8:
    assert v.visual.get_anim_instance().conversation_alpha<.01 and not v.is_conversing();v.set_editor_property('bUseVisual',False);v.refresh_presentation();assert sprite.is_visible() and not v.visual.is_visible();nextstage('fallback_bump',{'talk_to_idle':True,'sprite_fallback':True})
  elif stage=='restore':
   v.set_editor_property('bUseVisual',True);v.refresh_presentation();assert not sprite.is_visible() and v.visual.is_visible();assert v.visual.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;nextstage('complete',{'3d_restored':True,'no_extra_collision':True})
  else:finish()
 except Exception:finish(traceback.format_exc())
unreal._npcmotion2_interaction=unreal.register_slate_post_tick_callback(tick)
