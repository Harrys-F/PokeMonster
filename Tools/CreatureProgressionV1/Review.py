"""Actual existing-map PIE / UMG checks; explicit runtime fixtures, no save writes."""
import unreal,json,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();request=json.loads((R/'Saved/CreatureProgressionV1/ReviewRequest.json').read_text());label=request['label'];assert label.isalnum();O=R/'Saved/CreatureProgressionV1'/label;O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_TestMap_VisualV2' in w.get_name()
pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(s for s in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if s.get_outer()==gi)
# Isolate only this PIE fixture, not the saved map or the production habitat logic.
for actor in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 if actor.get_class().get_name()=='PokeMonsterVisibleWildCreatureActor':actor.destroy_actor()
 if actor.get_class().get_name()=='PokeMonsterWildEncounterZone':actor.set_actor_enable_collision(False)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';save_before=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
last_percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage');cases=[('classic','replace','accept'),('classic','replace','decline'),('world','replace','accept'),('world','replace','decline'),('classic','free','auto'),('classic','evolution','blocked')]
s={'phase':'start','case':0,'t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall_start':time.monotonic(),'rows':[],'shots':[]}
def cmd(x):unreal.SystemLibrary.execute_console_command(w,x,pc)
def shot(name):
 capture=label+'_'+str(s['case'])+'_'+name;cmd('pm.CreatureReview.CaptureLiveUI '+capture);path=R/'Saved/GlumandaV11/LiveUI'/capture/'ActualSlateViewport.png';s['shots'].append(str(path))
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._progression_v1_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);cmd('pm.EnvPerf2.Viewport 0 0');cmd('r.ScreenPercentage '+str(last_percentage));after=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
 if after!=save_before:error=(error or '')+' Developer save unexpectedly changed'
 s.update(passed=error is None,error=error,save_before=save_before,save_after=after);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('PROGRESSION_PIE_DONE '+str(error))
def advance(phase):s.update(phase=phase,t=0.)
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall_start']<500,'PIE review timeout'
  mode,kind,action=cases[s['case']]
  if s['phase']=='start' and s['t']>1:
   if p.is_overworld_input_locked():return
   row=dict(mode=mode,kind=kind,action=action,position_before=p.get_actor_location().to_tuple());s['rows'].append(row)
   cmd('pm.ProgressionV1.Start '+mode+' '+kind);assert enc.is_encounter_active();advance('ready')
  elif s['phase']=='ready'and s['t']>2:
   assert pc.get_viewport_size()==(2560,1440);pr=enc.get_presenter();v=pr.get_view();row=s['rows'][-1];row['before']=dict(level=v.player.level,hp=v.player.current_hp,max_hp=v.player.max_hp,moves=[str(m.name)for m in v.moves]);row['round_before']=v.round
   ui=enc.get_battle_widget();ui.set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);shot('Before');cmd('pm.Input.Key Enter tap');advance('resolving')
  elif s['phase']=='resolving':
   row=s['rows'][-1]
   if not enc.is_encounter_active():
    assert kind!='replace','Closed before the learn decision';advance('ended');return
   pr=enc.get_presenter();v=pr.get_view()
   if v.round>row['round_before'] and not row.get('events'):
    row['events']=[dict(type=str(e.type),xp=e.experience_added,before=e.level_before,after=e.level_after,text=str(e.information))for e in pr.get_last_result().events]
    assert any('EXPERIENCE_GAINED'in e['type'] for e in row['events']);assert any('LEVEL_UP'in e['type'] for e in row['events']);shot('LevelUp')
   if v.learning_move:
    assert kind=='replace';assert not v.finished and not v.busy;assert v.learning_team_index==0;row['prompt']=str(v.learning_prompt);row['offered_moves']=[str(m.name)for m in v.moves];assert 'Aquaknarre' in row['prompt'];shot('Learning');advance('choose')
  elif s['phase']=='choose'and s['t']>1:
   v=enc.get_presenter().get_view();assert v.learning_move
   # The real existing B/A mapping and D-pad path, not a direct model mutation.
   if action=='accept':cmd('pm.Input.Key Gamepad_DPad_Right tap');cmd('pm.Input.Key Gamepad_FaceButton_Right tap')
   else:cmd('pm.Input.Key Gamepad_FaceButton_Bottom tap')
   advance('chosen')
  elif s['phase']=='chosen'and s['t']>.3:
   if enc.is_encounter_active():assert not enc.get_presenter().get_view().learning_move
   shot('Decision');advance('wait_end')
  elif s['phase']=='wait_end':
   if not enc.is_encounter_active() and not p.is_overworld_input_locked():advance('ended')
  elif s['phase']=='ended'and s['t']>.8:
   row=s['rows'][-1];end=enc.get_last_result();assert end.outcome==unreal.PokeMonsterEncounterOutcome.VICTORY;team=enc.get_player_party();assert len(team)==1
   c=team[0];row['after']=dict(id=c.instance_id.to_string(),level=c.level,xp=c.experience,hp=c.current_hp,max_hp=c.calculated_stats.max_hp,pending=len(c.pending_moves));assert c.level>row['before']['level'];assert not c.pending_moves
   row['moves_after']=[str(x.get_editor_property('move').get_editor_property('internal_id'))if x.get_editor_property('move') else ''for x in c.get_editor_property('move_slots')]
   if kind=='replace':assert ('WaterGun'in row['moves_after'])==(action=='accept')
   elif kind=='free':assert 'Ember'in row['moves_after']
   elif kind=='evolution':assert any('EVOLUTION_PENDING'in e['type']for e in row['events'])
   assert (p.get_actor_location()-unreal.Vector(*row['position_before'])).length()<.1
   s['case']+=1
   if s['case']==len(cases):finish();return
   advance('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');unreal._progression_v1_review=unreal.register_slate_post_tick_callback(tick)
