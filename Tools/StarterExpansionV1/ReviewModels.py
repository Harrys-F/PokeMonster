"""Actual starter meshes in existing ClassicBattle/WorldBattle, plus existing save/load."""
import unreal,json,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/StarterExpansionV1/ModelReviewRequest.json').read_text())['label'];assert label.isalnum();O=R/'Saved/StarterExpansionV1'/label;assert O.exists()and not(O/'Result.json').exists();w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w)
def sub(cls):return next(x for x in unreal.ObjectIterator(cls)if x.get_outer()==gi)
e=sub(unreal.PokeMonsterEncounterSubsystem);save=sub(unreal.PokeMonsterSaveSubsystem);slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False);cases=[('classic','Schiggy','Bisasam'),('classic','Bisasam','Schiggy'),('world','Schiggy','Bisasam'),('world','Bisasam','Schiggy')];s={'case':0,'phase':'start','time':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[]}
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def phase(v):s.update(phase=v,time=0.)
def shot(v):n='Starter_'+label+'_'+str(s['case'])+'_'+v;cmd('pm.CreatureReview.CaptureLiveUI '+n);s['rows'][-1].setdefault('screenshots',[]).append(n)
def party():return [{'species':str(c.species),'id':c.instance_id.to_string(),'hp':c.current_hp,'xp':c.experience}for c in e.get_player_party()]
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._starter_models);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);s.update(passed=error is None,error=error,save_after_sha256=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('STARTER_MODEL_REVIEW_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<300
  mode,a,b=cases[s['case']]
  if s['phase']=='start'and s['time']>1:
   assert not e.is_encounter_active();s['wild_positions']={str(a.encounter_id):a.get_actor_location().to_tuple()for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor)};s['rows'].append({'mode':mode,'player':a,'opponent':b,'position_before':p.get_actor_location().to_tuple(),'camera_before':pc.player_camera_manager.get_camera_location().to_tuple()});cmd('pm.StarterReview.Start '+mode+' '+a+' '+b);assert e.is_encounter_active();phase('warm')
  elif s['phase']=='warm'and s['time']>4:
   assert all(a.get_actor_location().distance(unreal.Vector(*s['wild_positions'][str(a.encounter_id)]))<.01 for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor));comp=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterCreatureCompanionSubsystem)if x.get_outer()==w);assert not comp.get_visual() or comp.get_visual().get_editor_property('hidden');s['rows'][-1]['overworld_pause_verified']=True;v=e.get_presenter().get_view();ui=e.get_battle_widget();assert ui.is_classic_presentation()==(mode=='classic');s['rows'][-1]['move_names']=[str(m.name)for m in v.moves];slot=next(i for i,m in enumerate(v.moves)if str(m.name)in ['Aquaknarre','Rankenhieb']);shot('Commands');ui.set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);shot('Moves');cmd('pm.BattleV3.Click move '+str(slot));assert e.get_presenter().get_view().busy;phase('attack')
  elif s['phase']=='attack':
   if not e.is_encounter_active():phase('ended');return
   v=e.get_presenter().get_view()
   if s['time']>.8 and not s.get('shot_attack'):shot('Attack');s['shot_attack']=True
   if not v.busy:assert v.round>=1;phase('flee')
  elif s['phase']=='flee'and s['time']>.5:
   if not e.is_encounter_active():phase('ended');return
   v=e.get_presenter().get_view()
   if not v.busy:
    if not v.finished:assert e.get_presenter().try_select_flee();assert e.get_presenter().resolve_selection();s['time']=0
  elif s['phase']=='ended'and not p.is_overworld_input_locked()and s['time']>1:
   assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);assert p.get_actor_location().distance(unreal.Vector(*s['rows'][-1]['position_before']))<5
   before=party();assert save.save_current_game();assert save.load_game();assert party()==before;s['rows'][-1]['save_reload_equal']=True;s['rows'][-1]['outcome']=str(e.get_last_result().outcome);s['case']+=1;s['shot_attack']=False
   if s['case']==len(cases):finish();return
   phase('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
unreal._starter_models=unreal.register_slate_post_tick_callback(tick)
