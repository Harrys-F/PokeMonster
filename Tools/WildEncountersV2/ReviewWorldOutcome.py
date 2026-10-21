"""Existing WorldBattle with a real visible source and controlled one-HP opponent.
Verifies the new Classic-only defeat escape never leaks into special WorldBattle.
"""
import unreal,json,time,hashlib,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();label=json.loads((R/'Saved/WildEncountersV2/WorldOutcomeRequest.json').read_text())['label'];O=R/'Saved/WildEncountersV2'/label;assert not(O/'Result.json').exists();O.mkdir(exist_ok=True);w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w;p=unreal.GameplayStatics.get_player_pawn(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0);gi=unreal.GameplayStatics.get_game_instance(w);e=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==gi);wild=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.PokeMonsterVisibleWildCreatureActor);a=next(x for x in wild if 'Schiggy'in str(x.visual_species))
for x in wild:x.overworld_movement.set_movement_paused(True)
unreal.SystemLibrary.execute_console_command(w,'pm.StarterReview.Party Bisasam Zunderlauf Schiggy',pc);own,reserve,opponent=e.get_player_party();opponent.current_hp=1;p.set_actor_location(a.get_actor_location()+unreal.Vector(150,0,20.15),False,True)
d=unreal.PokeMonsterEncounterStartData(presentation_mode=unreal.PokeMonsterBattlePresentationMode.WORLD_BATTLE,encounter_id=a.encounter_id,kind=unreal.PokeMonsterEncounterKind.WILD,source=unreal.PokeMonsterEncounterSource.VISIBLE_CREATURE,player_team=[own,reserve],opponent_team=[opponent],random_seed=51,allow_flee=True,source_actor=a);assert e.start_encounter(d,p);s={'last':unreal.GameplayStatics.get_time_seconds(w),'time':0.,'wall':time.monotonic(),'fixture':'Explicit WorldBattle start, real visible source, 1HP opponent','moves':[]}
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(unreal._wild_world_outcome);settings.set_editor_property('bThrottleCPUWhenNotForeground',old);s.update(passed=error is None,error=error);(O/'Result.json').write_text(json.dumps(s,indent=2));unreal.log('WILD_WORLD_OUTCOME_DONE '+str(error))
def tick(dt):
 try:
  now=unreal.GameplayStatics.get_time_seconds(w);s['time']+=now-s['last'];s['last']=now;assert time.monotonic()-s['wall']<90
  if e.is_encounter_active():
   assert not e.get_battle_widget().is_classic_presentation();pr=e.get_presenter();v=pr.get_view()
   if not v.busy and not v.finished:
    names=[str(x.name)for x in v.moves];i=names.index('Rankenhieb');s['moves'].append(names[i]);assert pr.try_select_move(i);assert pr.resolve_selection()
  else:
   result=e.get_last_result();assert result.outcome==unreal.PokeMonsterEncounterOutcome.VICTORY;assert result.presentation_mode==unreal.PokeMonsterBattlePresentationMode.WORLD_BATTLE;assert result.source_actor==a;assert a.life_state==unreal.PokeMonsterWildLifeState.REMOVED;assert not a.overworld_movement.escaping_defeat;assert not p.is_overworld_input_locked();s['world_result_mode_preserved']=True;s['no_classic_escape']=True;finish()
 except Exception:finish(traceback.format_exc())
unreal._wild_world_outcome=unreal.register_slate_post_tick_callback(tick)
