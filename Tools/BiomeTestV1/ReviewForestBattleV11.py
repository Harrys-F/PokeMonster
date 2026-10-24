"""Real existing Classic/WorldBattle in the active local camera area, using protected RAM preview."""
import unreal,json,sys,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(R/'Tools/BiomeTestV1'));import Layout as L
req=json.loads((R/'Saved/BiomeTestV11/ForestBattleRequest.json').read_text());O=R/'Saved/BiomeTestV11'/req['label'];O.mkdir(exist_ok=False);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and w.get_name().endswith('Dev_BiomeTestMap_V1');p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);mode=unreal.GameplayStatics.get_game_mode(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);save=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==gi);arm=p.get_component_by_class(unreal.SpringArmComponent);vis=p.get_component_by_class(unreal.PokeMonsterCameraVisibilityComponent);original=p.get_actor_location();slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest();assert mode.begin_isolated_gameplay_review()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
s={'i':0,'phase':'position','last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'rows':[],'paused_frames':0,'max_arm_delta_cm':0.};cases=['classic','world']
def cmd(c):unreal.SystemLibrary.execute_console_command(w,c,pc)
def phase(v):s.update(phase=v,time=0.)
def party():return[(c.instance_id.to_string(),c.current_hp,c.experience,c.level,[(m.get_editor_property('move').get_path_name()if m.get_editor_property('move')else None,m.get_editor_property('current_pp'))for m in c.get_editor_property('move_slots')],[(m.get_editor_property('move').get_path_name(),m.get_editor_property('current_pp'))for m in c.get_editor_property('learned_moves')])for c in e.get_player_party()]
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._biome_forest_battle);settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
 (O/'Result.json').write_text(json.dumps({'passed':error is None,'error':error,'fixture':'Explicit player photograph positioning and native battle parties in existing RAM save protection; not natural encounters or a footwalk','rows':s['rows'],'battle_pause_frames':s['paused_frames'],'max_arm_delta_during_battle_cm':s['max_arm_delta_cm'],'save_before':before,'save_after':hashlib.sha256(slot.read_bytes()).hexdigest(),'RAM_active':mode.is_isolated_gameplay_review()},indent=2))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<180;assert hashlib.sha256(slot.read_bytes()).hexdigest()==before
  if e.is_encounter_active():s['paused_frames']+=1;s['max_arm_delta_cm']=max(s['max_arm_delta_cm'],abs(arm.target_arm_length-1700));assert abs(arm.target_arm_length-1700)<.01 and vis.dense_canopy_amount==1
  if s['phase']=='position':
   p.set_actor_location(unreal.Vector(*L.world(3200,-1800,L.height(3200,-1800)+p.get_component_by_class(unreal.CapsuleComponent).get_scaled_capsule_half_height()+2)),False,True);phase('begin')
  elif s['phase']=='begin'and s['time']>3:
   if s['i']>=len(cases):
    assert mode.end_isolated_gameplay_review();p.set_actor_location(original,False,True);phase('restore');return
   assert arm.target_arm_length==1700 and vis.dense_canopy_amount==1;cmd('pm.StarterReview.Party Habitak Zunderlauf');cmd('pm.StarterReview.Start '+cases[s['i']]+' Habitak Zunderlauf');assert e.is_encounter_active();phase('attack')
  elif s['phase']=='attack'and s['time']>3:
   v=e.get_presenter().get_view();assert not v.finished;idx=next(i for i,m in enumerate(v.moves)if m.enabled);cmd('pm.CreatureReview.CaptureLiveUI BiomeV11_'+req['label']+'_'+cases[s['i']]);assert e.get_presenter().try_select_move(idx)and e.get_presenter().resolve_selection();phase('finish_battle')
  elif s['phase']=='finish_battle'and s['time']>2:
   if e.is_encounter_active():
    v=e.get_presenter().get_view()
    if not v.busy and not v.finished:assert e.get_presenter().try_select_flee()and e.get_presenter().resolve_selection();s['time']=0
   elif not p.is_overworld_input_locked():
    old_party=party();assert save.save_current_game()and save.load_game()and party()==old_party;s['rows'].append({'mode':cases[s['i']],'actual_attack':True,'outcome':str(e.get_last_result().outcome),'camera_after_cm':arm.target_arm_length,'RAM_save_reload_AP_identity_equal':True});s['i']+=1;phase('begin')
  elif s['phase']=='restore'and s['time']>3:
   assert arm.target_arm_length==2850 and vis.dense_canopy_amount==0 and vis.get_dense_canopy_faded_tree_count()==0;assert not save.save_current_game()and not save.load_game();assert s['paused_frames']>10;finish()
 except Exception:finish(traceback.format_exc())
unreal._biome_forest_battle=unreal.register_slate_post_tick_callback(tick)
