"""Actual load of controlled legacy/bad/blocked/cross-world isolated snapshots."""
from pathlib import Path
import unreal,json,time,traceback,hashlib,math
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/SaveSystemV2';q=json.loads((D/'Request.json').read_text());O=D/q['label'];Editor=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
W=Editor.get_game_world();GI=unreal.GameplayStatics.get_game_instance(W)
def sub(c):return next(x for x in unreal.ObjectIterator(c)if x.get_outer()==GI)
S=sub(unreal.PokeMonsterSaveSubsystem);E=sub(unreal.PokeMonsterEncounterSubsystem);C=sub(unreal.PokeMonsterCheckpointSubsystem);assert S.use_isolated_pie_test_slot(q['slot']);slot=R/'Saved/SaveGames'/(q['slot']+'.sav');assert not slot.exists();original=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(original.read_bytes()).hexdigest()
def refs():
 w=Editor.get_game_world()
 if not w:return None,None,None
 pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0)if pc else None
 return w,pc,p
W,PC,P=refs();oldworld=W.get_path_name();party=[c.export_text()for c in E.get_player_party()];start=P.get_actor_location().to_tuple()
for a in unreal.GameplayStatics.get_all_actors_of_class(W,unreal.PokeMonsterVisibleWildCreatureActor):a.overworld_movement.set_movement_paused(True);a.set_actor_enable_collision(False)
unreal.SystemLibrary.execute_console_command(W,'pm.SaveV2Review.Fixture '+q['case'],PC);assert slot.exists(),'Fixture did not write its guarded test slot'
beforesha=hashlib.sha256(slot.read_bytes()).hexdigest();result={'case':q['case'],'checks':[],'source_world':oldworld,'original_save_unchanged':True,'isolated_slot':q['slot']};s={'stage':0,'time':0.,'wall':time.monotonic(),'phase':'load','first_load_checked':False}
def key(k):
 w,pc,p=refs()
 for edge in ['down','up']:unreal.SystemLibrary.execute_console_command(w,'pm.Input.Key '+k+' '+edge,pc)
backend=unreal.SystemLibrary.get_console_variable_int_value('Slate.MacControllerPreferGCImpl');B='Gamepad_FaceButton_Right'if backend else'Gamepad_FaceButton_Bottom'
keys=['Gamepad_Special_Right','Gamepad_DPad_Down','Gamepad_DPad_Down','Gamepad_DPad_Down',B,B]
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._save_v2_edges)
 try:
  w,pc,p=refs();mode=unreal.GameplayStatics.get_game_mode(S);sp=unreal.GameplayStatics.get_player_pawn(S,0)
  result['diagnostics']={'last_storage_message':S.get_last_storage_message(),'last_outcome':str(E.get_last_result().outcome),'recovery_saved':C.was_last_recovery_saved(),'encounter_active':E.is_encounter_active(),'returning':C.is_returning_from_defeat()if hasattr(C,'is_returning_from_defeat')else None,'world':w.get_path_name()if w else None,'subsystem_player':sp.get_path_name()if sp else None,'player':p.get_path_name()if p else None,'falling':p.get_component_by_class(unreal.CharacterMovementComponent).is_falling()if p else None,'on_ground':p.get_component_by_class(unreal.CharacterMovementComponent).is_moving_on_ground()if p else None,'game_mode':mode.get_class().get_name()if mode else None,'persistent_allowed':mode.get_editor_property('bEnablePersistentGameplay')if mode else None,'evolution_phase':pc.get_evolution_widget().get_phase()if pc and pc.get_evolution_widget()else None,'recovery_exists':S.has_recovery_game()}
 except Exception as detail:result['diagnostics_error']=str(detail)
 result.update(passed=error is None,error=error,original_save_unchanged=hashlib.sha256(original.read_bytes()).hexdigest()==sha);(O/'Result.json').write_text(json.dumps(result,indent=2))
def tick(dt):
 try:
  assert time.monotonic()-s['wall']<100,'Edge review timeout';s['time']+=dt
  if s['phase']=='fight':
   w,pc,p=refs()
   if E.is_encounter_active():
    pr=E.get_presenter();v=pr.get_view()
    if not v.busy and not v.finished:assert pr.try_select_move(0);assert pr.resolve_selection()
    return
   if not p or p.is_overworld_input_locked()or C.is_returning_from_defeat():return
   assert E.get_last_result().outcome==unreal.PokeMonsterEncounterOutcome.DEFEAT and C.was_last_recovery_saved()
   assert w.get_name()=='Dev_TestMap_VisualV2'and math.dist(p.get_actor_location().to_tuple(),start)<1
   assert all(c.current_hp==c.calculated_stats.max_hp for c in E.get_player_party())
   assert hashlib.sha256(slot.read_bytes()).hexdigest()==beforesha
   result['checks'].append('Defeat returns across maps or from unavailable checkpoint to a safe current-world start; manual slot unchanged')
   if q['case']=='crossmap':
    s.update(phase='load',stage=0,time=0.);return
   result.update(position=p.get_actor_location().to_tuple(),destination_world=w.get_path_name());finish();return
  if s['stage']<len(keys):
   if s['time']>.45:key(keys[s['stage']]);s['stage']+=1;s['time']=0
   return
  w,pc,p=refs()
  if not p or S.is_load_in_progress()or s['time']<2:return
  if q['case']=='crossmap':
   assert w.get_name()=='Dev_TestMap',w.get_path_name();assert math.dist(p.get_actor_location().to_tuple(),(-1000,-1100,50.15))<1
   assert math.dist(p.get_interaction_world_direction().to_tuple(),(math.cos(math.radians(123)),math.sin(math.radians(123)),0.))<.001
   assert str(C.get_active_checkpoint().map_package)=='/Game/Maps/Dev_TestMap_VisualV2'
   result['checks'].append('Actual OpenLevel restored target map, exact pose/facing, old-map checkpoint and existing team')
  else:
   assert w.get_name()=='Dev_TestMap_VisualV2'
   if q['case']!='blocked':assert math.dist(p.get_actor_location().to_tuple(),start)<1
   result['checks'].append('Legacy/missing/invalid/blocked position uses validated safe fallback without losing party')
  assert[c.export_text()for c in E.get_player_party()]==party
  assert not pc.is_menu_open()and not p.is_overworld_input_locked()
  assert hashlib.sha256(slot.read_bytes()).hexdigest()==beforesha,'Load must not rewrite/migrate the slot'
  result.update(destination_world=w.get_path_name(),position=p.get_actor_location().to_tuple(),message=S.get_last_storage_message(),no_load_write=True)
  result['checks'].extend(['Existing individual data exact','Menu/input restored','No slot rewrite on load'])
  if q['case']in['crossmap','missing-checkpoint']and not s['first_load_checked']:
   s.update(first_load_checked=True,phase='fight',time=0.)
   unreal.SystemLibrary.execute_console_command(w,'pm.BattleV3.Start classic defeat',pc);assert E.is_encounter_active();return
  unreal.SystemLibrary.execute_console_command(w,'HighResShot 2560x1440 filename="'+str(O/'Loaded.png')+'"',pc)
  finish()
 except Exception:finish(traceback.format_exc())
unreal._save_v2_edges=unreal.register_slate_post_tick_callback(tick)
