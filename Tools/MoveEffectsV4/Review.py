"""Explicit unsaved PIE fixtures through the existing encounter, renderer, UMG and key handling.
No production move definitions, assets, maps or save slots are changed.
"""
import unreal,json,time,hashlib
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/MoveEffectsV4/ReviewRequest.json').read_text())['label'];assert label.isalnum();O=R/'Saved/MoveEffectsV4'/label;O.mkdir(exist_ok=False)
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_TestMap_VisualV2'in w.get_name();pc=unreal.GameplayStatics.get_player_controller(w,0);p=unreal.GameplayStatics.get_player_pawn(w,0);gi=unreal.GameplayStatics.get_game_instance(w);enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi)
# Technical encounter fixtures only: avoid ambient encounters during the scripted review.
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor):a.destroy_actor()
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterWildEncounterZone):a.set_actor_enable_collision(False)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';before=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
percentage=unreal.SystemLibrary.get_console_variable_float_value('r.ScreenPercentage')
names=['Zunderlauf','Schiggy','Bisasam','Pikachu','Myrapla','Enton','Machomei','Nebulak','Gengar','Glurak'];effects=['stages','status','heal','drain','recoil','multi','confusion','protect','screen','multi'];cases=[(mode,name,effects[i])for mode in ['classic','world']for i,name in enumerate(names)]
expected={'stages':'STAT_CHANGED','status':'STATUS_APPLIED','heal':'HEALED','drain':'HEALED','recoil':'RECOIL','multi':'HIT_COUNT','confusion':'CONFUSED','protect':'PROTECTED','screen':'PROTECTED'}
s={'case':0,'phase':'start','t':0.,'last':unreal.GameplayStatics.get_time_seconds(w),'wall':time.monotonic(),'rows':[],'shots':[],'technical_fixture':True}
def cmd(t):unreal.SystemLibrary.execute_console_command(w,t,pc)
def phase(v):s.update(phase=v,t=0.)
def shot(v):
 n='EffectsV4'+label+str(s['case'])+v;cmd('pm.CreatureReview.CaptureLiveUI '+n);s['shots'].append(str(R/'Saved/GlumandaV11/LiveUI'/n/'ActualSlateViewport.png'))
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._effects_v4_review);settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle);cmd('pm.EnvPerf2.Viewport 0 0');cmd('r.ScreenPercentage '+str(percentage));after=hashlib.sha256(slot.read_bytes()).hexdigest()if slot.exists()else None
 if after!=before:error=(error or '')+' Developer save changed'
 s.update(passed=error is None,error=error,save_before=before,save_after=after);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('MOVE_EFFECTS_V4_PIE_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['t']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<700,'Review timeout';mode,name,effect=cases[s['case']]
  if s['phase']=='start'and s['t']>1:
   assert not enc.is_encounter_active();s['rows'].append(dict(mode=mode,species=name,technical_effect=effect,position_before=p.get_actor_location().to_tuple()));cmd('pm.MoveEffectsV4.Start '+mode+' '+effect+' '+name);assert enc.is_encounter_active();phase('ready')
  elif s['phase']=='ready'and s['t']>2:
   assert pc.get_viewport_size()==(2560,1440);v=enc.get_presenter().get_view();assert not v.busy;ui=enc.get_battle_widget();assert ui.is_classic_presentation()==(mode=='classic');ui.set_battle_menu(unreal.PokeMonsterBattleMenu.MOVES);shot('Before');s['rows'][-1]['pp_before']=v.moves[0].current_pp;cmd('pm.Input.Key Gamepad_FaceButton_Right tap');phase('attack')
  elif s['phase']=='attack':
   assert enc.is_encounter_active();pr=enc.get_presenter();v=pr.get_view()
   if v.round>=1 and not v.busy:
    result=pr.get_last_result();events=[dict(type=str(e.type),source=str(e.source),target=str(e.target),hp_before=e.hp_before,hp_after=e.hp_after,pp_before=e.pp_before,pp_after=e.pp_after,text=str(e.information))for e in result.events];assert any(expected[effect]in e['type']and 'PokeMonsterBattleSide.A' in e['source']for e in events),(effect,events)
    row=s['rows'][-1];row['events']=events;row['pp_after']=v.moves[0].current_pp;assert row['pp_after']==row['pp_before']-1
    if effect=='status':assert str(v.opponent.status_label)=='PAR'
    shot('After');phase('flee')
  elif s['phase']=='flee'and s['t']>1:
   pr=enc.get_presenter();assert pr.try_select_flee();assert pr.resolve_selection();phase('ended')
  elif s['phase']=='ended'and not enc.is_encounter_active()and not p.is_overworld_input_locked():
   assert p.get_actor_location().distance(unreal.Vector(*s['rows'][-1]['position_before']))<.1;assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterClassicBattleScene);s['rows'][-1]['returned']=True;s['case']+=1
   (O/'Progress.json').write_text(json.dumps(dict(completed=s['case'],total=len(cases))))
   if s['case']==len(cases):finish();return
   phase('start')
 except Exception:
  import traceback
  finish(traceback.format_exc())
cmd('pm.EnvPerf2.Viewport 2560 1440');cmd('r.ScreenPercentage 100');unreal._effects_v4_review=unreal.register_slate_post_tick_callback(tick)
