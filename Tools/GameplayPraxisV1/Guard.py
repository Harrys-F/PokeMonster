"""Existing RAM-save transport only. No disk slot moves, copies, restores, or writes."""
import unreal,json,hashlib,time,traceback
from pathlib import Path
R=Path(unreal.Paths.project_dir()).resolve();D=R/'Saved/ProjectRefinement/GameplayPraxisV1';req=json.loads((D/'Request.json').read_text());O=D/req['label'];W=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert W and W.get_name().endswith('Dev_TestMap_VisualV2')
P=unreal.GameplayStatics.get_player_pawn(W,0);PC=unreal.GameplayStatics.get_player_controller(W,0);GI=unreal.GameplayStatics.get_game_instance(W);G=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterNPCTestGround)if x.get_outer()==W);S=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterSaveSubsystem)if x.get_outer()==GI);Enc=next(x for x in unreal.ObjectIterator(unreal.PokeMonsterEncounterSubsystem)if x.get_outer()==GI)
slot=R/'Saved/SaveGames/PokeMonster_Dev.sav';sha=hashlib.sha256(slot.read_bytes()).hexdigest();party=[c.export_text()for c in Enc.get_player_party()];pos=P.get_actor_transform();assert not Enc.is_encounter_active()and not PC.is_menu_open()
# Visit reuses the already existing test-ground transport; no NPC/asset/map is created by this adapter.
assert G.visit(0);P.set_actor_transform(pos,False,True);P.get_component_by_class(unreal.CharacterMovementComponent).stop_movement_immediately()
unreal._praxis_guard={'party':party,'sha256':sha,'ground':G,'world':W,'output':O};started=time.monotonic()
def settled_guard(dt):
 try:
  assert time.monotonic()-started<8,'PIE movement did not settle after guarded return'
  if P.get_component_by_class(unreal.CharacterMovementComponent).is_falling():return
  assert S.save_current_game()and S.load_game();assert hashlib.sha256(slot.read_bytes()).hexdigest()==sha
  (O/'Guard.json').write_text(json.dumps({'ram_transport':'existing NPCTestGround.Visit, original transform restoration and actual grounded tick','disk_save_sha256':sha,'initial_party':party,'guard_roundtrip_disk_unchanged':True,'original_position':pos.translation.to_tuple(),'simulated_input_not_hardware':True},indent=2))
 except Exception:(O/'GuardFailure.json').write_text(json.dumps({'error':traceback.format_exc()}))
 unreal.unregister_slate_post_tick_callback(unreal._praxis_settled_guard)
unreal._praxis_settled_guard=unreal.register_slate_post_tick_callback(settled_guard)
