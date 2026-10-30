"""Normal shore interaction, actual Garados capture and isolated menu save/load in existing PIE."""
import unreal,time,json,traceback,math
from pathlib import Path
D=(Path(unreal.Paths.project_dir())/'Saved/ProjectRefinement/GaradosWaterV2').resolve();W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();PC=unreal.GameplayStatics.get_player_controller(W,0);P=unreal.GameplayStatics.get_player_pawn(W,0);GI=unreal.GameplayStatics.get_game_instance(W)
def sub(t,o=GI):return next(x for x in unreal.ObjectIterator(t)if x.get_outer()==o)
E=sub(unreal.PokeMonsterEncounterSubsystem);I=sub(unreal.PokeMonsterInventorySubsystem);S=sub(unreal.PokeMonsterSaveSubsystem);C=sub(unreal.PokeMonsterWorldClock);H=sub(unreal.PokeMonsterHabitatSubsystem,W);A=next(a for a in H.population if str(a.visual_species.get_internal_id())=='Garados');s={'start':time.monotonic(),'phase':'init','at':0,'done':False};r={'checks':[],'shore':[]};old=P.get_actor_location();identity=str(A.encounter_id);before=[x.export_text()for x in E.get_player_party()];original_ids=[x.instance_id.to_string()for x in E.get_player_party()];assert Path(unreal.Paths.project_saved_dir()).resolve().is_relative_to(D)
def finish(error=None):
 if s['done']:return
 s['done']=True;unreal.unregister_slate_post_tick_callback(unreal._garados_pie_gameplay);r.update(passed=error is None,error=error,seconds=time.monotonic()-s['start']);(D/'PIEGameplay02.json').write_text(json.dumps(r,indent=2,default=str))
def tick(dt):
 try:
  now=time.monotonic();assert now-s['start']<80
  if s['phase']=='init':
   assert not E.is_encounter_active()and not P.is_overworld_input_locked()
   candidates=[]
   for x,y in [(720,-1100),(1620,-1800),(720,-2500),(-180,-1800),(1300,-1200)]:
    P.set_actor_location(unreal.Vector(x,y,50.15),False,True);ok=A.can_interact(P);r['shore'].append({'player':[x,y,50.15],'can_interact':ok})
    if ok:candidates.append((x,y))
   assert candidates,'Long water Pokemon cannot be challenged from the real shore'
   x,y=candidates[0];P.set_actor_location(unreal.Vector(x,y,50.15),False,True);s.update(phase='aim',at=now);return
  if s['phase']=='aim':
   inputs=next(x for x in unreal.ObjectIterator(unreal.EnhancedInputLocalPlayerSubsystem)if 'LocalPlayer'in x.get_outer().get_class().get_name());move=next(x for x in unreal.ObjectIterator(unreal.InputAction)if x.get_outer()==P and x.get_name()=='MoveAction');d=A.get_actor_location()-P.get_actor_location();length=max(1,math.hypot(d.x,d.y));yaw=math.radians(P.get_movement_basis_yaw());inputs.inject_input_vector_for_action(move,unreal.Vector((-math.sin(yaw)*d.x+math.cos(yaw)*d.y)/length,(math.cos(yaw)*d.x+math.sin(yaw)*d.y)/length,0)if now-s['at']<.18 else unreal.Vector(),[],[])
   if now-s['at']<.18:return
   P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately();assert I.add_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'),1);assert P.try_interact(),'Normal player focus did not select the shore encounter';s.update(phase='battle',at=now);return
  if s['phase']=='battle':
   if now-s['at']<3:return
   assert E.is_encounter_active()and C.is_clock_paused();scene=unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterClassicBattleScene)[0];expected=unreal.load_asset('/Game/Characters/Creatures/Garados/MeshyV1/Meshes/SK_Garados_Meshy');assert scene.opponent_visual.mesh.get_skeletal_mesh_asset()==expected and not scene.opponent_visual.using_swim_mesh;r['checks'].append('Normal shore focus starts real ClassicBattle; wild opponent uses preserved original Garados battle rig');pr=E.get_presenter();view=pr.get_view()
   if view.busy or view.presentation_pending:return
   assert pr.try_select_capture_item(unreal.load_asset('/Game/Data/Items/DA_MasterBall'));assert pr.resolve_selection();s.update(phase='capture',at=now);return
  if s['phase']=='capture':
   if now-s['at']<6 or E.is_encounter_active():return
   team=list(E.get_player_party());assert len(team)==len(original_ids)+1 and E.is_encounter_completed(unreal.Name(identity));assert [x.instance_id.to_string()for x in team[:len(original_ids)]]==original_ids;assert str(team[-1].species.get_internal_id())=='Garados'and team[-1].instance_id.to_string()not in original_ids;r['checks'].append('Regular MasterBall capture adds a distinct Garados; existing Garados and other party identities preserved');PC.toggle_main_menu();assert PC.is_menu_open()and C.is_clock_paused();assert S.save_current_game(),S.get_last_storage_message();s['saved']=[x.export_text()for x in team];s['position']=P.get_actor_location().to_tuple();s['time']=C.get_time().export_text();assert S.load_game(),S.get_last_storage_message();s.update(phase='load',at=now);return
  if s['phase']=='load':
   if now-s['at']<3 or S.is_load_in_progress():return
   assert [x.export_text()for x in E.get_player_party()]==s['saved'];assert (P.get_actor_location()-unreal.Vector(*s['position'])).length()<.1;assert C.get_time().export_text()==s['time']and C.is_clock_paused();assert PC.close_menu();r['checks'].append('Existing menu save/load restores exact party fields, position and paused world time in own isolated PIE slot');P.set_actor_location(old,False,True);finish()
 except Exception:finish(traceback.format_exc())
unreal._garados_pie_gameplay=unreal.register_slate_post_tick_callback(tick)
