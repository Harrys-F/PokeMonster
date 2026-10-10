"""Controlled PIE save/load check, outside battle. Original disk save must be backed up first.
No player teleport; central existing SaveSubsystem performs both operations.
"""
import unreal,json
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();O=R/'Saved/WestlandRegion'
assert (O/'BeforeTour_Dev.sav').exists(),'Back up existing Dev save before this test'
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w and 'Dev_WestlandRegion' in w.get_name()
g=unreal.GameplayStatics.get_game_instance(w)
def subsystem(cls):return next(o for o in unreal.ObjectIterator(cls) if o.get_outer()==g)
e=subsystem(unreal.PokeMonsterEncounterSubsystem);i=subsystem(unreal.PokeMonsterInventorySubsystem);s=subsystem(unreal.PokeMonsterSaveSubsystem);p=unreal.GameplayStatics.get_player_pawn(w,0)
assert not e.is_encounter_active() and not p.is_overworld_input_locked()
def team():return [{'level':c.level,'HP':c.current_hp,'XP':c.experience,'PP':[(m.current_pp,m.max_pp) for m in c.move_slots]} for c in e.get_player_party()]
def inventory():return [(str(x.item),x.quantity) for x in i.get_stacks()]
# Public runtime API only. A normal test battle changes HP/PP, then LoadGame restores.
trainers=list(e.get_defeated_trainer_ids());e.restore_defeated_trainer_ids(trainers+['WestlandRegion_SaveTestTrainer'])
before={'team':team(),'inventory':inventory(),'trainers':[str(n) for n in e.get_defeated_trainer_ids()]};assert before['team'];position=p.get_actor_location();assert s.save_current_game()
assert e.start_test_encounter(p,None)
start=unreal.GameplayStatics.get_time_seconds(w);busy=False
def tick(dt):
 global busy
 if busy:return
 busy=True
 try:
  assert unreal.GameplayStatics.get_time_seconds(w)-start<120
  if e.is_encounter_active():
   v=e.get_presenter().get_view()
   if not v.busy and not v.presentation_pending and not v.finished:
    if v.must_switch:
     j=next(j for j,t in enumerate(v.player_team) if t.can_switch);e.get_battle_widget().call_method('Team'+str(j))
    else:
     j=1 if v.moves[1].enabled else next(j for j,m in enumerate(v.moves) if m.enabled);e.get_battle_widget().call_method('Move'+str(j))
  else:
   assert team()!=before['team'],'Battle did not change persistent HP/PP';assert i.restore_stacks([]);e.restore_defeated_trainer_ids([]);assert not i.get_stacks();assert s.load_game()
   after={'team':team(),'inventory':inventory(),'trainers':[str(n) for n in e.get_defeated_trainer_ids()]};assert before==after;assert p.get_actor_location()==position;assert not p.is_overworld_input_locked();e.restore_defeated_trainer_ids(trainers)
   (O/'SaveRoundTrip.json').write_text(json.dumps({'passed':True,'before':before,'after':after,'player_position_unchanged':True,'mutation':'Normal BattleSession/UMG round changes persistent HP/PP; inventory/trainer lists cleared via existing public APIs'},indent=2));unreal.log('REGION_SAVE_ROUNDTRIP_PASS');unreal.unregister_slate_post_tick_callback(unreal._wr_save);del unreal._wr_save
 except Exception as ex:
  unreal.unregister_slate_post_tick_callback(unreal._wr_save);del unreal._wr_save;unreal.log_error('REGION_SAVE_ROUNDTRIP_FAIL '+repr(ex))
 busy=False
unreal._wr_save=unreal.register_slate_post_tick_callback(tick)
